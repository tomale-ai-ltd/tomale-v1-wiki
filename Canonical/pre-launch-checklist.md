---
type: living-doc
title: pre-launch-checklist
project: tomale-rn-v1
status: current
version: 1.3
date: 2026-10-28
last_verified: 2026-11-24
owner: vault
related:
  - "[[roadmap]]"
  - "[[security-model]]"
  - "[[backend-xano]]"
---

# Pre-launch checklist

Everything that must be true before the public release, in one place. Items were previously spread across decisions, session notes and the security model. Most are in milestone M9 or M10 of the [[roadmap]]. Tick items here, with the date and evidence.

## 1. Backend security

- [ ] **Hidden-fields sweep:** `enforce_hidden_fields` enforced on every `db.add` / `db.edit` (199 statements say `false` today), columns mapped explicitly, `output` lists added; then a full `_tests` run ([[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]]).
- [ ] **Rate limiting:** per-endpoint limits on auth, order create/cancel and story/image generation, plus an IP pre-middleware on the `app` group if `$env` allows it ([[add-per-endpoint-rate-limiting-in-xano]]; CTO §4.1).
- [ ] **Request history off** on token-issuing auth endpoints (`auth/login` is 100 today) ([[keep-request-history-on-auth-endpoints-until-pre-launch]]).
- [x] **Parental PIN gate** on `auth/select_profile` (done 12/11, Postman folder 6; [[parental-gate-on-profile-switch]], [[m3-profiles-pin-backend-prep-brief]]).
- [x] **`user_profiles.is_child` required** (done 12/11 after checking no rows were null).
- [x] **`GET /instant_stories/{id}`** no longer returns the account owner's email and name (users addon removed 12/11), and no longer fails on a story with no characters.
- [ ] **Slice 300: give `GET /instant_stories/{id}` an explicit output list.** It returns the whole story record (`db.get` with no output). For a child profile, leave out `blocked_reason`, `approved_by_profile_id`, `approved_at` and `approval_rejected_at` (parent-only approval fields since M3 B5). The app doesn't show them; the server should still not send them ([[security-model]]; PU-2026-11-13-01).
- [x] **`POST /characters/{id}/model` deleted** (12/11): it could queue unlimited image jobs; create runs the model.
- [x] **`auth/reset_password` deleted** (12/11): public, never checked the emailed code, returned the user record. Forgotten password = email link login.
- [ ] **Restored session and the PIN:** a refresh returns a token for the last active profile, which may be the parent; the app must show the picker and require the PIN before using it. Server-side enforcement would need refresh to downgrade the token (not in V1; revisit before launch).
- [ ] **Precondition messages:** replace the 14 `error = 422` messages, and about 20 others that put a status number (`404`, `401`, `500`, `413`, `415`) in `error`, with real text. The status comes from `error_type` ([[backend-xano]] §3).
- [ ] **Account closing and deletion** (App Store guideline 5.1.1(v)): close, reopen within 30 days, then the daily purge job deletes the account and its content; orders and payments kept 6 years; soft-deleted items purged after 30 days ([[account-closing-micro-prd]], [[retain-account-data-30-days-after-closing]]).
- [ ] **Endpoint inventory** against [[security-model]] §3; remove the legacy functions (`mixam_*`, `make_com_*`, `mixpanel_import_event`).
- [ ] **CORS** settings reviewed for both groups.
- [ ] **Signed URLs for user images:** decide before launch or immediately after; all images are public URLs today ([[migrate-image-storage-to-aws-s3-signed-urls]]; CTO §2.9).
- [ ] **MFA** on GitHub, Stripe, Resend, AWS and OpenAI (Xano done) (CTO #13).
- [ ] **Xano quick settings:** Swagger/API docs set to private for both groups; Sensitive Data flags on credential and PII fields; unused Metadata API tokens removed (keep the read-only `cursor-read` token).
- [ ] **Response trimming:** `products` responses expose internal config (Stripe price and product ids, HPBC SKUs, Papermill template ids); return only what the app shows.
- [ ] **`utilities/upload_image`** still appears in the `app` spec: confirm external access is disabled, or remove it.
- [ ] **Postman collection re-synced** from the Xano OpenAPI export ([[adopt-openapi-import-for-postman-collection-sync]]), then `_tests` run green.

- [x] Server-side sign-out (done 06/11: Xano `auth/logout` revokes the session; the app calls it on a user sign-out, PR #24; Postman 1F/1G): add `auth/logout` in Xano that revokes the session's refresh token (`user_sessions`), and call it from the app's logout. Today sign-out is client-only, so a signed-out refresh token stays valid until it expires (found 04/11 reviewing speckit 007).
- [ ] **Sign out of all devices:** a shared Xano function `auth/revoke_all_sessions` marks every `user_sessions` row for the account `revoked`; `POST /auth/logout_all` (parent profile only, `PARENT_PROFILE_REQUIRED`; PIN if set, `PIN_INVALID`) calls it, and account closing (B2 in [[account-closing-micro-prd]]) uses the same function. Open: revoking only stops refresh, so a 1-hour access token on another device keeps working until it expires; decide whether the auth check should look up the session on each request.
- [ ] **Emergency revoke-all (incident runbook):** an admin-only Xano function that revokes every session for every account, with the steps written in the runbook (when to use it: leaked token or signing key, signing change, breaking session change). Not run on app updates.
- [ ] **Email-confirmed gate on create:** `POST /characters`, `POST /instant_stories` and the conversation create endpoints refuse with `EMAIL_NOT_VERIFIED` while `users.email_verified` is false, so 010b's in-app lock isn't the only check. Add Postman cases with an unconfirmed account.
- [ ] **Purge never-confirmed accounts:** the daily purge job also hard-deletes accounts with `email_verified` false created more than 7 days ago, with their profiles and sessions (they can't have orders, payments or stories, because creating needs a confirmed email). No reminder email (Kyle, 24/11: someone who hasn't confirmed in a week signs up again). Postman case: an unconfirmed account older than the cutoff is gone after the job runs; a confirmed one is untouched.
- [ ] No AI model in use has an OpenAI or Google shutdown date before 30/06/2027. Check the OpenAI deprecations page and the Vertex model-versions page, and `GET /v1/models` `shutdown_date`.
- [ ] Image pipeline gate G2 passed and the cut-over done ([[PRD-Image-Pipeline]] §6), or the OpenAI record confirmed as default with a dated plan.
- [ ] Output image moderation live (`moderation-image`) ([[moderate-generated-images-in-three-layers]]).
- [ ] Budgets and alerts on both clouds at 25/50/75% of credits.
- [ ] DPIA covers Vertex `eu` processing of generated character pictures.

## 2. Environments and money

- [ ] **Dev/prod Xano branches** set up, env vars duplicated with suffixes where they differ, one dev → prod merge and publish rehearsed ([[use-xano-branches-for-dev-and-prod]]; CTO #10–#12).
- [x] **New sign-ups get `test_mode = false`** (fixed in Xano 06/11). Before the fix, `auth/signup` wrote `test_mode: ""`. Stripe and the HPBC SKU are chosen from it and fail closed to test, so real customers' orders would go to test keys and the test SKU.
- [ ] **Stripe live:** live keys and live webhook secret in the prod branch; the live webhook endpoint registered.
- [ ] **HPBC live:** `hpbc_sku_live` set on every product; live callback URLs and bearer token registered with HPBC.
- [ ] **Papermill and OpenAI** production keys in prod.
- [ ] **Resend:** `tomale.ai` sender domain verified (SPF, DKIM, DMARC); templates recreated from SendGrid.
- [ ] **Test data cleaned:** test users, orders, stuck stories ([[purge-stuck-stories-with-manual-admin-function]]).
- [ ] **Backups:** a manual Xano snapshot plus a workspace export, stored encrypted outside the vault and repo.
- [ ] `audit_store_orders`: keep or remove ([[add-temporary-audit-trigger-on-store-orders]]).

## 3. Observability

- [ ] **Backend errors to Sentry** (try/catch + External API Request) on webhooks, executors, fulfilment and refunds ([[elevate-backend-observability-to-launch-requirement]]; CTO #15).
- [ ] **Email alerting** on repeated errors and crash spikes (CTO #17).
- [x] **App Sentry events** carry user and active-profile context (CTO #16): done 06/11 in 007 (account id and active profile id only; checked on a device).
- [ ] **Sentry location:** events carry `user.geo` down to city, derived by Sentry from the ingest IP (the SDK sends none). Turn on Project → Security & Privacy → "Prevent Storing of IP Addresses"; if `user.geo` still appears on a new event, add an Advanced Data Scrubbing rule removing the user's geo fields (ICO Children's Code).
- [ ] **Postman daily monitor** under the 10-minute limit ([[defer-postman-monitor-until-launch]]).

## 4. App and build

- [ ] **`eas.json` base URL** points at the `app` group (`api:1pgd39RE`); today every profile uses the old `api:T6T6tF5a`.
- [ ] **Production scheme `tomale://`** through `app.config.js`; backend-generated links (alert `action_url`, checkout return) use the per-environment scheme; `tomalerntest://` is hard-coded in two pipeline functions today ([[use-per-build-variant-url-schemes]]).
- [ ] **Universal Links / App Links** (`https://tomale.ai/app/*`), or a recorded decision to launch without them.
- [ ] **Tokens in SecureStore** and the 401 interceptor in place ([[use-expo-secure-store-for-client-tokens]], [[use-axios-401-interceptor-for-client-auth-session-handling]]).
- [ ] **Dependency audit** clean of high/critical, with pnpm (CTO #20, #27).
- [ ] **CI security stage** (Gitleaks, Semgrep, audit) required on `main` (CTO #18, #21, #22).
- [ ] **Avatar licence credit** in the app if the avatar set needs attribution ([[use-bundled-preset-avatars-for-profiles]]).

- [ ] **Squarespace app-link pages use the production scheme:** `/verify-email` and `/app/approvals` hard-code `tomalerntest://`; switch to `tomale://` (or Universal Links) for the production app, and set Xano `app_url_scheme` per environment ([[use-per-build-variant-url-schemes]]).

## 4a. App build and release hygiene (added 04/11)

- [ ] Remove the stray `?user_id=` param from `GET /instant_stories` in `hooks/useBookshelf.ts` (Xano ignores it; it leaks the account id into URLs and breadcrumbs). Do it in Slice 300.
- [ ] Sentry source maps: remove `SENTRY_DISABLE_AUTO_UPLOAD` / `SENTRY_SKIP_AUTO_UPLOAD` in the EAS environments for production builds and confirm a readable stack trace in Sentry.
- [ ] Delete the five old EAS updates on the `production` branch (runtime `1.0.0`, ~Nov 2025 test updates). Harmless since the runtime version moved to `fingerprint`, but clutter.
- [ ] Remove the "OTA UPDATE APPLIED" test marker from the Home screen (goes with the real Home screen).
- [ ] Backend-generated links (alert `action_url`, magic-link redirect) use the production scheme `tomale://` for production ([[use-per-build-variant-url-schemes]], Xano dev/prod split).
- [ ] **Web pages open the right app.** `/app/approvals`, `/verify-email` and the magic-link page read `?app=` (allowlist `tomale` | `tomalerntest`, fallback `tomale`) and open `<app>://…`. Each Xano environment's link env vars (`approvals_url`, the verify-email and magic-link links) carry `?app=tomalerntest` (dev) or `?app=tomale` (production). Verify with both apps on one phone ([[pass-app-scheme-to-web-intermediary-pages]]; Xano dev/prod split).

## 5. App Store and Google Play (both in scope: [[CURRENT]] launch plan)

- [x] Production bundle id / Android package `ai.tomale.app`: iOS App ID registered 01/11. Permanent once the first store build is uploaded ([[use-ai-tomale-app-as-production-bundle-id]]).
- [x] App Store app record (App Store Connect): created 03/11, name "Tomale", English (U.K.), bundle ID `ai.tomale.app`, SKU `tomale-ios`.
- [x] Google Play organisation developer account for Tomale.ai Ltd: created and paid 01/11 (old account closed for inactivity, disclosed); contact verification done and kyle@tomale.ai added as admin 03/11. Owner account has 2-Step Verification.
- [x] Play app record (Play Console): created 03/11, name "Tomale", free, English (UK), package `ai.tomale.app`. The "Set up your app" tasks (privacy policy, app access, content rating, target audience under the Families policy, data safety) come later in this checklist.
- [ ] Privacy policy and terms published; privacy nutrition labels (and Google Data safety) completed.
- [ ] Age rating and category decided (children are users; parents hold the account and pay).
- [ ] In-app purchase products configured, if subscriptions are in the launch ([[roadmap]] §3).
- [ ] Checkout copy states that personalised orders can't be cancelled once in production, and the pre-payment preview is in place ([[disallow-cancelling-personalised-orders-once-in-production]], [[use-e-reader-preview-before-order-payment]]).
- [ ] Screenshots, description, support URL; reviewer test account with sample stories.
- [ ] TestFlight round passed; final `_tests` regression on prod.

## 6. Legal and compliance (research, then act)

- [ ] **Legal pages** published 19/11/2026 (Terms, Content Guidelines, Privacy Notice, Cookie Policy, EULA; [[Project/Legal/README|Legal README]]); still to do: a UK solicitor's review. The Terms date (2026-11-19) is `terms_version` in sign-up (010b, B2). Book Club is in the published Terms; revisit §7 if App Review refuses a subscription that includes a printed book.
- [ ] **Privacy Notice** brought in line with the terms: no AI training on user content; usage information only in a form that doesn't identify anyone; account data deleted 30 days after closing; order and payment records kept as tax law requires. Written so a parent, and a child where relevant, can follow it.
- [ ] **Content Guidelines** page (`https://www.tomale.ai/content-guidelines`): a public summary of the Xano content policy, not the policy prompts.
- [ ] **Electronic Commerce Regulations 2002:** confirm the hosting defence applies (stories and pictures held for a household) and what "acting expeditiously" on a report means for us; the reporting route is support email (terms §6). No US DMCA agent needed while Tomale is UK-only.
- [ ] **Online Safety Act 2023:** a short written assessment of whether Tomale is a user-to-user service (content shared only within one household; shared characters across profiles; `instant_stories.is_public` exists but is unused). If in scope: Ofcom's illegal-content and children's risk assessments. Reassess before any public or cross-household sharing.
- [ ] **UK GDPR and the ICO Children's Code:** ICO registration and data protection fee; a DPIA covering children's data, AI processing and moderation; a review against the Code's 15 standards (high-privacy defaults, no profiling, data minimisation, parental controls, plain-language information); data processing agreements with Xano, OpenAI and other AI providers, Resend, Sentry, Stripe, HPBC/Pureprint, Papermill and Squarespace; international transfer safeguards for US providers; a retention schedule (including the 30-day delete after closing, which needs a backend job).
- [ ] **Consumer law:** pre-contract information for subscriptions and print orders (Consumer Contracts Regulations 2013); the personalised-goods exemption wording; check whether the subscription-contract rules in the Digital Markets, Competition and Consumers Act 2024 are in force by launch and what they require (reminders, easy exit).
- [ ] **Advertising and in-app purchases to children:** the CAP Code and the CMA's principles for online and app-based games: no direct exhortation to children to buy or to ask a parent to buy. Check every child-profile screen, especially the "limit reached" message ([[PRD-Subscription-Entitlement-System]]), upgrade prompts, Store entry points and any marketing.
- [ ] **Product safety for printed books:** UK General Product Safety Regulations 2005 (who is the "producer", us or HPBC/Pureprint; traceability on the book or packing slip). Delivery to Northern Ireland brings in the EU GPSR's seller and labelling rules: confirm with HPBC, or decide on Great Britain only.
- [ ] **Ownership of AI output:** CDPA 1988 s9(3) (computer-generated works) is under government review; check the terms §5 wording ("as far as we have rights") with the solicitor.
- [ ] **VAT:** printed books are zero-rated and digital subscriptions standard-rated; confirm how prices are shown and how the Creator discount and Book Club's included book are treated.
