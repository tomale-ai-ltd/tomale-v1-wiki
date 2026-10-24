---
type: source
origin: user-note
date: 2026-07-16
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/ack-unknown-webhook-event-types-with-200.md

This document outlines a decision regarding the handling of unrecognized webhook event types, specifying that they will be acknowledged with a 200 response to prevent retry storms from providers like Stripe.

## Entities

- [[tomale-v1|Tomale V1]]
- [[stripe|Stripe]]

## Concepts

- [[webhook-event-handling|Webhook Event Handling]]
