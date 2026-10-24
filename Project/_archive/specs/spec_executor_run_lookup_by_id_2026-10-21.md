# Executor run lookup by id (PDF and image pipelines)

## Goal
Async executor functions must find their own `executor_runs` row by its `id`, not by matching a timestamp. Today each worker tick starts the executor first and inserts the `executor_runs` row afterwards, and the executor looks the row up by job id plus `created_at`. This has two problems:
- **Timing gap.** If the executor starts before the row is inserted, its lookup finds nothing.
- **Overwrite.** The executors take an input named `created_at` (or `run_created_at` in the PDF functions). An input named `created_at` causes Xano to overwrite `created_at` on every record the executor edits.

Change the order of steps so the row exists first, and pass its id to the executor. Make no other behaviour changes.

## Functions in scope
- Worker ticks: `docgen/pdf_worker_tick` and `image_worker_tick`
- Executors:
  - `docgen/papermill_generate_pdf_cover`
  - `docgen/papermill_generate_pdf_inner`
  - `executor_cover_image`
  - `executor_page_image`
  - `executor_character_image`

## 1. Worker ticks: change every dispatch branch
That is 2 branches in `pdf_worker_tick` (cover-pdf, inner-pdf) and 3 in `image_worker_tick` (cover-image, page-image, character-image). In each branch, replace "function.run, then db.add executor_runs" with these steps, in this order:

1. `db.add executor_runs` with the same fields as today (`executor_name`, `job_type`, `status: "queued"`, the job id field, `created_at: $now`). Leave out `async_job_id`. Name the result `$executor_run`.
2. `function.run` the executor with `runtime_mode = "async-shared"`. Pass two inputs: the job id (`pdf_jobs_id` or `image_jobs_id`, as today) and `executor_runs_id: $executor_run.id`. Do not pass any timestamp.
3. `db.edit executor_runs` with id `$executor_run.id`, setting `async_job_id` to the value `function.run` returned.

Wrap step 2 in a try/catch. If the dispatch throws, edit the run row to `status: "error"`, with `completed_at: now` and an `executor_result` that notes "dispatch failed". The job's own retry logic then handles it, and no run row is left stuck at "queued".

Keep the `$now` variable for `created_at` on the run row and for the tick's own lock and retry fields.

## 2. Executors: change all five
1. Remove the `created_at` / `run_created_at` input. Add `int executor_runs_id` (required).
2. Replace the `db.query executor_runs` lookup by job id and `created_at` with `db.get executor_runs` by `id = $input.executor_runs_id`. Name the result `$executor_run`, as today.
3. Directly after the lookup, add a precondition that `$executor_run` is not null and that its job id field matches the job id input (`pdf_jobs_id` or `image_jobs_id`). On failure, throw a fatal error. Do not edit any rows.
4. Leave everything else unchanged.

## 3. Naming rule (applies to every change above)
No function input or variable may have the same name as a column in a table that the function adds to or edits, apart from the field used to look the record up. Xano writes values with matching names into those columns implicitly (the hidden-fields behaviour). In particular, never name an input or variable `created_at`, `status`, `message` or `last_modified_at`.

## 4. Do not change
- The claim functions (`claim_pdf_jobs`, `claim_image_jobs`)
- The orchestrators
- Existing `executor_runs` rows
- The table schemas

## 5. Tests
- PDFs: run the Postman `_tests` order folders. They must all pass. Then check the order's audit rows: `created_at` must not change.
- Images: one story run (2A–2B). Then check:
  - Every `executor_runs` row for the story ends in success or error. None is left at queued.
  - There is exactly one run per image job attempt, with no duplicates.
  - Each run's `async_job_id` is set.
  - `created_at` is unchanged on `image_jobs`, `instant_story_pages`, `characters` and `instant_stories`.
