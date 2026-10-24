---
type: decision
title: verify-stripe-checkout-totals-against-xano-prices
project: tomale-rn-v1
status: accepted
date: 2026-10-12
---

---

# Decision: verify-stripe-checkout-totals-against-xano-prices

## What we decided

Xano is the source of truth for physical book prices. `create_checkout_session` now verifies server-side that Stripe returned status 200 and that `amount_total` equals (subtotal + shipping) in pence before returning a checkout URL. Subscriptions keep per-platform price IDs with daily reconciliation; books remain Stripe-only.

## Why

A flow-test run showed Stripe charging £11.98 against an order of £26.98, because `stripe_price_test` pointed at an old £9.99 price. Without a guard, a stale price ID silently produces a wrong charge. The check also catches a cheaper client-supplied `shipping_option_id`.

## Alternatives considered

Building Stripe `price_data` directly from Xano amounts (so no Stripe price IDs are involved) was identified as the target approach but deferred. Archiving old test/live Stripe prices so stale IDs fail loudly is a housekeeping follow-up.

## Trade-offs accepted

V1 still depends on Stripe price IDs being correct and kept in sync with Xano; the guard detects mismatches rather than preventing them. Accepted until `price_data` is built from Xano amounts.

## Workflow detail

`create_checkout_session` now returns only `checkout_session_id`, `url` and `amount_total` (previously it leaked the raw Stripe request including the secret key), with `currency` populated (`gbp`) and amounts normalised to pence. New Postman tests CS5–CS8 assert no secrets in the response and that the Stripe amount equals the order total. Each `stripe_price_live` still needs verifying.

## Related notes

- [[Sessions/2026-10-12-001]]
- [[store-money-as-integer-minor-units]]
- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[use-fixture-story-for-order-flow-test]]
- [[order-fulfilment-flow]]
- [[PRD-Store-Orders]]
- [[formalise-story-status-lifecycle]]
- [[replace-long-done-poll-with-stuck-story-check]]
