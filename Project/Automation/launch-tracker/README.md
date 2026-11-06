# Launch tracker data

Source data for the **Tomale launch tracker** dashboard (https://claude.ai/artifact/XZ79NEg5XQiHphNDhAzs9i). The daily pipeline (step 7) updates these files and uploads them to the dashboard. Edit them by hand if an estimate or the target changes.

- `milestones.json`: one row per roadmap milestone: `est_min`/`est_max` (working days, from [[roadmap]]), `status` (done | in progress | not started), `progress` (0–1), `actual_days` (derived from `worklog.json`), `finished`, `estimate_assumed`, `note`.
- `worklog.json`: one row per milestone worked on per date (`date`, `milestone`, `what`). A date counts as one working day, split equally across the milestones worked that day.
- `plan.json`: `as_of` (snapshot date), `target_date` (late January, assumed 29/01/2027), `review_buffer_days`, Christmas break.
