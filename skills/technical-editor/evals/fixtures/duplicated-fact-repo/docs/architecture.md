# Architecture

The API accepts orders and publishes them to SQS. The worker consumes from SQS and writes to
Postgres.

## Retry behaviour

The worker retries failed writes three times using exponential backoff. The first retry waits
200ms, the second 400ms, the third 800ms, and 20% jitter is applied to each. Once three attempts
have failed the message is moved to the dead-letter queue.

## Configuration

The worker reads MaxConnections, RetryCount and RetryBaseDelayMs from environment variables.
In dev MaxConnections is 5, in staging it is 20, and in production it is 80.
