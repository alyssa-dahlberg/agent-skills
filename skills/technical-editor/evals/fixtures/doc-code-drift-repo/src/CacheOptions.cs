namespace Catalogue.Caching;

public sealed class CacheOptions
{
    /// <summary>
    /// How long an entry lives after it is written. This is an absolute lifetime, not a
    /// sliding window — reading an entry does not extend it.
    /// </summary>
    public TimeSpan Ttl { get; init; } = TimeSpan.FromSeconds(600);

    /// <summary>Maximum number of entries before least-recently-used eviction begins.</summary>
    public int Capacity { get; init; } = 10_000;

    /// <summary>Regions the cache replicates to.</summary>
    public string[] Regions { get; init; } = ["ap-southeast-2", "us-east-1", "eu-west-1", "us-west-2"];

    /// <summary>Number of retry attempts for a failed cache write.</summary>
    public int WriteRetries { get; init; } = 2;
}
