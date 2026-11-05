---
type: living-doc
title: CURRENT
project: tomale-rn-v1
status: current
version: 2.4
date: 2026-10-24
last_verified: 2026-11-05
owner: vault
related:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
  - "[[knowledge-architecture]]"
---

# CURRENT: where Tomale V1 stands

Start here. One page, updated whenever the phase or the next step changes. Last updated 30/10/2026.

## Now

- **Phase:** frontend development resumes ([[resume-frontend-at-slice-100]]). The knowledge restructure (B0–B12) finished on 30/10.
- **Backend:** Phase 1 (security and data integrity) signed off on 23/10, 86/86 `_tests` passing. Auth, profiles, stories and generation, store, payments and print fulfilment are built. Every PRD now has a backend prep list for what's still to build ([[v1-feature-map]]).
- **App repo:** everything is on `main` (foundations 001–006, Expo SDK 58, constitution 1.6.0, Node 22, pnpm; CI `test` runs Gitleaks, Semgrep, audit, lint, typecheck, tests; Renovate for updates). PRs go into `main` and must pass CI; Kyle merges by rebase. No feature screens yet; the app starts to Sign in, and password and magic-link sign-in work on an EAS development build (03/11).
- **Agents:** Claude Project knowledge auto-syncs from the vault; Cursor writes raw session notes; Xano's agent reads a locked AGENTS.md ([[agent-context-sync]]). Daily pipeline 17:40 weekdays, weekly check Mondays ([[knowledge-architecture]] §10).

## Launch plan

Public UK release on the App Store **and Google Play**, full V1 including subscriptions (Free and Creator via RevenueCat), targeted for **late January 2027** ([[move-v1-public-launch-to-late-january]]). Estimate 40–61 working days; the velocity checkpoint after Slice 100 decides whether an earlier closed beta is worth it ([[roadmap]] §2–3).

## Next

1. **M1 app foundations rework** ([[roadmap]] M1), four Cursor PRs ([[m1-cursor-briefs]]): ~~A Node 22, Renovate, CI security stage~~ done 01/11 (#15); ~~B Expo SDK 54 → 58 + constitution 1.6.0~~ done 03/11 (#19, device-tested); ~~C `app.config.js` (dev `com.tomaleai.tomalerntest`, prod `ai.tomale.app`) + gluestack-ui v5 with UniWind~~ done 04/11 (#20; also fixed a release-build startup crash in `config/env.ts` and set runtime version to `fingerprint`); **D** session handling (SecureStore, 401 interceptor, Sentry context) = speckit 007.
2. **Design system and Characters design** (before 008): review the Tomale design system (Claude artifact, first pass 05/11: tokens, Glacial Indifference, brand icons, core components), mock up the Characters screens with it, then a repo-sync item loads the tokens, fonts and icons into the app's gluestack/UniWind theme (RS-2026-11-05-01).
3. **Characters backend prep** ([[PRD-Characters]] §4), then **Slice 100 = speckit 008**.
4. Then Profiles and parental controls (M3), story creation (M4).

## Known risks

- **Schedule is tight:** 40–61 days of estimated work against late January.
- **New sign-ups get `test_mode: ""`.** Stripe and the print SKU fail closed to test, so real customers' orders would use test keys. Fix before launch ([[pre-launch-checklist]]).
- **Not built yet:** entitlements and in-app purchase (RevenueCat), the parental PIN gate, the approval flow, account deletion (App Store requirement), backend error reporting, rate limiting, the dev/prod Xano split.
- **Club and an Apple-approved bundle** are V2 ([[v2-backlog]]).
- **Google Play:** new organisation developer account for Tomale.ai Ltd (01/11; contact verification and admin user done 03/11). App record and first build still to do before an Android release ([[pre-launch-checklist]] §5).
- **Story generation takes 10–15 minutes**; the app must handle the wait.
- **User images are public URLs**; signed URLs are decided but not built.

## Where things are

| Need | Doc |
|---|---|
| Plan and order of work | [[roadmap]] · [[v1-feature-map]] · [[v2-backlog]] |
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
