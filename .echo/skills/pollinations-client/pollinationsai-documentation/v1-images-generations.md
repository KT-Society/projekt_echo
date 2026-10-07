# Endpoint: /v1/images/generations\n\n## Method: POST\n\n**Summary:** Generate Image (OpenAI-compatible)\n\n**Description:** OpenAI-compatible image generation endpoint.

Generate images from text prompts. Supports `response_format: "url"` (returns a pollinations.ai URL) or `"b64_json"` (returns base64-encoded image data, default).

**Authentication:** Include your API key as `Authorization: Bearer YOUR_API_KEY`.\n\n