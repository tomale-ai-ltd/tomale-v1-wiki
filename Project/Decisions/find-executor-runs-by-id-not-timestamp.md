---
type: decision
title: find-executor-runs-by-id-not-timestamp
project: tomale-rn-v1
status: accepted
date: 2026-10-15
---

---

# Decision: find-executor-runs-by-id-not-timestamp

## What we decided

Executor runs are looked up by `id`, not by timestamp, in both image pipelines.

## Why

Lookup by timestamp is fragile: the run row is created after the function starts.

## Alternatives considered

Timestamp-based lookup, the existing approach, was judged fragile.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Listed as a next-session item (executor run lookup by id in both pipelines); the blockers section later records it as fixed.

## Related notes

- [[2026-10-15-001]]
- [[avoid-column-named-function-inputs-in-xano]]
- [[defer-image-pipeline-throughput-to-phase-2]]
