---
type: decision
title: "generate-story-images-through-a-cloud-run-gateway-with-xano-callbacks"
project: tomale-rn-v1
status: proposed
date: "2026-11-24"
supersedes: []
related:
  - "[[2026-11-24-002]]"
  - "[[PRD-Image-Pipeline]]"
  - "[[defer-image-pipeline-throughput-to-phase-2]]"
affects:
  - "[[image-generation-flow]]"
  - "[[backend-xano]]"
  - "[[security-model]]"
  - "[[roadmap]]"
  - "image_jobs (status dispatched)"
  - "ai pipeline/executor_page_image, executor_cover_image, executor_character_image, image_worker_tick, orchestrator_story_images"
features:
  - F-story-generation
  - X-platform
---

# Decision: generate-story-images-through-a-cloud-run-gateway-with-xano-callbacks

## What we decided

- Xano keeps the orchestrator → tick → executor pipeline. Executors for a gateway record **dispatch** the job (`POST /v1/batches`, HMAC-signed) to a Cloud Run gateway and set `image_jobs.status = dispatched`.
- The gateway queues each job on Cloud Tasks; Cloud Run workers do compile → generate → moderate → store.
- Workers report back to an idempotent, HMAC-checked webhook in the Xano `webhooks` group.
- The orchestrator dispatches a whole book straight away. The tick stays as reaper, kill switch and safety net, and leases work as today.

## Why

Throughput is limited by Xano (5-minute tick, serial async pool), not the model. Moving the slow call off Xano, with a callback, is the parallel-worker hand-off already planned in [[roadmap]] §6 and already used for HPBC. It keeps `image_jobs` as the interface. Cloud Tasks gives per-queue rate and concurrency caps for Vertex's dynamic quota.

## Alternatives considered

- Xano calling Vertex directly: keeps the serial bottleneck.
- Pub/Sub push: no per-queue rate cap.
- SQS + Lambda: generation calls would cross clouds.

## Trade-offs accepted

- A new service to run, in a separate repo.
- A new `dispatched` status.
- Two clouds in the critical path.

## Workflow detail

- Xano changes are batched into Session A ([[IP-10-xano-session-a]]); the cut-over is Session B.
- When accepted, this supersedes [[defer-image-pipeline-throughput-to-phase-2]]: set `superseded_by` there.

## Related notes

- [[PRD-Image-Pipeline]]
- [[image-pipeline-future-state]]
- [[image-pipeline-research-2026-11]]
