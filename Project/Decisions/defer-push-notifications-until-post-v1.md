---
type: decision
title: defer-push-notifications-until-post-v1
project: tomale-rn-v1
status: accepted
date: 2026-06-30
features:
  - F-notifications
---

# Decision: defer-push-notifications-until-post-v1

## What we decided

Push notification infrastructure — including a new `user_push_tokens` table — is deferred out of V1 and treated as a post-V1 fast-follow, estimated at roughly 2-3 days of work.

## Why

The in-app `user_alerts` inbox reaches 100% of active users and covers the V1 notification need on its own; push only reaches opted-in users (~51% on iOS), so it adds coverage rather than being required for V1 to function.

## Alternatives considered

Building push notifications alongside `user_alerts` in Phase 1 was the implicit alternative — deferred since the in-app inbox alone is sufficient for V1 launch.

## Trade-offs accepted

V1 users who aren't actively opening the app won't be proactively notified of new alerts until push ships post-V1.

## Workflow detail

`user_alerts` (in-app inbox) ships in Phase 1. Push notification infrastructure, including the `user_push_tokens` table, is scoped as a fast-follow after V1.

## Related notes

- [[Sessions/2026-06-30-001]]
- [[scope-user-alerts-as-in-app-inbox]]
