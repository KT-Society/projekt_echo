> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Regenerate Phrase Callbacks

> Receive POST callbacks when a regenerated Suno Voice validation phrase is ready or fails.

When you submit a phrase regeneration task, provide the callback URL using the `calBackUrl` field from the API schema. The system sends a POST request when the regenerated phrase is ready or the task fails.

## Callback Mechanism Overview

<Info>
  The regenerated phrase callback uses the same response shape as validation phrase generation callbacks.
</Info>

### Callback Timing

* New validation phrase generated and ready for the user to record
* Phrase regeneration failed
* Error occurred during task processing

### Callback Method

* **HTTP Method**: POST
* **Content Type**: application/json
* **Timeout**: 15 seconds

## Callback Request Format

<CodeGroup>
  ```json Regenerated Phrase Ready Callback theme={null}
  {
    "code": 200,
    "msg": "success",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "validateInfo": "Please record this new validation phrase clearly.",
      "status": "wait_validating",
      "errorCode": 0,
      "errorMessage": ""
    }
  }
  ```

  ```json Regenerated Phrase Failed Callback theme={null}
  {
    "code": 400,
    "msg": "Validation phrase regeneration failed",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "validateInfo": "",
      "status": "processing_validate_fail",
      "errorCode": 500,
      "errorMessage": "Failed to regenerate validation phrase"
    }
  }
  ```
</CodeGroup>

## Field Description

<ParamField path="code" type="integer" required>
  Callback status code. `200` indicates success; non-200 values indicate task failure or processing error.
</ParamField>

<ParamField path="msg" type="string" required>
  Status message describing the callback result.
</ParamField>

<ParamField path="data.taskId" type="string" required>
  Task ID returned by the phrase regeneration API.
</ParamField>

<ParamField path="data.validateInfo" type="string">
  Regenerated validation phrase text. Returned when `status` is `wait_validating`.
</ParamField>

<ParamField path="data.status" type="string" required>
  Task status. Common callback statuses are `wait_validating`, `processing_validate_fail`, and `fail`.
</ParamField>

<ParamField path="data.errorCode" type="integer">
  Error code returned when the task fails.
</ParamField>

<ParamField path="data.errorMessage" type="string">
  Detailed error message returned when the task fails.
</ParamField>

## Related Endpoint

<Card title="Get Verification Phrase" icon="lucide-search" href="/suno-api/suno-voice-validate-info">
  Query the regenerated phrase manually with taskId
</Card>
