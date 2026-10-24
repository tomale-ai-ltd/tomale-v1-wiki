---
type: source
origin: user-note
date: 2026-07-16
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/adopt-unique-index-dedup-for-webhook-ingest.md

This document outlines the decision to implement a unique index for deduplication of webhook events in the Tomale RN V1 project.

## Entities

- [[xano|Xano]]
- [[stripe|Stripe]]
- [[tomale-rn-v1|Tomale-rn-v1]]
- [[hpbc|HPBC]]

## Concepts

- [[deduplication-mechanism|Deduplication Mechanism]]
- [[insert-and-catch-pattern|Insert-and-Catch Pattern]]
