---
type: source
origin: user-note
date: 2026-10-12
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/run-real-fulfilment-cascade-against-staging-sku.md

This document outlines the decision to run the real fulfilment cascade against a staging SKU instead of simulating the HPBC callback due to the lack of a sandbox environment.

## Entities

- [[tomale-rn-v1|Tomale-rn-v1]]
- [[hpbc|HPBC]]
- [[pureprint|Pureprint]]
- [[alex|Alex]]

## Concepts

- [[order-fulfilment-flow-test|Order-fulfilment flow-test]]
