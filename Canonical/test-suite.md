---
type: living-doc
title: test-suite
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
last_verified: 2026-10-28
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
| **1. Login & Auth.me** | 1A login, 1B `auth/me`, 1C no stuck stories, 1D refresh, 1E reused refresh | Login returns `userid`, `authToken`, `refreshToken`; `auth/me` carries `active_profile`; refresh rotates the token; a reused refresh token gets 401 `invalid_refresh_token`; no story has sat in a non-terminal state longer than `stuckStoryMaxAgeMin` (45 min) ([[replace-long-done-poll-with-stuck-story-check]]) |
| **2. Story Generation** | 2A-1 story, 2A-2 character, 2A-3 character model, 2B-1 story model | Creation endpoints and the LLM model calls; image jobs are queued. **Not in the monitor-sized run**: generation takes 10–15 minutes, so this folder runs on its own ([[use-fixture-story-for-order-flow-test]]) |
| **3A-NEG. User 2** | log in as user 2; order a story awaiting approval | `STORY_AWAITING_APPROVAL` (400) ([[block-ordering-of-stories-awaiting-parental-approval]]) |
| **3. Orders** | 3A create → patch → checkout (+ negative ownership) · 3B signed payment webhook, `check_order_paid` · 3C PDF poll · 3D HPBC confirm, Shipped callback, Error callback | Server-derived totals; no secrets in the checkout response; Stripe amount equals the order total in pence; user 2 gets 404 on user 1's checkout; payment confirmed; both PDFs attached; HPBC accepts the order; tracking stored on Shipped; an Error after Shipped is ignored and tracking kept |
| **4. Cancel & Refund** | 4A cancel after submission · 4B new order to paid · 4C–4E cancel by user 2 / user 1 · 4F refund failure · 4G duplicate event | `ORDER_NOT_CANCELLABLE` after HPBC submission; another user's cancel gets 404; cancel within the window → Cancelled + Refunded, never sent to HPBC; a failed refund puts `payment_status` back to Confirmed; a duplicate event is acknowledged without changing state |

### How it works

- **Order flow on a fixture story** (`completedStoryId`), so orders don't wait for generation ([[use-fixture-story-for-order-flow-test]]).
- **Payment is a signed, simulated Stripe webhook** built in a pre-request script (HMAC-SHA256 over `t.payload` with the test webhook secret), because there's no Stripe sandbox for a specific checkout session ([[simulate-stripe-payment-with-signed-postman-webhook]]).
- **Async steps are bounded polls**, failing fast on order status `Error`: 3C-1 waits for the PDFs (about 24 attempts), 3D-1 for the HPBC status (about 6) ([[replace-manual-test-gates-with-bounded-polling]]).
- **HPBC runs for real** against the test SKU; staging orders end at Order Confirmed, so 3D-2/3D-3 simulate the later callbacks with the bearer token ([[run-real-fulfilment-cascade-against-staging-sku]]).
- **Tokens:** 1A sets `bearerToken` as a run-scoped variable; user 2 uses `bearerToken_user2` ([[use-run-scoped-postman-token-in-tests-login]]).
- **Removed endpoints are not recreated for tests**; outcomes are checked through user-facing endpoints ([[avoid-recreating-removed-endpoints-for-testing]]).
- Test users have `test_mode = true` (Stripe test keys, HPBC test SKU, 1-minute cancellation window).

### How to run

1. In Postman, select the `TOMALE-RN-V1-DEV` environment (it holds `auth_base_url`, `webhooks_url`, user credentials and the webhook secrets).
2. Collection Runner on `_tests`, folders 1, 3A-NEG, 3 and 4 in order. That's the regression run (about 86 assertions, under 10 minutes).
3. Run folder 2 on its own when the generation pipeline has changed.
4. Run after any backend change and before go-live orders. No Postman monitor before launch; at launch, a daily monitor kept under the 10-minute free-plan limit ([[defer-postman-monitor-until-launch]]). Not in CI yet ([[defer-postman-suite-ci-until-suite-split]]).
5. Keep the collection in sync with Xano by importing the OpenAPI spec ([[adopt-openapi-import-for-postman-collection-sync]]).

### Known maintenance

- **Slice 100 backend prep:** 2A-2 stays valid; add tests for the new character endpoints and for a child profile being refused delete/archive ([[PRD-Characters]]).
- 3C-2 has no assertions (it only stores `hpbc_order_id`).

## 2. Not covered yet

| Area | Gap | When |
|---|---|---|
| Profiles | Child visibility, profile switch, PIN gate (not built) | M3 ([[roadmap]]) |
| Moderation and approval | Flagged story → parent approves → child sees it (CTO journey; approve flow not built) | M3 |
| Entitlements | Generation limits | M8 |
| App | jest-expo tests per slice: auth guard, stores, critical screens (CTO #24–#26 frontend side) | Each slice |
| CI | Postman not in CI; app CI runs lint, typecheck and tests only (security stage in M1) | M1 / later |
