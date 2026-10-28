---
type: decision
title: return-from-stripe-checkout-via-in-app-browser-sheet
project: tomale-rn-v1
status: accepted
date: 2026-10-28
supersedes:
  - "[[use-custom-url-scheme-for-stripe-checkout-redirect-v1]]"
related:
  - "[[v1-audit]]"
  - "[[use-per-build-variant-url-schemes]]"
affects:
  - stripe/create_checkout_session
  - PRD-Store-Orders
features:
  - F-store
  - F-payments
---

# Decision: return-from-stripe-checkout-via-in-app-browser-sheet

## What we decided

Stripe Checkout opens in an in-app browser sheet (`WebBrowser.openAuthSessionAsync`) that watches for a redirect to the app's URL scheme (`<scheme>://checkout/success|cancelled`). When Stripe redirects there, the sheet closes itself and the app shows its own confirmation (splash) screen. The customer never lands on the company website.

If Stripe won't accept a custom scheme as `success_url`/`cancel_url`, Stripe points at a blank https page on tomale.ai that immediately forwards to the app scheme. Which variant is used, and how Xano picks the scheme (server-side, from its branch or `test_mode`, never from client input, to avoid an open redirect), is settled in the Slice 400 spec.

## Why

The live flow sends customers to `https://www.tomale.ai/checkout-stripe-success`, which leaves them on the website after paying. Kyle wants the app to stay in control of the experience.

## Alternatives considered

- Keep the website success/cancel pages (current live behaviour): rejected, poor UX.
- Plain `tomale://` redirect with the system browser: the browser stays open behind the app.

## Trade-offs accepted

Needs a small amount of client work (auth session + confirmation screen) and possibly a forwarding page. Live checkout keeps the website pages until Slice 400 ships.

## Related notes

- [[v1-audit]] (C1)
- [[use-per-build-variant-url-schemes]]
- [[verify-stripe-checkout-totals-against-xano-prices]]
