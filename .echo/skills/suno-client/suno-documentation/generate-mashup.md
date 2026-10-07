> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Generate Mashup

> Mix two audio files to generate a new mashup work using AI models.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

### Usage Guide

* This endpoint always runs in custom mode. Simple mode is not available.
* This endpoint creates mashup music from 2 uploaded audio files (the upstream uses only the first 2)
* Combines elements from multiple tracks into a cohesive new composition

### Parameter Details

* **Required**: `uploadUrlList`, `model`, `callBackUrl`
* `uploadUrlList` must contain 2 audio file URLs
* **model** (string, required): `V6`, `V6_WILD`, `V6_MINI`. Deprecated: `V4`, `V4_5`, `V4_5PLUS`, `V4_5ALL`, `V5`, `V5_5`.
* `prompt` is lyrics. Optional. If `lyrics` is also provided, `lyrics` takes priority and `prompt` is not used as lyrics.
* Character limits:
  * **V4, V4\_5, V4\_5PLUS, V4\_5ALL, V5 & V5\_5 (Deprecated)**: `prompt` 3000–5000 characters and `style` 200–1000 characters according to the legacy model.
  * **V6, V6\_WILD & V6\_MINI**: `lyrics`/`prompt` 5000 characters, `style` 1000 characters, `title` 80 characters

### Optional parameters

<Note>
  The following fields are optional controls available for this endpoint:

  * <b>lyrics</b> (string): Lyrics content. Optional. V6 series maximum 5000 characters. Takes priority over `prompt` as lyrics.
  * <b>prompt</b> (string): Lyrics content. Optional. Used as lyrics when `lyrics` is not provided. V6 series maximum 5000 characters.
  * <b>style</b> (string): Music style. Optional. V6 series maximum 1000 characters.
  * <b>title</b> (string): Track title. Optional. Maximum 80 characters.
  * <b>vocalGender</b> (string): Preferred vocal gender. Allowed values: `m` (male), `f` (female)
  * <b>styleWeight</b> (number): Style adherence weight in range 0–1 (recommended two decimals)
  * <b>weirdnessConstraint</b> (number): Creativity/novelty constraint in range 0–1 (recommended two decimals)
  * <b>audioWeight</b> (number): Relative weight of audio consistency in range 0–1 (recommended two decimals)
  * <b>variety</b> (number): Diversity of generated results. Integer from 0–4, default 1. `0` off, `1` normal (default), `2` high, `3` extra, `4` max.
  * <b>duration</b> (number): Audio duration in seconds. Range 10–360. Valid for `V5_5`, `V6`, `V6_WILD`, and `V6_MINI`.
  * <b>personaId</b> (string): Persona ID or Suno Voice `voiceId`. If you use a Voice-generated ID, set `personaModel` to `voice_persona`.
  * <b>personaModel</b> (string): Persona type. Use `style_persona` for Generate Persona IDs, or `voice_persona` for Suno Voice IDs. Default `style_persona`.
</Note>

<RequestExample>
  ```json JSON body theme={null}
  {
    "uploadUrlList": [
      "https://example.com/audio1.mp3",
      "https://example.com/audio2.mp3"
    ],
    "lyrics": "[Verse] Night city lights shining bright",
    "style": "Electronic Dance Music",
    "title": "Mashup Work",
    "variety": 1,
    "model": "V6",
    "callBackUrl": "https://example.com/callback",
    "vocalGender": "m",
    "styleWeight": 0.65,
    "weirdnessConstraint": 0.72,
    "audioWeight": 0.65
  }
  ```
</RequestExample>

### Developer Notes

* Generated files are retained for 14 days
* Callback process has three stages: `text` (text generation), `first` (first track complete), `complete` (all tracks complete)
* The two audio files in `uploadUrlList` must be valid and accessible URLs
* Audio files should be in supported formats (MP3, WAV, etc.)


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate/mashup
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
  /api/v1/generate/mashup:
    post:
      summary: Generate Mashup Music
      operationId: generate-mashup
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - uploadUrlList
                - callBackUrl
                - model
              properties:
                uploadUrlList:
                  type: array
                  description: >-
                    Array of audio file URLs to mashup. Required. Pass 2 audio
                    URLs (the upstream uses only the first 2). Each URL must be
                    publicly accessible.
                  items:
                    type: string
                    format: uri
                  minItems: 2
                  maxItems: 2
                  example:
                    - https://example.com/audio1.mp3
                    - https://example.com/audio2.mp3
                prompt:
                  type: string
                  description: >-
                    Lyrics content. Optional. Used as lyrics when `lyrics` is
                    not provided. If `lyrics` is also provided, `lyrics` takes
                    priority and this field is not used as lyrics.

                    - **V4 (Deprecated)**: Maximum 3000 characters

                    - **V4_5, V4_5PLUS, V4_5ALL, V5, V5_5 (Deprecated)**:
                    Maximum 5000 characters

                    - **V6, V6_WILD, V6_MINI**: Maximum 5000 characters
                  example: '[Verse] Night city lights shining bright'
                lyrics:
                  type: string
                  description: >-
                    Lyrics for the generated audio. Optional. For V6, V6_MINI,
                    and V6_WILD: maximum 5000 characters. Takes priority over
                    `prompt` as lyrics. If omitted, `prompt` is used as lyrics.
                  example: '[Verse] Night city lights shining bright'
                style:
                  type: string
                  description: >-
                    Music style, e.g. Jazz, Classical, or Electronic. Optional.
                    For V6, V6_WILD, and V6_MINI: maximum 1000 characters.

                    - **V4 (Deprecated)**: Maximum 200 characters

                    - **V4_5, V4_5PLUS, V4_5ALL, V5, V5_5 (Deprecated)**:
                    Maximum 1000 characters
                  example: Jazz
                title:
                  type: string
                  description: Music title. Optional. Maximum 80 characters.
                  maxLength: 80
                  example: Relaxing Piano
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
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL to receive music generation task completion updates.
                    Required for all music generation requests.


                    - System will POST task status and results to this URL when
                    generation completes

                    - Callback process has three stages: `text` (text
                    generation), `first` (first track complete), `complete` (all
                    tracks complete)

                    - Note: Some cases may skip `text` and `first` stages and
                    return `complete` directly

                    - Your callback endpoint should accept POST requests with
                    JSON payload containing task results and audio URLs

                    - For detailed callback format and implementation guide, see
                    [Music Generation
                    Callbacks](https://docs.kie.ai/suno-api/generate-music-callbacks)

                    - Alternatively, use the Get Music Details endpoint to poll
                    task status
                  example: https://example.com/callback
                vocalGender:
                  type: string
                  description: >-
                    Vocal gender preference for the singing voice. Optional. Use
                    `m` for male and `f` for female. In practice, this only
                    increases probability and cannot guarantee male/female voice
                    instructions are followed.
                  enum:
                    - m
                    - f
                  example: m
                styleWeight:
                  type: number
                  description: >-
                    Style adherence weight. Optional. Range 0–1, up to 2 decimal
                    places.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                weirdnessConstraint:
                  type: number
                  description: >-
                    Creativity/novelty constraint. Optional. Range 0–1, up to 2
                    decimal places.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                audioWeight:
                  type: number
                  description: >-
                    Relative weight of audio consistency versus other controls.
                    Optional. Range 0–1, up to 2 decimal places.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                variety:
                  type: number
                  description: >-
                    Controls the diversity and stylistic variation of generated
                    results. Optional. Integer from 0–4, default 1.


                    - **`0`**: off (exact style) — fully off, strictly the same
                    style

                    - **`1`**: normal (balanced variety) — default, balances
                    stability and diversity

                    - **`2`**: high (distinct styles) — produces results with
                    clearly different styles

                    - **`3`**: extra (bold exploration) — higher variation,
                    encourages bold exploration of different styles

                    - **`4`**: max (unreasonably varied) — maximum diversity;
                    results may differ in style very significantly
                  minimum: 0
                  maximum: 4
                  multipleOf: 1
                  default: 1
                  example: 1
                personaId:
                  type: string
                  description: >-
                    Persona ID or Voice ID to apply to the generated music.
                    Optional. When using a Voice-generated ID, set
                    `personaModel` to `voice_persona`.
                  example: persona_123
                personaModel:
                  type: string
                  description: >-
                    Persona model type. Optional. `style_persona` (default) for
                    Generate Persona IDs; `voice_persona` when `personaId` is a
                    Suno Voice `voiceId`. Default `style_persona`.
                  enum:
                    - style_persona
                    - voice_persona
                  default: style_persona
                  example: style_persona
                duration:
                  type: integer
                  description: >-
                    Duration in seconds. Optional. Range 10–360. Only valid when
                    the model is `V5_5` (Deprecated), `V6`, `V6_WILD`, or
                    `V6_MINI`.
                  minimum: 10
                  maximum: 360
                  example: 20
      responses:
        '200':
          description: Request successful
          content:
            application/json:
              schema:
                allOf:
                  - type: object
                    properties:
                      code:
                        type: integer
                        enum:
                          - 200
                          - 401
                          - 402
                          - 404
                          - 409
                          - 422
                          - 429
                          - 451
                          - 455
                          - 500
                        description: >-
                          Response Status Codes


                          - **200**: Success - Request has been processed
                          successfully  

                          - **401**: Unauthorized - Authentication credentials
                          are missing or invalid  

                          - **402**: Insufficient Credits - Account does not
                          have enough credits to perform the operation  

                          - **404**: Not Found - The requested resource or
                          endpoint does not exist  

                          - **409**: Conflict - WAV record already exists  

                          - **422**: Validation Error - The request parameters
                          failed validation checks  

                          - **429**: Rate Limited - Request limit has been
                          exceeded for this resource  

                          - **451**: Unauthorized - Failed to fetch the image.
                          Kindly verify any access limits set by you or your
                          service provider  

                          - **455**: Service Unavailable - System is currently
                          undergoing maintenance  

                          - **500**: Server Error - An unexpected error occurred
                          while processing the request
                      msg:
                        type: string
                        description: Error message when code != 200
                        example: success
                  - type: object
                    properties:
                      data:
                        type: object
                        properties:
                          taskId:
                            type: string
                            description: >-
                              Task ID for tracking task status. Use this ID with
                              the "Get Music Details" endpoint to query task
                              details and results.
                            example: 5c79****be8e
        '500':
          $ref: '#/components/responses/Error'
      callbacks:
        audioGenerated:
          '{request.body#/callBackUrl}':
            post:
              description: >-
                System will call this callback when audio generation is
                complete.


                ### Callback Example

                ```json

                {
                  "code": 200,
                  "msg": "All generated successfully.",
                  "data": {
                    "callbackType": "complete",
                    "task_id": "2fac****9f72",
                    "data": [
                      {
                        "id": "e231****-****-****-****-****8cadc7dc",
                        "audio_url": "https://example.cn/****.mp3",
                        "stream_audio_url": "https://example.cn/****",
                        "image_url": "https://example.cn/****.jpeg",
                        "prompt": "[Verse] Night city lights shining bright",
                        "model_name": "chirp-v3-5",
                        "title": "Iron Man",
                        "tags": "electrifying, rock",
                        "createTime": "2025-01-01 00:00:00",
                        "duration": 198.44
                      },
                      {
                        "id": "bd15****1873",
                        "audio_url": "https://example.cn/****.mp3",
                        "stream_audio_url": "https://example.cn/****",
                        "image_url": "https://example.cn/****.jpeg",
                        "prompt": "[Verse] Night city lights shining bright",
                        "model_name": "chirp-v3-5",
                        "title": "Iron Man",
                        "tags": "electrifying, rock",
                        "createTime": "2025-01-01 00:00:00",
                        "duration": 228.28
                      }
                    ]
                  }
                }

                ```
              requestBody:
                content:
                  application/json:
                    schema:
                      type: object
                      properties:
                        code:
                          type: integer
                          description: Status code
                          example: 200
                        msg:
                          type: string
                          description: Response message
                          example: All generated successfully
                        data:
                          type: object
                          properties:
                            callbackType:
                              type: string
                              description: >-
                                Callback type: text (text generation complete),
                                first (first track complete), complete (all
                                tracks complete)
                              enum:
                                - text
                                - first
                                - complete
                            task_id:
                              type: string
                              description: Task ID
                            data:
                              type: array
                              items:
                                type: object
                                properties:
                                  id:
                                    type: string
                                    description: Audio unique identifier (audioId)
                                  audio_url:
                                    type: string
                                    description: Audio file URL
                                  stream_audio_url:
                                    type: string
                                    description: Streaming audio URL
                                  image_url:
                                    type: string
                                    description: Cover image URL
                                  prompt:
                                    type: string
                                    description: Generation prompt/lyrics
                                  model_name:
                                    type: string
                                    description: Model name used
                                  title:
                                    type: string
                                    description: Music title
                                  tags:
                                    type: string
                                    description: Music tags
                                  createTime:
                                    type: string
                                    description: Creation time
                                    format: date-time
                                  duration:
                                    type: number
                                    description: Audio duration (seconds)
              responses:
                '200':
                  description: Callback received successfully
                  content:
                    application/json:
                      schema:
                        allOf:
                          - type: object
                            properties:
                              code:
                                type: integer
                                enum:
                                  - 200
                                  - 400
                                  - 408
                                  - 413
                                  - 500
                                  - 501
                                  - 531
                                description: >-
                                  Response status code


                                  - **200**: Success - Request has been
                                  processed successfully

                                  - **400**: Validation Error - Lyrics contained
                                  copyrighted material.

                                  - **408**: Rate Limited - Timeout.

                                  - **413**: Conflict - Uploaded audio matches
                                  existing work of art.

                                  - **500**: Server Error - An unexpected error
                                  occurred while processing the request

                                  - **501**: Audio generation failed.

                                  - **531**: Server Error - Sorry, the
                                  generation failed due to an issue. Your
                                  credits have been refunded. Please try again.
                              msg:
                                type: string
                                description: Error message when code != 200
                                example: success
                      example:
                        code: 200
                        msg: success
              method: post
              type: path
            path: '{request.body#/callBackUrl}'
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