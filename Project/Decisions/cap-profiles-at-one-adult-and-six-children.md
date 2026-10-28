---
type: decision
title: cap-profiles-at-one-adult-and-six-children
project: tomale-rn-v1
status: accepted
date: 2026-06-29
related:
  - "[[2026-06-29-001]]"
  - "[[v1-audit]]"
affects:
  - user_profiles POST
features:
  - F-profiles
---

# Decision: cap-profiles-at-one-adult-and-six-children

## What we decided

Each account has one adult (primary) profile and up to six child profiles, free within any plan. `is_child` is set by the server and can't be changed. The primary adult profile can't be deleted or demoted in V1.

## Why

Profiles aren't a commercial lever. The levers are generation volume, premium artwork styles and print credits.

## Related notes

- [[2026-06-29-001]] (backfilled in B7)
- [[prevent-deleting-active-profile-via-soft-delete]]
