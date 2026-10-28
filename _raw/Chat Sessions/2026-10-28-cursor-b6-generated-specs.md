date: 2026-10-28
source: cursor
branch: b6/generated-specs
feature/spec: B6 generated specs

Implemented B6 generated-specs tooling on `b6/generated-specs` from `wip/pre-restructure-2026-10-24`.

What was done:
- Added `scripts/update-data-model.mjs`.
- Added `npm run update:datamodel` in `package.json`.
- Added empty `XANO_INSTANCE_URL`, `XANO_META_TOKEN`, and `XANO_WORKSPACE_ID` placeholders to `.env.example`.
- Ran `npm run update:datamodel`; it failed before writing because the Metadata API returned 401 for the table-list request using the current local `.env` values.
- Kyle corrected the local metadata token, then `npm run update:datamodel` passed.
- Updated the generator to normalize Xano display table names (`store orders` -> `store_orders`, `Fact` -> `fact`) because the table-list response exposes `name` only.
- Added live `audit_store_orders` to the Commerce & Orders domain.
- Re-ran `npm run update:datamodel`; the second run was deterministic.
- Ran `npm run update:openapi`; it completed.
- Ran `npm run typecheck`; it passed.
- Opened PR: https://github.com/tomale-ai-ltd/tomale-rn-test/pull/9

Decisions and why:
- The data-model script follows the existing `update-openapi.mjs` pattern for `.env` loading, `die()`, and atomic tmp + rename writes.
- Metadata API variables are checked inside the new script only, so `update:openapi` remains independent of them.
- Metadata API requests are sequential and retry 429 responses up to three times, honouring `Retry-After` when present, then failing without writing.
- `DOMAIN_MAP` is embedded in the script so domain grouping and table type classification are explicit and reviewed in code.
- `user_profiles` replaces the old expected `user_child_profiles` entry, and `blocked_terms` is included as expected live schema drift.
- `audit_store_orders` is included as a new live Commerce & Orders table.
- Indexes are requested from `/workspace/{id}/table/{table_id}/index`; unavailable indexes are omitted.
- The schema response for `_id` fields did not include target-table metadata, only `access` and `style`, so the generated Notes column does not infer references from field names.

Open questions:
- Kyle should compare the generated `users`, `user_profiles`, and `store_orders` sections in the PR against the Xano UI.
- Kyle should confirm the classifications noted in the PR: `products` and `shipping_options` in Commerce as `user_data`, `support_requests` in Locale & Misc as `system_or_reference`, `blocked_terms` in Moderation & Safety, and `audit_store_orders` in Commerce & Orders.

Commit hashes:
- `8f40cea` add data model generator
- `d79ea75` generate Xano data model
- OpenAPI refresh produced no committed diff after lint-staged normalized `api/client.ts`.
