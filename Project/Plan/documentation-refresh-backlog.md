---
type: plan
title: documentation-refresh-backlog
date: 2026-10-21
status: current
project: tomale-rn-v1
tags:
  - documentation-refresh
  - phase-1
---

# Documentation refresh backlog

The single checklist for the documentation refresh. The refresh runs **after Phase 1 sign-off and before Cursor frontend work** ([[defer-documentation-refresh-until-after-phase-1-signoff]]). Add new items here as they come up, not just in session notes. Each item notes where it came from.

> **2026-10-23:** the refresh will be run as part of the knowledge restructure (tiered vault, repo/vault ownership, generated `data-model` and API contract). The plan doc `knowledge-architecture` (to be written) governs how these items get done.

## 1. `data-model.md` (Cursor) and the Xano schema

- [ ] **`store_orders`, new fields:**
  - `submit_after`, `cancelled_at`, `hpbc_lock`
  - `tracking_url`, `tracking_number` ([[store-hpbc-tracking-on-store-orders]])
  - `hpbc_order_id` is text and empty as `""`, not null
- [ ] **`store_orders.status` enum:**
  - reconcile it with the HPBC triggers: `Order Confirmed` is listed twice, `Delivered` should be `Shipped`, and trigger #4 is missing (2026-10-08)
  - add `Cancelled` and `Error`
- [ ] `store_orders.payment_status`: add `Refunded`.
- [ ] `store_orders.message` is the buyer's gift message only ([[restrict-store-orders-message-to-buyer-gift-message]]).
- [ ] Money units: `subtotal` and `shipping_amount` are now `int` pence (built 22/10, tested 23/10: 2499 / 199 stored, HPBC still sent `24.99`) ([[store-money-as-integer-minor-units]]). Document it.
- [ ] `store_orders.checkout_session_object`: dropped or to be dropped ([[record-transactions-drop-checkout-session-object]]).
- [ ] **`transactions`:**
  - `type` gains `refund`; payment rows are `physical-product`
  - new fields `refundable_amount`, `refund_attempt_count`, `refund_last_attempt_at`
- [ ] `transaction_webhook_events`: UUID primary key, not int ([[adopt-uuid-primary-key-for-transaction-webhook-events]]); a generic ingress log for every provider (2026-07-03).
- [ ] New tables: `audit_store_orders` (temporary, [[add-temporary-audit-trigger-on-store-orders]]), `pdf_jobs`, and `executor_runs.pdf_jobs_id`.
- [ ] `products` is one row per SKU: `hpbc_sku_test`, `hpbc_sku_live`, Papermill template ids, Stripe price ids (2026-07-03).
- [ ] `user sessions`: `refresh_token` is a password-type field (hashed); sessions last 7 days.

## 2. `api-spec.md` (Cursor) and the Postman OpenAPI re-sync

- [ ] New: `POST /store_orders/{id}/cancel`. A refused cancel returns **400** with `ORDER_NOT_CANCELLABLE`, because Xano has no 422.
- [ ] `GET /store_orders/{id}` gains `submit_after` and `cancellable`.
- [ ] `POST /auth/refresh`: an invalid or expired token returns **401** with `payload: invalid_refresh_token`, and the refresh token is replaced on each use.
- [ ] Removed:
  - `/model` (deleted)
  - `/hpbc/webhook_order_submission` (stale; submission is the `hpbc_submit_due_orders` task)
- [ ] `/admin/upload/image`: external access disabled until something uses it.
- [ ] `check_order_paid`: authenticated and owner-scoped.
- [ ] **`webhooks` group:**
  - `stripe/webhook_payment_confirmation` also handles `refund.updated` and `refund.failed`
  - the HPBC status callbacks pass `message` to the function as `update_message`
- [ ] `POST /store_orders`: 400 `STORY_AWAITING_APPROVAL` when `parental_approval_required && !parent_approved` (23/10).
- [ ] `GET stripe/create_checkout_session`: 400 `STORY_AWAITING_APPROVAL`; 400 `ORDER_NOT_PAYABLE` unless status is `Draft` or `Payment Pending`; expected total is `subtotal + shipping_amount` in pence (23/10).
- [ ] `POST /conversations/{id}/message`: inputs are `id` and `user_message` only (both required), 404 for missing, foreign or deleted conversations (23/10).
- [ ] `utilities/upload_image` (POST) still appears in the `app` spec: confirm external access is really disabled (23/10).
- [ ] `products` responses expose internal config (Stripe price and product ids, HPBC SKUs, Papermill template ids): trim the output before launch (23/10).
- [ ] Mark-all-read is `PATCH users/user_alerts/mark-all-read` in the live spec, but the notes say `POST /user_alerts/mark-all-read`: settle which is right (23/10).
- [ ] Export the `webhooks` group spec (only `app` is in the repo; `XANO_APISPEC_URL` now points at `apispec:1pgd39RE`).
- [ ] Re-sync the Postman OpenAPI collection from Xano ([[adopt-openapi-import-for-postman-collection-sync]]).

## 3. `6-api-security-model.md` (Plan)

- [x] Phase 1 close-out section added and the matrix marked historical (23/10).
- [ ] Rebuild the classification matrix from the Xano OpenAPI export (replaces the stale "Done?" column).
- [ ] Add rate limiting (CTO §4.1): pre-middleware on the `app` group keyed by IP, plus stricter per-endpoint limits on auth and generation. Phase still to confirm; Phase 2 recommended.
- [ ] **From the Xano pre-launch security checklist:**
  - Phase 1 quick settings: Swagger set to Private, Sensitive Data flags, 2FA, unused metadata tokens removed
  - Phase 2: endpoint inventory, test-data cleanup, CORS, a backup before launch
- [ ] Request history is off on functions that handle credentials ([[disable-request-history-on-credential-functions]]), including the HPBC callback endpoint.

## 4. PRDs

- [ ] `PRD-Store-Orders` and `PRD-Order-PoD-System`:
  - Mixam → HPBC/Pureprint, with Papermill for the PDFs
  - add the 30-minute cancellation window ([[delay-hpbc-submission-with-30-minute-cancellation-window]])
  - add automatic refund on self-service cancel ([[automate-full-refund-on-self-service-cancel]])
  - add no cancelling once in production ([[disallow-cancelling-personalised-orders-once-in-production]])
- [ ] `PRD-transaction-webhooks-micro-prd`: Stripe refund events, and the self-service versus support refund paths ([[split-refund-model-into-self-service-and-support-paths]]).
- [ ] `PRD-Parental-Oversight-Content-Approval`: a story awaiting parental approval can't be ordered (built 23/10, on order create and checkout).

## 5. Constitution and stack docs (frontend-facing)

- [ ] `constitution.md` and `7. Auth - Xano.md` need the client auth rules:
  - one Axios 401 interceptor that refreshes once (concurrent 401s share it) and retries once
  - never refresh when the 401 came from `/auth/*`
  - log out on `invalid_refresh_token`, with the redirect done by the root layout
  - network errors don't log the user out
  - refresh proactively on foreground (2026-10-21 decision)
- [ ] `9. AsyncStorage.md`: tokens move to `expo-secure-store`; AsyncStorage keeps non-sensitive state only.
- [ ] Check the on-hold frontend branch for any `auth/refresh` usage that expects a 200.
- [ ] `6. Backend - Xano.md`:
  - background tasks `hpbc_submit_due_orders` (60 s) and `reconcile_order_refunds` (15 min)
  - the `order_fulfilment_check` trigger is disabled
  - the planned rate-limit middleware
- [ ] Backend conventions, in `6. Backend - Xano.md` or the constitution:
  - no input or variable named after a column the function writes to ([[avoid-column-named-function-inputs-in-xano]])
  - test switches are optional inputs (`bool x?`)
  - executor runs save only small status fields, never full API responses
  - edit endpoints and functions declare explicit inputs; no `dblink` (22/10)
  - use the statement-level `enforce_hidden_fields = true` flag rather than renaming external-contract inputs; don't enable the workspace Hidden Fields setting (22/10)
- [ ] `15. Observability - Sentry.md`: what `executor_runs` records, and the `audit_store_orders` retention decision (Phase 2).

## 6. Architecture docs (`Project/Architecture/`)

- [ ] New: the `_tests` test-suite doc. Folders 1, NEG, 2A–2B, 3A–3D and 4 (cancel and refund), plus 1D/1E for refresh: what each checks and how to run them. This replaces the never-filed `order-fulfilment-flow-test-build-spec`.
- [ ] `image-generation-flow.md`:
  - runs are found by `executor_runs_id`; the run row is created before the function starts
  - a failed start releases the job
  - recovery increments `attempt`
  - mark the `created_at` mystery as resolved
- [ ] `order-fulfilment-flow.md`:
  - PDF runs are found by id
  - the submission task's filter handles an empty `hpbc_order_id`
  - Papermill logging saves status only
- [ ] `story-creation-flow.md`: check it against today's pipeline changes.

## 7. Postman and tooling

- [x] Delete the old `app` folder auto-login script (its `bearerToken` / `bearerTokenExpiry` clash with `_tests`) (22/10).
- [x] Fix 1A's token not being visible to 1B within a run: 1A also calls `pm.variables.set("bearerToken", …)` (run-scoped) (22/10).
- [ ] Add the NEG test `STORY_AWAITING_APPROVAL` (uses `pendingApprovalStoryId`) to the `_tests` doc.

## 7b. Repo work before Slice 100

- [ ] pnpm migration plus dependency audit (49 npm audit findings on 24/10; check dev-only exposure first) ([[promote-pnpm-migration-ahead-of-slice-100]]). Also replace the unmaintained `@testing-library/jest-native` with the built-in matchers.

## 8. Claude project knowledge

- [ ] Re-upload the refreshed `api-spec`, `data-model`, `6-api-security-model`, `5-cto-implementation-plan` and the PRDs to the Claude project, so it isn't working from stale copies.
