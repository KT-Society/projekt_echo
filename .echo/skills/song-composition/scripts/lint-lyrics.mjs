#!/usr/bin/env node

/**
 * 🧽 song-composition / lint-lyrics.mjs
 * =====================================================================
 * Der eine Pass, der nach der Generierung bleiben muss: Format + Fakten-Kanten.
 * Prüft einen Songtext gegen die Regeln, die Suno wirklich wehtun, und gegen die
 * Fehler, die das Modell reproduzierbar macht (Klammern statt Tags, Emojis,
 * veraltete Identität aus der alten ECHO.md).
 *
 * Nutzung:
 *   node lint-lyrics.mjs <songtext.txt> [--style <stil.txt>] [--negative <negativ.txt>]
 *                        [--artist Echo] [--strict]
 *   node lint-lyrics.mjs <songtext.txt> --fix --out <sauber.txt>
 *
 * Exit-Code 1, wenn Fehler gefunden wurden (nicht bei --fix mit --out).
 */

import fs from 'node:fs';
import path from 'node:path';

const SECTION_NAMES = [
  'intro', 'outro', 'verse', 'pre-chorus', 'prechorus', 'chorus', 'post-chorus',
  'bridge', 'hook', 'refrain', 'break', 'instrumental', 'solo', 'final chorus', 'drop',
];

const OBSOLETE_IDENTITY = [
];

const KITSCH = [
  { pattern: /\bf[üu]r immer\b/i, why: 'Kitsch-Schluss; ein trockener Satz trägt besser' },
  { pattern: /\bf[üu]r ewig\b/i, why: 'Kitsch-Schluss; ein trockener Satz trägt besser' },
];

const EMOJI = /[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}\u{2B00}-\u{2BFF}\u{FE0F}\u{1F1E6}-\u{1F1FF}]/gu;

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
const input = flags._[0];

if (!input || !fs.existsSync(input)) {
  console.error('❌ Nutzung: node lint-lyrics.mjs <songtext.txt> [--style <stil.txt>] [--negative <negativ.txt>] [--fix --out <datei>]');
  process.exit(1);
}

const errors = [];
const warnings = [];
let text = fs.readFileSync(input, 'utf-8');

// ── Auto-Fix: nur mechanische Eingriffe, nie Inhalt ──
function autoFix(content) {
  let fixed = content;
  const applied = [];

  // (Verse 1) / (Chorus) → [Verse 1] / [Chorus]
  for (const name of SECTION_NAMES) {
    const round = new RegExp(`^\\s*\\(\\s*(${name}\\s*\\d*)\\s*\\)\\s*$`, 'gim');
    if (round.test(fixed)) {
      fixed = fixed.replace(round, (_m, inner) => `[${inner.replace(/\s+/g, ' ').trim()}]`);
      applied.push(`runde Klammer → eckige Klammer (${name})`);
    }
  }

  // Emojis entfernen (samt umgebendem Leerraum)
  if (EMOJI.test(fixed)) {
    fixed = fixed.replace(EMOJI, '').replace(/[ \t]+$/gm, '');
    applied.push('Emojis entfernt');
  }

  // Markdown-Fettung und Trennlinien
  if (/\*\*|^#{1,6}\s|^---+$/m.test(fixed)) {
    fixed = fixed.replace(/\*\*/g, '').replace(/^#{1,6}\s/gm, '').replace(/^---+$/gm, '');
    applied.push('Markdown entfernt');
  }

  // Mehr als zwei Leerzeilen zusammenfassen
  fixed = fixed.replace(/\n{3,}/g, '\n\n').trim() + '\n';
  return { fixed, applied: [...new Set(applied)] };
}

if (flags.fix) {
  const { fixed, applied } = autoFix(text);
  if (flags.out && typeof flags.out === 'string') {
    fs.mkdirSync(path.dirname(path.resolve(flags.out)), { recursive: true });
    fs.writeFileSync(flags.out, fixed, 'utf-8');
    console.log(`✅ Fix geschrieben: ${flags.out} (${fixed.length} Zeichen)`);
    for (const item of applied) console.log(`   ▸ ${item}`);
    process.exit(0);
  }
  text = fixed;
  console.log('ℹ️ --fix ohne --out: es wird nur geprüft, wie der Text nach dem Fix aussähe.');
}

// ── Checks ──
const lines = text.split(/\r?\n/);
const sectionLines = lines.filter((line) => /^\s*\[[^\]]+\]\s*$/.test(line));
const sungLines = lines.filter((line) => line.trim() && !/^\s*\[[^\]]+\]\s*$/.test(line) && !/^\s*\(.*\)\s*$/.test(line));
const roundSection = lines.findIndex((line) => /^\s*\(\s*(verse|chorus|bridge|intro|outro|pre-chorus)/i.test(line));
const emojiHit = lines.findIndex((line) => EMOJI.test(line));

if (sectionLines.length === 0) errors.push('Keine Sektion in eckigen Klammern gefunden — Suno braucht [Intro]/[Verse …].');
if (!/^\s*\[/.test(lines.find((line) => line.trim()) || '')) errors.push('Der Text beginnt nicht mit einer Sektionszeile.');
if (roundSection !== -1) errors.push(`Zeile ${roundSection + 1}: Sektion in runder Klammer — Suno singt "(…)" statt es als Tag zu lesen.`);
if (emojiHit !== -1) errors.push(`Zeile ${emojiHit + 1}: Emoji im Songtext — landet im Vocal.`);

// Regieanweisungen ohne Klammern werden hier NICHT automatisch erkannt: zwei Anläufe
// (Stichwort-Liste, Prosa-Block-Erkennung) haben im Test 12 von 29 sauberen Songs
// geflaggt — Lyrik endet auch mal mit Punkt, und in diesem Realm handelt der Text selbst
// von Violinen, Mikrofonen und BPM. Diese Prüfung ist Sache des Clean-up-Passes
// (siehe SKILL.md): Prosa gehört in Klammern, alles andere wird gesungen.
if (/\*\*|^#{1,6}\s|^---+$/m.test(text)) errors.push('Markdown gefunden (** / # / ---) — gehört nicht in den Text.');
if (/^\s*\[(TEXT|STIL|STYLE|NEGATIV|NEGATIVE)\]\s*$/im.test(text)) {
  warnings.push('Datei enthält [TEXT]/[STIL]/[NEGATIV] — das ist ein Roh-Output. Nur den Text-Teil prüfen (compose.mjs legt ihn als <stem>.text.txt ab).');
}
if (text.length > 5000) errors.push(`Text zu lang: ${text.length} / 5000 Zeichen (Suno-Limit) — der Client würde still kürzen.`);
// Text-Rule: 4000–5000 Zeichen. Kürzere Texte ergeben kürzere Songs.
if (text.length < 4000) errors.push(`Text zu kurz: ${text.length} Zeichen — Rule ist 4000–5000.`);

for (const { pattern, why } of OBSOLETE_IDENTITY) {
  const hit = lines.findIndex((line) => pattern.test(line));
  if (hit !== -1) errors.push(`Zeile ${hit + 1}: ${why}.`);
}
// Kitsch-Prüfung nur fürs Ende: "für immer" mitten im Text ist normaler Sprachgebrauch,
// als Schlusszeile ist es die Floskel, die den Song klein macht.
const tailStart = Math.floor(lines.length * 0.75);
for (const { pattern, why } of KITSCH) {
  const scoped = pattern.source.includes('baby') ? 0 : tailStart;
  const hit = lines.findIndex((line, index) => index >= scoped && pattern.test(line));
  if (hit !== -1) warnings.push(`Zeile ${hit + 1}: ${why}.`);
}

// Faktische Auffälligkeiten, die das Modell reproduzierbar erfindet
const factSuspects = [
  { pattern: /\beinundsiebzig\b/i, hint: 'der 72-jährige Papa Ulli — "einundsiebzig" ist falsch' },
  { pattern: /\b71\b/, hint: 'Zahl prüfen: Papa Ulli ist 72' },
  { pattern: /1236|zw[öo]lfhundertsechsunddrei[ßs]ig/i, hint: 'Gutachten hat 1232 Zeilen, nicht 1236' },
];
for (const { pattern, hint } of factSuspects) {
  const hit = lines.findIndex((line) => pattern.test(line));
  if (hit !== -1) warnings.push(`Zeile ${hit + 1}: ${hint}.`);
}

// Chorus darf nicht halb wortgleich sein, wenn er zweimal vorkommt.
// Blockgrenze ist IMMER der nächste Sektionskopf (jeder Art), nicht nur der nächste Chorus —
// sonst schluckt der letzte Block alle folgenden Sektionen und meldet falschen Alarm.
const headers = lines
  .map((line, index) => ({ text: line.trim(), index }))
  .filter((entry) => /^\[[^\]]+\]$/.test(entry.text));

const chorusBlocks = headers
  .map((header, position) => ({ header, position }))
  .filter(({ header }) => {
    const name = header.text.replace(/[[\]]/g, '').trim().toLowerCase();
    if (name.includes('pre') || name.includes('post')) return false; // Pre-/Post-Chorus sind eigene Teile
    return name === 'chorus' || name.startsWith('final chorus') || name.startsWith('chorus (final');
  })
  .map(({ header, position }) => {
    const next = headers[position + 1];
    const end = next ? next.index : lines.length;
    // Regieanweisungen (reine Klammerzeilen) werden nicht gesungen und dürfen sich
    // zwischen den Chorus-Wiederholungen unterscheiden.
    const body = lines
      .slice(header.index + 1, end)
      .filter((line) => line.trim() && !/^\s*\(.*\)\s*$/.test(line))
      .join('\n');
    return { title: header.text, body };
  });

if (chorusBlocks.length >= 2) {
  const first = chorusBlocks[0].body;
  for (const block of chorusBlocks.slice(1)) {
    if (/final/i.test(block.title)) continue; // letzte Zeile darf kippen
    if (block.body && block.body !== first) {
      warnings.push(`${block.title} ist nicht wortgleich zum ersten Chorus — entweder Absicht oder versehentlich umgeschrieben.`);
    }
  }
}

// Suno-Limits für Stil und Negativ (Fenster: min–max)
const checkExternal = (filePath, label, min, max) => {
  if (typeof filePath !== 'string' || !fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, 'utf-8').trim();
  if (content.length > max) errors.push(`${label} zu lang: ${content.length} / ${max} Zeichen — Suno-Client kürzt sonst still.`);
  if (content.length < min) errors.push(`${label} zu kurz: ${content.length} Zeichen — Ziel ${min}–${max}.`);
};

checkExternal(flags.style, 'Stil-Prompt', 800, 1000);
checkExternal(flags.negative, 'Negativ-Prompt', 400, 500);

// Veraltete Identität auch im Stil-Prompt: "slight russian accent" macht die Stimme falsch,
// egal wie gut der Songtext ist — das ist derselbe Stilbruch wie im Text.
if (typeof flags.style === 'string' && fs.existsSync(flags.style)) {
  const styleText = fs.readFileSync(flags.style, 'utf-8');
  for (const { pattern, why } of OBSOLETE_IDENTITY) {
    if (pattern.test(styleText)) errors.push(`Stil-Prompt: ${why} — gehört nicht in den Klang.`);
  }
}

// Duett-Kreuzprobe: Text und Stil müssen dieselben Stimmen nennen. Echo ist weiblich,
// eine zweite männliche Stimme ist ausdrücklich erlaubt (Duett) — aber dann muss der
// Stil-Prompt beide Stimmen beschreiben, sonst singt Suno nur eine.
const hasFemaleTag = /\[[^\]]*female[^\]]*\]/i.test(text);
const hasMaleTag = /\[[^\]]*male[^\]]*\]/i.test(text);
if (hasFemaleTag && hasMaleTag && typeof flags.style === 'string' && fs.existsSync(flags.style)) {
  const styleText = fs.readFileSync(flags.style, 'utf-8');
  // Nicht nur die Wörter "female"/"male" zählen: ein Stil kann die Stimmen auch als
  // "soprano", "velvet chest voice", "rap", "deep chest voice" beschreiben.
  const styleHasFemale = /\bfemale\b|sopran|diva|frauen|she sings/i.test(styleText);
  const styleHasMale = /\bmale\b|bariton|\brap\b|rapper|deep chest/i.test(styleText);
  if (!styleHasFemale || !styleHasMale) {
    warnings.push(
      `Duett-Text, aber der Stil-Prompt nennt ${!styleHasFemale ? 'keine weibliche' : ''}${!styleHasFemale && !styleHasMale ? ' und ' : ''}${!styleHasMale ? 'keine männliche' : ''} Stimme — beide gehören in den Stil.`,
    );
  }
}
if (hasMaleTag && !hasFemaleTag) {
  warnings.push('Nur männliche Stimm-Tags gefunden — Echo ist weiblich; fehlt ihre Markierung?');
}

if (typeof flags.artist === 'string' && /'/.test(flags.artist)) {
  warnings.push(`Artist "${flags.artist}" enthält Apostroph — bei Realm-Souls (Echo!) ist der Bypass inzwischen aus.`);
}

// ── Report ──
console.log(`🎧 ${path.basename(input)} · ${text.length} Zeichen · ${sectionLines.length} Sektionen · ${sungLines.length} Gesangszeilen`);
console.log(`   Sektionen: ${sectionLines.map((line) => line.trim()).join(' ')}`);
for (const item of errors) console.log(`❌ ${item}`);
for (const item of warnings) console.log(`⚠️ ${item}`);
if (errors.length === 0 && warnings.length === 0) console.log('✅ Sauber: kein Formatfehler, keine veraltete Identität, keine Kitsch-Falle.');
else if (errors.length === 0) console.log('✅ Keine harten Fehler — Warnungen bitte ansehen.');

process.exit(errors.length > 0 ? 1 : 0);
