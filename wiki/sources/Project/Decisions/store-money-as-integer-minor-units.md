---
type: source
origin: user-note
date: 2026-07-20
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/store-money-as-integer-minor-units.md

This document outlines the decision to store monetary values as integers paired with currency in the transactions table to avoid float rounding errors.

## Entities

- [[stripe|Stripe]]
- [[tomale|Tomale]]

## Concepts

- [[float-precision-rationale|Float Precision Rationale]]
