---
type: decision
title: gate-image-generation-with-entitlements-at-story-creation
project: tomale-rn-v1
status: accepted
date: 2026-10-28
related:
  - "[[v1-audit]]"
  - "[[PRD-Subscription-Entitlement-System]]"
affects:
  - PRD-Order-PoD-System
  - PRD-Subscription-Entitlement-System
  - image_jobs
  - roadmap
features:
  - F-subscriptions
  - F-story-generation
  - F-store
---

# Decision: gate-image-generation-with-entitlements-at-story-creation

## What we decided

Stories, including their illustrations, are created in the app before any order. Tomale is a creative and reading app first; subscriptions and printed books are additional income. Because we can offer neither unlimited image generation nor image generation after payment, **entitlements limit story and image generation**. They also encourage paid subscriptions and make pre-purchase previews possible.

The preference is to **launch with subscriptions** (and so the entitlement system). Launching without them is possible but depends on the ratio of stories created to books ordered and on profitability. The final call comes after the roadmap is sized in B8.

## Why

The PoD PRD's "images only after payment" contradicts the product: the illustrated story is what the child creates and reads. Unlimited free generation isn't affordable.

## Alternatives considered

- Generate images only after payment (PoD PRD): rejected, as it breaks the creative loop.
- Unlimited generation: rejected on cost.

## Trade-offs accepted

The entitlement system becomes launch-critical backend work. It does not exist in Xano yet.

## Related notes

- [[v1-audit]] (P1, P2)
- [[defer-image-pipeline-throughput-to-phase-2]]
- [[return-full-artwork-catalogue-with-locked-tiles]]
