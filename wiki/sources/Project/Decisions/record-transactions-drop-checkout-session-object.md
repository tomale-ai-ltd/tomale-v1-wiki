---
type: source
origin: user-note
date: 2026-07-20
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/record-transactions-drop-checkout-session-object.md

This document outlines the decision to restructure the payment processing system by recording payment facts in a dedicated transactions table instead of using a raw checkout session object.

## Entities

- [[stripe|Stripe]]
- [[tomale|Tomale]]

## Concepts

- [[transactions-table|transactions table]]
- [[checkoutsessionobject|checkout_session_object]]
