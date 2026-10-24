---
type: decision
title: separate-verify-email-deeplink-from-magic-link-path
date: 2026-05-21
status: current
project: tomale-rn-v1
---

---

# Decision: Separate the verify-email deeplink from the magic-link completion path

## What we decided

After email verification on the Squarespace `/verify-email` page, the app is
re-entered through a dedicated deeplink,
`tomalerntest://auth/verified?status=success|error&reason=...`. This is kept
separate from the magic link's `/auth/complete` deeplink path.

## Why

By the time the post-verification deeplink fires, the verification token has
already been consumed — the `/verify-email` page has called
`/auth/verify_email`. Reusing the magic link's `/auth/complete` path, which
expects a live token to complete sign-in, would be incorrect. A distinct
`auth/verified` route that simply carries a `status` / `reason` result keeps the
two flows cleanly separated and self-documenting.

## Alternatives considered

Routing the post-verification return through the existing magic-link
`/auth/complete` deeplink — rejected: that path expects an unconsumed token, and
the verification token is already spent by the time the user returns to the app.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The Squarespace `/verify-email` page now calls
`https://api.tomale.ai/api:1pgd39RE/auth/verify_email` and, on completion,
redirects into the app via `tomalerntest://auth/verified?status=...&reason=...`.
The app needs a route handler for `auth/verified` that is distinct from its
`/auth/complete` handler. Related to this work, the page's reason matching was
fixed to `data.reason?.includes('expired')`, since Xano returns the string
`"expired token"` rather than `"expired"`.

## Related notes

- [[Sessions/2026-05-21-001|2026-05-21-001]]
- [[6-api-security-model|6-api-security-model]]
- [[use-https-web-intermediary-for-magic-link-redirect|use-https-web-intermediary-for-magic-link-redirect]]
- [[collapse-bool-preference-endpoints-into-users-me|collapse-bool-preference-endpoints-into-users-me]]
- [[defer-explicit-profile-avatar-endpoint-until-kid-profiles|defer-explicit-profile-avatar-endpoint-until-kid-profiles]]
- [[make-username-user-editable|make-username-user-editable]]
- [[enforce-server-side-image-validation|enforce-server-side-image-validation]]
