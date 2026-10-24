# MICRO-PRD: Transaction Webhooks & Billing Event Processing

---

## Goal

Provide a reliable, provider-agnostic webhook ingestion system to:

- Process billing events from Stripe, Apple, and Google
- Maintain accurate subscription state
- Trigger entitlement recalculation
- Ensure auditability and replay capability

---

## Scope

Covers:

- Webhook ingestion endpoints (Stripe, Apple, Google)
- Event storage (`transaction_webhook_events`)
- Event validation & idempotency
- Normalisation into internal event format
- Subscription state updates
- Entitlement recalculation triggers

---

## Non-Goals

- Payment UI / checkout flows  
- Pricing logic  
- Subscription plan configuration  
- Frontend notification handling  

---

## Core Concepts (non-negotiable)

- Webhooks are **source of truth for billing state**
- All webhook payloads must be **stored before processing**
- Processing must be **idempotent**
- External events must be **normalised into internal events**
- Webhook ingestion must **fail safely and retryable**

---

## Backend Requirements

### API Endpoints

POST /webhooks/stripe  
POST /webhooks/apple  
POST /webhooks/google  

---

### Responsibilities (per endpoint)

1. Validate signature  
2. Store raw payload  
3. Check idempotency  
4. Normalise event  
5. Process event  
6. Emit internal event  

---

## Data Models

### transaction_webhook_events

id  
provider (stripe, apple, google)  
event_id (external id)  
event_type  
payload (JSON)  
processing_status (pending, success, failed)  
retry_count  
processed_at  
created_at  

---

### subscriptions (existing, updated via webhook)

user_id  
product_id  
status  
source (apple, google, stripe)  
current_period_start  
current_period_end  
provider_subscription_id  

---

## Event Normalisation

All provider-specific events must be converted into a common format:

{
  "type": "subscription_started | subscription_renewed | subscription_failed | subscription_cancelled",
  "user_id": 123,
  "source": "stripe",
  "external_id": "abc123"
}

---

## Supported Events (V1)

### Stripe

- checkout.session.completed → subscription_started  
- invoice.paid → subscription_renewed  
- invoice.payment_failed → subscription_failed  
- customer.subscription.deleted → subscription_cancelled  

---

### Apple

- DID_RENEW → subscription_renewed  
- DID_FAIL_TO_RENEW → subscription_failed  
- EXPIRED → subscription_cancelled  

---

### Google

- SUBSCRIPTION_PURCHASED → subscription_started  
- SUBSCRIPTION_RENEWED → subscription_renewed  
- SUBSCRIPTION_CANCELED → subscription_cancelled  
- SUBSCRIPTION_EXPIRED → subscription_cancelled  

---

## Processing Logic

### subscription_started

- Create or update subscription  
- Set status = active  
- Set billing period  

---

### subscription_renewed

- Extend billing period  
- Ensure status = active  

---

### subscription_failed

- Set status = past_due  
- Trigger entitlement downgrade  

---

### subscription_cancelled

- Set status = cancelled  
- Maintain access until period end  

---

## Hard Rules (Backend)

- Webhook must be **stored before any processing**
- Processing must be **idempotent (event_id unique)**
- Duplicate events must not mutate state twice
- Subscription state must always reflect latest valid event
- Webhook failures must be retryable without side effects

---

## Idempotency Strategy

- Use `event_id` (provider-specific) as unique key  
- Reject or ignore duplicate processing attempts  
- Processing must be safe to run multiple times  

---

## Entitlement Integration

After subscription update:

trigger entitlement recalculation

---

## Internal Event Emission

subscription_started  
subscription_renewed  
subscription_failed  
subscription_cancelled  

Used by:

- entitlement system  
- task system  
- notifications  

---

## Error Handling

### Failure Modes

- invalid signature → reject request  
- malformed payload → store + mark failed  
- processing error → retry  

---

### Retry Strategy

- Increment `retry_count`
- Reprocess failed events via cron
- Maximum retry threshold (configurable)

---

## Observability

Track:

- total events received
- success vs failure rate
- retry counts
- processing latency

---

## Acceptance Criteria

- All webhook events are stored before processing  
- Duplicate events do not cause duplicate state changes  
- Subscription state always reflects latest valid billing event  
- Entitlements update correctly after webhook processing  
- Failed events can be retried safely  
- System supports multiple providers without branching logic  

---

## Payment Source Abstraction

{
  "source": "apple | google | stripe"
}

### Rules

- Processing logic must not differ by source  
- Only mapping layer handles provider differences  

---

## Architecture Summary

Webhook → Store → Normalise → Process → Update Subscription → Recalculate Entitlements → Emit Event

---

## Final Note

This system is your **single point of truth for billing**.

If it fails:
- entitlements break  
- billing breaks  
- user trust breaks  

Keep it:
- simple  
- observable  
- idempotent  
