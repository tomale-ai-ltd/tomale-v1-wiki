---
type: prd
title: PRD-Parental-Oversight-Content-Approval
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-parental-oversight
related:
  - "[[PRD-Profiles]]"
  - "[[v1-feature-map]]"
  - "[[story-creation-flow]]"
---

# **PRD — Parental Oversight & Content Approval**

> **Changes in 2.0 (B9, 29/10/2026):** fields matched to the live schema (`parental_approval_required`, `parent_approved`, `status_moderation`); V1 channel decided: an approvals inbox in the parent profile built on `user_alerts`, plus a notification email that opens the inbox (Kyle, 29/10); the child sees a "Waiting for a grown-up" card; approval happens in the app only, so email approval tokens are dropped from V1; the PIN gate on switching profiles is a dependency; ordering a story awaiting approval is already blocked. What's built and what's missing is marked in §5.

Product: Tomale
Feature: Parental Oversight & Content Approval
Version: V1 (Launch-Grade)

## 1. Purpose

Tomale allows children to create AI-generated stories. Some stories may include sensitive but appropriate themes (e.g. bullying, illness, grief). This PRD defines a parental oversight system that locks sensitive content until a parent explicitly approves it, enforced server-side and suitable for app store review.

## 2. Design Principles

- **Moderation outcomes and lifecycle are separate.** A story needing approval still completes normally (Draft → Preparing → In Queue → Done); access is controlled by flags. Only a hard moderation **fail** changes the lifecycle (status `Blocked`) ([[formalise-story-status-lifecycle]]).
- Enforcement is driven by explicit boolean flags.
- Household account with multiple profiles ([[PRD-Profiles]]).
- Backend-first enforcement: nothing locked is ever sent to a child profile.

## 3. User Model

Users represent the household account (email, subscription, legal responsibility). User profiles represent parent or child usage under the same account.

## 4. Moderation Model

The story-text moderation step sets `instant_stories.status_moderation`:

| Outcome | `status_moderation` | Effect |
|---|---|---|
| Pass | `Pass` | Visible to the creating profile and parents |
| Sensitive but allowed | `Parental Approval` | `parental_approval_required = true`; locked for the child until a parent approves |
| Fail | `Fail` | `status = Blocked`, `blocked_reason` set; never shown |
| Not yet run | `Pending` | Not shown to the child |

## 5. Data Model (`instant_stories`)

| Field | State |
|---|---|
| `status_moderation` (Pass, Fail, Parental Approval, Pending) | Built |
| `parental_approval_required` (bool) | Built |
| `parent_approved` (bool) | Built |
| `blocked_reason` (text) | Built (used for Fail) |
| `approved_by_profile_id` (uuid) | **To add** |
| `approved_at` (timestamp) | **To add** |
| `approval_rejected_at` (timestamp) | **To add** (records a rejection) |

**Rule:** if `parental_approval_required = true` and `parent_approved = false`, child access is locked.

## 6. Functional Flow

1. A child creates a story.
2. Moderation returns `Parental Approval`, so `parental_approval_required = true` (built).
3. An alert is created for the household (built: `user_alerts`, type `Content Moderation`, `action_url` pointing at the story). **To change:** the alert must be shown to **parent profiles only**. `user_alerts` is account-level today, so it needs an audience field (e.g. `audience = parents`) or a target profile.
4. The parent is also emailed (Resend, notification only, no approval in the email). The link opens the app at the approvals inbox (§8a).
5. The parent switches to their profile (PIN required, [[parental-gate-on-profile-switch]]), opens the approvals inbox and taps the alert, which deep-links to the story.
6. The parent reads the full story and approves or rejects it (no editing in V1).
7. On approval, the child can open it. On rejection, it stays locked and the parent can delete it.
8. Ordering a print copy is blocked until approval (built: `STORY_AWAITING_APPROVAL`, [[block-ordering-of-stories-awaiting-parental-approval]]).

## 7. Backend Function Logic (Xano)

### 7.1 Story reads (built, one change)
`GET /instant_stories` and `GET /instant_stories/{id}` use an allowlist on `status_moderation` (`Pass`, or `Parental Approval` with `parent_approved = true`). Today a child profile simply **doesn't see** a story awaiting approval ([[per-child-story-visibility]]). **To change (decided 29/10):** the list returns a redacted card for the child instead: title and "Waiting for a grown-up" only, never pages or cover. `GET /instant_stories/{id}` stays refused for the child until approval.

### 7.2 Approve: `POST /instant_stories/{id}/approve` (to build)
Preconditions:
- Caller's active profile is a parent profile (not `is_child`)
- Same household (`users_id` matches `$auth.id`)
- `parental_approval_required = true` and `parent_approved = false`

Effects:
- `parent_approved = true`, `approved_by_profile_id`, `approved_at`
- Mark the related alert read
- Optional: an alert to the child profile ("Your story is ready!")

### 7.3 Reject: `POST /instant_stories/{id}/reject` (to build)
Same preconditions. Story stays locked; `approval_rejected_at` set; alert resolved.

### 7.4 Removed from V1
Email approval tokens (`consume_approval_token`): approval happens only in the app, behind the PIN.

## 7a. Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** `instant_stories` (`status_moderation`, `parental_approval_required`, `parent_approved`, `blocked_reason`), the allowlist on story reads, `user_alerts` (`type`, `action_url`, `action_label`, `is_read`), `create_user_alert`, the ordering gate.

**To build:**
1. **`instant_stories` fields:** `approved_by_profile_id` (uuid), `approved_at`, `approval_rejected_at`.
2. **Alerts for parents only:** add an audience to `user_alerts` (e.g. `audience` = all | parents, default all); alert reads filter on the active profile; the moderation step creates its alert with `audience = parents`.
3. **`POST /instant_stories/{id}/approve`** and **`/reject`** (parent profile, same household, preconditions in §7.2–7.3); approve also marks the alert read and can alert the child.
4. **Child's waiting card:** the story list returns a redacted card for stories awaiting approval (§7.1).
5. **Notification email:** a Resend template sent with the parent alert, linking to the approvals inbox (§8a); no token.
6. **Backend-generated links** (`action_url`, email link) use the per-environment scheme ([[use-per-build-variant-url-schemes]]).
7. **Postman `_tests`:** child can't open a locked story; child refused on approve; parent approves → child can open; reject keeps it locked; alert visible to parents only.

## 8. UI Requirements

Child UI:
- Locked state on the story card
- "Waiting for a grown-up to say yes" message

Parent UI:
- Approvals inbox (filtered alerts) with a count badge
- Full story view with Approve / Reject
- Rejected stories listed, with Delete

## 8a. Email link and resuming the route

The email carries a plain link to the approvals inbox (e.g. `https://tomale.ai/app/approvals`, handled like the magic link: a web page that opens the app, until Universal Links exist), and **no token**. The app remembers the requested route and resumes it once the gates are passed:

| App state when the link opens | What happens |
|---|---|
| Logged out | Login → lands on the primary (parent) profile → approvals inbox |
| Session restored, parent profile active | Straight to the approvals inbox |
| Session restored, child profile active (or picker shown) | Profile picker with the parent profile highlighted → PIN → approvals inbox |

The pending route is kept in memory only, cleared once used or when the user goes elsewhere. Any route marked parent-only (approvals, store, settings) goes through the same check.

## 9. Security & Compliance

- No locked payload sent to a child profile.
- Approve/reject only from a parent profile; reaching a parent profile from a child profile requires the PIN.
- Full audit trail: who approved and when (`approved_by_profile_id`, `approved_at`, `approval_rejected_at`).

## 10. Open Questions

None. Resolved 29/10: the child sees a "Waiting for a grown-up" card; parents get an in-app alert and a notification email linking to the inbox; no editing before approval in V1.

## 11. Verdict

A launch-grade parental oversight system that separates moderation from lifecycle, prevents trivial bypass (server-side locks plus the PIN), and satisfies app store expectations.
