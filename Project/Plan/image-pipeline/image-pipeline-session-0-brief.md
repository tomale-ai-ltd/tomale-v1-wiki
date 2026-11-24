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

**Goal:** story, cover and character images keep working after OpenAI removes `gpt-image-1.5` on **1 December 2026**. Do this by **Friday 27/11**, which leaves Monday 30/11 spare. About half a day, all Kyle in Xano and Postman. No code changes.

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

## S0-2: change the records (about 15 minutes)

1. Set env `image_workers_enabled` = `false`. This stops the tick claiming jobs while you edit; queued jobs just wait.
2. For each page, cover and in-use character record, change only these fields:
   - `model_settings.image.model` → `gpt-image-2.6-flare`
   - leave `model_settings.pricing.image.per_image` at its current `0.08` until S0-3 measures it
   - `version` → next minor (for example `1.0` → `1.1`)
   - `last_modified_at` → now
   Leave `model_settings.url`, `image.url`, `size`, `n`, the text model and everything else as they are.
3. Set `image_workers_enabled` = `true`.

**Why edit in place rather than add new records:** characters are pinned to their record, so new records would need every character repointed. Rolling back to 1.5 is impossible after 1 December anyway. The separate fallback record comes with Session A ([[keep-openai-image-record-as-fallback-provider]]).

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
5. **If Flare looks clearly worse:** set the page record to `gpt-image-2.6-sunburst`, run one more story and compare.
6. **Correct the cost:** read the image output tokens per image on the OpenAI usage page. Set `per_image` to (output tokens × $30 ÷ 1M) plus input, rounded up, on all edited records.

**Pass:** every job completes, no terminal errors, no story over about 20 minutes, and pictures at least as good as on 1.5.

## Rollback

- **Before 1 December:** paste the saved `model_settings` back (model `gpt-image-1.5`).
- **After 1 December:** switch between Flare and Sunburst only.

The image kill switch stays available as always.

## Not in this session (but close)

The same deprecations page also lists:
- `gpt-4o-mini` for shutdown on **14 Jan 2027** (replacement `gpt-6-luna`). It's used by the prompt compiler, moderation, story text, chat and `generate_character_model`.
- `gpt-4o-mini-tts` and `tts-1` for shutdown on **6 Jan 2027** (replacement `gpt-realtime-2.1-mini`). It's used for read-aloud.

Both land before launch. They're planned as [[IP-03-replace-text-and-voice-models]] and should be done in Session A.

## Record

Raw session note: the old JSON, the record ids changed, the Postman results, run times, the corrected `per_image`, and which model each type ended on. Then apply [[PU-2026-11-24-05]] (stack, backend-xano and image-generation-flow wording).
