---
type: decision
title: defer-workspace-hidden-fields-setting-to-pre-launch-sweep
project: tomale-rn-v1
status: accepted
date: 2026-10-22
features:
  - X-security
---

# Decision: defer-workspace-hidden-fields-setting-to-pre-launch-sweep

## What we decided

The Xano workspace-level Hidden Fields setting was reviewed and deliberately not enabled. Instead, a pre-launch sweep will set `enforce_hidden_fields = true` on every `db.add` / `db.edit`, map columns explicitly, add `output` lists, and finish with a full `_tests` run. The sweep is added to the pre-launch checklist alongside rate limiting.

## Why

Enabling the setting workspace-wide would change behaviour on every endpoint at once. Handling it per statement during a dedicated sweep, verified by a full `_tests` run, keeps the change reviewable. Today's triage also showed that same-value collisions (`auth/refresh`, `reset_password`, magic-link) need individual treatment, so they were deferred to that sweep. Only the `last_login` edit in `auth/login` gets the toggle now.

## Alternatives considered

Enabling the workspace-level setting now (reviewed, rejected). Renaming contract inputs was also set aside in favour of statement-level `enforce_hidden_fields`.

## Trade-offs accepted

Remaining endpoints stay unhardened until the pre-launch sweep. The `users.password` hash check is not possible directly (masked) and is covered only indirectly by the `_tests` run.

## Workflow detail

Fixes are applied one at a time and reviewed against the published version before publishing. The pre-launch checklist gains the sweep. Phase 1 close-out proceeds with only four live items fixed: `conversations/{id}/message`, `API/character_edit`, `admin/create_user_log`, `auth/login`.

## Related notes

[[replace-dblink-inputs-with-explicit-allowlists]]
[[add-per-endpoint-rate-limiting-in-xano]]
[[avoid-column-named-function-inputs-in-xano]]
[[security-model]]
[[5-cto-implementation-plan]]
