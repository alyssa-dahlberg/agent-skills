# Rate limiting

Search queries are rate limited per tenant. The limit will be 60 queries per minute for standard
tenants and 600 for enterprise, enforced at the edge using a token bucket with a burst allowance of
twice the sustained rate.

Exceeding the limit returns 429 with a `Retry-After` header. Clients are expected to back off rather
than retry immediately.

We will keep counters in Redis with a one-minute sliding window, keyed by tenant. The edge worker
reads and increments in a single round trip using a Lua script, so the check adds roughly 1ms.

Limits are configured per tenant tier and can be raised for a specific tenant by support.
