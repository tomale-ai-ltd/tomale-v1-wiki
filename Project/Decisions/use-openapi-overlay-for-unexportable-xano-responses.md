---
type: decision
title: "use-openapi-overlay-for-unexportable-xano-responses"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
  - "[[RS-2026-11-12-01]]"
  - "[[RS-2026-11-11-01]]"
affects:
  - "[[backend-xano]]"
  - "api/openapi/overrides.yaml"
  - "api/client.ts"
  - ".cursor/rules/tomale-api.mdc"
features:
  - X-process
  - F-characters
---

# Decision: use-openapi-overlay-for-unexportable-xano-responses

## What we decided
Responses Xano can't describe in its OpenAPI export are kept in an overlay: `api/openapi/overrides.yaml`, merged by `pnpm update:openapi`, backed by recorded Postman fixtures in `.tests/fixtures/`, a Jest fixture test, and a rule in `tomale-api.mdc`. Kyle approved it as [[RS-2026-11-12-01]] (12/11); Cursor applied it with [[RS-2026-11-11-01]] in PR #26.

## Why
The Xano AI confirmed XanoScript has no response-schema syntax, so any response built in the stack (characters list and detail, `auth/me`) exports as an empty object and the generated client gets no types for it.

## Alternatives considered
Not discussed in session notes.

## Trade-offs accepted
Not discussed in session notes.

## Workflow detail
Each regeneration merges the overlay; the fixture test checks overlay shapes against recorded responses. A follow-up commit makes `picture_status` required and adds the `POST /characters` 200 response. [[RS-2026-11-12-04]] updates the overlay after M3 part A.

## Related notes
[[2026-11-12-001]], [[RS-2026-11-12-01]], [[RS-2026-11-11-01]], [[backend-xano]]
