> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Get Verification Phrase

> Query the validation phrase generation result for a Suno Voice task.

### Usage Guide

* Use the `taskId` returned by the validation phrase generation or regeneration API.
* When the task reaches `wait_validating`, read `validateInfo` and ask the user to record that phrase.
* If the task fails, inspect `errorCode` and `errorMessage` before retrying.

### Status Handling

| Status                     | Meaning                                           |
| -------------------------- | ------------------------------------------------- |
| `wait_processing`          | Task is waiting to be processed                   |
| `processing_validate`      | Validation phrase is being generated              |
| `processing_validate_fail` | Validation phrase generation failed               |
| `wait_validating`          | Phrase is ready and waiting for user verification |
| `success`                  | The full voice creation flow has completed        |
| `fail`                     | Task failed                                       |

### Next Step

<Card title="Generate Voice" icon="lucide-mic" href="/suno-api/suno-voice-generate">
  Submit the verification audio and create the final custom voice
</Card>


## OpenAPI

````yaml suno-api/suno-voice-api.json GET /api/v1/voice/validate-info
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
  /api/v1/voice/validate-info:
    get:
      tags:
        - docs/en/Market/Suno API/voice
        - suno接口/voice
      summary: Suno Voice Get Verification Phrase API
      description: >
        Query the validation phrase generation result for a Suno Voice task.


        Use this endpoint with the `taskId` returned by the validation phrase
        generation or regeneration endpoint. When the task is ready, the
        response contains `validateInfo`, which is the phrase the user should
        record for voice verification.


        ## Status Handling


        Check the `status` field to determine the next action:


        - `wait_processing` or `processing_validate`: the validation phrase is
        still being generated

        - `processing_validate_fail` or `fail`: the task failed, check
        `errorMessage` for details

        - `wait_validating`: the phrase is ready and waiting for the user to
        record verification audio

        - `success`: the validation and voice creation flow has completed


        ## Continue the Flow


        After receiving `validateInfo`, record or upload audio of the user
        performing that phrase and submit it to the voice generation endpoint.
        For best voice generation results, singing is recommended.


        <Card
          title="Generate Voice"
          icon="lucide-mic"
          href="/suno-api/suno-voice-generate"
        >
          Submit the user's verification audio to generate the final custom voice
        </Card>


        Related resources


        <CardGroup cols={2}>
          <Card title="Generate Validation Phrase" icon="lucide-file-audio" href="/suno-api/suno-voice-validate"> Create a validation phrase from source audio </Card>
          <Card title="Regenerate Validation Phrase" icon="lucide-refresh-cw" href="/suno-api/suno-voice-regenerate"> Generate a new phrase for an existing task </Card>
        </CardGroup>
      operationId: suno-voice-validate-info
      parameters:
        - name: taskId
          in: query
          description: 任务id
          required: false
          schema:
            type: string
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
                      validateInfo:
                        type: string
                        description: Validation phrase text
                      status:
                        type: string
                        description: Task status
                        enum:
                          - wait_processing
                          - processing_validate
                          - processing_validate_fail
                          - wait_validating
                          - success
                          - fail
                      errorCode:
                        type: integer
                      errorMessage:
                        type: string
                    required:
                      - taskId
                      - validateInfo
                      - status
                      - errorCode
                      - errorMessage
                required:
                  - code
                  - msg
                  - data
              example:
                code: 200
                msg: success
                data:
                  taskId: xxx_task_id_xxx
                  validateInfo: Harmonies fill the air with joyful melodies tonight
                  status: >-
                    wait_processing, processing_validate: waiting for validation
                    code, processing_validate_fail: failed to obtain validation
                    code, wait_validating: waiting for verification, success,
                    fail
                  errorCode: 500
                  errorMessage: xxxxx
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