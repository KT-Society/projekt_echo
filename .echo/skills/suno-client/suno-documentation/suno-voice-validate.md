> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Generate Verification Phrase

> Generate the validation phrase required for the Suno Voice custom voice workflow.

### Usage Guide

* Submit the source recording URL and the vocal segment you want to use for voice creation.
* The API returns a `taskId`; use it to query the generated validation phrase.
* When `callBackUrl` is provided, the system sends a POST callback when the phrase is ready or the task fails. The callback URL must be publicly accessible and return HTTP 200 within 15 seconds.
* After receiving `validateInfo`, ask the user to record the phrase and upload the verification audio to the voice generation API. For best voice generation results, singing is recommended.

### Workflow

1. Upload or host the source audio and make sure `voiceUrl` is publicly accessible.
2. Choose a clean vocal segment with `vocalStartS` and `vocalEndS`.
3. Submit the validation phrase task and store the returned `taskId`.
4. Wait for `validateInfo` through the query API or callback.
5. Record the user performing the validation phrase, then call the custom voice generation API. For best voice generation results, singing is recommended.

### Callback

<Card title="Validation Phrase Callbacks" icon="lucide-webhook" href="/suno-api/suno-voice-validate-callbacks">
  Learn the callback payload sent when the validation phrase is ready or the task fails
</Card>

### Developer Notes

* `vocalEndS` must be greater than `vocalStartS`.
* Use a segment with clear speech and minimal background noise for better validation.
* `language` controls the validation phrase language. Supported values include `en`, `zh`, `es`, `fr`, `pt`, `de`, `ja`, `ko`, `hi`, and `ru`.


## OpenAPI

````yaml suno-api/suno-voice-api.json POST /api/v1/voice/validate
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
  /api/v1/voice/validate:
    post:
      tags:
        - docs/en/Market/Suno API/voice
        - suno接口/voice
      summary: Suno Voice Generate Verification Phrase API
      description: >
        Generate a validation phrase for the Suno Voice custom voice workflow.


        Submit the source audio URL and the selected vocal segment. The system
        will analyze the source voice and create a validation phrase for the
        user to record in the next step.


        ## Query Task Status


        After submitting the task, you can check the validation phrase
        generation progress and obtain the generated phrase through the
        validation phrase query endpoint:


        <Card
          title="Get Validation Phrase"
          icon="lucide-search"
          href="/suno-api/suno-voice-validate-info"
        >
          Learn how to check the validation phrase task status and obtain the phrase users should record
        </Card>


        :::tip[]

        In the production environment, it is recommended to use the
        `callBackUrl` parameter to receive automatic notifications when the
        validation phrase is ready, rather than polling the status endpoint.

        :::


        ## Next Step


        After the validation phrase is ready, ask the user to record the phrase
        and upload the verification audio to continue creating the voice. For
        best voice generation results, singing is recommended.


        <Card
          title="Generate Voice"
          icon="lucide-mic"
          href="/suno-api/suno-voice-generate"
        >
          Submit the verification audio and generate the final custom voice
        </Card>


        Related resources


        <CardGroup cols={2}>
          <Card title="Regenerate Validation Phrase" icon="lucide-refresh-cw" href="/suno-api/suno-voice-regenerate"> Generate a new validation phrase for an existing task </Card>
          <Card title="General API" icon="lucide-cog" href="/suno-api/get-remaining-credits"> View account credits and usage </Card>
        </CardGroup>
      operationId: suno-voice-validate
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                voiceUrl:
                  description: The original recording URL uploaded by the user [Required]
                  type: string
                vocalStartS:
                  description: >-
                    Start time (in seconds) for extracting the vocal segment
                    [Required]
                  type: integer
                vocalEndS:
                  description: >-
                    End time (in seconds) for extracting the vocal segment, must
                    be greater than vocalStartS [Required]
                  type: integer
                language:
                  description: >-
                    Verify the language of the short phrase. Supported languages
                    ​​include: English (en), Chinese (zh), Spanish (es), French
                    (fr), Portuguese (pt), German (de), Japanese (ja), Korean
                    (ko), Hindi (hi), and Russian (ru).
                  type: string
                callBackUrl:
                  description: >-
                    Callback URL used to receive validation phrase generation
                    results. The system sends a POST request when the phrase is
                    ready (`status: wait_validating`) or when the task fails.
                    The URL must be publicly accessible and return HTTP 200
                    within 15 seconds. For the payload format, see [Validation
                    Phrase
                    Callbacks](https://docs.sunoapi.org/suno-api/suno-voice-validate-callbacks).
                  type: string
              required:
                - voiceUrl
                - vocalStartS
                - vocalEndS
            example:
              voiceUrl: https://example.com/audio/user_voice.mp3
              vocalStartS: 0
              vocalEndS: 10
              language: en
              callBackUrl: https://example.com/callback/suno/voice_prepare
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