---
type: decision
title: parental-gate-on-profile-switch
project: tomale-rn-v1
status: accepted
date: 2026-06-22
features:
  - F-profiles
---

# Decision: parental-gate-on-profile-switch

## What we decided

Switching from a child profile into a parent profile must require a PIN, verified server-side inside the `select_profile` endpoint. The PIN is account-level (one PIN per account, not per-profile).

## Why

Without a gate, a child with physical access to the device could switch to a parent profile and bypass content restrictions. Server-side verification ensures the gate cannot be circumvented by a modified client. An account-level PIN is simpler to manage than per-profile PINs and sufficient for V1.

## Alternatives considered

Per-profile PINs were raised as a question but not adopted — an account-level PIN is the recommended approach for V1. Whether to force the profile selector and PIN on every app open (vs. resuming the last profile) was also raised; the recommendation is to force the selector on every open, but this is not yet resolved.

## Trade-offs accepted

A single account-level PIN means that any parent-level user on the account shares the same PIN. PIN length, lockout policy, and force-on-open vs. resume-last-profile behaviour are open items to be resolved before implementation.

## Workflow detail

Not yet built as of 2026-06-22 — this is a committed design decision pending implementation. The gate will live server-side in `select_profile`. Open implementation questions (PIN length, lockout, force-on-open) are tracked as blockers in [[sessions/2026-06-22-001]].


**Amendment (2026-10-29, B9 review with Kyle):** the PIN is 4 digits, set during onboarding after email verification. Five wrong attempts lock it; unlocking needs a password reset, which also sets a new PIN. Parent-only areas are also refused by the backend for child profiles. See [[PRD-Profiles]].

## Related notes

- [[sessions/2026-06-22-001]]
- [[per-child-story-visibility]]
- [[security-model]]
