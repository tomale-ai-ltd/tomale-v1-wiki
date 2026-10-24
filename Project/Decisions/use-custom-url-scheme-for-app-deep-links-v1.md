---
type: decision
title: "use-custom-url-scheme-for-app-deep-links-v1"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: use-custom-url-scheme-for-app-deep-links-v1

## What we decided

Use a custom URL scheme (`tomalerntest://`) for general in-app deep links in V1, migrating to Universal Links (`https://tomale.ai/app/*`) pre-launch.

## Why

Not elaborated in session notes beyond the stated approach. This mirrors the same custom-scheme-now, universal-links-later pattern already adopted for Stripe checkout redirects (see related note), applied here to general app deep-linking such as `user_alerts.action_url`.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes. Universal Links migration work will still be required before public launch.

## Workflow detail

Applies to general in-app deep links, including the `action_url` field used by `user_alerts`. Universal Links setup is deferred to pre-launch preparation, alongside the equivalent Stripe checkout redirect migration.

## Related notes

- [[Sessions/2026-06-30-001]]
- [[Project/Decisions/use-action-url-for-user-alert-deep-linking]]
- [[Project/Decisions/use-custom-url-scheme-for-stripe-checkout-redirect-v1]]
