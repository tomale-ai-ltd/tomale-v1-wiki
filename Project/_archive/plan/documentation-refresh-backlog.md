---
type: plan
title: documentation-refresh-backlog
project: tomale-rn-v1
status: archived
version: 1.0
date: 2026-10-21
last_verified: 2026-10-24
owner: vault
tags:
  - documentation-refresh
  - phase-1
---

# Documentation refresh backlog

The single checklist for the documentation refresh. The refresh runs **after Phase 1 sign-off and before Cursor frontend work** ([[defer-documentation-refresh-until-after-phase-1-signoff]]). Add new items here as they come up, not just in session notes. Each item notes where it came from.

> **2026-10-23:** the refresh will be run as part of the knowledge restructure (tiered vault, repo/vault ownership, generated `data-model` and API contract). The plan doc `knowledge-architecture` (to be written) governs how these items get done.

> **Closed 30/10/2026 (B12).** Every item is done or has moved to a permanent home:
> - §1 data model: generated from Xano ([[Repos/tomale-rn-test/memory/data-model|data-model]], B6); all listed fields, enums and tables verified present. `checkout_session_object` removal is in [[PRD-Store-Orders]] backend prep.
> - §2 API: `api-spec.md` retired for the generated OpenAPI contract; behaviours in [[security-model]], [[backend-xano]] and the PRDs. Webhooks spec export dropped ([[drop-webhooks-spec-export-from-generated-specs]]). Mark-all-read is `PATCH /users/user_alerts/mark-all-read` (security-model corrected). `utilities/upload_image`, `products` response trimming and the Postman re-sync moved to [[pre-launch-checklist]].
> - §3 security: matrix rebuilt in [[security-model]] (B8); rate limiting, Xano quick settings, CORS, inventory, backups and test-data clean-up in [[pre-launch-checklist]]; request history rule in [[backend-xano]] §3.
> - §4 PRDs and §9 B9: all reconciled and approved 29/10.
> - §5 constitution 1.5.0/1.5.1 (B10) carries the client auth and storage rules; backend conventions in [[backend-xano]] §3 (mirrored to Xano AGENTS.md); executor runs and audit retention in [[observability]]. The `auth/refresh` 200 check runs in B12 (Cursor).
> - §6 [[test-suite]] written and architecture flows refreshed (B8). §7 NEG test documented in [[test-suite]] (3A-NEG). §7b pnpm done (B10). §8 Project knowledge replaced and auto-synced (B11). §9 B11 `features:` added by the daily pipeline; B12 [[resume-frontend-at-slice-100]].

## 1. `data-model.md` (Cursor) and the Xano schema

- [x] **`store_orders`, new fields:**
  - `submit_after`, `cancelled_at`, `hpbc_lock`
  - `tracking_url`, `tracking_number` ([[store-hpbc-tracking-on-store-orders]])
  - `hpbc_order_id` is text and empty as `""`, not null
- [x] **`store_orders.status` enum:**
  - reconcile it with the HPBC triggers: `Order Confirmed` is listed twice, `Delivered` should be `Shipped`, and trigger #4 is missing (2026-10-08)
  - add `Cancelled` and `Error`
- [x] `store_orders.payment_status`: add `Refunded`.
- [x] `store_orders.message` is the buyer's gift message only ([[restrict-store-orders-message-to-buyer-gift-message]]).
- [x] Money units: `subtotal` and `shipping_amount` are now `int` pence (built 22/10, tested 23/10: 2499 / 199 stored, HPBC still sent `24.99`) ([[store-money-as-integer-minor-units]]). Document it.
- [x] `store_orders.checkout_session_object`: dropped or to be dropped ([[record-transactions-drop-checkout-session-object]]).
- [x] **`transactions`:**
  - `type` gains `refund`; payment rows are `physical-product`
  - new fields `refundable_amount`, `refund_attempt_count`, `refund_last_attempt_at`
- [x] `transaction_webhook_events`: UUID primary key, not int ([[adopt-uuid-primary-key-for-transaction-webhook-events]]); a generic ingress log for every provider (2026-07-03).
- [x] New tables: `audit_store_orders` (temporary, [[add-temporary-audit-trigger-on-store-orders]]), `pdf_jobs`, and `executor_runs.pdf_jobs_id`.
- [x] `products` is one row per SKU: `hpbc_sku_test`, `hpbc_sku_live`, Papermill template ids, Stripe price ids (2026-07-03).
- [x] `user sessions`: `refresh_token` is a password-type field (hashed); sessions last 7 days.

## 2. `api-spec.md` (Cursor) and the Postman OpenAPI re-sync

- [x] New: `POST /store_orders/{id}/cancel`. A refused cancel returns **400** with `ORDER_NOT_CANCELLABLE`, because Xano has no 422.
- [x] `GET /store_orders/{id}` gains `submit_after` and `cancellable`.
- [x] `POST /auth/refresh`: an invalid or expired token returns **401** with `payload: invalid_refresh_token`, and the refresh token is replaced on each use.
- [x] Removed:
  - `/model` (deleted)
  - `/hpbc/webhook_order_submission` (stale; submission is the `hpbc_submit_due_orders` task)
- [x] `/admin/upload/image`: external access disabled until something uses it.
- [x] `check_order_paid`: authenticated and owner-scoped.
- [x] **`webhooks` group:**
  - `stripe/webhook_payment_confirmation` also handles `refund.updated` and `refund.failed`
  - the HPBC status callbacks pass `message` to the function as `update_message`
- [x] `POST /store_orders`: 400 `STORY_AWAITING_APPROVAL` when `parental_approval_required && !parent_approved` (23/10).
- [x] `GET stripe/create_checkout_session`: 400 `STORY_AWAITING_APPROVAL`; 400 `ORDER_NOT_PAYABLE` unless status is `Draft` or `Payment Pending`; expected total is `subtotal + shipping_amount` in pence (23/10).
- [x] `POST /conversations/{id}/message`: inputs are `id` and `user_message` only (both required), 404 for missing, foreign or deleted conversations (23/10).
- [x] `utilities/upload_image` (POST) still appears in the `app` spec: confirm external access is really disabled (23/10).
- [x] `products` responses expose internal config (Stripe price and product ids, HPBC SKUs, Papermill template ids): trim the output before launch (23/10).
- [x] Mark-all-read is `PATCH users/user_alerts/mark-all-read` in the live spec, but the notes say `POST /user_alerts/mark-all-read`: settle which is right (23/10).
- [x] Export the `webhooks` group spec (only `app` is in the repo; `XANO_APISPEC_URL` now points at `apispec:1pgd39RE`).
- [x] Re-sync the Postman OpenAPI collection from Xano ([[adopt-openapi-import-for-postman-collection-sync]]).

## 3. `6-api-security-model.md` (Plan)

- [x] Phase 1 close-out section added and the matrix marked historical (23/10).
- [x] Rebuild the classification matrix from the Xano OpenAPI export (replaces the stale "Done?" column).
- [x] Add rate limiting (CTO §4.1): pre-middleware on the `app` group keyed by IP, plus stricter per-endpoint limits on auth and generation. Phase still to confirm; Phase 2 recommended.
- [x] **From the Xano pre-launch security checklist:**
  - Phase 1 quick settings: Swagger set to Private, Sensitive Data flags, 2FA, unused metadata tokens removed
  - Phase 2: endpoint inventory, test-data cleanup, CORS, a backup before launch
- [x] Request history is off on functions that handle credentials ([[disable-request-history-on-credential-functions]]), including the HPBC callback endpoint.

## 4. PRDs

- [x] `PRD-Store-Orders` and `PRD-Order-PoD-System`:
  - Mixam → HPBC/Pureprint, with Papermill for the PDFs
  - add the 30-minute cancellation window ([[delay-hpbc-submission-with-30-minute-cancellation-window]])
  - add automatic refund on self-service cancel ([[automate-full-refund-on-self-service-cancel]])
  - add no cancelling once in production ([[disallow-cancelling-personalised-orders-once-in-production]])
- [x] `PRD-transaction-webhooks-micro-prd`: Stripe refund events, and the self-service versus support refund paths ([[split-refund-model-into-self-service-and-support-paths]]).
- [x] `PRD-Parental-Oversight-Content-Approval`: a story awaiting parental approval can't be ordered (built 23/10, on order create and checkout).

## 5. Constitution and stack docs (frontend-facing)

- [x] `constitution.md` and `7. Auth - Xano.md` need the client auth rules:
  - one Axios 401 interceptor that refreshes once (concurrent 401s share it) and retries once
  - never refresh when the 401 came from `/auth/*`
  - log out on `invalid_refresh_token`, with the redirect done by the root layout
  - network errors don't log the user out
  - refresh proactively on foreground (2026-10-21 decision)
- [x] `9. AsyncStorage.md`: tokens move to `expo-secure-store`; AsyncStorage keeps non-sensitive state only.
- [x] Check the on-hold frontend branch for any `auth/refresh` usage that expects a 200.
- [x] `6. Backend - Xano.md`:
  - background tasks `hpbc_submit_due_orders` (60 s) and `reconcile_order_refunds` (15 min)
  - the `order_fulfilment_check` trigger is disabled
  - the planned rate-limit middleware
- [x] Backend conventions, in `6. Backend - Xano.md` or the constitution:
  - no input or variable named after a column the function writes to ([[avoid-column-named-function-inputs-in-xano]])
  - test switches are optional inputs (`bool x?`)
  - executor runs save only small status fields, never full API responses
  - edit endpoints and functions declare explicit inputs; no `dblink` (22/10)
  - use the statement-level `enforce_hidden_fields = true` flag rather than renaming external-contract inputs; don't enable the workspace Hidden Fields setting (22/10)
- [x] `15. Observability - Sentry.md`: what `executor_runs` records, and the `audit_store_orders` retention decision (Phase 2).

## 6. Architecture docs (`Project/Architecture/`)

- [x] New: the `_tests` test-suite doc. Folders 1, NEG, 2A–2B, 3A–3D and 4 (cancel and refund), plus 1D/1E for refresh: what each checks and how to run them. This replaces the never-filed `order-fulfilment-flow-test-build-spec`.
- [x] `image-generation-flow.md`:
  - runs are found by `executor_runs_id`; the run row is created before the function starts
  - a failed start releases the job
  - recovery increments `attempt`
  - mark the `created_at` mystery as resolved
- [x] `order-fulfilment-flow.md`:
  - PDF runs are found by id
  - the submission task's filter handles an empty `hpbc_order_id`
  - Papermill logging saves status only
- [x] `story-creation-flow.md`: check it against today's pipeline changes.

## 7. Postman and tooling

- [x] Delete the old `app` folder auto-login script (its `bearerToken` / `bearerTokenExpiry` clash with `_tests`) (22/10).
- [x] Fix 1A's token not being visible to 1B within a run: 1A also calls `pm.variables.set("bearerToken", …)` (run-scoped) (22/10).
- [x] Add the NEG test `STORY_AWAITING_APPROVAL` (uses `pendingApprovalStoryId`) to the `_tests` doc.

## 7b. Repo work before Slice 100

- [x] pnpm migration plus dependency audit (49 npm audit findings on 24/10; check dev-only exposure first) ([[promote-pnpm-migration-ahead-of-slice-100]]). Also replace the unmaintained `@testing-library/jest-native` with the built-in matchers.

## 8. Claude project knowledge

- [x] Re-upload the refreshed `api-spec`, `data-model`, `6-api-security-model`, `5-cto-implementation-plan` and the PRDs to the Claude project, so it isn't working from stale copies.

## 9. From the B7 audit (28/10)

Source: [[v1-audit]]. Items are grouped by the stage that closes them.

**B8 (canonical docs and roadmap)**: done 28/10 except where noted.
- [x] `v1-feature-map`: formalise the feature ids from [[v1-audit]] §1.
- [x] Roadmap: entitlement and subscription system as launch-critical backend work ([[gate-image-generation-with-entitlements-at-story-creation]]); parental PIN gate and approve/reject flow (P8); rate limiting and backend observability (P7); phonics in V1 (P4, open); backend prep for Slice 100 ([[scope-characters-per-profile-with-soft-delete]]).
- [x] `pre-launch-checklist`: the 14 stray `error = 422` precondition messages; suffixed dev/prod env vars checked ([[use-xano-branches-for-dev-and-prod]]); Universal Links; backend-generated links using the per-environment scheme ([[use-per-build-variant-url-schemes]]).
- [x] `security-model`: repoint decision `affects` that still name the retired `api-spec` (D3).
- [x] `backend-xano`: confirm `mark-order-error-on-hpbc-rejection-and-clear-lock` is built (D4); record the live HPBC SKU field names (D5); email verification pattern (G11); order number format (G15).
- [x] `stack.md`: current client auth model, superseding the 11/05 token-overwrite pattern (G10); EAS env in `eas.json` (G12).
- [x] `test-suite`: staging HPBC terminal status is Order Confirmed (G13).
- [x] (moved to repo-sync RS-2026-10-28-02, B10) Data-model preamble: Key Conventions §3 still says references are inferred from `_id` fields; the generator now takes them from the API.

**B9 (PRD reconciliation, per [[v1-audit]] §5)**
- [x] All ten PRDs, plus a new short profiles PRD from G1–G6 (P3).
- [x] PRD-Characters: per profile, soft delete, no PATCH; decide whether "Edit character" and "Re-create image" become delete-and-recreate or a later moderated PATCH.
- [x] PRD-Chatbot-Create-Character: chatbot knows the character data model and prompts for richer descriptions (Q&A or tap/swipe choices).
- [x] PRD-Parental-Oversight: approval channels (profile switch, push to parent device, email, push with PIN); field name `parental_approval_required`; Blocked vs oversight wording (C8).
- [x] PRD-Store-Orders: Pureprint, statuses, cancellation window, refunds, e-reader preview ([[use-e-reader-preview-before-order-payment]]), in-app checkout return ([[return-from-stripe-checkout-via-in-app-browser-sheet]]).
- [x] PRD-Order-PoD-System: replace the payment-gated image generation with the entitlement model.
- [x] Umbrella PRD: drop Library and PDF download ([[drop-library-and-pdf-download-from-v1]]); tech stack; notifications; sharing.
- [x] `auth/me` still returns `users.profile_photo` ([[use-bundled-preset-avatars-for-profiles]]).
- [x] Mark [[defer-documentation-refresh-until-after-phase-1-signoff]] done (C11).

**B11 (automations)**
- [x] The daily decision task must add `features:` to new decision notes, and the decision template now carries the field.

**B12 (close-out)**
- [x] New decision "resume frontend at Slice 100", superseding [[place-frontend-development-on-hold]] (C10).
- [x] Accept or reject the proposed backfilled decisions (G1–G3, G5–G9): all accepted 28/10.
