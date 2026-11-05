---
type: brief
title: characters-backend-prep-brief
project: tomale-rn-v1
status: done
date: 2026-11-05
related:
  - "[[PRD-Characters]]"
  - "[[backend-xano]]"
  - "[[security-model]]"
  - "[[operating-model]]"
---

# Characters backend prep (before speckit 008): Xano brief

Implements [[PRD-Characters]] §4 "Backend prep". Process: [[operating-model]] §3.2. One change set at a time, in order: Xano AI drafts → Claude reviews the draft against the mirror (`Repos/tomale-xano`, `git pull` first) → Kyle publishes on the live branch (no dev/prod split yet) → Postman. Read [[backend-xano]] before drafting.

Checked against the mirror on 05/11 (sync of 30/10). Conventions that apply everywhere:
- Ownership: `characters.users_id == $auth.id` and `is_deleted != true`; anything else is `notfound` "Not Found." (no information leak).
- Parent check: `$auth.extras.active_profile.is_child == false`. If `active_profile` is missing, fail closed ([[fail-closed-active-profile-resolution]]).
- Error codes: HTTP 400 with a payload `code` (Xano has no 422), per the constitution: `PARENT_PROFILE_REQUIRED`, plus the new ones named below.
- Explicit input allowlists, no `dblink` inputs ([[replace-dblink-inputs-with-explicit-allowlists]]); hidden fields stay enforced unless a line says otherwise.
- Every change gets Postman `_tests` (step 6).

## 1. Table `characters`: add `is_favourite`

- Add `bool is_favourite?` default `false`. No backfill needed (null reads as false; the app treats null as false).
- Do not change any other column. `status` (active | archived), `is_deleted`, `deleted_at` stay as built.

## 2. Parent-only delete: `DELETE /characters/{characters_id}`

Today: owner check, then soft delete (`status: archived`, `is_deleted: true`, `deleted_at: now`).
- Add, as the first step: if the active profile is a child → 400, `code: PARENT_PROFILE_REQUIRED`, `message: "Ask a grown-up to do this."`.
- Keep the rest exactly as is (owner check, soft delete, response).
- Note: `DELETE /users/user_profiles/{id}` uses 403 `PROFILE_NOT_PARENT` for the same rule. Leave it for now; flagged to align later.

## 3. New `PATCH /characters/{characters_id}/flags`

Archive/unarchive and favourite. Inputs (explicit, both optional, at least one required): `enum status? values ["active","archived"]`, `bool is_favourite?`.
- Owner check as above (not deleted).
- If `status` is present: parent-only (child → 400 `PARENT_PROFILE_REQUIRED`).
- `is_favourite`: any profile on the account may change it (household-wide).
- Neither present → 400 `code: NOTHING_TO_UPDATE`.
- `db.edit` only `status`, `is_favourite`, `last_modified_at: now`. No other field can change through this endpoint.
- Response: the character in the same shape as `GET /characters/{id}` (no hidden attribute fields).

## 4. `GET /characters`: explicit inputs, archived filter, favourites first

Replace the `dblink` input with explicit inputs: `text name?`, `int instant_stories_id?`, `enum status?` values `["active","archived"]` default `active`.
- Where: owner, `is_deleted != true`, `status == $input.status`, plus the existing optional `name` and `instant_stories_id` filters.
- A child profile requesting `status = archived` gets the active list instead (children never see archived characters).
- Sort: `is_favourite` desc, then `created_at` desc.
- Output: add `is_favourite` to the fields returned; keep the rest of the current output unchanged.

## 5. New `POST /instant_stories/{instant_stories_id}/characters`

Links existing characters to a story (used by story chat and "Create a story with this character"). Inputs: `int instant_stories_id`, `int[] characters_ids` (1–6 items).
- Story: owner (`users_id == $auth.id`), not deleted, and `status == "Draft"`; otherwise `notfound`, or 400 `code: STORY_NOT_EDITABLE` for a story that exists but is past Draft.
- Each character: owner, not deleted, `status == "active"`. Any that fail → `notfound` for the whole request (nothing written).
- For each id not already linked, `db.add instant_story_characters` (`instant_stories_id`, `characters_id`). Already-linked ids are skipped, not errors (idempotent).
- Never edit `characters.instant_stories_id`.
- Response: `{ instant_stories_id, characters_ids: [all linked ids after the call] }`.

## 6. New `POST /characters/{characters_id}/regenerate_image` (image-to-image)

Inputs: `int characters_id`, `text instruction? filters=trim` (max 200 characters).
- Owner check (not deleted, `status == "active"`).
- `instruction` present → run `ai pipeline/content_moderation_name` (or the text moderation used on create) on it; a failure → 400 `code: CONTENT_REJECTED` with the generic moderation message.
- If an `image_jobs` row for this character is `queued` or in progress → 400 `code: IMAGE_JOB_IN_PROGRESS`.
- Entitlement gate: call the single "can create image" check if it exists by then; until it does, leave a clearly marked `// ENTITLEMENT GATE` step that allows the request (the simple cap lands with M4/M8, [[roadmap]] §3). Do not invent a limit here.
- Queue a job like `generate_character_model` does (`job_type: character-image`, `status: queued`, same priority/attempt fields) plus two new `image_jobs` columns: `text instruction?` and `bool use_reference?` (true here).
- `ai pipeline/executor_character_image`: when `use_reference` is true and the character has a `cover_image`, call the OpenAI image **edit** endpoint with the current `cover_image` as the input image and the existing prompt template plus `instruction` appended; otherwise keep today's generation call unchanged. On success it already writes `characters.cover_image`; keep that. Keep the existing retry and error handling.
- Response: `{ characters_id, image_jobs_id, status: "queued" }`. The app polls `GET /characters/{id}` (or waits for the alert) as it does after create.

## 7. Postman `_tests`

Add a Characters folder (or extend the existing one) per [[test-suite]]:
- parent: archive → unarchive → favourite → list shows it first; delete works.
- child profile (after `select_profile` to a child): delete and archive → 400 `PARENT_PROFILE_REQUIRED`; favourite works; `GET /characters?status=archived` returns active only.
- other user's character: flags, delete, regenerate, link → `notfound`.
- link: Draft story + own active characters → linked; repeat call idempotent; past-Draft story → `STORY_NOT_EDITABLE`.
- regenerate: queues a job; second call while queued → `IMAGE_JOB_IN_PROGRESS`.
- Run the full `_tests` suite after publishing (auth and ownership changed).

## Must not change

Auth endpoints, `POST /characters` (create + moderation), the image worker tick's scheduling, story generation (`generate_story_page_text` still reads `instant_story_characters`), `characters.instant_stories_id`, response shapes of existing endpoints except the added `is_favourite` field.

## After publishing

`pnpm update:openapi` and `pnpm update:datamodel` in Cursor (class C repo-sync), then speckit 008 can start.
