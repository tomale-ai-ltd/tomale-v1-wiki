---
type: living-doc
title: backend-xano
project: tomale-rn-v1
status: current
version: 1.1
date: 2026-10-28
last_verified: 2026-10-30
owner: vault
related:
  - "[[security-model]]"
  - "[[test-suite]]"
  - "[[stack]]"
  - "[[agent-context-sync]]"
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

## 3. Rules for agents (mirrored to Xano AGENTS.md)

The block below is copied **verbatim** into Xano → Knowledge → AGENTS.md (locked with Enforcement). Edit it here only; the daily pipeline flags a re-paste when it changes ([[agent-context-sync]]). Keep it short: Xano loads it with every prompt.

<!-- xano-agents:start -->
# Tomale backend rules

Backend for Tomale, a children's personalised storybook app (iOS and Android). API groups: `app` (everything the app calls) and `webhooks` (Stripe, HPBC/Pureprint). You draft; Kyle reviews and publishes.

## Identity and access
- Identity comes from `$auth.id`, the active profile from `$auth.extras.active_profile`. Never take user or profile ids from inputs.
- Fail closed: no `active_profile` in the token means refuse (re-login). A missing segment in `$auth.extras.a.b` is a fatal error, so the path must exist.
- User-owned rows carry `users_id`, and every read and write filters on it.
- Parent-only actions (store, orders, subscriptions, approvals, profile create/delete, character archive/delete) require `active_profile.is_child = false`, else error code `PARENT_PROFILE_REQUIRED`.
- A child sees only their own stories (`user_profiles_id`); characters are shared by the household.

## Errors and data
- Domain errors are `inputerror` (HTTP 400) with a machine-readable `code` in the payload, e.g. `ORDER_NOT_PAYABLE`. Never 422.
- Money is integer minor units (pence) everywhere. Only HPBC is sent pounds.
- Inputs are explicit allowlists; no `dblink`. Never name an input or variable after a column the function writes. Test switches are `bool x?` (optional).
- `db.add` / `db.edit` map columns explicitly. Never write `enforce_hidden_fields = false`.
- Soft delete with `deleted_at` for user content and profiles.
- Counters such as `images_remaining` are recounted, never decremented.
- Check for empty, not only null: blank values are stored as `""`.
- Env vars used as numbers are cast to integer.

## Jobs and integrations
- Error and terminal-state handling sits outside success conditionals, so failed jobs never stay stuck.
- `executor_runs` stores small status fields only (url, method, status). Look runs up by `id`, never by timestamp.
- Request history is 0 on any function that sends an API key.
- OpenAI image responses are `b64_json`: decode once before Create File Resource (it re-encodes).

## Guardrails
- Never delete or rename tables, fields, endpoints or data without asking.
- Suggest a manual snapshot before structural changes.
- Prefer fail-closed preconditions. Never reveal whether an account exists.
- Test failure paths, not only the happy path.
- After a schema change, remind Kyle to run `pnpm update:datamodel` (a new table must also be added to the generator's domain map). After an `app` endpoint change, `pnpm update:openapi` and the Postman `_tests`.
<!-- xano-agents:end -->

**Sources:** [[security-model]] §1, [[fail-closed-active-profile-resolution]], [[ratify-users-id-as-ownership-field-standard]], [[share-characters-across-the-household]], [[per-child-story-visibility]], [[store-money-as-integer-minor-units]], [[replace-dblink-inputs-with-explicit-allowlists]], [[avoid-column-named-function-inputs-in-xano]], [[make-simulate-test-switch-inputs-optional]], [[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]], [[log-only-small-status-fields-in-executor-runs]], [[find-executor-runs-by-id-not-timestamp]], [[disable-request-history-on-credential-functions]], [[keep-agents-out-of-xano-no-mcp]].

**Known exceptions (pre-launch clean-up):** 14 preconditions still put `422` in the message; 199 statements still say `enforce_hidden_fields = false` ([[pre-launch-checklist]]).

**Other conventions:**
- **Order numbers:** `{id}-{yyyymmdd}-{users_id}-{instant_stories_id}`, built in a Lambda step (the expression `format_timestamp:"Ymd"` failed).
- **Email verification:** single-use UUID token, 1-hour expiry, landing page on Squarespace (`/verify-email`), back into the app by deep link ([[separate-verify-email-deeplink-from-magic-link-path]]).
- `characters` keeps `status` (archive) and `is_deleted` alongside `deleted_at`, by choice.

## 4. Pipelines

Flows with diagrams: [[story-creation-flow]], [[image-generation-flow]], [[order-fulfilment-flow]], [[order-cancellation-and-refund-flow]].

- **Story:** Draft → Preparing → In Queue → Done; Blocked from moderation ([[formalise-story-status-lifecycle]]). Text via `generate_story_page_text` with moderation; images queued as `image_jobs` and drained by `image_worker_tick` → `claim_image_jobs` → executors. 10–15 minutes per story; throughput work is Phase 2 off Xano ([[defer-image-pipeline-throughput-to-phase-2]]).
- **Orders:** Stripe `checkout.session.completed` → `webhook_payment_confirmation` (verify, ingest, dedup, transaction row, PDF orchestrator, `submit_after` = paid + 30 min, 1 min for test users) → PDFs by Papermill via `pdf_jobs` → `hpbc_submit_due_orders` → `hpbc_create_order` (one fail-closed request; marks the order Error and releases `hpbc_lock` on every failure path) → HPBC callbacks move status forward only ([[delay-hpbc-submission-with-30-minute-cancellation-window]], [[make-hpbc-create-order-a-single-fail-closed-request]], [[mark-order-error-on-hpbc-rejection-and-clear-lock]], [[enforce-forward-only-hpbc-callback-status-transitions]]).
- **Staging vs live print:** `users.test_mode` picks the SKU (`products.hpbc_sku_test` / `hpbc_sku_live`; the decision's "staging" name was never used in the schema) and fails closed to test ([[key-hpbc-environment-switch-off-stripe-test-mode]]).
- **Cancel and refund:** self-service within the window → automatic full Stripe refund with idempotency key `refund_{order}_{attempt}`; misprints go through support ([[automate-full-refund-on-self-service-cancel]], [[split-refund-model-into-self-service-and-support-paths]]).

## 5. Integrations

| Service | Used for | Where | Notes |
|---|---|---|---|
| OpenAI | Story text, moderation, images (`gpt-image-1.5`, model set in `data_models`) | `ai_pipeline/` | Image responses are always `b64_json` |
| Stripe | Book checkout, refunds, customers | `ecommerce/`, `payments/`, webhook | Test/live chosen per user by `test_mode`; subscriptions not built |
| HP Brand Centre / Pureprint | Print fulfilment | `print on demand/`, 2 callbacks | Bearer-token callbacks; 6 customer-facing statuses ([[scope-hpbc-callbacks-to-six-customer-facing-statuses]]) |
| Papermill | Cover and inner print PDFs | `docgen/` | Request history 0 |
| Resend | Transactional email | `admin/resend_*` | Internal functions only ([[replace-sendgrid-with-resend-for-transactional-email]]) |
| Squarespace (www.tomale.ai) | Email verification, magic-link and checkout landing pages | — | Checkout return moves into the app ([[return-from-stripe-checkout-via-in-app-browser-sheet]]) |

## 6. XanoScript gotchas

Rules that follow from gotchas are in the §3 block. These are the remaining traps:
- An `object { schema }` with an empty schema block serialises as `[]`, not `{}`, when values are set with `|set`.
- `regex_match` is deprecated: use `regex_matches`. `lambda_map` needs a quoted string and a timeout.
- Xano JWE tokens can't be decoded client-side; track expiry by time.
- Metadata API filters are query-string parameters on GET; in a JSON body they're silently ignored.
- A column-named input once silently overwrote `created_at` and `message` (hence the naming rule).
