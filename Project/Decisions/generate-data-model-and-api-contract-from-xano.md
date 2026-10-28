---
type: decision
title: generate-data-model-and-api-contract-from-xano
project: tomale-rn-v1
status: accepted
date: 2026-10-23
related:
  - "[[knowledge-architecture]]"
features:
  - X-process
---

# Decision: generate-data-model-and-api-contract-from-xano

## What we decided

The API contract and data model are generated from Xano, never hand-written. API: `npm run update:openapi` (existing) fetches the private `app` group spec (`apispec:1pgd39RE`) into `api/openapi/xano.yaml` and regenerates `api/client.ts`. Data model: a new `npm run update:datamodel` script (built by Cursor) reads the Xano Metadata API with a read-only token and writes `.specify/memory/data-model.md`. The hand-written `api-spec.md` is retired.

## Why

`api-spec.md` and `data-model.md` were the docs that drifted worst (e.g. `user_child_profiles`, decimal money). Generated output can't drift from the backend.

## Alternatives considered

Keep hand-maintaining both docs during each session (rejected: it has already failed).

## Trade-offs accepted

Uses the existing read-only `cursor-read` Metadata token (database read scope confirmed) in a gitignored `.env`. Scripts must be run after backend changes. The data-model script is built and run in B6, before the canonical docs are written (B8), so they're written from current specs.

## Workflow detail

After an `app` endpoint change: `npm run update:openapi`. After a schema change: `npm run update:datamodel`. Commit the output in Cursor.

## Related notes

- [[knowledge-architecture]]
- [[2026-10-23-001]]
- [[adopt-repo-vault-ownership-split-for-project-knowledge]]
- [[adopt-tiered-vault-structure-with-canonical-folder]]
- [[adopt-frontmatter-lifecycle-schema]]
- [[add-propose-only-reconcile-and-staleness-automations]]
- [[retire-obsidian-llm-wiki-plugin]]
- [[scope-agent-context-per-tool]]
- [[version-the-vault-with-git]]
- [[defer-postman-suite-ci-until-suite-split]]
