---
type: decision
title: defer-explicit-profile-avatar-endpoint-until-kid-profiles
project: tomale-rn-v1
status: accepted
date: 2026-05-21
---

---

# Decision: Defer the explicit profile-avatar endpoint until kid-profile support lands

## What we decided

Only `PATCH /users/me/image` is built for V1. A dedicated
`PATCH /user_profiles/{id}/avatar` endpoint is deferred until kid-profile
support is implemented. When both endpoints eventually exist, they will share a
single internal upload function rather than duplicating upload logic.

## Why

- Kid profiles are not in V1 scope, so a per-profile avatar endpoint has no
  caller yet.
- `PATCH /users/me/image` already resolves the active profile via
  `$auth.extras.active_profile_id`, which covers the only profile a V1 user can
  edit.
- The convenience-wrapper pattern (`/users/me/image` delegating to
  `/user_profiles/{id}/avatar`) only stays DRY if both endpoints call a shared
  internal function. Building the wrapper now, before that function exists,
  would invite divergence when the rebuild happens.

## Alternatives considered

- Build `PATCH /user_profiles/{id}/avatar` now alongside `/users/me/image` —
  rejected: no V1 caller, and duplicated upload logic would have to be
  reconciled later anyway.
- A single generic upload endpoint with a `context` parameter — rejected as an
  anti-pattern: it collapses authorization into a switch statement, breaks
  endpoint self-documentation, and couples unrelated change cycles. Pattern B
  (resource-specific endpoints, each owning its own authorization, sharing
  internal upload mechanics) was confirmed instead.

## Trade-offs accepted

V1 ships without a way to set a non-active profile's avatar — acceptable because
kid profiles do not exist in V1. The rebuild stays DRY only if the shared
internal upload function is created when the second endpoint is added; this is a
known follow-up rather than something resolved now.

## Workflow detail

When kid-profile support is built, add `PATCH /user_profiles/{id}/avatar` and
refactor both it and `PATCH /users/me/image` onto a shared internal upload
function. The `PATCH /users/me/image` contract is stable in the meantime, so the
deferral does not block other `users`-group work.

## Related notes

- [[Sessions/2026-05-21-001|2026-05-21-001]]
- [[5-cto-implementation-plan|5-cto-implementation-plan]]
- [[6-api-security-model|6-api-security-model]]
- [[migrate-image-storage-to-aws-s3-signed-urls|migrate-image-storage-to-aws-s3-signed-urls]]
- [[enforce-server-side-image-validation|enforce-server-side-image-validation]]
- [[collapse-bool-preference-endpoints-into-users-me|collapse-bool-preference-endpoints-into-users-me]]
- [[make-username-user-editable|make-username-user-editable]]
- [[separate-verify-email-deeplink-from-magic-link-path|separate-verify-email-deeplink-from-magic-link-path]]
