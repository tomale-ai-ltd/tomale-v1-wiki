---
type: decision
title: scope-hpbc-callbacks-to-six-customer-facing-statuses
date: 2026-07-15
status: current
project: tomale-rn-v1
---

---

# Decision: scope-hpbc-callbacks-to-six-customer-facing-statuses

## What we decided

HPBC callbacks are the customer-facing status surface, limited to six statuses total: Order Confirmed, In Production, Shipped, and Cancelled on the success endpoint (`webhook_statusCallbackUrl`), and Error (covering both error triggers) on the error endpoint (`webhook_statusCallbackUrl_Error`). As part of this, the `store_orders.status` enum's `Delivered` value was renamed to `Shipped`, because the HPBC callback fires at dispatch, not delivery, and there is no delivery-confirmation trigger available. Delivery-status tracking (e.g. carrier or aggregator tracking-link scraping) is parked as a future item; Shipped-with-tracking-link is the terminal customer state for v1. Full HPBC operational granularity stays in the HPBC dashboards and is deliberately not surfaced to the customer; both error trigger types collapse to a single customer-facing Error status, with the specific operational detail preserved in the `store_order_updates` message rather than exposed as separate statuses.

## Why

The live `store_orders.status` enum (draft, Payment Pending, Payment Confirmed, Order Confirmed, In Production, Delivered, Cancelled, Error) assumed a delivery-confirmation event that HPBC doesn't send — HPBC's dispatch callback is the last signal available, so a status named "Delivered" would be inaccurate. Collapsing HPBC's full operational detail down to six customer statuses keeps the customer-facing surface simple and avoids exposing internal fulfilment machinery the customer doesn't need to see; that detail remains available to support via the HPBC dashboard and the stored update message.

## Alternatives considered

Building carrier or aggregator tracking-link integration to get a true delivery-confirmation signal — considered and explicitly parked as not worth the integration or aggregator cost for v1. Surfacing HPBC's full operational granularity (rather than collapsing to six statuses) as separate customer-facing states.

## Trade-offs accepted

Shipped-with-tracking-link, not true delivery confirmation, is the terminal customer state for v1 — accepted because building carrier/aggregator tracking isn't worth the cost at this stage. Both error trigger types (submission error, production error) collapse to the same customer-facing Error status, with the distinguishing detail available only in the internal update log, not as separate customer states — accepted because the customer-facing status is "Error" either way and support handles resolution from the dashboard detail.

## Workflow detail

Implemented in `webhook_statusCallbackUrl` and `webhook_statusCallbackUrl_Error`, both built this session by wrapping the existing `hpbc_update_order` call in the proven ingest/dedup/complete pattern. Both error triggers send `status: "Error"` with no field distinguishing the two, which the router passes through without mapping.

## Related notes

[[Sessions/2026-07-15-001]]
[[order-fulfilment-flow]] — full order lifecycle flowchart produced this session
[[confirm-hpbc-webhook-dedup-key-format]] — same endpoints, dedup key mechanics
[[authenticate-hpbc-webhooks-with-shared-secret-bearer-token]] — same endpoints, auth mechanics
