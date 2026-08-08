# imagepipe Architecture

imagepipe is the service that takes an image from an untrusted uploader and turns it into safe, CDN-served derivatives. It exists because we cannot let arbitrary user bytes reach a public origin, and we cannot make users wait while we prove those bytes are safe. This document describes how the pipeline is put together, what guarantees it makes, and where things go when they break.

The audience is a developer who knows AWS basics (S3, SQS, IAM) but has not worked on this pipeline before.

## Overview

The pipeline is a chain of buckets connected by queue-driven workers. An image moves forward one bucket at a time, and each move represents a fact we have established about the image. Nothing is copied ahead of the check that authorizes it.

```
client ──presigned PUT──▶ quarantine ──▶ scanning worker
                                              │
                              clean ──────────┴────────── flagged
                                │                            │
                              base                          hold
                                │                    (Object Lock)
                        derivative worker
                                │
                            serving ──▶ CDN
```

There are four buckets: **quarantine**, **base**, **hold**, and **serving**. Only **serving** is configured as a CDN origin. Every other bucket has S3 Block Public Access fully enabled and is reachable only through IAM roles held by the workers. This is the single most important invariant in the system: if you find yourself adding a public read path to quarantine, base, or hold, you have misunderstood the design.

## Upload

Clients never receive long-lived write credentials. They ask the API for a presigned S3 URL scoped to a single object key in the quarantine bucket, then `PUT` the bytes directly to S3. The API server never handles image bytes, which keeps it small and keeps large uploads off our request path.

The object landing in quarantine is untrusted. It may be malware, it may be illegal content, it may be a 4GB file with a `.jpg` extension. Treat anything in this bucket as hostile.

## Scanning

The upload emits an SQS message, which triggers the scanning worker. The worker performs two independent checks:

1. **ClamAV** — a conventional malware scan of the file contents.
2. **CSAM hash check** — the file's hash is checked against Arachnid Shield.

Both checks must pass for an image to be considered clean.

- **Clean images** move to the **base** bucket. Base holds the canonical original and is the input to everything downstream.
- **Flagged images** move to the **hold** bucket, which has S3 Object Lock enabled. Object Lock means the object cannot be deleted or overwritten for the duration of its retention period — not by the worker, not by an operator, not by a compromised credential. Flagged material must be preserved intact for legal and reporting obligations, so the storage layer enforces that rather than relying on process discipline.

Nothing flagged ever reaches base, and therefore nothing flagged ever reaches serving.

## Derivatives

A clean arrival in base triggers the derivative worker, which generates two thumbnails at **256px** and **1024px** and writes them to the **serving** bucket. Serving sits behind a CDN and is the only bucket the public can read from, and then only through the CDN.

The originals stay in base. If we add a new derivative size later, base is the source we re-run against.

## Retries and failure handling

Any step can fail for boring reasons: a throttled S3 call, a scanner timeout, a worker that dies mid-task. Failed work is retried **3 times with exponential backoff**, using a **200ms base delay** with **20% jitter**. Jitter matters more than it looks: without it, a batch of messages that fail together will retry together and reproduce the same overload that caused the failure.

After the third retry, the message goes to a **dead-letter queue**. Dead-lettering is not a silent discard — it is a signal that something needs human attention. The image stays in whatever bucket it was in, so a DLQ message plus the quarantine or base object is enough to reconstruct what happened and replay the work once the underlying cause is fixed.

Note that retries are bounded by the latency budget below. A step that retries three times is spending real wall-clock time against that budget, so a "successful" outcome after several retries can still be a user-visible failure.

## Latency budget

The full pipeline — upload complete through derivatives available on the CDN — must finish within **30 seconds at p99**. That is the number the product depends on and the number to hold in your head when changing anything here.

Practically, this constrains what you can add. A new synchronous check inside the scanning worker consumes budget for every image. A new derivative size adds work to the critical path. If a change cannot fit in the budget, it belongs off the critical path — triggered from base after the pipeline completes — rather than inside it.

## Working on imagepipe

Two rules cover most changes. First, do not widen public access: serving is the only origin, and the others block public access without exception. Second, do not let anything skip the scan; every path into base must come through a scanning worker that ran both checks.
