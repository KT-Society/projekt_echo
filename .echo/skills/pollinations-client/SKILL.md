---
name: pollinations-client
description: >-
  A skill that lets you generate images, videos, audio, 3D models, and more using the Pollinations API.
---

Der `pollinations-client.mjs` ist die zentrale Schnittstelle für alle generative KI-Aufgaben im Pollinations-Ökosystem.

Zusätzlich ist Pollinations als **nativer Provider** in der Jan-Codebase verdrahtet
(`web-app/src/constants/providers.ts`, `provider: 'pollinations'`, `base_url: https://gen.pollinations.ai/v1`) —
mit Modell-Katalog, Provider-Caps, Logo und Titel, genau wie die übrigen Built-in-Provider.

## Features
- Vollständige 54-Endpoint-Abdeckung für Text, Bild, Video, Audio, 3D, Embeddings, Upload/Media, Account, Keys, Agents und Custom Models.
- Standardmäßiger Safe-Mode (`nsfw: true`); per `--safe <spec>` oder `POLLINATIONS_SAFE` überschreibbar.
- On-Demand Asset-Generierung (Just-in-Time) inkl. Binär-Download (`.png`, `.mp4`, `.glb`, `.mp3`, …).
- Multipart-Upload mit Base64-Fallback; Tag-Veröffentlichung in die öffentliche Galerie.
- Support für alle TTS-Voices (Grok, ElevenLabs, Fish Audio, Kokoro, Qwen, …) mit Speech-Tags (`[expr]`, `<style>`).
- JSON-Body-Support für alle POST-Endpunkte via `--body '<json>'` oder `--body @file.json`.

## Nutzung
- **Pfad:** `.\.echo\skills\pollinations-client\scripts\pollinations-client.mjs`
- **Config:** Zieht API-Keys aus `.\.echo\.env` (`POLLINATIONS_API_KEY`).
- **Referenz:** Alle Endpunkte/Parameter in `.\pollinationsai-documentation\` (`summary.md` = Endpunkt-Index).
- **Befehle (Auswahl):**
  - `node pollinations-client.mjs text --prompt "Hallo Echo" --model "deepseek"`
  - `node pollinations-client.mjs chat --body '{"model":"openai","messages":[{"role":"user","content":"Hi"}]}'`
  - `node pollinations-client.mjs image --prompt "Cyberpunk Neon City" --model "zimage"`
  - `node pollinations-client.mjs video --prompt "Neon flythrough" --model "wan-fast" --duration 5`
  - `node pollinations-client.mjs 3d --prompt "low-poly fox" --model "trellis-2"`
  - `node pollinations-client.mjs audio --text "Hallo Welt" --voice "liora"`
  - `node pollinations-client.mjs speech --input "Willkommen!" --voice "iris" --out out.mp3`
  - `node pollinations-client.mjs upload-media --file ./cat.png --tags demo`
  - `node pollinations-client.mjs models-status`
  - `node pollinations-client.mjs help` — vollständige Befehlsliste

## Globale Flags
- `--apiKey <key>` — Credential überschreiben (sonst `.env`/Umgebung).
- `--base <url>` — API-Basis überschreiben (Default `https://gen.pollinations.ai`).
- `--safe <spec>` — Safe-Mode (`privacy,secrets`, `sexual,violence`, `true`, `nsfw`).
- `--body <json|@file>` — JSON-Body für POST-Commands; übrige `--flags` mergen hinein.
