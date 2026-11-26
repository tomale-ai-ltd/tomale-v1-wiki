---
date: 2026-11-26
source: cursor
branch: chore/foundation
feature: IP-04 PR A foundation
---

# IP-04 PR A: tomale-image-gateway repo foundation

## What changed
- Opened https://github.com/tomale-ai-ltd/tomale-image-gateway/pull/1 on `chore/foundation` (6 commits, one per brief bullet).
- Guard rails from rn-test plus Terraform/cloud deny and plan/init ask; `tests/guard/` pytest cases.
- `.cursor/rules/tomale-gateway.mdc`; Spec Kit copy from rn-test `@05f27b1`; constitution v1.0.0; uv/Python 3.13 tooling; CI `test` (Gitleaks, ruff, pytest, OpenAPI lint skip-if-empty).
- `gh pr checks`: **test pass**.

## Decisions
- Cursor treated `bq show` as not read-only under the brief’s describe/list/get allowlist (allow cases use `bq ls` / `--help` only).
- Redocly chosen for OpenAPI lint; skipped when `contracts/` is empty.
- Minimal `src/tomale_image_gateway` package so hatchling/`uv sync` works before IP-09 service code.

## Open questions / blockers
- Kyle: after merge, add `test` as a required status check on `protect-main`.
- PR B (spec/contract/ADRs) not started — stop per brief after PR A green.

## Next
- Kyle reviews/merges PR #1; then IP-04 PR B (`001-image-gateway`) per the same brief.
