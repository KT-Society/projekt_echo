> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Upload And Cover Audio

> This API covers an audio track by transforming it into a new style while retaining its core melody. It incorporates Suno's upload capability, enabling users to upload an audio file for processing. The expected result is a refreshed audio track with a new style, keeping the original melody intact.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

### Parameter Usage Guide

* This endpoint always runs in custom mode. Simple mode is not available. A source audio (`uploadUrl`) is enough to generate; `lyrics` (or `prompt`), `title`, and `style` are optional.
* **Required**: `uploadUrl`, `model`, `callBackUrl`
* **model** (string, required): `V6`, `V6_WILD`, `V6_MINI`. Deprecated: `V4_5ALL`, `V4`, `V4_5`, `V4_5PLUS`, `V5`, `V5_5`.
* `prompt` is lyrics. Optional. If `lyrics` is also provided, `lyrics` takes priority and `prompt` is not used as lyrics.
* **Character limits (based on model):**
  * **V4 model (Deprecated)**: prompt max 3000 characters, style max 200 characters
  * **V4\_5, V4\_5PLUS, V5, V5\_5 & V4\_5ALL models (Deprecated)**: prompt max 5000 characters, style max 1000 characters
  * **V6, V6\_WILD & V6\_MINI models**: lyrics/prompt max 5000 characters, style max 1000 characters, title max 80 characters
* `uploadUrl` specifies the source audio file; ensure the uploaded audio does not exceed 8 minutes in length.

### Optional parameters

<Note>
  The following fields are optional controls available for this endpoint:

  * <b>lyrics</b> (string): Lyrics content. Optional. V6 series maximum 5000 characters. Takes priority over `prompt` as lyrics.
  * <b>prompt</b> (string): Lyrics content. Optional. Used as lyrics when `lyrics` is not provided. V6 series maximum 5000 characters.
  * <b>style</b> (string): Music style. Optional. V6 series maximum 1000 characters.
  * <b>title</b> (string): Track title. Optional. Maximum 80 characters.
  * <b>instrumental</b> (boolean): Whether to generate instrumental music. Defaults to `false`.
  * <b>vocalGender</b> (string): Preferred vocal gender. Allowed values: `m` (male), `f` (female)
  * <b>styleWeight</b> (number): Style adherence weight in range 0–1 (recommended two decimals)
  * <b>weirdnessConstraint</b> (number): Creativity/novelty constraint in range 0–1 (recommended two decimals)
  * <b>audioWeight</b> (number): Relative weight of audio consistency in range 0–1 (recommended two decimals)
  * <b>variety</b> (number): Diversity of generated results. Integer from 0–4, default 1. `0` off, `1` normal (default), `2` high, `3` extra, `4` max.
  * <b>personaId</b> (string): Persona ID or Suno Voice `voiceId`. If you use a Voice-generated ID, set `personaModel` to `voice_persona`.
  * <b>personaModel</b> (string): Persona type. Use `style_persona` for Generate Persona IDs, or `voice_persona` for Suno Voice IDs. Default `style_persona`.
</Note>

<RequestExample>
  ```json JSON body theme={null}
  {
    "instrumental": false,
    "lyrics": "[Verse] Night city lights shining bright",
    "style": "Cinematic",
    "title": "Dark Cover",
    "uploadUrl": "https://storage.example.com/upload",
    "variety": 1,
    "model": "V6",
    "callBackUrl": "https://example.com/callback",
    "vocalGender": "m",
    "styleWeight": 0.61,
    "weirdnessConstraint": 0.72,
    "audioWeight": 0.65
  }
  ```
</RequestExample>

### Developer Notes

1. Recommended settings for new users: provide `uploadUrl`, `model`, and `callBackUrl`. `lyrics`, `title`, and `style` are optional.
2. Generated files will be deleted after 15 days
3. Pay attention to character limits for lyrics/prompt, style, and title to ensure successful processing
4. Callback process has three stages: text (text generation complete), first (first track complete), complete (all tracks complete)
5. You can use the Get Music Generation Details endpoint to actively check task status instead of waiting for callbacks
6. The uploadUrl parameter is used to specify the source audio file; please provide a valid URL.


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate/upload-cover
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
  /api/v1/generate/upload-cover:
    post:
      summary: Upload And Cover Audio
      operationId: upload-and-cover-audio
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - uploadUrl
                - callBackUrl
                - model
              properties:
                uploadUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL of the source audio file to cover. Required. With a
                    source audio URL, generation can proceed; `lyrics` (or
                    `prompt`), `title`, and `style` are optional.


                    **Upload Audio Duration Limits:** Maximum upload duration is
                    **8 minutes**
                  example: https://storage.example.com/upload
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
                  example: Classical
                title:
                  type: string
                  description: Music title. Optional. Maximum 80 characters.
                  maxLength: 80
                  example: Peaceful Piano Meditation
                instrumental:
                  type: boolean
                  description: >-
                    Determines if the audio should be instrumental (no lyrics).
                    Optional. Defaults to `false`.
                  example: true
                personaId:
                  type: string
                  description: >-
                    Persona ID to apply to the generated music. Optional. You
                    can use either:


                    - A Persona ID generated by the [Generate
                    Persona](https://docs.api.box/suno-api/generate-persona)
                    endpoint. Use `personaModel: style_persona` or omit
                    `personaModel` to use the default.

                    - A `voiceId` generated by the [Suno
                    Voice](https://docs.api.box/suno-api/suno-voice-generate)
                    workflow. When using a voice-generated ID, you must set
                    `personaModel: voice_persona`.
                  example: persona_123
                personaModel:
                  type: string
                  description: >-
                    Persona model type to apply when using `personaId`.
                    Optional.

                    - `style_persona` (default): Use this for Persona IDs
                    generated by the Generate Persona endpoint.

                    - `voice_persona`: Required when `personaId` is a `voiceId`
                    generated by Suno Voice. This option is only available with
                    V5 (Deprecated), V5_5 (Deprecated), V6, V6_WILD, and V6_MINI
                    models.
                  enum:
                    - style_persona
                    - voice_persona
                  default: style_persona
                  example: style_persona
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
                negativeTags:
                  type: string
                  description: >-
                    Music styles or traits to exclude from the generated
                    audio.  

                    - Optional. Use to avoid specific styles.  
                      Example: "Heavy Metal, Upbeat Drums"
                  example: Heavy Metal, Upbeat Drums
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL to receive task completion notifications when upload
                    and cover audio is complete. The callback process has three
                    stages: `text` (text generation), `first` (first track
                    complete), `complete` (all tracks complete). Note: In some
                    cases, `text` and `first` stages may be skipped, directly
                    returning `complete`.

                    - For detailed callback format and implementation guide, see
                    [Upload and Cover Audio
                    Callbacks](https://docs.api.box/suno-api/upload-and-cover-audio-callbacks)

                    - Alternatively, you can use the Get Music Generation
                    Details interface to poll task status
                  example: https://api.example.com/callback
                vocalGender:
                  type: string
                  description: >-
                    Preferred vocal gender. Optional. Allowed values: `m`
                    (male), `f` (female).
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
                  - $ref: '#/components/schemas/ApiResponse'
                  - type: object
                    properties:
                      data:
                        type: object
                        properties:
                          taskId:
                            type: string
                            description: Task ID for tracking task status
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
                        "id": "8551****662c",
                        "audio_url": "https://example.cn/****.mp3",
                        "source_audio_url": "https://example.cn/****.mp3",
                        "stream_audio_url": "https://example.cn/****",
                        "source_stream_audio_url": "https://example.cn/****",
                        "image_url": "https://example.cn/****.jpeg",
                        "source_image_url": "https://example.cn/****.jpeg",
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
                        "source_audio_url": "https://example.cn/****.mp3",
                        "stream_audio_url": "https://example.cn/****",
                        "source_stream_audio_url": "https://example.cn/****",
                        "image_url": "https://example.cn/****.jpeg",
                        "source_image_url": "https://example.cn/****.jpeg",
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
                                  source_audio_url:
                                    type: string
                                    description: (Deprecated) Original audio file URL
                                    deprecated: true
                                  stream_audio_url:
                                    type: string
                                    description: Streaming audio URL
                                  source_stream_audio_url:
                                    type: string
                                    description: Original streaming audio URL
                                  image_url:
                                    type: string
                                    description: Cover image URL
                                  source_image_url:
                                    type: string
                                    description: Original cover image URL
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
              method: post
              type: path
            path: '{request.body#/callBackUrl}'
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