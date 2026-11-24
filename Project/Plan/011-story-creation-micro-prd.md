# 011-story-creation -- Make a story -- Guided chat, wait, ready #

<!--
Micro-PRD for speckit 011 (roadmap M4, Slice 200). Drafted by Claude 24/11; status: draft, for Kyle's review.
Cursor copies it to `.docs/prd/011-story-creation.md` before `/speckit.specify`. Starts after 010b merges (needs the email lock, the kit BackButton and the shared toast).
Sources: [[PRD-Chatbot-Story-Conversations]] (2.0), [[story-creation-flow]], [[formalise-story-status-lifecycle]], [[gate-image-generation-with-entitlements-at-story-creation]], [[add-phonics-focus-to-story-creation]], [[PRD-Subscription-Entitlement-System]] §6a, [[PRD-Parental-Oversight-Content-Approval]] §8a, [[share-characters-across-the-household]], the live OpenAPI export (24/11).
Kyle's 24/11 answers: guided chat (scripted steps with tap cards; AI only writes story ideas), a simple monthly story cap in Xano now (M8 swaps in plans), phonics in this slice, and a being-made card plus an in-app "ready" toast; a finished story opens a simple cover page until the reader (012). Whole of M4 in one slice.
Backend: [[011-xano-prompts]] (X1–X9, Postman folder 9). The app work can start once X1–X3 are published; X4–X7 before the phone pass.
Mock-ups: Design canvas "Tomale Make a story screens (011)" (https://claude.ai/artifact/8xGVeLeKT7UnjCJ8pZUJf6), boards 1101–1108, exported to `Project/Design/011-story-creation/` (with a README of states). Cursor copies that folder into `specs/011-story-creation/design/`; it can't open the canvas.
-->

## Goal

A parent or a child makes a story in a few taps: pick who's in it, what kind of story, how it looks and what happens, optionally a phonics focus, then "Make my story". They can leave while it's made, see it being made from Home and Create, get a "Your story is ready" toast, and open the finished story's cover. Unfinished stories wait in a Story builder so nothing is lost, including when the monthly limit is reached.

## Screen flow

- **Entry points** (all behind 010b's email lock, unchanged): Create tab "Make a story", Home "New story" / "Make a story", character detail "Create a story with [name]" and the character panel's "Make a story" (that character is already chosen), and a Story builder card (resumes that draft).
- **Create tab (1101):** the two tiles stay; below them **"Being made"** (stories in Preparing or In Queue, each with progress) and **"Story builder"** (the active profile's drafts: title or "Untitled story", up to three character pictures, theme name, "Edited 2 days ago"; tap resumes; the "…" menu has "Delete draft" with a confirmation). Each section is hidden when empty.
- **Story chat (1102):** one screen, compact header with the kit BackButton and "New story" (or the draft's title). Tomale's book mark speaks in bubbles; the person answers by tapping cards, which then show as their reply bubble. Steps, in order:
  1. **Who's in your story?** Household characters as picture cards (multi-select, 1 to 3), plus a "Make a new character" card that opens the 008 form and comes back with the new character chosen. "These ones" confirms.
  2. **What kind of story?** Theme cards (name and one line), single choice.
  3. **How should it look?** Art-style cards with the sample picture, single choice.
  4. **What happens in your story?** A text box ("A dragon who's scared of the dark…", up to 300 characters) and a "Give me ideas" chip: three short idea cards from the AI (title and one line, built from the chosen characters and theme). Tapping one fills the box; the person can edit it. "Give me ideas" can be tapped again ("More ideas").
  5. **Practise some sounds?** "Not this time" or "Yes, let's practise". Yes → scheme cards → stage cards with plain labels (e.g. "Phase 2: first sounds"). Skipping is the default.
  6. **Here's your story:** a summary card (characters, theme, style, idea, sounds) with "Change" on each row (jumps back to that step, then returns here), the allowance line for a parent ("3 of 4 stories left this month"; hidden for a child), and **"Make my story"**.
- **Being made (1103):** straight after "Make my story": the book mark with a gentle animation (Reduce Motion: still), "We're making your story", a progress line ("Writing the words…", then "Drawing the pictures: 5 of 13"), and "You can leave. We'll tell you when it's ready." with "Back to Home". Closing or leaving doesn't stop anything.
- **Being-made card (1104)** on Home (parent and child) and in Create: cover placeholder, "Being made", the same progress line; tap opens 1103 for that story.
- **Ready (1105):** while the app is open, a "Your story is ready" toast (with the title) above the tab bar, with "Open". The story appears in Home's list as normal. A child's story held for a grown-up becomes 010's waiting card instead, and the child's toast says "Your story is made! A grown-up will look at it soon." (no "Open").
- **Story cover (1106):** cover picture, title, subtitle, characters, the phonics focus if any ("Practising: Phase 3, week 2"), and a disabled "Read" with "Reading comes soon" (012 replaces this screen's button with the reader).
- **Limit reached (1107):** a sheet on "Make my story" when the cap is hit; the story stays in the Story builder. Child: "You've made lots of stories this month! New ones unlock on [1 December]." with "Ask a grown-up" (opens the profile picker with the parent highlighted, then the PIN, then parent Home; no prices) and "OK". Parent: "You've used this month's [4] stories. More unlock on [1 December]." with OK (plans and upgrades come with M8).
- **Couldn't make it (1108):** a moderation block or a failed generation. Blocked (child and parent): "We can't make this story. Let's try a different idea." with "Try a different idea" (opens a new chat with the same characters, theme and style chosen, the idea box empty). Failed (story rolled back to Draft): "Something went wrong making your story." with "Try again" (back to the summary) and "Later" (it stays in the Story builder). Never say why a story was blocked to a child.

## Scope (this slice only)

- **Draft lifecycle:** the draft is created on the first confirmed step (characters), not on opening the chat, so an abandoned empty chat leaves nothing behind: `POST /instant_stories {}` then `POST /instant_stories/{id}/characters {characters_ids}`. Each later step saves at once with `PATCH /instant_stories/{id}` (`theme_id`, `artwork_style_id`, `user_prompt`, `phonics_phase_stage_id`). Back, closing the app or a dropped connection lose nothing already confirmed. Resuming rebuilds the chat from the draft's fields (no transcript is stored; the steps are scripted) and opens at the first unanswered step, or the summary if all are done.
- **Catalogues:** `GET /themes?status=active` (check the live value), `GET /artwork_style`, `GET /characters` (household, not archived), `GET /phonics/phonics_schemes` and `…/{id}/stages`. Loaded when the chat opens; a failed load shows the step's "Try again" bubble. Locked art styles (plans) are M8: every live style is selectable in 011.
- **Ideas:** `POST /instant_stories/{id}/ideas` → `{ideas: [{title, idea}]}` (three). Waiting state on the chip; `RATE_LIMITED` → "That's lots of ideas! Try writing your own, or ask again in a minute."; any other failure → "Ideas aren't working right now. You can write your own."
- **Make my story:** `GET /story_allowance` when the summary opens (`{used, limit, resets_at}`; parent line only). "Make my story" → `POST /instant_stories/{id}/page_text`. Navigate to 1103 at once and don't wait for the response (text generation can take a minute); the screen follows `GET /instant_stories/{id}`. The button can't be tapped twice.
- **Refusals by `payload.code`:** `ENTITLEMENT_LIMIT_REACHED` (with `payload.resets_at`) → 1107; `EMAIL_NOT_VERIFIED` → 010b's confirm sheet (the in-app lock normally prevents this); `STORY_NOT_EDITABLE` → reload the story and open 1103 or the cover for its real status; `STORY_NOT_FOUND` → back to Create with "That story isn't here any more"; `INVALID_CHARACTERS` → reload characters and ask step 1 again; `INVALID_INPUT` → reload the catalogues and ask that step again.
- **Following progress:** poll `GET /instant_stories/{id}` every 10 s while 1103 is open, and the in-progress list (`GET /instant_stories?in_progress=true`) every 30 s while Home or Create is focused and the list isn't empty; stop in the background; check once on return to the foreground. Progress text: Preparing → "Writing the words…"; In Queue → "Drawing the pictures: (total − images_remaining) of total". Done → the ready toast once per story per device session (a set of story ids in memory), then the story leaves the in-progress list. Blocked → 1108. Draft again after "Make my story" → the failed state of 1108.
- **Toast:** reuse the shared confirmation toast host (010b). "Open" goes to 1106 (or, for a child's held story, there is no "Open").
- **Story cover (1106):** `GET /instant_stories/{id}`; the e-reader is 012.
- **Story builder:** `GET /instant_stories?status=Draft` (the active profile's own drafts, newest first); delete with `DELETE /instant_stories/{id}`.
- **Phonics:** stored as `phonics_phase_stage_id`; the summary and cover show the stage's plain label.
- **Child and parent:** the same flow and copy, written so a 5-year-old can follow it with help. No prices, plans or purchase prompts for a child anywhere (CAP Code; [[pre-launch-checklist]] §6).
- **Copy** follows the design-system README and British English; "story", never "book" (books are the printed product in the Store).

## Design notes (for the mock-ups)

- Chat: the book mark avatar on Tomale's bubbles (cream bubble, `ink` text); the person's replies on the right in `teal` with white text; cards in a horizontal scroller (characters, styles) or a wrapped grid (themes, phonics), 48-point targets, a tick on a chosen card. Typing dots (S-032's three pulsing dots) while ideas load. The input box appears only at step 4.
- Being made: no percentage bar (text generation has no progress). While pictures are drawn, a row of 13 dots fills in with the count ("5 of 13"); while the words are written, just the line.
- Sheets keep the 40% `ink` scrim, no blur. Toasts above the tab bar, as in 010.
- Header bands, BackButton and `ScreenHeader` as in 009/010b.

## Out of scope

- The e-reader and the Bookshelf tab (012); the alerts inbox (M7) and push notifications (post-V1); plans, upgrades and locked art styles (M8); AI-led free chat and storing a chat transcript (guided steps only, Kyle 24/11); naming the story yourself (the generation writes the title); editing a story after "Make my story"; regenerating pictures (V2); 16- and 20-page stories; draft clean-up (a backend job, see the Xano prompts).

## State Management

`store/storyDraftStore.ts` (Zustand, memory only): the open draft's fields, the current step, catalogue caches for the session, and the ideas returned. `store/storyProgressStore.ts` (memory only): in-progress stories `{id, status, total_pages, images_remaining}`, the polling timers and the set of ids already toasted. Nothing persisted: the server is the record (Story builder and the in-progress list are refetched on focus). Both stores are cleared with the other household caches on sign-out, Start again and a new sign-in (010b bug fix `ca572a0`).

## Data the app needs (from [[011-xano-prompts]])

- `PATCH /instant_stories/{id}` (Draft only), `POST /instant_stories/{id}/characters` (Draft only, 1–3 household characters, replaces the set), `POST /instant_stories/{id}/ideas`, `GET /story_allowance`, `GET /instant_stories?status=Draft` scoped to the active profile, `GET /instant_stories?in_progress=true` with `total_pages` and `images_remaining`, `phonics_phase_stage_id` on the story (create, patch, get), the email gate and the monthly cap on `page_text`.
- New codes for the constitution's live list (a `/speckit.constitution` PATCH before plan): `STORY_NOT_EDITABLE`, `INVALID_CHARACTERS`, `INVALID_INPUT`, `ENTITLEMENT_LIMIT_REACHED` (moves from planned to live). `STORY_NOT_FOUND`, `EMAIL_NOT_VERIFIED` and `RATE_LIMITED` are already live.
