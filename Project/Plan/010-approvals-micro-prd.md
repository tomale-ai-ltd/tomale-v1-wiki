# 010-approvals -- Approvals -- Review, approve, reject, wait #

<!--
Micro-PRD for speckit 010 (roadmap M3, second of two specs: [[split-m3-into-specs-009-and-010]]). Drafted by Claude 18/11; approved by Kyle 18/11.
Cursor copies it to `.docs/prd/010-approvals.md` before `/speckit.specify`. Starts after 009 merges (needs the avatar menu, the picker, the PIN pad and the typed refusal body).
Sources: [[PRD-Parental-Oversight-Content-Approval]] §6–§8a, [[hide-rejected-stories-from-child]], [[surface-approvals-on-parent-home-and-avatar-menu]], [[block-ordering-of-stories-awaiting-parental-approval]],
[[m3-approvals-backend-prep-brief]] (backend built 13/11, Postman folder 7), PRD-Home-Dashboard (PU-2026-11-18-01).
Kyle's 18/11 answers: the word is "Rejected" everywhere (tab, button "Reject"; "Blocked" is the internal status for a failed story); review is a text-first screen, not a reader (no page pictures; the concern is the request, the text and the reason); the child's waiting card shows in Home's story list; badges count stories awaiting review.
Backend change B6 (story list returns `user_profiles_id`) is live since 18/11 (mirror `03a8b55`); 010 runs `pnpm update:openapi` so the client has the field.
Mock-ups: "Tomale Approvals screens (010)" Design canvas (https://claude.ai/artifact/34aqKVgMpEAAJtfzKQiAUa), boards 1001–1007; exported 18/11 to `Project/Design/010-approvals/` (with README of states). Cursor copies that folder into `specs/010-approvals/design/`; it can't open the canvas.
-->

## Goal

When a story needs a grown-up's OK, the parent sees it, reads it and decides; the child sees a friendly "waiting" card and never the story itself until it's approved. A rejected story disappears for the child; the parent can later approve it for the child, approve it and keep it for themselves, or delete it. A rejected story never sits in limbo on a profile.

## Screen flow

- Parent Home (minimal, from the 05/11 Home boards): greeting header (009 `ScreenHeader`), "Stories to review (N)" card when N > 0 → inbox; the existing story list below.
- Avatar menu (009): adds "Approvals" with the count badge (parent only) → inbox.
- Approvals inbox (parent): two segments, "To review" (awaiting) and "Rejected" (rejected). Each row: cover (or placeholder), title, whose story ("Mia's story", from the profile list), when it was made, and "Still being made" if the story isn't Done.
- Review screen (parent), text first, no page pictures (Kyle, 18/11): (1) why it needs a look (`blocked_reason`), highlighted; (2) what the child asked for (`user_prompt`); (3) the characters in the story, each with its picture and name, tappable to the character's detail (008) where the parent can archive it so it can't be used again; (4) the story text as a one-page-at-a-time carousel (swipe, plus previous and next buttons, "Page N of M" and dots; Kyle, 18/11); then "Approve" (primary) and "Reject" (secondary). Approve can be tapped before the story has finished making (the child is told when it's ready).
- Reject confirmation sheet: what happens ("Mia won't see this story. You can delete it or keep it on your profile.").
- Rejected story actions (parent, from "Rejected"): "Approve for [child]", "Approve and keep it for me" (the story moves to the parent and is approved, so it's readable and orderable and the child never sees it), or "Delete story" (with confirmation). Rejected stories appear only in the Rejected tab, never in Home's recent stories or any other parent list (filter on `approval_state`).
- Child Home story list: an awaiting story appears as a locked card ("Waiting for a grown-up", title only, no cover); tapping it shows that message, nothing opens. Approved stories appear as normal; rejected ones never appear.
- Email link and alerts: `tomalerntest://approvals` (dev) / `tomale://approvals` opens the inbox through the gates in [[PRD-Parental-Oversight-Content-Approval]] §8a.

## Scope (this slice only)

- Count: `GET /instant_stories?approval_state=awaiting` → N, refreshed when parent Home or the avatar menu comes into focus and after any approve or reject. Badge hidden at 0. Never shown on a child profile.
- Inbox lists: `GET /instant_stories?approval_state=awaiting` and `?approval_state=rejected`; child name from `user_profiles_id` matched against `GET /users/user_profiles` (fallback "A story").
- Review: `GET /instant_stories/{id}` (parent fields `approval_state`, `blocked_reason`, `approved_at`, `approval_rejected_at`; `user_prompt`; `characters[]` `{id, name, physical_description, cover_image}`; `pages[]`). Page text in `page_number` order; page pictures are not shown. A character without a picture yet shows the drawing placeholder. Tapping a character opens its 008 detail (parent: archive is there).
- Approve: `POST /instant_stories/{id}/approve` → back to the inbox with a toast "Approved. Mia can read it now" (or "…once it's ready" if not Done). Reject: confirmation, then `POST /instant_stories/{id}/reject` → toast "Mia won't see this story".
- Rejected actions: approve for the child via the approve endpoint; "Approve and keep it for me" is two calls in this order: `POST /instant_stories/{id}/assign {user_profiles_id: primary}`, then `POST /instant_stories/{id}/approve` (assign first, so the "is ready!" alert goes to the parent's profile, not the child's; if the approve fails after the assign, the story is on the parent and still rejected, and the screen offers Approve again); delete via `DELETE /instant_stories/{id}`.
- Refusals by `payload.code` (009's typed body): `ALREADY_APPROVED` and `NOT_AWAITING_APPROVAL` refresh the inbox with "This story has already been approved"; `STORY_NOT_FOUND` removes the row; `PARENT_PROFILE_REQUIRED` should not happen (route is parent-only) and signs into the picker.
- Child waiting card in Home's story list (the child list already returns `{id, title, approval_state: "awaiting", created_at}`).
- Pending route (§8a): an approvals link remembered in memory and resumed after login, picker (parent highlighted) and PIN; cleared once used or when the person goes elsewhere. The same check guards any parent-only route.
- Minimal parent and child Home per the new mock-ups (header, review card, story list). Badges, announcements, favourite characters and the rest of the dashboard stay for the dashboard slice.
- Copy follows the design-system README; never tell a child why a story was held.

## Design notes (mock-ups, 18/11)

- Parent Home: the header avatar carries the review count as a small badge; the "Stories to review (N)" card is just that line and an arrow, with no names (Kyle, 18/11); the inbox rows say whose story it is.
- Sheets (avatar menu, PIN pad, confirmations, waiting sheet): the real screen stays visible behind, under a 40% `ink` scrim; no blur (Android performance). The grey blocks behind sheets on the boards are stand-ins only.
- Home quick actions and favourites (Kyle, 18/11): both Homes show two quick-action tiles (parent "New story" / "New character"; child "Make a story" / "Make a character", child-sized) and a favourites row drawn as placeholders. "New character" opens the 008 form; "New story" is disabled with "Coming soon" until 011. Favourite stories stays an empty placeholder: stories have no favourite flag yet (backend field needed in the dashboard slice).
- Timing (checked in the mirror 18/11): moderation runs at the start of `generate_story_page_text`, and a held story carries on to write its text, so the alert and email go out a minute or so before the text exists. Normally the parent sees the text with pictures still being made ("Still being made" in the inbox); "Still being written" on the review screen is the rare early case.
- Review screen: if the story text isn't written yet, the story section says "Still being written" and the parent can still decide from the request and characters; Approve and Reject sit in a bar fixed to the bottom.
- Toasts: "Approved. Mia can read it now." / "Approved. Mia can read it once it's ready." / "Rejected. Mia won't see this story."
- Inbox empty states: "All caught up" (To review) and "Nothing rejected" (Rejected).
- Child waiting card: dashed outline, lock, title and "Waiting for a grown-up"; tapping opens a sheet "A grown-up will look at this story soon. You'll be able to read it once they say yes." with OK.
- Rejected actions sheet: Approve and keep it for me, Approve for [child], Delete story (then a confirmation: "This can't be undone"). Reject sheet: "…where you can approve it for Mia, keep it for yourself, or delete it."

## Out of scope

- The full Home dashboard; the in-app alerts inbox (M7); push notifications; the e-reader (012, which can later open from the review screen); editing a story before approval; ordering (Store, 013; the backend gate already blocks awaiting stories).

## State Management

`store/approvalsStore.ts` (Zustand, memory only): `awaiting[]`, `rejected[]`, `count`, loading and error. Refetched on focus; nothing persisted (the server decides). Child names come from 009's `profilesStore` (`GET /users/user_profiles`, already loaded for the menu and picker; fetched once if empty), matched on `user_profiles_id`. No profile addon on the story list (Kyle and Claude, 18/11). Pending route lives in memory in the navigation layer.

## Endpoints

GET /instant_stories?approval_state=awaiting|rejected (parent) → Story[] with `approval_state` and (after B6) `user_profiles_id`.

GET /instant_stories (child) → visible stories plus awaiting cards `{id, title, approval_state: "awaiting", created_at}`.

GET /instant_stories/{id} (parent) → story with `user_prompt`, `characters[]`, `pages[]` (text used), `approval_state`, `blocked_reason`, `approved_at`, `approval_rejected_at`. Child: 404 until approved.

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
- Then the waiting card is gone; the parent finds it under "Rejected" with Approve for Mia, Approve and keep it for me, and Delete story

Device checks (Kyle, phone): trigger a held story (Run & Debug or a sensitive prompt); child sees the waiting card; email link from the child profile → picker → PIN → inbox; review (reason, request, characters, text; no page pictures), open a character and archive it, approve before and after Done; reject, then keep on my profile, delete, and approve after all; badge counts on Home and the avatar menu; light and dark.
