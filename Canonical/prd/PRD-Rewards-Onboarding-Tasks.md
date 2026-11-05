---
type: prd
title: PRD-Rewards-Onboarding-Tasks
project: tomale-rn-v1
status: draft
version: 0.1
date: 2026-11-05
owner: vault
features:
  - F-rewards
related:
  - "[[split-rewards-into-celebrations-and-onboarding-tasks]]"
  - "[[PRD-Home-Dashboard]]"
  - "[[PRD-Subscription-Entitlement-System]]"
  - "[[PRD-Store-Orders]]"
---

# PRD: Rewards and onboarding tasks (stub)

> **Stub, 05/11/2026.** Both parts are in V1 ([[split-rewards-into-celebrations-and-onboarding-tasks]]). To be filled in before slicing.

## 1. Celebrations (children)
- Reward animation when a story or a character is finished (the character reveal in [[PRD-Chatbot-Create-Character]] is the first).
- Collectable badges for things made: first story, first character, five characters, first book read to the end, and so on.
- Shown on Home and the profile. No streaks, timers or "come back" prompts (ICO Children's Code).

## 2. Onboarding tasks (parents, first month)
- Automated tasks starting after onboarding, e.g. create your first story, add a child profile, create 3 stories, read a story with read-to-me, preview a book.
- Completing tasks earns rewards: a discount on a printed book (Stripe coupon or promotion code), a free Creator trial (RevenueCat offer).
- Progress card on the parent's Home; rewards are claimed on the parent profile only.

## 3. Out of V1
- Tomale currency ([[v2-backlog]]).

## 4. Open questions
- The task list, the rewards and their values; how long the window is (30 days from sign-up or from onboarding).
- Backend: task definitions, per-account progress, a rewards ledger, idempotent award on the triggering event (story created, order paid).
- Abuse: one reward per household; deleted stories still count or not.
- How a discount applies at checkout (server-side, checked against Xano prices as today).
- Slice: after Store (M6) for discounts and Subscriptions (M8) for trials.
