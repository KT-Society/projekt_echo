# Endpoint: /v1/embeddings\n\n## Method: POST\n\n**Summary:** Create Embeddings\n\n**Description:** Generate vector embeddings with an OpenAI-compatible response format.

**Models:** `gemini-2` supports text, image, audio, and video. `cohere-embed-v4` supports text and one image. OpenAI and Qwen embedding models are text-only.

**Input:** Pass a string, an array of up to 32 strings, or supported multimodal content parts (`text`, `image_url`, `input_audio`, `video_url`) in the `input` field.

**Retrieval roles:** Use `task_type` with Gemini text input; it is converted to the model's recommended prompt instruction. Use `input_type` (`query` or `document`) with Cohere.

**Billing:** Gemini task instructions count toward prompt token usage. Cohere image requests expose one combined usage count, so text accompanying an image is billed at the image-input rate.

**Gemini migration:** `gemini-2` uses the GA embedding space. Do not mix preview-era and GA vectors; re-embed stored `gemini-2` data before comparing it with new results.

**Dimensions:** Defaults are model-specific. Qwen supports up to 4096; Gemini and OpenAI large up to 3072; OpenAI small up to 1536; Cohere supports 256, 512, 1024, or 1536.\n\n