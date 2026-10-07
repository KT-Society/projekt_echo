# Endpoint: /v1/images/edits\n\n## Method: POST\n\n**Summary:** Edit Image (OpenAI-compatible)\n\n**Description:** OpenAI-compatible image editing endpoint.

Edit images using a text prompt and one or more source images.
Accepts JSON with image URLs or multipart/form-data with file uploads.
Community image models forward edits to the registrant's OpenAI-compatible endpoint as multipart form data.

**Authentication:** Include your API key as `Authorization: Bearer YOUR_API_KEY`.\n\n