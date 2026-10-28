---
type: decision
title: moderate-names-in-two-stages
project: tomale-rn-v1
status: proposed
date: 2026-06-29
related:
  - "[[2026-06-29-001]]"
  - "[[v1-audit]]"
affects:
  - admin/check_for_profanity
  - blocked_terms
features:
  - F-profiles
  - F-characters
---

# Decision: moderate-names-in-two-stages

## What we decided

Names (profiles and characters, on create) go through two stages. A word-list check against `blocked_terms` is a signal only, with no early exit. AI moderation is the final arbiter: lenient on real names that contain blocked substrings (e.g. Hancock), and accepting of whimsical names and digit suffixes.

## Why

A word list alone rejects legitimate names.

## Related notes

- [[2026-06-29-001]] (backfilled in B7)
- [[scope-characters-per-profile-with-soft-delete]]
