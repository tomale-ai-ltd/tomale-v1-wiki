---
type: prd
title: PRD-Home-Dashboard
project: tomale-rn-v1
status: draft
version: 0.1
date: 2026-11-05
owner: vault
features:
  - F-home
related:
  - "[[use-profile-aware-bottom-tabs-with-home-dashboard]]"
  - "[[PRD-Rewards-Onboarding-Tasks]]"
  - "[[v1-feature-map]]"
---

# PRD: Home dashboard (stub)

> **Stub, 05/11/2026.** Captures Kyle's direction from the navigation discussion; to be filled in before its slice is specified.

## 1. Overview
Home is the first tab for every profile: a dashboard that gets a parent or child back into what they love quickly.

## 2. Content (first pass)
- **Greeting band:** profile avatar, "Hello Mia", colourful illustrated header (reference: Kyle's 05/11 layout image).
- **Recent stories:** the profile's latest stories, including ones still being illustrated.
- **Favourite characters:** characters with `is_favourite`, with a link to Characters.
- **Announcements:** new artwork styles, themes, offers. Child profiles see creative news only, never prices or offers.
- **Onboarding tasks** (parent profile, first month): progress card from [[PRD-Rewards-Onboarding-Tasks]].
- Badges earned (child), from the celebrations part of rewards.

## 3. Open questions
- Where announcements come from (a Xano table managed by Kyle, or a CMS).
- Whether `activities` and `fact/random` (home-screen endpoints with no PRD) are used or removed.
- Empty state for a new account.
- Slice and order: needs Bookshelf (recent stories) and Characters (favourites).
