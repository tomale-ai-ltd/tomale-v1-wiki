---
type: plan
title: knowledge-inventory
project: tomale-rn-v1
status: draft
version: 0.2
date: 2026-10-24
owner: vault
related:
  - "[[knowledge-architecture]]"
---

# Knowledge inventory (B3)

> Every document in the vault, the Cursor repo and the working folders outside the vault, each with its tier, owner and the action B4 will take. Built read-only on 2026-10-24. **Kyle reviews before B4 moves anything.** Tiers and ownership follow [[knowledge-architecture]] §5.

## Ground rules for B4

1. **Moves keep filenames.** Obsidian links resolve by filename, so a move doesn't break `[[links]]`. Renames (e.g. `6-api-security-model` → `security-model`) happen later, in B8, with a link-rewrite script.
2. **Nothing is lost.** Every deletion is either a duplicate, in git history (baseline `d17557e`), or in the encrypted backup (`.bak` files are gitignored but in the 24/10 zip).
3. **Obsidian Git auto-sync is paused** during B4. B4 runs on branch `b4-structure`, and Kyle reviews the diff on GitHub before merging.

## Vault: `Project/Plan/`

| File | Tier | Owner | Action in B4 | Later |
|---|---|---|---|---|
| `1-prd-tomale-react-native-app-v1` | 1 | vault | Move → `Canonical/prd/` | B9: becomes the V1 umbrella PRD, linked to `v1-feature-map` |
| `2-build-plan` | 1 | vault | Move → `Canonical/` | B8: merged into `roadmap.md` with CTO phases 2–5 |
| `3-cto-tech-review` | 3 | vault | Move → `Project/_archive/plan/` | n/a |
| `4-cto-improvements-list` | 3 | vault | Move → `Project/_archive/plan/` | n/a |
| `5-cto-implementation-plan` | 1 → 3 | vault | **Stays in `Project/Plan/`** for now | B8: remaining phases → `roadmap.md` / `pre-launch-checklist.md`, then archived |
| `6-api-security-model` | 1 | vault | Move → `Canonical/` | B8: matrix rebuilt from OpenAPI; renamed `security-model` |
| `documentation-refresh-backlog` | 1 (temporary) | vault | Stays | Work list for B8–B10; archived at B12 |
| `knowledge-architecture` | 1 | vault | Move → `Canonical/` | n/a |
| `operating-model` | 1 | vault | Move → `Canonical/` | B8: absorbs the speckit process docs |
| `knowledge-inventory` (this file) | temporary | vault | Stays | Archived at B12 |

## Vault: `Project/Plan/Feature PRDs/` (all 2026-04-14)

| File | Tier | Action in B4 | B9 priority |
|---|---|---|---|
| `PRD-Characters` | 1 | Move → `Canonical/prd/` | **Critical path: needed for Slice 100** |
| `PRD-Chatbot-Create-Character` | 1 | Move → `Canonical/prd/` | High (Characters-adjacent) |
| `PRD-Chatbot-Story-Conversations` | 1 | Move → `Canonical/prd/` | Normal |
| `PRD-E-Reader` | 1 | Move → `Canonical/prd/` | Normal |
| `PRD-Order-PoD-System` | 1 | Move → `Canonical/prd/` | Normal (backlog has Mixam → HPBC, cancellation window) |
| `PRD-Store-Orders` | 1 | Move → `Canonical/prd/` | Normal (same backlog items) |
| `PRD-Parental-Oversight-Content-Approval` | 1 | Move → `Canonical/prd/` | Normal (order gate added 23/10) |
| `PRD-Subscription-Entitlement-System` | 1 | Move → `Canonical/prd/` | Normal |
| `PRD-transaction-webhooks-micro-prd` | 1 | Move → `Canonical/prd/` | Normal (refund events) |

## Vault: `Project/Architecture/`

| File | Tier | Action in B4 | Later |
|---|---|---|---|
| `story-creation-flow` | 1 | Move → `Canonical/architecture/` | B8 refresh |
| `image-generation-flow` | 1 | Move → `Canonical/architecture/` | B8: runs found by id, failed start releases the job, `created_at` mystery solved |
| `order-fulfilment-flow` | 1 | Move → `Canonical/architecture/` | B8: PDF runs by id, empty `hpbc_order_id`, Papermill logs status only |
| `order-cancellation-and-refund-flow` | 1 | Move → `Canonical/architecture/` | B8: check against 23/10 checks |
| 3 × `.bak-*` files | none | **Delete** (in the encrypted zip) | n/a |

## Vault: `Project/Stack/` (15 notes, all 2026-04-14)

**Why Tier 3:** they're April snapshots of each technology's *intended* use, split across 15 notes and partly overtaken by Phase 1 (e.g. `9. AsyncStorage` puts tokens in AsyncStorage; `7. Auth` predates refresh rotation and the 401 rules). The idea of a stack overview stays; the 15 frozen notes don't.

**Replacement: one living `Canonical/stack.md`** (written in B8). One page, one row per layer: technology and version, what it's used for in Tomale, where its rules live (constitution, `backend-xano`, `observability`, generated specs), and its status (in use / planned / retired). It's the first place to look for a stack overview, and `CURRENT.md` links to it.

**Observability gets its own canonical doc, `Canonical/observability.md`,** rather than being folded into `backend-xano`. Sentry covers what Xano can't see: frontend crashes, error boundaries, release health, OTA updates. Backend observability (`executor_runs`, the `audit_store_orders` trigger, request history, `user logs`) sits alongside it, so the whole picture is in one place. Frontend engineering rules for Sentry stay in the constitution (Principle 5); `observability.md` describes the system end to end and links to them.

| File | Harvested into (B8) | Then |
|---|---|---|
| `1. Overview` | `stack.md` (structure) | Archive |
| `2. Frontend - React`, `3. Routing - Expo Router`, `4. Frontend - UI`, `5. State Management - Zustand` | `stack.md` rows; engineering rules are already in the constitution | Archive |
| `6. Backend - Xano` | `stack.md` + `backend-xano.md` (background tasks, disabled trigger, conventions) | Archive |
| `7. Auth - Xano` | `stack.md` + `backend-xano.md` + constitution item (401 interceptor rules) | Archive |
| `8. Storage - AWS` | `stack.md` (planned: S3 + CloudFront, Phase 1.5) | Archive |
| `9. AsyncStorage` | `stack.md` + constitution item (tokens → SecureStore) | Archive |
| `10. DevTools - GitHub, Cursor` | `stack.md` + `operating-model` | Archive |
| `11. Manual Testing` | `test-suite.md` | Archive |
| `12. CICD - EAS, GitHub` | `stack.md` + `operating-model` §3.7 + pnpm migration | Archive |
| `13. AI Text Generation - OpenAI`, `14. AI Image Generation - OpenAI` | `stack.md` (gpt-4o-mini, gpt-image-1; Bedrock planned for Phase 2) + `backend-xano.md` (pipeline notes) | Archive |
| `15. Observability - Sentry` | **`observability.md`** (frontend section) + `stack.md` row | Archive |

In B4 the 15 notes move to `Project/_archive/stack/`; B8 harvests them from there.

## Vault: `Project/Cursor/`

| File | Tier | Action in B4 | Why |
|---|---|---|---|
| `constitution` | none | **Delete** | Copy of `tomale-rn-test/.specify/memory/constitution.md` (repo is master). It would also clash by name with the `Repos/` link |
| `data-model` | none | **Delete** | Copy of the repo's `data-model.md`, about to be generated; same name clash |
| `api-spec` | 3 | Move → `Project/_archive/cursor/` | Hand-written, stale; superseded by `xano.yaml`. Kept for history (no repo copy exists) |
| `sdd-flow`, `sdd-process-overview` | 3 | Move → `Project/_archive/cursor/` | B8: merged into `operating-model` §3.3 |

## Vault: other folders

| Location | Count | Tier | Action |
|---|---|---|---|
| `Project/Decisions/` | 97 | 2 | Stays. B5: frontmatter backfill (status, `superseded_by`, `affects`) |
| `Sessions/` | 42 | 3 | Stays (decision 24/10). B5: normalise `type` only |
| `_raw/Chat Sessions/` (+ `_archive/` 24) | 1 pending | 3 | Stays: pipeline input |
| `_raw/Web Clippings/` | 0 | 3 | Stays (empty) |
| `Project/Research/` | 4 notes | 3 | Stays; frontmatter only |
| `Project/Research/Research Proposals/CFI…` | 4 | 3 | Stays (decision 24/10); excluded from agent defaults. Note: `Fathers-Engagement-Draft-v1` is 590 KB, so it must stay out of any default context |
| `Templates/decision-note`, `session-note` | n/a | n/a | B5: decision template updated to the new schema |
| `Templates/stack-note` | n/a | n/a | Move → `Project/_archive/` (stack notes retired) |
| `wiki/` | 584 + `knowledge.json` | none | **Delete** (in git history) |
| `.obsidian/plugins/llm-wiki/` | n/a | n/a | **Delete** the plugin folder (holds the revoked API keys); already turned off |

## New in B4

- `Canonical/`, `Canonical/prd/`, `Canonical/architecture/`
- Tier 1 stubs, written in B8: `Canonical/CURRENT.md`, `Canonical/stack.md`, `Canonical/observability.md`
- `Canonical/repo-sync.md` (format plus the queued items known so far) and `Canonical/pending-updates.md` (format only)
- `Project/_archive/` (`plan/`, `stack/`, `cursor/`)
- `Repos/tomale-rn-test/`, with symlinks:
  - `memory` → `.specify/memory`
  - `specs` → `specs`
  - `prd` → `.docs/prd`
  - `openapi` → `api/openapi`
- `Repos/tomale-xano` → symlink to `~/Developer/tomale/tomale-xano`

## Cursor repo `tomale-rn-test` (stays in place; protected per [[knowledge-architecture]] §6)

| Path | Contents | Owner | Notes |
|---|---|---|---|
| `.specify/memory/constitution.md` | v1.4.0, Nov 2025 | repo | B10 class A amendment (SecureStore, 401 interceptor, pence, generated data model, "review" for a solo maintainer, pnpm) |
| `.specify/memory/data-model.md` | 14 Apr 2026 | generated | B6: replaced by `update:datamodel` output |
| `specs/001…006` | 6 feature folders (006 has a spec only) | repo | Untouched. 002 `plan.md` gets the SecureStore source fix in B10 |
| `.docs/prd/000…006` | foundation PRDs (000 is speckit's example) | repo | Untouched |
| `api/openapi/xano.yaml`, `api/client.ts` | refreshed 23/10 | generated | B6 refresh |
| `.cursor/rules/specify-rules.mdc` | speckit-generated | nobody | Never edited |
| `README.md` | n/a | repo | Untouched |

Repo note: the working branch is `wip/pre-restructure-2026-10-24`; `main` is `507a26f`, now protected by the `protect-main` ruleset.

## Outside the vault (retire)

| Location                                        | Contents                                                                               | Action                                                                                    |
| ----------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `Desktop/Kyle/Work/Tomale/Tech/tomale-v1-wiki/` | Legacy vault; only an empty `Sessions/`                                                | **Kyle deletes** the folder. It's referenced only by the paused old scheduled task        |
| `Documents/Claude/Projects/Tomale-rn-v1/`       | `DRAFT_order-fulfilment-flow`, `DRAFT_order-cancellation-and-refund-flow`              | Delete (superseded by the Architecture docs, 14–15/10)                                    |
| ″                                               | 6 × `.xs` (`hpbc_*`, `auth_refresh_*`, `admin_purge_stuck_stories`)                    | Delete (superseded by the `tomale-xano` mirror)                                           |
| ″                                               | `spec_delayed_hpbc_submission_2026-10-14`, `spec_executor_run_lookup_by_id_2026-10-21` | Move → vault `Project/_archive/specs/` (backend specs as history)                         |
| ″                                               | the folder itself                                                                      | Retire as a Claude working source once emptied; remove it from this Project's folder list |
| Claude Project knowledge                        | 37 uploaded copies (stale)                                                             | B11: replaced by `Canonical/` + decisions, synced                                         |

## Findings to note

**1. How speckit actually works (read 24/10 from `.specify/scripts/bash/*.sh`, `.cursor/commands/speckit.*.md` and specs 002 and 005):**
- **A feature is identified by the git branch name.** `/speckit.specify` runs `create-new-feature.sh`, which takes the highest `specs/NNN-*` number + 1, creates branch `NNN-<first three words>` and `specs/NNN-<…>/spec.md` from the template, plus `checklists/requirements.md`. Every later command (`clarify`, `plan`, `tasks`, `analyze`, `implement`) resolves paths from the current branch (or `SPECIFY_FEATURE`) and **refuses to run unless the branch matches `^[0-9]{3}-`**.
- **`/speckit.plan`** copies the plan template, reads the spec and the constitution, then generates `research.md`, a **per-feature** `data-model.md` (entities for this feature only), `contracts/` and `quickstart.md`. In this repo, `contracts/README.md` points at the canonical `api/openapi/xano.yaml` rather than inventing endpoints (a good convention to keep). It then runs `update-agent-context.sh cursor`.
- **`update-agent-context.sh` only appends.** It reads `Language/Version`, `Primary Dependencies` and `Storage` from the current `plan.md`, adds those lines to "Active Technologies" if they aren't already there, rotates "Recent Changes" (keeps 2) and updates the date. **It never removes old lines.** So my earlier advice ("fix the AsyncStorage line at its source in the 002 plan and the next run corrects it") was **wrong**: the stale line would stay. Correction: leave 002's `plan.md` alone (it's the historical record of that slice); cleaning the stale "Active Technologies" lines in `specify-rules.mdc` is a one-off class B edit the script won't undo (it only re-adds a line if a future plan names it).
- **`specify-rules.mdc` has no frontmatter.** Cursor probably treats it as a manual rule, loaded only when @-mentioned rather than automatically. To check in Cursor's rules settings. Either way, what speckit actually loads is the constitution.
- **The global `.specify/memory/data-model.md` is a Tomale addition, not part of speckit.** No speckit command reads it; it's used because the constitution names it the data-model source of truth. So generating it (B6) only helps if the constitution and `tomale-api.mdc` keep pointing to it, and the B10 amendment must keep that link.
- **Bug: `speckit.plan.md` and `speckit.tasks.md` contain the path `.specify.specify/…`** (doubled), for the constitution and the tasks template. Agents probably recover by finding the real path, but it's unreliable. These are speckit tool files (never edited for project content), so the fix is a **speckit upgrade** or a deliberate, recorded one-line correction. To decide in B10.

**2. What this means for `Repos/`:** the vault only ever *reads* the repo, and `Repos/tomale-rn-test/specs` shows new `NNN-*` folders as soon as speckit creates them, which is what we want. Because each feature folder reuses the same filenames, **links into `Repos/` are path-qualified** (`[[Repos/tomale-rn-test/specs/007-characters/spec|007 spec]]`), and no vault note may be named `spec`, `plan`, `tasks`, `research`, `quickstart` or `data-model`. Nothing in this setup touches speckit's paths or scripts.

**3. Slice numbering:** the build plan calls the next slice "Slice 100 (Characters)", but speckit will number it **007** (highest existing is 006). `v1-feature-map` will map slices to spec numbers (e.g. Slice 100 → `007-characters`) rather than fight the script.

**4. The `wip/` branch blocks speckit.** The repo is on `wip/pre-restructure-2026-10-24` (not an `NNN-` branch), with uncommitted-then-snapshotted work that isn't on `main`. Before `/speckit.specify` for Slice 100, decide what from the WIP snapshot goes to `main` (by PR), then start `007-*` from `main`.

**5. Constitution "≥1 review"** can't be met by a solo maintainer on GitHub; it's queued for the B10 amendment.

**6. Sessions count is 42**, not 40.

## Kyle: confirmations (24/10)

- [x] Vault copies of `constitution` and `data-model` deleted (Kyle, 24/10).
- [x] `5-cto-implementation-plan` stays in `Project/Plan/` until B8.
- [x] Path-qualified links for `Repos/`.
- [x] `.xs` and `DRAFT_` files deleted from the Claude working folder (Kyle). The two `spec_` files move to `Project/_archive/specs/` in B4.
- [x] `Canonical/stack.md` and `Canonical/observability.md` (Tier 1), created as stubs in B4 (Kyle, 24/10).
