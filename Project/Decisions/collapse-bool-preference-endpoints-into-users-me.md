---
type: decision
title: collapse-bool-preference-endpoints-into-users-me
date: 2026-05-21
status: current
project: tomale-rn-v1
---

---

# Decision: Collapse bool_* preference endpoints into PATCH /users/me

## What we decided

The standalone `bool_*` preference endpoints on the `users` group are removed.
User-settable preferences are now updated through a single `preferences` object
on `PATCH /users/me` (`push_alerts`, `push_marketing`, `email_opt_in`).
Specifically:

- `POST /users/{users_id}/bool_email_verified` — deleted; email verification is
  handled by `/auth/verify_email`.
- `bool_subscription` — deleted; subscription state is set internally by
  webhooks and is never user-settable.
- `bool_onboarding` — promoted to its own event-style endpoint,
  `POST /users/me/complete_onboarding` (idempotent, no body required).

## Why

- Email verification and subscription state are not user-editable fields.
  Exposing them as writable preference endpoints invited misuse — `email_verified`
  belongs to the verification flow, and `subscription_active` / `plan_level` are
  set by the Stripe / HPBC webhooks only.
- Genuine user preferences are a natural part of the profile-update surface, so
  they belong on `PATCH /users/me` under a `preferences` object rather than as
  separate single-field endpoints.
- Onboarding completion is an event, not a toggle. Modelling it as
  `POST /users/me/complete_onboarding` captures intent better than a writable
  boolean and lets the handler stay idempotent.

## Alternatives considered

Keeping the per-field `bool_*` endpoints as defined in `api-spec` — rejected:
they exposed non-user-settable fields as writable and multiplied endpoint
surface for what is fundamentally a single profile update.

## Trade-offs accepted

This deviates from `api-spec` as currently written and must be reconciled
(carryover item #5). The deviation is tracked alongside the other `users`-group
changes from this session.

## Workflow detail

`PATCH /users/me` now carries a `preferences` object; `opt_in_status_last_updated`
is bumped only when a consent field actually changes. `api-spec` and `data-model`
need updating to match. This is one of the pending decision notes counted under
carryover item #6.

## Related notes

- [[Sessions/2026-05-21-001|2026-05-21-001]]
- [[Project/Cursor/api-spec|api-spec]]
- [[Project/Plan/5-cto-implementation-plan|5-cto-implementation-plan]]
- [[Project/Plan/6-api-security-model|6-api-security-model]]
- [[Project/Decisions/make-username-user-editable|make-username-user-editable]]
- [[Project/Decisions/defer-explicit-profile-avatar-endpoint-until-kid-profiles|defer-explicit-profile-avatar-endpoint-until-kid-profiles]]
- [[Project/Decisions/enforce-server-side-image-validation|enforce-server-side-image-validation]]
- [[Project/Decisions/separate-verify-email-deeplink-from-magic-link-path|separate-verify-email-deeplink-from-magic-link-path]]
