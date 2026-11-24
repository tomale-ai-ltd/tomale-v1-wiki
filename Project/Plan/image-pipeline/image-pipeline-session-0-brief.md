---
type: plan
title: "Image pipeline, Xano Session 0: move image models off gpt-image-1.5 before 1 December"
project: tomale-rn-v1
status: active
date: 2026-11-24
deadline: 2026-11-27
related:
  - "[[image-pipeline-plan]]"
  - "[[repoint-image-models-to-gpt-image-2-6-before-shutdown]]"
  - "[[image-generation-flow]]"
  - "[[image-pipeline-research-2026-11]]"
---

# Image pipeline, Xano Session 0: move off gpt-image-1.5

**Goal:** story, cover and character images keep working after OpenAI removes `gpt-image-1.5` on **1 December 2026**. Do this by **Friday 27/11**, which leaves Monday 30/11 spare. About half a day, all Kyle in Xano and Postman. No code changes: three new `data_models` records and a bulk repoint of characters.

## Why now (checked 24/11)

- OpenAI's deprecations page (developers.openai.com/api/docs/deprecations) lists `gpt-image-1.5` and `gpt-image-1.5-2025-12-16` for shutdown on **1 Dec 2026** (notice 2 June). The recommended replacement is `gpt-image-2.6-sunburst` or `gpt-image-2.6-flare`.
- **Skip `gpt-image-2`:** the same page lists it for shutdown on **10 Feb 2027** (notice 10 Nov 2026).
- The 2.6 models serve `/v1/images/generations` and `/v1/images/edits`. The Image API reference says GPT image models always return base64 (`data[0].b64_json`), and `response_format` is unsupported for them. `1024x1024` and `1536x1024` are still standard sizes.
- **Choice: `gpt-image-2.6-flare` for all three types.** Flare is the speed-oriented variant and Sunburst the detail-oriented, slower one, at the same token price ($30 per 1M image output tokens). Speed matters while Xano runs the jobs. Use Sunburst only if the smoke test shows Flare is clearly worse.

## What's live (mirror `5783a3f`, 23/11)

- **Page and cover executors** load the default active record for their type (`story-page-image`, `story-cover-image`) each time they run. Editing those two records changes every job from then on. They do not use `instant_stories.data_models_id`.
- **Character executor** loads the record saved on the character (`characters.data_models_id`, set by `POST /characters` from the default `character-image` record). **Existing characters keep whatever record they were created with**, so every `character-image` record that any character points to must be changed, not just the default.
- **Fields sent today:**
  - Page and cover call generations with `model`, `prompt`, `n` and `size` from the record, at `model_settings.image.url`.
  - Character without a reference calls generations at `model_settings.url` (a top-level key, unlike page and cover). Keep that key.
  - Character with a reference ("draw again", `use_reference`) calls the hard-coded `https://api.openai.com/v1/images/edits` with `image`, `prompt`, `n: 1` and `size: 1024x1024`.
  - The `dall-e` branch (adds `response_format`) doesn't fire for a GPT image model.
- **Not settable without a code change:** the new `complexity` field. When it's omitted the models plan at `high`, which can add latency. Check run times against `image_worker_lease_seconds` (below).
- **Cost logging** uses the fixed `model_settings.pricing.image.per_image`. It needs a new value.

## S0-1: prepare (nothing changes yet)

1. **Keep a rollback copy.** In Xano → Database → `data models`, filter `type` to `story-page-image`, `story-cover-image` and `character-image`. Copy each record's `id`, `slug`, `version`, `is_default`, `status` and full `model_settings` JSON into today's raw session note. Records are data, so the GitHub mirror won't record this change; the note is the history.
2. **Find the character records in use.** In `characters`, filter `data_models_id` to each `character-image` record id in turn. Write down every id that has rows. Those records all get changed in S0-2.
3. **Check model access.** In Postman, a scratch request (not in `_tests`):
   - `POST https://api.openai.com/v1/images/generations`
   - Header `Authorization: Bearer {{openai_api_key}}`. Put the key in the environment as a current value only. Never paste it into chat or notes.
   - Body `{"model": "gpt-image-2.6-flare", "prompt": "a small red ball on a white table", "size": "1024x1024", "quality": "low"}`
   - Expect 200 with `data[0].b64_json` and a `usage` object. A 403 means the organisation needs access or verification for this model: fix that in the OpenAI dashboard before going on.

## S0-2: add new versioned records (about 25 minutes)

Changed 24/11 (Kyle): add new records rather than editing in place, so the table keeps its history and rollback is a matter of flipping defaults. Every character points to record 1 (S0-1 found 0 rows on any other id), so the only extra step is one bulk repoint.

1. Set env `image_workers_enabled` = `false`. Each type must have exactly one active default, and the executors query for a single record, so make the swap while nothing runs.
2. **Add three records** in `data models`, copying the old record's `type`, `output_schema`, `prompt_template` and `model_settings`, with only these changes:

| From | New slug | name | version | `model_settings` change |
|---|---|---|---|---|
| 5 (page) | `tomale_story_page_image_v_1_1` | Tomale Page Image V1.1 | 1.1 | `image.model` → `gpt-image-2.6-flare` (the `text` model stays) |
| 9 (cover) | `tomale_story_cover_image_v_1_2` | Tomale Cover Image V1.2 | 1.2 | `image.model` → `gpt-image-2.6-flare` (the `text` model stays) |
| 1 (character) | `tomale_character_image_v_1_1` | Tomale Character Image V1.1 | 1.1 | `image.model` → `gpt-image-2.6-flare`; keep the top-level `url` |

   New records: `is_default` = true, `status` = active. Leave `pricing.image.per_image` at 0.08 until S0-3. Write down the three new ids.
3. **Retire the old records:** on 1, 5 and 9 set `is_default` = false and `status` = `deprecated`. `gpt-image-1.5` stops working on 1 Dec, so they can't serve as a fallback.
4. **Repoint the characters:** in `characters`, filter `data_models_id` = 1, select all rows and bulk-edit `data_models_id` to the new character record id. Afterwards, the same filter must return 0 rows. If Xano's table view won't bulk-edit, tell Claude and we'll use a one-off function instead.
5. **Check:** each of the three types has exactly one row with `is_default` true and `status` active.
6. Set `image_workers_enabled` = `true`.

The OpenAI fallback record for the new pipeline is added the same way in Session A ([[keep-openai-image-record-as-fallback-provider]]).

## S0-3: smoke test

1. **Story run:** Postman `_tests` folder 2 on its own (2A-1 story, 2A-2 character) with the test parent. Wait until the story is Done.
2. **Draw again:** folder 5D with env `runImageTests` = `true` (one paid edit with a reference).
3. **Two more stories by hand** in Postman or the app, so the set covers two themes, two art styles from tiers 0 and 1, and one story with at least two characters.
4. **Check each story:**
   - all 13 images present
   - `image_jobs` all `complete`, no `error_terminal`, and no job retried more than once
   - in `executor_runs`, `completed_at` − `started_at` per image well under `image_worker_lease_seconds`. If it isn't, raise the lease before go-live.
   - no stray text in the pictures
   - characters recognisable across pages
   - put one story next to a recent 1.5 story
5. **If Flare looks clearly worse:** add a page record with `gpt-image-2.6-sunburst` (next version), make it the default, run one more story and compare.
6. **Correct the cost:** read the image output tokens per image on the OpenAI usage page. Set `per_image` to (output tokens × $30 ÷ 1M) plus input, rounded up, on all edited records.

**Pass:** every job completes, no terminal errors, no story over about 20 minutes, and pictures at least as good as on 1.5.

## Rollback

- **Before 1 December:** set records 1, 5 and 9 back to default and active, set the new ones to `is_default` false, and repoint the characters to 1.
- **After 1 December:** add a Sunburst version the same way, if Flare disappoints.

The image kill switch stays available as always.

## Not in this session (but close)

The same deprecations page also lists:
- `gpt-4o-mini` for shutdown on **14 Jan 2027** (replacement `gpt-6-luna`). It's used by the prompt compiler, moderation, story text, chat and `generate_character_model`.
- `gpt-4o-mini-tts` and `tts-1` for shutdown on **6 Jan 2027** (replacement `gpt-realtime-2.1-mini`). It's used for read-aloud.

Both land before launch. They're planned as [[IP-03-replace-text-and-voice-models]] and should be done in Session A.

## Record

Raw session note: the old JSON, the record ids changed, the Postman results, run times, the corrected `per_image`, and which model each type ended on. Then apply [[PU-2026-11-24-05]] (stack, backend-xano and image-generation-flow wording).
