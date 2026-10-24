---
type: living-doc
title: repo-sync
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-24
owner: vault
---

# Repo sync queue

Changes to protected specs in `tomale-rn-test`, applied by a Cursor agent **only once approved**, in batches between slices, on a `repo-sync/YYYY-MM-DD` branch with one PR per batch. Process and classes: [[operating-model]] §3.5. Protected documents: [[knowledge-architecture]] §6.

### RS-2026-10-24-01: Constitution amendment (V1 rules after Phase 1)
- Class: A
- Target: `.specify/memory/constitution.md`
- Change: client tokens in `expo-secure-store`, not AsyncStorage; a single Axios 401 interceptor (shared refresh, one retry, never for `/auth/*`; log out on `invalid_refresh_token`; network errors don't log out; proactive refresh on foreground); money in integer minor units (pence); error-code conventions (`STORY_AWAITING_APPROVAL`, `ORDER_NOT_PAYABLE`, `ORDER_NOT_CANCELLABLE`, 400 as Xano has no 422); backend schema procedure says `data-model.md` is generated (`npm run update:datamodel`), not hand-edited; "≥1 review" defined for a solo maintainer (Kyle's PR review); package manager is pnpm (after RS-03); `main` merges by squash or rebase (linear history ruleset)
- Source: [[use-expo-secure-store-for-client-tokens]], [[use-axios-401-interceptor-for-client-auth-session-handling]], [[store-money-as-integer-minor-units]], [[generate-data-model-and-api-contract-from-xano]], [[promote-pnpm-migration-ahead-of-slice-100]]
- Speckit impact: Constitution Check in every new plan; `/speckit.analyze` against any active spec (none active)
- Process: `/speckit.constitution` (Sync Impact Report, semver MINOR → 1.5.0), PR with migration notes
- Verify: Sync Impact Report present; templates consistent; `/speckit.analyze` clean on the first 007 spec
- Status: queued

### RS-2026-10-24-02: Data-model generator script
- Class: C (new script) / B (`package.json` script entry)
- Target: `scripts/update-data-model.mjs`, `package.json` (`update:datamodel`), `.specify/memory/data-model.md`
- Change: generate `data-model.md` from the Xano Metadata API (read-only `cursor-read` token in `.env`), same pattern as `update-openapi.mjs`
- Source: [[generate-data-model-and-api-contract-from-xano]]
- Speckit impact: none (the global data model isn't read by speckit commands; the constitution points to it)
- Process: Cursor builds and runs it; PR
- Verify: output matches live Xano tables (spot-check `store_orders` int pence, `user_profiles.is_primary`)
- Status: queued

### RS-2026-10-24-03: pnpm migration and dependency audit
- Class: B
- Target: `package.json`, lock file, CI workflow, `.npmrc`/`pnpm-workspace` settings
- Change: pnpm with install scripts blocked by default (allow only what needs them), `minimumReleaseAge: 7`, `pnpm audit` in CI failing on high and critical; review the 49 npm audit findings (dev-only exposure first); replace `@testing-library/jest-native` with built-in matchers
- Source: [[promote-pnpm-migration-ahead-of-slice-100]]
- Speckit impact: none
- Process: Cursor on its own branch; PR
- Verify: `pnpm install` clean; CI green; Expo app builds and runs
- Status: queued

### RS-2026-10-24-04: Cursor rule files
- Class: B
- Target: `.cursor/rules/tomale-project.mdc` (always), `.cursor/rules/tomale-api.mdc` (`api/**`), `.cursorignore` / `.cursorindexingignore`
- Change: short project rule (stack, conventions, pointers to `CURRENT.md` and the constitution, raw session notes to the vault, never edit protected docs outside their process); API rule (`client.ts` types only; contracts come from `xano.yaml`; any new endpoint is a backend change request; 401 rules; pence); keep `node_modules`, `dist`, `ios` build out of the index
- Source: [[scope-agent-context-per-tool]], [[operating-model]] §0
- Speckit impact: none
- Process: Cursor edit; PR
- Verify: rules visible in Cursor settings with the right attach mode
- Status: queued

### RS-2026-10-24-05: `specify-rules.mdc` one-off cleanup
- Class: B (one-off; the file is otherwise never edited)
- Target: `.cursor/rules/specify-rules.mdc`
- Change: remove the stale "AsyncStorage for auth token" lines and the unfilled template placeholders from "Active Technologies" / "Commands". The agent-context script only appends, so the cleanup sticks. Check whether Cursor loads this file at all (no frontmatter).
- Source: [[knowledge-inventory]] finding 1
- Speckit impact: none
- Process: Cursor edit; PR
- Verify: next `/speckit.plan` appends cleanly
- Status: queued

### RS-2026-10-24-06: speckit `.specify.specify/` path bug
- Class: decision needed (speckit tool files)
- Target: `.cursor/commands/speckit.plan.md`, `speckit.tasks.md`
- Change: either upgrade speckit to a current release (re-check the templates and commands afterwards) or make a recorded one-line path correction
- Source: [[knowledge-inventory]] finding 1
- Speckit impact: `/speckit.plan` and `/speckit.tasks` load the constitution and the tasks template reliably
- Process: Kyle decides; then Cursor
- Verify: `/speckit.plan` logs that the constitution was read
- Status: queued (needs decision)
