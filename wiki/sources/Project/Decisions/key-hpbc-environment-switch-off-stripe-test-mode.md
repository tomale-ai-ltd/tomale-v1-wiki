---
type: source
origin: user-note
date: 2026-10-12
tags:
  - llm-wiki/source
aliases: []
cssclasses: []
---


# Project/Decisions/key-hpbc-environment-switch-off-stripe-test-mode.md

This document outlines a decision regarding the management of the HPBC/Pureprint environment by switching off the Stripe `test_mode` flag to prevent mismatched payment states.

## Entities

- [[tomale-v1|Tomale V1]]
- [[stripe|Stripe]]
- [[hpbc|HPBC]]
- [[pureprint|Pureprint]]
- [[alex|Alex]]

## Concepts

- [[testmode-flag-management|test_mode flag management]]
