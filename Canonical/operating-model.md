---
type: plan
title: operating-model
project: tomale-rn-v1
status: current
version: 1.1
date: 2026-10-24
last_verified: 2026-10-30
owner: vault
related:
  - "[[knowledge-architecture]]"
  - "[[2026-10-23-001]]"
---

# Operating model: who does what, and how work gets done

> **Status: approved 2026-10-24 (v1.0).** Decision notes accepted; the migration stages are in progress.
>
> **Scope.** This document covers *roles, decision rights and workflows* for building Tomale V1. *Where knowledge lives and who may change it* is in [[knowledge-architecture]]. Agents should read this document to understand how to behave on this project; Kyle should be able to hand it to any new collaborator, human or AI.

## 0. How this document relates to the constitution and Cursor rules

This document must never conflict with the repo's governing documents. If it did, Cursor would follow the repo, and this document would be useless for Cursor's role.

- **The constitution governs engineering inside `tomale-rn-test`:** principles, technology standards, quality gates, branch protection, the Constitution Check. Its own Governance section says it "supersedes other practices where conflicting". **This document does not restate or override any of it.** Where a workflow below touches the repo (e.g. §3.3), it defers to the constitution and only adds what happens *outside* the repo (vault, Xano, approvals).
- **This document governs collaboration:** roles, decision rights, how work and knowledge move between Kyle, Claude, Cursor, Xano and the vault.
- **Cursor's collaboration rules are defined once, here,** and carried into the repo only through `.cursor/rules/tomale-project.mdc`. That rule file is a faithful, short copy of §1.2 (Cursor row), §1.3, §3.1 and §3.5, changed only through a `repo-sync` item.
- **When either changes, the other is checked.** The weekly staleness check compares `tomale-project.mdc` with this document's Cursor sections and flags any divergence. A change here that affects Cursor always comes with a `repo-sync` item.
- **Resolved (29/10/2026):** the constitution used to say `data-model.md` was edited by hand; constitution 1.5.0 (RS-2026-10-24-01, PR #11) now says it is generated (`pnpm run update:datamodel`).

## 1. The team

Tomale is built by one human founder working with several AI collaborators. Each has a defined role, defined permissions, and defined limits. **No AI collaborator acts on a live system (Xano, the app repo, Stripe, Pureprint) on its own authority.**

### 1.1 Kyle: founder, product owner, technical lead

- **Decision rights:** final say on product, architecture, security, spend and release. Approves every decision note (`proposed` → `accepted`), every canonical-doc change and every `repo-sync` batch.
- **Sole operator of live systems:**
  - publishes in Xano
  - merges and commits in the app repo (Cursor agents prepare)
  - runs Postman regression
  - deals with Stripe, Pureprint/HPBC and Apple/Google
- **Background:** a non-developer by training who works technically every day. Explain unfamiliar UI steps explicitly (exact menus, field names, before/after). Don't assume deep framework knowledge; do assume strong systems thinking.
- **How Kyle wants AI collaborators to work:**
  - **Ask clarifying questions first** when a request is ambiguous or the answer would change materially.
  - **Be brief and concrete.** Lead with the answer; next steps over general advice; flag risks and trade-offs in a line. Expand only when asked.
  - **Verify before asserting.** Check code, data or docs rather than guessing, and say which source was used.
  - **Flag drift and downstream impact** as soon as it's found; don't silently work around it.
  - **Give a strict yes/no** when asked for one.
  - **Respect separation of concerns:** no direct writes to systems outside your role.
  - **Watch for secrets** in pastes and screenshots, and say so at once.

### 1.2 AI collaborators

| Role | Who | Purpose | May | Must not |
|---|---|---|---|---|
| **Technical co-founder / reviewer** | Claude chat (Tomale-rn-v1 Project, desktop link to the vault and repos) | Think with Kyle: design, specs, briefs for other agents, code review of XanoScript and app code, decisions, documentation | Read everything; write the vault (canonical docs after approval, decisions, raw notes, `repo-sync`, `pending-updates`); run read-only checks on the repos | Edit the app repo or Xano; publish anything; approve its own proposals |
| **Scribe** | Claude daily pipeline (scheduled task, 17:00 weekdays) | Turn raw notes into session notes and decision notes; propose canonical edits; sync Claude Project knowledge | Write sessions, decisions, `pending-updates`, `repo-sync`; archive raw notes | Edit canonical docs, repos or Xano; invent rationale not in the notes |
| **Frontend engineer** | Cursor agents (in `tomale-rn-test`) | Implement V1 slices through speckit; keep repo specs current; apply `repo-sync` items | Edit repo code and specs through speckit and `repo-sync`; write raw session notes to the vault | Edit protected docs outside their process; edit vault canonical docs or decisions; touch Xano |
| **Backend pair** | Xano AI (inside Xano) | Draft XanoScript and analyse the workspace | Draft; analyse; propose | Have anything published without Kyle's review against the published version in the `tomale-xano` mirror; be trusted on security without review |
| **Regression evidence** | Postman `_tests` | Prove the backend behaves | n/a | n/a |
| **System of record** | GitHub | History, diffs, rollback for the app repo, the Xano mirror and the vault | n/a | n/a |

### 1.3 Escalate to Kyle immediately

- Anything irreversible: data deletion, schema type changes, live-mode payments, real print orders, token rotation.
- Anything security-relevant: auth, ownership, secrets, payment amounts.
- Any conflict between sources of truth (see the order of authority in [[knowledge-architecture]] §4).
- Any proposal to change a protected document.

## 2. Decision rights (RACI)

R = does the work · A = approves · C = consulted · I = informed

| Activity | Kyle | Claude chat | Pipeline | Cursor agents | Xano AI |
|---|---|---|---|---|---|
| Product scope and PRDs | A | R | I | C | n/a |
| Backend design (Xano) | A | R (design, review) | n/a | C | R (draft) |
| Publishing in Xano | R/A | C (review first) | n/a | n/a | n/a |
| Frontend slice (speckit) | A | C (review) | n/a | R | n/a |
| Protected spec changes | A | R (`repo-sync` item) | R (proposes) | R (applies) | n/a |
| Decision notes | A | R | R (drafts) | I | n/a |
| Canonical doc changes | A | R | R (proposes) | I | n/a |
| Regression testing | R/A | C (designs tests) | n/a | n/a | n/a |
| Release (EAS, stores) | R/A | C | n/a | R (build config) | n/a |
| Third parties (Stripe, Pureprint, Apple, Google) | R/A | C (drafts) | n/a | n/a | n/a |

## 3. Workflows

### 3.1 Every working session (Claude or Cursor)

1. **Start.** Read `Canonical/CURRENT.md` and the latest session note. Review `pending-updates.md` and open `repo-sync` items if any. Don't ask Kyle to re-explain anything that's documented.
2. **Work.** Keep a task list. Ask clarifying questions up front. Record decisions as they're made, in plain words.
3. **End.** Write a raw note into `_raw/Chat Sessions/`.
   - **Claude** writes it in session-note template form, named `YYYY-MM-DD-NNN.md`.
   - **Cursor** needs no template and no naming rules. It writes a plain note, `YYYY-MM-DD-cursor-<slug>.md`, starting with a four-line header (`date`, `source: cursor`, `branch`, `feature/spec`) followed by free text: what was done, decisions made and why, open questions, next steps. Commit hashes help.
   - The 17:00 pipeline converts both into proper session notes.

### 3.2 Backend change (Xano)

1. **Brief.** Claude (or Kyle) writes a prose brief naming the exact tables, fields, functions and behaviour, plus what must *not* change.
2. **Draft.** Xano AI (or Kyle in the visual builder) drafts the change.
3. **Review against the published version.** Diff the draft against the current file in the `tomale-xano` mirror (`git pull` first), which is the published version. The mirror doesn't include `guid`, so match by file path and query or function name. In XanoScript, a `db.add`/`db.edit` with no `enforce_hidden_fields` line means hidden fields are enforced (the default); only `= false` is written out. Claude reviews for security, fail-closed logic, the hidden-fields rules, money in pence and ownership. Nothing is pasted unreviewed.
4. **Snapshot** before structural changes (schema, group moves, deletions).
5. **Publish on dev** (Kyle). GitHub sync records the commit on the dev git branch. Until the dev/prod split exists, publish on the live branch.
6. **Test.** Run the relevant Postman folder; a full `_tests` run for anything touching auth, orders or payments.
7. **Regenerate.** If an `app` endpoint changed: `pnpm run update:openapi`. If the schema changed: `pnpm run update:datamodel` (both in Cursor).
8. **Record** in the session note, with the mirror commit link.

Backend rules live in `Canonical/backend-xano.md` and are copied into the Xano Knowledge tab.

### 3.3 Frontend slice (speckit, in Cursor)

1. Check that the feature's PRD in `Canonical/prd/` is current and linked in [[v1-feature-map]].
2. Write the feature's micro-PRD in the repo at `.docs/prd/NNN-slicename.md` (template `000-example-prd.md`), drawn from the vault PRD. One per speckit feature, as for 001–006.
3. `/speckit.specify` (referencing the micro-PRD; it creates the `NNN-…` branch) → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`. After `specify`, check the spec against the micro-PRD and the constitution. `analyze` is read-only: changes go back through specify, plan or tasks.
4. `/speckit.implement` also writes `specs/NNN-…/checklists/validation.md`; Kyle and the agent work through it before the PR.
5. Branching, CI, Constitution Check and review follow the constitution's *Development Workflow & Quality Gates*; they aren't restated here. Kyle reviews, squash-merges and deletes the branch ([[name-branches-by-speckit-feature-number]]).
6. If implementation reveals a needed backend change, stop and raise it as a backend change (§3.2). Agents don't work around the API.
7. The raw session note goes to the vault (§3.1).

This replaces the April process notes `sdd-process-overview` and `sdd-flow` (archived in `Project/_archive/cursor/`).

### 3.4 Decision

1. A choice is made in session and recorded in the raw note as a decision, with why, the alternatives and the trade-offs.
2. The pipeline drafts the decision note (`proposed`, or `accepted` if Kyle explicitly decided in session) and fills in **`features`** and **`affects`** (see below).
3. Reconcile proposes edits to every doc in `affects`: vault docs → `pending-updates.md`, repo specs → `repo-sync.md`.
4. Kyle approves; Claude applies vault edits; a Cursor agent applies repo items.
5. If the decision replaces an earlier one, set `superseded_by` on the old note and `supersedes` on the new one.

**How impact is detected reliably, without RAG.** The project uses stable identifiers: table names (`store_orders`), endpoint paths (`POST /store_orders`), function names, feature ids (`F-characters`) and doc names. Impact detection is mechanical:
- **At creation**, `affects` is filled by matching the decision text against:
  - a canonical index: the list of `Canonical/` docs, plus the backend objects and features each one covers, kept in `CURRENT.md`;
  - an exact search for those identifiers across `Canonical/` and `Repos/`.
- **Inverse view for free:** because `affects` holds links, each canonical doc's backlinks show every decision that touches it.
- **Weekly check:** any accepted decision whose `affects` doc has a `last_verified` older than the decision is flagged in `pending-updates.md`. That catches promotions that never happened.
- **Escalation:** if the pipeline can't map a decision to anything, it flags it for Kyle rather than guessing.

### 3.5 Repo sync (vault → protected specs)

Changes to protected specs can change how speckit works and how Cursor builds, so repo sync is a controlled change process, not a to-do list.

**Change classes**

| Class | Examples | Risk | Process |
|---|---|---|---|
| **A: governance** | `constitution.md` principles, quality gates, governance, schema change procedure | Changes every future spec and plan | Constitution amendment per its own Governance section: `/speckit.constitution` with a Sync Impact Report and semver bump; PR with migration/retrofit notes; Kyle approves as document owner; then `/speckit.analyze` against any active spec |
| **B: agent rules** | `tomale-project.mdc`, `tomale-api.mdc`, `.cursorignore`; source fixes in a feature `plan.md` | Changes agent behaviour | Cursor edits; PR; Kyle reviews |
| **C: generated** | `data-model.md`, `xano.yaml`, `client.ts` | Mechanical | Run the script; PR (can go with the backend change that caused it) |
| **Never** | `specify-rules.mdc`, `.specify/templates`, `.specify/scripts`, `.cursor/commands/speckit.*` | Breaks speckit | Not changed by repo sync (only a speckit upgrade, as its own planned task) |

**Item format** (one block per item in `Canonical/repo-sync.md`):
```
### RS-YYYY-MM-DD-NN: <short title>
- Class: A | B | C
- Target: <file(s)>
- Change: <exact intent, not wording>
- Source: [[decision-note]]
- Speckit impact: <templates/specs/active features affected, or "none">
- Process: </speckit.constitution | edit | npm run …>
- Verify: <how we know it worked, e.g. "/speckit.analyze clean on spec 006">
- Status: queued | approved | applied (<commit>) | rejected
```

**Rules**
1. **Approve before applying.** Kyle moves an item to `approved`; Cursor applies only approved items.
2. **Batch between slices.** Apply on a dedicated branch (`repo-sync/YYYY-MM-DD`) when no feature branch is mid-implementation, so the rules don't change under an in-flight slice. Class C can go any time.
3. **One PR per batch**, listing the item ids. CI must pass. For class A, the PR includes the Sync Impact Report.
4. **Verify, then tick:** Cursor records the commit hash and runs each item's check. Failures go back to `queued`, with a note.
5. **Close the loop:** the source decision's `affects` docs get `last_verified` updated by the pipeline on its next run.

### 3.6 Testing

- **Backend regression:** Postman `_tests` (folders 1, NEG, 2A–2B story run, 3, 4), documented in `Canonical/test-suite.md`. Run the full suite before any sign-off or release and after auth, order or payment changes.
- **Test data:** test-mode users only (`test_mode = true`), HPBC staging SKUs and Stripe test keys. Never the live path from tests.
- **Frontend:** Jest and CI in the repo. Journey tests from the CTO plan Phase 4 as slices land.
- **Later:** Xano function tests; split Postman suite in CI (see `defer-postman-suite-ci-until-suite-split`).

### 3.7 Release (outline; detailed before launch)

- **Pre-launch gate:** every item in `Canonical/pre-launch-checklist.md` done:
  - hidden-fields sweep
  - rate limiting
  - parental PIN
  - request history off on token-issuing endpoints
  - dev/prod workspaces
  - Universal/App Links
  - trim the `products` output
  - endpoint inventory, CORS, test-data cleanup, backup
- **Backend release:** in Xano, *branch footer → Merge Branches → source dev, destination prod*, review the change list, Merge, then publish prod once. That gives one GitHub commit on prod. Take a backup first. Run the full `_tests` against prod test accounts afterwards.
- **Builds:** EAS; store submission by Kyle.

## 4. Security habits (everyone)

- Secrets never go in chat, notes, screenshots or git. If one does, say so at once and rotate it.
- `EXPO_PUBLIC_*` variables are bundled into the app, so never put secrets there.
- Metadata and docs tokens are read-only, and live in gitignored `.env` files.
- Backups and exports that include environment variables are stored encrypted, outside the vault and repos.
- Xano: 2FA on, Swagger private, sensitive fields flagged.

## 5. Open questions

**Resolved 2026-10-24:**
- Cursor doesn't write to `CURRENT.md`; the pipeline handles it.
- The release workflow is detailed before launch.
- A second human means adding a role here and moving to PR-only merges.

## Related

- [[knowledge-architecture]]
- [[parental-gate-on-profile-switch]]
- [[defer-postman-suite-ci-until-suite-split]]
- [[keep-agents-out-of-xano-no-mcp]]
- [[protect-speckit-and-generated-spec-documents]]
- [[classify-and-batch-repo-sync-changes]]
