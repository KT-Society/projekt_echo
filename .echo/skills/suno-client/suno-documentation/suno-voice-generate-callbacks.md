> ## Documentation Index
> Fetch the complete documentation index at: https://docs.sunoapi.org/llms.txt
> Use this file to discover all available pages before exploring further.

# Suno Voice Generation Callbacks

> Receive POST callbacks when a Suno Voice custom voice task succeeds or fails.

When you submit a custom voice generation task with `callBackUrl`, the system sends a POST request to your callback URL when the task completes.

## Callback Mechanism Overview

<Info>
  The callback contains the generated `voiceId` when custom voice creation succeeds.
</Info>

### Callback Timing

* Custom voice created successfully
* Voice verification or creation failed
* Error occurred during task processing

### Callback Method

* **HTTP Method**: POST
* **Content Type**: application/json
* **Timeout**: 15 seconds

## Callback Request Format

<CodeGroup>
  ```json Custom Voice Ready Callback theme={null}
  {
    "code": 200,
    "msg": "success",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "voiceId": "voice_xxx",
      "status": "success",
      "errorCode": 0,
      "errorMessage": ""
    }
  }
  ```

  ```json Custom Voice Failed Callback theme={null}
  {
    "code": 400,
    "msg": "Voice generation failed",
    "data": {
      "taskId": "xxx_task_id_xxx",
      "voiceId": "",
      "status": "fail",
      "errorCode": 500,
      "errorMessage": "Verification audio did not match the validation phrase"
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
  Task ID returned by the custom voice generation API.
</ParamField>

<ParamField path="data.voiceId" type="string">
  Generated custom voice ID. Returned when `status` is `success`.
</ParamField>

<ParamField path="data.status" type="string" required>
  Task status. Common callback statuses are `success`, `processing_validate_fail`, and `fail`.
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

app.post('/suno/voice-generate-callback', (req, res) => {
  const { code, msg, data } = req.body;

  if (code === 200 && data.status === 'success') {
    console.log('Custom voice ready:', data.voiceId);
  } else {
    console.error('Custom voice task failed:', msg, data.errorMessage);
  }

  res.status(200).json({ status: 'received' });
});

app.listen(3000);
```

## Related Endpoint

<Card title="Get Custom Voice Record" icon="lucide-list-checks" href="/suno-api/suno-voice-record-info">
  Query the same voice generation task manually with taskId
</Card>
