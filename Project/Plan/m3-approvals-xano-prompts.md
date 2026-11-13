---
type: plan
title: "M3 part B: Xano AI prompts (B1–B5)"
project: tomale-rn-v1
status: active
date: 2026-11-12
related:
  - "[[m3-approvals-backend-prep-brief]]"
---

# M3 part B: Xano AI prompts

Paste one at a time. Send Claude the Xano AI's summary (or the code) before publishing. B0 (Resend template, web page, env vars) must be done before B3.

## B1: schema
```
Schema changes only. Don't change any endpoint or function.
1. Table "instant stories": add approved_by_profile_id (uuid, nullable, references user_profiles), approved_at (timestamp, nullable), approval_rejected_at (timestamp, nullable).
2. Table "user alerts": add audience (enum: "all", "parents", "profile"; default "all"), user_profiles_id (uuid, nullable, references user_profiles), instant_stories_id (int, nullable, references "instant stories").
```

## B2: alerts by audience
```
Change the alert function and the three alert endpoints in the app API group. Change nothing else.
1. Function notifications/create_user_alert: replace the dblink input with explicit inputs: enum type ("Content Moderation","System","Rewards"), text message, int users_id, text? action_url?, text? action_label?, enum? audience? ("all","parents","profile"; default "all"), uuid? user_profiles_id?, int? instant_stories_id?. Precondition: if audience == "profile", user_profiles_id must be set. Save all fields (is_read false).
2. GET /user_alerts, PATCH /user_alerts/{user_alerts_id}, PATCH /users/user_alerts/mark_all_read: a row is visible only when users_id == $auth.id AND (audience == "all" OR audience is null OR (audience == "parents" AND $auth.extras.active_profile.is_child === false) OR (audience == "profile" AND user_profiles_id == $auth.extras.active_profile.id)). Apply this in each where clause. The single PATCH returns 404 (notfound) for a row that isn't visible; mark_all_read only updates visible rows.
Strict comparisons; codes in payload.code.
```

## B3: moderation alert, email, completion alert
```
Two functions. Change only what's described.
1. ai pipeline/content_moderation_story_text, in the branch that sets status_moderation "Parental Approval": change the notifications/create_user_alert call to: type "Content Moderation", message "A story needs your review before your child can read it.", audience "parents", instant_stories_id = the story id, users_id = the story's users_id, action_url = $env.app_url_scheme ~ "://approvals", action_label "Review story". Do not put the moderation reason in the alert (it stays in blocked_reason).
   Then, inside a try_catch (an email failure must never stop moderation), get the story owner's users.email and run admin/resend_dynamic_send with to_email = that email, template_id = $env.resend_approval_template, variables = {approvals_url: $env.approvals_url}. In the catch, do nothing except log if a log function is already used in this function.
2. ai pipeline/story_completion_check: the "<title> is ready!" alert: skip it entirely when the story has parental_approval_required === true AND parent_approved !== true. Otherwise send it with audience "profile", user_profiles_id = the story's user_profiles_id, instant_stories_id = the story id, and action_url = $env.app_url_scheme ~ "://stories/" ~ the story id.
Use the table name "instant stories" (quoted, with the space) wherever the stories table is used.
```

## B4: approve and reject
```
Two new endpoints in the app API group, auth = users.
POST /instant_stories/{instant_stories_id}/approve and POST /instant_stories/{instant_stories_id}/reject. Input: int instant_stories_id.
Both, in order:
- Strict parent check: $auth.extras.active_profile.is_child === false, else 400 (inputerror) payload.code "PARENT_PROFILE_REQUIRED".
- Story: "instant stories" where id == input && users_id == $auth.id && is_deleted != true (single), else 404 (notfound) payload.code "STORY_NOT_FOUND".
- parental_approval_required === true, else 400 "NOT_AWAITING_APPROVAL".
- parent_approved !== true, else 400 "ALREADY_APPROVED".
- Mark read (is_read true, read_at now) every "user alerts" row with users_id == $auth.id && instant_stories_id == the story && type == "Content Moderation" (guard for none).
Approve: set parent_approved = true, approved_by_profile_id = $auth.extras.active_profile.id, approved_at = now, approval_rejected_at = null, last_modified_at = now. If the story's status == "Done", run notifications/create_user_alert with type "System", message (title or "Your story") ~ " is ready!", audience "profile", user_profiles_id = the story's user_profiles_id, instant_stories_id, users_id = $auth.id, action_url = $env.app_url_scheme ~ "://stories/" ~ id, action_label "Read now". Response {instant_stories_id, approval_state: "approved", approved_at}.
Reject: set approval_rejected_at = now, last_modified_at = now (parent_approved stays false). Response {instant_stories_id, approval_state: "rejected"}.
Also, in function ai pipeline/content_moderation_story_text, "blocked" branch only: add audience "parents" and instant_stories_id = the story id to the notifications/create_user_alert call (keep the message, including the reason). Change nothing else in that function.
Use the table name "instant stories" (quoted, with the space). Strict comparisons.
```

## B5: story reads
```
Edit GET /instant_stories and GET /instant_stories/{id} in the app API group. Change only the following.
Derived approval_state for each story: "none" when parental_approval_required !== true; "approved" when parent_approved === true; "rejected" when approval_rejected_at is set; otherwise "awaiting".
GET /instant_stories:
- Parent (is_child === false): same results as today, each with approval_state. Add input enum? approval_state? ("awaiting","rejected"); when given, return only stories in that state.
- Child: the existing results (each with approval_state), PLUS their own awaiting stories (user_profiles_id == active profile id, is_deleted != true, status_moderation == "Parental Approval", parent_approved !== true, approval_rejected_at empty), returned as redacted items containing only {id, title, approval_state: "awaiting", created_at}. Never include cover, pages, prompt, moderation or blocked_reason fields in those items. Rejected stories are not returned to a child.
- Update the comment that says the where clause must stay identical to stories/visible_story_ids: the child's awaiting cards are the one deliberate difference. Do not change that function.
GET /instant_stories/{id}: child behaviour unchanged (404 unless allowed today). For a parent, add approval_state, blocked_reason, approved_at and approval_rejected_at to the response.
Use the table name "instant stories" (quoted, with the space); no stack variable named $output; guard lists before reading fields.
```
