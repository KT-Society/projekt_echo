# Endpoint: /v1/realtime\n\n## Method: GET\n\n**Summary:** Realtime WebSocket\n\n**Description:** OpenAI-compatible Realtime WebSocket for voice, multimodal, and transcription sessions.

Connect with `wss://gen.pollinations.ai/v1/realtime?model=gpt-realtime-2.1` and send/receive OpenAI Realtime JSON events over the socket. Selecting `scribe-realtime` creates a transcription session automatically.
Server clients can authenticate with `Authorization: Bearer <key>`. Browser WebSocket clients can use `?key=pk_...` because they cannot set custom authorization headers.

**Models:** `gpt-realtime-2.1`, `gpt-realtime-2.1-mini`, `gpt-realtime-2`, `scribe-realtime`, `gpt-live-transcribe`.

**Billing:** requires a positive balance and settles one session total when the socket closes.\n\n### Parameters\n\n- **model** (query): Realtime model to use. Supported models: gpt-realtime-2.1, gpt-realtime-2.1-mini, gpt-realtime-2, scribe-realtime, gpt-live-transcribe.\n- **key** (query): Pollinations API key. Useful for browser WebSocket clients that cannot set custom Authorization headers.\n\n