---
type: decision
title: "diagnose-before-briefing-and-use-contract-fixtures"
project: tomale-rn-v1
status: accepted
date: "2026-11-06"
related:
  - "[[2026-11-06-001]]"
  - "[[tag-crash-reports-with-active-profile-id-only]]"
affects:
  - "[[operating-model]]"
  - ".cursor/rules/tomale-api.mdc"
features:
  - X-process
  - X-testing
---

# Decision: diagnose-before-briefing-and-use-contract-fixtures

## What we decided

1. **Claude diagnoses before briefing a fix.** When a test or device check shows a symptom, Claude checks the cause against the source of truth (Xano mirror, app repo, Postman) before writing Cursor's prompt, then gives Cursor the cause first, the exact expected data shape, and the fix, with limits on approach where a simpler route exists (fix it in our code, don't work around library internals).
2. **Test fixtures come from the real contract.** API response data in app tests is copied from `api/openapi/xano.yaml` or a recorded Postman response. If the spec lacks a field the code needs, Cursor asks rather than inventing the shape.

## Why

Kyle (06/11) after the 007 T026 Sentry check: `profile_id` showed `<invalid>`. Claude's prompt led with tag set/clear handling, so Cursor spent a long turn in Sentry scope internals. The real cause was one line in the mirror: `GET /auth/me` returns `{ user, auth: { active_profile } }`, while `readActiveProfileId` read top-level `active_profile`; the Jest tests passed because their invented fixtures used the same wrong shape (the generated OpenAPI type omits `active_profile`).

## Alternatives considered

Not discussed beyond the fix itself.

## Trade-offs accepted

A few minutes of checking before each fix brief; fixtures need a spec or recorded response to copy from.
