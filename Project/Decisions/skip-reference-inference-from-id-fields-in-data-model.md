---
type: decision
title: skip-reference-inference-from-id-fields-in-data-model
project: tomale-rn-v1
status: proposed
date: 2026-10-28
related:
  - "[[2026-10-28-001]]"
  - "[[generate-data-model-and-api-contract-from-xano]]"
  - "[[embed-domain-map-in-data-model-generator]]"
affects:
  - data-model
  - "scripts/update-data-model.mjs"
features:
  - X-process
---

# Decision: skip-reference-inference-from-id-fields-in-data-model

## What we decided

The data-model generator (`npm run update:datamodel`) does not infer table references from `_id` field names. References are left out of the generated Notes column.

## Why

The Xano Metadata API schema response for `_id` fields carries no target-table metadata, so any reference would be a guess from the field name.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

The generated data model doesn't show references between tables (logged as an open point in [[2026-10-28-001]]).

## Workflow detail

Part of B6 on branch `b6/generated-specs`, PR #9, awaiting Kyle's review.

## Related notes

- [[2026-10-28-001]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[embed-domain-map-in-data-model-generator]]
- [[protect-speckit-and-generated-spec-documents]]
- [[knowledge-architecture]]
