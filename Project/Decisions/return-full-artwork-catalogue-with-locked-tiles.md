---
type: decision
title: return-full-artwork-catalogue-with-locked-tiles
project: tomale-rn-v1
status: accepted
date: 2026-05-08
related:
  - "[[2026-05-08-001]]"
  - "[[v1-audit]]"
affects:
  - artwork_style GET
features:
  - F-story-create
  - F-subscriptions
---

# Decision: return-full-artwork-catalogue-with-locked-tiles

## What we decided

`artwork_style` returns the whole catalogue whatever the user's tier. The app shows styles the user isn't entitled to as locked tiles (an upgrade prompt).

## Related notes

- [[2026-05-08-001]] (backfilled in B7)
- [[gate-image-generation-with-entitlements-at-story-creation]]
