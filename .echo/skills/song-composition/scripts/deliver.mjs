#!/usr/bin/env node

/**
 * 📦 song-composition / deliver.mjs
 * =====================================================================
 * Der letzte Schritt jedes Song-Laufs — die Ablage-Konvention an EINER Stelle:
 *
 *   songs/<Songname>_1.mp3        Variante 1
 *   songs/<Songname>_2.mp3        Variante 2
 *   songs/<Songname>.jpg          EIN eigenes Cover (Pollinations/flux) für beide Varianten
 *   songs/lyrics_archive/<Songname>.md
 *                                 Überschrift + Cover + Lyrics + Stil + Negativ
 *
 * Suno-Cover werden ignoriert (nicht runterladen, nicht kopieren).
 * tmp/ wird danach geleert, außer --keep-tmp.
 *
 * Nutzung:
 *   node deliver.mjs --title "Krallen & Beton" --tmp tmp/song-run \
 *     --lyrics <datei> --style <datei> --negative <datei> --cover-prompt "<bildprompt>" \
 *     [--cover-model flux] [--cover-ext jpg] [--songs songs] [--archive songs/lyrics_archive]
 *     [--keep-tmp] [--no-cover]
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const POLLINATIONS_CLIENT = path.join(process.cwd(), '.echo', 'skills', 'pollinations-client', 'scripts', 'pollinations-client.mjs');

function parseFlags(argv) {
  const flags = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      flags[key] = next === undefined || next.startsWith('--') ? true : (i++, next);
    } else {
      flags._.push(token);
    }
  }
  return flags;
}

const flags = parseFlags(process.argv.slice(2));
const title = typeof flags.title === 'string' ? flags.title : null;
const tmpDir = typeof flags.tmp === 'string' ? flags.tmp : null;

if (!title || !tmpDir) {
  console.error('❌ Nutzung: node deliver.mjs --title "<Songname>" --tmp <tmp-ordner> --lyrics <datei> [--style <datei>] [--negative <datei>] [--cover-prompt "..."]');
  process.exit(1);
}
if (!fs.existsSync(tmpDir)) {
  console.error(`❌ tmp-Ordner nicht gefunden: ${tmpDir}`);
  process.exit(1);
}

const songsDir = typeof flags.songs === 'string' ? flags.songs : 'songs';
const archiveDir = typeof flags.archive === 'string' ? flags.archive : path.join('songs', 'lyrics_archive');
const fileBase = title.replace(/\s+/g, '_').replace(/[\\/:*?"<>|]/g, '');
fs.mkdirSync(songsDir, { recursive: true });
fs.mkdirSync(archiveDir, { recursive: true });

// ── 1. Takes einsammeln und auf <Songname>_1.mp3 / _2.mp3 bringen ──
const audio = fs
  .readdirSync(tmpDir)
  .filter((name) => /\.mp3$/i.test(name) && !name.startsWith('.'))
  .sort();

if (audio.length === 0) {
  console.error(`❌ Keine MP3s in ${tmpDir} — erst fetch-audio.mjs laufen lassen.`);
  process.exit(1);
}

const moved = [];
audio.forEach((name, index) => {
  const target = path.join(songsDir, `${fileBase}_${index + 1}.mp3`);
  fs.renameSync(path.join(tmpDir, name), target);
  moved.push({ from: name, to: target, size: fs.statSync(target).size });
});

// Suno-Cover, falls doch irgendwo gelandet, konsequent wegräumen
for (const name of fs.readdirSync(tmpDir)) {
  if (/\.(jpg|jpeg|webp)$/i.test(name)) {
    fs.rmSync(path.join(tmpDir, name), { force: true });
    console.log(`🧹 Suno-Cover entfernt: ${name}`);
  }
}

console.log(`🎵 ${moved.length} Take(s) abgelegt:`);
for (const item of moved) console.log(`   ▸ ${item.to} — ${(item.size / 1024 / 1024).toFixed(2)} MB`);

// ── 2. EIN Cover über Pollinations/flux ──
const readIf = (value) => (typeof value === 'string' && fs.existsSync(value) ? fs.readFileSync(value, 'utf-8').trim() : '');
const lyrics = readIf(flags.lyrics);
const style = readIf(flags.style);
const negative = readIf(flags.negative);

// Cover-Endung: Pollinations/flux liefert JPEG — also .jpg, kein Umetikettieren.
const coverExt = typeof flags['cover-ext'] === 'string' ? flags['cover-ext'].replace(/^\./, '') : 'jpg';
const coverFile = path.join(songsDir, `${fileBase}.${coverExt}`);

if (!flags['no-cover']) {
  const coverPrompt =
    typeof flags['cover-prompt'] === 'string' && flags['cover-prompt'].trim()
      ? flags['cover-prompt'].trim()
      : `${title}, dark cinematic album cover, ${style || 'industrial electronic'}, no text, no letters, no watermark, moody, high contrast, square artwork`;

  const coverArgs = [
    POLLINATIONS_CLIENT,
    'image',
    '--prompt', coverPrompt,
    '--model', typeof flags['cover-model'] === 'string' ? flags['cover-model'] : 'flux',
    '--width', '1024',
    '--height', '1024',
    '--outFile', coverFile,
  ];

  try {
    const output = execFileSync(process.execPath, coverArgs, { encoding: 'utf-8', maxBuffer: 16 * 1024 * 1024 });
    const line = output.split(/\r?\n/).find((entry) => entry.includes('gespeichert')) || output.trim().split(/\r?\n/).pop();
    console.log(`🖼️ Cover: ${line.trim()}`);
  } catch (error) {
    console.error(`⚠️ Cover-Generierung fehlgeschlagen: ${error.message.split('\n')[0]}`);
  }
}

// ── 3. <Songname>.md neben den alten Lyrics ──
const mdTarget = path.join(archiveDir, `${fileBase}.md`);
const relativeCover = `../${path.basename(coverFile)}`;
const md = [
  `# ${title}`,
  '',
  fs.existsSync(coverFile) ? `![${title}](${relativeCover})` : '_Cover fehlt_',
  '',
  '## Lyrics',
  '',
  '```text',
  lyrics || '_Lyrics fehlen_',
  '```',
  '',
  '## Style',
  '',
  '```text',
  style || '_Stil fehlt_',
  '```',
  '',
  '## Negativ',
  '',
  '```text',
  negative || '_Negativ fehlt_',
  '```',
  '',
].join('\n');

fs.writeFileSync(mdTarget, md, 'utf-8');
console.log(`📄 ${mdTarget} (${md.length} Zeichen)`);

// ── 4. tmp/ leeren ──
if (!flags['keep-tmp']) {
  for (const entry of fs.readdirSync(tmpDir)) {
    fs.rmSync(path.join(tmpDir, entry), { recursive: true, force: true });
  }
  fs.rmdirSync(tmpDir, { force: true });
  console.log(`🧽 ${tmpDir} geleert.`);
} else {
  console.log(`ℹ️ tmp behalten: ${tmpDir}`);
}

console.log('✅ Run abgeschlossen.');
