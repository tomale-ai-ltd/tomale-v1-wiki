---
type: decision
title: defer-stripe-webhook-mode-branching-to-phase-2
project: tomale-rn-v1
status: accepted
date: 2026-05-07
related:
  - "[[2026-05-07-003]]"
  - "[[PRD-transaction-webhooks-micro-prd]]"
features:
  - F-payments
  - F-subscriptions
---

# Decision: defer-stripe-webhook-mode-branching-to-phase-2

> Body restored in B7 (2026-10-28) from the 07/05 chat. The note had been overwritten with the Resend email text ([[replace-sendgrid-with-resend-for-transactional-email]]).

## What we decided

To defer the work of making the Stripe webhook handler branch on event mode (book order vs subscription) to Phase 2 of the CTO implementation plan, alongside the broader transaction-webhooks build defined in [[PRD-transaction-webhooks-micro-prd]].

The current `stripe/webhook_payment_confirmation` endpoint handles book orders only: confirming payment, updating the store order, creating a store order update and triggering the PDF generation orchestrator. It does not yet handle subscription events (`checkout.session.completed` with `mode: "subscription"`, `invoice.paid`, etc.).

## Why

- Phase 1 scope is API security and ownership, not new functional capability.
- No subscription purchases were happening (frontend paused, no live users buying subscriptions).
- The transaction-webhooks micro-PRD already specifies a unified `POST /webhooks/stripe` endpoint handling both flows; duplicating that work then would be wasted effort.
- The correct shape (one handler, two paths branched on `mode`) is well understood and can be built cleanly in Phase 2.

## Alternatives considered

- **Branch the handler in Phase 1:** rejected. It adds functional scope to a security phase and needs subscription-side logic (entitlements, subscription records) not otherwise needed yet.
- **A separate endpoint for subscriptions:** rejected. It conflicts with the PRD's unified handler and means two webhook URLs to register with Stripe.

## Trade-offs accepted

- The handler ignores subscription events until Phase 2, which is acceptable while there are no subscription purchases.
- Any subscription test traffic needs manual cleanup until then.

## Workflow detail

Phase 2 replaces `stripe/webhook_payment_confirmation` with `POST /webhooks/stripe`, branching on `mode` to the book order flow or the subscription flow. Now launch-relevant: see [[gate-image-generation-with-entitlements-at-story-creation]].

## Related notes

- [[5-cto-implementation-plan]]
- [[PRD-Subscription-Entitlement-System]]
- [[PRD-transaction-webhooks-micro-prd]]
