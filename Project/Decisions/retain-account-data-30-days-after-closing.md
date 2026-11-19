---
type: decision
title: retain-account-data-30-days-after-closing
project: tomale-rn-v1
status: accepted
date: 2026-11-19
related:
  - "[[account-closing-micro-prd]]"
  - "[[pre-launch-checklist]]"
affects:
  - "[[backend-xano]]"
  - "[[roadmap]]"
  - Privacy Notice and Terms (Claude Docs drafts, 19/11)
features:
  - F-account
---

# Decision: retain-account-data-30-days-after-closing

## What we decided
Kyle, 19/11: when a parent closes their account, Tomale keeps the account, profiles, stories and characters for 30 days so they can come back, then deletes them from our systems. Items a parent deletes (story, character, profile) are hidden at once and deleted from our systems after 30 days. A scheduled backend job does the deleting.

Retention schedule (as published in the Privacy Notice draft):

| Data | Kept |
|---|---|
| Account, profiles, stories, pages, characters, conversations, alerts, sessions, files | 30 days after closing, then deleted |
| Deleted story, character or profile | 30 days after `deleted_at`, then deleted |
| Orders, payments, refunds (`store_orders`, `transactions`) | 6 years after the order (tax records), then deleted |
| Moderation records (`moderation_flags`) | **Proposed 2 years** from the flag, including after closing; longer only for a live police or court request. Kept indefinitely today (Kyle, 19/11: can change). |
| Crash reports (Sentry, EU) | 90 days |
| Support emails | 2 years after the last message (suggested) |
| Marketing consent (HubSpot) | Until unsubscribe; the contact is deleted on account deletion |

## Why
The Terms (§9) and Privacy Notice (§7) promise it; UK GDPR's storage-limitation principle needs a defined period; the App Store requires in-app account deletion (guideline 5.1.1(v)). A grace period lets a parent who closes by mistake come back without losing their children's stories.

## Alternatives considered
Delete at once on closing (no way back); keep data until the parent asks again (breaks storage limitation); keep moderation records indefinitely (hard to justify; 2 years proposed).

## Trade-offs accepted
Data lingers for 30 days after a parent asks to leave; backups can hold it up to the backup period longer.

## Workflow detail
Build in M7 with account deletion: [[account-closing-micro-prd]]. Published in the Privacy Notice 19/11/2026 (backups: up to 35 days). Open: moderation retention (Kyle; 2 years published), whether Apple accepts a 30-day grace period when the app states it.

## Related notes
- [[account-closing-micro-prd]]
- [[pre-launch-checklist]]
