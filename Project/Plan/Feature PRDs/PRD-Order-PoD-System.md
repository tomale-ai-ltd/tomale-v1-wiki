# **MICRO-PRD: Order & Print-on-Demand System**

## **Goal**

Allow users to **safely order bespoke illustrated books** without incurring unrecoverable costs before payment.

---

## **Scope**

Covers:

* Book ordering flow

* Payment handling

* Image generation gating

* Print job creation

* Refund / regeneration policy enforcement

---

## **Non-Goals**

* Bulk orders

* Returns logistics

* Customer support tooling (later)

---

## **Core Principle**

**No irreversible cost before payment or entitlement consumption.**

---

## **Backend Requirements**

### **Data Models**

#### **`orders`**

* `id`

* `user_id`

* `status` (`draft`, `paid`, `rendering`, `ready`, `sent_to_print`, `completed`)

* `book_format` (`paperback`, `hardback`)

* `price_paid`

* `discount_applied`

* `payment_id`

---

#### **`order_assets`**

* `order_id`

* `story_id`

* `image_job_ids`

* `print_ready_pdf_url`

---

#### **`payments`**

* `provider_payment_id`

* `status`

* `amount`

* `refundable_amount`

---

### **Order State Machine (Strict)**

`DRAFT`  
  `→ PAID`  
    `→ RENDERING (image generation)`  
      `→ READY (preview)`  
        `→ SENT_TO_PRINT`  
          `→ COMPLETED`

No skipping states.

---

### **Image Generation Rules (Backend)**

* Images are generated **only after**:

  * Payment success OR

  * Included book entitlement is consumed

* Regeneration attempts are capped:

  * e.g. `max_regenerations = 1`

* Regeneration consumes:

  * Another entitlement OR

  * Explicit confirmation

---

### **Refund Policy Logic**

* Image generation fee: **non-refundable**

* Printing fee: refundable **until SENT\_TO\_PRINT**

* Refunds automatically block further regeneration

---

## **Frontend Requirements**

### **Order UX Flow**

1. Create text story (free)

2. Click **“Order illustrated book”**

3. Checkout screen:

   * Clear pricing

   * Explicit bespoke disclaimer

4. Payment confirmation

5. Status screen:

   * “Generating illustrations…”

6. Preview screen:

   * Approve

   * Regenerate (if allowed)

7. Confirm print

---

### **Mandatory Copy (UX)**

“This book is made just for your child. Illustrations are generated after payment and can’t be refunded, but you’ll have one chance to request changes.”

This is not optional.

---

### **Failure States**

* Payment succeeds, image generation fails → retry automatically

* Image generation fails repeatedly → support fallback

* User abandons after payment → auto-continue to preview

---

## **Acceptance Criteria**

* No unpaid image generation is possible

* Orders cannot reach `RENDERING` without payment or entitlement

* Refunds cannot occur after print submission

* Every printed book has a traceable order \+ payment

