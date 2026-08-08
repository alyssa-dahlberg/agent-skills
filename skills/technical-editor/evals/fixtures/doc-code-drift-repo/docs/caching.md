# Caching

The response cache sits in front of the catalogue endpoints. It's not just a cache — it's a
resilience layer that fundamentally changes how the service behaves under load.

## The one thing you must know about eviction

Entries are evicted least-recently-used once the cache reaches capacity. It's worth noting that we
utilise a bounded store here, so the eviction path is exercised constantly rather than only under
memory pressure — this is deliberate, and it means the seamless degradation we want under load is
tested by ordinary traffic rather than by an incident.

Cache entries expire after 5 minutes of inactivity.

## Capacity

The cache holds 10,000 entries. On overflow the oldest entry is dropped.

## Environments

Development runs a smaller cache with a longer TTL, since the data barely changes locally. Production
uses the standard 10-minute TTL with retries enabled.

| Environment | TTL | Capacity |
|-------------|-----|----------|
| Development | 1 hour | 500 |
| Production | 10 minutes | 10,000 |

## Regions

The cache is replicated across three regions. See [replication.md](replication.md) for the topology.

## Failure handling

If the cache is unavailable the service falls back to the database. Failed writes to the cache are
retried a few times before being abandoned; a cache write failure never fails the request.

The fallback path is robust.
