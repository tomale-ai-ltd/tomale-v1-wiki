---
type: source
origin: user-note
date: 2026-10-15
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/add-temporary-audit-trigger-on-store-orders.md

This document outlines the decision to add a temporary audit trigger on store orders to diagnose issues related to the `created_at` field in the database.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]
- [[auditstoreorders|audit_store_orders]]
- [[auditstoreorderschanges|audit_store_orders_changes]]

## Concepts

- [[phase-2-observability-work|Phase 2 observability work]]
