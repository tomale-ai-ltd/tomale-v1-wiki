---
type: decision
title: "tag-crash-reports-with-active-profile-id-only"
project: tomale-rn-v1
status: accepted
date: "2026-11-04"
related:
  - "[[2026-11-04-001]]"
  - "[[2026-11-03-002]]"
affects:
  - "[[observability]]"
  - "specs/007-foundations-session/spec.md"
features:
  - F-auth
  - X-security
---

# Decision: tag-crash-reports-with-active-profile-id-only

## What we decided

The profile id attached to crash reports is `auth.active_profile.id` from `GET /auth/me`: the ID only, never the profile name or `is_child`. If the field is absent, the report includes the account id and omits the profile id. Profile switching stays out of scope for speckit 007.

## Why

Not discussed in session notes beyond keeping profile details other than the id out of crash reports.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

The checked-in `/auth/me` type doesn't describe `active_profile`, so the 007 plan reads it through a type guard rather than hand-editing the generated contract.

## Workflow detail

Answered by Kyle in `/speckit.clarify` for speckit 007. PR D must verify Sentry end to end: a temporary dev-only test error arrives with `user.id` and `profile_id` ([[m1-cursor-briefs]]).

## Related notes

- [[2026-11-04-001]]
- [[2026-11-03-002]]
- [[observability]]
- [[m1-cursor-briefs]]
