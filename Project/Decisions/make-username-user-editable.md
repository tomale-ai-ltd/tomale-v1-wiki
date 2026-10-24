---
type: decision
title: make-username-user-editable
date: 2026-05-21
status: current
project: tomale-rn-v1
---

---

# Decision: Make username user-editable via PATCH /users/me

## What we decided

`username` is a user-editable field, included in the `PATCH /users/me`
allow-list. Updates are validated for uniqueness, must match the regex
`^[a-z0-9_]+$`, and are normalised to lowercase. Changing a username does not
trigger email re-verification.

## Why

A username is distinct from the login email, so changing it has no
authentication or identity-verification consequence — email re-verification is
unnecessary. Allowing edits is the expected affordance for a profile field, and
the uniqueness, regex, and lowercase rules keep usernames well-formed and
collision-free.

## Alternatives considered

Requiring email re-verification on a username change — rejected: the username is
not the login credential, so a change carries no verification implication.
Treating username as immutable after signup was not explicitly weighed in the
session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

`username` joins `first_name`, `last_name`, `about_me`, and the `preferences`
fields in the `PATCH /users/me` allow-list, with server-side uniqueness, regex,
and case validation applied on each update. Like the rest of the `users`-group
restructuring, this deviates from `api-spec` / `data-model` as currently written
and is tracked for reconciliation under carryover item #5.

## Related notes

- [[Sessions/2026-05-21-001|2026-05-21-001]]
- [[Project/Cursor/api-spec|api-spec]]
- [[Project/Plan/5-cto-implementation-plan|5-cto-implementation-plan]]
- [[Project/Decisions/collapse-bool-preference-endpoints-into-users-me|collapse-bool-preference-endpoints-into-users-me]]
- [[Project/Decisions/defer-explicit-profile-avatar-endpoint-until-kid-profiles|defer-explicit-profile-avatar-endpoint-until-kid-profiles]]
- [[Project/Decisions/enforce-server-side-image-validation|enforce-server-side-image-validation]]
- [[Project/Decisions/separate-verify-email-deeplink-from-magic-link-path|separate-verify-email-deeplink-from-magic-link-path]]
