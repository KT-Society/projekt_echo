# Endpoint: /v1/audio/transcriptions\n\n## Method: POST\n\n**Summary:** Transcribe Audio\n\n**Description:** Transcribe audio files to text. Compatible with the OpenAI Whisper API.

**Supported audio formats:** mp3, mp4, mpeg, mpga, m4a, wav, webm

**Models:**
- `whisper-large-v3` (default) — OpenAI Whisper via OVHcloud
- `whisper-1` — Alias for whisper-large-v3
- `gpt-transcribe` — Fast multilingual speech recognition with prompt context
- `scribe` — ElevenLabs Scribe (90+ languages, word-level timestamps)
- `grok-transcribe` — xAI speech recognition with word timestamps, speaker labels, and text formatting
- `universal-2` — AssemblyAI Universal-2 (99 languages)
- `universal-3.5-pro` — AssemblyAI Universal-3.5 Pro (18 languages, code switching, prompting)\n\n