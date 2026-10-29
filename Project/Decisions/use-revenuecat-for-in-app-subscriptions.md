---
type: decision
title: use-revenuecat-for-in-app-subscriptions
project: tomale-rn-v1
status: accepted
date: 2026-10-29
related:
  - "[[PRD-Subscription-Entitlement-System]]"
  - "[[PRD-transaction-webhooks-micro-prd]]"
  - "[[defer-stripe-webhook-mode-branching-to-phase-2]]"
affects:
  - subscriptions
  - transaction_webhook_events
  - "[[PRD-Subscription-Entitlement-System]]"
  - "[[PRD-transaction-webhooks-micro-prd]]"
features:
  - F-subscriptions
  - F-payments
---

# Decision: use-revenuecat-for-in-app-subscriptions

## What we decided

V1 sells the Creator subscription (monthly and annual, 1-month free trial) through Apple In-App Purchase and Google Play Billing, on **iOS and Android at launch**, using **RevenueCat** between the stores and Xano. Stripe subscriptions move to V2 with Club.

**Who owns what:**

| Thing | Source of truth | Managed in |
|---|---|---|
| Price, payment, trial, renewal, refunds | Apple / Google | App Store Connect, Play Console |
| Store products → plan (`creator`) | RevenueCat | RevenueCat dashboard |
| Whether the account is subscribed, to which plan, until when | RevenueCat | (automatic) |
| Copy of that state used by the backend | Xano `subscriptions` (mirror) | Updated from RevenueCat |
| What a plan allows (limits, discount, promotions) | Xano `entitlement_plans` | Xano |
| Usage this month | Xano `usage_counters` | Xano |
| What the app shows | `GET /me/entitlements` | Xano |

- Subscriptions belong to the **account** (`users`), never a profile. The RevenueCat app user id is a uuid on `users`, set in the SDK at login.
- The entitlement gate reads only the Xano mirror; a story request never waits on RevenueCat.
- The mirror is refreshed three ways: a sync call from the app straight after a purchase or restore; the RevenueCat webhook; a daily reconciliation task. Each refresh fetches the subscriber from RevenueCat's API and overwrites the mirror, so event order doesn't matter.
- The app uses the RevenueCat SDK only to show the paywall (store prices), buy and restore.
- **Naming:** RevenueCat's "entitlement" (on/off access) is called the **plan** in the vault; "entitlements" means Tomale's limits.

## Why

Verifying Apple's signed purchases and notifications (a certificate chain) in Xano is fiddly and easy to get wrong, and the stores' trial, renewal, grace and refund cases add a lot of work. RevenueCat handles both stores, has an Expo-compatible SDK and sends one webhook. Kyle (29/10): fine, provided it's clear who owns what.

## Alternatives considered

- Direct Apple App Store Server API and Google Play Developer API from Xano (more work, two webhook formats, certificate checks).
- iOS only at launch (halves the work; rejected, Android is in V1).

## Trade-offs accepted

Another service holds subscription state, and there's a fee once revenue grows (free up to about $2.5k monthly tracked revenue, then about 1%; to confirm on RevenueCat's pricing page before signing up). The Xano mirror makes it possible to move off later.

## Related notes

- [[PRD-Subscription-Entitlement-System]]
- [[PRD-transaction-webhooks-micro-prd]]
