---
type: decision
title: use-https-web-intermediary-for-magic-link-redirect
project: tomale-rn-v1
status: accepted
date: 2026-05-15
features:
  - F-auth
---

# Decision: use-https-web-intermediary-for-magic-link-redirect

## What we decided

Magic-link emails carry a standard `https://` link pointing at the Squarespace site, which then prompts the user to open the Tomale app. The email link itself carries only a single-use magic-link token — never a bearer. `POST /auth/complete_magic_link` exchanges the magic-link token for a fresh bearer + refresh, creates a `user_sessions` row, and marks the link used.

A custom URL scheme (`tomale://`) is NOT used for magic links. Universal Links / App Links are deferred to pre-launch polish.

## Why

A standard `https://` link works everywhere email clients and browsers can reach — no deep-link support required on the receiving side — and the intermediary page can render a clean "Continue to open app?" prompt. Universal Links / App Links would remove the extra browser tap but require DNS, hosted association files, and domain verification, which is operational work better batched with other launch-prep tasks. Issuing the bearer through a dedicated endpoint rather than embedding it in the URL aligns with the bearer-handling rules in `6-api-security-model`.

## Alternatives considered

- **Custom `tomale://` scheme directly in the email link.** Rejected — non-https schemes are stripped or warned on by many email clients, making the tapped-link UX unreliable.
- **Universal Links / App Links from day one.** Deferred — necessary eventually but adds DNS + hosting + domain-verification work not on the Phase 1 critical path. Queued for pre-launch polish to remove the extra browser tap.
- **Embed the bearer token directly in the magic link URL.** Rejected — violates the API security model's bearer-handling rules; bearers must not appear in URLs.

## Trade-offs accepted

- Users hit an extra "Continue to open app?" tap in the browser before landing in the app. Acceptable for V1; Universal Links / App Links work is queued to remove it pre-launch.
- The Squarespace intermediary becomes part of the auth surface — the `YOUR_AUTH_GROUP_ID` placeholder still needs replacing and production CORS for `tomale.ai` still needs confirming before launch.

## Workflow detail

`POST /auth/complete_magic_link` accepts the magic-link token, JWE-decodes via `$env.magic_jwt_secret`, validates (user exists, token matches, `used == false`, `expiration >= now`), issues fresh refresh + auth tokens preserving the `active_profile` extras pattern, creates a new `user_sessions` row, and sets `users.magic_link.used = true` to enforce single-use. A bug caught during review — the `db.edit users` step was writing to `magic_link_login` instead of `magic_link`, which would have broken single-use enforcement — has been corrected and verified.

End-to-end on a phone dev build via `npx expo start`: send → email → tap link → Chrome iOS prompt → app opens callback → token exchange → authenticated. Reused link correctly fails. EAS dev-build install (not just Metro) is the remaining validation; expired, used, malformed, and offline-at-callback cases are still pending on the installed build.

## Related notes

- [[use-custom-url-scheme-for-stripe-checkout-redirect-v1]]
- [[consolidate-xano-api-groups-into-app-and-webhooks]]
- [[enforce-strict-env-validation-at-startup]]
