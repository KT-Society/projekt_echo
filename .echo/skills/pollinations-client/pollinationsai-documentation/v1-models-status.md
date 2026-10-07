# Endpoint: /v1/models/status\n\n## Method: GET\n\n**Summary:** Model Health Status\n\n**Description:** Returns raw model health rows from the public Tinybird `model_health` pipe.

The optional `minutes` query parameter controls the rolling window and must be an integer between 1 and 10080.
The X-Model-Status-Timestamp response header reports when the data was fetched from Tinybird; X-Model-Status-Stale is set when stale data is returned during an upstream failure.\n\n