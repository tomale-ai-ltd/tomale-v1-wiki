---
type: decision
title: remove-instant-story-reviews-endpoint
project: tomale-rn-v1
status: accepted
date: 2026-06-30
features:
  - F-bookshelf
---

# Decision: remove-instant-story-reviews-endpoint

## What we decided

Mark `instant_story_reviews` for removal from the V1 API surface, identified during the alphabetical Phase 1 API security-model classification audit.

## Why

There is no sharing or audience feature in V1, so review functionality tied to that use case has no user-facing purpose in this release.

## Alternatives considered

Retaining the endpoint was the implicit alternative — rejected since nothing in V1 consumes it.

## Trade-offs accepted

Not discussed in session notes. If sharing/audience features are added post-V1, the endpoint (or an equivalent) would need to be rebuilt.

## Workflow detail

Marked for removal in the Phase 1 classification matrix; actual deletion is part of the ongoing API surface reduction work tracked in [[security-model]].

## Related notes

- [[Sessions/2026-06-30-001]]
- [[remove-user-activities-endpoint]]
- [[replace-support-requests-endpoint-with-mailto-ops-inbox]]
- [[security-model]]
