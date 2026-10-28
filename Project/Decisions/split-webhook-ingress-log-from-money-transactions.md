---
type: decision
title: split-webhook-ingress-log-from-money-transactions
project: tomale-rn-v1
status: accepted
date: 2026-07-03
related:
  - "[[2026-07-03-001]]"
  - "[[v1-audit]]"
affects:
  - transaction_webhook_events
  - transactions
features:
  - F-payments
---

# Decision: split-webhook-ingress-log-from-money-transactions

## What we decided

`transaction_webhook_events` is a single ingress log for every provider's webhooks (Stripe, HPBC, later Apple and Google), with `provider` as indexed free text. `transactions` holds money only. HPBC events drive `store_orders` and `store_order_updates`, never `transactions`.

## Related notes

- [[2026-07-03-001]] (backfilled in B7)
- [[record-transactions-drop-checkout-session-object]]
- [[adopt-unique-index-dedup-for-webhook-ingest]]
