---
type: decision
title: use-e-reader-preview-before-order-payment
project: tomale-rn-v1
status: accepted
date: 2026-10-28
related:
  - "[[v1-audit]]"
  - "[[disallow-cancelling-personalised-orders-once-in-production]]"
affects:
  - PRD-Store-Orders
features:
  - F-store
  - F-bookshelf
---

# Decision: use-e-reader-preview-before-order-payment

## What we decided

The preview a customer approves before paying is the e-reader showing the story they built, with page swipe or scroll. It includes the cover image and the gift message (`store_orders.message`).

## Why

[[disallow-cancelling-personalised-orders-once-in-production]] relies on the customer approving a preview before paying (the personalised-goods exemption). The story already exists in the app, so the e-reader is the natural preview.

## Trade-offs accepted

The preview shows the story as built, not a rendering of the print PDF.

## Related notes

- [[v1-audit]] (P5)
- [[restrict-store-orders-message-to-buyer-gift-message]]
