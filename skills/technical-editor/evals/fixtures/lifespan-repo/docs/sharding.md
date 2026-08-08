# Sharding

Search is sharded by tenant. Each tenant's documents live in a single shard, so a query never fans
out across shards and ranking stays comparable within a result set.

Shard assignment is by consistent hash of the tenant ID, with 64 virtual nodes per physical shard.
Rebalancing moves virtual nodes rather than tenants, so a rebalance touches a bounded fraction of
the data.

Cross-tenant search is not supported. Admin search runs a separate scatter-gather path that queries
every shard and merges results without ranking, which is acceptable because admin result sets are
small and ordering is by date.
