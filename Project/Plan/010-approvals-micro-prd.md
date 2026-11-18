# 010-approvals -- Approvals -- Review, approve, reject, wait #

<!--
Micro-PRD for speckit 010 (roadmap M3, second of two specs: [[split-m3-into-specs-009-and-010]]). Drafted by Claude 18/11. DRAFT: Kyle reviews before Cursor copies it.
Cursor copies it to `.docs/prd/010-approvals.md` before `/speckit.specify`. Starts after 009 merges (needs the avatar menu, the picker, the PIN pad and the typed refusal body).
Sources: [[PRD-Parental-Oversight-Content-Approval]] §6–§8a, [[hide-rejected-stories-from-child]], [[surface-approvals-on-parent-home-and-avatar-menu]], [[block-ordering-of-stories-awaiting-parental-approval]],
[[m3-approvals-backend-prep-brief]] (backend built 13/11, Postman folder 7), PRD-Home-Dashboard (PU-2026-11-18-01).
Kyle's 18/11 answers: review is a simple scrolling view (no e-reader yet); the child's waiting card shows in Home's story list; badges count stories awaiting review.
Needs backend change B6 first (story list returns `user_profiles_id`): [[m3-approvals-xano-prompts]].
Mock-ups: to come (Design canvas), including a minimal Home for parent and child.
-->

## Goal

When a story needs a grown-up's OK, the parent sees it, reads it and decides; the child sees a friendly "waiting" card and never the story itself until it's approved. A rejected story disappears for the child; the parent can delete it or keep it on their own profile.

## Screen flow

- Parent Home (minimal, from the 05/11 Home boards): greeting header (009 `ScreenHeader`), "Stories to review (N)" card when N > 0 → inbox; the existing story list below.
- Avatar menu (009): adds "Approvals" with the count badge (parent only) → inbox.
- Approvals inbox (parent): two segments, "To review" (awaiting) and "Not approved" (rejected). Each row: cover (or placeholder), title, whose story ("Mia's story", from the profile list), when it was made, and "Still being made" if the story isn't Done.
- Review screen (parent): a highlighted note with why it needs a look (`blocked_reason`), then the cover and every page (picture and text) in one scrolling view, then "Approve" (primary) and "Not this one" (secondary). Approve can be tapped before the story has finished making (the child is told when it's ready).
- Reject confirmation sheet: what happens ("Mia won't see this story. You can delete it or keep it on your profile.").
- Rejected story actions (parent, from "Not approved"): "Keep it on my profile" (assign to the primary profile), "Delete story" (with confirmation), or "Approve after all".
- Child Home story list: an awaiting story appears as a locked card ("Waiting for a grown-up to say yes", title only, no cover); tapping it shows that message, nothing opens. Approved stories appear as normal; rejected ones never appear.
- Email link and alerts: `tomalerntest://approvals` (dev) / `tomale://approvals` opens the inbox through the gates in [[PRD-Parental-Oversight-Content-Approval]] §8a.

## Scope (this slice only)

- Count: `GET /instant_stories?approval_state=awaiting` → N, refreshed when parent Home or the avatar menu comes into focus and after any approve or reject. Badge hidden at 0. Never shown on a child profile.
- Inbox lists: `GET /instant_stories?approval_state=awaiting` and `?approval_state=rejected`; child name from `user_profiles_id` matched against `GET /users/user_profiles` (fallback "A story").
- Review: `GET /instant_stories/{id}` (parent fields `approval_state`, `blocked_reason`, `approved_at`, `approval_rejected_at`; pages and cover). Pages in `page_number` order; a page without a picture yet shows a placeholder.
- Approve: `POST /instant_stories/{id}/approve` → back to the inbox with a toast "Approved. Mia can read it now" (or "…once it's ready" if not Done). Reject: confirmation, then `POST /instant_stories/{id}/reject` → toast "Mia won't see this story".
- Rejected actions: assign `POST /instant_stories/{id}/assign {user_profiles_id: primary}` (009 backend), delete `DELETE /instant_stories/{id}`, approve again via the approve endpoint.
- Refusals by `payload.code` (009's typed body): `ALREADY_APPROVED` and `NOT_AWAITING_APPROVAL` refresh the inbox with "This story has already been sorted"; `STORY_NOT_FOUND` removes the row; `PARENT_PROFILE_REQUIRED` should not happen (route is parent-only) and signs into the picker.
- Child waiting card in Home's story list (the child list already returns `{id, title, approval_state: "awaiting", created_at}`).
- Pending route (§8a): an approvals link remembered in memory and resumed after login, picker (parent highlighted) and PIN; cleared once used or when the person goes elsewhere. The same check guards any parent-only route.
- Minimal parent and child Home per the new mock-ups (header, review card, story list). Badges, announcements, favourite characters and the rest of the dashboard stay for the dashboard slice.
- Copy follows the design-system README; never tell a child why a story was held.

## Out of scope

- The full Home dashboard; the in-app alerts inbox (M7); push notifications; the e-reader (012, which can later open from the review screen); editing a story before approval; ordering (Store, 013; the backend gate already blocks awaiting stories).

## State Management

`store/approvalsStore.ts` (Zustand, memory only): `awaiting[]`, `rejected[]`, `count`, loading and error. Refetched on focus; nothing persisted (the server decides). Pending route lives in memory in the navigation layer.

## Endpoints

GET /instant_stories?approval_state=awaiting|rejected (parent) → Story[] with `approval_state` and (after B6) `user_profiles_id`.

GET /instant_stories (child) → visible stories plus awaiting cards `{id, title, approval_state: "awaiting", created_at}`.

GET /instant_stories/{id} (parent) → story with pages, `approval_state`, `blocked_reason`, `approved_at`, `approval_rejected_at`. Child: 404 until approved.

POST /instant_stories/{id}/approve → 200 `{instant_stories_id, approval_state: "approved", approved_at}`. 400 `PARENT_PROFILE_REQUIRED` | `NOT_AWAITING_APPROVAL` | `ALREADY_APPROVED`; 404 `STORY_NOT_FOUND`.

POST /instant_stories/{id}/reject → 200 `{instant_stories_id, approval_state: "rejected"}`. Same refusals.

POST /instant_stories/{id}/assign {user_profiles_id} → 200 `{instant_stories_id, user_profiles_id}`. DELETE /instant_stories/{id} → 200.

GET /users/user_profiles → names for "Mia's story".

## Acceptance (Given/When/Then)

Happy path
- Given a child's story held for review
- When the parent opens "Stories to review", reads it and taps Approve
- Then the count drops, the child's waiting card becomes the story, and the child gets "… is ready!" when it's done

Edge
- Given the parent opens the approval email on a phone where a child is using the app
- When the link opens
- Then the picker shows with the parent highlighted, the PIN is asked, and the inbox opens

Error
- Given the parent rejects a story
- When the child next looks at Home
- Then the waiting card is gone; the parent finds it under "Not approved" with Keep, Delete and Approve after all

Device checks (Kyle, phone): trigger a held story (Run & Debug or a sensitive prompt); child sees the waiting card; email link from the child profile → picker → PIN → inbox; review, approve before and after Done; reject, then keep on my profile, delete, and approve after all; badge counts on Home and the avatar menu; light and dark.
