---
type: living-doc
title: security-model
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-10-28
last_verified: 2026-10-28
owner: vault
related:
  - "[[backend-xano]]"
  - "[[pre-launch-checklist]]"
  - "[[roadmap]]"
---

# API security model

How the Xano API is protected, and what every endpoint does about access. Renamed from `6-api-security-model` in B8. The old table-by-table matrix (last edited 07/05/2026) is replaced by the endpoint matrix in §3, generated from the published code. The old version is in git history.

## 1. Rules every endpoint follows

1. **Default deny.** Every `app` endpoint requires a signed-in user (`auth = "users"`) except the auth flow itself. Webhooks have no user auth but verify the caller in the stack.
2. **Identity comes from the token, never from inputs.** Ownership is checked against `$auth.id`; profile context comes from `$auth.extras.active_profile` ([[carry-active-profile-in-token-extras]], [[fail-closed-active-profile-resolution]]).
3. **Ownership field:** `users_id` ([[ratify-users-id-as-ownership-field-standard]]). Stories are also scoped to the creating profile ([[per-child-story-visibility]]); characters will be ([[scope-characters-per-profile-with-soft-delete]]).
4. **Fail closed.** Preconditions reject anything not explicitly allowed; another user's record returns `notfound`.
5. **Errors:** 400 (`inputerror`) with a `code` in the payload (e.g. `STORY_AWAITING_APPROVAL`, `ORDER_NOT_PAYABLE`, `CANNOT_DELETE_ACTIVE`). Xano has no 422.
6. **Webhooks:** verify (Stripe signature, HPBC bearer token) → ingest → dedup → complete ([[adopt-unique-index-dedup-for-webhook-ingest]], [[authenticate-hpbc-webhooks-with-shared-secret-bearer-token]]).
7. **Inputs:** explicit allowlists, no `dblink` ([[replace-dblink-inputs-with-explicit-allowlists]]); no input named after a column it writes ([[avoid-column-named-function-inputs-in-xano]]); test switches optional ([[make-simulate-test-switch-inputs-optional]]).
8. **Outputs:** explicit `output` lists on user records. `users.password` is never returned. The hidden-fields sweep is a pre-launch item (§5).
9. **Internal work stays internal.** Workers, executors, email and fulfilment run as functions and background tasks, not endpoints. Their logs hold small status fields only, never keys or payloads ([[log-only-small-status-fields-in-executor-runs]], [[disable-request-history-on-credential-functions]]).
10. **No agent access to Xano.** Agents read the read-only GitHub mirror; only Kyle publishes ([[keep-agents-out-of-xano-no-mcp]]).

## 2. Scope types

| Scope | Meaning |
|---|---|
| Public (auth flow) | No token: sign-up, login, magic link, refresh, password reset, email verification |
| Owner (`$auth.id`) | Signed in; only the caller's own records (household for profile endpoints) |
| Owner + active profile | As Owner, and also filtered or checked by the active profile (child visibility) |
| Reference | Signed in; shared catalogue data (themes, art styles, products, phonics) |
| Webhook | No user; the caller is verified in the stack |
| Disabled | Exists but `external_access = false` |

## 3. Endpoint matrix

Generated on 28/10/2026 from the Xano mirror (`Repos/tomale-xano`, sync of 24/10, no publishes since). Scope is inferred from the code (`auth`, use of `$auth.id` and `active_profile`) and spot-checked; it is not a substitute for reading the endpoint. `enforce_hidden_fields = false` counts size the pre-launch sweep (199 across all functions, endpoints and tasks).

| Group | Method | Path | Auth | Scope | Notes |
|---|---|---|---|---|---|
| `app` | GET | `/activities` | users | Reference (any signed-in user) |  |
| `app` | GET | `/artwork_style` | users | Reference (any signed-in user) |  |
| `app` | GET | `/artwork_style/{artwork_style_id}` | users | Reference (any signed-in user) |  |
| `app` | POST | `/auth/complete_magic_link` | none | Public (auth flow) | 2× `enforce_hidden_fields = false` |
| `app` | POST | `/auth/login` | none | Public (auth flow) | Generic error for unknown user or wrong password; request history 100; 1× `enforce_hidden_fields = false` |
| `app` | GET | `/auth/me` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/auth/refresh` | none | Public (auth flow) | `users_id` is only a lookup key; the hashed refresh token is the credential; 1× `enforce_hidden_fields = false` |
| `app` | POST | `/auth/request_magic_link` | none | Public (auth flow) |  |
| `app` | POST | `/auth/reset_password` | none | Public (auth flow) | 1× `enforce_hidden_fields = false` |
| `app` | POST | `/auth/select_profile` | users | Owner (`$auth.id`) + active profile | PIN gate not built yet; 1× `enforce_hidden_fields = false` |
| `app` | POST | `/auth/signup` | none | Public (auth flow) | 5× `enforce_hidden_fields = false` |
| `app` | GET | `/auth/verify_email` | none | Public (auth flow) | 1× `enforce_hidden_fields = false` |
| `app` | GET | `/characters` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/characters` | users | Owner (`$auth.id`) | 2× `enforce_hidden_fields = false` |
| `app` | DELETE | `/characters/{characters_id}` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | GET | `/characters/{characters_id}` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/characters/{id}/model` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/conversations` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/conversations` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | DELETE | `/conversations/{conversations_id}` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | GET | `/conversations/{conversations_id}` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/conversations/{id}/message` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/fact/random` | users | Reference, profile-gated | Gated on `is_child` |
| `app` | GET | `/instant_stories` | users | Owner (`$auth.id`) + active profile | request history 100 |
| `app` | POST | `/instant_stories` | users | Owner (`$auth.id`) + active profile | 2× `enforce_hidden_fields = false` |
| `app` | DELETE | `/instant_stories/{id}` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | GET | `/instant_stories/{id}` | users | Owner (`$auth.id`) + active profile |  |
| `app` | POST | `/instant_stories/{id}/cover_image` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | POST | `/instant_stories/{id}/model` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/instant_stories/{id}/page_image` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | POST | `/instant_stories/{id}/page_text` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/phonics/phonics_schemes` | users | Reference (any signed-in user) |  |
| `app` | GET | `/phonics/phonics_schemes/{phonics_schemes_id}/stages` | users | Reference (any signed-in user) |  |
| `app` | GET | `/products` | users | Reference (any signed-in user) |  |
| `app` | GET | `/products/{id}` | users | Reference (any signed-in user) |  |
| `app` | GET | `/shipping_options` | users | Reference (any signed-in user) |  |
| `app` | GET | `/shipping_options/{shipping_options_id}` | users | Reference (any signed-in user) |  |
| `app` | GET | `/store_orders` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/store_orders` | users | Owner (`$auth.id`) | Parental-approval gate (`STORY_AWAITING_APPROVAL`); 1× `enforce_hidden_fields = false` |
| `app` | GET | `/store_orders/{store_orders_id}` | users | Owner (`$auth.id`) |  |
| `app` | PATCH | `/store_orders/{store_orders_id}` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | POST | `/store_orders/{store_orders_id}/cancel` | users | Owner (`$auth.id`) | 3× `enforce_hidden_fields = false` |
| `app` | GET | `/stripe/check_order_paid` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/stripe/create_checkout_session` | users | Owner (`$auth.id`) | Parental-approval gate, order-status guard, Stripe total checked against Xano prices; 1× `enforce_hidden_fields = false` |
| `app` | GET | `/subscriptions` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/subscriptions/{subscriptions_id}` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/themes` | users | Reference (any signed-in user) |  |
| `app` | GET | `/user_alerts` | users | Owner (`$auth.id`) |  |
| `app` | GET | `/user_alerts/{user_alerts_id}` | users | Owner (`$auth.id`) |  |
| `app` | PATCH | `/user_alerts/{user_alerts_id}` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | PATCH | `/users/me` | users | Owner (`$auth.id`) | 2× `enforce_hidden_fields = false` |
| `app` | POST | `/users/me/complete_onboarding` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | PATCH | `/users/me/image` | users | Owner (`$auth.id`) + active profile | 2× `enforce_hidden_fields = false` |
| `app` | PATCH | `/users/user_alerts/mark-all-read` | users | Owner (`$auth.id`) | 1× `enforce_hidden_fields = false` |
| `app` | GET | `/users/user_profiles` | users | Owner (`$auth.id`) |  |
| `app` | POST | `/users/user_profiles` | users | Owner (`$auth.id`) + active profile | 1× `enforce_hidden_fields = false` |
| `app` | DELETE | `/users/user_profiles/{user_profiles_id}` | users | Owner (`$auth.id`) + active profile | 1× `enforce_hidden_fields = false` |
| `app` | PATCH | `/users/user_profiles/{user_profiles_id}` | users | Owner (`$auth.id`) + active profile | 1× `enforce_hidden_fields = false` |
| `app` | POST | `/utilities/upload_image` | users | Disabled | `external_access = false`: not reachable from outside |
| `webhooks` | POST | `/hpbc/webhook_statusCallbackUrl` | none (verified in stack) | Webhook: HPBC bearer token | request history 100 |
| `webhooks` | POST | `/hpbc/webhook_statusCallbackUrl_Error` | none (verified in stack) | Webhook: HPBC bearer token | request history 100 |
| `webhooks` | POST | `/stripe/webhook_payment_confirmation` | none (verified in stack) | Webhook: Stripe signature | request history 1000; 6× `enforce_hidden_fields = false` |

**58 `app` endpoints** are reachable (one more is disabled) and **3 `webhooks`**. The private Swagger spec (`apispec:1pgd39RE`) covers the `app` group and is what the app's client is generated from (`npm run update:openapi`).

## 4. Tables

Exposure by table follows the domains in the generated [[Repos/tomale-rn-test/memory/data-model|data-model]]:

| Domain | Tables | Exposure |
|---|---|---|
| Core content | `characters`, `conversations`, `instant_stories`, `instant_story_characters`, `instant_story_pages` | Owner (+ profile for stories); pages and character links only inside story responses |
| Content configuration | `artwork_style`, `themes`, `data_models` | Reference read; `data_models` internal |
| AI and processing pipeline | `executor_runs`, `image_jobs`, `pdf_jobs`, `token_usage` | Internal only |
| Commerce and orders | `store_orders`, `store_order_updates`, `products`, `shipping_options`, `audit_store_orders` | Orders owner-scoped (updates embedded); products and shipping are reference; the audit table is internal and temporary ([[add-temporary-audit-trigger-on-store-orders]]) |
| Billing and subscriptions | `subscriptions`, `transactions`, `transaction_webhook_events` | `subscriptions` owner read; the rest internal ([[split-webhook-ingress-log-from-money-transactions]]) |
| Users and accounts | `users`, `user_profiles`, `user_alerts`, `user_sessions`, `user_logs`, `user_activities` | `users`, profiles and alerts owner-scoped; sessions, logs and activities internal |
| Moderation and safety | `moderation_flags`, `blocked_terms` | Internal |
| Phonics | 7 `phonics_*` tables | Reference, through two nested read endpoints only |
| Locale and misc | `activities`, `fact`, `locale_data`, `support_requests` | `activities` and `fact` reference; the rest internal (`support_requests` replaced by a mailto) |

## 5. Open items before launch

All tracked on [[pre-launch-checklist]]:
- the `enforce_hidden_fields = true` sweep (199 statements)
- rate limiting on auth, order and generation endpoints ([[add-per-endpoint-rate-limiting-in-xano]])
- the parental PIN gate on `auth/select_profile` ([[parental-gate-on-profile-switch]])
- request history off on token-issuing auth endpoints (`auth/login` keeps 100 today: accepted risk while only test accounts exist, [[keep-request-history-on-auth-endpoints-until-pre-launch]])
- the 14 precondition messages reading `422`
- an account-deletion endpoint (App Store requirement)
- signed URLs for user images (all images are public URLs today, [[migrate-image-storage-to-aws-s3-signed-urls]])
- the dev/prod Xano branch split ([[use-xano-branches-for-dev-and-prod]])

## 6. Phase 1 close-out (2026-10-23)

**Status:** Phase 1 signed off on 2026-10-23, after the final `_tests` regression run (86/86).

> The table-by-table matrix this section used to sit above has been replaced by §3 (28/10).

Per [[5-cto-implementation-plan]], Phase 1 items 5–9 closed on 2026-07-16 and items 1–4 on 2026-10-14.

### What was hardened, by area

- **Auth:** magic-link login; JWE tokens (1 hour) carrying `active_profile` extras; `select_profile`; refresh with rotation, hashed refresh tokens and 401 `invalid_refresh_token`; `verify_email` through the Squarespace intermediary. `auth/login` returns a single generic "Invalid Credentials." for an unknown user or a wrong password.
- **Users and profiles:** `PATCH /users/me` (boolean preferences folded in), `complete_onboarding`, the image endpoint. `user_profiles` is one table with `is_child` and `is_primary`: parent-only create and delete, household scope, soft delete, profanity list plus AI moderation.
- **Stories and characters:** owner-scoped `instant_stories` with per-child visibility and the moderation and parental-approval flags. `conversations/{id}/message` and `API/character_edit` take explicit input lists, no `dblink` (2026-10-23).
- **System:** activities, `artwork_style`, `fact/random` (with an `is_child` gate), themes; phonics reduced to two nested read endpoints.
- **Engagement:** `user_alerts`, an account-level inbox (list, get, mark read, `POST /user_alerts/mark-all-read`).
- **Commerce:**
  - `store_orders` owned through `$auth.id`; a 30-minute self-service cancel window with automatic refund; ordering blocked while a story awaits parental approval (`STORY_AWAITING_APPROVAL`); money stored in integer pence.
  - `stripe/create_checkout_session`: owner-scoped; never returns the raw Stripe response; checks the Stripe total against Xano prices; parental-approval gate; order-status guard (`ORDER_NOT_PAYABLE`).
  - `check_order_paid` authenticated and owner-scoped.
- **Subscriptions group:** completed under Phase 1 items 1–9.
- **Integrations (`webhooks` group):**
  - Stripe: signature validated; idempotent through a unique `provider_payment_id`; refund events handled.
  - HPBC callbacks: bearer-token auth; ingest, dedup and complete pattern; status changes only move forward.
  - Resend email functions are internal only.
- **Removed or locked down:**
  - endpoints for `instant_story_reviews`, `user_activities` and `support_requests`
  - `/model`
  - `/hpbc/webhook_order_submission`
  - `/admin/upload/image`: external access disabled
- **Pipelines and logging:**
  - executor runs found by id
  - `executor_runs` logs only small status fields
  - no API keys or base64 payloads in run logs (the leaked OpenAI key was rotated)

### Patterns every endpoint follows

- Ownership is checked against `$auth.id`; profile context comes from `$auth.extras.active_profile`, never from inputs.
- Preconditions fail closed. Another user's record returns `notfound`.
- Webhooks: a signature or bearer token, then ingest, dedup and complete.
- Money is held as integer minor units ([[store-money-as-integer-minor-units]]).
- Inputs: no input or variable named after a column the function writes to ([[avoid-column-named-function-inputs-in-xano]]); explicit input lists instead of `dblink` on edits; test switches are optional inputs ([[make-simulate-test-switch-inputs-optional]]).

### Evidence

- Postman `_tests` (folders 1, NEG, 3, 4): 86 tests covering auth and refresh, cross-user and invalid-input negatives, the full order flow (checkout → Stripe → PDF → HPBC → shipped) and cancel/refund.
- 2026-10-23: 85/86. The one failure was a stale pounds conversion in a test assertion, since fixed.
- Final regression run, 2026-10-23: **86/86 passed** (orders 180 and 181).

### Phase 1 quick settings (Xano pre-launch checklist)

- [x] Refreshed the `app` OpenAPI spec into the repo with `npm run update:openapi` (`app` group only; the `webhooks` export was dropped on 28/10)
- [x] Set Swagger to private for both groups (repo `.env` points at `apispec:1pgd39RE` with the docs token)
- [x] Turned on sensitive-data flags (`users.password`, `magic_link`, `temp_login`; `user sessions.refresh_token`). Note: these only mask `dblink` inputs
- [x] 2FA on the Xano account (authenticator app)
- [x] Removed the expired metadata API tokens (`metadata-api`, `ncScale`); `cursor-read` kept

### Carried forward (not Phase 1)

- **Before launch:**
  - the `enforce_hidden_fields = true` sweep across every `db.add` / `db.edit` (sized from the mirror on 2026-10-24: **199 of 222** write statements still say `= false`; in XanoScript, leaving the line out means enforced)
  - rate limiting ([[add-per-endpoint-rate-limiting-in-xano]])
  - the parental PIN gate ([[parental-gate-on-profile-switch]])
  - the dev/prod split, now Xano branches ([[use-xano-branches-for-dev-and-prod]])
  - endpoint inventory, CORS, test-data cleanup, and a backup before launch
  - iOS Universal Links / Android App Links
- HPBC bearer token that appeared in chat: rotated (confirmed 2026-10-23).
- **Accepted risk:** request history stays on for token-issuing auth endpoints while only test accounts exist (outputs show tokens). Revisit before launch or if anyone else gets workspace access.
- **Phase 2:** Stripe webhook branching by mode; S3/CloudFront private media (Phase 1.5).

