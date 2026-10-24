---
type: decision
title: use-action-url-for-user-alert-deep-linking
project: tomale-rn-v1
status: accepted
date: 2026-06-30
---

---

# Decision: use-action-url-for-user-alert-deep-linking

## What we decided

`user_alerts` deep-linking uses a nullable `action_url` text column rather than a typed `entity_type` / `entity_id` foreign-key pair.

## Why

`action_url` is simpler, versionable, and gives universal handling on the frontend — one field the client can route on, rather than a typed reference that requires entity-specific resolution logic for every alert type.

## Alternatives considered

A typed `entity_type` / `entity_id` FK pair was considered and rejected in favor of the plain URL approach.

## Trade-offs accepted

Not discussed in session notes beyond the stated rationale — no referential integrity at the database level for the linked entity, since `action_url` is an opaque string rather than an FK.

## Workflow detail

The `action_url` column still needs to be added to `user_alerts` (queued as the immediate next task). It will use the app's deep-link URL format established the same session (see related note).

## Related notes

- [[Sessions/2026-06-30-001]]
- [[scope-user-alerts-as-in-app-inbox]]
- [[use-custom-url-scheme-for-app-deep-links-v1]]
