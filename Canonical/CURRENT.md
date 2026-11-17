---
type: living-doc
title: CURRENT
project: tomale-rn-v1
status: current
version: 2.5
date: 2026-10-24
last_verified: 2026-11-17
owner: vault
related:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
  - "[[knowledge-architecture]]"
---

# CURRENT: where Tomale V1 stands

Start here. One page, updated whenever the phase or the next step changes. Last updated 17/11/2026.

## Now

- **Phase:** M3 Profiles and parental controls. **Part A (profiles and PIN backend) done 12/11; part B (approvals backend) built 13/11, Postman folder 7 green 17/11** ([[m3-approvals-backend-prep-brief]], prompts in [[m3-approvals-xano-prompts]]). M1a and M2 (Characters, speckit 008, PR #27/#28) done 12/11.
- **Backend:** Phase 1 (security and data integrity) signed off on 23/10, 86/86 `_tests` passing. Auth, profiles, stories and generation, store, payments and print fulfilment are built. Every PRD now has a backend prep list for what's still to build ([[v1-feature-map]]).
- **App repo:** everything is on `main` (foundations 001–006, Expo SDK 58, constitution 1.6.0, Node 22, pnpm; CI `test` runs Gitleaks, Semgrep, audit, lint, typecheck, tests; Renovate for updates). PRs go into `main` and must pass CI; Kyle merges by rebase. No feature screens yet; the app starts to Sign in, and password and magic-link sign-in work on an EAS development build. **007 merged 06/11:** the session lives in `expo-secure-store` (memory only on web), one shared refresh with retry, sign-out only when refresh is rejected, and crash reports carry the account id and active profile id only.
- **Agents:** Claude Project knowledge auto-syncs from the vault; Cursor writes raw session notes; Xano's agent reads a locked AGENTS.md ([[agent-context-sync]]). Daily pipeline 17:40 weekdays, weekly check Mondays ([[knowledge-architecture]] §10).

## Launch plan

Public UK release on the App Store **and Google Play**, full V1 including subscriptions (Free and Creator via RevenueCat), targeted for **late January 2027** ([[move-v1-public-launch-to-late-january]]). Estimate 40–61 working days; the velocity checkpoint after Slice 100 decides whether an earlier closed beta is worth it ([[roadmap]] §2–3).

## Next

1. **Speckit 009 profiles and PIN** (micro-PRD `Project/Plan/009-profiles-pin-micro-prd.md`, 17/11): specify → Claude review → clarify/plan; mock-ups needed before implement. Then **010 approvals** ([[split-m3-into-specs-009-and-010]]). API client regenerated 17/11 (PR #29), constitution 1.6.2 (PR #30).
2. Snag polish pass S-001 to S-003 ([[snags]]) when convenient. Then M4 story creation.

Handover for a new chat: the latest note in `_raw/Chat Sessions/` (or `Sessions/` once the pipeline has run). Launch tracker dashboard (live progress, pace, day ratings): https://claude.ai/artifact/XZ79NEg5XQiHphNDhAzs9i, source data in `Project/Automation/launch-tracker/`.

## Known risks

- **Schedule is tight:** 40–61 days of estimated work against late January.
- **Not built yet:** entitlements and in-app purchase (RevenueCat), the parental PIN gate, the approval flow, account deletion (App Store requirement), backend error reporting, rate limiting, the dev/prod Xano split.
- **Club and an Apple-approved bundle** are V2 ([[v2-backlog]]).
- **Google Play:** new organisation developer account for Tomale.ai Ltd (01/11; contact verification and admin user done 03/11). App record and first build still to do before an Android release ([[pre-launch-checklist]] §5).
- **Story generation takes 10–15 minutes**; the app must handle the wait.
- **User images are public URLs**; signed URLs are decided but not built.

## Where things are

| Need | Doc |
|---|---|
| Plan and order of work | [[roadmap]] · [[v1-feature-map]] · [[v2-backlog]] · launch tracker (link under Next) |
| Product | `Canonical/prd/` (all approved 29/10) |
| Backend conventions and gotchas | [[backend-xano]] |
| Access rules and endpoint matrix | [[security-model]] |
| Tests | [[test-suite]] |
| Before launch | [[pre-launch-checklist]] |
| Stack and monitoring | [[stack]] · [[observability]] |
| System flows | [[story-creation-flow]] · [[image-generation-flow]] · [[order-fulfilment-flow]] · [[order-cancellation-and-refund-flow]] |
| How we work | [[operating-model]] · [[knowledge-architecture]] · [[agent-context-sync]] |
| Queues | [[repo-sync]] · [[pending-updates]] |
| Live code (read-only) | `Repos/tomale-rn-test/` · `Repos/tomale-xano/` |
