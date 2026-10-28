---
type: decision
title: adopt-unified-user-profiles-table
project: tomale-rn-v1
status: proposed
date: 2026-05-11
related:
  - "[[2026-05-11-001]]"
  - "[[v1-audit]]"
affects:
  - user_profiles
  - data-model
features:
  - F-profiles
---

# Decision: adopt-unified-user-profiles-table

## What we decided

One `user_profiles` table holds both adult and child profiles, with an `is_child` flag (Model B), replacing `user_child_profiles`. Every profile-scoped record points at `user_profiles`.

## Why

A cleaner model: a single foreign-key target, and room for per-profile data later (age, preferences, reading level).

## Alternatives considered

Keep `user_child_profiles`, with "adult" implied by null: rejected.

## Related notes

- [[2026-05-11-001]] (backfilled in B7)
- [[rename-user-profiles-is-default-to-is-primary]]
