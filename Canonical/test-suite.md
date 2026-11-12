---
type: living-doc
title: test-suite
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
last_verified: 2026-11-12
owner: vault
related:
  - "[[backend-xano]]"
  - "[[security-model]]"
  - "[[pre-launch-checklist]]"
---

# Test suite

What is tested, how to run it, and what isn't covered yet. The backend is tested end to end by the Postman collection `_tests`. App tests (jest-expo) are still minimal and arrive slice by slice.

**Source:** export of `_tests` attached by Kyle on 28/10/2026 (Postman v2.1, 36 requests). Last full regression: **86/86 on 23/10/2026** (orders 180 and 181), the Phase 1 sign-off run.

## 1. Postman `_tests`

| Folder | Requests | What it proves |
|---|---|---|
| **1. Login & Auth.me** | 1A login, 1B `auth/me`, 1C no stuck stories, 1D refresh, 1E reused refresh, 1F logout (saves `revokedSessionId`), 1G refresh after logout, 1H log in again (fresh token and session for later folders) | Login returns `userid`, `authToken`, `refreshToken`; `auth/me` carries `active_profile`; refresh rotates the token; a reused refresh token gets 401 `invalid_refresh_token`; after `auth/logout` the session's refresh token gets 401 too; no story has sat in a non-terminal state longer than `stuckStoryMaxAgeMin` (45 min) ([[replace-long-done-poll-with-stuck-story-check]]) |
| **2. Story Generation** | 2A-1 story, 2A-2 character (starts its own picture since 11/11; 2A-3 removed with the model endpoint 12/11), 2B-1 story model | Creation endpoints and the LLM model calls; image jobs are queued. **Not in the monitor-sized run**: generation takes 10–15 minutes, so this folder runs on its own ([[use-fixture-story-for-order-flow-test]]) |
| **3A-NEG. User 2** | log in as user 2; order a story awaiting approval | `STORY_AWAITING_APPROVAL` (400) ([[block-ordering-of-stories-awaiting-parental-approval]]) |
| **3. Orders** | 3A create → patch → checkout (+ negative ownership) · 3B signed payment webhook, `check_order_paid` · 3C PDF poll · 3D HPBC confirm, Shipped callback, Error callback | Server-derived totals; no secrets in the checkout response; Stripe amount equals the order total in pence; user 2 gets 404 on user 1's checkout; payment confirmed; both PDFs attached; HPBC accepts the order; tracking stored on Shipped; an Error after Shipped is ignored and tracking kept |
| **4. Cancel & Refund** | 4A cancel after submission · 4B new order to paid · 4C–4E cancel by user 2 / user 1 · 4F refund failure · 4G duplicate event | `ORDER_NOT_CANCELLABLE` after HPBC submission; another user's cancel gets 404; cancel within the window → Cancelled + Refunded, never sent to HPBC; a failed refund puts `payment_status` back to Confirmed; a duplicate event is acknowledged without changing state |
| **5. Characters** | 5A create (+ 5A-2 blocked name) · 5B flags (favourite, archive, unarchive, empty) · 5C link to a Draft story · 5H counts, 13-field detail, story filter (incl. an id with no links) · 5D draw again · 5E child via `select_profile` (+ 5K child counts 0 for a parent's story) · 5F user 2 (+ 5L empty list / 404) · 5G cleanup | `picture_status` on create and reads; `stories_count` per reader; flags return only public fields; favourites listed first; archived hidden unless a parent asks; empty update gets `NOTHING_TO_UPDATE`; linking is idempotent and a story past Draft gets `STORY_NOT_EDITABLE`; a copyright instruction gets `CONTENT_REJECTED`; a child gets `PARENT_PROFILE_REQUIRED` on delete/archive but can favourite and never sees archived; user 2 gets 404 on everything. 5D queued/`IMAGE_JOB_IN_PROGRESS` run only when env `runImageTests` = `true` (one paid image edit). 103 green on 11/11 (folders 1, NEG, 5) |
| **6. Profiles and PIN** | 6A set/change PIN · 6B switching (PIN gate, attempt count, unknown profile, logged-out session) · 6C lock and email reset · 6D profiles create/edit/delete · 6E parent-only areas · 6F story move on delete, assign, `auth/me` | `PIN_FORMAT`/`PIN_REQUIRED`/`PIN_INVALID` with `attempts_remaining`; right PIN resets the count; 5 wrong locks (`PIN_LOCKED`), only an emailed `reset_pin` link unlocks; names 1–18, `NAME_NOT_ALLOWED`, `preset:`/`character:` avatars; child refused on profiles, store, Stripe, subscriptions, assign; deleting a profile moves its stories to the primary; `auth/me` has `pin_set`/`pin_locked`, no PIN data. 6C runs only with env `runLockTests` = `true`, in two passes (6C-11 to 6C-13 need the emailed token in `magicLinkToken`). The whole folder skips itself without `test_parent_pin`. Green 12/11 |

### How it works

- **Order flow on a fixture story** (`completedStoryId`), so orders don't wait for generation ([[use-fixture-story-for-order-flow-test]]).
- **Payment is a signed, simulated Stripe webhook** built in a pre-request script (HMAC-SHA256 over `t.payload` with the test webhook secret), because there's no Stripe sandbox for a specific checkout session ([[simulate-stripe-payment-with-signed-postman-webhook]]).
- **Async steps are bounded polls**, failing fast on order status `Error`: 3C-1 waits for the PDFs (about 24 attempts), 3D-1 for the HPBC status (about 6) ([[replace-manual-test-gates-with-bounded-polling]]).
- **HPBC runs for real** against the test SKU; staging orders end at Order Confirmed, so 3D-2/3D-3 simulate the later callbacks with the bearer token ([[run-real-fulfilment-cascade-against-staging-sku]]).
- **Tokens:** 1A sets `bearerToken` as a run-scoped variable; user 2 uses `bearerToken_user2` ([[use-run-scoped-postman-token-in-tests-login]]).
- **Removed endpoints are not recreated for tests**; outcomes are checked through user-facing endpoints ([[avoid-recreating-removed-endpoints-for-testing]]).
- **Session id:** 1A saves `sessionId` from `auth/login`'s `session_id` (added 05/11); 5E-0 uses it for `select_profile`.
- **Domain error codes** are asserted at `payload.code`; the top-level `code` is Xano's `ERROR_CODE_*`.
- **Variables:** credentials (passwords, tokens, `test_parent_pin`, webhook secrets) live in the environment as current values only. Fixed test inputs (`themeId`, `artworkStyleId`, `totalPages`, shipping and product ids) are collection variables with initial values, so exports keep them. The environment wins over the collection, and import with **Replace** (a copy duplicates the collection; Replace blanks current values of collection variables).
- Test users have `test_mode = true` (Stripe test keys, HPBC test SKU, 1-minute cancellation window).

### How to run

1. In Postman, select the `TOMALE-RN-V1-DEV` environment (it holds `auth_base_url`, `webhooks_url`, user credentials and the webhook secrets).
2. Collection Runner on `_tests`, folders 1, 3A-NEG, 3, 4, 5 and 6 in order. That's the regression run (under 10 minutes). Keep the test-account passwords in the environment current.
3. Run folder 2 on its own when the generation pipeline has changed.
4. Run after any backend change and before go-live orders. No Postman monitor before launch; at launch, a daily monitor kept under the 10-minute free-plan limit ([[defer-postman-monitor-until-launch]]). Not in CI yet ([[defer-postman-suite-ci-until-suite-split]]).
5. Keep the collection in sync with Xano by importing the OpenAPI spec ([[adopt-openapi-import-for-postman-collection-sync]]).

### Known maintenance

- **Characters backend prep:** done 05/11, folder 5 all green ([[PRD-Characters]]); 008 additions 11/11.
- **Profiles and PIN (M3 part A):** done 12/11, folder 6 green ([[m3-profiles-pin-backend-prep-brief]]).
- 3C-2 has no assertions (it only stores `hpbc_order_id`).

## 2. Not covered yet

| Area | Gap | When |
|---|---|---|
| Moderation and approval | Flagged story → parent approves → child sees it (CTO journey; approve flow not built) | M3 |
| Entitlements | Generation limits | M8 |
| App | jest-expo tests per slice: auth guard, stores, critical screens (CTO #24–#26 frontend side) | Each slice |
| CI | Postman not in CI; app CI runs lint, typecheck and tests only (security stage in M1) | M1 / later |
