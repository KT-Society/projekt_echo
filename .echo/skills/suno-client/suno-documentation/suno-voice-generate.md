> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Create Custom Voice

> Generate a reusable Suno custom voice from the user's verification recording.

### Usage Guide

* Call this API after the validation phrase is generated and the user has recorded the verification audio.
* The validation phrase is the `validateInfo` text returned by the server. For best voice generation results, have the user record the server-provided phrase in a singing voice rather than plain speech.
* Submit the original validation `taskId` and the verification audio URL in `verifyUrl`.
* Optional metadata such as `voiceName`, `description`, `style`, and `singerSkillLevel` helps organize and tune the generated voice.
* The API returns a `taskId`; use it to query the final `voiceId`.
* When `callBackUrl` is provided, the system sends a POST callback when the voice is created or the task fails. The callback URL must be publicly accessible and return HTTP 200 within 15 seconds.

### Workflow

1. Generate and retrieve the validation phrase.
2. Record clear verification audio for the phrase; singing is recommended for best voice generation results.
3. Upload or host the verification audio and pass the URL as `verifyUrl`.
4. Submit the voice generation task and store the returned `taskId`.
5. Receive `voiceId` through the record query API or callback when the task succeeds.

### Callback

<Card title="Custom Voice Generation Callbacks" icon="lucide-webhook" href="/suno-api/suno-voice-generate-callbacks">
  Learn the callback payload sent when the custom voice is created or the task fails
</Card>

### Developer Notes

* `taskId` must come from the validation phrase task for the same voice workflow.
* `verifyUrl` should point to the user's recording of the exact validation phrase returned by the server; for best results, recording it in a singing voice is recommended.
* After receiving `voiceId`, use the availability check endpoint before starting generation workflows that depend on the custom voice.


## OpenAPI

````yaml suno-api/suno-voice-api.json POST /api/v1/voice/generate
openapi: 3.0.1
info:
  title: Suno Voice API
  description: API documentation for Suno Voice custom voice services
  version: 1.0.0
  contact:
    name: Technical Support
    email: support@sunoapi.org
servers:
  - url: https://api.sunoapi.org
    description: API Server
security:
  - BearerAuth: []
tags:
  - name: docs
  - name: docs/en
  - name: docs/en/Market
  - name: docs/en/Market/Suno API
  - name: docs/en/Market/Suno API/voice
  - name: suno接口/voice
paths:
  /api/v1/voice/generate:
    post:
      tags:
        - docs/en/Market/Suno API/voice
        - suno接口/voice
      summary: Suno Voice Create Custom Voice API
      description: >
        Generate a custom Suno Voice from verification audio for the validation
        phrase returned by the server.


        Submit the original validation task ID, the user's verification audio
        URL, and optional voice metadata such as `voiceName`, `description`, and
        `style`. For best voice generation results, the verification audio
        should contain the user recording the exact `validateInfo` phrase in a
        singing voice rather than plain speech. The system will validate the
        recording and create a reusable custom voice.


        ## Query Task Status


        After submitting the task, you can check the voice generation progress
        and obtain the final `voiceId` through the voice record query endpoint:


        <Card
          title="Get Voice Record"
          icon="lucide-search"
          href="/suno-api/suno-voice-record-info"
        >
          Learn how to check the custom voice generation status and obtain the generated voiceId
        </Card>


        :::tip[]

        In the production environment, it is recommended to use the
        `callBackUrl` parameter to receive automatic notifications when the
        custom voice is generated, rather than polling the status endpoint.

        :::


        ## Use the Generated Voice


        When the task succeeds, the response from the query or callback contains
        `voiceId`. You can use this ID in supported Suno generation endpoints
        that accept a custom voice.


        Related resources


        <CardGroup cols={2}>
          <Card title="Check Voice Availability" icon="lucide-badge-check" href="/suno-api/suno-voice-check-voice"> Verify whether a generated voice is available for use </Card>
          <Card title="General API" icon="lucide-cog" href="/suno-api/get-remaining-credits"> View account credits and usage </Card>
        </CardGroup>
      operationId: suno-voice-generate
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                taskId:
                  description: Task ID
                  type: string
                verifyUrl:
                  description: >-
                    Audio URL for the user's recording of the validation phrase
                    returned by the server; singing is recommended for best
                    results [Required]
                  type: string
                voiceName:
                  description: Voice name
                  type: string
                description:
                  description: Voice description
                  type: string
                style:
                  description: Voice style
                  type: string
                singerSkillLevel:
                  type: string
                  description: >-
                    Singer skill level. Supported: beginner, intermediate,
                    advanced, professional
                  default: beginner
                  enum:
                    - beginner
                    - intermediate
                    - advanced
                    - professional
                  x-apidog-enum:
                    - value: beginner
                      name: ''
                      description: ''
                    - value: intermediate
                      name: ''
                      description: ''
                    - value: advanced
                      name: ''
                      description: ''
                    - value: professional
                      name: ''
                      description: ''
                callBackUrl:
                  description: >-
                    Callback URL used to receive custom voice generation
                    results. When the task succeeds, the callback includes the
                    generated `voiceId`; when it fails, it includes `errorCode`
                    and `errorMessage`. The URL must be publicly accessible and
                    return HTTP 200 within 15 seconds. For the payload format,
                    see [Custom Voice Generation
                    Callbacks](https://docs.sunoapi.org/suno-api/suno-voice-generate-callbacks).
                  type: string
              required:
                - taskId
                - verifyUrl
            example:
              taskId: voice_create_001
              verifyUrl: https://example.com/audio/verify_read.mp3
              voiceName: My Voice
              description: created from uploaded voice
              style: Pop, Female Vocal
              singerSkillLevel: beginner
              callBackUrl: https://example.com/callback/suno/voice_create
        required: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  code:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      taskId:
                        description: Task ID
                        type: string
                    required:
                      - taskId
                required:
                  - code
                  - msg
                  - data
              example:
                code: 200
                msg: success
                data:
                  taskId: xxx_task_id_xxx
          headers: {}
      deprecated: false
      security:
        - BearerAuth1: []
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API Key
      description: >-
        # API Authentication


        All endpoints require authentication using Bearer Token.


        ## Get API Key


        1. Visit the [API Key Management Page](https://sunoapi.org/api-key) to
        obtain your API Key


        ## Usage


        Add to request headers:


        ```

        Authorization: Bearer YOUR_API_KEY

        ```


        > **Note:**

        > - Keep your API Key secure and do not share it with others

        > - If you suspect your API Key has been compromised, reset it
        immediately from the management page
    BearerAuth1:
      type: http
      scheme: bearer
      bearerFormat: API Key
      description: >-
        # API Authentication


        All endpoints require authentication using Bearer Token.


        ## Get API Key


        1. Visit the [API Key Management Page](https://sunoapi.org/api-key) to
        obtain your API Key


        ## Usage


        Add to request headers:


        ```

        Authorization: Bearer YOUR_API_KEY

        ```


        > **Note:**

        > - Keep your API Key secure and do not share it with others

        > - If you suspect your API Key has been compromised, reset it
        immediately from the management page

````