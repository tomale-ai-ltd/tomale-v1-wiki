---
type: architecture
title: order-cancellation-and-refund-flow
project: tomale-rn-v1
status: current
version: 1.1
date: 2026-10-14
last_verified: 2026-10-28
owner: vault
tags:
  - store-orders
  - cancellation
  - refunds
  - stripe
  - transactions
  - flow
---

# Order Cancellation and Refund Flow

How a customer cancels a paid print order during the cancellation window, and how the self-service refund is issued, retried and reconciled with Stripe. Companion to [[order-fulfilment-flow]].

Scope: this is the **self-service, pre-production** path only, per [[split-refund-model-into-self-service-and-support-paths]]. Misprint and quality refunds are support-driven and go through a future account-credit ledger. They never touch `refundable_amount`.

---

## 1. Customer cancel and refund

```mermaid
flowchart TD
    subgraph Key[" Key "]
        direction LR
        k1["🔗 API call / webhook"]
        k2["⚙ Custom function"]
        k8["⏱ Scheduled task"]
        k4["❓ Decision gate"]
        k5["🌐 External service"]
        k6["⏹ Response / end"]
        k7["💾 Database write"]
    end

    A["🔗 POST /app/store_orders/{id}/cancel<br/><i>auth: users</i>"]
    A --> B{"❓ Order exists AND<br/>users_id = $auth.id?"}
    B -->|no| B404["⏹ 404 ORDER_NOT_FOUND"]
    B -->|yes| C{{"❓ Cancellable?<br/>payment_status Confirmed<br/>status not Cancelled<br/>hpbc_order_id empty<br/>hpbc_lock false"}}
    C -->|no| C422["⏹ 422 ORDER_NOT_CANCELLABLE<br/><i>gone to print</i>"]
    C -->|yes| D["💾 store_order<br/>status: Cancelled, cancelled_at = now<br/>store_order_updates: Cancelled by customer"]
    D --> E["💾 queued pdf_jobs cancelled"]
    E --> F["⚙ payments/stripe_refund_order"]

    F --> F1{"❓ Payment row<br/>transactions type physical-product<br/>refundable_amount > 0?"}
    F1 -->|"0 (already refunded)"| OK["⏹ 200 Cancelled<br/>refund_status: succeeded"]
    F1 -->|yes| F2{"❓ refund_force_success = true<br/>AND users.test_mode?"}
    F2 -->|yes| F3["Fake refund id re_test_{order}"]
    F2 -->|no| F4["🌐 Stripe POST /v1/refunds<br/>payment_intent, amount = refundable_amount<br/>Idempotency-Key refund_{order}_{refund_attempt_count}"]

    F3 --> G["💾 transactions refund row<br/>payment row refundable_amount = 0<br/>store_order_updates: Refund issued"]
    F4 -->|"succeeded / pending"| G
    F4 -->|"error / failed"| H["💾 payment row<br/>refund_attempt_count + 1<br/>refund_last_attempt_at = now"]

    G --> OK2["⏹ 200 Cancelled<br/>refund_status: succeeded / pending"]
    H --> P["⏹ 200 Cancelled<br/>refund_status: pending"]

    classDef apiCall fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef function fill:#ede9fe,stroke:#7c3aed,color:#4c1d95;
    classDef task fill:#dcfce7,stroke:#16a34a,color:#14532d;
    classDef gate fill:#cffafe,stroke:#0891b2,color:#164e63;
    classDef external fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef terminal fill:#e2e8f0,stroke:#64748b,color:#334155;
    classDef write fill:#f1f5f9,stroke:#94a3b8,color:#1e293b;

    class k1 apiCall;
    class k2 function;
    class k8 task;
    class k4 gate;
    class k5 external;
    class k6 terminal;
    class k7 write;

    class A apiCall;
    class F,F3 function;
    class B,C,F1,F2 gate;
    class F4 external;
    class B404,C422,OK,OK2,P terminal;
    class D,E,G,H write;
```

---

## 2. Retrying and reconciling refunds

```mermaid
flowchart TD
    R0["⏱ reconcile_order_refunds<br/>every 15 min"] --> R1{{"❓ Needs refund?<br/>status Cancelled, hpbc_order_id empty<br/>payment row refundable_amount > 0<br/>refund_attempt_count < 5<br/>≥ 15 min since refund_last_attempt_at"}}
    R1 -->|yes| R2["⚙ payments/stripe_refund_order<br/><i>new idempotency key per attempt</i>"]
    R1 -->|"attempts = 5"| R3["💾 store_order_updates<br/>Refund failed after 5 attempts: manual handling<br/>⏹ support"]
    R1 -->|none| R4["⏹ Wait for next run"]

    S0["🌐 Stripe refund.updated / refund.failed"] --> S1["🔗 POST /stripe/webhook_payment_confirmation<br/><i>signature, webhook_event_ingest, dedup_key</i>"]
    S1 --> S2{"❓ transactions refund row<br/>with provider_payment_id = refund id?"}
    S2 -->|found| S3["💾 refund row status updated"]
    S3 --> S4{"❓ New status failed / canceled?"}
    S4 -->|yes| S5["💾 payment row<br/>refundable_amount restored<br/>refund_attempt_count + 1<br/>store_order_updates: Refund failed, retrying"]
    S5 -.->|picked up by| R0
    S4 -->|"succeeded"| S6["⏹ Done"]
    S2 -->|"not found<br/>(refund made in Stripe dashboard)"| S7["💾 refund row recorded<br/>refundable_amount unchanged<br/>store_order_updates: review"]
    S3 --> S8["⚙ webhook_event_complete<br/>⏹ 200"]
    S7 --> S8

    classDef apiCall fill:#dbeafe,stroke:#2563eb,color:#1e3a8a;
    classDef function fill:#ede9fe,stroke:#7c3aed,color:#4c1d95;
    classDef task fill:#dcfce7,stroke:#16a34a,color:#14532d;
    classDef gate fill:#cffafe,stroke:#0891b2,color:#164e63;
    classDef external fill:#fce7f3,stroke:#db2777,color:#831843;
    classDef terminal fill:#e2e8f0,stroke:#64748b,color:#334155;
    classDef write fill:#f1f5f9,stroke:#94a3b8,color:#1e293b;

    class S1 apiCall;
    class R2,S8 function;
    class R0 task;
    class R1,S2,S4 gate;
    class S0 external;
    class R4,S6 terminal;
    class R3,S3,S5,S7 write;
```

---

## Rules

- **Cancellable window:** from payment until `hpbc_submit_due_orders` claims the order: `submit_after` (30 min, or 1 min for test users) plus up to one 60-second task interval. After submission, cancellation is closed. Personalised goods are exempt from the 14-day cancellation right (Consumer Contracts Regulations 2013, reg. 28(1)(b)); confirm the wording in the terms.
- **Order before money:** the order is set to Cancelled before the refund is attempted, so a failed refund can never let a cancelled order print.
- **Full refunds only** on this path, for the amount in `refundable_amount` on the original `transactions` row (type `physical-product`).
- **Idempotency key** `refund_{store_orders_id}_{refund_attempt_count}`. A network retry reuses the key and Stripe returns the same refund. After a confirmed failure the count increases, so the next attempt is a fresh refund. Stripe keeps a key's result for 24 h.
- **Test mode:** with `refund_force_success = "true"` and `users.test_mode = true`, Stripe is skipped and a fake `re_test_` id is recorded. Postman's simulated payments have no real payment intent. `refund_force_success` must be `"false"` in prod.
- **Webhooks never read `$auth`.**

## Tables and fields

| Table | Fields used |
|---|---|
| `store_orders` | `status`, `payment_status`, `hpbc_order_id`, `hpbc_lock`, `submit_after`, `cancelled_at` |
| `store_order_updates` | `store_orders_id`, `message`, `created_at` |
| `transactions` (payment row) | `type` = physical-product, `provider_payment_id` (payment intent), `amount_minor`, `currency`, `refundable_amount`, `refund_attempt_count`, `refund_last_attempt_at` |
| `transactions` (refund row) | `type` = refund, `provider_payment_id` (`re_…`), `amount_minor`, `currency`, `status`, `users_id`, `store_orders_id` |
| `transaction_webhook_events` | `dedup_key`, `event_type`, `status`, `processing_errors` |
| `pdf_jobs` | queued jobs for the order are cancelled |

## Open points

- `store_orders.payment_status` is not set to `Refunded` when a refund succeeds. The value exists in the enum, so add the write in `stripe_refund_order` (and in the webhook handler, if it confirms a pending refund).
- There is no customer notification yet for a cancellation or refund (in-app alert or Resend email).
- The support-driven refund / account-credit ledger is a future item.

## Related notes

- [[order-fulfilment-flow]]
- [[split-refund-model-into-self-service-and-support-paths]]
- [[record-transactions-drop-checkout-session-object]]
- [[store-money-as-integer-minor-units]]
- [[differentiate-ingest-vs-processing-failure-responses-for-webhooks]]
