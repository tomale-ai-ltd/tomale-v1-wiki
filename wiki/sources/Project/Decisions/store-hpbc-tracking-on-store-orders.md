---
type: source
origin: user-note
date: 2026-10-14
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/store-hpbc-tracking-on-store-orders.md

This document outlines the decision to store tracking data from the HPBC Shipped callback in the store_orders database, detailing the implementation and rationale behind it.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]
- [[hpbc|HPBC]]
- [[pureprint|Pureprint]]

## Concepts

- [[storeorders|store_orders]]
- [[tracking-fields|tracking fields]]
