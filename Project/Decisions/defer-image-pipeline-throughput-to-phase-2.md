---
type: decision
title: defer-image-pipeline-throughput-to-phase-2
project: tomale-rn-v1
status: accepted
date: 2026-08-04
features:
  - F-story-generation
---

# Decision: defer-image-pipeline-throughput-to-phase-2

## What we decided

Image generation throughput (currently 10 to 15 minutes per story) will not be optimized within Xano in Phase 1. It is deferred to Phase 2, to be solved by moving to a parallel off-Xano pipeline as part of the Bedrock migration. Phase 1 scope is limited to correctness: eliminating duplicate executor runs and ensuring every job reaches a terminal state.

## Why

Correctness (duplicate paid image generations, jobs stuck in `processing`) was a launch-blocking bug and has been fixed. Throughput is a performance concern, not a correctness one, and does not block Phase 1 close-out.

## Alternatives considered

Patching throughput now within Xano's async-shared pool.

## Trade-offs accepted

Stories will continue to take 10 to 15 minutes to generate all images through Phase 1 launch. Acceptable since it does not block correctness or the Phase 1 flow test run.

## Workflow detail

No changes to the current Xano async executor pattern during Phase 1. Parallelization work is scoped to the future Bedrock migration in Phase 2.

## Related notes

- [[Sessions/2026-08-03-001]]
- [[image-generation-flow]]
