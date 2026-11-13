---
type: plan
title: "M3 backend prep, part B: parental approvals (inbox, approve/reject, waiting card, email)"
project: tomale-rn-v1
status: active
date: 2026-11-12
related:
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "[[m3-profiles-pin-backend-prep-brief]]"
  - "[[per-child-story-visibility]]"
  - "[[block-ordering-of-stories-awaiting-parental-approval]]"
  - "[[use-per-build-variant-url-schemes]]"
  - "[[use-https-web-intermediary-for-magic-link-redirect]]"
---

# M3 backend prep, part B: parental approvals

Goal: every backend item in [[PRD-Parental-Oversight-Content-Approval]] §7a built and tested before `/speckit.specify` for M3. Depends on part A (PIN), done 12/11.

## Kyle's decisions (12/11)
- **A rejected story is hidden from the child** (no "not this one" card). The parent can delete it or move it to their own profile (assign, part A).
- **The parent email is built now**, with the rest of the backend. Kyle prepares the Resend template and the web page (change set B0).

## What's live (mirror 773794d, 12/11)
- `instant_stories`: `status_moderation`, `parental_approval_required`, `parent_approved`, `blocked_reason`. No approval audit fields.
- `ai pipeline/content_moderation_story_text`: on `Parental Approval` sets the flags and calls `notifications/create_user_alert` (type `Content Moderation`, message includes the moderation reason, `action_url` hard-coded `tomalerntest://stories/<id>`). No email.
- `ai pipeline/story_completion_check`: on Done sends "<title> is ready!" (type `System`) to the **whole account**, including for stories still awaiting approval.
- `user alerts` table: account-level only (`users_id`); no audience, profile or story link. `notifications/create_user_alert` uses a `dblink` input. Reads (`GET /user_alerts`, `PATCH /user_alerts/{id}`, `PATCH /users/user_alerts/mark_all_read`) filter on `users_id` only, so a child sees the moderation alert today.
- `GET /instant_stories`: a child never sees a story awaiting approval (the allowlist); no approval state in the output. Ordering is blocked while awaiting (`STORY_AWAITING_APPROVAL`).
- Env vars: `resend_api_key`, `resend_from_email`, `resend_magic_link_template`, `magic_link_redirect_uri`; no app-scheme or approvals settings.

## Change set B0 (Kyle, before B3)
1. **Resend template** "approval needed" with one variable `approvals_url`. Wording, no story content: "One of your children's stories needs a quick look from you before they can read it. Open Tomale to review it." Button: "Review in Tomale" → `{{approvals_url}}`.
2. **Web page** `https://tomale.ai/app/approvals` (Squarespace, like `/verify-email`): a button that opens `tomalerntest://approvals` (dev; `tomale://approvals` in production).
3. **Xano env vars:** `app_url_scheme` = `tomalerntest`; `approvals_url` = `https://tomale.ai/app/approvals`; `resend_approval_template` = the template id.

## Change set B1: schema
- `instant stories`: `approved_by_profile_id` (uuid, nullable, table user_profiles), `approved_at` (timestamp, nullable), `approval_rejected_at` (timestamp, nullable).
- `user alerts`: `audience` (enum `all` | `parents` | `profile`, default `all`), `user_profiles_id` (uuid, nullable, table user_profiles), `instant_stories_id` (int, nullable, table instant stories). Existing rows count as `all`.

## Change set B2: alerts by audience
- `notifications/create_user_alert`: replace the `dblink` input with explicit inputs: `type`, `message`, `users_id`, `action_url?`, `action_label?`, `audience?` (default `all`), `user_profiles_id?` (required when `audience` = `profile`), `instant_stories_id?`.
- One visibility rule on all three alert endpoints (list, single PATCH, mark all read): a row is visible when `users_id == $auth.id` and (`audience` is `all` or null, or (`audience == "parents"` and the active profile is a parent, strict), or (`audience == "profile"` and `user_profiles_id == active_profile.id`)). Not visible → 404 on the single PATCH; mark-all-read only touches visible rows.

## Change set B3: moderation and completion
- `content_moderation_story_text`, `Parental Approval` branch: alert with `audience: "parents"`, `instant_stories_id`, message without the moderation reason ("A story needs your review before your child can read it."), `action_url` = `$env.app_url_scheme ~ "://approvals"`. Then send the email to the account's address with `admin/resend_dynamic_send` (`template_id: $env.resend_approval_template`, `variables: {approvals_url: $env.approvals_url}`) inside a `try_catch`: an email failure must never fail moderation. The reason stays in `blocked_reason` for the parent's story view.
- `story_completion_check`: the "is ready!" alert goes to the creating profile (`audience: "profile"`, `user_profiles_id`, `instant_stories_id`), and is **skipped** while the story awaits approval (`parental_approval_required === true && parent_approved !== true`). `action_url` uses `$env.app_url_scheme`.

## Change set B4: approve and reject
`POST /instant_stories/{instant_stories_id}/approve` and `/reject` (auth users):
- Strict parent check (400 `PARENT_PROFILE_REQUIRED`); story on this account, not deleted (404 `STORY_NOT_FOUND`); `parental_approval_required === true` (else 400 `NOT_AWAITING_APPROVAL`); not already approved (400 `ALREADY_APPROVED`).
- **Approve:** `parent_approved = true`, `approved_by_profile_id` = active profile, `approved_at = now`, `approval_rejected_at = null` (a parent may change their mind after a rejection). Mark that story's `Content Moderation` alerts read. If the story is `Done`, send the creating profile "<title> is ready!" (`audience: "profile"`); otherwise the completion check sends it later. Response `{instant_stories_id, approval_state: "approved", approved_at}`.
- **Reject:** `approval_rejected_at = now`, story stays locked; mark its alerts read. Response `{instant_stories_id, approval_state: "rejected"}`.
- **Blocked alert (added 13/11, Kyle):** in `content_moderation_story_text`, the `blocked` branch alert gets `audience: "parents"` and `instant_stories_id`, so a child no longer sees the moderation reason. Message unchanged.

## Change set B5: story reads
- Both story GETs add a derived `approval_state`: `none` (no approval needed), `awaiting` (required, not approved, not rejected), `approved`, `rejected`.
- `GET /instant_stories`, child: also returns their own **awaiting** stories as redacted cards `{id, title, approval_state: "awaiting", created_at}` (no cover, pages, prompt or moderation data). Rejected stories stay hidden. Parent: unchanged list plus `approval_state`, and an optional input `approval_state` (`awaiting` | `rejected`) for the inbox and the rejected list.
- `GET /instant_stories/{id}`: unchanged for a child (404 until approved); parent output adds `approval_state`, `blocked_reason` (the reason it needs review), `approved_at`, `approval_rejected_at`.
- `stories/visible_story_ids` is unchanged (it lists stories a reader can open; counts exclude awaiting ones). Update the "must stay identical" comment in `GET /instant_stories` to say the child's awaiting cards are the one deliberate difference.

## Order and testing
B0 (Kyle) and B1 first; then B2 → B3 → B4 → B5, publishing and testing each. Strict checks; explicit inputs; guard lists; table name `"instant stories"` (with the space) everywhere; no blank table names.

**Test fixture (Kyle, in the Xano table, once):** a Done story on the test child profile with `status_moderation = "Parental Approval"`, `parental_approval_required = true`, `parent_approved = false`, `approval_rejected_at` empty; its id in env `approvalStoryId`. A parents alert row for it (`audience: parents`, `instant_stories_id`). Before each run of folder 7, reset `parent_approved = false` and `approval_rejected_at` empty (folder 7 approves it). Folder gated by env `runApprovalTests` = `true`.

Postman folder 7 (Claude builds): child sees the awaiting card with no cover/pages; child gets 404 on the story; child doesn't see the parents alert; child refused on approve/reject; parent sees the alert and the story with `approval_state: awaiting` and `blocked_reason`; reject → child no longer sees the card; approve after reject → child opens the story, alert read, child alert present; second approve → `ALREADY_APPROVED`; a story that never needed approval → `NOT_AWAITING_APPROVAL`; order gate still refuses an awaiting story.

The email is checked once by hand: trigger moderation on a sensitive test story (or call the function in Run & Debug) and confirm the email arrives with the right link.
