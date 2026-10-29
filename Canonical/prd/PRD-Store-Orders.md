---
type: prd
title: PRD-Store-Orders
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-store
related:
  - "[[PRD-Order-PoD-System]]"
  - "[[order-fulfilment-flow]]"
  - "[[order-cancellation-and-refund-flow]]"
  - "[[v1-feature-map]]"
---

# PRD: Store Feature (Checkout + Order History)

> **Changes in 2.0 (B9, 29/10/2026):**
> - Fulfilment is HP Brand Centre / Pureprint, not Mixam.
> - Statuses match the live `store_orders`.
> - Prices come from Xano in pence, not Stripe.
> - New: a pre-payment e-reader preview; Stripe Checkout opens in an in-app browser sheet that returns to an in-app confirmation; a 30-minute self-service cancel window with automatic refund; no cancellation once in production; the parental-approval gate; tracking; the gift message.
> - Push notifications are replaced by in-app alerts.
>
> - Reviewed with Kyle (29/10): products are A4 landscape paperback and hardback; Creator gets 25% off; Club moved to V2; emails on confirm, ship and cancel; a countdown on the order page instead of a window-closing email; the gift message is editable until payment.
>
> The backend is built and tested (86/86 `_tests`). Slice 400 / expected speckit 010 ([[roadmap]] M6).

## Overview
The Store feature enables users to purchase printed versions of their stories. Orders are paid through Stripe Checkout and fulfilled by HP Brand Centre / Pureprint via backend automation in Xano. Users can view their order history and track status updates.

## Goals
- Provide a smooth, multi-step checkout journey for story orders.
- Let the customer approve the book in the e-reader before paying.
- Support native/device autofill for shipping details (iOS/Android).
- Pay with Stripe Checkout without leaving the app experience.
- Handle fulfilment automatically (Xano → Papermill PDFs → HPBC/Pureprint), with no user involvement.
- Show order history, status and tracking.
- Support error states (payment failure, cancellation, retries).

## Scope
### Entry
- **8.0 Store index**: entry point from `(tabs)/store/index.tsx`; explainer and onboarding tips; hidden if the profile has no finished stories.
- **8.1 Store create order**: launches the checkout flow in `(main)`.
- **8.1.1 Store modal**: explains the product and what happens after ordering.

### Checkout Flow (stateful, single RN route in `(main)`)
- **8.2 Select product**
  - Select a story (pre-loaded if launched from story detail). Only finished stories (`Done`); a story awaiting parental approval can't be ordered (`STORY_AWAITING_APPROVAL`).
  - Choose the product: **A4 landscape paperback** or **A4 landscape hardback** (SKU-level, [[make-store-orders-sku-based-and-draft-only-editable]]).
  - Prices from Xano (`products.amount`, pence), [[verify-stripe-checkout-totals-against-xano-prices]].
- **8.2.1 Select shipping**
  - Options from `shipping_options` (standard = Royal Mail 48 Tracked, express = Royal Mail 24 Tracked).
  - Name, address, phone and email with native autofill.
  - Optional gift message (`store_orders.message`, buyer's message only), **printed on the book's first page**. Editable until payment (the order is Draft); it's shown again in the preview so it can be checked before paying.
- **8.2.2 Preview**: the e-reader in preview mode with the cover, the **gift message on the first page** (where it's printed), and every story page ([[use-e-reader-preview-before-order-payment]]). Copy states the book is personalised and can't be cancelled once in production.
- **8.2.3 Payment**
  - Order summary (server-derived totals): product, shipping, and the **Creator discount (25%) as its own line**.
  - `GET /stripe/create_checkout_session` → Stripe Checkout in an in-app browser sheet; the sheet closes itself on the app-scheme redirect ([[return-from-stripe-checkout-via-in-app-browser-sheet]]).
- **8.2.4 Confirmation**: in-app confirmation screen; `GET /stripe/check_order_paid` confirms payment.

### Order History
- **8.4 Order history (index)**: the account's orders.
  - `status`: Draft, Payment Pending, Payment Confirmed, Order Confirmed, In Production, Shipped, Cancelled, Error.
  - `payment_status`: Pending, Confirmed, Refunded, Cancelled, Error.
- **8.4.1 Order detail**: status timeline (from `store_order_updates`), tracking link and number once shipped, and a **countdown** while the 30-minute cancel window is open (from `submit_after`).
- **8.4.2 Payment failure**: retry from the order (it stays Draft / Payment Pending).
- **8.4.3 Cancellation**: within 30 minutes of payment (1 minute for test users) and before submission to print, cancel → automatic full refund. After that, cancellation is closed; misprints and quality issues go through support ([[split-refund-model-into-self-service-and-support-paths]]).
- **Changing the gift message after paying:** not editable once paid (the print PDFs are made straight after payment). Inside the cancel window the customer can cancel (full refund) and order again with the new message; the order page says so.

## Data Model (Xano, live)
- **products**: SKU-level catalogue (`amount` in pence, `size`, `orientation`, `Type` = physical-product, print specification, HPBC SKUs, Papermill templates).
- **shipping_options**: `name`, `description`, `amount` (pence).
- **store_orders**: user, story, product, shipping, totals (`subtotal`, `shipping_amount` in pence), status, payment status, `submit_after`, `cancelled_at`, PDFs, `hpbc_order_id`, tracking.
- **store_order_updates**: status history from HPBC callbacks (embedded in order detail).
- **transactions**: payment and refund records (money only).

## Endpoints (`app` group)
`GET /products`, `GET /shipping_options`, `POST /store_orders`, `PATCH /store_orders/{id}` (Draft only), `GET /store_orders`, `GET /store_orders/{id}`, `POST /store_orders/{id}/cancel`, `GET /stripe/create_checkout_session`, `GET /stripe/check_order_paid`. Error codes: `STORY_AWAITING_APPROVAL`, `ORDER_NOT_PAYABLE`, `ORDER_NOT_CANCELLABLE` (all 400).

## Backend Flow
1. The app creates the order (Draft) and patches product, shipping and address; totals are derived on the server.
2. `create_checkout_session` checks ownership, parental approval and order status, builds the Stripe session from Xano prices and checks Stripe's total.
3. On payment, the Stripe webhook confirms the order, records the transaction, starts PDF generation and sets `submit_after` (+30 min).
4. `hpbc_submit_due_orders` submits due orders to HPBC/Pureprint.
5. HPBC callbacks move the order forward (Order Confirmed → In Production → Shipped, or Error) and store tracking.
6. The app polls order detail; in-app alerts announce key changes.

Full detail: [[order-fulfilment-flow]], [[order-cancellation-and-refund-flow]].

## Technical Considerations
- **Autofill:** RN `TextInput` with `autoComplete` + `textContentType`.
- **Errors:** payment failure → retry; HPBC rejection → order `Error`, handled by support.
- **Notifications:** in-app alert and email (Resend) for **order confirmed**, **shipped** (with tracking) and **cancelled/refunded**. No email when the cancel window closes (the countdown covers it). No push in V1.
- **Offline:** orders cached in Zustand for viewing.
- **Purchases from a child profile:** checkout only from a parent profile (see [[PRD-Profiles]] open question on PIN for purchases).

## Out of Scope (V1)
- Library orders (8.3 series).
- Teacher/classroom publishing.
- Ratings/sharing of stories.
- Manual order submission (backend automation only).
- Push notifications.

## Pricing rules
- Prices from `products.amount` and `shipping_options.amount` (pence).
- **Creator:** 25% off the book (not shipping), applied on the server before the Stripe session and shown as a line.
- **Club (V2):** its monthly book at £0 with free standard shipping, and £0 orders that skip Stripe, move to V2 with Club ([[v2-backlog]]).

## Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** the full order flow (endpoints above), `transactions`, webhooks, cancel and refund, `hpbc_submit_due_orders`.

**To build:**
1. **Parent-only:** every store endpoint refuses a child profile (400 `PARENT_PROFILE_REQUIRED`).
2. **Products:** A4 landscape paperback and hardback records with live and test HPBC SKUs, Papermill templates and prices (pence).
3. **Discount:** price calculation reads `book_discount_pct` from the entitlements. Until M8 the tiers don't exist, so this ships with entitlements.
4. **Checkout return:** success/cancel URLs to the app scheme for the environment (or the forwarding page), [[return-from-stripe-checkout-via-in-app-browser-sheet]].
5. **Emails:** Resend templates for confirmed, shipped (tracking) and cancelled/refunded, sent from the existing status changes; matching in-app alerts.
6. **Clean-up:** remove `store_orders.checkout_session_object` (still in the schema although [[record-transactions-drop-checkout-session-object]] dropped it).
7. **Pre-launch:** new sign-ups get `test_mode = false` ([[pre-launch-checklist]]).
8. **Postman `_tests`:** child refused; discount line correct; emails triggered (check the alerts).

## Open Questions
None. Resolved 29/10: the gift message is printed on the book's first page. Club (monthly £0 book, free standard shipping, 25% off) moved to V2 with the Subscriptions review.
