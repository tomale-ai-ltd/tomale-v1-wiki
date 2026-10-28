---
type: living-doc
title: backend-xano
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
last_verified: 2026-10-28
owner: vault
related:
  - "[[security-model]]"
  - "[[test-suite]]"
  - "[[stack]]"
---

# Backend: Xano

How the Xano backend is organised, the conventions every change follows, and the XanoScript gotchas that have cost time. Access rules are in [[security-model]]. Endpoint-level detail is in the code: the read-only mirror at `Repos/tomale-xano`, which is the source of truth (published code beats this page).

## 1. Workspace

| Item | Value |
|---|---|
| Workspace | `tomale.ai`, Launch plan |
| Branches | `v1` (live, the only branch). Dev/prod as two branches is decided but not set up ([[use-xano-branches-for-dev-and-prod]]) |
| API groups | `app` (everything the app calls, base `https://api.tomale.ai/api:1pgd39RE`) and `webhooks` (Stripe and HPBC) ([[consolidate-xano-api-groups-into-app-and-webhooks]]) |
| Size (mirror, 24/10) | 58 `app` endpoints (+1 disabled), 3 webhooks, 71 functions, 10 background tasks, 39 tables with 3 table triggers |
| Mirror | Xano GitHub sync → `tomale-ai-ltd/tomale-xano` (read-only), cloned at `~/Developer/tomale/tomale-xano` and exposed as `Repos/tomale-xano` ([[mirror-xano-workspace-to-github-read-only]]) |
| Generated specs | `npm run update:openapi` (app contract) and `npm run update:datamodel` (schema) in the app repo ([[generate-data-model-and-api-contract-from-xano]]) |
| Who changes it | Only Kyle publishes. Xano AI or Claude draft; drafts are reviewed against the mirror file after a `git pull` ([[keep-agents-out-of-xano-no-mcp]], [[operating-model]] §3.2) |

## 2. Function folders

| Folder | What lives there |
|---|---|
| `ai_pipeline/` | Story model, page text, moderation (story and name), image orchestration, claim/worker/executors for cover, page and character images, completion check, TTS |
| `docgen/` | PDF jobs: orchestrator, claim, worker, cover and inner executors, Papermill calls, `reconcile_order_fulfilment` |
| `ecommerce/` | Stripe customer, shared webhook ingest and complete functions |
| `payments/` | `stripe_refund_order` |
| `print on demand/` | `hpbc_create_order`, `hpbc_update_order` |
| `notifications/` | `create_user_alert`, broadcast, mark-read |
| `phonics/` | Grapheme and exception lookups by stage |
| `admin/`, `housekeeping/` | Profanity check, JWT and magic-link helpers, Resend send functions, one-off migrations (run manually) |
| `api/` | Character edit and image/attachment uploads used by endpoints |

**Legacy still in the workspace** (candidates for the pre-launch clean-up): `print on demand/mixam_*` (2), `webhooks/make_com_*` (7), `admin/mixpanel_import_event`.

**Background tasks:** `image_worker_tick`, `pdf_worker_tick`, `hpbc_submit_due_orders` (every 60 s, up to 20 orders), `reconcile_order_refunds`, `reconcile_stripe_customers`, `check_session_expiry`, story/theme/art-style counters, `update_instant_stories_data_model`, `mapping_phonics_stage_exceptions`.

## 3. Conventions

- **Ownership:** `users_id` on user-owned rows; identity always from `$auth.id`, profile from `$auth.extras.active_profile` ([[security-model]] §1).
- **Errors:** `error_type = "inputerror"` (400) with a `code` in the payload. Xano has no 422. 14 preconditions still put `422` in the message field; it's on the pre-launch list.
- **Money:** integer minor units (pence). `store_orders.subtotal` / `shipping_amount`, `products.amount`, `shipping_options.amount`, `transactions.amount_minor` + `currency`. HPBC is sent pounds (`subtotal / 100.0`) ([[store-money-as-integer-minor-units]], [[migrate-store-orders-money-fields-to-integer-pence]]).
- **Writes:** `db.add` / `db.edit` map columns explicitly and should enforce hidden fields. In XanoScript an omitted `enforce_hidden_fields` means enforced, and only `= false` is written out. 199 statements still say `false`; the sweep is pre-launch ([[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]]).
- **Inputs:** explicit allowlists, no `dblink` ([[replace-dblink-inputs-with-explicit-allowlists]]). Never name an input or variable after a column the function writes ([[avoid-column-named-function-inputs-in-xano]]). Test switches are `bool x?` (optional), not `bool? x` (nullable but required) ([[make-simulate-test-switch-inputs-optional]]).
- **Soft delete:** `deleted_at` is the standard for user content and profiles. `characters` still has three overlapping fields until the Slice 100 prep ([[scope-characters-per-profile-with-soft-delete]]).
- **Logging:** `executor_runs` keeps small status fields only (url, method, status) ([[log-only-small-status-fields-in-executor-runs]]). Request history is 0 on functions that send API keys (`hpbc_create_order`, `reconcile_order_fulfilment`, both Papermill functions, the refund) ([[disable-request-history-on-credential-functions]]). The workspace default is 100.
- **Lookups:** executor runs are found by `id`, never by timestamp ([[find-executor-runs-by-id-not-timestamp]]).
- **Order numbers:** `{id}-{yyyymmdd}-{users_id}-{instant_stories_id}`, built in a Lambda step (the expression `format_timestamp:"Ymd"` failed).
- **Email verification:** single-use UUID token, 1-hour expiry, landing page on Squarespace (`/verify-email`), back into the app by deep link ([[separate-verify-email-deeplink-from-magic-link-path]]).

## 4. Pipelines

Flows with diagrams: [[story-creation-flow]], [[image-generation-flow]], [[order-fulfilment-flow]], [[order-cancellation-and-refund-flow]].

- **Story:** Draft → Preparing → In Queue → Done; Blocked from moderation ([[formalise-story-status-lifecycle]]). Text via `generate_story_page_text` with moderation; images queued as `image_jobs` and drained by `image_worker_tick` → `claim_image_jobs` → executors. 10–15 minutes per story; throughput work is Phase 2 off Xano ([[defer-image-pipeline-throughput-to-phase-2]]).
- **Orders:** Stripe `checkout.session.completed` → `webhook_payment_confirmation` (verify, ingest, dedup, transaction row, PDF orchestrator, `submit_after` = paid + 30 min, 1 min for test users) → PDFs by Papermill via `pdf_jobs` → `hpbc_submit_due_orders` → `hpbc_create_order` (one fail-closed request; marks the order Error and releases `hpbc_lock` on every failure path) → HPBC callbacks move status forward only ([[delay-hpbc-submission-with-30-minute-cancellation-window]], [[make-hpbc-create-order-a-single-fail-closed-request]], [[mark-order-error-on-hpbc-rejection-and-clear-lock]], [[enforce-forward-only-hpbc-callback-status-transitions]]).
- **Staging vs live print:** `users.test_mode` picks the SKU (`products.hpbc_sku_test` / `hpbc_sku_live`; the decision's "staging" name was never used in the schema) and fails closed to test ([[key-hpbc-environment-switch-off-stripe-test-mode]]).
- **Cancel and refund:** self-service within the window → automatic full Stripe refund with idempotency key `refund_{order}_{attempt}`; misprints go through support ([[automate-full-refund-on-self-service-cancel]], [[split-refund-model-into-self-service-and-support-paths]]).

## 5. Integrations

| Service | Used for | Where | Notes |
|---|---|---|---|
| OpenAI | Story text, moderation, images (`gpt-image-1`) | `ai_pipeline/` | Image responses are always `b64_json` |
| Stripe | Book checkout, refunds, customers | `ecommerce/`, `payments/`, webhook | Test/live chosen per user by `test_mode`; subscriptions not built |
| HP Brand Centre / Pureprint | Print fulfilment | `print on demand/`, 2 callbacks | Bearer-token callbacks; 6 customer-facing statuses ([[scope-hpbc-callbacks-to-six-customer-facing-statuses]]) |
| Papermill | Cover and inner print PDFs | `docgen/` | Request history 0 |
| Resend | Transactional email | `admin/resend_*` | Internal functions only ([[replace-sendgrid-with-resend-for-transactional-email]]) |
| Squarespace (www.tomale.ai) | Email verification, magic-link and checkout landing pages | — | Checkout return moves into the app ([[return-from-stripe-checkout-via-in-app-browser-sheet]]) |

## 6. XanoScript gotchas

- `$auth.extras.a.b` throws a fatal error if any segment is missing; `first_notempty` doesn't help. The path must exist.
- An `object { schema }` with an empty schema block serialises as `[]`, not `{}`, when values are set with `|set`.
- Env vars used as numbers must be cast to integer; read as text, `locked_until` became 1970.
- `regex_match` is deprecated: use `regex_matches`. `lambda_map` needs a quoted string and a timeout.
- Error and terminal-state handling must sit outside success conditionals, or failed jobs stay stuck.
- Counters like `images_remaining` are recounts, never decrements (race conditions).
- `gpt-image-1` returns `b64_json`: decode before Create File Resource, which re-encodes; double encoding corrupts the file.
- A blank `hpbc_order_id` was stored as `""`, not null, and blocked submission. Test for empty, not just null.
- A column-named input silently overwrote `created_at` and `message`. Hence the naming rule in §3.
- Xano JWE tokens can't be decoded client-side; track expiry by time.
- Metadata API filters are query-string parameters on GET; in a JSON body they're silently ignored.

## 7. Working rules

- Take a manual snapshot before structural changes (group deletes, bulk moves, schema changes).
- Test failure paths explicitly; a passing happy path proves little. Run `_tests` after backend changes ([[test-suite]]).
- Prefer fail-closed preconditions; Xano AI suggestions have introduced fail-open logic and user enumeration before.
- After a schema change: `npm run update:datamodel`. After an `app` endpoint change: `npm run update:openapi` (both in Cursor).
