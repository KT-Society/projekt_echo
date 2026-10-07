> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Replace Music Section

> Replace a specific time segment within existing music.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

### Parameter Usage Guide

This endpoint supports two modes for specifying the source audio:

**Mode 1: Replace section using existing audio**

* `taskId` and `audioId` are required
* `uploadUrl` and `model` must NOT be provided

**Mode 2: Replace section using uploaded custom audio**

* `uploadUrl` and `model` are required
* `taskId` and `audioId` must NOT be provided

This endpoint always runs in custom mode.

### Common Required Parameters

* **prompt** (string, required): Lyrics for the replaced segment. If `lyrics` is also provided, `lyrics` takes priority for the replaced segment.
* **tags** (string, required): Music style tags, such as jazz, electronic, etc.
* **title** (string, required): Music title
* **infillStartS** (number, required): Start time point for replacement (seconds), 2 decimal places. Must be less than infillEndS. The time interval (infillEndS - infillStartS) must be at least 10 seconds.
* **infillEndS** (number, required): End time point for replacement (seconds), 2 decimal places. Must be greater than infillStartS. The time interval (infillEndS - infillStartS) must be at least 10 seconds.
* **fullLyrics** (string, required): Complete lyrics of the whole song after modification, combining both modified and unmodified lyrics. Distinct from `lyrics`/`prompt`, which apply only to the replaced segment.

### Optional Parameters

<Note>
  The following fields are optional controls available for this endpoint:

  * <b>lyrics</b> (string): Lyrics for the replaced segment. Optional. V6 series maximum 5000 characters. Takes priority over `prompt` for the replaced segment. Distinct from `fullLyrics`, which is the complete song lyrics.
  * <b>negativeTags</b> (string): Excluded music styles, used to avoid specific style elements in the replacement segment
  * <b>vocalGender</b> (string): Preferred vocal gender. Allowed values: `m` (male), `f` (female)
  * <b>styleWeight</b> (number): Style adherence weight in range 0–1 (recommended two decimals)
  * <b>weirdnessConstraint</b> (number): Creativity/novelty constraint in range 0–1 (recommended two decimals)
  * <b>audioWeight</b> (number): Relative weight of audio consistency in range 0–1 (recommended two decimals)
  * <b>variety</b> (number): Diversity of generated results. Integer from 0–4, default 1. `0` off, `1` normal (default), `2` high, `3` extra, `4` max.
  * <b>personaId</b> (string): Persona ID or Suno Voice `voiceId`. If you use a Voice-generated ID, set `personaModel` to `voice_persona`.
  * <b>personaModel</b> (string): Persona type. Use `style_persona` for Generate Persona IDs, or `voice_persona` for Suno Voice IDs. Default `style_persona`.
  * <b>callBackUrl</b> (string): Callback URL for task completion notification. For detailed callback format, see [Replace Music Section Callbacks](/suno-api/replace-section-callbacks).
</Note>

### Time Range Instructions

* `infillStartS` must be less than `infillEndS`
* Time values are precise to 2 decimal places, e.g., `10.50` seconds
* The replacement time must be at least **10 seconds**.
* Replacement duration should not exceed **50%** of the original music's total duration

<RequestExample>
  ```json Replace using existing audio theme={null}
  {
    "taskId": "2fac****9f72",
    "audioId": "e231****-****-****-****-****8cadc7dc",
    "prompt": "A calm and relaxing piano track.",
    "tags": "Jazz",
    "title": "Relaxing Piano",
    "negativeTags": "Rock",
    "infillStartS": 10.5,
    "infillEndS": 20.75,
    "fullLyrics": "[Verse 1]\nOriginal lyrics here\n[Chorus]\nModified lyrics for this section\n[Verse 2]\nMore original lyrics",
    "callBackUrl": "https://example.com/callback"
  }
  ```

  ```json Replace using uploaded audio theme={null}
  {
    "uploadUrl": "https://example.com/audio.mp3",
    "model": "V6",
    "prompt": "A calm and relaxing piano track.",
    "tags": "Jazz",
    "title": "Relaxing Piano",
    "negativeTags": "Rock",
    "infillStartS": 10.5,
    "infillEndS": 20.75,
    "fullLyrics": "[Verse 1]\nOriginal lyrics here\n[Chorus]\nModified lyrics for this section\n[Verse 2]\nMore original lyrics",
    "callBackUrl": "https://example.com/callback"
  }
  ```
</RequestExample>

### Developer Notes

1. Replacement segments will be regenerated based on the provided `lyrics`/`prompt` and `tags`. Use `lyrics` (or `prompt`) for the replaced segment and `fullLyrics` for the complete song.
2. Generated replacement segments will automatically blend with the original music's preceding and following parts
3. Generated files will be retained for **14 days**
4. Query task status using the same interface as generating music: [Get Music Details](/suno-api/get-music-generation-details)


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate/replace-section
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
  /api/v1/generate/replace-section:
    post:
      summary: Replace Music Section
      description: >-
        Replace a specific time segment within existing music.


        > Replace a specific time segment within existing music.


        This interface can replace specific time segments in already generated
        music. It requires providing the original music's task ID and the time
        range to be replaced. The replaced audio will naturally blend with the
        original music.


        ## Time Range Instructions


        *   `infillStartS` must be less than `infillEndS`.

        *   Time values are precise to 2 decimal places, e.g., `10.50` seconds.

        *   The replacement time must be at least **10 seconds**.

        *   Replacement duration should not exceed **50%** of the original
        music's total duration.


        ## Developer Notes


        *   Replacement segments will be regenerated based on the provided
        `lyrics`/`prompt` and `tags`. Use `lyrics` (or `prompt`) for the
        replaced segment and `fullLyrics` for the complete song.

        *   Generated replacement segments will automatically blend with the
        original music's preceding and following parts.

        *   Generated files will be retained for **14 days**.

        *   Query task status using the same interface as generating music: [Get
        Music Details](/suno-api/get-music-generation-details).
      operationId: replace-section
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - prompt
                - tags
                - title
                - infillStartS
                - infillEndS
                - fullLyrics
              oneOf:
                - title: Replace section using existing audio
                  required:
                    - taskId
                    - audioId
                  properties:
                    taskId:
                      type: string
                      description: >-
                        Original task ID (parent task), used to identify the
                        source music for section replacement.
                      example: 2fac****9f72
                    audioId:
                      type: string
                      description: >-
                        Unique identifier of the audio track to replace. This ID
                        is returned in the callback data after music generation
                        completes.
                      example: e231****-****-****-****-****8cadc7dc
                - title: Replace section using uploaded custom audio
                  required:
                    - uploadUrl
                    - model
                  properties:
                    uploadUrl:
                      type: string
                      format: uri
                      description: URL of the custom audio uploaded by the user.
                      example: https://example.com/audio.mp3
                    model:
                      type: string
                      description: >-
                        AI model version. Default: `V6`.

                        - **`V6`**: Current standard model and recommended
                        default.

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
              properties:
                prompt:
                  type: string
                  description: >-
                    Lyrics for the replaced segment. Required. If `lyrics` is
                    also provided, `lyrics` takes priority for the replaced
                    segment.
                  example: A calm and relaxing piano track.
                lyrics:
                  type: string
                  description: >-
                    Lyrics content. Optional. For V6, V6_MINI, and V6_WILD:
                    maximum 5000 characters. Lyrics for the replaced segment
                    only. Distinct from `fullLyrics`, which is the complete song
                    lyrics.
                  example: '[Verse] Night city lights shining bright'
                tags:
                  type: string
                  description: Music style tags, such as jazz, electronic, etc.
                  example: Jazz
                title:
                  type: string
                  description: Music title
                  example: Relaxing Piano
                negativeTags:
                  type: string
                  description: >-
                    Excluded music styles, used to avoid specific style elements
                    in the replacement segment
                  example: Rock
                infillStartS:
                  type: number
                  description: >-
                    Start time point for replacement (seconds), 2 decimal
                    places. Must be less than infillEndS. The time interval
                    (infillEndS - infillStartS) must be at least 10 seconds.
                  minimum: 0
                  example: 10.5
                infillEndS:
                  type: number
                  description: >-
                    End time point for replacement (seconds), 2 decimal places.
                    Must be greater than infillStartS. The time interval
                    (infillEndS - infillStartS) must be at least 10 seconds.
                  minimum: 0
                  example: 20.75
                fullLyrics:
                  type: string
                  description: >-
                    Complete lyrics of the whole song after modification,
                    combining both modified and unmodified lyrics. Distinct from
                    `lyrics` (and `prompt`), which apply only to the replaced
                    segment. This field is the full lyrics text used for the
                    entire song after the section replacement.
                  example: |-
                    [Verse 1]
                    Original lyrics here
                    [Chorus]
                    Modified lyrics for this section
                    [Verse 2]
                    More original lyrics
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
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    Callback URL for task completion. The system will send a
                    POST request to this URL when replacement is complete,
                    containing task status and results.


                    - Your callback endpoint should be able to accept POST
                    requests containing JSON payloads with replacement results

                    - For detailed callback format and implementation guide, see
                    [Replace Music Section
                    Callbacks](/suno-api/replace-section-callbacks)

                    - Alternatively, you can use the get music details interface
                    to poll task status
                  example: https://example.com/callback
            example:
              taskId: 2fac****9f72
              audioId: e231****-****-****-****-****8cadc7dc
              prompt: A calm and relaxing piano track.
              tags: Jazz
              title: Relaxing Piano
              negativeTags: Rock
              infillStartS: 10.5
              infillEndS: 20.75
              fullLyrics: |-
                [Verse 1]
                Original lyrics here
                [Chorus]
                Modified lyrics for this section
                [Verse 2]
                More original lyrics
              callBackUrl: https://example.com/callback
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
                          Response status code


                          - **200**: Success - Request processed successfully

                          - **401**: Unauthorized - Authentication credentials
                          missing or invalid

                          - **402**: Insufficient credits - Account does not
                          have enough credits to perform this operation

                          - **404**: Not found - Requested resource or endpoint
                          does not exist

                          - **409**: Conflict - WAV record already exists

                          - **422**: Validation error - Request parameters
                          failed validation checks

                          - **429**: Rate limit exceeded - Exceeded request
                          limit for this resource

                          - **451**: Unauthorized - Failed to retrieve image.
                          Please verify any access restrictions set by you or
                          your service provider.

                          - **455**: Service unavailable - System is currently
                          undergoing maintenance

                          - **500**: Server error - Unexpected error occurred
                          while processing request
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
                              Task ID for tracking task status. You can use this
                              ID to query task details and results through the
                              "Get Music Details" interface.
                            example: 5c79****be8e
        '500':
          $ref: '#/components/responses/Error'
      callbacks:
        audioGenerated:
          '{request.body#/callBackUrl}':
            post:
              description: >-
                When audio generation is complete, the system will call this
                callback to notify the result.


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
                        "prompt": "A calm and relaxing piano track.",
                        "model_name": "chirp-v3-5",
                        "title": "Relaxing Piano",
                        "tags": "Jazz",
                        "createTime": "2025-01-01 00:00:00",
                        "duration": 198.44
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
                          description: Return message
                          example: All generated successfully
                        data:
                          type: object
                          properties:
                            callbackType:
                              type: string
                              description: >-
                                Callback type: text (text generation complete),
                                first (first song complete), complete (all
                                complete)
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


                                  - **200**: Success - Request processed
                                  successfully

                                  - **400**: Validation error - Lyrics contain
                                  copyrighted content.

                                  - **408**: Rate limit exceeded - Timeout.

                                  - **413**: Conflict - Uploaded audio matches
                                  existing artwork.

                                  - **500**: Server error - Unexpected error
                                  occurred while processing request

                                  - **501**: Audio generation failed.

                                  - **531**: Server error - Sorry, generation
                                  failed due to issues. Your credits have been
                                  refunded. Please try again.
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