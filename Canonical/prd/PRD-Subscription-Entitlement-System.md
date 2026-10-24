---
type: prd
title: PRD-Subscription-Entitlement-System
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-04-14
last_verified: 2026-04-14
owner: vault
---

# **MICRO-PRD: Subscription & Entitlement System**

## **Goal**

Provide a **tiered subscription system** that controls access to cost-incurring features (image generation, included books, discounts) without coupling business logic to plan names.

---

## **Scope**

Covers:

* Subscription tiers (Free, Creator, Club)

* Trial handling

* Entitlement resolution

* Metering & limits

* Billing state reconciliation

---

## **Non-Goals**

* Pricing experiments

* Discount campaigns

* Education / enterprise tiers (future)

---

## **Core Concepts (non-negotiable)**

* **Plans ≠ logic**

* **Entitlements drive behaviour**

* **Image generation requires entitlement OR payment**

* **Trials are overlays, not plans**

---

## **Backend Requirements**

### **Data Models**

#### **`subscriptions`**

* `id`

* `user_id`

* `tier` (`creator`, `delivery`)

* `status` (`active`, `paused`, `cancelled`)

* `current_period_start`

* `current_period_end`

* `provider_subscription_id`

---

#### **`entitlements`**

Key–value store, resolved at runtime.

Examples:

* `can_generate_text` (bool)

* `can_generate_images` (bool)

* `monthly_included_books` (int)

* `book_discount_pct` (int)

* `trial_active` (bool)

---

#### **`usage_counters`**

Reset monthly.

* `images_generated_count`

* `included_books_used`

* `books_purchased_count`

---

#### **`trial_state`**

* `trial_started_at`

* `trial_ends_at`

* `trial_consumed` (bool)

* `trial_books_used`

---

### **Entitlement Resolution Logic**

**At request time:**

`effective_entitlements =`  
  `base_entitlements`  
  `+ subscription_entitlements`  
  `+ trial_entitlements (if active)`

Never read plan names directly in feature logic.

---

### **Hard Rules (Backend)**

* Image generation **MUST fail closed** if entitlement is missing

* Usage counters **increment before job execution**

* Trial can only be consumed once per user (forever)

* Billing provider is source of truth

* Entitlements reconciled daily via webhook \+ cron

---

## **Frontend Requirements**

### **Subscription UX**

* Clear comparison of:

  * Creator (£6.99)

  * Book Delivery (£20)

* Explicit explanation of:

  * What is included

  * What costs extra

* Trial messaging:

   “One free book during your trial. Cancel anytime before printing.”

---

### **User State Display**

* Current tier

* Remaining included books

* Trial countdown (if active)

* Clear CTAs:

  * “Upgrade”

  * “Order book”

  * “Buy delivery subscription”

---

### **Edge Cases (Frontend)**

* Payment failed → downgrade entitlements immediately

* Trial expired → lock image generation

* Grace period → allow reading, block images

---

## **Acceptance Criteria**

* No image job can run without entitlement or payment

* Trial cannot be restarted

* Cancelling subscription removes future entitlements, not access to purchased content

* Subscription tier changes do not require code changes  
* V1 subscriptions and entitlements must support app store / play store IAP checkout.

```json
{
  "source": "apple | google | stripe"
}

```

Frontend behaviour remains identical, but important to know.

UX Flow:

When user hits limit:

1. Show:

    “You’ve reached your limit. Upgrade to continue.”

2. CTA:  
   * iOS → Apple IAP  
   * Android → Google Play Billing  
3. Backend:  
   * receives webhook / purchase validation  
   * updates `subscriptions`

# **`🔧 ADDITION 1 — Entitlements Schema (strict structure)`**

## **`New Section: Entitlement Schema (Required)`**

`All entitlements MUST conform to a strict schema.`  
 `No dynamic or untyped key-value access is allowed in application logic.`

### **`Schema (V1)`**

```json
{
 "can_generate_text": "boolean",
 "can_generate_images": "boolean",
 "monthly_included_books": "integer",
 "book_discount_pct": "integer",
 "trial_active": "boolean"
}
```

### **`Rules`**

* `All fields must have defaults`  
* `Missing fields must fail validation`  
* `No feature logic may reference undefined keys`  
* `Entitlements must be versionable (future-proofing)`

---

# **`🔧 ADDITION 2 — Entitlements API`**

## **`New Section: Entitlements API`**

### **`Endpoint`**

`GET /me/entitlements`

### **`Response`**

```json
{
 "plan": "free | creator | delivery",
 "status": "active | trial | past_due | cancelled",
 "source": "apple | google | stripe",
 "entitlements": {
   "can_generate_text": true,
   "can_generate_images": false,
   "monthly_included_books": 1,
   "book_discount_pct": 0
 },
 "usage": {
   "images_generated_count": 12,
   "included_books_used": 1
 },
 "limits": {
   "monthly_included_books": 1
 },
 "remaining": {
   "included_books": 0
 },
 "trial": {
   "active": true,
   "ends_at": "timestamp"
 }
}
```

### **`Rules`**

* `This endpoint is the single source of truth for frontend gating`  
* `Frontend must NOT compute entitlements locally`  
* `All UI gating must rely on this response`

---

# **`🔧 ADDITION 3 — Entitlement Gate (Core Backend Logic)`**

## **`New Section: Entitlement Gate`**

`All cost-incurring or restricted actions MUST pass through a centralized entitlement check.`

### **`Interface`**

```json
{
 "action": "generate_image | generate_story | order_book",
 "result": {
   "allowed": true,
   "reason": null,
   "remaining": 12
 }
}
```

### **`Failure Example`**

```json
{
 "allowed": false,
 "reason": "limit_reached",
 "remaining": 0
}
```

### **`Rules`**

* `No job execution without passing entitlement gate`  
* `Gate must run BEFORE:`  
  * `image_jobs creation`  
  * `story generation`  
  * `PDF generation`  
* `Gate must return deterministic results (no partial state)`

---

# **`🔧 ADDITION 4 — Usage Counters (Explicit Rules)`**

## **`New Section: Usage Counter Behaviour`**

### **`Reset Rules`**

* `Reset frequency: calendar month (UTC)`  
* `Reset mechanism: cron job (daily check)`  
* `No rolling windows in V1`

---

### **`Increment Rules`**

* `Counters MUST increment before execution`  
* `If execution fails:`  
  * `V1: no rollback (simpler, acceptable)`  
  * `Future: retry-aware reconciliation`

---

### **`Edge Cases`**

| `Scenario` | `Behaviour` |
| ----- | ----- |
| `Upgrade mid-cycle` | `entitlements increase immediately, usage unchanged` |
| `Downgrade mid-cycle` | `entitlements reduce immediately, no refund of usage` |
| `Trial expiry` | `immediately remove trial entitlements` |
| `Payment failure` | `downgrade to free entitlements immediately` |

---

# **`🔧 ADDITION 5 — Entitlement Snapshotting`**

## **`New Section: Execution Snapshot`**

`At the moment of job execution, store entitlement state.`

### **`Example`**

```json
{
 "entitlement_snapshot": {
   "can_generate_images": true,
   "monthly_included_books": 1
 }
}
```

### **`Applies To`**

* `image_jobs`  
* `story generation`  
* `PDF generation`

### **`Purpose`**

* `auditability`  
* `debugging`  
* `consistency during race conditions`

---

# **`🔧 ADDITION 6 — Subscription State Model`**

## **`Update Section: subscriptions`**

`Add:`

`status:`

 `active`

 `trial`

 `past_due`

 `grace`

 `cancelled`

---

## **`New Rules`**

* `grace:`  
  * `allow reading existing content`  
  * `block new image/story generation`  
* `past_due:`  
  * `immediate restriction of cost-incurring features`  
* `cancelled:`  
  * `retain access until current_period_end`

---

# **`🔧 ADDITION 7 — Trial Abuse Prevention`**

## **`New Section: Trial Enforcement`**

### **`Rules`**

* `Trial may only be consumed once per user`  
* `Must enforce via:`  
  * `user_id`  
  * `AND secondary identifier (email)`

### **`Optional (future)`**

* `device fingerprint`  
* `payment method fingerprint`

---

# **`🔧 ADDITION 8 — Plan Independence Enforcement`**

## **`New Section: Plan Isolation Rule`**

`Application logic MUST NOT:`

* `check tier`  
* `check plan name`  
* `branch logic on subscription labels`

`All logic MUST rely on:`

`entitlements only`

---

# **`🔧 ADDITION 9 — Payment Source Abstraction`**

## **`New Section: Payment Source Handling`**

### **`Supported Sources`**

```json
{
 "source": "apple | google | stripe"
}
```

### **`Rules`**

* `Entitlements MUST NOT differ by source`  
* `Subscription resolution must be identical regardless of provider`  
* `Provider is only used for:`  
  * `reconciliation`  
  * `debugging`  
  * `reporting`

---

# **`🔧 ADDITION 10 — Backend Responsibility Boundary`**

## **`New Section: Responsibility Split`**

### **`Backend owns:`**

* `entitlement resolution`  
* `usage tracking`  
* `gating decisions`  
* `subscription reconciliation`

### **`Frontend owns:`**

* `display of entitlements`  
* `UX gating (based on API response)`  
* `triggering upgrade flows`

