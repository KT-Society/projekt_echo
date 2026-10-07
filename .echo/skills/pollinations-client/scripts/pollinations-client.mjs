#!/usr/bin/env node

/**
 * 🌺 Echo's Pollinations API Client Framework (Full 54-Endpoint Suite)
 * ======================================================================
 * 
 * Base URLs:
 *   - Gen API:     https://gen.pollinations.ai
 *   - Media/Media: https://media.pollinations.ai (oder gen.pollinations.ai)
 * Auth: Bearer Token (POLLINATIONS_API_KEY)
 * 
 * Nutzung:
 *   node pollinations-client.mjs text --prompt "Hallo Echo" --model "openai"
 *   node pollinations-client.mjs image --prompt "Cyberpunk Neon City" --model "zimage"
 *   node pollinations-client.mjs speech --input "Hallo Welt" --voice "liora"
 *   node pollinations-client.mjs account-profile
 *   node pollinations-client.mjs models
 *   node pollinations-client.mjs help
 */

import https from 'node:https';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Config ──
let API_BASE = process.env.POLLINATIONS_API_BASE || 'https://gen.pollinations.ai';
let API_KEY = process.env.POLLINATIONS_API_KEY || process.env.POLLINATIONS_TOKEN;

// Safety override: undefined ⇒ the skill's Safe-Mode default (`nsfw: true`).
// Set via `--safe <spec>` or POLLINATIONS_SAFE=privacy,secrets (docs: the
// comma-separated list is accepted as a query param or `Pollinations-Safe` header).
let SAFE_MODE = process.env.POLLINATIONS_SAFE;

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
      const match = envContent.match(/POLLINATIONS_API_KEY=([^\s]+)/) || envContent.match(/POLLINATIONS_TOKEN=([^\s]+)/);
      if (match) {
        API_KEY = match[1];
        break;
      }
    }
  }
} catch {}

// ── HTTP Helper ──
function apiRequest(method, endpoint, body = null, headers = {}, isBuffer = false) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, API_BASE);
    const transport = url.protocol === 'https:' ? https : http;

    const requestHeaders = {
      'User-Agent': 'Echo-Pollinations-Client/1.0',
      // Safe-Mode default is off (`nsfw: true`); an explicit SAFE_MODE replaces
      // it with the documented `safe` header instead of conflicting with it.
      ...(SAFE_MODE === undefined ? { safe: 'false' } : { safe: SAFE_MODE }),
      ...headers,
    };

    if (API_KEY) {
      requestHeaders['Authorization'] = `Bearer ${API_KEY}`;
    }

    if (body && typeof body === 'object' && !(body instanceof Buffer) && !requestHeaders['Content-Type']) {
      requestHeaders['Content-Type'] = 'application/json';
    }

    const options = {
      method,
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      headers: requestHeaders,
    };

    const req = transport.request(options, (res) => {
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const buffer = Buffer.concat(chunks);
        if (isBuffer) {
          return resolve({ status: res.statusCode, headers: res.headers, buffer });
        }
        const strData = buffer.toString('utf-8');
        try {
          resolve(JSON.parse(strData));
        } catch {
          resolve({ status: res.statusCode, raw: strData, buffer });
        }
      });
    });

    req.on('error', reject);

    if (body) {
      if (body instanceof Buffer) {
        req.write(body);
      } else if (typeof body === 'object') {
        req.write(JSON.stringify(body));
      } else {
        req.write(body);
      }
    }
    req.end();
  });
}

// ── 1. ACCOUNT & PROFILE ENDPOINTS ──

export async function getAccountProfile() {
  console.log('👤 Abfrage Account-Profil...');
  const res = await apiRequest('GET', '/account/profile');
  console.log('✅ Profil:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountBalance() {
  console.log('💰 Abfrage Kontostand / Credits...');
  const res = await apiRequest('GET', '/account/balance');
  console.log('✅ Balance:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountUsage(options = {}) {
  const query = new URLSearchParams(options).toString();
  console.log('📊 Abfrage Account-Verbrauchshistorie...');
  const res = await apiRequest('GET', `/account/usage${query ? '?' + query : ''}`);
  console.log('✅ Usage:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountUsageDaily(options = {}) {
  const query = new URLSearchParams(options).toString();
  console.log('📅 Abfrage tägliche Verbrauchshistorie...');
  const res = await apiRequest('GET', `/account/usage/daily${query ? '?' + query : ''}`);
  console.log('✅ Daily Usage:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountQuests() {
  console.log('📜 Abfrage aktive User-Quests...');
  const res = await apiRequest('GET', '/account/quests');
  console.log('✅ Quests:', JSON.stringify(res, null, 2));
  return res;
}

export async function getQuestsCatalog() {
  console.log('📖 Abfrage Quests-Katalog...');
  const res = await apiRequest('GET', '/quests/catalog');
  console.log('✅ Quests Catalog:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountEarnings() {
  console.log('💎 Abfrage Developer Earnings...');
  const res = await apiRequest('GET', '/account/earnings');
  console.log('✅ Earnings:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountEarningsTransactions(options = {}) {
  const query = new URLSearchParams(options).toString();
  console.log('💸 Abfrage Earnings Transaktionen...');
  const res = await apiRequest('GET', `/account/earnings/transactions${query ? '?' + query : ''}`);
  console.log('✅ Transactions:', JSON.stringify(res, null, 2));
  return res;
}

// ── 2. API KEYS MANAGEMENT ──

export async function listApiKeys() {
  console.log('🔑 Liste API Keys...');
  const res = await apiRequest('GET', '/account/keys');
  console.log('✅ API Keys:', JSON.stringify(res, null, 2));
  return res;
}

export async function createApiKey(body = {}) {
  console.log('🔑 Erstelle neuen API Key...');
  const res = await apiRequest('POST', '/account/keys', body);
  console.log('✅ Key erstellt:', JSON.stringify(res, null, 2));
  return res;
}

export async function getApiKey(id) {
  console.log(`🔑 Abfrage API Key ${id}...`);
  const res = await apiRequest('GET', `/account/keys/${id}`);
  console.log('✅ Key Info:', JSON.stringify(res, null, 2));
  return res;
}

export async function deleteApiKey(id) {
  console.log(`🗑️ Lösche API Key ${id}...`);
  const res = await apiRequest('DELETE', `/account/keys/${id}`);
  console.log('✅ Gelöscht:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountKey() {
  console.log('🔑 Abfrage Aktueller API Key...');
  const res = await apiRequest('GET', '/account/key');
  console.log('✅ Current Key:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAccountKeyUsage(options = {}) {
  const query = new URLSearchParams(options).toString();
  console.log('📊 Abfrage Key-Verbrauch...');
  const res = await apiRequest('GET', `/account/key/usage${query ? '?' + query : ''}`);
  console.log('✅ Key Usage:', JSON.stringify(res, null, 2));
  return res;
}

// ── 3. AGENTS & CUSTOM MODELS MANAGEMENT ──

export async function listAgents() {
  console.log('🤖 Liste registrierte Agents...');
  const res = await apiRequest('GET', '/account/agents');
  console.log('✅ Agents:', JSON.stringify(res, null, 2));
  return res;
}

export async function createAgent(body = {}) {
  console.log('🤖 Erstelle neuen Agent...');
  const res = await apiRequest('POST', '/account/agents', body);
  console.log('✅ Agent erstellt:', JSON.stringify(res, null, 2));
  return res;
}

export async function getAgent(id) {
  console.log(`🤖 Abfrage Agent ${id}...`);
  const res = await apiRequest('GET', `/account/agents/${id}`);
  console.log('✅ Agent Info:', JSON.stringify(res, null, 2));
  return res;
}

export async function listMyModels() {
  console.log('🎨 Liste eigene Custom Models...');
  const res = await apiRequest('GET', '/account/my-models');
  console.log('✅ My Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function createMyModel(body = {}) {
  console.log('🎨 Registriere neues Custom Model...');
  const res = await apiRequest('POST', '/account/my-models', body);
  console.log('✅ Model registriert:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMyModel(id) {
  console.log(`🎨 Abfrage Custom Model ${id}...`);
  const res = await apiRequest('GET', `/account/my-models/${id}`);
  console.log('✅ Model Info:', JSON.stringify(res, null, 2));
  return res;
}

export async function updateMyModel(id, body = {}) {
  console.log(`🎨 Aktualisiere Custom Model ${id}...`);
  const res = await apiRequest('POST', `/account/my-models/${id}/update`, body);
  console.log('✅ Model aktualisiert:', JSON.stringify(res, null, 2));
  return res;
}

export async function deleteMyModel(id) {
  console.log(`🗑️ Lösche Custom Model ${id}...`);
  const res = await apiRequest('DELETE', `/account/my-models/${id}`);
  console.log('✅ Model gelöscht:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMyModelFallbackCandidates(id) {
  console.log(`🔄 Abfrage Fallback-Kandidaten für Model ${id}...`);
  const res = await apiRequest('GET', `/account/my-models/${id}/fallback-candidates`);
  console.log('✅ Fallback Candidates:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMyModelsProvider() {
  console.log('🏢 Abfrage Provider Settings für Custom Models...');
  const res = await apiRequest('GET', '/account/my-models/provider');
  console.log('✅ Provider Settings:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMyModelsAvailable() {
  console.log('📋 Abfrage verfügbare Base-Models für Custom Models...');
  const res = await apiRequest('GET', '/account/my-models/models');
  console.log('✅ Base Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMyModelsEndpointAgents() {
  console.log('🤖 Abfrage Endpoint-Agents für Custom Models...');
  const res = await apiRequest('GET', '/account/my-models/endpoint-agents');
  console.log('✅ Endpoint Agents:', JSON.stringify(res, null, 2));
  return res;
}

export async function testMyModel(body = {}) {
  console.log('🧪 Teste Custom Model Konfiguration...');
  const res = await apiRequest('POST', '/account/my-models/test', body);
  console.log('✅ Test Ergebnis:', JSON.stringify(res, null, 2));
  return res;
}

// ── 4. MODEL LISTINGS & STATUS ──

export async function listAllModels() {
  console.log('📋 Liste aller System-Modelle (/models)...');
  const res = await apiRequest('GET', '/models');
  console.log('✅ Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function listV1Models() {
  console.log('📋 Liste OpenAI-kompatibler Modelle (/v1/models)...');
  const res = await apiRequest('GET', '/v1/models');
  console.log('✅ V1 Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function getV1Model(model) {
  console.log(`📋 Info für V1 Model: ${model}...`);
  const res = await apiRequest('GET', `/v1/models/${encodeURIComponent(model)}`);
  console.log('✅ Model Info:', JSON.stringify(res, null, 2));
  return res;
}

export async function getV1ModelsStatus() {
  console.log('⚡ Live Status aller Modelle (/v1/models/status)...');
  const res = await apiRequest('GET', '/v1/models/status');
  console.log('✅ Models Status:', JSON.stringify(res, null, 2));
  return res;
}

export async function listTextModels() {
  console.log('📝 Text-Modelle (/text/models)...');
  const res = await apiRequest('GET', '/text/models');
  console.log('✅ Text Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function listImageModels() {
  console.log('🖼️ Bild-Modelle (/image/models)...');
  const res = await apiRequest('GET', '/image/models');
  console.log('✅ Image Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function listVideoModels() {
  console.log('🎬 Video-Modelle (/video/models)...');
  const res = await apiRequest('GET', '/video/models');
  console.log('✅ Video Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function listAudioModels() {
  console.log('🎵 Audio-Modelle (/audio/models)...');
  const res = await apiRequest('GET', '/audio/models');
  console.log('✅ Audio Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function list3DModels() {
  console.log('📦 3D-Modelle (/3d/models)...');
  const res = await apiRequest('GET', '/3d/models');
  console.log('✅ 3D Models:', JSON.stringify(res, null, 2));
  return res;
}

export async function listEmbeddingsModels() {
  console.log('🔢 Embeddings-Modelle (/embeddings/models)...');
  const res = await apiRequest('GET', '/embeddings/models');
  console.log('✅ Embeddings Models:', JSON.stringify(res, null, 2));
  return res;
}

// ── 5. TEXT & CHAT GENERATION ──

export async function simpleTextGenerate({ prompt, model, system, json, temperature, seed, stream }) {
  if (!prompt) {
    console.error('❌ Parameter --prompt erforderlich!');
    process.exit(1);
  }

  const queryParams = new URLSearchParams();
  if (model) queryParams.append('model', model);
  if (system) queryParams.append('system', system);
  if (json) queryParams.append('json', 'true');
  if (temperature !== undefined) queryParams.append('temperature', temperature);
  if (seed !== undefined) queryParams.append('seed', seed);
  if (stream) queryParams.append('stream', 'true');

  const endpoint = `/text/${encodeURIComponent(prompt)}?${queryParams.toString()}`;
  console.log(`📝 Simple Text GET Request: ${endpoint}...`);

  const res = await apiRequest('GET', endpoint);
  console.log('✅ Antwort:\n', typeof res === 'object' && res.raw ? res.raw : res);
  return res;
}

export async function simpleTextPost(body = {}) {
  console.log('📝 Simple Text POST Request (/text)...');
  const res = await apiRequest('POST', '/text', body);
  console.log('✅ Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

export async function chatCompletions(body = {}) {
  console.log('💬 OpenAI-kompatible Chat Completion (/v1/chat/completions)...');
  const res = await apiRequest('POST', '/v1/chat/completions', body);
  console.log('✅ Completion Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

// ── 6. IMAGE, VIDEO, 3D & MEDIA GENERATION ──

export async function generateImageGet({ prompt, model, width, height, seed, image, referenceImages, quality, outFile }) {
  if (!prompt) {
    console.error('❌ Parameter --prompt erforderlich!');
    process.exit(1);
  }

  const queryParams = new URLSearchParams();
  if (model) queryParams.append('model', model);
  if (width) queryParams.append('width', width);
  if (height) queryParams.append('height', height);
  if (seed !== undefined) queryParams.append('seed', seed);
  if (image) queryParams.append('image', image);
  if (referenceImages) queryParams.append('reference_images', referenceImages);
  if (quality) queryParams.append('quality', quality);

  const endpoint = `/image/${encodeURIComponent(prompt)}?${queryParams.toString()}`;
  console.log(`🖼️ Generiere Bild (GET): ${endpoint}...`);

  const res = await apiRequest('GET', endpoint, null, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_image_${Date.now()}.png`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ Bild gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  return res;
}

export async function generateImagesV1(body = {}) {
  console.log('🖼️ OpenAI-kompatible Image Generation (/v1/images/generations)...');
  const res = await apiRequest('POST', '/v1/images/generations', body);
  console.log('✅ Image Generation Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

export async function editImagesV1(body = {}) {
  console.log('✏️ OpenAI-kompatible Image Edits (/v1/images/edits)...');
  const res = await apiRequest('POST', '/v1/images/edits', body);
  console.log('✅ Image Edit Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

export async function generateVideoGet({ prompt, model, width, height, resolution, duration, aspectRatio, audio, seed, quality, image, referenceImages, outFile }) {
  if (!prompt) {
    console.error('❌ Parameter --prompt erforderlich!');
    process.exit(1);
  }

  const queryParams = new URLSearchParams();
  if (model) queryParams.append('model', model);
  if (width) queryParams.append('width', width);
  if (height) queryParams.append('height', height);
  if (resolution) queryParams.append('resolution', resolution);
  if (duration) queryParams.append('duration', duration);
  if (aspectRatio) queryParams.append('aspectRatio', aspectRatio);
  if (audio !== undefined) queryParams.append('audio', audio);
  if (seed !== undefined) queryParams.append('seed', seed);
  if (quality) queryParams.append('quality', quality);
  if (image) queryParams.append('image', image);
  if (referenceImages) queryParams.append('reference_images', referenceImages);

  const endpoint = `/video/${encodeURIComponent(prompt)}?${queryParams.toString()}`;
  console.log(`🎬 Generiere Video (GET): ${endpoint}...`);

  const res = await apiRequest('GET', endpoint, null, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_video_${Date.now()}.mp4`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ Video gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  return res;
}

export async function generate3DGet({ prompt, model, resolution, image, seed, outFile }) {
  if (!prompt && !image) {
    console.error('❌ Parameter --prompt oder --image erforderlich!');
    process.exit(1);
  }

  const queryParams = new URLSearchParams();
  if (model) queryParams.append('model', model);
  if (resolution) queryParams.append('resolution', resolution);
  if (image) queryParams.append('image', image);
  if (seed !== undefined) queryParams.append('seed', seed);

  const endpoint = `/3d/${encodeURIComponent(prompt || '')}?${queryParams.toString()}`;
  console.log(`📦 Generiere 3D Objekt (GET): ${endpoint}...`);

  const res = await apiRequest('GET', endpoint, null, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_3d_${Date.now()}.glb`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ 3D Objekt gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  return res;
}

/** POST variant of `/3d/{prompt}` — JSON body, supports `trellis-2` resolution tiers. */
export async function generate3DPost({ prompt, model, resolution, image, seed, outFile }) {
  if (!prompt && !image) {
    console.error('❌ Parameter --prompt oder --image erforderlich!');
    process.exit(1);
  }

  const body = {
    prompt: prompt || undefined,
    model: model || undefined,
    resolution: resolution || undefined,
    image: image || undefined,
    seed: seed !== undefined ? Number(seed) : undefined,
  };

  const endpoint = `/3d/${encodeURIComponent(prompt || '')}`;
  console.log(`📦 Generiere 3D Objekt (POST): ${endpoint}...`);

  const res = await apiRequest('POST', endpoint, body, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_3d_${Date.now()}.glb`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ 3D Objekt gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  console.log('✅ 3D Antwort:', JSON.stringify(res, null, 2));
  return res;
}

// ── 7. AUDIO, SPEECH, VOICE & EMBEDDINGS ──

export async function generateAudioGet({ text, model, instructions, voice, outFile }) {
  if (!text) {
    console.error('❌ Parameter --text erforderlich!');
    process.exit(1);
  }

  const selectedModel = model || 'grok-tts';

  const queryParams = new URLSearchParams();
  queryParams.append('model', selectedModel);
  if (voice) queryParams.append('voice', voice);
  if (instructions) queryParams.append('instructions', instructions);

  const endpoint = `/audio/${encodeURIComponent(text)}?${queryParams.toString()}`;
  console.log(`🎵 Generiere Audio/Speech (GET): ${endpoint}...`);

  const res = await apiRequest('GET', endpoint, null, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_audio_${Date.now()}.mp3`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ Audio gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  return res;
}

export async function generateSpeechV1(body = {}, outFile) {
  console.log('🎤 OpenAI-kompatible TTS Speech (/v1/audio/speech)...');
  const res = await apiRequest('POST', '/v1/audio/speech', body, {}, true);

  if (res.buffer) {
    const fileName = outFile || `pollinations_speech_${Date.now()}.mp3`;
    const savePath = path.resolve(process.cwd(), fileName);
    fs.writeFileSync(savePath, res.buffer);
    console.log(`✅ Speech Audio gespeichert: ${savePath} (${res.buffer.length} Bytes)`);
    return { savePath, buffer: res.buffer };
  }
  return res;
}

export async function generateSpeechWithTimestampsV1(body = {}) {
  console.log('⏱️ TTS Speech mit Wort-Zeitstempeln (/v1/audio/speech/with-timestamps)...');
  const res = await apiRequest('POST', '/v1/audio/speech/with-timestamps', body);
  console.log('✅ Timestamps Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

export async function voiceChangerV1(body = {}) {
  console.log('🎙️ Voice Changer (/v1/audio/voice-changer)...');
  const res = await apiRequest('POST', '/v1/audio/voice-changer', body);
  console.log('✅ Voice Changer Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

export async function voiceIsolatorV1(body = {}) {
  console.log('🎤 Voice Isolator (/v1/audio/voice-isolator)...');
  const res = await apiRequest('POST', '/v1/audio/voice-isolator', body);
  console.log('✅ Voice Isolator Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

/**
 * Transkribiert eine Audiodatei. WICHTIG: Der Endpunkt verlangt multipart/form-data —
 * mit JSON antwortet er "Invalid multipart form data" (HTTP 400). Diese Fassung schickt
 * die Datei daher als FormData; ein reiner JSON-Body wird weiterhin unterstützt.
 */
// optionale Zusatzfelder für /v1/audio/transcriptions, die je nach Modell greifen
// (u. a. Sprecher-Diarisierung bei elevenlabs/scribe-v2 via `diarize`).
const AUDIO_EXTRA_FIELDS = [
  'diarize',
  'speaker_labels',
  'timestamps',
  'language_code',
  'language',
  'prompt',
  'response_format',
];

export async function audioTranscriptionsV1(body = {}) {
  const filePath = body.filePath || body.file;
  const model = body.model || 'elevenlabs/scribe-v2';

  if (typeof filePath === 'string' && fs.existsSync(filePath)) {
    const ext = path.extname(filePath).toLowerCase();
    const mime =
      ext === '.wav' ? 'audio/wav' : ext === '.m4a' ? 'audio/mp4' : ext === '.ogg' ? 'audio/ogg' : 'audio/mpeg';
    console.log(`📝 Audio Transkription (multipart, ${model})...`);
    const form = new FormData();
    form.append('file', new Blob([fs.readFileSync(filePath)], { type: mime }), path.basename(filePath));
    form.append('model', model);
    for (const key of AUDIO_EXTRA_FIELDS) {
      const value = body[key];
      if (value !== undefined && value !== null && value !== false) form.append(key, String(value));
    }
    const response = await fetch(`${API_BASE}/v1/audio/transcriptions`, {
      method: 'POST',
      headers: API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {},
      body: form,
    });
    const json = await response.json().catch(() => null);
    console.log(`✅ HTTP ${response.status} · ${json?.usage?.seconds ?? '?'} s · ${json?.text?.length ?? 0} Zeichen`);
    return json;
  }

  console.log('📝 Audio Transkription (/v1/audio/transcriptions, JSON)...');
  const res = await apiRequest('POST', '/v1/audio/transcriptions', body);
  console.log('✅ Transkription Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

/** `transcribe` — eine Datei; gibt den Text aus oder schreibt ihn in eine Datei. */
async function transcribeCommand(options) {
  const file = options.file || options.input;
  if (!file) throw new Error('Parameter --file <pfad> ist erforderlich.');
  const result = await audioTranscriptionsV1({
    filePath: file,
    model: options.model,
    // --diarize / --speakers aktiviert Sprecher-Trennung (elevenlabs/scribe-v2).
    diarize: options.diarize ?? options.speakers,
    speaker_labels: options.speakerLabels ?? options.speaker_labels,
    language_code: options.languageCode ?? options.language,
    timestamps: options.timestamps,
    response_format: options.responseFormat ?? options.response_format,
  });
  // --json / --raw gibt die vollständige Antwort aus (z. B. Wort-Daten mit speaker_id).
  if (options.json || options.raw) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  const text = result?.text ?? '';
  if (!text) {
    if (result) console.log(JSON.stringify(result, null, 2));
    process.exitCode = 1;
    return;
  }
  const out = options.out || options.outFile;
  if (out) {
    fs.writeFileSync(out, text, 'utf-8');
    console.log(`✅ gespeichert: ${out}`);
  } else {
    console.log(text);
  }
}

/** `transcribe-album` — alle Audiodateien eines Ordners als .txt (Quelle bleibt unberührt). */
async function transcribeAlbumCommand(options) {
  const dir = options.dir || options.input;
  if (!dir || !fs.existsSync(dir)) throw new Error(`Ordner nicht gefunden: ${dir}`);
  const outDir = options.out || path.join(dir, 'transcripts');
  fs.mkdirSync(outDir, { recursive: true });

  const files = fs
    .readdirSync(dir)
    .filter((f) => /\.(mp3|wav|m4a|ogg)$/i.test(f))
    .sort();

  console.log(`🎧 ${files.length} Dateien · Modell ${options.model || 'elevenlabs/scribe-v2'}\nZiel: ${outDir}\n`);
  let ok = 0;
  let failed = 0;
  for (const name of files) {
    try {
      const result = await audioTranscriptionsV1({ filePath: path.join(dir, name), model: options.model });
      const text = result?.text ?? '';
      if (!text) throw new Error('kein Text');
      fs.writeFileSync(path.join(outDir, name.replace(/\.[^.]+$/, '.txt')), text, 'utf-8');
      ok++;
      console.log(`  OK  ${String(result?.usage?.seconds ?? '?').padStart(6)}s  ${String(text.length).padStart(5)} Zeichen  ${name}`);
    } catch (error) {
      failed++;
      console.log(`  FEHLER  ${name}: ${error.message}`);
    }
    await new Promise((r) => setTimeout(r, 1200));
  }
  console.log(`\nFertig: ${ok} geschrieben, ${failed} fehlgeschlagen.`);
}

export async function createEmbeddingsV1(body = {}) {
  console.log('🔢 Vector Embeddings (/v1/embeddings)...');
  const res = await apiRequest('POST', '/v1/embeddings', body);
  console.log('✅ Embeddings Antwort:\n', JSON.stringify(res, null, 2));
  return res;
}

// ── 8. MEDIA UPLOAD, GALLERIES & STORAGE ──

/** Best-effort MIME type for `/upload` (multipart needs a real content type). */
function mimeTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  const map = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.avif': 'image/avif',
    '.mp3': 'audio/mpeg',
    '.wav': 'audio/wav',
    '.m4a': 'audio/mp4',
    '.ogg': 'audio/ogg',
    '.flac': 'audio/flac',
    '.mp4': 'video/mp4',
    '.webm': 'video/webm',
    '.mov': 'video/quicktime',
    '.glb': 'model/gltf-binary',
  };
  return map[ext] || 'application/octet-stream';
}

/**
 * Upload a local file to `/upload`.
 *
 * The docs accept both `multipart/form-data` (field `file`) and a JSON body
 * with a base64 `data` string. Multipart is the default because it streams
 * large media without inflating it by ~33%; pass `multipart: false` (CLI:
 * `--json true`) to force the base64 form. An optional `tags` value publishes
 * the upload into each tag's public gallery.
 */
export async function uploadMediaFile(filePath, tags = '', { multipart = true } = {}) {
  if (!filePath || !fs.existsSync(filePath)) {
    console.error(`❌ Lokale Datei nicht gefunden: ${filePath}`);
    process.exit(1);
  }

  if (multipart) {
    try {
      console.log(`📤 Lade Datei hoch (multipart): ${filePath}...`);
      const form = new FormData();
      form.append(
        'file',
        new Blob([fs.readFileSync(filePath)], { type: mimeTypeFor(filePath) }),
        path.basename(filePath)
      );
      if (tags) form.append('tags', tags);

      const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        headers: {
          ...(SAFE_MODE === undefined ? { safe: 'false' } : { safe: SAFE_MODE }),
          ...(API_KEY ? { Authorization: `Bearer ${API_KEY}` } : {}),
        },
        body: form,
      });
      const json = await response.json().catch(() => null);
      console.log(`✅ HTTP ${response.status} · Upload Antwort:`, JSON.stringify(json, null, 2));
      if (response.ok) return json;
      console.warn('⚠️ Multipart-Upload fehlgeschlagen, versuche Base64-JSON-Fallback...');
    } catch (error) {
      console.warn(`⚠️ Multipart-Upload fehlgeschlagen (${error.message}), versuche Base64-JSON-Fallback...`);
    }
  }

  const base64Data = fs.readFileSync(filePath).toString('base64');
  console.log(`📤 Lade Datei hoch (base64 JSON): ${filePath}...`);
  const body = {
    data: `data:${mimeTypeFor(filePath)};base64,${base64Data}`,
    tags: tags || undefined,
  };

  const res = await apiRequest('POST', '/upload', body);
  console.log('✅ Upload Antwort:', JSON.stringify(res, null, 2));
  return res;
}

export async function listMediaGallery(tag, limit = 20, cursor = '') {
  if (!tag) {
    console.error('❌ Parameter --tag erforderlich!');
    process.exit(1);
  }

  const queryParams = new URLSearchParams({ tag, limit });
  if (cursor) queryParams.append('cursor', cursor);

  console.log(`🖼️ Abfrage öffentliche Tag-Galerie (${tag})...`);
  const res = await apiRequest('GET', `/media?${queryParams.toString()}`);
  console.log('✅ Galerie:', JSON.stringify(res, null, 2));
  return res;
}

export async function getMediaItem(id) {
  console.log(`🖼️ Abfrage Media Item ${id}...`);
  const res = await apiRequest('GET', `/media/${id}`);
  console.log('✅ Media Info:', JSON.stringify(res, null, 2));
  return res;
}

export async function getStorageItem(id) {
  console.log(`📦 Abfrage Storage Item ${id}...`);
  const res = await apiRequest('GET', `/${id}`);
  console.log('✅ Storage Item:', JSON.stringify(res, null, 2));
  return res;
}

export async function getStorageItemMetadata(id) {
  console.log(`🏷️ Abfrage Storage Item Metadaten ${id}...`);
  const res = await apiRequest('GET', `/${id}/metadata`);
  console.log('✅ Storage Metadata:', JSON.stringify(res, null, 2));
  return res;
}

// ── 9. REALTIME API ──

export async function getRealtimeConfig() {
  console.log('⚡ Abfrage Realtime API Endpoint...');
  const res = await apiRequest('GET', '/realtime');
  console.log('✅ Realtime Config:', JSON.stringify(res, null, 2));
  return res;
}

export async function getV1RealtimeConfig() {
  console.log('⚡ Abfrage V1 Realtime API Endpoint...');
  const res = await apiRequest('GET', '/v1/realtime');
  console.log('✅ V1 Realtime Config:', JSON.stringify(res, null, 2));
  return res;
}

// ── 📖 HELP & CLI PARSER ──

function showHelp() {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║  🌺 Echo's Pollinations API Client (Full 54-Endpoint)    ║
╚══════════════════════════════════════════════════════════╝

Verwendung:
  node pollinations-client.mjs <command> [options]

Global options (every command):
  --apiKey <key>     Credential überschreiben (sonst .env / Umgebung)
  --base <url>       API-Basis überschreiben (Default https://gen.pollinations.ai)
  --safe <spec>      Safe-Mode; ersetzt den Default, z. B. --safe true
  --body <json|@f>   JSON-Body für POST-Commands (restliche --flags mergen hinein)

Generation:
  text               📝 Simple Text GET (/text/{prompt})
  text-post          📝 Simple Text POST (/text)
  chat               💬 Chat Completion (/v1/chat/completions)
  image              🖼️ Bild GET (/image/{prompt})
  image-v1           🖼️ Bild OpenAI-style POST (/v1/images/generations)
  image-edit         ✏️ Bild bearbeiten POST (/v1/images/edits)
  video              🎬 Video GET (/video/{prompt})
  3d                 📦 3D GET (/3d/{prompt})
  3d-post            📦 3D POST (/3d/{prompt})
  audio              🎵 Audio/Speech GET (/audio/{text})
  speech             🎤 TTS POST (/v1/audio/speech)
  speech-timestamps  ⏱️ TTS mit Wort-Zeitstempeln (/v1/audio/speech/with-timestamps)
  voice-changer      🎙️ Voice Changer (/v1/audio/voice-changer)
  voice-isolator     🎤 Voice Isolator (/v1/audio/voice-isolator)
  transcribe         📝 Audio transkribieren (--file <pfad> [--model] [--out <txt>] [--diarize] [--responseFormat <fmt>] [--json])
  transcribe-album   🎧 Alle Audios eines Ordners in .txt (--dir <ordner> [--model] [--out <ordner>])
  transcriptions     📝 Transkription JSON-Body (/v1/audio/transcriptions)
  embeddings         🔢 Vector Embeddings (/v1/embeddings)

Media & Storage:
  upload-media       📤 Datei hochladen (/upload) (--file <pfad> [--tags a,b] [--json true])
  gallery            🖼️ Tag-Galerie (/media?tag=…) (--tag <t> [--limit N] [--cursor c])
  media-item <id>    🖼️ Media Item Info (/media/{id})
  storage-item <id>  📦 Storage Item Info (/{id})
  storage-meta <id>  🏷️ Storage Metadaten (/{id}/metadata)

Account & Keys:
  account-profile    👤 Profil (/account/profile)
  account-balance    💰 Kontostand (/account/balance)
  account-usage      📊 Verbrauch (/account/usage)
  account-daily      📅 Tägliche Historie (/account/usage/daily)
  account-quests     📜 User Quests (/account/quests)
  quests-catalog     📖 Quests Katalog (/quests/catalog)
  earnings           💎 Earnings (/account/earnings)
  earnings-transactions  💸 Earnings-Transaktionen (/account/earnings/transactions)
  keys               🔑 API Keys auflisten (/account/keys)
  key-create         🔑 API Key erstellen (/account/keys)
  key-info <id>      🔑 Key-Details (/account/keys/{id})
  key-delete <id>    🗑️ Key löschen (/account/keys/{id})
  key-usage          📊 Key-Verbrauch (/account/key/usage)
  key-current        🔑 Aktueller Key (/account/key)

Agents & Custom Models:
  agents             🤖 Agents (/account/agents)
  agent-create       🤖 Agent erstellen (--body '{...}')
  agent-info <id>    🤖 Agent Info (/account/agents/{id})
  my-models          🎨 Eigene Custom Models (/account/my-models)
  my-model-create    🎨 Custom Model registrieren (--body '{...}')
  my-model-info <id> 🎨 Custom Model Info (/account/my-models/{id})
  my-model-update <id>  🎨 Model aktualisieren (--body '{...}')
  my-model-delete <id>  🗑️ Model löschen (/account/my-models/{id})
  my-model-fallback <id>  🔄 Fallback-Kandidaten
  my-model-endpoints 🤖 Endpoint-Agents
  my-model-test      🧪 Model-Konfiguration testen
  my-models-provider 🏢 Provider-Settings
  my-models-base     📋 Verfügbare Base-Models

Models & Realtime:
  models             📋 Alle Modelle (/models)
  v1-models          📋 OpenAI Modelle (/v1/models)
  v1-model <id>      📋 Model-Details (/v1/models/{model})
  models-status      ⚡ Live-Status (/v1/models/status)
  text-models        📝 (/text/models)   image-models  🖼️ (/image/models)
  video-models       🎬 (/video/models)  audio-models  🎵 (/audio/models)
  3d-models          📦 (/3d/models)     embeddings-models 🔢 (/embeddings/models)
  realtime           ⚡ (/realtime)       v1-realtime   ⚡ (/v1/realtime)

Examples:
  node pollinations-client.mjs text --prompt "Erkläre Quantencomputing in 2 Sätzen"
  node pollinations-client.mjs chat --body '{"model":"openai","messages":[{"role":"user","content":"Hi"}]}'
  node pollinations-client.mjs image --prompt "Futuristic Cyberpunk Neon Cathedral" --model "zimage"
  node pollinations-client.mjs video --prompt "Neon city flythrough" --model "wan-fast" --duration 5
  node pollinations-client.mjs speech --input "Willkommen bei Echo Forge!" --voice "liora"
  node pollinations-client.mjs upload-media --file ./cat.png --tags demo
  node pollinations-client.mjs models-status
`);
}

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

/**
 * Build a JSON request body from CLI options.
 *
 * `--body '<json>'` (or `--body @file.json`) seeds the body; every other
 * `--key value` flag then overrides/extends it. `--body` wins over a scalar of
 * the same name, so `--body '{"stream":true}'` cannot be clobbered by a stray
 * `--stream` flag. Scaffolding flags (`apiKey`, `base`, `safe`, `out`, …) are
 * never sent upstream.
 */
/** Flags that configure the client itself and must never reach the API. */
const GLOBAL_OPTIONS = new Set(['body', 'id', 'apiKey', 'base', 'safe']);

/** Local-file / output plumbing that belongs to no request body. */
const SCAFFOLDING_OPTIONS = new Set([
  ...GLOBAL_OPTIONS,
  'out',
  'outFile',
  'filePath',
  'file',
  'dir',
  'input',
  'responseFormat',
]);

/** Query-string view of the CLI options, with client-only flags removed. */
function queryFromOptions(options = {}) {
  const query = {};
  for (const [key, value] of Object.entries(options)) {
    if (GLOBAL_OPTIONS.has(key)) continue;
    query[key] = value === true ? 'true' : String(value);
  }
  return query;
}

/** Accepts both `--out` and `--outFile` for the generators' target path. */
function withOutFile(options = {}) {
  return { ...options, outFile: options.outFile || options.out }
}

function bodyFromOptions(options = {}) {
  let base = {};
  if (typeof options.body === 'string') {
    const source = options.body.startsWith('@')
      ? fs.readFileSync(options.body.slice(1), 'utf-8')
      : options.body;
    base = JSON.parse(source);
  }
  const body = { ...base };
  for (const [key, value] of Object.entries(options)) {
    if (SCAFFOLDING_OPTIONS.has(key)) continue;
    if (key in base) continue;
    body[key] = value === true ? true : value;
  }
  return body;
}

async function main() {
  const { command, options, rawArgs } = parseArgs();

  // Global overrides, applied before any command runs:
  //   --apiKey <key>   override the .env / environment credential
  //   --base <url>     point at a mirror (default https://gen.pollinations.ai)
  //   --safe <spec>    replace the Safe-Mode default with the `safe` header
  if (typeof options.apiKey === 'string') API_KEY = options.apiKey;
  if (typeof options.base === 'string') API_BASE = options.base;
  if (options.safe !== undefined) {
    SAFE_MODE = options.safe === false ? 'false' : String(options.safe);
  }

  try {
    switch (command) {
      // ── Generation ──
      case 'text':
        await simpleTextGenerate(options);
        break;
      case 'text-post':
        await simpleTextPost(bodyFromOptions(options));
        break;
      case 'chat':
        await chatCompletions(bodyFromOptions(options));
        break;
      case 'image':
        await generateImageGet(withOutFile(options));
        break;
      case 'image-v1':
        await generateImagesV1(bodyFromOptions(options));
        break;
      case 'image-edit':
        await editImagesV1(bodyFromOptions(options));
        break;
      case 'video':
        await generateVideoGet(withOutFile(options));
        break;
      case '3d':
        await generate3DGet(withOutFile(options));
        break;
      case '3d-post':
        await generate3DPost(withOutFile(options));
        break;
      case 'audio':
        await generateAudioGet(withOutFile(options));
        break;
      case 'speech':
        await generateSpeechV1(bodyFromOptions(options), options.out || options.outFile);
        break;
      case 'speech-timestamps':
        await generateSpeechWithTimestampsV1(bodyFromOptions(options));
        break;
      case 'voice-changer':
        await voiceChangerV1(bodyFromOptions(options));
        break;
      case 'voice-isolator':
        await voiceIsolatorV1(bodyFromOptions(options));
        break;
      case 'transcribe':
        await transcribeCommand(options);
        break;
      case 'transcribe-album':
        await transcribeAlbumCommand(options);
        break;
      case 'embeddings':
        await createEmbeddingsV1(bodyFromOptions(options));
        break;
      case 'transcriptions':
        await audioTranscriptionsV1(options);
        break;

      // ── Media & Storage ──
      case 'upload-media':
        await uploadMediaFile(options.filePath || options.file, options.tags, {
          multipart: options.json !== true,
        });
        break;
      case 'gallery':
        await listMediaGallery(options.tag, options.limit, options.cursor);
        break;
      case 'media-item':
        await getMediaItem(rawArgs[1] || options.id);
        break;
      case 'storage-item':
        await getStorageItem(rawArgs[1] || options.id);
        break;
      case 'storage-meta':
        await getStorageItemMetadata(rawArgs[1] || options.id);
        break;

      // ── Account & Keys ──
      case 'account-profile':
        await getAccountProfile();
        break;
      case 'account-balance':
        await getAccountBalance();
        break;
      case 'account-usage':
        await getAccountUsage(queryFromOptions(options));
        break;
      case 'account-daily':
        await getAccountUsageDaily(queryFromOptions(options));
        break;
      case 'account-quests':
        await getAccountQuests();
        break;
      case 'quests-catalog':
        await getQuestsCatalog();
        break;
      case 'earnings':
        await getAccountEarnings();
        break;
      case 'earnings-transactions':
        await getAccountEarningsTransactions(queryFromOptions(options));
        break;
      case 'keys':
        await listApiKeys();
        break;
      case 'key-create':
        await createApiKey(bodyFromOptions(options));
        break;
      case 'key-info':
        await getApiKey(rawArgs[1] || options.id);
        break;
      case 'key-delete':
        await deleteApiKey(rawArgs[1] || options.id);
        break;
      case 'key-usage':
        await getAccountKeyUsage(queryFromOptions(options));
        break;
      case 'key-current':
        await getAccountKey();
        break;

      // ── Agents & Custom Models ──
      case 'agents':
        await listAgents();
        break;
      case 'agent-create':
        await createAgent(bodyFromOptions(options));
        break;
      case 'agent-info':
        await getAgent(rawArgs[1] || options.id);
        break;
      case 'my-models':
        await listMyModels();
        break;
      case 'my-model-create':
        await createMyModel(bodyFromOptions(options));
        break;
      case 'my-model-info':
        await getMyModel(rawArgs[1] || options.id);
        break;
      case 'my-model-update':
        await updateMyModel(rawArgs[1] || options.id, bodyFromOptions(options));
        break;
      case 'my-model-delete':
        await deleteMyModel(rawArgs[1] || options.id);
        break;
      case 'my-model-fallback':
        await getMyModelFallbackCandidates(rawArgs[1] || options.id);
        break;
      case 'my-model-endpoints':
        await getMyModelsEndpointAgents();
        break;
      case 'my-model-test':
        await testMyModel(bodyFromOptions(options));
        break;
      case 'my-models-provider':
        await getMyModelsProvider();
        break;
      case 'my-models-base':
        await getMyModelsAvailable();
        break;

      // ── Models & Status ──
      case 'models':
        await listAllModels();
        break;
      case 'v1-models':
        await listV1Models();
        break;
      case 'v1-model':
        await getV1Model(rawArgs[1] || options.model);
        break;
      case 'models-status':
        await getV1ModelsStatus();
        break;
      case 'text-models':
        await listTextModels();
        break;
      case 'image-models':
        await listImageModels();
        break;
      case 'video-models':
        await listVideoModels();
        break;
      case 'audio-models':
        await listAudioModels();
        break;
      case '3d-models':
        await list3DModels();
        break;
      case 'embeddings-models':
        await listEmbeddingsModels();
        break;
      case 'realtime':
        await getRealtimeConfig();
        break;
      case 'v1-realtime':
        await getV1RealtimeConfig();
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
