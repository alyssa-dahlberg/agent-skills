namespace OrderFlow.Worker;

/// <summary>
/// Retry policy for failed writes. Retries three times with exponential backoff starting at
/// 200ms and doubling each attempt, applying 20% jitter. After three failures the message is
/// dead-lettered. Implemented by SqlRetryPolicy and used by OrderWriter.
/// </summary>
public interface IRetryPolicy
{
    // Returns true if the operation should be retried
    bool Check(int attempt);

    // delayMs is in milliseconds
    void Wait(int delayMs);
}
