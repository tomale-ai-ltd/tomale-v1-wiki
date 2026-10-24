---
type: decision
title: use-custom-url-scheme-for-stripe-checkout-redirect-v1
date: 2026-05-07
status: current
project: tomale-rn-v1
---

---

# Decision: use-custom-url-scheme-for-stripe-checkout-redirect-v1

## What we decided

To use a custom URL scheme (`tomale://`) for Stripe Checkout `success_url` and `cancel_url` redirects in V1, deferring universal links / App Links setup to pre-launch preparation.

URL formats:

- `success_url: tomale://checkout/success?session_id={CHECKOUT_SESSION_ID}`
- `cancel_url:  tomale://checkout/cancel?session_id={CHECKOUT_SESSION_ID}`

These will be set in the `stripe/create_checkout_session` endpoint's Stripe API call.

## Why

- Custom URL schemes work on both iOS and Android with minimal configuration (single `scheme` entry in `app.json`)
- Universal links require hosting `apple-app-site-association` (iOS) and `assetlinks.json` (Android) on the production domain — operational work better suited to launch prep
- V1 testing and internal dogfooding does not require the cross-app robustness universal links provide
- Payment confirmation does not depend on the redirect — it comes from the Stripe webhook server-side. The redirect only tells the app to navigate to the confirmation screen and call `check_order_paid`

## Alternatives considered

**Universal links / App Links from V1** — rejected:

- Requires DNS, file hosting, and domain verification work that is not on the Phase 1 critical path
- Adds complexity without delivering V1 user value
- Better completed alongside other launch-prep tasks (App Store submission, production environment setup)

**Web-only redirect to a success page** — rejected:

- Breaks the native app UX — user ends up on a web page after paying, with no clear path back into the app
- Cannot reliably trigger in-app payment confirmation flow

## Trade-offs accepted

- Custom URL schemes can be claimed by any app installed on the device — minor security / UX risk, acceptable for V1
- No fallback to web if the app is uninstalled — acceptable since checkout is only initiated from within the app
- Universal links migration work will be required before public launch

## Consequences

- `app.json` must register `tomale` as the URL scheme
- Frontend (Expo Router) must implement deep link routes for `/checkout/success` and `/checkout/cancel`
- Success screen must poll `check_order_paid` rather than trusting the redirect alone (payment is confirmed by Stripe webhook, not by the redirect)
- Cancel screen may use the included `session_id` for abandoned-cart logging

## Related notes

- [[Project/Plan/5-cto-implementation-plan|5-cto-implementation-plan]]
- [[Project/PRDs/PRD-Store-Orders|PRD-Store-Orders]]
- [[Project/Stack/3__Routing_-_Expo_Router|3. Routing - Expo Router]]