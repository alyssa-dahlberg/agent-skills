# orderflow

Order processing service.

## Retries

Failed writes are retried three times with exponential backoff, starting at 200ms and doubling
each attempt, with 20% jitter. After the third failure the message goes to the dead-letter queue.

See docs/architecture.md for the architecture.
