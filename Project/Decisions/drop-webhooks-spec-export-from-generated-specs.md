---
type: decision
title: drop-webhooks-spec-export-from-generated-specs
project: tomale-rn-v1
status: accepted
date: 2026-10-28
related:
  - "[[2026-10-28-002]]"
  - "[[2026-10-24-001]]"
  - "[[generate-data-model-and-api-contract-from-xano]]"
  - "[[follow-knowledge-architecture-stage-order-before-slice-100]]"
affects:
  - "[[knowledge-architecture]]"
  - "xano.yaml"
features:
  - X-process
---

# Decision: drop-webhooks-spec-export-from-generated-specs

## What we decided

The `webhooks` OpenAPI spec export is dropped from B6 (generated specs). Only the `app` group spec is refreshed into the app repo with `npm run update:openapi`.

## Why

Postman already holds the `webhooks` spec, and the XanoScript mirror is the source for those endpoints.

## Alternatives considered

Exporting the `webhooks` spec as part of B6, as listed in the stage order agreed on 24/10 ([[follow-knowledge-architecture-stage-order-before-slice-100]]).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

B6 closed without a `webhooks` export. Anyone needing the webhook endpoint contracts uses Postman or the XanoScript mirror (`tomale-xano`), not a generated spec in `tomale-rn-test`.

## Related notes

- [[2026-10-28-002]]
- [[2026-10-28-001]]
- [[2026-10-24-001]]
- [[generate-data-model-and-api-contract-from-xano]]
- [[follow-knowledge-architecture-stage-order-before-slice-100]]
- [[mirror-xano-workspace-to-github-read-only]]
- [[knowledge-architecture]]
