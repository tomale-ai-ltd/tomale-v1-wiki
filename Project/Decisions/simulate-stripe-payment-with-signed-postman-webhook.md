---
type: decision
title: simulate-stripe-payment-with-signed-postman-webhook
project: tomale-rn-v1
status: accepted
date: 2026-10-09
features:
  - X-testing
---

# Decision: Simulate the Stripe Payment Hop with a Signed Webhook Sent from Postman

## What we decided

In the order-fulfilment flow test, the payment step (3B-2, formerly the manual A4 gate) is a Postman request to `POST {{webhookUrl}}/stripe/webhook_payment_confirmation`. A pre-request script builds a `checkout.session.completed` event for `{{checkoutSessionId}}`, signs it with HMAC-SHA256 over `t.payload` using the test-mode `stripe_webhook_secret`, and sends it raw with a `Stripe-Signature` header. Each run uses a unique `evt_test_…` event id because the webhook dedups. The post-response script asserts 200. This replaces the previous plan (2026-10-08) of a one-off Stripe CLI trigger plus a dev-only simulate flag. Test environment only.

## Why

`stripe trigger` fires fixture events that are not tied to our checkout session, so the backend would not mark the order paid. The Stripe CLI also cannot run inside a Postman monitor, and no simulate endpoint exists. Signing with the test-mode `whsec_` secret exercises the real signature-validation path. A sample real payload showed `metadata: {}` and `client_reference_id: null`, so the webhook matches the order by the `cs_test_…` session id; the simulated event only needs that to match.

## Alternatives considered

- **Stripe CLI one-off trigger** — rejected: fixture events do not match our checkout session, and the CLI cannot run in a monitor.
- **Dev-only simulate flag** — rejected: no simulate endpoint exists (see [[avoid-recreating-removed-endpoints-for-testing]]).

## Trade-offs accepted

The simulation is not yet verified end to end: the signing secret must match the one Xano verifies against, and extra fields (`customer`, `customer_details`) may be needed if the 15-step webhook reads them. Polling and `setNextRequest` aside, the request only works with a correctly populated `checkoutSessionId`, which was not yet captured at the time of the decision.

## Workflow detail

The payment gate is no longer manual, so the collection can run unattended in the Collection Runner, Newman, or a monitor. `stripe_webhook_secret` is a secret-type environment variable; whether secret variables are available in cloud monitor runs is unconfirmed. 3B-2 must be moved above 3B-1 (`check_order_paid`) so the paid check runs after the simulated payment.

## Related notes

- [[avoid-recreating-removed-endpoints-for-testing]]
- [[use-fixture-story-for-order-flow-test]]
- [[replace-manual-test-gates-with-bounded-polling]]
- [[run-real-fulfilment-cascade-against-staging-sku]]
- [[authenticate-hpbc-webhooks-with-shared-secret-bearer-token]]
- [[order-fulfilment-flow]]
- [[6-api-security-model]]
- [[2026-10-09-001]]
