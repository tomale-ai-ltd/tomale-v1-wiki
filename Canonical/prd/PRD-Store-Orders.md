---
type: prd
title: PRD-Store-Orders
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-04-14
last_verified: 2026-04-14
owner: vault
---

# PRD: Store Feature (Checkout + Order History)

## Overview
The Store feature enables users to purchase printed versions of their stories. Orders are processed through Stripe for payment and fulfilled by Mixam via backend automation in Xano. Users can view their order history and track status updates.

---

## Goals
- Provide a smooth, multi-step checkout journey for story orders.
- Support native/device autofill for shipping details (iOS/Android).
- Integrate with Stripe checkout for secure payments.
- Handle order fulfilment through Xano → Mixam integration (no user involvement).
- Allow users to view their order history and track production/shipping status.
- Support error states (payment failure, cancellation, retries).

---

## Scope
### Entry
- **8.0 Store index**
  - Entry point from `(tabs)/store/index.tsx`.
  - Displays available store options, onboarding tips.
- **8.1 Store create order**
  - Launches checkout flow in `(main)`.
- **8.1.1 Store modal**
  - Info modal: explains store features and available order types.

### Checkout Flow (stateful, single RN route in `(main)`)
- **8.2 Select product**
  - User selects story (pre-loaded if launched from `story-detail`).
  - Choose size, orientation, product options.
  - Show dynamic pricing (from Stripe Products table via Xano).
- **8.2.1 Select shipping**
  - Choose from Shipping_Options (Xano).
  - Autofill supported (native autofill fields or Stripe PaymentSheet).
- **8.2.2 Payment**
  - Review order summary.
  - Initiate Stripe Checkout Session (via Xano endpoint).
  - Handle payment success/failure states.
- **8.2.3 Confirmation**
  - Show order confirmation + delivery details.
  - Trigger toast/notification for successful purchase.

### Order History
- **8.4 Order history (index)**
  - Lists past Store_Orders for user (fetched via Xano).
  - Status values include `processing`, `in_production`, `shipped`, `cancelled`, `payment_failed`.
- **8.4.1 Order detail**
  - Shows full detail of a single Store_Order.
  - Includes production/dispatch updates (from Store_Order_Updates table).
- **8.4.2 Payment failure**
  - Modal/screen shown if Stripe reports failure.
  - Option to retry payment.
- **8.4.3 Cancellation**
  - Confirmation that an order has been cancelled (archived in Xano).

---

## Data Model (Xano)
- **Products** → Source of product catalogue (synced with Stripe).
- **Shipping_Options** → Stored shipping methods.
- **Store_Orders** → Core entity linking user, instant_story.pdf, product, shipping, payment status.
- **Store_Order_Updates** → Created via Mixam webhook (production/dispatch updates).

---

## Backend Flow
1. User initiates checkout → frontend posts to `stripe_create_checkout_session` in Xano.  
2. Xano fetches Products + Shipping_Options, builds Store_Order, calls Stripe Checkout API.  
3. On payment success → Store_Order confirmed.  
4. Xano sends Store_Order + instant_story.pdf to Mixam API for fulfilment (Tomale pays).  
5. Mixam webhook → Xano creates Store_Order_Update (production/shipping).  
6. Frontend polls or listens for updates to display in Order History.  

---

## Technical Considerations
- **Autofill:**  
  - RN `TextInput` with `autoComplete` + `textContentType` props.  
  - Alternative: use Stripe PaymentSheet autofill.  
- **Error handling:**  
  - Payment failure → retry flow (8.4.2).  
  - Cancelled orders archived in Xano (status = cancelled).  
- **Notifications:**  
  - Push notification when order confirmed and when shipped (optional V1).  
- **Offline mode:**  
  - Orders cached locally via Zustand for offline access.  

---

## Out of Scope (V1)
- Library orders (8.3 series).  
- Teacher/classroom publishing.  
- Ratings/sharing of stories.  
- Manual order submission to Mixam (handled only by backend automation).  
