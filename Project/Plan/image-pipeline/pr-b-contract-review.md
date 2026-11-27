---
type: plan
title: pr-b-contract-review
project: tomale-rn-v1
status: active
date: 2026-11-27
related:
  - "[[ip-04-cursor-brief]]"
  - "[[IP-04-spec-contract-and-repo]]"
  - "[[PRD-Image-Pipeline]]"
---

# Review: gateway PR B (#2, `001-image-gateway` @ `1aa6884`)

Claude's review against the vault PRD and decisions, and the Xano mirror (`5783a3f`+): executors, `image_worker_tick`, `characters_POST`, the Stripe and HPBC webhooks.

**Verdict: well structured; not approvable yet.** Six must-fix items in the contract, four should-fix items, and two decisions for Kyle. Most of the feasibility questions are answered below from the mirror.

## Must-fix

1. **The page-planner config is missing.** Today each executor runs the planner (`data_models.prompt_template` + `output_schema`) before the image call. In the new design the worker runs it, but `DataModelSnapshot` carries only `model_settings`. Add `prompt_template` and `output_schema`, or the gateway would need its own copy of the prompts: two sources of truth, against the decisions.
2. **Character jobs can't be expressed.** `JobInputs` requires `artwork_style` and `theme`, but `executor_character_image` uses a fixed portrait style and no theme. Make the inputs depend on `job_type` (`oneOf` with `PageInputs`, `CoverInputs`, `CharacterInputs`, discriminated by `job_type`):
   - page needs `page_text` and `page_number`
   - cover needs `title`
   - character needs the one character, plus the current portrait and `instruction` for "draw again"
3. **`CharacterInput` has no `name` and no defined shape.** Labelled references ("Reference image 1 = MIA …") and the judge's answer key both rely on the name and the attribute fields. Make `name` required, and define the attributes as the Xano `characters` fields (`physical_description`, `primary_attributes`, `face_attributes`, `eyes_attributes`, `hair_attributes`, `clothing_attributes`) instead of an open object.
4. **The rules linking moderation to status are undefined.** The spec says "error_terminal (or the documented terminal path)". State normatively:
   - `complete` ⇒ `enforcement: none` (subject to decision D1)
   - any other enforcement ⇒ `error_terminal` with `MODERATION_BLOCKED`
   - `flag_account` ⇒ Xano writes `moderation_flags`
   - a provider safety block that survives the one softened retry ⇒ `error_terminal` with `PROVIDER_SAFETY_BLOCK`
   Add schema rules where OpenAPI allows (`if`/`then` on `status`), and prose where it doesn't.
5. **Remove `callback_url` from the request.** A caller-supplied URL is a server-side request forgery and exfiltration path, which the threat model has to patch with an allowlist. Make the Xano webhook URL fixed per-environment configuration in the gateway instead.
6. **`TOO_MANY_CHARACTERS` conflicts with `maxItems: 4`.** Schema-level `maxItems` turns one bad job into a `400` for the whole batch, but the spec wants a per-job reject. Drop `maxItems` from the schema and enforce 4 as a per-job validation rule. (New stories link 1–3 characters through `POST /instant_stories/{id}/characters`; legacy stories have up to 7, but they're never regenerated in V1.)

## Should-fix

7. **Correlate with `executor_runs`.** Xano finds runs by id ([[find-executor-runs-by-id-not-timestamp]]). Add `executor_runs_id` per job in the request and echo it in the callback.
8. **Spell out `error_retry`:** it means Xano requeues the job with `attempt + 1` through the existing claim and backoff path. Add an optional `retry_after_seconds`.
9. **Reference images by storage key:** allow `reference_image_s3_key` alongside `reference_image_url`, so that once portraits live in private S3 the worker reads them directly rather than through a public URL.
10. **Threat model additions:**
    - the batch endpoint is reachable from the internet, so the signature check must run first and cheaply, with Cloud Run max instances as the ceiling
    - one HMAC secret per direction, plus a rotation procedure
    - `GET /v1/health` reveals no version or build details

## Decisions for Kyle

- **D1, borderline images.** When image moderation says "a parent should look at this":
  - **(a) Regenerate, then fail if it's still borderline.** No borderline picture ever reaches a story; this matches the rule already used for character pictures ([[moderate-free-text-instructions-with-moderation-text-policy]]). *Claude recommends (a).*
  - **(b) Keep the picture and send the story to parental approval,** like flagged text.
- **D2, private images at cut-over.** New images land in private S3, so the app has to show links that expire after an hour.
  - **(a) Signed links from cut-over:** Xano returns signed links, and the app refreshes them on expiry. That's a small app change (Cursor) plus Session A work.
  - **(b) Interim copy:** Xano copies each finished image into its own storage as today, so there's no app change, and private S3 follows in M9.
  - Signed URLs are a launch requirement either way ([[pre-launch-checklist]]). *Claude recommends (a), so it's done once, if the app change fits beside 011–013. Otherwise (b), with children's images staying public until M9.*

## Xano feasibility: answers from the mirror

| # | Question | Answer |
|---|---|---|
| 1 | HMAC-SHA256 outbound | **Yes.** Xano lambdas run JavaScript with Node `crypto`; `print_on_demand/hpbc_create_order` already signs with `crypto.createHmac`. SHA-256 works the same way. |
| 2 | Raw body inbound | **Partly.** `util.get_raw_input` exists and is used by the Stripe and HPBC webhooks (`encoding = "json"`). **Kyle to check:** does the encoding dropdown offer a raw or text option? HMAC needs the exact bytes. The Stripe verify action works, which suggests yes. |
| 3 | Headers | **Yes.** Inbound via `$env.$http_headers` (Stripe, HPBC); outbound via `api.request` headers. |
| 4 | Clock | Server UTC; a 5-minute window is fine. |
| 5–6 | Sizes | 20 jobs × (attributes ≈ 2 KB + style ≈ 1 KB + page text) is under 100 KB, well within normal limits. Callbacks are about 2 KB. |
| 7 | Logging | Don't log batch bodies: `executor_runs` logs small status fields only ([[log-only-small-status-fields-in-executor-runs]]). |
| 8 | Outbound timeout | `api.request` has a `timeout` (30–300 s in use). Use about 15 s; the gateway answers `202` quickly. |
| 9 | Timeout after accept | Re-send the same `image_jobs_id` + `attempt`; the gateway answers `duplicate: true`, so there's no double charge. |
| 10, 13 | Idempotent upsert, atomicity | No `db.transaction` in use today. Make the webhook idempotent: a unique index on `token_usage` (`image_jobs_id`, `attempt_number`) for the image row ([[adopt-unique-index-dedup-for-webhook-ingest]]), and status writes that only move forward. |
| 11 | `dispatched` status | Session A (IP-10). |
| 14–15 | Kill switch, reaper | **Session A must extend the reaper** to requeue `dispatched` jobs whose lease expired. Today it only looks at `processing`, so a lost callback would leave a job stuck. On `503 KILL_SWITCH` the executor leaves the job `queued`. |
| 16–17 | Secrets | Xano env vars, as for every other secret. **Use two secrets, one per direction**, so a leak on one side can't be used to forge the other direction. Rotation: add the new one, accept both for a day, drop the old. |
| 12 | Storage columns | Session A adds a storage-key field next to each native image field (page `image`, story `cover_image`, character `cover_image`), as planned in [[migrate-image-storage-to-aws-s3-signed-urls]]. |

## Next

Kyle answers D1, D2 and feasibility question 2 → Cursor applies the fixes on PR #2 → Claude re-checks → Kyle approves → IP-08 and IP-09 briefs.
