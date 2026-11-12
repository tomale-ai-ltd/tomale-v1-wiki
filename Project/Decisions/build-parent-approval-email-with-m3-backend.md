---
type: decision
title: "build-parent-approval-email-with-m3-backend"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
  - "[[m3-approvals-backend-prep-brief]]"
  - "[[use-https-web-intermediary-for-magic-link-redirect]]"
  - "[[use-per-build-variant-url-schemes]]"
affects:
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "ai pipeline/content_moderation_story_text"
features:
  - F-parental-oversight
  - F-notifications
---

# Decision: build-parent-approval-email-with-m3-backend

## What we decided
Kyle, 12/11: the parent "approval needed" email is built now, with the rest of the M3 approvals backend, not later. Kyle prepares the Resend template, the `tomale.ai/app/approvals` page and the env vars (change set B0).

## Why
Not discussed in session notes.

## Alternatives considered
Not discussed in session notes.

## Trade-offs accepted
Not discussed in session notes.

## Workflow detail
B0 (Kyle): Resend template with one variable `approvals_url` and no story content; a Squarespace page that opens `tomalerntest://approvals` (dev; `tomale://approvals` in production); env vars `app_url_scheme`, `approvals_url`, `resend_approval_template`. B3 sends the email from the moderation function inside a `try_catch` so an email failure never fails moderation. The email is checked once by hand.

## Related notes
[[m3-approvals-backend-prep-brief]], [[m3-approvals-xano-prompts]], [[PRD-Parental-Oversight-Content-Approval]]
