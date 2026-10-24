---
type: decision
title: "adopt-openapi-import-for-postman-collection-sync"
date: 2026-06-30
status: current
project: tomale-rn-v1
---

---

# Decision: adopt-openapi-import-for-postman-collection-sync

## What we decided

Keep the Postman collection in sync with Xano via OpenAPI import/merge from Xano's Swagger export, rather than maintaining the collection by hand.

## Why

Xano's Swagger export makes Postman collection maintenance ~free via OpenAPI import/merge — the same pattern already used for the frontend's `xano.yaml` sync, at roughly 15 minutes of setup.

## Alternatives considered

Manually maintaining the Postman collection was the implicit alternative — rejected given the near-zero cost of the OpenAPI import/merge approach.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Postman collection maintenance follows the same OpenAPI-sync pattern as the frontend's `xano.yaml` sync: export Swagger/OpenAPI from Xano, import/merge into Postman as needed (~15 min setup).

## Related notes

- [[Sessions/2026-06-30-001]]
