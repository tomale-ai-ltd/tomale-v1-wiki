---
type: decision
title: disallow-cancelling-personalised-orders-once-in-production
project: tomale-rn-v1
status: accepted
date: 2026-10-14
---

---

# Decision: disallow-cancelling-personalised-orders-once-in-production

## What we decided

Customers cannot cancel a personalised order once it is in production. The customer approves a web-view preview before paying, and checkout states that orders cannot be cancelled once in production. This relies on the Consumer Contracts Regulations 2013 reg. 28(1)(b) exemption for personalised goods.

## Why

Pureprint's Order Print Ready step is batched and cannot be backed out, and the books are personalised, so the personalised-goods exemption removes the right to cancel after production starts.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Accepted risk: the customer's approval is based on the web view, not the final PDF. The terms wording still needs checking against the regulation.

## Workflow detail

Cancellation is only available within the pre-submission window (`cancellable` flag on `GET /store_orders/{id}`; `POST /store_orders/{id}/cancel` enforces the conditions). Terms and checkout wording need review.

## Related notes

- [[delay-hpbc-submission-with-30-minute-cancellation-window]]
- [[automate-full-refund-on-self-service-cancel]]
- [[2026-10-14-001]]
