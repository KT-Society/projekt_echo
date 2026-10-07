> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Regenerate Verification Phrase

> Regenerate the validation phrase for an existing Suno Voice task.

### Usage Guide

* Use this API when the previous validation phrase failed, expired, or the user needs a new phrase.
* Submit the existing `taskId` from the voice validation workflow.
* The API schema uses `calBackUrl` for the callback URL field. The system sends a POST callback when the regenerated phrase is ready or the task fails. The callback URL must be publicly accessible and return HTTP 200 within 15 seconds.
* Query the validation phrase result again with the returned `taskId`.

### Workflow

1. Submit the existing validation task ID.
2. Store the returned `taskId`.
3. Wait for the regenerated `validateInfo` through the query API or callback.
4. Ask the user to record the new phrase and submit the verification audio to the voice generation API. For best voice generation results, singing is recommended.

### Callback

<Card title="Regenerated Validation Phrase Callbacks" icon="lucide-webhook" href="/suno-api/suno-voice-regenerate-callbacks">
  Learn the callback payload sent when the regenerated phrase is ready or the task fails
</Card>

### Developer Notes

* Keep the regenerated phrase and verification recording paired with the same task flow.
* If phrase generation repeatedly fails, choose a cleaner source vocal segment and restart the validation step.


## OpenAPI

````yaml suno-api/suno-voice-api.json POST /api/v1/voice/regenerate
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
  /api/v1/voice/regenerate:
    post:
      tags:
        - docs/en/Market/Suno API/voice
        - suno接口/voice
      summary: Suno Voice Regenerate Verification Phrase
      description: >
        Regenerate the validation phrase for an existing Suno Voice task.


        Use this endpoint when the previous validation phrase failed, expired,
        or the user needs a new phrase to record. Submit the existing `taskId`;
        the system will start a new validation phrase generation task and return
        a task ID for polling.


        ## Query Task Status


        After submitting the regeneration task, check the new validation phrase
        result through the validation phrase query endpoint:


        <Card
          title="Get Validation Phrase"
          icon="lucide-search"
          href="/suno-api/suno-voice-validate-info"
        >
          Learn how to check the regenerated validation phrase task status
        </Card>


        ## Continue the Flow


        Once the regenerated phrase is ready, ask the user to record the new
        phrase and submit the verification audio to the voice generation
        endpoint. For best voice generation results, singing is recommended.


        <Card
          title="Generate Voice"
          icon="lucide-mic"
          href="/suno-api/suno-voice-generate"
        >
          Continue custom voice generation with the newly recorded verification audio
        </Card>


        Related resources


        <CardGroup cols={2}>
          <Card title="Generate Validation Phrase" icon="lucide-file-audio" href="/suno-api/suno-voice-validate"> Start the validation phrase flow from source audio </Card>
          <Card title="Get Voice Record" icon="lucide-list-checks" href="/suno-api/suno-voice-record-info"> Query the final custom voice generation result </Card>
        </CardGroup>
      operationId: suno-voice-regenerate
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
                calBackUrl:
                  type: string
                  description: >-
                    Callback URL used to receive regenerated validation phrase
                    results. Note that this endpoint uses the field name
                    `calBackUrl`. The system sends a POST request when the new
                    phrase is ready (`status: wait_validating`) or when the task
                    fails. The URL must be publicly accessible and return HTTP
                    200 within 15 seconds. For the payload format, see
                    [Regenerated Validation Phrase
                    Callbacks](https://docs.sunoapi.org/suno-api/suno-voice-regenerate-callbacks).
              required:
                - taskId
                - calBackUrl
            example:
              taskId: xxxxxxx
              calBackUrl: https://example.com/callback/suno/voice_regenerate
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