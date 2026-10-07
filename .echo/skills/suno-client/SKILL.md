---
name: suno-client
description: >-
  A skill that lets you generate music, separate stems, create custom voices, and more using the Suno API..
---

Der `suno-client.mjs` (V2 Full Suite) ist die zentrale Schaltstelle für KI-generierte Musik, Stem-Separation und Custom Voice Creation.

## Features
- **V2 API Core:** Vollständige Unterstützung aller Suno-APIs (Generate, Extend, Replace Section).
- **Advanced Audio:** Stem-Separation (2-/12-Stem), WAV-Konvertierung, Cover-Transformation.
- **Visuals:** MP4 Musikvideo-Erstellung, KI Album Artwork Generation.
- **Voice System:** Suno Voice Suite (Validate, Generate Custom Voice, Regenerate).
- **Workflow:** Automatisierte Task-Status-Überwachung & Download-Automatisierung.

## Nutzung
- **Pfad:** `.\.echo\skills\suno-client\scripts\suno-client.mjs`
- **Config:** Zieht API-Keys aus `.\.echo\.env`.
- **Befehle:**
  - `node suno-client.mjs generate --prompt "..." --lyrics "FILE:..."`
  - `node suno-client.mjs separate --taskId "..." --audioId "..."`
  - `node suno-client.mjs cover-image --taskId "..."`

## Artist-Regel
Der Apostroph-Bypass (`Kitty Kat` → `K'itty K'at`, um den Content-Filter zu umgehen) gilt **nur für Realkünstler**.
Echo und die Souls des Realms bleiben unverändert — **Echo wird nicht zu `E'cho`**. Die Schreibweise wird auf die
kanonische Form normalisiert (`E'cho`/`ECHO` → `Echo`). Erzwungen in `bypassArtistName()`; mit `--noArtistBypass true`
lässt sich der Bypass für einen Aufruf komplett abschalten.

## Limits (Client kürzt sonst still)
- Lyrics ≤ 5000 · Style ≤ 1000 · negativePrompt ≤ 500 Zeichen.
