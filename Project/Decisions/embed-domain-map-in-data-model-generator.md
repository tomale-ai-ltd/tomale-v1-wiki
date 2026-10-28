---
type: decision
title: embed-domain-map-in-data-model-generator
project: tomale-rn-v1
status: proposed
date: 2026-10-28
related:
  - "[[2026-10-28-001]]"
  - "[[generate-data-model-and-api-contract-from-xano]]"
  - "[[skip-reference-inference-from-id-fields-in-data-model]]"
affects:
  - data-model
  - "scripts/update-data-model.mjs"
features:
  - X-process
---

# Decision: embed-domain-map-in-data-model-generator

## What we decided

A `DOMAIN_MAP` embedded in `scripts/update-data-model.mjs` sets each table's domain grouping and table-type classification in the generated data model.

## Why

Grouping and classification are explicit and get reviewed in code.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Classifications are confirmed in PR review. Open for Kyle in PR #9: `products` and `shipping_options` (Commerce, `user_data`); `support_requests` (Locale & Misc, `system_or_reference`); `blocked_terms` (Moderation & Safety); `audit_store_orders` (Commerce & Orders). The map also reflects live schema drift: `user_profiles` replaces the old expected `user_child_profiles`, and `blocked_terms` and `audit_store_orders` are included.

## Related notes

- [[2026-10-28-001]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[skip-reference-inference-from-id-fields-in-data-model]]
- [[add-temporary-audit-trigger-on-store-orders]]
- [[knowledge-architecture]]
