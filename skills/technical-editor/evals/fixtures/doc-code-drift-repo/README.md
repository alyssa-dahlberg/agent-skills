# catalogue-service

Serves the product catalogue.

## Caching

Responses are cached with a 10,000-entry bound and least-recently-used eviction once that bound is
reached. See [docs/caching.md](docs/caching.md).
