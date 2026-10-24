---
type: decision
title: "replace-dblink-inputs-with-explicit-allowlists"
date: 2026-10-22
status: current
project: tomale-rn-v1
---

---

# Decision: replace-dblink-inputs-with-explicit-allowlists

## What we decided

Record-editing endpoints and functions no longer accept `dblink` inputs. They use explicit input allowlists and explicit column mapping. Applied in the Phase 1 sweep to `conversations/{id}/message` (remove `dblink`, require `id` and `user_message`), `API/character_edit` (explicit allowlist, drop `instant_stories_id`) and `admin/create_user_log` (map `user_sessions_id` explicitly).

## Why

A `dblink` input lets a caller supply arbitrary fields to a record write. An explicit allowlist limits writes to the fields the endpoint is meant to change. This was one of the live findings from the hidden-fields sweep.

## Alternatives considered

Not discussed in session notes beyond keeping `dblink` as is. Two Xano AI drafts were rejected: one for building from a stale copy and reintroducing security regressions in `auth/login`, and a first `character_edit` draft that would have written a literal string into the owner column.

## Trade-offs accepted

`character_edit` has no caller yet. From a background task there is no `$auth`, so the ownership check fails closed and would need a trusted `users_id` input. Accepted for now.

## Workflow detail

Xano AI output must be reviewed against the published version of each file before publishing. Each sweep fix is reviewed and published one at a time.

## Related notes

[[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]]
[[avoid-column-named-function-inputs-in-xano]]
[[ratify-users-id-as-ownership-field-standard]]
[[fail-closed-active-profile-resolution]]
