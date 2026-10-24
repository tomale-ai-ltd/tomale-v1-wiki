---
type: decision
title: "scope-user-alerts-as-in-app-inbox"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: scope-user-alerts-as-in-app-inbox

## What we decided

`user_alerts` is scoped as an in-app inbox, distinct from push notifications. Its public surface is READ + mark-read only; creation is internal-only via a `create_user_alert()` function, and deletion is server-side maintenance rather than a user-facing action.

## Why

In-app inbox and push notifications are complementary rather than either/or: the inbox reaches 100% of active users, while push only reaches opted-in users (~51% on iOS). Keeping alert creation internal-only prevents users from writing arbitrary alerts into their own or others' inboxes.

## Alternatives considered

Not discussed in session notes as an explicit rejected alternative, beyond the general framing that push notifications were considered and deferred separately (see [[defer-push-notifications-until-post-v1]]).

## Trade-offs accepted

Alerts are read-only from the client's perspective — all creation logic must be routed through internal callsites (e.g. the content moderation pipeline), which adds a coordination step whenever a new alert-generating event is introduced.

## Workflow detail

`GET /user_alerts` (scoped list, sorted `created_at` desc, returns full history regardless of read status) shipped this session. Remaining endpoints (GET single, PATCH single mark-read, PATCH mark-all-read) and the `create_user_alert()` internal function are next up, with the content moderation pipeline as the first alert-generating callsite.

## Related notes

- [[Sessions/2026-06-30-001]]
- [[use-action-url-for-user-alert-deep-linking]]
- [[defer-push-notifications-until-post-v1]]
