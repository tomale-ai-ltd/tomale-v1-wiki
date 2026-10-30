---
type: living-doc
title: roadmap
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
last_verified: 2026-10-28
owner: vault
supersedes:
  - "[[2-build-plan]]"
related:
  - "[[v1-feature-map]]"
  - "[[5-cto-implementation-plan]]"
  - "[[pre-launch-checklist]]"
  - "[[v1-audit]]"
---

# Roadmap to V1

Replaces [[2-build-plan]] (slice order) and the open phases 2–5 of the fractional CTO's [[5-cto-implementation-plan]]. Both originals are archived unchanged. Every outstanding CTO task is listed by its original number in §5 and placed in a milestone below, tagged **CTO #n**.

**Target:** public App Store release in the UK of the full V1, **late January 2027** (moved from the end of November on 28/10, [[move-v1-public-launch-to-late-january]]). Google Play at the same time (confirmed 29/10).

## 1. Where we are (28/10)

- **Backend:** Phase 1 (security and data integrity) was signed off on 23/10 with 86/86 `_tests` passing. Auth, profiles, stories and generation, store, payments and print fulfilment are built ([[v1-feature-map]]).
- **App:** foundations 001–005 are merged, and 006 (HTTP client) is on `wip/pre-restructure-2026-10-24`. No feature screens have been built since the frontend hold in December 2025.
- **Knowledge restructure:** B0–B7 are done; B8 (this) is in progress, with B9–B12 to follow.
- **Not built:** entitlements and subscriptions, the parental PIN gate, the approve/reject flow, account deletion, backend Sentry, rate limiting, the dev/prod Xano split.

## 2. Feasibility of the end-of-November date

The estimates are rough: one person working with Cursor agents, in working days. The milestones in §4 add up to about **37–56 days** without AI character creation (**40–61 days** with it, added to V1 on 29/10). From 29/10 to a submission around 23/11 (leaving about a week for App Store review and one rejection round), there are roughly **20–25 working days**.

**The full V1 does not fit by the end of November.** The largest items are story creation (M4) and entitlements with in-app purchase (M8). Apple requires in-app purchase for digital subscriptions, so it can't be Stripe. Printed books are physical goods and can keep using Stripe.

## 3. Options

> **Decided 28/10: option A** ([[move-v1-public-launch-to-late-january]]). Public UK release of the full V1 targeted for late January 2027. Velocity checkpoint after M2 (Slice 100): if actual effort runs at roughly 60% of the estimates or less, an earlier closed beta (option B) is reconsidered. Record actual days per milestone below as they finish.

| Option | What ships by end of November | Then | Risk |
|---|---|---|---|
| **A. Move the date** | Nothing public | Full V1 (M0–M10), public launch about late January 2027 (after Apple's holiday slowdown) | Lowest delivery risk; two more months without users |
| **B. Closed beta, then launch (recommended)** | A TestFlight beta with M0–M7 and the M9 essentials. A simple server-side generation cap replaces the full entitlement system. Books are sold through Stripe. | Subscriptions (M8) and the public release in January | Medium. The beta produces the stories-created-to-books-ordered data needed to price subscriptions ([[gate-image-generation-with-entitlements-at-story-creation]]) |
| **C. Public launch without subscriptions** | M0–M7, M9 and M10 public, with a simple generation cap and books through Stripe, so no in-app purchase is needed | Subscriptions added later | High. About 30+ days of work in about 22, so it needs cuts: card-guided story creation instead of free chat, a minimal onboarding, no reading progress |

The simple cap (for example N stories per account, checked in one backend function where stories and image jobs are created) is the first step of the entitlement gate, not throwaway work. M8 replaces the fixed number with plan-based entitlements. Slice 200 handles a "limit reached" error code from day one, so either can be added without UI rework.

## 4. Milestones (build order)

Dependency order follows the original build plan: foundations → characters → story creation → bookshelf → store → AI character creation. New milestones fill the gaps the plan didn't cover (profiles, parental controls, account, entitlements, launch). Each slice starts with its backend prep.

### M0. Finish the knowledge restructure (about 1 day)
B9 PRD reconciliation → B10 repo sync → B11 agent access and automations → B12 close-out ([[knowledge-architecture]] §13).

### M1. App foundations rework (2–3 days)
- pnpm migration with install scripts blocked, `minimumReleaseAge: 7` and an audit in CI (**CTO #27**, **#20**; [[promote-pnpm-migration-ahead-of-slice-100]]; repo-sync RS-03).
- Tokens in `expo-secure-store` and a single Axios 401 interceptor (repo-sync RS-01; [[use-expo-secure-store-for-client-tokens]]).
- `eas.json` still points every build at the old `api:T6T6tF5a` group; it must point at the `app` group `api:1pgd39RE`.
- `app.config.js` with per-build schemes ([[use-per-build-variant-url-schemes]]).
- CI security stage: Gitleaks (**CTO #18**), Semgrep (**#21**), audit (**#20**); CI checks required for merges into `main` (**#22**).
- Frontend Sentry already exists (004); add the user and profile context to events (**CTO #16**).
- **Choose the UI component library** before Slice 100: the constitution names NativeBase, which isn't installed and is, as far as we know, no longer maintained (successor: gluestack-ui). Candidates: gluestack-ui, Tamagui, React Native Paper, custom on Reanimated. The choice goes into the constitution amendment (RS-01).

### M2. Characters, Slice 100 / speckit 007 (3–4 days)
- Backend prep: characters stay household-wide (no schema change for visibility); parent-only delete/archive; `is_favourite`; endpoints to link existing characters to a story, re-create an image, and set archive/favourite ([[PRD-Characters]] §4, [[share-characters-across-the-household]]).
- App: 101 index, 102 detail, 103 create (form, names moderated on create), 104 carousel, 105 quick actions (favourite, archive, delete) and re-create image. "Create a story with this character" ships with Slice 200.

### M3. Profiles and parental controls (4–6 days)
- Profile picker, create child profile, preset avatars ([[use-bundled-preset-avatars-for-profiles]]).
- **PIN gate** on switching to a parent profile, backend and UI ([[parental-gate-on-profile-switch]]).
- **Approve/reject flow** for flagged stories, with the channel (profile switch, email, push with PIN) decided in the B9 PRD ([[PRD-Parental-Oversight-Content-Approval]]).
- Child-experience tests (**CTO #23–#26**, moderation and approval journey).

### M4. Story creation, Slice 200 / speckit 008 (5–8 days)
- 201 draft bootstrap → 202 conversation → 203 suggestion cards → 204 complete. Uses the live `conversations` endpoints and the Draft → Preparing → In Queue → Done lifecycle ([[formalise-story-status-lifecycle]]).
- "Limit reached" error handled from day one (§3).
- Generation takes 10–15 minutes per story, so the UI must handle waiting and the completion alert ([[defer-image-pipeline-throughput-to-phase-2]]).

### M5. Bookshelf and e-reader, Slice 300 / speckit 009 (3–5 days)
- 301 bookshelf, 302 e-reader (cover, pager, read-to-me). 303 reading progress only if it needs no major backend change ([[drop-library-and-pdf-download-from-v1]]).
- Child locked state for stories awaiting approval.

### M6. Store, Slice 400 / speckit 010 (4–6 days)
- 401 index, 402 checkout with the e-reader preview ([[use-e-reader-preview-before-order-payment]]) and the in-app browser return ([[return-from-stripe-checkout-via-in-app-browser-sheet]]), 403 order history and tracking, 404 failure/retry and cancel within the 30-minute window.

### M6a. AI character creation, Slice 500 / expected speckit 011 (3–5 days)
- **In V1 (Kyle, 29/10, [[include-ai-character-creation-in-v1]]).** 501 chatbot create-character, reusing the chat UI from M4 and the `conversations` endpoints ([[PRD-Chatbot-Create-Character]]).
- Backend: `character-chat` prompt record and the character message handler.
- 502 voice input stays behind a feature flag and is the first thing cut if the date is at risk.

### M7. Account, onboarding, notifications (3–4 days)
- Settings and preferences, onboarding walkthrough, alerts inbox.
- **Account deletion** (App Store guideline 5.1.1(v)): a new backend endpoint plus UI.

### M8. Entitlements and subscriptions (6–10 days)
- Backend: entitlement gate before story and image-job creation, usage counters, `GET /me/entitlements`, subscription state ([[PRD-Subscription-Entitlement-System]]).
- In-app purchase (Apple and Google) through RevenueCat: the subscription mirror, sync endpoint, RevenueCat webhook and daily reconciliation ([[use-revenuecat-for-in-app-subscriptions]]). Stripe subscriptions are V2 with Club.
- Locked art-style tiles become live ([[return-full-artwork-catalogue-with-locked-tiles]]).

### M9. Launch hardening (4–6 days)
- Dev/prod Xano branches with suffixed env vars, and a dev → prod promotion run once end to end (**CTO #10, #11, #12**; [[use-xano-branches-for-dev-and-prod]]).
- Backend error reporting to Sentry and email alerting (**CTO #15** as elevated, **#17**; [[elevate-backend-observability-to-launch-requirement]]).
- Everything on [[pre-launch-checklist]]: rate limiting (CTO §4.1), the hidden-fields sweep (CTO §4.6), request history off on auth endpoints, stray `422` messages, Stripe live keys, HPBC live SKU, MFA on all services (**CTO #13**, remainder).
- Signed URLs for user images (CTO §2.9, [[migrate-image-storage-to-aws-s3-signed-urls]]): decide whether this happens before launch or straight after (children's images are public URLs today).

### M10. Store submission (2–3 days, plus review)
App Store Connect listing, privacy policy and nutrition labels, age rating and category, screenshots, TestFlight round, submission. Google Play listing, data safety form, internal testing track and submission at the same time.

### Later
502 voice input for character creation, if it doesn't make M6a. Everything else deferred is in [[v2-backlog]].

## 5. CTO implementation plan: outstanding tasks

From [[5-cto-implementation-plan]] (archived). Phase 1 (#1–#9) was signed off on 23/10.

| CTO # | Task                                                              | Status (28/10)                                                                                                                | Where                      |
| ----- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 10    | Create dev + prod environments                                    | Not done. Now dev/prod Xano branches ([[use-xano-branches-for-dev-and-prod]])                                                 | M9                         |
| 11    | Separate API keys and services per environment                    | Partly done (`test_mode` drives Stripe and HPBC; suffixed env vars)                                                           | M9                         |
| 12    | Manual dev → prod promotion flow                                  | Defined in [[knowledge-architecture]] §9, not yet exercised                                                                   | M9                         |
| 13    | MFA on all critical services                                      | Xano done; GitHub, Stripe, Resend, AWS and OpenAI to confirm                                                                  | M9                         |
| 14    | Secrets in environment variables                                  | Done                                                                                                                          | —                          |
| 15    | Sentry (frontend minimum)                                         | Frontend done (004). Elevated: backend reporting is now a launch requirement                                                  | M1 (context), M9 (backend) |
| 16    | user id + profile id in logs and events                           | Not done                                                                                                                      | M1                         |
| 17    | Basic error alerting (email)                                      | Not done                                                                                                                      | M9                         |
| 18    | Gitleaks in CI                                                    | Repo scanned once (B0, 24/10); not yet in CI                                                                                  | M1                         |
| 19    | Initial secret scan and key rotation                              | Done (B0 scan; LLM-wiki keys, HPBC token and docs token rotated)                                                              | —                          |
| 20    | Dependency audit                                                  | **Done 30/10**: `pnpm audit` (high) in CI, five documented exceptions (repo-sync RS-2026-10-24-03)                            | —                          |
| 21    | Semgrep (SAST, high only)                                         | Not done                                                                                                                      | M1                         |
| 22    | CI blocking for merges                                            | Partly: `main` needs a PR (ruleset); CI now green on pnpm and runs on wip PRs; make the CI check required on `main` at B12    | B12 / M1                   |
| 23–26 | Map journeys; auth, story/ownership, moderation and payment tests | Backend journeys covered by Postman `_tests` ([[test-suite]]); frontend tests and the moderation/approval journey outstanding | M3, then per slice         |
| 27    | Migrate to pnpm                                                   | **Done 30/10** (B10, PR #12)                                                                                                  | —                          |
| 28    | Naming conventions across the schema                              | Closed: `users_id` ratified ([[ratify-users-id-as-ownership-field-standard]])                                                 | —                          |
| 29    | Join tables for child visibility                                  | Not for V1: single `user_profiles_id` per story ([[per-child-story-visibility]]); revisit with sharing                        | Post-V1                    |

Requirements outside the phase tables that are still open: rate limiting (§4.1), sensitive data flagging and the hidden-fields sweep (§4.6), signed URLs for files (§2.9), Sentry context and backend event logging (§8.2, §8.4), and the dependency policy (§5.4–5.5, applied from M1). Each is placed in M1 or M9 above.

## 6. Background track: image pipeline off Xano

Raised by Kyle on 28/10. The goal is **cost**, not only speed: moving generation off Xano onto AWS (Bedrock and/or a queue-based worker) so most post-launch running costs can be covered by credits, and early revenue goes into marketing. It builds on [[defer-image-pipeline-throughput-to-phase-2]] and pairs naturally with S3 signed URLs ([[migrate-image-storage-to-aws-s3-signed-urls]]): images generated on AWS can land in S3 directly.

- **Inputs (Kyle, 28/10):** £25k GCP and £10k AWS credits, both expiring 30/06/2027 (about five months after launch). Character consistency across pages is already a problem with `gpt-image-1.5`. Preferred shape: storage on AWS, images from Google models, keeping the Xano orchestrator → worker tick → executor cycle with new `data_models` records and minimal infrastructure.
- **Working assumption to test:** Google's image models (Gemini image, Imagen) are API-only on Vertex AI, not models you can host on your own VMs, so credits apply when Vertex is called and billed on GCP. The simplest version then needs no VMs: the Xano executors call Vertex AI instead of OpenAI, and write images to S3. Throughput stays Xano-bound until a later step moves the executor to Cloud Run or Lambda.
- **Now (background, off the critical path):** a research note covering cost per story today vs on Vertex; which Vertex models handle character consistency (multi-image reference input); whether the credit terms cover Vertex AI; Vertex auth from Xano (a service-account token signed with RS256); S3 uploads and signed URLs from Xano (note: Xano already authenticates to Google Cloud with a service account and uploads to a GCS bucket in `create_tts_audio`, so Google-side storage is also an option); and what happens to costs after June 2027. Added by Kyle, 28/10:
  - **Other credit-eligible models:** on Vertex AI, Imagen, Gemini image and the open models in Model Garden (e.g. FLUX, SDXL) deployed to Vertex endpoints; on Bedrock, the Stability and Amazon image models currently offered (check what's still available).
  - **Concurrency and speed:** several GPU workers in parallel (GCP or AWS), scale-to-zero vs always-on (idle GPUs burn credits), cold starts. The real limit today is Xano dispatching one job at a time, so parallel workers need a hand-off: Xano queues the job externally and the worker posts the result back to a webhook, like the HPBC callbacks.
  - **LoRA pipelines:** start from the **SDXL + LoRA + IP-Adapter pipeline in the CfI "Boosting Fathers' Engagement" application** (`Project/Research/Research Proposals/CFI Boosting Fathers Engagement/`: project plan, cost model and draft). It covers LoRA training per art style on SageMaker, IP-Adapter for character conditioning, and evaluation against a golden dataset for multi-character bleed. Earlier background, imported 28/10: [[bedrock-image-migration-plan-2026-04]] (Bedrock → self-hosted ComfyUI on GPU for LoRA → two-stage img2img, with a cost model) and [[latent-preserving-regeneration-2026-05]]. Product idea on record: trained per-character LoRAs as a premium upsell.
- **Decision point:** before M8. Either build before launch (together with the S3 change in M9) or as the first post-launch milestone.
- **Contract to keep:** `image_jobs` stays the interface. The app and story flow shouldn't change whichever side runs the work.

## 7. After V1

Push notifications, Universal Links, story sharing, the public library, AI character creation if it isn't in V1, phonics (scope undecided: depends on how complex revealing it during text generation is).

## 8. Velocity log

Actual working days per milestone, against the estimate, for the checkpoint after M2.

| Milestone | Estimate (days) | Actual (days) | Finished |
|---|---|---|---|
| M0 Finish restructure | ~1 | | |
| M1 App foundations rework | 2–3 | | |
| M2 Characters (007) | 3–4 | | |
