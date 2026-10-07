> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Recovery Audio

> Recover playable audio links for an existing music generation task.

Used to recover playable audio links for a music generation task that has already completed. Submit the `sunoTaskId` of the original task and the service regenerates accessible audio URLs for every track that belongs to it.

## 🚀 User Guide

* Suno's original links are only valid for a limited period of time. Once they expire, the audio can no longer be played or downloaded from those URLs.
* Submit the `sunoTaskId` of the original music generation task — all tracks of that task are recovered together.
* This endpoint only creates the task: it returns a recovery `task_id` immediately and the recovery itself runs asynchronously.
* The result is pushed to `callBackUrl` when the task finishes, and can also be read by polling [Get Recovery Audio Details](/suno-api/get-recovery-audio-details).

<Warning>
  **`source_audio_url` is deprecated.**

  `source_audio_url` in the generation responses and callbacks points to Suno's original file. That link expires after a period of time and is no longer maintained, so it must not be stored for long-term use. Call this endpoint to obtain a fresh playable link instead.
</Warning>

## 📌 Usage Scenarios

* 🔗 Restoring playback for songs that were generated a long time ago
* 📦 Refreshing audio links before archiving or migrating your own library
* 🛠️ Repairing broken audio URLs reported by your end users

## ⚠️ Notes

* `sunoTaskId` in the request body is the **music generation task ID** (for example the one returned by [Generate Music](/suno-api/generate-music)), not the ID returned by this endpoint.
* The `task_id` in the response is the **recovery task ID** and is only accepted by [Get Recovery Audio Details](/suno-api/get-recovery-audio-details).
* `callBackUrl` is required. The recovery result is pushed to it once the task finishes.
* Creating the task successfully does not guarantee that every track can be recovered — check the final result for the per-track `status`.

## 📩 Callback

Once the recovery task finishes, a `POST` request is sent to `callBackUrl`:

```json theme={null}
{
  "code": 200,
  "msg": "success",
  "task_id": "bbbb****0f7b",
  "data": [
    {
      "id": "3bc3****48fc",
      "audio_url": "https://example.com/****.m4a",
      "title": "Sunrise Love",
      "status": "success",
      "error": ""
    }
  ]
}
```

The task level `code` is `200` when at least one track was recovered, and `500` when all of them failed. The order of `data` matches the tracks of the original task.


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/suno/recovery
openapi: 3.0.0
info:
  title: intro
  description: API documentation for audio generation services
  version: 1.0.0
  contact:
    name: Technical Support
    email: support@api.box
servers:
  - url: https://apibox.erweima.ai
    description: API Server
security:
  - BearerAuth: []
tags:
  - name: Music Generation
    description: Endpoints for creating and managing music generation tasks
  - name: Lyrics Generation
    description: Endpoints for lyrics generation and management
  - name: WAV Conversion
    description: Endpoints for converting music to WAV format
  - name: Vocal Removal
    description: Endpoints for vocal removal from music tracks
  - name: Music Video Generation
    description: Endpoints for generating MP4 videos from music tracks
  - name: Account Management
    description: Endpoints for account and credits management
paths:
  /api/v1/suno/recovery:
    post:
      summary: Recovery Audio
      description: >-
        Recover playable audio links for a music generation task that has
        already completed.


        ## User Guide

        - Suno's original links (`source_audio_url`) are only valid for a
        limited period of time and are deprecated.

        - Submit the `sunoTaskId` of the original music generation task; every
        track of that task is recovered together.

        - This endpoint only creates the task and returns immediately. The
        result is pushed to the required `callBackUrl`, and can also be read by
        polling `Get Recovery Audio Details`.
      operationId: recovery-audio
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - sunoTaskId
                - callBackUrl
              properties:
                sunoTaskId:
                  type: string
                  description: >-
                    The task ID of the original music generation task whose
                    audio links need to be recovered.
                  example: 5c79****be8e
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL notified when the recovery task finishes. The
                    recovery result is pushed to this address.
                  example: https://api.example.com/callback
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/ApiResponse'
                  - type: object
                    properties:
                      data:
                        type: object
                        properties:
                          task_id:
                            type: string
                            description: >-
                              Recovery task ID. Use it with the Get Recovery
                              Audio Details endpoint.
                            example: dc19****18b3
        '500':
          $ref: '#/components/responses/Error'
components:
  schemas:
    ApiResponse:
      type: object
      properties:
        code:
          type: integer
          description: |-
            # Status Codes

            - ✅ 200 - Request successful
            - ⚠️ 400 - Invalid parameters
            - ⚠️ 401 - Unauthorized access
            - ⚠️ 404 - Invalid request method or path
            - ⚠️ 405 - Rate limit exceeded
            - ⚠️ 413 - Theme or prompt too long
            - ⚠️ 429 - Insufficient credits
            - ⚠️ 430 - Your call frequency is too high. Please try again later.
            - ⚠️ 455 - System maintenance
            - ❌ 500 - Server error
          example: 200
          enum:
            - 200
            - 400
            - 401
            - 404
            - 405
            - 413
            - 429
            - 430
            - 455
            - 500
        msg:
          type: string
          description: Error message when code != 200
          example: success
  responses:
    Error:
      description: Server error
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API Key
      description: >-
        # 🔑 API Authentication


        All endpoints require authentication using Bearer Token.


        ## Get API Key


        1. Visit the [API Key Management Page](https://api.box/api-key) to
        obtain your API Key


        ## Usage


        Add to request headers:


        ```

        Authorization: Bearer YOUR_API_KEY

        ```


        > **⚠️ Note:**

        > - Keep your API Key secure and do not share it with others

        > - If you suspect your API Key has been compromised, reset it
        immediately from the management page

````