---
type: living-doc
title: CURRENT
project: tomale-rn-v1
status: draft
version: 0.1
date: 2026-10-24
last_verified: 2026-10-24
owner: vault
---

# CURRENT: where Tomale V1 stands

> **Stub (B4).** Written properly in B8. Start here: this page links out to everything else.

## Phase
- Phase 1 (Security & Data Integrity) **signed off 2026-10-23** (86/86 `_tests`). See [[6-api-security-model]].
- **Now:** knowledge restructure, per [[knowledge-architecture]] (B0–B4 done; next B5–B12), then the frontend resumes at **Slice 100 (Characters)**, which will be speckit feature **007**.

## Critical path to Slice 100
1. Generated specs: `update:datamodel` (new) and `update:openapi` (B6, in Cursor)
2. Constitution amendment and Cursor rules (B10, via [[repo-sync]])
3. pnpm migration and dependency audit ([[promote-pnpm-migration-ahead-of-slice-100]])
4. `PRD-Characters` reconciled; `v1-feature-map` row; this page written
5. Decide what from `wip/pre-restructure-2026-10-24` goes to `main`, then start `007-*` from `main`

## Where things are
- How knowledge works: [[knowledge-architecture]] · How we work: [[operating-model]]
- Stack overview: [[stack]] · Observability: [[observability]]
- Roadmap: [[2-build-plan]] (becomes `roadmap.md` in B8) · Remaining CTO phases: [[5-cto-implementation-plan]]
- PRDs: `Canonical/prd/` · Architecture flows: `Canonical/architecture/`
- Repo specs (read-only): `Repos/tomale-rn-test/` · Published backend code: `Repos/tomale-xano/`
- Queues: [[repo-sync]] · [[pending-updates]]
