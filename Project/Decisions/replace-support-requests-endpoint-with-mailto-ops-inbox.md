---
type: decision
title: "replace-support-requests-endpoint-with-mailto-ops-inbox"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: replace-support-requests-endpoint-with-mailto-ops-inbox

## What we decided

Remove the `support_requests` endpoint from V1 and replace it with a `mailto:` link plus an ops inbox process — no backend endpoint needed.

## Why

A `mailto:` link routed to an ops inbox covers the V1 support-request need without the overhead of building and securing a dedicated backend endpoint.

## Alternatives considered

Keeping the `support_requests` backend endpoint was the implicit alternative — rejected as unnecessary complexity for a need that a simple `mailto:` + ops process already covers.

## Trade-offs accepted

Support requests submitted this way aren't stored or queryable in the app's own data — they live in whatever inbox/ops tooling receives the `mailto:` email. Not discussed further in session notes.

## Workflow detail

Marked for removal in the Phase 1 classification matrix; actual deletion is part of the ongoing API surface reduction work tracked in [[6-api-security-model]]. Frontend support entry point becomes a `mailto:` link rather than a form submission.

## Related notes

- [[Sessions/2026-06-30-001]]
- [[remove-instant-story-reviews-endpoint]]
- [[remove-user-activities-endpoint]]
- [[6-api-security-model]]
