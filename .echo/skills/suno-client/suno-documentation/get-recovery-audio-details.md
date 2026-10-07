> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Get Recovery Audio Details

> Query the status and recovered audio links of a recovery task.

Query a recovery task created by [Recovery Audio](/suno-api/recovery-audio) and read the recovered audio links.

### Status Descriptions

* `201` — the recovery task is still running, keep polling
* `200` — the recovery finished and at least one track was recovered successfully
* `500` — every track failed to recover

### Per-track `status`

* `success` — `audio_url` carries the recovered playable link
* `failed` — `audio_url` is empty and `error` explains the reason

Common `error` values:

| Value                   | Meaning                                             |
| ----------------------- | --------------------------------------------------- |
| `no_audio_id_mappings`  | The track cannot be found for this task             |
| `account_missing`       | The source account is unavailable                   |
| `get_tokens_failed`     | Failed to authenticate against the upstream service |
| `feed_failed`           | Failed to query the track from the upstream service |
| `clip_error`            | The upstream track is in an error state             |
| `clip_not_complete`     | The upstream track is not finished yet              |
| `mango_transfer_failed` | Failed to transfer the recovered file               |

### Developer Notes

* Poll this endpoint instead of waiting for the callback when you cannot expose a public callback URL. A 2 second interval is recommended.
* `data` is `null` while `code` is `201`.
* A recovered `audio_url` may be an `.m4a` file — do not assume `.mp3` when saving it.


## OpenAPI

````yaml suno-api/suno-api.json GET /api/v1/suno/recovery/record-info
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
  /api/v1/suno/recovery/record-info:
    get:
      summary: Get Recovery Audio Details
      description: >-
        Query the status and recovered audio links of a recovery task.


        ## User Guide

        - `code` = 201 means the task is still running, keep polling (a 2 second
        interval is recommended).

        - `code` = 200 means the recovery finished and `data` carries one entry
        per track.

        - `code` = 500 means every track failed to recover.
      operationId: get-recovery-audio-details
      parameters:
        - in: query
          name: task_id
          description: The recovery task ID returned by the Recovery Audio endpoint.
          required: true
          example: dc19****18b3
          schema:
            type: string
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                    enum:
                      - 200
                      - 201
                      - 400
                      - 401
                      - 404
                      - 405
                      - 429
                      - 430
                      - 455
                      - 500
                    description: >-
                      # Status Codes


                      - ✅ 200 - Recovery finished, at least one track recovered
                      successfully

                      - ⏳ 201 - Recovery task is still running, keep polling

                      - ⚠️ 400 - Invalid parameters

                      - ⚠️ 401 - Unauthorized access

                      - ⚠️ 404 - Invalid request method or path

                      - ⚠️ 405 - Rate limit exceeded

                      - ⚠️ 429 - Insufficient credits

                      - ⚠️ 430 - Your call frequency is too high. Please try
                      again later.

                      - ⚠️ 455 - System maintenance

                      - ❌ 500 - Recovery task failed or server error
                    example: 200
                  task_id:
                    type: string
                    description: Recovery task ID.
                    example: bbbb****0f7b
                  msg:
                    type: string
                    description: Result message
                    example: success
                  data:
                    type: array
                    nullable: true
                    description: >-
                      Recovery result of each track. Returns `null` while the
                      task is still running.
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                          description: >-
                            Track ID, identical to the audio ID of the original
                            music generation task.
                          example: f8d6****9b93
                        audio_url:
                          type: string
                          description: >-
                            Recovered playable audio link. Only present when
                            `status` is `success`.
                          example: https://example.com/****.m4a
                        title:
                          type: string
                          description: >-
                            Track title. Only present when `status` is
                            `success`.
                          example: Sunrise Love
                        status:
                          type: string
                          enum:
                            - success
                            - failed
                          description: Recovery result of this track.
                          example: success
                        error:
                          type: string
                          description: Failure reason. Empty when `status` is `success`.
                          example: ''
        '500':
          $ref: '#/components/responses/Error'
components:
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