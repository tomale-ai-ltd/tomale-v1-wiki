---
type: entity
entity-type: other
name: store_orders
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/other
source-count: 4
date-updated: 2026-10-24
cssclasses: []
---


# store_orders

## Facts

- Completed store_orders with auth + ownership scoping on POST/GET/GET by ID/PATCH.
- The `store_orders` schema is used to track the lifecycle of orders, including statuses such as Payment Pending and Payment Confirmed.
- store_orders is the schema that tracks the status and details of orders.
- Represents the schema for managing orders in the system.
- Money fields are now integer pence, matching products, shipping_options, and transactions.
- The `store_orders.subtotal` and `shipping_amount` fields are moved from decimal pounds to integer pence.

## Connections

- [[commerce]] *(related-to)*
- [[transactionwebhookevents]] *(related-to)*
- [[transactionwebhookevents]] *(uses)*
- [[order-fulfilment-flow]] *(part-of)*
- [[status-vocabulary]] *(related-to)*
- [[hpbc-aka-pureprint]] *(related-to)*
- [[papermill]] *(uses)*
- [[money-units]] *(extends)*
- [[hpbc]] *(related-to)*
- [[stripecreatecheckoutsession]] *(uses)*
- [[tomale-rn-v1]] *(part-of)*
- [[hpbc]] *(uses)*
- [[striperefundorder]] *(related-to)*
- [[hpbc]] *(related-to)*

## Sources

- [[Sessions/2026-04-16-001.md]]
- [[Project/Architecture/story-creation-flow.md]]
- [[Project/Architecture/order-fulfilment-flow.md]]
- [[Project/Decisions/migrate-store-orders-money-fields-to-integer-pence.md]]
