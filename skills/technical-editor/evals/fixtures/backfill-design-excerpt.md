# Design: Derivative backfill worker

Derivative sizes are generated up front, at ingest, from the single decode base generation already
holds — an image only flips Active once its whole size × format set exists in the serving bucket, so
serving is a pure read with no render path (the reasoning is in the image-pipeline plan's up-front
generation step, and lands in the pipeline's as-built docs when that arc closes).

That leaves one gap: adding a size or a format after images already exist. New uploads pick it up
from the next deploy, but every image already Active is missing it, and there is no serve-time miss
path to quietly fill it in. Something has to walk the existing library and generate the gap. This
design is that worker.

It is also what makes up-front generation defensible at all. The standing objection to generating
everything at ingest was that it couples "processed" to a fixed size list, so changing the list means
reprocessing the library. A first-class backfill worker dissolves it: adding a size becomes backfill,
then enable, and because the backfill finishes before the size is served, viewers never meet an
ungenerated one.

## Not needed to migrate today's data

At the time of writing no image has ever been served, so the handful of operator test images are
reprocessed by hand (delete and re-drive base generation). The worker is built for the future
size-addition case. Nothing is waiting on it.

The trigger to build it is the first size or format added to the list after real images exist — which
in practice means it lands ahead of, or with, that change. Building it earlier buys nothing; building
it later means the first size addition either reprocesses by hand or ships a size that only new
uploads have.

## Shape

Its own worker task, a sibling of the pipeline worker — same container/ECS-service shape, so it can
be scaled independently and run to completion rather than sitting in the ingest path. It reuses the
NetVips core and the ensure-routine; it holds no image logic of its own.

Reads base, writes serving. Same least-privilege split the processor tier already has, and notably no
read on archive — the user originals stay out of reach of a bulk worker.
