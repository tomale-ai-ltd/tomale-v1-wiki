---
type: decision
title: "remove-user-activities-endpoint"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: remove-user-activities-endpoint

## What we decided

Mark `user_activities` for removal from the V1 API surface, identified during the alphabetical Phase 1 API security-model classification audit.

## Why

`user_activities` is analytics-only and deferrable — it doesn't serve a user-facing V1 function.

## Alternatives considered

Retaining the endpoint was the implicit alternative — rejected as unnecessary for V1 given its analytics-only purpose.

## Trade-offs accepted

Not discussed in session notes. Analytics capability that endpoint provided is deferred, not replaced.

## Workflow detail

Marked for removal in the Phase 1 classification matrix; actual deletion is part of the ongoing API surface reduction work tracked in [[Project/Plan/6-api-security-model]].

## Related notes

- [[Sessions/2026-06-30-001]]
- [[Project/Decisions/remove-instant-story-reviews-endpoint]]
- [[Project/Decisions/replace-support-requests-endpoint-with-mailto-ops-inbox]]
- [[Project/Plan/6-api-security-model]]
