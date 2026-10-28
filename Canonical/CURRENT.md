---
type: living-doc
title: CURRENT
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-28
owner: vault
related:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
  - "[[knowledge-architecture]]"
---

# CURRENT: where Tomale V1 stands

Start here. One page, updated whenever the phase or the next step changes. Last updated 28/10/2026.

## Now

- **Backend:** Phase 1 (security and data integrity) signed off on 23/10, with 86/86 `_tests` passing. Auth, profiles, stories and generation, store, payments and print fulfilment are built ([[v1-feature-map]]).
- **App:** foundations 001–005 merged; 006 (HTTP client) on `wip/pre-restructure-2026-10-24`. No feature screens yet.
- **Knowledge restructure:** B0–B7 done; B8 (canonical docs) in review; then B9 PRD reconciliation → B10 repo sync → B11 automations → B12 close-out ([[knowledge-architecture]] §13).

## Decision needed: the launch plan

Target: public App Store release in the UK by the end of November. The full V1 is about 37–56 days of work against about 20–25 available, so it doesn't fit. Options in [[roadmap]] §3:
- **A.** Move the date (full V1 around late January).
- **B.** Closed beta by end of November, then a public launch with subscriptions in January. **Recommended.**
- **C.** Public launch at the end of November without subscriptions, with cuts.

## Next

1. Choose A, B or C. The roadmap's milestones and the [[pre-launch-checklist]] follow from it.
2. Finish the restructure (B9–B12, about a day).
3. App foundations rework (M1): pnpm, SecureStore and the 401 interceptor, fix `eas.json` (it points at the old API group), per-build schemes, CI security stage.
4. Backend prep for Characters, then **Slice 100 = speckit 007** ([[scope-characters-per-profile-with-soft-delete]]).

## Known risks

- **New sign-ups get `test_mode: ""`.** Stripe and the print SKU fail closed to test, so real customers' orders would use test keys. Must be fixed before launch ([[pre-launch-checklist]]).
- **Not built yet:** entitlements and in-app purchase, the parental PIN gate, the approval flow, account deletion (App Store requirement), backend error reporting, rate limiting, the dev/prod Xano split.
- **Story generation takes 10–15 minutes**; the app must handle the wait (Phase 2 fix).
- **User images are public URLs**; signed URLs are decided but not built.

## Where things are

| Need | Doc |
|---|---|
| Plan and order of work | [[roadmap]] · [[v1-feature-map]] |
| Backend conventions and gotchas | [[backend-xano]] |
| Access rules and endpoint matrix | [[security-model]] |
| Tests | [[test-suite]] |
| Before launch | [[pre-launch-checklist]] |
| Stack and monitoring | [[stack]] · [[observability]] |
| System flows | [[story-creation-flow]] · [[image-generation-flow]] · [[order-fulfilment-flow]] · [[order-cancellation-and-refund-flow]] |
| Product | `Canonical/prd/` (reconciled in B9) · [[v1-audit]] |
| How we work | [[operating-model]] · [[knowledge-architecture]] |
| Queues | [[repo-sync]] · [[pending-updates]] · [[documentation-refresh-backlog]] |
| Live code (read-only) | `Repos/tomale-rn-test/` · `Repos/tomale-xano/` |
