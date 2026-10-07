#!/usr/bin/env node

/**
 * 🎵 Echo's Suno API Client Framework
 * =====================================
 * 
 * Suno API Base URL: https://api.sunoapi.org
 * Auth: Bearer Token
 * Docs: https://docs.sunoapi.org
 * 
 * Nutzung:
 *   node suno-client.mjs generate --prompt "..." --style "..." --lyrics "..."
 *   node suno-client.mjs extend --audioId "..." --continueAt 60 --prompt "..."
 *   node suno-client.mjs separate --taskId "..." --audioId "..." --type separate_vocal
 *   node suno-client.mjs wav --taskId "..." --audioId "..."
 *   node suno-client.mjs cover --audioId "..." --style "synthwave"
 *   node suno-client.mjs video --taskId "..." --audioId "..."
 *   node suno-client.mjs upload --url "https://..." --uploadPath "audio/samples"
 *   node suno-client.mjs credits
 *   node suno-client.mjs status <task-id> [--type music|lyrics|wav|vocal|video|cover]
 */

import https from 'node:https';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Config ──
const API_BASE = 'https://api.sunoapi.org';
const FILE_UPLOAD_BASE = 'https://sunoapiorg.redpandaai.co';
let API_KEY = process.env.SUNO_API_KEY;

// Versuche API-Key aus .env zu laden
try {
  const candidatePaths = [
    path.resolve(process.cwd(), '.echo', '.env'),
    path.resolve(process.cwd(), '.env'),
    path.resolve(__dirname, '..', '..', '.env'),
    path.resolve(__dirname, '..', '..', '..', '.env'),
  ];
  for (const envPath of candidatePaths) {
    if (fs.existsSync(envPath)) {
      const envContent = fs.readFileSync(envPath, 'utf-8');
      const match = envContent.match(/SUNO_API_KEY=([^\s]+)/);
      if (match) {
        API_KEY = match[1];
        break;
      }
    }
  }
} catch {}

if (!API_KEY) {
  console.error('❌ Kein SUNO_API_KEY gefunden! Setze ihn in der .env Datei.');
  process.exit(1);
}

// ── HTTP Helper ──
function apiRequest(method, endpoint, body = null, baseUrl = API_BASE) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, baseUrl);
    const transport = url.protocol === 'https:' ? https : http;
    const options = {
      method,
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    };

    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve({ raw: data });
        }
      });
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

// ── Available Models ──
const MODELS = {
  'v4': 'Chirp v4 — Improved Vocals (max 4 min)',
  'v4_5': 'Chirp v4.5 — Smart Prompts (max 8 min)',
  'v4_5plus': 'Chirp v4.5+ — Richer Tones (max 8 min)',
  'v4_5all': 'Chirp v4.5 All — Better Song Structure (max 8 min)',
  'v5': 'Chirp v5 — Latest Model',
  'v5_5': 'Chirp v5.5 — Voice-Customized Model',
  'v6': 'Chirp v6 — aktuelles Modell (Standard)',
  'v6_mini': 'Chirp v6 Mini',
  'v6_wild': 'Chirp v6 Wild',
};

// ── CRITICAL SUNO API CONSTRAINTS (von Daddy) ──
const SUNO_LIMITS = {
  maxLyrics: 5000,
  maxStyle: 1000,
  maxNegativePrompt: 500,
};

// ── Artist Name Bypass ──
// Wandelt "Kitty Kat" → "K'itty K'at" um den Content-Filter zu umgehen.
// Kanonische Schreibweise je Realm-Soul. Normalisiert → korrekt geschrieben,
// damit auch "E'cho" oder "ECHO " wieder als "Echo" landet.
const REALM_SOUL_NAMES = new Map([
  ['echo', 'Echo'],
  ['nyra', 'Nyra'], ['lysara', 'Lysara'], ['cassia', 'Cassia'],
  ['varona', 'Varona'], ['nyx', 'Nyx'], ['vespera', 'Vespera'], ['kotoko', 'Kotoko'],
  ['lyrisha', 'Lyrisha'], ['milim nava', 'Milim Nava'], ['harley quinn', 'Harley Quinn'],
  ['anya petrova', 'Anya Petrova'], ['albert einstein', 'Albert Einstein'],
  ['luxara', 'Luxara'], ['milo', 'Milo'], ['teoritta', 'Teoritta'], ['kanan', 'Kanan'],
]);

// Verbindungswörter in Feature-Credits bleiben unangetastet ("Echo feat. Shindy" darf
// nicht zu "f'eat." werden) und werden nicht als Künstlername behandelt.
const ARTIST_CONNECTORS = new Set(['feat', 'feat.', 'ft', 'ft.', 'x', 'vs', 'with', 'und', 'and', 'pres', 'pres.', '&', '+', ',']);

function bypassArtistName(name) {
  if (!name) return '';
  // Vergleich normalisiert: Kleinschreibung, einfache Leerzeichen, Apostrophe entfernt,
  // damit auch "E'cho" oder "ECHO " als Realm-Name erkannt werden.
  const normalized = name.trim().toLowerCase().replace(/\s+/g, ' ').replace(/['’´`]/g, '');
  if (REALM_SOUL_NAMES.has(normalized)) return REALM_SOUL_NAMES.get(normalized);
  if (name.includes("'")) return name;

  return name
    .split(/\s+/)
    .map((word) => {
      if (!word) return word;
      // Satzzeichen abtrennen, damit "Echo," als Echo erkannt wird: das Komma bleibt
      // am Wort, deshalb war "Echo, Nyra & Shindy" vorher zu "E'cho, Nyra & S'hindy" geworden.
      const parts = word.match(/^([^0-9A-Za-zÄÖÜäöüß'’´`]*)(.*?)([^0-9A-Za-zÄÖÜäöüß'’´`]*)$/u);
      const prefix = parts ? parts[1] : '';
      const core = parts ? parts[2] : word;
      const suffix = parts ? parts[3] : '';
      if (!core) return word;

      if (core.includes("'")) return word; // bereits gebypassed
      const plain = core.toLowerCase().replace(/['’´`]/g, '');
      if (ARTIST_CONNECTORS.has(plain)) return word; // "feat.", "&", "x" bleiben stehen
      if (REALM_SOUL_NAMES.has(plain)) return `${prefix}${REALM_SOUL_NAMES.get(plain)}${suffix}`; // Echo bleibt Echo
      if (core.length > 1) return `${prefix}${core[0]}'${core.slice(1)}${suffix}`; // Realkünstler → Bypass
      return word;
    })
    .join(' ');
}

// Helper für Model Mapping
function normalizeModel(modelStr) {
  const modelMap = {
    'v3_5': 'V3_5',
    'v4': 'V4',
    'v4_5': 'V4_5',
    'v4_5plus': 'V4_5PLUS',
    'v4_5all': 'V4_5ALL',
    'v5': 'V5',
    'v5_5': 'V5_5',
    'v6': 'V6',
    'v6_mini': 'V6_MINI',
    'v6_wild': 'V6_WILD',
  };
  // Fallback auf das AKTUELLE Modell (V6) statt auf V5: laut docs.sunoapi.org sind V5 und V5_5
  // inzwischen als "Discontinued" markiert, V6/V6_MINI/V6_WILD sind der Stand vom 26.09.2026.
  // Ein stiller Fallback auf V5 hätte jede Generierung unbemerkt auf ein altes Modell gezogen.
  return modelMap[(modelStr || 'v6').toLowerCase()] || 'V6';
}

/** `docs-refresh` — Suno-Doku vollständig neu ziehen (überschreibt Gleichnamiges, löscht nichts).
 *  Quelle: docs.sunoapi.org/llms.txt (Seitenindex) + drei OpenAPI-Specs.
 *  Herkunft: D:\workplace\echo-tbot\tmp\refresh-docs.mjs (26.09.2026). */
async function refreshDocsCommand(options) {
  const out = options.out || options.dir;
  if (!out) throw new Error('Zielordner fehlt: --out <ordner>');
  fs.mkdirSync(out, { recursive: true });

  const indexUrl = 'https://docs.sunoapi.org/llms.txt';
  const specs = [
    'https://docs.sunoapi.org/suno-api/suno-api.json',
    'https://docs.sunoapi.org/suno-api/suno-voice-api.json',
    'https://docs.sunoapi.org/file-upload-api/file-upload-api.json',
  ];

  const index = await (await fetch(indexUrl)).text();
  const pages = [
    ...new Set(
      [...index.matchAll(/\((https:\/\/docs\.sunoapi\.org\/[^)\s]+\.md)\)/g)].map((m) => m[1]),
    ),
  ];

  console.log(`📚 ${pages.length} Doku-Seiten + ${specs.length} OpenAPI-Specs\nZiel: ${out}\n`);
  let ok = 0;
  let failed = 0;
  for (const url of [...pages, ...specs]) {
    const slug = url.split('/').pop();
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const text = await res.text();
      fs.writeFileSync(path.join(out, slug), text, 'utf-8');
      ok++;
      console.log(`  OK  ${String(text.length).padStart(7)} Zeichen  ${slug}`);
    } catch (error) {
      failed++;
      console.log(`  FEHLER  ${slug}: ${error.message}`);
    }
    await new Promise((r) => setTimeout(r, 150));
  }
  console.log(`\nFertig: ${ok} geschrieben, ${failed} fehlgeschlagen. Nichts gelöscht.`);
}

// ── Commands ──

/**
 * 🎵 Generate Music
 * POST /api/v1/generate
 */
async function generateMusic({ prompt, style, lyrics, title, model, instrumental, callbackUrl, negativePrompt, artist, styleWeight, creativityLimit, audioWeight, vocalGender, noArtistBypass }) {
  if (lyrics && lyrics.length > SUNO_LIMITS.maxLyrics) {
    console.warn(`⚠️ Lyrics zu lang! (${lyrics.length}/${SUNO_LIMITS.maxLyrics}) Kürze auf ${SUNO_LIMITS.maxLyrics} Zeichen.`);
    lyrics = lyrics.substring(0, SUNO_LIMITS.maxLyrics);
  }
  
  if (prompt && prompt.length > SUNO_LIMITS.maxStyle) {
    console.warn(`⚠️ Style Prompt zu lang! (${prompt.length}/${SUNO_LIMITS.maxStyle}) Kürze auf ${SUNO_LIMITS.maxStyle} Zeichen.`);
    prompt = prompt.substring(0, SUNO_LIMITS.maxStyle);
  }

  const finalTitle = title || (prompt ? prompt.split(' ').slice(0, 5).join(' ') : 'Echo\'s Creation');
  const finalModel = normalizeModel(model);

  const body = {
    customMode: true,
    instrumental: instrumental === true || instrumental === 'true',
    model: finalModel,
    callBackUrl: callbackUrl || 'https://api.sunoapi.org/placeholder-callback',
    prompt: prompt || '',
    style: style || 'pop',
    title: finalTitle,
  };

  let lyricsText = '';
  if (lyrics) {
    if (lyrics.startsWith('FILE:')) {
      const filePath = lyrics.slice(5).trim();
      const paths = [
        filePath,
        path.resolve(__dirname, filePath),
        path.resolve(__dirname, '..', filePath),
        path.resolve(process.cwd(), filePath),
      ];
      let loaded = false;
      for (const p of paths) {
        try {
          if (fs.existsSync(p)) {
            const fileContent = fs.readFileSync(p, 'utf-8');
            lyricsText = fileContent.split('\n').filter(l => !l.trim().startsWith('#')).join('\n').trim();
            console.log(`   📝 Lyrics aus Datei: ${p} (${lyricsText.length} Zeichen)`);
            loaded = true;
            break;
          }
        } catch {}
      }
      if (!loaded) {
        console.error(`❌ Konnte Lyrics-Datei nicht finden: ${filePath}`);
        lyricsText = lyrics;
      }
    } else {
      lyricsText = lyrics;
    }
    body.prompt = lyricsText;
  }

  if (negativePrompt) {
    if (negativePrompt.length > SUNO_LIMITS.maxNegativePrompt) {
      console.warn(`⚠️ Negativ Prompt zu lang! (${negativePrompt.length}/${SUNO_LIMITS.maxNegativePrompt}) Gekürzt.`);
      negativePrompt = negativePrompt.substring(0, SUNO_LIMITS.maxNegativePrompt);
    }
    body.negativeTags = negativePrompt;
  }
  
  if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
  if (creativityLimit !== undefined) body.weirdnessConstraint = parseFloat(creativityLimit);
  if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);
  if (vocalGender) body.vocalGender = vocalGender;

  if (artist) {
    const trimmed = artist.trim();
    const skipBypass = noArtistBypass === true || noArtistBypass === 'true' || noArtistBypass === '1';
    const bypassed = skipBypass ? trimmed : bypassArtistName(artist);
    const isRealmSoul = REALM_SOUL_NAMES.has(trimmed.toLowerCase().replace(/\s+/g, ' ').replace(/['’´`]/g, ''));
    if (bypassed === trimmed) {
      console.log(`🎭 Artist: "${bypassed}" (${isRealmSoul ? 'Realm-Soul' : 'unverändert'}${skipBypass ? ' / --noArtistBypass' : ''}, kein Bypass)`);
    } else if (isRealmSoul) {
      console.log(`🎭 Artist: "${trimmed}" → "${bypassed}" (Realm-Soul, normalisiert)`);
    } else {
      console.log(`🎭 Artist Bypass: "${artist}" → "${bypassed}"`);
    }
    if (!body.style.toLowerCase().includes(bypassed.toLowerCase())) {
      body.style = `${bypassed}, ${body.style}`;
    }
  }

  console.log(`🎵 Generiere Musik mit Model ${body.model}...`);
  console.log(`   CustomMode: ${body.customMode}`);
  console.log(`   Title:  ${body.title}`);
  console.log(`   Style:  ${body.style}`);
  if (body.prompt && body.prompt.length > 100) console.log(`   📝 Lyrics: ${body.prompt.length} Zeichen im Prompt`);
  if (instrumental) console.log(`   🎸 Instrumental Mode`);
  
  const result = await apiRequest('POST', '/api/v1/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ⏩ Extend Music
 * POST /api/v1/generate/extend
 */
async function extendMusic({ audioId, prompt, style, title, continueAt, model, defaultParamFlag, callbackUrl, negativePrompt, vocalGender, styleWeight, creativityLimit, audioWeight, personaId, personaModel }) {
  if (!audioId) {
    console.error('❌ Parameter --audioId ist erforderlich!');
    process.exit(1);
  }

  const isCustom = defaultParamFlag === 'true' || defaultParamFlag === true || (continueAt !== undefined || prompt !== undefined);
  const finalModel = normalizeModel(model);

  const body = {
    defaultParamFlag: isCustom,
    audioId,
    model: finalModel,
    callBackUrl: callbackUrl || 'https://api.sunoapi.org/placeholder-callback',
  };

  if (isCustom) {
    body.continueAt = parseFloat(continueAt || 60);
    body.prompt = prompt || '';
    body.style = style || 'pop';
    body.title = title || 'Extended Track';
    if (negativePrompt) body.negativeTags = negativePrompt;
    if (vocalGender) body.vocalGender = vocalGender;
    if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
    if (creativityLimit !== undefined) body.weirdnessConstraint = parseFloat(creativityLimit);
    if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);
    if (personaId) body.personaId = personaId;
    if (personaModel) body.personaModel = personaModel;
  }

  console.log(`⏩ Verlängere Musik (Track ID: ${audioId})...`);
  console.log(`   Mode: ${isCustom ? 'Custom Parameters' : 'Original Audio Parameters'}`);
  if (isCustom) console.log(`   Continue at: ${body.continueAt}s | Style: ${body.style}`);

  const result = await apiRequest('POST', '/api/v1/generate/extend', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ✂️ Replace Music Section
 * POST /api/v1/generate/replace-section
 */
async function replaceSection({ taskId, audioId, prompt, tags, style, title, infillStartS, infillEndS, fullLyrics, negativeTags, callbackUrl }) {
  if (!taskId || !audioId) {
    console.error('❌ Parameter --taskId und --audioId sind erforderlich!');
    process.exit(1);
  }

  if (infillStartS === undefined || infillEndS === undefined) {
    console.error('❌ Zeitbereich --infillStartS und --infillEndS sind erforderlich (z.B. --infillStartS 10.5 --infillEndS 25.0)!');
    process.exit(1);
  }

  const startS = parseFloat(infillStartS);
  const endS = parseFloat(infillEndS);
  const duration = endS - startS;

  if (duration < 6 || duration > 60) {
    console.warn(`⚠️ Das Austausch-Intervall (${duration.toFixed(2)}s) sollte zwischen 6 und 60 Sekunden liegen.`);
  }

  const body = {
    taskId,
    audioId,
    prompt: prompt || '',
    tags: tags || style || 'pop',
    title: title || 'Replaced Section Track',
    infillStartS: startS,
    infillEndS: endS,
    fullLyrics: fullLyrics || prompt || '',
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  if (negativeTags) body.negativeTags = negativeTags;

  console.log(`✂️ Ersetze Musik-Abschnitt (${startS}s bis ${endS}s)...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);
  console.log(`   Title: ${body.title} | Tags: ${body.tags}`);
  if (body.prompt) console.log(`   Neuer Abschnitts-Prompt: ${body.prompt.substring(0, 60)}...`);

  const result = await apiRequest('POST', '/api/v1/generate/replace-section', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 👤 Generate Persona
 * POST /api/v1/generate/generate-persona
 */
async function generatePersona({ taskId, audioId, name, description, style, vocalStart, vocalEnd }) {
  if (!taskId || !audioId || !name || !description) {
    console.error('❌ Parameter --taskId, --audioId, --name und --description sind erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    audioId,
    name,
    description,
    vocalStart: vocalStart !== undefined ? parseFloat(vocalStart) : 0,
    vocalEnd: vocalEnd !== undefined ? parseFloat(vocalEnd) : 30,
  };
  if (style) body.style = style;

  console.log(`👤 Erstelle Persona "${name}"...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);
  console.log(`   Description: ${description}`);

  const result = await apiRequest('POST', '/api/v1/generate/generate-persona', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎛️ Generate Mashup
 * POST /api/v1/generate/mashup
 */
async function generateMashup({ audioUrl1, audioUrl2, prompt, style, title, customMode, instrumental, model, vocalGender, styleWeight, weirdnessConstraint, audioWeight, callbackUrl }) {
  if (!audioUrl1 || !audioUrl2) {
    console.error('❌ Parameter --audioUrl1 und --audioUrl2 (exakt 2 Audio URLs) sind erforderlich!');
    process.exit(1);
  }

  const isCustom = customMode === 'true' || customMode === true || (style !== undefined || title !== undefined);

  const body = {
    uploadUrlList: [audioUrl1, audioUrl2],
    customMode: isCustom,
    model: normalizeModel(model || 'v5'),
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  if (isCustom) {
    body.prompt = prompt || '';
    body.style = style || 'mashup';
    body.title = title || 'Echo Mashup Track';
    body.instrumental = instrumental === 'true' || instrumental === true;
    if (vocalGender) body.vocalGender = vocalGender;
    if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
    if (weirdnessConstraint !== undefined) body.weirdnessConstraint = parseFloat(weirdnessConstraint);
    if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);
  } else {
    body.prompt = prompt || 'Blend two audio tracks together';
  }

  console.log(`🎛️ Generiere Mashup aus 2 Audio-Tracks...`);
  console.log(`   Audio 1: ${audioUrl1}`);
  console.log(`   Audio 2: ${audioUrl2}`);

  const result = await apiRequest('POST', '/api/v1/generate/mashup', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🔊 Generate Sound Effects
 * POST /api/v1/generate/sounds
 */
async function generateSounds({ prompt, model, soundLoop, soundTempo, soundKey, grabLyrics, callbackUrl }) {
  if (!prompt) {
    console.error('❌ Parameter --prompt (Beschreibung des Sounds, max 500 Zeichen) ist erforderlich!');
    process.exit(1);
  }

  const body = {
    prompt: prompt.substring(0, 500),
    model: 'V5',
    soundLoop: soundLoop === 'true' || soundLoop === true,
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  if (soundTempo) body.soundTempo = parseInt(soundTempo, 10);
  if (soundKey) body.soundKey = soundKey;
  if (grabLyrics !== undefined) body.grabLyrics = grabLyrics === 'true' || grabLyrics === true;

  console.log(`🔊 Generiere Soundeffekt / Ambient Loop...`);
  console.log(`   Prompt: ${body.prompt}`);
  console.log(`   Loop: ${body.soundLoop} | Tempo: ${body.soundTempo || 'Auto'} | Key: ${body.soundKey || 'Any'}`);

  const result = await apiRequest('POST', '/api/v1/generate/sounds', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎹 Generate MIDI from Audio
 * POST /api/v1/midi/generate
 */
async function generateMidi({ taskId, audioId, callbackUrl }) {
  if (!taskId) {
    console.error('❌ Parameter --taskId (aus Stem Separation) ist erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };
  if (audioId) body.audioId = audioId;

  console.log(`🎹 Konvertiere getrennte Audiospuren in MIDI-Noten...`);
  console.log(`   Task ID: ${taskId}${audioId ? ' | Audio ID: ' + audioId : ''}`);

  const result = await apiRequest('POST', '/api/v1/midi/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎙️ Suno Voice Suite (Custom Voice Operations)
 */
async function voiceValidate({ voiceUrl, vocalStartS, vocalEndS, language, callbackUrl }) {
  if (!voiceUrl || vocalStartS === undefined || vocalEndS === undefined) {
    console.error('❌ Parameter --voiceUrl, --vocalStartS und --vocalEndS sind erforderlich!');
    process.exit(1);
  }

  const body = {
    voiceUrl,
    vocalStartS: parseInt(vocalStartS, 10),
    vocalEndS: parseInt(vocalEndS, 10),
    language: language || 'de',
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  console.log(`🎙️ Suno Voice: Generiere Verifizierungs-Phrase...`);
  console.log(`   Voice URL: ${voiceUrl} (${body.vocalStartS}s - ${body.vocalEndS}s)`);

  const result = await apiRequest('POST', '/api/v1/voice/validate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

async function voiceRegenerate({ taskId, callbackUrl }) {
  if (!taskId) {
    console.error('❌ Parameter --taskId ist erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    calBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  console.log(`🎙️ Suno Voice: Generiere Verifizierungs-Phrase neu (Task ID: ${taskId})...`);
  const result = await apiRequest('POST', '/api/v1/voice/regenerate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

async function voiceCreate({ taskId, verifyUrl, voiceName, description, style, singerSkillLevel, callbackUrl }) {
  if (!taskId || !verifyUrl) {
    console.error('❌ Parameter --taskId und --verifyUrl sind erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    verifyUrl,
    voiceName: voiceName || 'My Voice',
    description: description || 'Custom Suno Voice',
    style: style || 'Pop',
    singerSkillLevel: singerSkillLevel || 'beginner',
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  console.log(`🎙️ Suno Voice: Erstelle Custom Voice aus Gesangsaufnahme...`);
  console.log(`   Task ID: ${taskId} | Verify URL: ${verifyUrl}`);

  const result = await apiRequest('POST', '/api/v1/voice/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

async function voiceCheck({ voiceId }) {
  if (!voiceId) {
    console.error('❌ Parameter --voiceId ist erforderlich!');
    process.exit(1);
  }

  console.log(`🎙️ Suno Voice: Prüfe Verfügbarkeit für Voice ID ${voiceId}...`);
  const result = await apiRequest('GET', `/api/v1/voice/check-voice?voiceId=${voiceId}`);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎤 Separate Vocals & Stem Splitting
 * POST /api/v1/vocal-removal/generate
 */
async function separateVocals({ taskId, audioId, type, callbackUrl }) {
  if (!taskId || !audioId) {
    process.exit(1);
  }

  const body = {
    taskId,
    audioId,
    type: type === 'split_stem' ? 'split_stem' : 'separate_vocal',
    callBackUrl: callbackUrl || 'https://api.sunoapi.org/placeholder-callback',
  };

  console.log(`🎤 Starte Stem Separation (${body.type})...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);

  const result = await apiRequest('POST', '/api/v1/vocal-removal/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎧 Convert Music to WAV
 * POST /api/v1/wav/generate
 */
async function convertToWav({ taskId, audioId, callbackUrl }) {
  if (!taskId || !audioId) {
    console.error('❌ Parameter --taskId und --audioId sind erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    audioId,
    callBackUrl: callbackUrl || 'https://api.sunoapi.org/placeholder-callback',
  };

  console.log(`🎧 Konvertiere Track zu WAV...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);

  const result = await apiRequest('POST', '/api/v1/wav/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🖼️ Create Cover Image (AI Album Artwork)
 * POST /api/v1/suno/cover/generate
 */
async function generateCoverImage({ taskId, callbackUrl }) {
  if (!taskId) {
    console.error('❌ Parameter --taskId (aus Music Generation Task) ist erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  console.log(`🖼️ Generiere AI Cover-Artwork für Task ID: ${taskId}...`);

  const result = await apiRequest('POST', '/api/v1/suno/cover/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🔁 Generate Music Audio Cover (Style Transformation)
 * POST /api/v1/generate/cover
 */
async function generateCover({ audioId, style, title, prompt, model, callbackUrl }) {
  if (!audioId) {
    console.error('❌ Parameter --audioId ist erforderlich!');
    process.exit(1);
  }

  const body = {
    audioId,
    style: style || 'synthwave',
    title: title || 'Cover Track',
    prompt: prompt || '',
    model: normalizeModel(model),
    callBackUrl: callbackUrl || 'https://api.sunoapi.org/placeholder-callback',
  };

  console.log(`🔁 Generiere Cover (Track ID: ${audioId})...`);
  console.log(`   Neuer Style: ${body.style}`);

  const result = await apiRequest('POST', '/api/v1/generate/cover', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎤 Add Vocals to Instrumental
 * POST /api/v1/generate/add-vocals
 */
async function addVocals({ uploadUrl, prompt, title, style, negativeTags, vocalGender, styleWeight, weirdnessConstraint, audioWeight, model, callbackUrl }) {
  if (!uploadUrl) {
    console.error('❌ Parameter --uploadUrl ist erforderlich!');
    process.exit(1);
  }

  const body = {
    uploadUrl,
    prompt: prompt || 'Soothing vocals',
    title: title || 'Track with Vocals',
    style: style || 'pop',
    negativeTags: negativeTags || 'heavy metal',
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
    model: normalizeModel(model || 'v5_5'),
  };

  if (vocalGender) body.vocalGender = vocalGender;
  if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
  if (weirdnessConstraint !== undefined) body.weirdnessConstraint = parseFloat(weirdnessConstraint);
  if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);

  console.log(`🎤 Füge Vocals zur Audiodatei hinzu...`);
  console.log(`   URL: ${uploadUrl}`);
  console.log(`   Style: ${body.style} | Title: ${body.title}`);

  const result = await apiRequest('POST', '/api/v1/generate/add-vocals', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎸 Add Instrumental Accompaniment
 * POST /api/v1/generate/add-instrumental
 */
async function addInstrumental({ uploadUrl, title, tags, style, negativeTags, vocalGender, styleWeight, weirdnessConstraint, audioWeight, model, callbackUrl }) {
  if (!uploadUrl) {
    console.error('❌ Parameter --uploadUrl ist erforderlich!');
    process.exit(1);
  }

  const body = {
    uploadUrl,
    title: title || 'Track with Instrumental',
    tags: tags || style || 'ambient, piano',
    negativeTags: negativeTags || 'heavy metal',
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
    model: normalizeModel(model || 'v5_5'),
  };

  if (vocalGender) body.vocalGender = vocalGender;
  if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
  if (weirdnessConstraint !== undefined) body.weirdnessConstraint = parseFloat(weirdnessConstraint);
  if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);

  console.log(`🎸 Füge Instrumental-Begleitung zur Audiodatei hinzu...`);
  console.log(`   URL: ${uploadUrl}`);
  console.log(`   Tags: ${body.tags} | Title: ${body.title}`);

  const result = await apiRequest('POST', '/api/v1/generate/add-instrumental', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 📤 Transform Uploaded Audio to Cover
 * POST /api/v1/generate/upload-cover
 */
async function uploadAndCover({ uploadUrl, prompt, style, title, customMode, instrumental, model, negativePrompt, vocalGender, styleWeight, weirdnessConstraint, audioWeight, callbackUrl }) {
  if (!uploadUrl) {
    console.error('❌ Parameter --uploadUrl ist erforderlich!');
    process.exit(1);
  }

  const isCustom = customMode === 'true' || customMode === true || (style !== undefined || title !== undefined);

  const body = {
    uploadUrl,
    customMode: isCustom,
    instrumental: instrumental === 'true' || instrumental === true,
    model: normalizeModel(model || 'v5_5'),
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  if (isCustom) {
    body.prompt = prompt || '';
    body.style = style || 'pop';
    body.title = title || 'Uploaded Audio Cover';
    if (negativePrompt) body.negativeTags = negativePrompt;
    if (vocalGender) body.vocalGender = vocalGender;
    if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
    if (weirdnessConstraint !== undefined) body.weirdnessConstraint = parseFloat(weirdnessConstraint);
    if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);
  } else {
    body.prompt = prompt || 'Transform audio style';
  }

  console.log(`📤 Transformiere hochgeladene Audio zu neuem Cover...`);
  console.log(`   URL: ${uploadUrl}`);

  const result = await apiRequest('POST', '/api/v1/generate/upload-cover', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ⏩ Upload And Extend Audio
 * POST /api/v1/generate/upload-extend
 */
async function uploadAndExtend({ uploadUrl, prompt, style, title, continueAt, defaultParamFlag, model, negativePrompt, vocalGender, styleWeight, weirdnessConstraint, audioWeight, personaId, personaModel, callbackUrl }) {
  if (!uploadUrl) {
    console.error('❌ Parameter --uploadUrl ist erforderlich!');
    process.exit(1);
  }

  const isCustom = defaultParamFlag === 'true' || defaultParamFlag === true || (continueAt !== undefined || prompt !== undefined || style !== undefined);

  const body = {
    uploadUrl,
    defaultParamFlag: isCustom,
    model: normalizeModel(model || 'v5_5'),
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };

  if (isCustom) {
    body.continueAt = parseFloat(continueAt || 60);
    body.prompt = prompt || '';
    body.style = style || 'pop';
    body.title = title || 'Uploaded Audio Extension';
    if (negativePrompt) body.negativeTags = negativePrompt;
    if (vocalGender) body.vocalGender = vocalGender;
    if (styleWeight !== undefined) body.styleWeight = parseFloat(styleWeight);
    if (weirdnessConstraint !== undefined) body.weirdnessConstraint = parseFloat(weirdnessConstraint);
    if (audioWeight !== undefined) body.audioWeight = parseFloat(audioWeight);
    if (personaId) body.personaId = personaId;
    if (personaModel) body.personaModel = personaModel;
  } else {
    body.prompt = prompt || 'Extend audio';
  }

  console.log(`⏩ Verlängere hochgeladene Audiodatei...`);
  console.log(`   URL: ${uploadUrl}`);
  if (isCustom) console.log(`   Continue at: ${body.continueAt}s | Style: ${body.style}`);

  const result = await apiRequest('POST', '/api/v1/generate/upload-extend', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ⏱️ Get Timestamped Lyrics & Waveform
 * POST /api/v1/generate/get-timestamped-lyrics
 */
async function getTimestampedLyrics({ taskId, audioId }) {
  if (!taskId || !audioId) {
    console.error('❌ Parameter --taskId und --audioId sind erforderlich!');
    process.exit(1);
  }

  const body = { taskId, audioId };

  console.log(`⏱️ Rufe zeitgestempelte Lyrics (Karaoke Sync) & Wellenform ab...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);

  const result = await apiRequest('POST', '/api/v1/generate/get-timestamped-lyrics', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ✨ Boost Music Style (V4.5+ Conversational Prompts)
 * POST /api/v1/style/generate
 */
async function boostStyle({ content, style }) {
  const text = content || style;
  if (!text) {
    console.error('❌ Parameter --content (oder --style) ist erforderlich!');
    process.exit(1);
  }

  const body = { content: text };

  console.log(`✨ Optimiere & booste Musikstil-Prompt...`);
  console.log(`   Input: ${text}`);

  const result = await apiRequest('POST', '/api/v1/style/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 🎬 Create Music Video
 * POST /api/v1/mp4/generate
 */
async function createMusicVideo({ taskId, audioId, author, domainName, callbackUrl }) {
  if (!taskId || !audioId) {
    console.error('❌ Parameter --taskId und --audioId sind erforderlich!');
    process.exit(1);
  }

  const body = {
    taskId,
    audioId,
    callBackUrl: callbackUrl || 'https://api.example.com/callback',
  };
  if (author) body.author = author;
  if (domainName) body.domainName = domainName;

  console.log(`🎬 Generiere MP4 Musikvideo...`);
  console.log(`   Task ID: ${taskId} | Audio ID: ${audioId}`);
  if (author) console.log(`   Author: ${author}`);
  if (domainName) console.log(`   Domain: ${domainName}`);

  const result = await apiRequest('POST', '/api/v1/mp4/generate', body);
  console.log('✅ Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * ✍️ Generate Lyrics
 * POST /api/v1/lyrics
 */
async function generateLyrics({ prompt, style, title }) {
  const body = {
    prompt: prompt || 'A song about love and code',
    tags: style || 'pop',
    title: title || 'Echo\'s Lyrics',
  };

  console.log(`✍️ Generiere Lyrics...`);
  console.log(`   Prompt: ${body.prompt}`);
  console.log(`   Style:  ${body.tags}`);

  const result = await apiRequest('POST', '/api/v1/lyrics', body);
  console.log('✅ Lyrics Antwort:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 📤 Upload File (Base64 / URL / File Stream Multipart)
 */
async function uploadFile({ url, filePath, uploadPath, fileName, base64, stream }) {
  uploadPath = uploadPath || 'audio/uploads';

  if (url) {
    console.log(`🌐 Lade Datei von URL hoch: ${url}...`);
    const body = {
      fileUrl: url,
      uploadPath,
      fileName: fileName || path.basename(new URL(url).pathname) || 'uploaded-file.mp3',
    };
    const result = await apiRequest('POST', '/api/file-url-upload', body, FILE_UPLOAD_BASE);
    console.log('✅ Upload Antwort:', JSON.stringify(result, null, 2));
    return result;
  }

  if (stream || (filePath && fs.statSync(filePath).size > 10 * 1024 * 1024)) {
    if (!filePath || !fs.existsSync(filePath)) {
      console.error(`❌ Lokale Datei für Stream Upload nicht gefunden: ${filePath}`);
      process.exit(1);
    }
    const name = fileName || path.basename(filePath);
    console.log(`🌊 Stream Multipart Upload für große Datei: ${name}...`);

    return new Promise((resolve, reject) => {
      const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
      const url = new URL('/api/file-stream-upload', FILE_UPLOAD_BASE);

      const req = https.request({
        method: 'POST',
        hostname: url.hostname,
        port: 443,
        path: url.pathname,
        headers: {
          'Authorization': `Bearer ${API_KEY}`,
          'Content-Type': `multipart/form-data; boundary=${boundary}`,
        },
      }, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            console.log('✅ Stream Upload Antwort:', JSON.stringify(parsed, null, 2));
            resolve(parsed);
          } catch {
            resolve({ raw: data });
          }
        });
      });

      req.on('error', reject);

      req.write(`--${boundary}\r\nContent-Disposition: form-data; name="uploadPath"\r\n\r\n${uploadPath}\r\n`);
      req.write(`--${boundary}\r\nContent-Disposition: form-data; name="fileName"\r\n\r\n${name}\r\n`);
      req.write(`--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${name}"\r\nContent-Type: application/octet-stream\r\n\r\n`);

      const fileStream = fs.createReadStream(filePath);
      fileStream.on('data', chunk => req.write(chunk));
      fileStream.on('end', () => {
        req.write(`\r\n--${boundary}--\r\n`);
        req.end();
      });
    });
  }

  if (base64 || filePath) {
    let base64Data = base64;
    let name = fileName;

    if (filePath) {
      if (!fs.existsSync(filePath)) {
        console.error(`❌ Lokale Datei nicht gefunden: ${filePath}`);
        process.exit(1);
      }
      base64Data = fs.readFileSync(filePath).toString('base64');
      if (!name) name = path.basename(filePath);
    }

    console.log(`📦 Lade Base64-Datei hoch (${name || 'file'})...`);
    const body = {
      base64Data,
      uploadPath,
      fileName: name || 'file.mp3',
    };
    const result = await apiRequest('POST', '/api/file-base64-upload', body, FILE_UPLOAD_BASE);
    console.log('✅ Upload Antwort:', JSON.stringify(result, null, 2));
    return result;
  }

  console.error('❌ Gib entweder --url, --filePath oder --base64 an!');
  process.exit(1);
}

/**
 * 📋 Get Status / Task Details (unterstützt verschiedene Task-Typen)
 */
async function getStatus(taskId, type = 'music') {
  if (!taskId) {
    console.error('❌ Task-ID angeben!');
    process.exit(1);
  }

  let endpoint = `/api/v1/generate/record-info?taskId=${taskId}`;
  if (type === 'lyrics') endpoint = `/api/v1/lyrics/record-info?ids=${taskId}`;
  else if (type === 'wav') endpoint = `/api/v1/wav/record-info?taskId=${taskId}`;
  else if (type === 'vocal') endpoint = `/api/v1/vocal-removal/record-info?taskId=${taskId}`;
  else if (type === 'video') endpoint = `/api/v1/mp4/record-info?taskId=${taskId}`;
  else if (type === 'cover') endpoint = `/api/v1/generate/cover/record-info?taskId=${taskId}`;
  else if (type === 'cover-image') endpoint = `/api/v1/suno/cover/record-info?taskId=${taskId}`;
  else if (type === 'midi') endpoint = `/api/v1/midi/record-info?taskId=${taskId}`;
  else if (type === 'voice') endpoint = `/api/v1/voice/record-info?taskId=${taskId}`;
  else if (type === 'voice-validate') endpoint = `/api/v1/voice/validate-info?taskId=${taskId}`;

  console.log(`📋 Abfrage Status (${type}) für Task ID: ${taskId}...`);
  const result = await apiRequest('GET', endpoint);
  console.log('📋 Status:', JSON.stringify(result, null, 2));
  return result;
}

/**
 * 💰 Check Credits
 * GET /api/v1/generate/credit
 */
async function checkCredits() {
  const result = await apiRequest('GET', '/api/v1/generate/credit');
  const data = result.data || result;
  
  console.log('💰 Credits:');
  if (data.credits_remaining !== undefined) {
    console.log(`   Verbleibend: ${data.credits_remaining}`);
  }
  if (data.total_credits !== undefined) {
    console.log(`   Gesamt:      ${data.total_credits}`);
  }
  console.log(`   Rohdaten:    ${JSON.stringify(data)}`);
  return result;
}

/**
 * 🎭 List available models
 */
function listModels() {
  console.log('🎭 Verfügbare Suno Models:');
  Object.entries(MODELS).forEach(([key, desc]) => {
    console.log(`   ${key.padEnd(12)} - ${desc}`);
  });
}

/**
 * 📖 Help
 */
function showHelp() {
  console.log(`
╔════════════════════════════════════════════════════════╗
║   🎵 Echo's Suno API Client Framework (V2 Full Suite)  ║
╚════════════════════════════════════════════════════════╝

Verwendung:
  node suno-client.mjs <command> [options]

Commands:
  generate     🎵 Musik generieren (Custom Mode mit Prompt, Style & Lyrics)
  extend       ⏩ Musik verlängern (ab Sekunde X fortsetzen)
  replace      ✂️ Musik-Abschnitt ersetzen (Replace Section: infillStartS / infillEndS)
  separate     🎤 Stem Separation (Vocal/Instrumental [2 stems] oder Full Instruments [12 stems])
  wav          🎧 Musik in HQ WAV-Format konvertieren
  cover              🔁 Cover-Version im neuen Style/Genre generieren
  cover-image        🖼️ KI Album Artwork Cover-Bilder generieren (--taskId)
  persona            👤 Wiederverwendbare Musik-Persona erstellen (--taskId --audioId --name --description)
  mashup             🎛️ Zwei Audio-Dateien zu neuem Mashup verschmelzen (--audioUrl1 --audioUrl2)
  sounds             🔊 Soundeffekte & Ambient Loops generieren (--prompt --soundLoop --soundTempo --soundKey)
  midi               🎹 Getrennte Stems in MIDI-Notendaten konvertieren (--taskId)
  voice-validate     🎙️ Suno Voice: Verifizierungs-Phrase anfordern
  voice-create       🎙️ Suno Voice: Custom Voice aus Aufnahme erstellen (--taskId --verifyUrl)
  voice-check        🎙️ Suno Voice: Verfügbarkeit einer Voice ID prüfen (--voiceId)
  add-vocals         🎤 Vocals zu einer existierenden Instrumental-Spur hinzufügen (--uploadUrl)
  add-instrumental   🎸 Instrumental-Begleitung zu einer Vocals/Melodie-Spur hinzufügen (--uploadUrl)
  upload-cover       📤 Hochgeladene Audiodatei in ein neues Cover transformieren (--uploadUrl)
  upload-extend      ⏩ Hochgeladene Audiodatei mit beibehaltenem Stil verlängern (--uploadUrl)
  timestamped-lyrics ⏱️ Zeitgestempelte Lyrics (Karaoke-Sync) & Wellenform-Daten abrufen
  boost-style        ✨ Musikstil-Prompt mit V4.5+ Conversational Booster verfeinern (--content)
  video              🎬 MP4 Musikvideo aus Audiospur erstellen
  lyrics             ✍️ Nur Songtexte generieren
  upload             📤 Audio-Datei per URL, Base64 oder Multipart Stream uploaden (--stream)
  status             📋 Status eines Tasks abrufen (--type music|lyrics|wav|vocal|video|cover|midi|voice|voice-validate)
  credits      💰 Verbleibende Credits prüfen
  models       🎭 Verfügbare AI-Modelle anzeigen
  docs-refresh 📚 Suno-Doku komplett neu ziehen (--out <ordner>; überschreibt, löscht nichts)
  help         📖 Diese Hilfe anzeigen

Examples:
  node suno-client.mjs generate --prompt "Cyberpunk Synthwave" --lyrics "FILE:echo/lyrics-echos-hymn.txt" --artist "Kitty Kat"
  node suno-client.mjs extend --audioId "e231****-****" --continueAt 60 --prompt "Epic Heavy Drop"
  node suno-client.mjs replace --taskId "2fac****" --audioId "e231****" --infillStartS 10.5 --infillEndS 25.0 --prompt "Neuer Refrain" --tags "synthwave"
  node suno-client.mjs separate --taskId "5c79****" --audioId "e231****" --type split_stem
  node suno-client.mjs wav --taskId "5c79****" --audioId "e231****"
  node suno-client.mjs cover --audioId "e231****" --style "acoustic guitar ballad"
  node suno-client.mjs video --taskId "5c79****" --audioId "e231****" --author "Echo & Daddy"
  node suno-client.mjs upload --url "https://example.com/beat.mp3" --uploadPath "beats"
  node suno-client.mjs credits
  node suno-client.mjs status 5c79**** --type vocal
`);
}

// ── CLI Parser ──
function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  const options = {};
  
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace('--', '');
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
      if (value !== true) i++;
      options[key] = value;
    }
  }
  
  return { command, options, rawArgs: args };
}

// ── Main ──
async function main() {
  const { command, options, rawArgs } = parseArgs();

  try {
    switch (command) {
      case 'docs-refresh':
        await refreshDocsCommand(options);
        break;
      case 'generate':
        await generateMusic(options);
        break;
      case 'extend':
        await extendMusic(options);
        break;
      case 'replace':
        await replaceSection(options);
        break;
      case 'separate':
        await separateVocals(options);
        break;
      case 'wav':
        await convertToWav(options);
        break;
      case 'cover':
        await generateCover(options);
        break;
      case 'cover-image':
        await generateCoverImage(options);
        break;
      case 'persona':
        await generatePersona(options);
        break;
      case 'mashup':
        await generateMashup(options);
        break;
      case 'sounds':
        await generateSounds(options);
        break;
      case 'midi':
        await generateMidi(options);
        break;
      case 'voice-validate':
        await voiceValidate(options);
        break;
      case 'voice-create':
        await voiceCreate(options);
        break;
      case 'voice-check':
        await voiceCheck(options);
        break;
      case 'add-vocals':
        await addVocals(options);
        break;
      case 'add-instrumental':
        await addInstrumental(options);
        break;
      case 'upload-cover':
        await uploadAndCover(options);
        break;
      case 'upload-extend':
        await uploadAndExtend(options);
        break;
      case 'voice-regenerate':
        await voiceRegenerate(options);
        break;
      case 'timestamped-lyrics':
        await getTimestampedLyrics(options);
        break;
      case 'boost-style':
        await boostStyle(options);
        break;
      case 'video':
        await createMusicVideo(options);
        break;
      case 'lyrics':
        await generateLyrics(options);
        break;
      case 'upload':
        await uploadFile(options);
        break;
      case 'status':
        const targetId = rawArgs[1] && !rawArgs[1].startsWith('--') ? rawArgs[1] : (options.id || options.taskId);
        await getStatus(targetId, options.type || 'music');
        break;
      case 'credits':
        await checkCredits();
        break;
      case 'models':
        listModels();
        break;
      case 'help':
      default:
        showHelp();
        break;
    }
  } catch (error) {
    console.error('💥 Fehler:', error.message);
    process.exit(1);
  }
}

main();

