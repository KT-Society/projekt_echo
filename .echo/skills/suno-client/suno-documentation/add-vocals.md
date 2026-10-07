> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Add Vocals

> This endpoint layers AI-generated vocals on top of an existing instrumental. Given a prompt (e.g., lyrical concept or musical mood) and optional audio, it produces vocal output harmonized with the provided track.

### Model Versions

* **Current models**: `V6` (default), `V6_WILD`, `V6_MINI`
* **Deprecated models**: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`
* Deprecated values remain available only for backward compatibility. New integrations should use a V6-series model.

### **Key Capabilities**

* Accepts an existing instrumental via uploadUrl, with optional prompt-based stylistic input.
* Supports control parameters including:
  * lyrics, prompt, style, tags, negativeTags (define lyrical content and vocal style)
  * vocalGender, styleWeight, weirdnessConstraint, audioWeight, variety, callBackUrl.
* Returns a taskId, supports the same 14-day retention and three-stage callback model as the instrumental endpoint  .

### **Typical Use Cases**

* Music platforms or tools enabling topline creation and rapid prototyping of lyrical ideas.
* Collaborative songwriting or co-creation workflows, where lyrics or vocal styles are iteratively tested over instrumental drafts.

### Parameter Details

* A source audio (`uploadUrl`) is enough to start generation together with the required fields below. Remaining fields are optional.
* **Required fields**: `uploadUrl`, `callBackUrl`, `title`, `negativeTags`, `style`
* **Upload URL**: Must be a valid, publicly accessible audio file URL
* **Style**: Describes the overall genre and vocal approach (Jazz, Classical, Electronic, Pop)
* **Negative Tags**: Music styles or vocal traits to exclude from generation
* **Title**: Used as the title for the generated vocal track

### Optional parameters

<Note>
  The following fields are optional controls available for this endpoint:

  * <b>lyrics</b> (string): Lyrics content. Optional. V6 series maximum 5000 characters. Takes priority over `prompt` as lyrics.
  * <b>prompt</b> (string): Lyrics content. Optional. Used as lyrics when `lyrics` is not provided. V6 series maximum 5000 characters.
  * <b>vocalGender</b> (string): Preferred vocal gender. Allowed values: `m` (male), `f` (female)
  * <b>styleWeight</b> (number): Style adherence weight in range 0–1 (recommended two decimals)
  * <b>weirdnessConstraint</b> (number): Creativity/novelty constraint in range 0–1 (recommended two decimals)
  * <b>audioWeight</b> (number): Relative weight of audio consistency in range 0–1 (recommended two decimals)
  * <b>variety</b> (number): Diversity of generated results. Integer from 0–4, default 1. `0` off, `1` normal (default), `2` high, `3` extra, `4` max.
  * <b>model</b> (string): Model version used for generation. Current values: `V6` (default), `V6_WILD`, `V6_MINI`. Deprecated: `V5_5`, `V5`, `V4_5PLUS`, `V4_5ALL`, `V4_5`, `V4`.
</Note>

### Developer Notes

* Callback process has three stages: `text` (text generation), `first` (first track complete), `complete` (all tracks complete)
* In some cases, `text` and `first` stages may be skipped, directly returning `complete`
* See [Add Vocals Callbacks](./add-vocals-callbacks) for detailed callback format
* Monitor task progress using [Get Music Generation Details](./get-music-generation-details)


## OpenAPI

````yaml suno-api/suno-api.json POST /api/v1/generate/add-vocals
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
  /api/v1/generate/add-vocals:
    post:
      tags:
        - Music Generation
      summary: Add Vocals
      operationId: add-vocals
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - uploadUrl
                - callBackUrl
                - title
                - negativeTags
                - style
              properties:
                prompt:
                  type: string
                  description: >-
                    Lyrics content. Optional. Used as lyrics when `lyrics` is
                    not provided. If `lyrics` is also provided, `lyrics` takes
                    priority. For V6, V6_MINI, and V6_WILD: maximum 5000
                    characters.
                  example: A calm and relaxing piano track with soothing vocals
                lyrics:
                  type: string
                  description: >-
                    Lyrics for the generated audio. Optional. For V6, V6_MINI,
                    and V6_WILD: maximum 5000 characters. Takes priority over
                    `prompt` as lyrics. If omitted, `prompt` is used as lyrics.
                  example: '[Verse] Night city lights shining bright'
                title:
                  type: string
                  description: >-
                    The title of the music track.  

                    - Required.  

                    - This will be used as the title for the generated vocal
                    track.
                  example: Relaxing Piano with Vocals
                negativeTags:
                  type: string
                  description: >-
                    Music styles or vocal traits to exclude from the generated
                    track.  

                    - Required.  

                    - Use to avoid specific vocal styles or characteristics.  
                      Example: "Heavy Metal, Aggressive Vocals"
                  example: Heavy Metal, Aggressive Vocals
                style:
                  type: string
                  description: |-
                    The music and vocal style.  
                    - Required.  
                    - Examples: "Jazz", "Classical", "Electronic", "Pop".  
                    - Describes the overall genre and vocal approach.
                  example: Jazz
                vocalGender:
                  type: string
                  description: >-
                    Preferred vocal gender. Optional. Allowed values: 'm'
                    (male), 'f' (female).
                  enum:
                    - m
                    - f
                  example: m
                styleWeight:
                  type: number
                  description: >-
                    Style adherence weight. Optional. Range: 0-1. Two decimal
                    places recommended.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.61
                weirdnessConstraint:
                  type: number
                  description: >-
                    Creativity/novelty constraint. Optional. Range: 0-1. Two
                    decimal places recommended.
                  minimum: 0
                  maximum: 1
                  multipleOf: 0.01
                  example: 0.72
                audioWeight:
                  type: number
                  description: >-
                    Relative weight of audio consistency versus other controls.
                    Optional. Range: 0-1. Two decimal places recommended.
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
                uploadUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL of the uploaded audio file to add vocals to.  

                    - Required.  

                    - Must be a valid audio file URL accessible by the system.  

                    - The uploaded audio should be in a supported format (MP3,
                    WAV, etc.).
                  example: https://example.com/instrumental.mp3
                callBackUrl:
                  type: string
                  format: uri
                  description: >-
                    The URL to receive task completion notifications when vocal
                    generation is complete. The callback process has three
                    stages: `text` (text generation), `first` (first track
                    complete), `complete` (all tracks complete). Note: In some
                    cases, `text` and `first` stages may be skipped, directly
                    returning `complete`.

                    - For detailed callback format and implementation guide, see
                    [Add Vocals
                    Callbacks](https://docs.api.box/suno-api/add-vocals-callbacks)

                    - Alternatively, you can use the Get Music Generation
                    Details interface to poll task status
                  example: https://api.example.com/callback
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
        vocalsAdded:
          '{request.body#/callBackUrl}':
            post:
              description: >-
                System will call this callback when vocal generation is
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
                        "prompt": "[Verse] Calm and relaxing melodies with soothing vocals",
                        "model_name": "chirp-v3-5",
                        "title": "Relaxing Piano with Vocals",
                        "tags": "relaxing, piano, vocals, jazz",
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