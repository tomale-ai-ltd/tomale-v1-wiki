---
type: entity
entity-type: org
name: HPBC
aliases:
  - Pureprint
tags:
  - llm-wiki/entity
  - llm-wiki/entity/org
source-count: 46
date-updated: 2026-10-24
cssclasses: []
---


# HPBC

## Facts

- HPBC server-to-server callbacks are included in the 'webhooks' group.
- HPBC is referenced in relation to transaction webhook events and payment processing.
- HPBC is referenced in relation to transaction webhook events and order processing.
- HPBC is referenced in the context of transaction webhook events and payment processing.
- HPBC is involved in webhook signature validation.
- Confirmed HPBC uses bearer token auth, not a signature.
- HPBC is the fulfilment provider integrated into the order flow.
- Silent failures on fulfilment paths can occur without backend error reporting.
- HPBC is another webhook provider wired into the webhook router.
- Built both HPBC status callback endpoints against a real captured payload.
- HPBC callback endpoints were built and verified against real captured payloads.
- Built both HPBC callback endpoints against a real captured payload.
- HPBC callbacks are limited to six customer-facing statuses: Order Confirmed, In Production, Shipped, Cancelled, and Error.
- HPBC is an external service with no user account or JWT to authenticate against.
- The HPBC webhook dedup key is formatted as 'hpbc:{hpbc_order_id}:{status}' on the success endpoint and 'hpbc_error:{hpbc_order_id}:Error' on the error endpoint.
- HPBC webhook endpoints were confirmed complete.
- HPBC webhook endpoints completed.
- Bearer token rotated and updated in Xano.
- Involved in the order fulfillment process for generating PDFs.
- HPBC is part of the order fulfillment process, specifically in generating PDFs and handling callbacks.
- HPBC is involved in the order-fulfillment process as part of the test design.
- The fulfilment provider integrated into the order flow.
- HPBC terminal-status is part of the order-fulfilment flow.
- HPBC is involved in the order-fulfilment process and is linked to the PDF generation.
- HPBC is involved in the order-fulfilment process, specifically for print services.
- HPBC has no sandbox available for testing.
- The HPBC environment is involved in the decision regarding the Stripe test mode.
- Reviewed the HPBC order payload for order confirmation.
- Used for terminal-status checks in the order-fulfilment flow.
- HPBC confirmed the order with PDFs attached.
- HPBC is involved in the order-fulfilment process.
- The HPBC terminal-status gate is part of the polling loops with bounded attempts.
- Involved in the order fulfillment process and provided specifications for order handling.
- Staging orders confirmed to sit at Order Confirmed indefinitely unless manually cancelled.
- Tracking data from the HPBC Shipped callback is stored on store_orders.
- HPBC (Pureprint) order payloads will not include preflight profile, production timescales, unit price, or unit cost.
- HPBC is involved in the order creation process, which now fails closed to prevent accidental live orders.
- HPBC submission processes and status transitions were outlined in relation to order fulfilment.
- HPBC is associated with the order submission process and tracking.
- When HPBC rejects an order, it is marked Error.
- HPBC is the organization to which orders are submitted.
- HPBC is responsible for the fulfilment of orders and status callbacks.
- Order 134 was not sent to HPBC due to a query issue with the hpbc_order_id.
- Order 134 did not reach HPBC due to a blank hpbc_order_id.
- HPBC is involved in the tracking and order management processes.
- HPBC status callback endpoints now map 'message' to 'update_message'.
- HPBC still receives pounds, converted at dispatch in hpbc_create_order.
- HPBC callbacks use bearer-token authentication for ingesting and deduplicating events.
- HPBC request was made for order amounts during testing.
- HPBC request was made for order amounts during the money units test.
- HPBC token rotation confirmed.
- HPBC still receives pounds for order amounts.
- HPBC callbacks are used for authentication and data ingestion.
- HPBC still receives amounts in pounds, requiring a divide-by-100 adjustment.

## Connections

- [[xano-api-group-consolidation]] *(related-to)*
- [[webhookeventingest]] *(uses)*
- [[order-fulfilment-flow]] *(part-of)*
- [[order-fulfilment-flow]] *(uses)*
- [[transactionwebhookevents]] *(related-to)*
- [[backend-observability]] *(related-to)*
- [[deduplication-mechanism]] *(uses)*
- [[webhook]] *(applies-to)*
- [[webhookstatuscallbackurl]] *(uses)*
- [[webhookstatuscallbackurlerror]] *(uses)*
- [[tomale-rn-v1]] *(part-of)*
- [[bearer-token-authentication]] *(uses)*
- [[webhook-deduplication-key-format]] *(extends)*
- [[tomale-rn-v1]] *(related-to)*
- [[order-fulfillment]] *(part-of)*
- [[order-fulfilment-test-design]] *(part-of)*
- [[order-fulfilment-flow-test]] *(related-to)*
- [[order-fulfilment-flow-test]] *(uses)*
- [[bounded-polling]] *(part-of)*
- [[storeorders]] *(uses)*
- [[order-error-handling]] *(influences)*
- [[order-fulfillment]] *(applies-to)*
- [[xano]] *(related-to)*
- [[api-security-model]] *(uses)*
- [[storeorders]] *(related-to)*
- [[monetisation-strategy]] *(uses)*
- [[transactionwebhookevents]] *(related-to)*
- [[tomale-v1]] *(uses)*
- [[tomale-rn-v1]] *(uses)*
- [[order-fulfilment-flow-test]] *(uses)*
- [[stripe]] *(related-to)*
- [[pureprint]] *(related-to)*
- [[tomale-rn-v1]] *(related-to)*
- [[tomale]] *(uses)*
- [[storeorders]] *(related-to)*

## Sources

- [[Project/Decisions/consolidate-xano-api-groups-into-app-and-webhooks.md]]
- [[_raw/Chat Sessions/_archive/2026-07-03-001.md]]
- [[Sessions/2026-07-03-001.md]]
- [[Project/Architecture/story-creation-flow.md]]
- [[Project/Architecture/order-fulfilment-flow.md]]
- [[_raw/Chat Sessions/_archive/2026-07-14-001.md]]
- [[Sessions/2026-07-14-001.md]]
- [[Project/Decisions/elevate-backend-observability-to-launch-requirement.md]]
- [[Project/Decisions/adopt-unique-index-dedup-for-webhook-ingest.md]]
- [[_raw/Chat Sessions/_archive/2026-07-15-001.md]]
- [[Sessions/2026-07-15-001.md]]
- [[Project/Decisions/scope-hpbc-callbacks-to-six-customer-facing-statuses.md]]
- [[Project/Decisions/authenticate-hpbc-webhooks-with-shared-secret-bearer-token.md]]
- [[Project/Decisions/confirm-hpbc-webhook-dedup-key-format.md]]
- [[_raw/Chat Sessions/_archive/2026-07-16-001.md]]
- [[_raw/Chat Sessions/Untitled.md]]
- [[_raw/Chat Sessions/_archive/2026-09-14-001.md]]
- [[Sessions/2026-09-14-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-08-001.md]]
- [[Sessions/2026-10-08-001.md]]
- [[Project/Decisions/run-real-fulfilment-cascade-against-staging-sku.md]]
- [[Project/Decisions/key-hpbc-environment-switch-off-stripe-test-mode.md]]
- [[_raw/Chat Sessions/_archive/2026-10-12-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-09-001.md]]
- [[Sessions/2026-10-12-001.md]]
- [[Sessions/2026-10-09-001.md]]
- [[Project/Decisions/replace-manual-test-gates-with-bounded-polling.md]]
- [[_raw/Chat Sessions/_archive/2026-10-13-001.md]]
- [[Sessions/2026-10-13-001.md]]
- [[Project/Decisions/store-hpbc-tracking-on-store-orders.md]]
- [[Project/Decisions/omit-preflight-timescales-and-unit-prices-from-hpbc-orders.md]]
- [[Project/Decisions/make-hpbc-create-order-a-single-fail-closed-request.md]]
- [[_raw/Chat Sessions/_archive/2026-10-14-001.md]]
- [[Sessions/2026-10-14-001.md]]
- [[Project/Decisions/mark-order-error-on-hpbc-rejection-and-clear-lock.md]]
- [[Project/Decisions/delay-hpbc-submission-with-30-minute-cancellation-window.md]]
- [[_raw/Chat Sessions/_archive/2026-10-15-001.md]]
- [[Sessions/2026-10-15-001.md]]
- [[Project/Plan/documentation-refresh-backlog.md]]
- [[Project/Decisions/avoid-column-named-function-inputs-in-xano.md]]
- [[Project/Plan/6-api-security-model.md]]
- [[_raw/Chat Sessions/_archive/2026-10-23-001.md]]
- [[_raw/Chat Sessions/_archive/2026-10-22-001.md]]
- [[Sessions/2026-10-23-001.md]]
- [[Sessions/2026-10-22-001.md]]
- [[Project/Decisions/migrate-store-orders-money-fields-to-integer-pence.md]]
