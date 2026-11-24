---
type: living-doc
title: CURRENT
project: tomale-rn-v1
status: current
version: 2.6
date: 2026-10-24
last_verified: 2026-11-24
owner: vault
related:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
  - "[[knowledge-architecture]]"
---

# CURRENT: where Tomale V1 stands

Start here. One page, updated whenever the phase or the next step changes. Last updated 24/11/2026.

## Now

- **Phase:** M3 Profiles and parental controls. **Part A (profiles and PIN backend) done 12/11; part B (approvals backend) built 13/11, Postman folder 7 green 17/11** ([[m3-approvals-backend-prep-brief]], prompts in [[m3-approvals-xano-prompts]]). M1a and M2 (Characters, speckit 008, PR #27/#28) done 12/11. **Speckit 009 (profiles and PIN) merged 18/11** (PR #31, `e688caf`): profile picker on cold start and after 15 minutes in the background, parent PIN pad with lockout and email unlock, Set/Change PIN, Manage/Add/Edit/Delete profiles, 30 animal avatars or a character picture, header avatar menu. Phone pass done 18/11. **Speckit 010 (approvals) merged 20/11** (PR #32, `417f073`): parent inbox (To review, Rejected), text-first review with characters and a page carousel, approve, reject, then approve for the child, keep for the parent or delete; the child's locked waiting card; the review count on the header avatar, a Home card and the avatar menu; the approvals link held until sign-in, picker and PIN; minimal parent and child Home (shortcuts, empty favourites, typed story list); Settings as its own page with Log out. Phone pass done 19/11. M3 is complete. **Snag polish pass merged 23/11** (PR #33, up to `caee36f`): S-001 to S-030 fixed. **Speckit 010b (sign-up, sign-in, confirm email) merged 24/11** (main `05f27b1`): Create account with terms, Check your email with resend and the 60-second wait, the email-confirmed lock on creating (parent sheet, child "Ask a grown-up"), the Name step, restyled Sign in and magic link, and one kit back button (S-031). Constitution 1.6.3 (RS-2026-11-17-02). Phone pass and bug round done 24/11; snags S-034 to S-039 for the polish slice. **Now: 011 make a story** ([[011-story-creation-micro-prd]], draft for review).
- **Backend:** Phase 1 (security and data integrity) signed off on 23/10, 86/86 `_tests` passing. Auth, profiles, stories and generation, store, payments and print fulfilment are built. Every PRD now has a backend prep list for what's still to build ([[v1-feature-map]]).
- **App repo:** everything is on `main` (foundations 001–006, Expo SDK 58, constitution 1.6.2, Node 22, pnpm; CI `test` runs Gitleaks, Semgrep, audit, lint, typecheck, tests; Renovate for updates). PRs go into `main` and must pass CI; Kyle merges by rebase. Feature screens so far: Characters (008), profiles and PIN (009) and approvals (010). 010 also fixed two 009 profile-gate bugs: a brief background no longer drops the picker (a PIN bypass), and a switch no longer raises the picker again. The iOS development build was rebuilt on EAS 18/11 after the distribution certificate expired on 13/11 (new certificate and ad hoc profile). **007 merged 06/11:** the session lives in `expo-secure-store` (memory only on web), one shared refresh with retry, sign-out only when refresh is rejected, and crash reports carry the account id and active profile id only.
- **Agents:** Claude Project knowledge auto-syncs from the vault; Cursor writes raw session notes; Xano's agent reads a locked AGENTS.md ([[agent-context-sync]]). Daily pipeline 17:40 weekdays, weekly check Mondays ([[knowledge-architecture]] §10).

## Launch plan

Public UK release on the App Store **and Google Play**, full V1 including subscriptions (Free and Creator via RevenueCat), targeted for **late January 2027** ([[move-v1-public-launch-to-late-january]]). Estimate 40–61 working days; the velocity checkpoint after Slice 100 decides whether an earlier closed beta is worth it ([[roadmap]] §2–3). Image pipeline milestone MI runs in parallel and goes live before launch ([[PRD-Image-Pipeline]]).

## Next

0. **Image models off `gpt-image-1.5` by 27/11** (shutdown 1 Dec): [[image-pipeline-session-0-brief]]. Then the G0 child-image spike.
1. **Speckit 011 make a story** (whole of M4): Kyle reviews the micro-PRD, [[011-xano-prompts]] and the canvas (`Project/Design/011-story-creation/`); Xano X1–X3 first, then a `/speckit.constitution` PATCH for the new codes, then specify → … → implement, one phone pass at the end.
2. The B6 docs PU (`user_profiles_id` in [[backend-xano]] and [[security-model]]); Then a short polish slice (S-032 loading states, S-033 animated launch; [[snags]]), then M4 story creation (011).

Handover for a new chat: the latest note in `_raw/Chat Sessions/` (or `Sessions/` once the pipeline has run). Launch tracker dashboard (live progress, pace, day ratings): https://claude.ai/artifact/XZ79NEg5XQiHphNDhAzs9i, source data in `Project/Automation/launch-tracker/`.

## Known risks

- **OpenAI shutdowns before launch:** `gpt-image-1.5` 1 Dec 2026 (Session 0); `gpt-4o-mini-tts`/`tts-1` 6 Jan 2027 (read-aloud); `gpt-4o-mini` 14 Jan 2027 (compiler, moderation, story text, chat) ([[IP-03-replace-text-and-voice-models]]).
- **Moderation:** a gentle illness story passed text moderation in testing (19/11); check the prompt before launch.
- **Schedule is tight:** 40–61 days of estimated work against late January.
- **Not built yet:** entitlements and in-app purchase (RevenueCat), account closing (App Store requirement), sign out of all devices, the server-side email-confirmed gate, backend error reporting, rate limiting, the dev/prod Xano split.
- **Club and an Apple-approved bundle** are V2 ([[v2-backlog]]).
- **Google Play:** new organisation developer account for Tomale.ai Ltd (01/11; contact verification and admin user done 03/11). App record and first build still to do before an Android release ([[pre-launch-checklist]] §5).
- **Apple distribution certificate** renewed 18/11 (the old one expired 13/11 and broke the dev build). The next production or preview build will ask for new App Store signing; annual renewal reminder set.
- **Story generation takes 10–15 minutes**; the app must handle the wait (target under 3 minutes after MI).
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
