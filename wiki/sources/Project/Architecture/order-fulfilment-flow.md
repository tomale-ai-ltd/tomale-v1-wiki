---
type: source
origin: user-note
date: 2026-10-15
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Architecture/order-fulfilment-flow.md

This document outlines the order and fulfilment flow for the Tomale project, detailing the lifecycle of a store order from creation to payment and submission to HPBC (Pureprint). It includes a flowchart and discusses various statuses and error handling mechanisms.

## Entities

- [[stripe|Stripe]]
- [[papermill|Papermill]]
- [[tomale|Tomale]]
- [[tomale-rn-v1|Tomale-rn-v1]]
- [[storeorders|store_orders]]
- [[hpbc|HPBC]]

## Concepts

- [[order-fulfilment-flow|Order Fulfilment Flow]]
- [[idempotency-guards|Idempotency Guards]]
- [[status-vocabulary|Status Vocabulary]]
- [[order-status|Order Status]]
