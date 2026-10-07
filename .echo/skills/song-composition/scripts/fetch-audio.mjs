#!/usr/bin/env node

/**
 * 📥 song-composition / fetch-audio.mjs
 * =====================================================================
 * Holt die fertigen Takes zu einem Suno-Task ab: beide MP3s und beide Cover,
 * mit Größenprüfung und Retry. Das Gegenstück zum bekannten 0,44-MB-Abbruch:
 * ein Take unter 2 MB gilt als unvollständig und wird erneut geladen.
 *
 * Nutzung:
 *   node fetch-audio.mjs --task-id <id> --title "Meine Echo" [--out-dir songs]
 *   node fetch-audio.mjs --status <status.json> --title "Meine Echo" [--out-dir songs]
 *
 * Suno-Cover werden NICHT geladen (Standard) — die Cover entstehen über die
 * Pollinations-Route (deliver.mjs, ein Bild pro Song). Für den Ausnahmefall: --suno-covers.
 *
 * Läuft in zwei Stufen, weil Suno erst liefert, wenn der Task SUCCESS ist:
 *   1) ohne Treffer  → Exit 3 (noch nicht fertig), Aufrufer pollt weiter
 *   2) mit Treffern  → Download, Exit 0
 */

import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const SUNO_CLIENT = path.join(process.cwd(), '.echo', 'skills', 'suno-client', 'scripts', 'suno-client.mjs');

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
const taskId = typeof flags['task-id'] === 'string' ? flags['task-id'] : null;
const statusPath = typeof flags.status === 'string' ? flags.status : null;
const title = typeof flags.title === 'string' ? flags.title : 'Echo_Song';
const outDir = typeof flags['out-dir'] === 'string' ? flags['out-dir'] : 'songs';
const minBytes = flags['min-bytes'] ? Number(flags['min-bytes']) : 2_000_000;

if (!taskId && !statusPath) {
  console.error('❌ Nutzung: node fetch-audio.mjs --task-id <id> --title "Titel" [--out-dir songs] | --status <status.json> --title "Titel"');
  process.exit(1);
}

/** Liest den Status entweder aus der Datei oder frisch aus dem suno-client. */
function loadStatus() {
  if (statusPath) {
    const raw = fs.readFileSync(statusPath, 'utf-8');
    const json = raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1);
    return { text: raw, json: safeParse(json) };
  }
  const raw = execFileSync(process.execPath, [SUNO_CLIENT, 'status', taskId, '--type', 'music'], {
    encoding: 'utf-8',
    maxBuffer: 32 * 1024 * 1024,
  });
  const json = raw.slice(raw.indexOf('{'), raw.lastIndexOf('}') + 1);
  return { text: raw, json: safeParse(json) };
}

function safeParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}

/** Sammelt alle Objekte mit audioUrl — unabhängig davon, wie tief Suno sie verschachtelt. */
function collectAudioObjects(node, found = []) {
  if (Array.isArray(node)) {
    for (const item of node) collectAudioObjects(item, found);
  } else if (node && typeof node === 'object') {
    if (typeof node.audioUrl === 'string') found.push(node);
    for (const value of Object.values(node)) collectAudioObjects(value, found);
  }
  return found;
}

const { text: statusText, json: statusJson } = loadStatus();
const statusMatch = /"status"\s*:\s*"([A-Z_]+)"/.exec(statusText);
const status = statusMatch ? statusMatch[1] : 'UNKNOWN';

if (status !== 'SUCCESS') {
  console.log(`⏳ Status ${status} — noch keine fertigen Takes.`);
  process.exit(3);
}

const takes = statusJson ? collectAudioObjects(statusJson) : [];
if (takes.length === 0) {
  console.log('⏳ Status SUCCESS, aber keine audioUrl gefunden — Status-JSON prüfen.');
  process.exit(3);
}

fs.mkdirSync(outDir, { recursive: true });

async function download(url, target, expectAudio) {
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const buffer = Buffer.from(await res.arrayBuffer());
      if (expectAudio && buffer.length < minBytes) throw new Error(`nur ${buffer.length} Bytes (unvollständig)`);
      fs.writeFileSync(target, buffer);
      return buffer.length;
    } catch (error) {
      if (attempt === 3) return { error: error.message };
      await new Promise((resolve) => setTimeout(resolve, 4000));
    }
  }
  return { error: 'unerreichbar' };
}

let index = 0;
let failures = 0;
for (const take of takes) {
  index += 1;
  const suffix = `V${index}`;
  const audioTarget = path.join(outDir, `${title}_${suffix}.mp3`);
  const result = await download(take.audioUrl, audioTarget, true);
  if (typeof result === 'number') {
    console.log(`✅ ${path.basename(audioTarget)} — ${(result / 1024 / 1024).toFixed(2)} MB${take.duration ? ` · ${take.duration}s` : ''}`);
  } else {
    failures += 1;
    console.log(`❌ ${path.basename(audioTarget)} — ${result.error}`);
  }

  if (typeof take.imageUrl === 'string' && flags['suno-covers']) {
    const coverTarget = path.join(outDir, `${title}_${suffix}.jpg`);
    const coverResult = await download(take.imageUrl, coverTarget, false);
    if (typeof coverResult === 'number') console.log(`🖼️ ${path.basename(coverTarget)} — ${(coverResult / 1024).toFixed(1)} KB`);
  }
}

console.log(failures === 0 ? `🎉 ${index} Takes vollständig in ${outDir}/` : `⚠️ ${failures} von ${index} Takes unvollständig — erneut laufen lassen.`);
process.exit(failures === 0 ? 0 : 1);
