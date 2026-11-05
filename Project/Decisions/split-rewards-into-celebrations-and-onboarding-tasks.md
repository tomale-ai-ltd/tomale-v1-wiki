---
type: decision
title: "split-rewards-into-celebrations-and-onboarding-tasks"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-002]]"
  - "[[PRD-Rewards-Onboarding-Tasks]]"
  - "[[PRD-Subscription-Entitlement-System]]"
affects:
  - "[[roadmap]]"
  - "[[v1-feature-map]]"
  - "[[v2-backlog]]"
features:
  - F-rewards
---

# Decision: split-rewards-into-celebrations-and-onboarding-tasks

## What we decided

Rewards come in two parts, both in V1:

1. **Celebrations for children:** animated reward moments when a story or character is finished, and collectable badges for what the child made ("First story", "Five characters"). Mostly app-side.
2. **First-month onboarding tasks for parents:** automated tasks after onboarding (for example "Create 3 stories in your first month") that earn real rewards: a discount on a printed book or a free Creator trial. Its own slice in V1, with a backend ledger and links to Stripe coupons and RevenueCat offers ([[PRD-Rewards-Onboarding-Tasks]]).

A **Tomale currency** is not in V1 ([[v2-backlog]]).

## Why

Kyle (05/11) wants to lean into interactive rewards around creation, and to use first-month tasks to drive early engagement and conversion. Splitting them keeps the child-facing part cheap and safe while the money-linked part gets a proper backend.

## Constraints

- **ICO Children's Code:** no nudges that push a child to use the app longer or to spend (no streaks, no "come back tomorrow"). Child rewards celebrate what was made, never time spent. Anything with money attached is shown and claimed on the parent profile only.
- **Virtual currency:** in a children's app it draws Apple and UK consumer-law scrutiny, especially if it can be bought; deferred.

## Trade-offs accepted

- Onboarding tasks add a slice to a tight January launch and depend on subscriptions (M8) for trial rewards.
