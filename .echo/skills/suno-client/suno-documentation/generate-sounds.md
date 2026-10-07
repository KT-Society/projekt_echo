> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Generate Sounds

> Create a sound generation task with loop, tempo, key, and optional lyrics subtitle capture settings.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

Used for creating a sound generation task (Sounds Task). It supports settings for looping, tempo (BPM), pitch (Key), as well as lyrics subtitle capture, etc.

## 🚀 User Guide

* By using this interface, you can generate corresponding audio content based on the input `prompt`.
* It supports setting up loop playback effect, which is suitable for background music, ambient sounds, and other scenarios.
* It allows specifying BPM (beats per minute) and pitch (Key) to facilitate control over the style of the generated result.
* Optional feature to enable lyric subtitle capture for easier display or processing of lyric content later.
* Supports asynchronous reception of task completion notifications through callback address.

### `model` parameter

* Allowed values: `V6`, `V6_WILD`, `V6_MINI`. Deprecated: `V5`, `V5_5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`.

## 📌 Usage Scenarios

* 🎧 Background music creation
* 🎮 Game sound effects or looped ambient sounds generation
* 🌐 Integration of audio content platforms and creative tools


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate/sounds
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
  /api/v1/generate/sounds:
    post:
      summary: Generate Sounds
      description: >-
        Used for creating a sound generation task (Sounds Task). It supports
        settings for looping, tempo (BPM), pitch (Key), as well as lyrics
        subtitle capture, etc.


        ## User Guide

        - Generate corresponding audio content based on input `prompt`

        - Supports loop playback for background music and ambient sound
        scenarios

        - Supports BPM and Key controls for style shaping

        - Optional lyrics subtitle capture after generation

        - Supports async task completion notifications via callback URL
      operationId: generate-sounds
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - prompt
                - model
              properties:
                prompt:
                  type: string
                  description: Prompt text for sound generation. Maximum 500 characters.
                  maxLength: 500
                  example: A soft rain ambience with distant thunder and gentle wind
                model:
                  type: string
                  description: >-
                    AI model version. Default: `V6`.

                    - **`V6`**: Current standard model and recommended default.

                    - **`V6_WILD`**: Current model for more experimental and
                    creative results.

                    - **`V6_MINI`**: Current lightweight model.

                    - **Deprecated**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`,
                    `V4_5`, and `V4`. These values remain listed only for
                    backward compatibility; use a V6-series model for new
                    integrations.
                  enum:
                    - V6
                    - V6_WILD
                    - V6_MINI
                    - V5_5
                    - V5
                    - V4_5PLUS
                    - V4_5ALL
                    - V4_5
                    - V4
                  example: V6
                  default: V6
                soundLoop:
                  type: boolean
                  description: Whether to enable loop playback for the generated sound.
                  default: false
                  example: false
                soundTempo:
                  type: integer
                  description: BPM (beats per minute). If omitted, Auto is used.
                  minimum: 1
                  maximum: 300
                  nullable: true
                  example: 120
                soundKey:
                  type: string
                  description: Pitch key of generated sound. Default is `Any`.
                  default: Any
                  enum:
                    - Any
                    - Cm
                    - C#m
                    - Dm
                    - D#m
                    - Em
                    - Fm
                    - F#m
                    - Gm
                    - G#m
                    - Am
                    - A#m
                    - Bm
                    - C
                    - C#
                    - D
                    - D#
                    - E
                    - F
                    - F#
                    - G
                    - G#
                    - A
                    - A#
                    - B
                  example: Any
                grabLyrics:
                  type: boolean
                  description: Whether to fetch lyric subtitle data after task completion.
                  example: false
                callBackUrl:
                  type: string
                  format: uri
                  description: Callback URL for asynchronous task completion notifications.
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
                          taskId:
                            type: string
                            description: Task ID for tracking sound generation status
                            example: a1b2****c3d4
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