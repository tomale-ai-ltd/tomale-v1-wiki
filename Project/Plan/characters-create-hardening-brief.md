---
type: brief
title: characters-create-hardening-brief
project: tomale-rn-v1
status: draft
date: 2026-11-11
related:
  - "[[PRD-Characters]]"
  - "[[moderate-names-in-two-stages]]"
  - "[[moderate-free-text-instructions-with-moderation-text-policy]]"
  - "[[replace-dblink-inputs-with-explicit-allowlists]]"
  - "[[backend-xano]]"
---

# Harden `POST /characters` before speckit 008: Xano brief

Found 11/11 while writing the 008 micro-PRD, against the mirror at `c167fea`. Today `POST /characters`:
- takes a `dblink` input (against the explicit-inputs rule);
- **does no moderation**: neither the name ([[moderate-names-in-two-stages]], which the PRD requires on create) nor the free-text description, which then goes to the LLM and image model;
- accepts any `instant_stories_id` and links the new character to it **without checking the story belongs to the caller** (cross-account write);
- returns the raw record (internal fields);
- doesn't start the picture: the app must call `POST /characters/{id}/model` separately, which runs the LLM synchronously and then queues the image job. A failed or skipped second call leaves a character with no picture forever.

## Change set 1: explicit inputs and story check
- Inputs: `text name filters=trim` (required, 1–40 characters), `text physical_description filters=trim` (required, 1–500), `int? instant_stories_id?`.
- If `instant_stories_id` is given: the story must have `users_id == $auth.id`, not be deleted, and be `Draft`; otherwise 404 for not found / not yours, 400 `STORY_NOT_EDITABLE` if past Draft (same codes as `POST /instant_stories/{id}/characters`).

## Change set 2: moderation before anything is saved
- Name: `admin/check_for_profanity` as a signal only, then `ai pipeline/content_moderation_name` as the final decision. Refused → 400 `NAME_NOT_ALLOWED`, message "That name isn't allowed. Please try another." (the reason is logged, never shown).
- Description: `ai pipeline/content_moderation_text` with the `moderation-text` policy, as in `regenerate_image`. `enforcement: none` continues; `flag_account` writes `moderation_flags` and refuses; anything else refuses with 400 `CONTENT_REJECTED` and the policy's user-facing `blocked_reason`.
- Fail closed: if a moderation call errors, refuse with the generic message.

## Change set 3: start the picture from create
**Decided 11/11 (Kyle): option A.** after saving, run `ai pipeline/generate_character_model` in `util.post_process` (it already queues the image job), so one call creates the character and starts its picture. The app shows "Drawing [name]…" until `cover_image` appears. `POST /characters/{id}/model` stays for now (story chat may use it) but the app no longer calls it after create.
Rejected: option B (keep two calls; the app calls `/model` after create and retries on failure), because a closed app between the calls leaves a character with no picture.

## Change set 4: trimmed response
Return the same 10 fields as `GET /characters` plus `physical_description` and `stories_count` (0, or 1 when linked to a story).

## Change set 5: `picture_status` on list and detail (Kyle, 11/11)
Rather than a `draft` character status (considered and rejected: `status` means visibility, and half-made AI-chat characters live in `conversations`), add a derived `picture_status` to `GET /characters`, `GET /characters/{characters_id}` and the `POST /characters` response, from the character's **latest** `image_jobs` row (`job_type = "character-image"`, highest `created_at`):
- `drawing`: latest job is `queued`, `processing` or `error_retry`;
- `failed`: latest job is `error_terminal`;
- `ready`: no job in progress and `cover_image` is set (also when the latest job is `complete`);
- `drawing` also when there's no job yet and no `cover_image` (create has just queued it in the background).
On the list, fetch the latest jobs for all returned characters in one query (`characters_id in` the page's ids), not per row; guard empty lists. A Draw again after a failure moves it back to `drawing`. The app polls only while `drawing`, and shows "We couldn't draw [name]. Try again" (→ Draw again) when `failed`.
Add an index on `image_jobs.characters_id` if none exists.

## Planned for 012 (AI character chat), not now
`POST /characters` gains optional inputs for the structured attributes (from the `conversations` draft) and `conversations_id`. When attributes are supplied, the background step skips `generate_character_model` and only queues the image job; the conversation is marked complete with `characters_id` ([[PRD-Chatbot-Create-Character]] §5a). Additive: nothing in change sets 1–5 needs to change for it. No rename in V1 (Kyle, 11/11, reaffirming the PRD): a name is fixed once saved; "Change something" before saving covers it.

## Conventions and tests
Strict `=== false` parent checks where any appear; guard `$list.field` with a count check; no `enforce_hidden_fields = false` on new writes (the existing `db.add` lines keep it until the pre-launch sweep). Postman folder 5: 5A-1 still passes; add a blocked name (`NAME_NOT_ALLOWED`), a blocked description (`CONTENT_REJECTED`), user2's story id (404), a non-Draft story (`STORY_NOT_EDITABLE`, skips without `completedStoryId`), and `picture_status` = `drawing` straight after 5A-1 create, then `ready` or `drawing` on later reads (never missing).

## Xano AI prompt: change set 5 on the two GETs (12/11)
Found on 12/11 that change set 5 had only reached `POST /characters`; both GETs were missing `picture_status` (Postman 5H-1, 5I-1). Prompt used:

```
Add a derived field picture_status to two endpoints in the app API group: GET /characters and GET /characters/{characters_id}. Do not change anything else in either endpoint.

picture_status is one of "drawing", "ready", "failed", worked out per character from that character's LATEST image_jobs row (job_type == "character-image", highest created_at):
1. latest job status is "queued", "processing" or "error_retry"  -> "drawing"
2. otherwise, cover_image is not null                             -> "ready"
3. otherwise, latest job status is "error_terminal"               -> "failed"
4. otherwise (no job, or a finished job but no cover_image): "drawing" if the character's created_at is less than 15 minutes ago, else "failed"

GET /characters (list):
- After $characters is fetched, run ONE db.query on image_jobs for all returned characters (characters_id in $characters.id, job_type == "character-image", is_deleted not relevant), sorted by created_at desc, output ["characters_id","status","created_at"]. Only run it inside a conditional when ($characters|count) > 0; initialise $jobs to [] first. Do not query per character.
- In the existing foreach that builds $characters_with_count, find that character's latest job with ($jobs|filter:($$.characters_id == $character.id))|first (guard: it may be null), apply the rules above, and set "picture_status" on the character alongside "stories_count".

GET /characters/{characters_id} (detail):
- After the ownership/archived preconditions, query image_jobs for this character (job_type == "character-image"), sorted created_at desc, return a single row (or first of list, guarded for empty).
- Apply the rules above and add picture_status to $response_character after stories_count.

Use strict comparisons (=== / !==), guard every list before reading a field from it (an empty list makes $list.field a fatal error), and keep the existing outputs and response shapes otherwise identical.
```
