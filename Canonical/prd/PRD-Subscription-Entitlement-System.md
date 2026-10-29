---
type: prd
title: PRD-Subscription-Entitlement-System
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-subscriptions
related:
  - "[[gate-image-generation-with-entitlements-at-story-creation]]"
  - "[[PRD-transaction-webhooks-micro-prd]]"
  - "[[roadmap]]"
---

# **MICRO-PRD: Subscription & Entitlement System**

> **Changes in 2.0 (B9, 29/10/2026):**
> - Tiers set by Kyle (29/10): **Free, Creator, Club**. The conflicting `creator` / `delivery` labels are gone.
> - Entitlements limit story and image generation at creation; image generation after payment is gone ([[gate-image-generation-with-entitlements-at-story-creation]]).
> - "Unlimited" generation is replaced by a high fair-use limit, since unlimited image generation isn't affordable.
> - Live tables and endpoints are noted.
> - The ten "additions" are folded into the main text.
> - From the Store review (Kyle, 29/10): Creator and Club get 25% off books; Club's monthly A4 paperback is ordered in the store at £0 with free standard shipping; a story's images can't be regenerated in V1 ([[v2-backlog]]).
> - New: "limit reached" behaviour for child and parent profiles; backend prep.
> - Second review (Kyle, 29/10): Free is 4 stories a month; Creator 30 (fair use); limits live in dated, editable entitlement records so promotions need no code; a 1-month Creator free trial; annual plans at launch (12 months for the price of 10). **Club moves to V2** because of the App Store rules on bundling a physical book ([[v2-backlog]]).
> - Third review (Kyle, 29/10): iOS and Android at launch, through **RevenueCat** ([[use-revenuecat-for-in-app-subscriptions]]); Stripe subscriptions move to V2 with Club.
>
> Not built yet; launch-critical backend work ([[roadmap]] M8).

## **Goal**
Provide a **tiered subscription system** that controls access to cost-incurring features (story and image generation, included books, discounts) without coupling business logic to plan names.

## **Tiers**

| Tier | Price (to confirm) | Story generation | Store orders | Included books |
|---|---|---|---|---|
| **Free** | £0 | 4 stories and 4 character images a month | Full price | — |
| **Creator** | £6.99 / month, or £69.90 / year (12 months for the price of 10) | 30 stories and 30 character images a month (fair use) | 25% off books | — |

Everyone gets the full Bookshelf, e-reader and store. The discount applies to the book, not shipping ([[PRD-Store-Orders]] pricing rules). Limits are values in the entitlement records, not code, so they can be changed or promoted without a release (see Entitlement records).

**Club (£20 / month, a monthly printed book) is V2.** Apple requires in-app purchase for digital subscriptions and forbids it for physical goods, and its guidelines don't settle a subscription that bundles both. Kyle's alternative (29/10): make the book the paid product and include Creator for free. That could fit Apple's multiplatform rule (3.1.3(b): content bought elsewhere may be used in the app if it's also sold in-app, which Creator is), with Club sold on the website through Stripe, but it's untested with App Review and adds a web purchase flow. Parked in [[v2-backlog]]; ask App Review before building it.

**What counts against the limit:** a new story (text and its page images together, narration included) and a character image, including "re-create image" on a character ([[PRD-Characters]]). A story's images can't be regenerated in V1.

## **Scope**
Covers: tiers, trials, entitlement resolution, usage limits, billing state reconciliation, in-app purchase.

## **Non-Goals**
Pricing experiments, price discount campaigns, education / enterprise tiers. (Limit promotions are in scope, via dated entitlement records.)

## **Core Concepts (non-negotiable)**
- **Plans ≠ logic.** Feature code never checks a plan name; it checks entitlements.
- **Generation requires entitlement.** No story or image job runs without passing the gate.
- **Trials are overlays, not plans.**
- **Apple / Google own the money; RevenueCat owns subscription state; Xano owns what a plan allows** (see Who owns what).

## **Backend Requirements**

### Data models
- **`products`** (live): already has `Type` (subscription-monthly, subscription-annual, physical-product), `billing_frequency`, `subscription_level`, `apple_product_id`, `google_product_id`, Stripe IDs.
- **`subscriptions`** (live, to extend): `users_id`, `products_id`, `status` (today Active / Inactive → extend to active, trial, past_due, grace, cancelled), `billing_frequency`, period start/end, cancel fields. **Add:** `source` (apple | google | stripe), provider subscription id per source.
- **Entitlement records** (to build): an `entitlement_plans` table, one row per plan per period, with typed columns:
```json
{
  "plan_key": "free | creator",
  "products_id": "integer (null for free)",
  "can_generate_text": "boolean",
  "can_generate_images": "boolean",
  "monthly_story_limit": "integer",
  "monthly_character_image_limit": "integer",
  "book_discount_pct": "integer",
  "valid_from": "timestamp",
  "valid_to": "timestamp (null = open-ended)",
  "priority": "integer"
}
```
  Values are edited in Xano without a release. A **promotion** is a new row for the same plan with a date range and a higher priority (e.g. Creator with 40 stories during December); when it ends, the base row applies again. Resolution picks the highest-priority row valid now; exactly one base row per plan must have no end date.
- **Usage counters** (to build), reset each calendar month (UTC): `stories_generated_count`, `images_generated_count`, `included_books_used`.
- **Trial:** a 1-month free trial of Creator, set up as an introductory offer on the Apple and Google subscription products. The store handles eligibility (once per Apple / Google account) and converts it to paid unless cancelled; the subscription arrives with status `trial` through the purchase notifications. No trial fields on `users`.

### Entitlement resolution
At request time: the active subscription's plan (`creator` when active, trial, or cancelled but inside the paid period), else `free`; then the current `entitlement_plans` row for that plan.

### Entitlement gate
One backend function runs **before** story generation, character image creation and re-creation, and included-book orders (page and cover image jobs belong to an already-approved story and aren't re-checked). It returns `{allowed, reason, remaining}` and is deterministic. The story endpoints return a stable error code when refused (e.g. 400 `ENTITLEMENT_LIMIT_REACHED`); the app handles that code from Slice 200 onward.

### Hard rules
- Fail closed if entitlements can't be resolved.
- Counters increment before execution; no rollback on failure in V1.
- A trial can be used once per Apple / Google account (enforced by the store).
- Snapshot the entitlements on each job (`image_jobs`, story generation, PDFs) for audit.
- Daily reconciliation against providers, plus webhooks ([[PRD-transaction-webhooks-micro-prd]]).

### State rules
| State | Effect |
|---|---|
| active / trial | Full tier entitlements |
| past_due | Cost-incurring features restricted immediately |
| grace | Reading allowed, new generation blocked |
| cancelled | Access until `current_period_end`, then Free |
| Upgrade mid-cycle | Entitlements increase immediately; usage unchanged |
| Downgrade mid-cycle | Entitlements reduce immediately; no refund of usage |

### Endpoint
`GET /me/entitlements` (to build) returns plan, status, source, entitlements, usage, remaining and trial. It's the single source for UI gating; the app never computes entitlements itself.

## **In-app purchase**
Digital subscriptions in the iOS and Android apps must use Apple In-App Purchase and Google Play Billing. V1 uses **RevenueCat** for both stores ([[use-revenuecat-for-in-app-subscriptions]]). Entitlements don't differ by store; the store is used only for reconciliation, debugging and reporting.

### Who owns what
| Thing | Source of truth | Managed in |
|---|---|---|
| Price, payment, trial, renewal, refunds | Apple / Google | App Store Connect, Play Console |
| Store products → plan (`creator`) | RevenueCat | RevenueCat dashboard |
| Whether the account is subscribed, to which plan, until when | RevenueCat | (automatic) |
| Copy of that state used by the backend | Xano `subscriptions` (mirror) | Updated from RevenueCat |
| What a plan allows (limits, discount, promotions) | Xano `entitlement_plans` | Xano |
| Usage this month | Xano `usage_counters` | Xano |
| What the app shows | `GET /me/entitlements` | Xano |

**Naming:** RevenueCat's "entitlement" (on/off access) is the **plan** here; "entitlements" means Tomale's limits.

### Purchase flow
1. A parent profile opens the paywall (RevenueCat offerings, store prices) and buys.
2. The app calls `POST /me/subscription/sync`; Xano fetches the subscriber from RevenueCat's API and updates the mirror.
3. The RevenueCat webhook arrives and triggers the same refresh ([[PRD-transaction-webhooks-micro-prd]]).
4. The app refetches `GET /me/entitlements`.
"Restore purchases" follows the same path. A daily task refreshes every active subscription in case a webhook was missed.

## **Frontend Requirements**
- Plan comparison: what's included and what costs extra.
- Current plan, remaining stories this month, included book status, trial countdown.
- "Limit reached" sheet with upgrade options (native purchase sheets).
- Locked art-style tiles ([[return-full-artwork-catalogue-with-locked-tiles]]).
- Purchases only from a parent profile.

### Limit reached
Plans are account-level, so the whole household shares one allowance ([[PRD-Profiles]]).
- **Parent profile:** the sheet shows what's left, when it resets, and upgrade options.
- **Child profile:** a friendly lock card with **"Ask a grown-up"**, which opens the profile picker and the PIN pad; no prices or purchase buttons are shown to a child. The story stays a Draft and can be finished once allowance is available ([[PRD-Chatbot-Story-Conversations]] §6a).

## **Backend prep** (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** `products` with subscription types and Apple/Google/Stripe ids; `subscriptions` (Active/Inactive, Stripe id, period dates); `GET /subscriptions` and `/subscriptions/{id}`; `users.stripe_customer_id`.

**To build:**
1. **`entitlement_plans` table** (above), seeded with Free (4 stories, 4 character images) and Creator (30 and 30); and **`products` records** for Creator monthly (£6.99) and annual (£69.90) with Apple and Google product ids and the 1-month introductory offer set up in App Store Connect and Play Console.
2. **`subscriptions` as the RevenueCat mirror:** extend `status` (active, trial, past_due, grace, cancelled, expired); add `plan_key`, `store` (app_store | play_store), `store_product_id`, `revenuecat_synced_at`, `environment` (sandbox | production); fix `cancel_at_period_end` (a date today, should be a bool). **`users.revenuecat_app_user_id`** (uuid), set at sign-up and passed to the SDK at login.
3. **Usage counters:** a `usage_counters` table per account and month (`users_id`, `period` e.g. `2027-02`, `stories_generated`, `character_images_generated`).
4. **Promotion rules:** a check (or a test) that each plan always has exactly one open-ended base row.
5. **`check_entitlement` function** returning `{allowed, reason, remaining}`; called by story generation, `POST /characters` and `POST /characters/{id}/regenerate_image`; the store reads `book_discount_pct` from it. Refusal: 400 `ENTITLEMENT_LIMIT_REACHED`.
6. **`GET /me/entitlements`** for the app.
7. **Snapshots:** `entitlement_snapshot` JSON on `instant_stories`, `image_jobs` and `store_orders`.
8. **RevenueCat sync:** a `revenuecat_sync_subscriber` function (calls RevenueCat's subscriber API with the secret key from environment variables, maps the plan and status, overwrites the mirror); `POST /me/subscription/sync` calls it and refuses child profiles (400 `PARENT_PROFILE_REQUIRED`). The webhook is in [[PRD-transaction-webhooks-micro-prd]].
9. **Daily reconciliation task:** runs the sync for every subscription that's active, in trial or in grace.
10. **Store and RevenueCat setup (not Xano):** Creator monthly and annual products with the 1-month introductory offer in App Store Connect and Play Console; RevenueCat project, plan `creator`, offering; transfer behaviour set so one Apple / Google account can't power several Tomale accounts.
11. **Postman `_tests`:** Free's 5th story refused; Creator discount; a promotion row overrides the base and expires; trial subscription gets Creator entitlements; child refused on purchase; downgrade takes effect immediately.

## **Acceptance Criteria**
- No story or image job runs without passing the gate.
- A trial can't be restarted.
- Cancelling removes future entitlements, not purchased content.
- Changing tiers needs no code change.
- The same entitlements apply whether the purchase came through Apple, Google or Stripe.

## **Open Questions**
None. Resolved 29/10 (approved by Kyle): Free 4 stories and 4 character images a month, Creator 30 and 30; £6.99 monthly, annual at 12 for 10; a 1-month Creator trial as a store-managed introductory offer (the lighter build; the stores enforce one trial per account, and starting a new account to get another trial loses access to existing stories); Club moved to V2.
