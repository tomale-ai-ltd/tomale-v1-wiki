---
type: plan
title: "Image pipeline migration (milestone MI): plan and task board"
project: tomale-rn-v1
status: active
date: 2026-11-24
related:
  - "[[PRD-Image-Pipeline]]"
  - "[[image-pipeline-research-2026-11]]"
  - "[[image-pipeline-future-state]]"
  - "[[image-pipeline-session-0-brief]]"
---

# Image pipeline migration (MI)

Scope: [[PRD-Image-Pipeline]] · Evidence: [[image-pipeline-research-2026-11]] · Diagrams: [[image-pipeline-future-state]].

**Target:** live before the late-January launch (Kyle, 24/11).
- **Effort:** about 28 days in total. About 9 of those are Kyle's: Session 0, credits, Sessions A and B, IP-03, reviews and the printed proof. The rest is Cursor work that Kyle reviews.
- **Parallel work:** the app contract doesn't change, so Cursor milestones carry on alongside.

## Task board

![[image-pipeline-tasks.base]]

To update a task, change its Status cell (`todo` → `in-progress` → `done`, or `blocked`).

## Gates

| Gate | When | Pass | If it fails |
|---|---|---|---|
| **G0** child-image policy ✅ **passed 26/11** (165/165, 0 blocks) | Week of 24/11 | Under 2% child-filter blocks on Vertex `eu` | Ask for allowlisting; launch on the OpenAI record; consider self-hosting earlier |
| **G1** quality | About 12/12 | Blind consistency ≥ baseline, bleed ≤ baseline, VLM attribute accuracy ≥ 90% | Try another model or strategy; or launch on OpenAI 2.6 with references |
| **G2** live | By 13/01 | p95 under 3 minutes at 20 books, no lost or duplicate jobs, chaos tests pass, no high findings, print approved, rollback under 5 minutes | Launch on the OpenAI record; cut over after launch |
| **G3** character pictures | After G2 | Portrait eval ≥ today | Character pictures stay on OpenAI |

Every gate has a safe fallback (the OpenAI record), so the launch never depends on the migration finishing.

## Calendar

| When | Work |
|---|---|
| 24–28 Nov | IP-00 Session 0 (by 27/11), IP-01 credits, IP-02 G0 spike, IP-05 golden set |
| 1–12 Dec | IP-04 spec and contract, IP-06 harness, IP-08 Terraform, IP-09 gateway, IP-07 G1 bake-off |
| about 15–17 Dec | IP-10 Session A (with IP-03 text and voice models) |
| 18 Dec–8 Jan | IP-11 shadow, IP-12 load, IP-13 chaos, IP-14 review, IP-15 printed proof (order by 5/01) |
| about 11–13 Jan | IP-16 Session B cut-over |
| from about 15 Jan | IP-17 runbooks and drill; launch freeze from about 18/01 |

IP-03 has hard dates: TTS ends 6/01 and `gpt-4o-mini` ends 14/01. If Session A slips past about 20/12, do IP-03 in its own Xano session.

## How the work is run

- **Scoping is proportionate and just in time.**
  - A full spec only where code is built or an interface crosses into Xano: IP-04, IP-06, IP-08, IP-09 and IP-10.
  - A one-page test plan with pass rules for spikes and tests.
  - A checklist for admin and cut-over.
  - Nothing after a gate is detailed until that gate passes.
- **Xano changes** follow [[operating-model]] §3.2 (brief → draft → review against the mirror → publish → Postman), batched into Sessions 0, A and B.
- **The gateway repo** is spec-first, with Cursor building and Kyle merging. Plan on PR; apply after approval ([[build-image-infrastructure-in-a-cursor-terraform-repo]], [[PU-2026-11-24-04]]).
- **Decisions** are notes in `Project/Decisions/`, `proposed` until their gate passes.
- **Canonical changes** go through `Canonical/pending-updates/` (PU-2026-11-24-02 to -08).
- **Session notes** go to `_raw/Chat Sessions/` as usual. Cursor's raw notes for the gateway repo follow the usual `YYYY-MM-DD-cursor-<slug>.md` format.
- **Cost** is tracked per job in `token_usage` (provider, model, cost), with budgets at 25/50/75% of credits on both clouds.
