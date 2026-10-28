---
type: decision
title: ratify-users-id-as-ownership-field-standard
project: tomale-rn-v1
status: accepted
date: 2026-07-16
features:
  - X-security
---

# Decision: Ratify `users_id` as the ownership field standard

## What we decided

`users_id` is ratified as the ownership field standard used across the schema, superseding `owner_user_id`. This resolves (rather than defers) Phase 5 item 28.

## Why

Reviewing all nine Phase 1 items against actual state during this session's cross-cutting sweep, item 8 (ownership model) was checked against [[5-cto-implementation-plan]] §3.2/3.6 and Phase 5 item 28, which specify `owner_user_id` as the standardized ownership/naming convention. The session confirmed `users_id` is what's actually in use in practice and judged it functionally equivalent given consistent scoping, so the field was ratified as-is rather than renamed.

## Alternatives considered

Renaming the field to `owner_user_id` to match the convention specified in the written CTO implementation plan — not pursued, since `users_id` was found functionally equivalent given consistent scoping already in place.

## Trade-offs accepted

This is a deviation from the written CTO implementation plan ([[5-cto-implementation-plan]] §3.2/3.6, Phase 5 item 28), which will remain technically inaccurate on this point unless updated. Accepted because renaming offered no functional benefit over the existing, consistently-scoped field.

## Workflow detail

Not discussed in session notes beyond resolving Phase 5 item 28 and closing out Phase 1 item 8 (ownership model). No migration or renaming work follows from this decision.

## Related notes

- [[Sessions/2026-07-16-001|2026-07-16-001]]
- [[5-cto-implementation-plan|5-cto-implementation-plan]]
