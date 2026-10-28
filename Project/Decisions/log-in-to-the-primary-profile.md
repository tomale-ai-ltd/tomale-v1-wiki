---
type: decision
title: log-in-to-the-primary-profile
project: tomale-rn-v1
status: proposed
date: 2026-05-11
related:
  - "[[2026-05-11-001]]"
  - "[[v1-audit]]"
affects:
  - auth/login
features:
  - F-profiles
  - F-auth
---

# Decision: log-in-to-the-primary-profile

## What we decided

Login always starts on the account's primary (adult) profile. A parent who usually uses a child profile switches after logging in. A "last used profile" behaviour (`users.last_active_profile_id`) is post-V1.

## Why

The safer default, and simpler logic.

## Related notes

- [[2026-05-11-001]] (backfilled in B7)
- [[parental-gate-on-profile-switch]]
