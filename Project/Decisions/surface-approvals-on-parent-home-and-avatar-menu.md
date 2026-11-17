---
type: decision
title: "surface-approvals-on-parent-home-and-avatar-menu"
project: tomale-rn-v1
status: accepted
date: "2026-11-17"
related:
  - "[[2026-11-17-001]]"
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "[[use-profile-aware-bottom-tabs-with-home-dashboard]]"
affects:
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "[[PRD-Home-Dashboard]]"
features:
  - F-parental-oversight
  - F-home
---

# Decision: surface-approvals-on-parent-home-and-avatar-menu

## What we decided
The approvals inbox has no tab. A parent reaches it from a "Stories to review (N)" card on the parent Home and from an Approvals entry with a count badge in the header avatar menu; the approval email link lands on the inbox (Kyle, 17/11).

## Why
Parent tabs are already at five, the platform ceiling; approvals are occasional, so a Home card and a badge are enough to be noticed.

## Alternatives considered
Avatar menu only; a "Needs review" section inside Bookshelf.

## Trade-offs accepted
The Home dashboard isn't built yet (later slice), so 010 adds a minimal Home card that the dashboard slice keeps.
