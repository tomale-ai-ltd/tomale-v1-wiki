---
type: living-doc
title: repo-sync
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-29
owner: vault
---

# Repo sync queue

Changes to protected specs in `tomale-rn-test`, applied by a Cursor agent **only once approved**, in batches between slices, on a `repo-sync/YYYY-MM-DD` branch with one PR per batch. Process and classes: [[operating-model]] §3.5. Protected documents: [[knowledge-architecture]] §6.

### RS-2026-10-24-01: Constitution amendment (V1 rules after Phase 1)
- Class: A
- Target: `.specify/memory/constitution.md`
- Change: client tokens in `expo-secure-store`, not AsyncStorage; a single Axios 401 interceptor (shared refresh, one retry, never for `/auth/*`; log out on `invalid_refresh_token`; network errors don't log out; proactive refresh on foreground); money in integer minor units (pence); error-code conventions (`STORY_AWAITING_APPROVAL`, `ORDER_NOT_PAYABLE`, `ORDER_NOT_CANCELLABLE`, 400 as Xano has no 422); backend schema procedure says `data-model.md` is generated (`npm run update:datamodel`), not hand-edited; "≥1 review" defined for a solo maintainer (Kyle's PR review); package manager is pnpm (after RS-03); `main` merges by squash or rebase (linear history ruleset); fix the typo `/speckit.spec` → `/speckit.specify` in the Development Workflow section (Cursor review, 29/10)
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
- Status: **done** 28/10 (B6, PR #9 into `wip/pre-restructure-2026-10-24`, spot-checked by Kyle)

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
- Decision (Kyle, 29/10): targeted fix now, speckit upgrade later (after launch or between slices). The fix also corrects `speckit.constitution.md`, which points at a non-existent `.specify/templates/commands/` instead of `.cursor/commands/` (needed before RS-01 runs `/speckit.constitution`).
- Local customisation log: these are edits to speckit tool files. A future upgrade must re-apply them or confirm upstream fixed them.
- Note (29/10): `.cursor/` was entirely gitignored, so the speckit commands and Cursor rules weren't versioned. This PR un-ignores it: commit A tracks `.cursor/commands/` (8) and `.cursor/rules/` unchanged, commit B is the 3-line fix. Merge with rebase, not squash, to keep commit B visible. RS-04 and RS-05 depend on `.cursor/` being tracked.
- Status: in progress (Cursor, `repo-sync/2026-10-29`, 29/10)

### RS-2026-10-28-01: `eas.json` API base URL
- Class: B
- Target: `eas.json` (all three build profiles)
- Change: `EXPO_PUBLIC_API_BASE_URL` points at the old `api:T6T6tF5a` group; change it to the `app` group `https://api.tomale.ai/api:1pgd39RE` (as in `.env`). Fold into the per-build-variant set-up when `app.config.js` arrives ([[use-per-build-variant-url-schemes]]).
- Source: B8 stack check (28/10), [[consolidate-xano-api-groups-into-app-and-webhooks]]
- Speckit impact: none
- Process: Cursor; PR
- Verify: a development build calls `/api:1pgd39RE`
- Status: queued

### RS-2026-10-28-02: Data-model preamble wording
- Class: C (generator script; the output is regenerated)
- Target: `scripts/update-data-model.mjs` (fixed preamble)
- Change: Key Conventions §3 says relationships are inferred from `_id` fields; the generator takes references from the API ([[skip-reference-inference-from-id-fields-in-data-model]]). Reword §3 and review the rest of the preamble against [[backend-xano]] §3.
- Source: B6 review, [[documentation-refresh-backlog]] §9
- Speckit impact: none
- Process: Cursor edits the script, reruns `npm run update:datamodel`; PR
- Verify: second run gives no diff
- Status: queued

### RS-2026-10-29-01: Optional micro-PRD input for `/speckit.specify`
- Class: B (speckit command file, recorded customisation) + template
- Target: `.cursor/commands/speckit.specify.md`, `.specify/templates/spec-template.md`
- Change: if the user names a `.docs/prd/*.md` file, read it and use its goal, scope, out of scope, flow and acceptance sections as the feature description; pass only a short slug (filename without number and extension) to `create-new-feature.sh`; record the source on the spec's Input line. No PRD given → unchanged behaviour. No new gate, artefact or command. Template: one line noting a `.docs/prd/` path is an allowed source.
- Source: Cursor `.specify` review (29/10); [[operating-model]] §3.3
- Speckit impact: `/speckit.specify` only; first used by 007
- Process: repo-sync batch (B10); PR
- Verify: `/speckit.specify` for 007 reads the micro-PRD and creates a sensible `007-…` branch
- Status: queued

### RS-2026-10-29-02: `update-agent-context.sh` sed escaping
- Class: B (speckit script, recorded customisation)
- Target: `.specify/scripts/bash/update-agent-context.sh`
- Change: escape `&`, `\` and the delimiter in `sed` replacement strings. An unescaped `&` produced the garbled commands line in `specify-rules.mdc`. Pair with RS-2026-10-24-05 (one-off cleanup of that file).
- Source: Cursor `.specify` review (29/10)
- Speckit impact: `/speckit.plan` writes a clean rules file
- Process: repo-sync batch (B10); PR
- Verify: next `/speckit.plan` writes `npm test && npm run lint` correctly
- Status: queued

### RS-2026-10-29-03: `.gitignore` hardening
- Class: B
- Target: `.gitignore`
- Change: replace `.env` + `.env*.local` with `.env*` and `!.env.example` (today `.env.production` or `.env.development` would be committed); add `.cursor/mcp.json` (may hold tokens) now that `.cursor/` is tracked; add `coverage/`; add build outputs `*.ipa`, `*.apk`, `*.aab`; add Sentry CLI credentials `.sentryclirc` and `sentry.properties` (source-map upload is planned); anchor `ios`/`android` to the root (`/ios`, `/android`). After pnpm (RS-03): drop `package-lock.json` from the repo and keep `pnpm-lock.yaml`.
- Source: Kyle's question (29/10); review of the current `.gitignore`
- Speckit impact: none
- Process: repo-sync batch (B10); PR
- Verify: `git status --ignored` shows `.env` ignored, `.env.example` tracked; no previously tracked file becomes ignored
- Status: queued
