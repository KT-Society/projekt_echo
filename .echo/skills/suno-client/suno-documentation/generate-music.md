> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Generate Music

> Generate music with or without lyrics using AI models.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

### Usage Guide

* This endpoint creates music based on your text prompt
* Multiple variations will be generated for each request
* You can control detail level with custom mode and instrumental settings

### Parameter Details

* Always required: `customMode`, `instrumental`, `model`

* In Custom Mode (`customMode: true`):
  * `title` is optional, maximum 80 characters. Only available in this mode; not supported when `customMode` is `false`
  * `prompt` is optional; when provided, it is used strictly as lyrics and sung in the generated track. If `lyrics` is also provided, `lyrics` takes priority
  * At least one of `style`, `lyrics`, or `negativeTags` must be provided; generation is rejected if all are empty
  * If `instrumental: true`: generate instrumental music (no vocals)
  * If `instrumental: false`: use `lyrics` as lyrics (fall back to `prompt` if `lyrics` is not provided)
  * `negativeTags`, `vocalGender`, and `duration` are available only in this mode. Do not pass them when `customMode` is `false`
  * Optional: `duration` (10–360 seconds), `negativeTags` (V6 max 1000 characters), `vocalGender` (`m` / `f`), `styleWeight`, `weirdnessConstraint`, `audioWeight`, `variety`, `personaId`, `personaModel`
  * Character limits by model:
    * **V4 (Deprecated)**: `prompt` 3000 characters, `style` 200 characters
    * **V4\_5, V4\_5PLUS, V4\_5ALL, V5, V5\_5 (Deprecated)**: `prompt` 5000 characters, `style` 1000 characters
    * **V6, V6\_MINI, V6\_WILD**: `style` 1000 characters; `lyrics` 5000 characters; `negativeTags` 1000 characters
  * `title` length limit: 80 characters (all models)

* In Non-custom Mode (`customMode: false`):
  * `prompt` is optional; it serves as the core idea, and lyrics are generated automatically (not a strict match), maximum 3000 characters
  * `lyrics` can be used as a lyrics attachment together with `prompt`
  * At least one of `imageUrls`, `videoUrls`, `audioUrls`, `style`, or `lyrics` must be provided; generation is rejected if all are empty
  * `imageUrls`, `videoUrls`, and `audioUrls` are only valid in this mode
  * Do not pass parameters that are only available in custom mode: `title`, `negativeTags`, `duration`, `vocalGender`, `styleWeight`, `weirdnessConstraint`, `audioWeight`, `variety`
  * Total attachments must not exceed 10: `style` + `lyrics` + `imageUrls` + `videoUrls` + `audioUrls`

### Optional Parameters

<Note>
  The following fields are optional controls available for this endpoint:

  * <b>prompt</b> (string): Description of the desired audio content. Optional. Used as lyrics in custom mode; used as the core idea in non-custom mode (maximum 3000 characters).
  * <b>lyrics</b> (string): Lyrics content. Optional. V6 series maximum 5000 characters. In custom mode, takes priority over `prompt` as lyrics; in non-custom mode, can be used as a lyrics attachment together with `prompt`.
  * <b>imageUrls</b> (array): Image references. Only effective when `customMode` is `false`. Up to 5 images, each no more than 10 MB. Supported formats: jpeg, png, webp, bmp.
  * <b>videoUrls</b> (array): Video references. Only effective when `customMode` is `false`. Up to 1 file, each no more than 100 MB, duration no more than 241 seconds. Supported formats: mp4, mov, webm.
  * <b>audioUrls</b> (array): Audio references. Only effective when `customMode` is `false`. Duration must be between 6 seconds and 30 minutes; each file no more than 500 MB.
  * <b>style</b> (string): Music style specification. See character limits in Parameter Details above.
  * <b>title</b> (string): Track title. Optional. Only available when `customMode` is `true`. Maximum 80 characters. Displayed in player interfaces and filenames.
  * <b>negativeTags</b> (string): Music styles or traits to exclude from the generated audio. Only available when `customMode` is `true`. For V6, V6\_MINI, and V6\_WILD: maximum 1000 characters.
  * <b>vocalGender</b> (string): Vocal gender preference. `m` for male, `f` for female. Only available when `customMode` is `true`. In practice, this only increases probability and cannot guarantee the instruction is followed.
  * <b>styleWeight</b> (number): Strength of adherence to the specified style. Range 0–1, up to 2 decimal places. Only effective when `customMode` is `true`.
  * <b>weirdnessConstraint</b> (number): Creative/experimental deviation. Range 0–1, up to 2 decimal places. Only effective when `customMode` is `true`.
  * <b>audioWeight</b> (number): Relative weight of audio features. Range 0–1, up to 2 decimal places. Only effective when `customMode` is `true`. Not supported when there are no vocals.
  * <b>variety</b> (number): Diversity of generated results. Integer from 0–4, default 1. Only effective when `customMode` is `true`. `0` off (exact style), `1` normal (default, balanced), `2` high (distinct styles), `3` extra (bold exploration), `4` max (maximum variation).
  * <b>personaId</b> (string): Persona ID or Voice ID. Optional. To generate a Persona ID, see [Generate Persona](/suno-api/generate-persona).
  * <b>personaModel</b> (string): Persona model, `style_persona` or `voice_persona`. Only available for `V5` (Discontinued), `V5_5` (Discontinued), `V6`, `V6_MINI`, and `V6_WILD`.
  * <b>duration</b> (number): Audio duration in seconds. Range 10–360, default 20. Only available when `customMode` is `true`, and only valid when the model is `V5_5`, `V6`, `V6_MINI`, or `V6_WILD`.
</Note>

<RequestExample>
  ```json Non-custom mode theme={null}
  {
    "customMode": false,
    "instrumental": false,
    "prompt": "A chill lo-fi beat with soft vocals",
    "lyrics": "[Verse] Night city lights shining bright",
    "style": "lo-fi, chill",
    "imageUrls": [
      "https://example.com/reference-image.png"
    ],
    "videoUrls": [
      "https://example.com/reference-video.mp4"
    ],
    "audioUrls": [
      "https://example.com/reference-audio.mp3"
    ],
    "model": "V6",
    "callBackUrl": "https://example.com/callback"
  }
  ```

  ```json Custom mode theme={null}
  {
    "customMode": true,
    "instrumental": false,
    "title": "Peaceful Piano Meditation",
    "style": "Classical",
    "lyrics": "[Verse] Night city lights shining bright",
    "prompt": "A calm and relaxing piano track with soft melodies",
    "negativeTags": "Heavy Metal, Upbeat Drums",
    "vocalGender": "m",
    "styleWeight": 0.65,
    "weirdnessConstraint": 0.65,
    "audioWeight": 0.65,
    "variety": 1,
    "duration": 20,
    "model": "V6",
    "callBackUrl": "https://example.com/callback"
  }
  ```
</RequestExample>

### Developer Notes

* Recommendation for new users: Start with `customMode: false` for simpler usage
* Generated files are retained for 14 days
* Callback process has three stages: `text` (text generation), `first` (first track complete), `complete` (all tracks complete)


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate
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
  /api/v1/generate:
    post:
      summary: Generate Music
      description: Generate music with or without lyrics using AI models.
      operationId: generate-music
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - customMode
                - instrumental
                - callBackUrl
                - model
              properties:
                prompt:
                  type: string
                  description: >-
                    A description of the desired audio content. Optional.

                    - Custom mode (`customMode=true`): When provided, the prompt
                    is used strictly as lyrics and sung in the generated track.
                    If `lyrics` is also provided, `lyrics` takes priority.
                    Character limits by model:
                      - **V4 (Discontinued)**: Maximum 3000 characters
                      - **V4_5, V4_5PLUS, V4_5ALL, V5_5, V5 (Discontinued)**: Maximum 5000 characters
                    - Non-custom mode (`customMode=false`): When provided, the
                    prompt serves as the core idea. Lyrics are generated
                    automatically based on it and do not strictly match the
                    input. Maximum 3000 characters.

                    `prompt` is not required. In non-custom mode, provide at
                    least one of `imageUrls`, `videoUrls`, `audioUrls`, `style`,
                    or `lyrics`. In custom mode, provide at least one of
                    `style`, `lyrics`, or `negativeTags`. Generation is rejected
                    if all related inputs are empty.
                  example: A calm and relaxing piano track with soft melodies
                lyrics:
                  type: string
                  description: >-
                    Lyrics for the generated audio. Optional.

                    - **V6, V6_MINI, V6_WILD**: Maximum 5000 characters.

                    - When `customMode=true`, `lyrics` is used as lyrics first;
                    if `lyrics` is not provided, `prompt` is used as lyrics.

                    - When `customMode=false`, `lyrics` is used as a lyrics
                    attachment and can be used together with the audio
                    description in `prompt`.
                  example: '[Verse] Night city lights shining bright'
                imageUrls:
                  type: array
                  description: >-
                    Image references. Only effective when `customMode=false`.

                    - Optional

                    - Up to 5 images; each image must not exceed 10 MB

                    - Supported formats: `jpeg`, `png`, `webp`, and `bmp`

                    - In non-custom mode, total attachments must not exceed 10:
                    `style` + `lyrics` + `imageUrls` + `videoUrls` + `audioUrls`
                  items:
                    type: string
                  maxItems: 5
                  example:
                    - https://example.com/reference-image.png
                videoUrls:
                  type: array
                  description: >-
                    Video references. Only effective when `customMode=false`.

                    - Optional

                    - Up to 1 video file; each file must not exceed 100 MB,
                    duration must not exceed 241 seconds, with no minimum
                    duration

                    - Supported formats: mp4, mov, and webm
                  items:
                    type: string
                  maxItems: 1
                  example:
                    - https://example.com/reference-video.mp4
                audioUrls:
                  type: array
                  description: >-
                    Audio references. Only effective when `customMode=false`.

                    - Optional

                    - Audio duration must be between 6 seconds and 30 minutes;
                    each audio file must not exceed 500 MB
                  items:
                    type: string
                  example:
                    - https://example.com/reference-audio.mp3
                style:
                  type: string
                  description: >-
                    Music style specification for the generated audio.

                    - Character limits by model:
                      - **V4 (Discontinued)**: Maximum 200 characters
                      - **V4_5 and V4_5PLUS (Discontinued)**: Maximum 1000 characters
                      - **V4_5ALL (Discontinued)**: Maximum 1000 characters
                      - **V5_5 and V5 (Discontinued)**: Maximum 1000 characters
                      - **V6, V6_MINI, and V6_WILD**: Maximum 1000 characters
                    - Common examples: Jazz, Classical, Electronic, Pop, Rock,
                    Hip-hop, etc.

                    - In custom mode, provide at least one of `style`, `lyrics`,
                    or `negativeTags`. In non-custom mode, provide at least one
                    of `imageUrls`, `videoUrls`, `audioUrls`, `style`, or
                    `lyrics`.
                  example: Classical
                title:
                  type: string
                  description: >-
                    Title for the generated music track. Optional.

                    - Only available when `customMode` is `true`. Not supported
                    when `customMode` is `false`.

                    - Maximum 80 characters.

                    - Displayed in player interfaces and filenames.
                  maxLength: 80
                  example: Peaceful Piano Meditation
                customMode:
                  type: boolean
                  description: >-
                    Determines whether advanced parameter customization is
                    enabled.

                    - If `true`: Allows detailed control

                    - If `false`: Simplified mode
                  example: true
                instrumental:
                  type: boolean
                  description: >-
                    Determines whether the audio should be instrumental (no
                    lyrics).

                    - In Custom Mode (`customMode: true`):
                      - If `true`: generate instrumental music (no vocals)
                      - If `false`: use `lyrics` as lyrics (fall back to `prompt` if `lyrics` is not provided)
                    - In Non-custom Mode (`customMode: false`):
                      - If `true`: generate instrumental music (no vocals)
                      - If `false`: `lyrics` can be used as a lyrics attachment together with the audio description in `prompt`
                  example: true
                model:
                  type: string
                  description: >-
                    The AI model version to use for generation. Required for all
                    requests. Default: `V6`. Available options:

                    - **`V6_WILD`**: Pushes creative boundaries for bolder, more
                    distinctive musical expression.

                    - **`V6_MINI`**: Lightweight and fast, balancing quality and
                    speed for effortless creation.

                    - **`V6`**: Greater musical expression with more natural
                    vocals and richer details. Recommended default.

                    - **`V5_5` (Discontinued)**: Custom models tailored to your
                    unique taste.

                    - **`V5` (Discontinued)**: Superior musical expression,
                    faster generation.

                    - **`V4_5PLUS` (Discontinued)**: V4.5+ delivers richer
                    sound, new ways to create, max 8 min.

                    - **`V4_5` (Discontinued)**: V4.5 enables smarter prompts,
                    faster generations, max 8 min.

                    - **`V4_5ALL` (Discontinued)**: V4.5ALL enables smarter
                    prompts, faster generations, max 8 min.

                    - **`V4` (Discontinued)**: V4 improves vocal quality, max 4
                    min.

                    Discontinued values remain listed only for backward
                    compatibility; use a V6-series model for new integrations.
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
                    The URL to receive task completion notifications when music
                    generation is complete. The callback process has three
                    stages: `text` (text generation), `first` (first track
                    complete), `complete` (all tracks complete). Note: In some
                    cases, `text` and `first` stages may be skipped, directly
                    returning `complete`.

                    - For detailed callback format and implementation guide, see
                    [Music Generation
                    Callbacks](https://docs.sunoapi.org/suno-api/generate-music-callbacks)

                    - Alternatively, you can use the Get Music Generation
                    Details interface to poll task status
                  example: https://api.example.com/callback
                negativeTags:
                  type: string
                  description: >-
                    Music styles or traits to exclude from the generated audio.
                    Optional.

                    - Only available when `customMode` is `true`. Do not pass
                    this field when `customMode` is `false`.

                    - For V6, V6_MINI, and V6_WILD: maximum 1000 characters.

                    - In custom mode, provide at least one of `style`, `lyrics`,
                    or `negativeTags`.
                  maxLength: 1000
                  example: Heavy Metal, Upbeat Drums
                vocalGender:
                  type: string
                  description: >-
                    Vocal gender preference. Optional.

                    - Only available when `customMode` is `true`. Do not pass
                    this field when `customMode` is `false`.

                    - Use `m` for male and `f` for female.

                    - In practice, this only increases probability and cannot
                    guarantee male/female voice instructions are followed.
                  enum:
                    - m
                    - f
                  example: m
                styleWeight:
                  type: number
                  description: >-
                    Only available when Custom Mode (`customMode: true`) is
                    enabled. Strength of adherence to the specified style.
                    Optional. Range 0–1, up to 2 decimal places.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                weirdnessConstraint:
                  type: number
                  description: >-
                    Only available when Custom Mode (`customMode: true`) is
                    enabled. Controls experimental/creative deviation. Optional.
                    Range 0–1, up to 2 decimal places.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                audioWeight:
                  type: number
                  description: >-
                    Only available when Custom Mode (`customMode: true`) is
                    enabled. Relative weight of audio features. Optional. Range
                    0–1, up to 2 decimal places.

                    - `audioWeight` is not supported when there are no vocals
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.65
                variety:
                  type: number
                  description: >-
                    Only available when Custom Mode (`customMode: true`) is
                    enabled. Controls the diversity and stylistic variation of
                    generated results. Optional. Range 0–4, integer, default 1.


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
                    Optional. Use this to apply a specific persona style to your
                    music generation.


                    To generate a Persona ID, use the [Generate
                    Persona](https://docs.sunoapi.org/suno-api/generate-persona)
                    endpoint to create a personalized music Persona based on
                    generated music.


                    To generate a Voice ID, use the [Generate
                    Voice](https://docs.sunoapi.org/suno-api/suno-voice-generate)
                    endpoint. When using a Voice-generated ID, you must set
                    `personaModel: voice_persona`.
                  example: persona_123
                personaModel:
                  type: string
                  description: >-
                    Persona model. Optional `style_persona` or `voice_persona`.
                    Only available for `V5` (Discontinued), `V5_5`
                    (Discontinued), `V6`, `V6_MINI`, and `V6_WILD`.

                    - `style_persona` (default): Use this for Persona IDs
                    generated by the Generate Persona endpoint.

                    - `voice_persona`: Required when `personaId` is a `voiceId`
                    generated by Suno Voice.
                  enum:
                    - style_persona
                    - voice_persona
                  default: style_persona
                  example: style_persona
                duration:
                  type: number
                  description: >-
                    Audio duration in seconds. Optional.

                    - Only available when `customMode` is `true`. Do not pass
                    this field when `customMode` is `false`.

                    - Range: 10–360 seconds. Default: 20.

                    - Only valid when the model is `V5_5` (Discontinued), `V6`,
                    `V6_MINI`, or `V6_WILD`.
                  minimum: 10
                  maximum: 360
                  default: 20
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