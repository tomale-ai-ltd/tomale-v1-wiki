---
type: decision
title: enforce-strict-env-validation-at-startup
project: tomale-rn-v1
status: accepted
date: 2026-05-15
features:
  - X-platform
---

# Decision: enforce-strict-env-validation-at-startup

## What we decided

All `EXPO_PUBLIC_*` env reads go through a single source of truth: `config/env.ts`. The module performs strict validation at startup and **throws** if any required variable (currently `EXPO_PUBLIC_API_BASE_URL`) is missing — in every environment, dev included. No hardcoded fallback URLs anywhere in the codebase.

Non-secret `EXPO_PUBLIC_*` values live in `eas.json` (version-controlled, PR-reviewable) with per-profile blocks for `development`, `preview`, and `production` — set up now even though all three currently point at the same Xano URL. The EAS dashboard is reserved for real secrets only.

A `scripts/check-env.mjs` preflight is wired into `npm run update:openapi` so misconfigured environments also fail fast at the tooling layer.

## Why

Silent fallbacks mask configuration drift between dev, preview, and prod — bugs surface late and look like unrelated app behavior. A loud startup failure forces misconfiguration to be fixed at the source. A single env-reading module makes it trivial to audit which variables the app actually depends on, and storing non-secret config in `eas.json` keeps it reviewable in PRs rather than mutable through a dashboard. Setting up per-profile env blocks now — at zero current cost — leaves the dev/prod Xano split queued in Phase 2 §1 of the CTO plan as a config-only change later.

## Alternatives considered

- **Sensible hardcoded fallbacks** (e.g. fall back to a known dev Xano URL if env is missing). Rejected — exactly the silent-drift pattern this decision is meant to eliminate.
- **Warn-but-continue on missing env.** Rejected — warnings are easy to miss and the resulting app behavior is misleading.
- **EAS env config in the EAS dashboard rather than `eas.json`.** Rejected for non-secrets — dashboard values aren't PR-reviewable or reproducible. Dashboard reserved for actual secrets.
- **Per-module env reads with their own validation.** Rejected — fragments the contract and makes auditing harder.

## Trade-offs accepted

- Developers who clone the repo without a `.env` get an immediate startup failure. Mitigated by `.env.example` and the updated env matrix in `README.md`.
- Any new `EXPO_PUBLIC_*` variable now requires a corresponding update in `config/env.ts`, `.env.example`, the README matrix, and the `eas.json` profile blocks. Small bookkeeping cost.

## Workflow detail

`api/http.ts` was refactored to read its base URL via `config/env.ts`; the previous hardcoded fallback URL is gone. The `eas.json` env blocks for `development`, `preview`, and `production` all currently point at the same Xano workspace; when the dev/prod split lands, only those values change. `scripts/check-env.mjs` runs as a preflight to `npm run update:openapi`, alongside the new guardrails that prevent HTML/error responses from silently overwriting `api/openapi/xano.yaml`.

## Related notes

- [[consolidate-xano-api-groups-into-app-and-webhooks]]
- [[use-https-web-intermediary-for-magic-link-redirect]]
- [[separate-dev-prod-environments]]
