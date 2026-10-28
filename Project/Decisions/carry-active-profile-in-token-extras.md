---
type: decision
title: carry-active-profile-in-token-extras
project: tomale-rn-v1
status: proposed
date: 2026-05-08
related:
  - "[[2026-05-08-001]]"
  - "[[v1-audit]]"
affects:
  - auth/select_profile
  - user_sessions
features:
  - F-profiles
  - F-auth
---

# Decision: carry-active-profile-in-token-extras

## What we decided

Profile context travels in the auth token's extras (`active_profile` with `id`, `name`, `is_child`), so profile-aware endpoints need no lookup per request. `auth/select_profile` issues a new token and updates the existing `user_sessions` row rather than inserting one.

## Why

Cheap, consistent profile checks on every endpoint.

## Related notes

- [[2026-05-08-001]] (backfilled in B7)
- [[fail-closed-active-profile-resolution]]
- [[parental-gate-on-profile-switch]]
