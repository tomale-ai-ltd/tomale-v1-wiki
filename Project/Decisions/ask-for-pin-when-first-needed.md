---
type: decision
title: "ask-for-pin-when-first-needed"
project: tomale-rn-v1
status: accepted
date: "2026-11-17"
related:
  - "[[2026-11-17-001]]"
  - "[[parental-gate-on-profile-switch]]"
  - "[[PRD-Profiles]]"
affects:
  - "[[PRD-Profiles]]"
features:
  - F-profiles
  - F-onboarding
---

# Decision: ask-for-pin-when-first-needed

## What we decided
Until the onboarding walkthrough (M7), the app asks the parent to set their PIN when it's first needed: adding the first child profile (the backend refuses with `PIN_NOT_SET` otherwise) or any other step that needs it. "Change PIN" sits in Manage profiles. M7 onboarding reuses the same Set PIN screen (Kyle, 17/11).

## Why
The backend already requires a PIN before a child profile exists; building the onboarding walkthrough now would pull M7 work into M3.

## Alternatives considered
Building the onboarding step (verify email → name → PIN) in M3.

## Trade-offs accepted
Until M7, a parent who never adds a child never sets a PIN, which is fine because there's nothing to protect.
