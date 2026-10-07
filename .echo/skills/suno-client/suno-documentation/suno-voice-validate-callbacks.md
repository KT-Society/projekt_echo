> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Validation Phrase Callbacks

> Receive POST callbacks when a Suno Voice validation phrase task is ready or fails.

When you submit a validation phrase task with `callBackUrl`, the system sends a POST request to your callback URL after the validation phrase task reaches a terminal state.

## Callback Mechanism Overview

<Info>
  Use callbacks in production to avoid polling the validation phrase query endpoint.
</Info>

### Callback Timing

* Validation phrase generated and ready for the user to record
* Validation phrase generation failed
* Error occurred during task processing

### Callback Method

* **HTTP Method**: POST
* **Content Type**: application/json
* **Timeout**: 15 seconds

## Callback Request Format

<CodeGroup>
  ```json Validation Phrase Ready Callback theme={null}
  {
    "code": 200,
    "msg": "success",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "validateInfo": "Please record this validation phrase clearly.",
      "status": "wait_validating",
      "errorCode": 0,
      "errorMessage": ""
    }
  }
  ```

  ```json Validation Phrase Failed Callback theme={null}
  {
    "code": 400,
    "msg": "Validation phrase generation failed",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "validateInfo": "",
      "status": "processing_validate_fail",
      "errorCode": 500,
      "errorMessage": "Failed to generate validation phrase"
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
  Task ID returned by the validation phrase generation API.
</ParamField>

<ParamField path="data.validateInfo" type="string">
  Validation phrase text. Returned when `status` is `wait_validating`.
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

## Receiving Callbacks

```javascript Node.js theme={null}
const express = require('express');
const app = express();

app.use(express.json());

app.post('/suno/voice-validate-callback', (req, res) => {
  const { code, msg, data } = req.body;

  if (code === 200 && data.status === 'wait_validating') {
    console.log('Validation phrase ready:', data.taskId, data.validateInfo);
  } else {
    console.error('Validation phrase task failed:', msg, data.errorMessage);
  }

  res.status(200).json({ status: 'received' });
});

app.listen(3000);
```

## Related Endpoint

<Card title="Get Verification Phrase" icon="lucide-search" href="/suno-api/suno-voice-validate-info">
  Query the same task status manually with taskId
</Card>
