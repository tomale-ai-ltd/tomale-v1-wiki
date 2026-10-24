---
type: living-doc
title: 6-api-security-model
aliases:
  - API Security Model — Table Classification
project: tomale-rn-v1
status: current
version: 1.1
date: 2026-04-15
last_verified: 2026-10-23
owner: vault
phase-1: signed-off-2026-10-23
---

# API Security Model — Table Classification

> Maps all Xano tables to their exposure type, CRUD permissions, and
> required actions. Used to implement API surface reduction per CTO
> recommendations (section 2.5 of implementation plan).

## Summary

This document relates to how we are executing  "Implementation Phases - Phase 1 — Security & Data Integrity" in [[5-cto-implementation-plan|5-cto-implementation-plan]].

In essence, it reflects the desired future state of the Xano API, in readiness for the public launch of tomale-rn-v1.

An exercise was carried out to assess the [[Repos/tomale-rn-test/memory/data-model|data-model]] and Xano API for security issues, and review each endpoint on a case by case basis.

As of 2026-10-23, Phase 1 is complete. See the close-out section below.

---

## Phase 1 close-out (2026-10-23)

**Status:** Phase 1 signed off on 2026-10-23, after the final `_tests` regression run (86/86).

> **The classification matrix below is historical** (last edited 2026-05-07). Its "Done?" column is not maintained and should not be trusted. It will be rebuilt from the Xano OpenAPI export during the documentation refresh ([[documentation-refresh-backlog]]). This section is the authoritative Phase 1 record until then.

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

- [x] Refreshed the `app` OpenAPI spec into the repo with `npm run update:openapi` (59 operations, `app` group only); export `webhooks` during the doc refresh
- [x] Set Swagger to private for both groups (repo `.env` points at `apispec:1pgd39RE` with the docs token)
- [x] Turned on sensitive-data flags (`users.password`, `magic_link`, `temp_login`; `user sessions.refresh_token`). Note: these only mask `dblink` inputs
- [x] 2FA on the Xano account (authenticator app)
- [x] Removed the expired metadata API tokens (`metadata-api`, `ncScale`); `cursor-read` kept

### Carried forward (not Phase 1)

- **Before launch:**
  - the `enforce_hidden_fields = true` sweep across every `db.add` / `db.edit` (sized from the mirror on 2026-10-24: **199 of 222** write statements still say `= false`; in XanoScript, leaving the line out means enforced)
  - rate limiting ([[add-per-endpoint-rate-limiting-in-xano]])
  - the parental PIN gate ([[parental-gate-on-profile-switch]])
  - separate dev and prod workspaces
  - endpoint inventory, CORS, test-data cleanup, and a backup before launch
  - iOS Universal Links / Android App Links
- HPBC bearer token that appeared in chat: rotated (confirmed 2026-10-23).
- **Accepted risk:** request history stays on for token-issuing auth endpoints while only test accounts exist (outputs show tokens). Revisit before launch or if anyone else gets workspace access.
- **Phase 2:** Stripe webhook branching by mode; S3/CloudFront private media (Phase 1.5).

---

## Exposure Type Definitions

| Exposure Type | Meaning |
|---|---|
| `public` | Readable by any authenticated user |
| `user-scoped` | Only accessible to the owning user |
| `system` | Readable but controlled (may evolve, not fully open) |
| `internal` | Never exposed via public API |
| `DELETE` | Table and/or endpoints to be deleted entirely |

---

## Table Classification Matrix

### Characters

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| characters | characters | yes | user-scoped | yes | yes | yes | yes | no | no | All operations for authenticated users only. Add scoped queries for `owner_user_id`. Add soft delete. Add rate limiting. | yes |
| character_traits | characters | no | internal | no | no | no | no | yes | yes | Delete table and endpoints | no |
| character_types | characters | no | internal | no | no | no | no | yes | yes | Delete table and endpoints | no |

### Stories

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| instant_stories | stories | yes | user-scoped | yes | yes | no | yes | no | no | All operations for authenticated users, scoped queries, soft delete. New endpoint `/instant_stories/:id/phonics`. New endpoint `/instant_stories/:id/characters`. Expand `instant_stories/$id` to include IS_page data. | yes |
| conversations | stories | yes | user-scoped | yes | yes | yes | no | no | no | All operations for authenticated users only. Add scoped queries for `owner_user_id`. Add soft delete. | yes |
| instant_story_pages | stories | no | user-scoped | no | no | no | no | yes | no | Delete endpoints | no |
| instant_story_reviews | stories | yes | user-scoped | yes | yes | no | no | no | no | Users need to be able to leave and read reviews | no |
| instant_story_characters | stories | no | internal | no | no | no | no | yes | no | Mapping table only. Story character data should come via `GET /instant_stories/$id` with characters mapped into API response using join table. | no |
| image_jobs | stories | no | internal | no | no | no | no | yes | no | Only visible internally to worker function. No endpoint needed. | no |
| pdf_jobs | stories | no | internal | no | no | no | no | yes | no | Async processing queue, required internally but not via API | no |
| artwork_style | stories | yes | system | no | yes | no | no | no | no | Read only to authenticated users | no |
| themes | stories | yes | system | no | yes | no | no | no | no | Read only to authenticated users | no |
| stories | stories | no | DELETE | no | no | no | no | yes | yes | Delete endpoints and table | no |

### Store

| Table                      | Group | Used by app | Exposure    | C   | R   | U   | D   | Delete endpoints? | Delete table? | Action                                                                                                                                    | Done? |
| -------------------------- | ----- | ----------- | ----------- | --- | --- | --- | --- | ----------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ----- |
| store_orders               | c     | yes         | user-scoped | yes | yes | no  | no  | no                | no            | Authenticated users can create, read and update a scoped list of orders. Expand `store_orders/$id` to include `store_order_updates` data. | no    |
| store_order_updates        | store | no          | user-scoped | no  | no  | no  | no  | yes               | no            | Delete endpoint. Embed filtered data within orders.                                                                                       | no    |
| products                   | store | yes         | public      | no  | yes | no  | no  | no                | no            | Read only for authenticated user                                                                                                          | no    |
| shipping_options           | store | yes         | public      | no  | yes | no  | no  | no                | no            | Read only for authenticated user                                                                                                          | no    |
| transaction_webhook_events | store | no          | internal    | no  | no  | no  | no  | no                | no            | Internal logging. Delete endpoint. Replace with webhook to store raw transaction event data from all providers (Stripe, Apple, Google).   | no    |
| transactions               | store | no          | internal    | no  | no  | no  | no  | yes               | no            | Internal logging                                                                                                                          | no    |

### Subscriptions

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| subscriptions | subscriptions | yes | user-scoped | no | yes | no | no | no | no | Read only for authenticated user, scoped to their data | no |

### Phonics

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| phonics_phase_stage | phonics | yes | system | no | yes | no | no | no | no | Read only for authenticated user | no |
| phonics_scheme_phase | phonics | yes | system | no | yes | no | no | no | no | Read only for authenticated user | no |
| phonics_exceptions | phonics | no | system | no | no | no | no | yes | no | Delete endpoints | no |
| phonics_grapheme | phonics | no | system | no | no | no | no | yes | no | Delete endpoints | no |
| phonics_scheme | phonics | no | system | no | no | no | no | yes | no | Delete endpoints | no |
| phonics_stage_exceptions | phonics | no | system | no | no | no | no | yes | no | Delete endpoints | no |
| phonics_stage_grapheme | phonics | no | system | no | no | no | no | yes | no | Delete endpoints | no |

### Engagement

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| user_activities | engagement | yes | user-scoped | no | yes | no | no | no | no | Read only for authenticated users, scoped to user | no |
| user_alerts | engagement | yes | user-scoped | no | yes | yes | no | no | no | Read and update for authenticated users, scoped to user | no |
| activities | engagement | yes | system | no | yes | no | no | no | no | Read only to authenticated users | no |
| Fact | engagement | yes | system | no | yes | no | no | no | no | Read only to authenticated users | no |

### Users & Auth

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| users | admin | yes | user-scoped | no | yes | yes | no | no | no | Read and update for authenticated users, scoped to user, heavily secured | no |
| support_requests | support | yes | user-scoped | yes | yes | yes | no | no | no | C, R, U for authenticated user, scoped to their data | no |

### Admin & Internal

| Table | Group | Used by app | Exposure | C | R | U | D | Delete endpoints? | Delete table? | Action | Done? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| API_Key_Storage | admin | no | internal | no | no | no | no | yes | yes | Delete table and endpoints | no |
| data_models | admin | no | internal | no | no | no | no | yes | no | Delete endpoints | no |
| executor_runs | admin | no | internal | no | no | no | no | yes | no | Delete endpoints | no |
| locale_data | admin | no | internal | no | no | no | no | yes | no | Delete endpoints | no |
| moderation_flags | admin | no | internal | no | no | no | no | yes | no | Delete endpoints | no |
| token_usage | admin | no | internal | no | no | no | no | yes | no | Internal logging | no |
| user_logs | log | no | internal | no | no | no | no | yes | no | Delete endpoints | no |
| user_sessions | admin | no | internal | no | no | no | no | yes | no | Delete endpoints | no |

### To Delete Entirely

| Table | Group | Action |
|---|---|---|
| locations | locations | Delete table and endpoints |
| stories | stories | Delete table and endpoints |
| API_Key_Storage | admin | Delete table and endpoints |
| character_traits | characters | Delete table and endpoints |
| character_types | characters | Delete table and endpoints |

---

## Summary Counts

| Exposure Type | Count |
|---|---|
| User-scoped | 13 |
| Internal | 12 |
| System | 10 |
| Public | 2 |
| Delete | 2 |

---

## Related notes

- [[5-cto-implementation-plan]]
- [[3-cto-tech-review]]
- [[Repos/tomale-rn-test/memory/data-model|data-model]]
- [[6. Backend - Xano]]
- [[adopt-rebac-auth-model]]