---
type: entity
entity-type: org
name: Pureprint
aliases:
  - Alex
tags:
  - llm-wiki/entity
  - llm-wiki/entity/org
source-count: 18
date-updated: 2026-10-24
cssclasses: []
---


# Pureprint

## Facts

- Pureprint is the print supplier confirmed for staging SKUs.
- Pureprint confirmed that staging orders incur no HPBC charge.
- Alex at Pureprint is responsible for confirming live SKU strings.
- Pureprint confirmed staging orders stay at 'Order Confirmed' unless manually cancelled.
- Provided key facts regarding staging orders and product specifications.
- Pureprint's Shipped template was updated to include the tracking fields.
- Pureprint's process alignment was discussed, including their PDF settings and order trigger sequence.
- Pureprint is involved in the order fulfilment process and provides printing services.
- The submission may have reached Pureprint.
- Pureprint's real trigger sequence is referenced for managing order statuses.
- Pureprint's Order Print Ready step is batched and cannot be backed out.
- Pureprint's trigger sequence influences the decision to implement a cancellation window.
- The PRDs include Mixam to Pureprint.
- Pureprint's status text was overwriting the buyer's gift message in store_orders.
- The buyer's gift message was overwritten with Pureprint text on every HPBC callback.
- Pureprint is one of the third parties involved in the Tomale project.

## Connections

- [[tomale-rn-v1]] *(related-to)*
- [[order-fulfilment-flow-test]] *(related-to)*
- [[hpbc]] *(related-to)*
- [[tracking-fields]] *(extends)*
- [[order-error-handling]] *(related-to)*
- [[hpbcupdateorder]] *(related-to)*
- [[cancellation-window]] *(influences)*
- [[xano]] *(related-to)*
- [[tomale-v1]] *(related-to)*
- [[tomale-rn-v1]] *(related-to)*
- [[mixam]] *(related-to)*

## Sources

- [[_raw/Chat Sessions/_archive/2026-10-08-001.md]]
- [[Sessions/2026-10-08-001.md]]
- [[Project/Decisions/run-real-fulfilment-cascade-against-staging-sku.md]]
- [[Project/Decisions/key-hpbc-environment-switch-off-stripe-test-mode.md]]
- [[Project/Decisions/replace-manual-test-gates-with-bounded-polling.md]]
- [[_raw/Chat Sessions/_archive/2026-10-13-001.md]]
- [[Sessions/2026-10-13-001.md]]
- [[Project/Decisions/store-hpbc-tracking-on-store-orders.md]]
- [[_raw/Chat Sessions/_archive/2026-10-14-001.md]]
- [[Sessions/2026-10-14-001.md]]
- [[Project/Decisions/mark-order-error-on-hpbc-rejection-and-clear-lock.md]]
- [[Project/Decisions/enforce-forward-only-hpbc-callback-status-transitions.md]]
- [[Project/Decisions/disallow-cancelling-personalised-orders-once-in-production.md]]
- [[Project/Decisions/delay-hpbc-submission-with-30-minute-cancellation-window.md]]
- [[Project/Decisions/defer-documentation-refresh-until-after-phase-1-signoff.md]]
- [[_raw/Chat Sessions/_archive/2026-10-15-001.md]]
- [[Project/Decisions/avoid-column-named-function-inputs-in-xano.md]]
- [[Project/Plan/operating-model.md]]
