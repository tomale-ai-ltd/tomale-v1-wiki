---
type: decision
title: fail-closed-active-profile-resolution
project: tomale-rn-v1
status: accepted
date: 2026-06-22
---

---

# Decision: fail-closed-active-profile-resolution

## What we decided

When `active_profile` cannot be resolved from `$auth.extras`, the endpoint fails closed and returns a re-login error. There is no fallback that silently elevates a missing-extras token to the default profile or parent visibility.

## Why

Silent privilege escalation is explicitly prohibited by [[6-api-security-model]]. A token missing extras is in an indeterminate state; treating it as a lesser-privileged default still grants access it may not be entitled to. Failing closed forces re-authentication, which restores a known-good token state.

## Alternatives considered

Xano proposed a fail-open fallback — resolving a missing-extras token to the account's default or parent profile. This was rejected because it would silently elevate an incomplete token to parent-level visibility, violating the no-silent-privilege-escalation principle.

## Trade-offs accepted

A user with a malformed or expired token gets a re-login error rather than degraded-but-functional access. This adds friction in edge cases (e.g., token issued before extras were added to the auth model) but is the correct security posture.

## Workflow detail

Implemented in Xano using `|get` to safely read `active_profile` from extras without throwing on a missing key, followed by a null precondition that returns the re-login error if the value is absent. Tested with a real Postman token to confirm the precondition fires correctly on a missing-extras token.

## Related notes

- [[6-api-security-model]]
- [[per-child-story-visibility]]
