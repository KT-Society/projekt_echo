> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Check Availability

> Check whether a generated Suno custom voice is available for use.

### Usage Guide

* Use this endpoint after the custom voice generation task succeeds.
* Submit the related task ID in `task_id`.
* If `isAvailable` is `true`, the generated voice is ready for supported Suno generation workflows.

### When to Use

Call this endpoint before starting a generation request that depends on a custom voice. It helps avoid submitting downstream tasks while the voice is still unavailable.

### Related Endpoint

<Card title="Get Custom Voice Record" icon="lucide-list-checks" href="/suno-api/suno-voice-record-info">
  Query the latest task status and generated voice information before checking availability
</Card>


## OpenAPI

````yaml suno-api/suno-voice-api.json POST /api/v1/voice/check-voice
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
  /api/v1/voice/check-voice:
    post:
      tags:
        - docs/en/Market/Suno API/voice
        - suno接口/voice
      summary: Suno Voice Check Availability API
      description: >
        Check whether a generated Suno custom voice is available.


        Use this endpoint after voice generation completes to verify that the
        generated voice can be used in supported Suno generation APIs. Submit
        the related task ID and check the `isAvailable` value in the response.


        ## When to Use


        This endpoint is useful when you need to confirm voice availability
        before starting a music generation request that depends on the custom
        voice.


        <Card
          title="Get Voice Record"
          icon="lucide-search"
          href="/suno-api/suno-voice-record-info"
        >
          Query the voice generation task first to obtain the latest task status and generated voice information
        </Card>


        Related resources


        <CardGroup cols={2}>
          <Card title="Generate Voice" icon="lucide-mic" href="/suno-api/suno-voice-generate"> Create a custom voice from verification audio </Card>
          <Card title="General API" icon="lucide-cog" href="/suno-api/get-remaining-credits"> View account credits and usage </Card>
        </CardGroup>
      operationId: suno-voice-check-voice
      parameters: []
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                task_id:
                  description: Task ID that needs to be checked
                  type: string
              required:
                - task_id
            example:
              task_id: ''
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
                      isAvailable:
                        type: boolean
                    required:
                      - isAvailable
                required:
                  - code
                  - msg
                  - data
              example:
                code: 200
                msg: success
                data:
                  isAvailable: true
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