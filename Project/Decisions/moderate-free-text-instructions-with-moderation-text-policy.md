---
type: decision
title: "moderate-free-text-instructions-with-moderation-text-policy"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-002]]"
  - "[[moderate-names-in-two-stages]]"
  - "[[characters-backend-prep-brief]]"
affects:
  - "[[PRD-Characters]]"
  - "ai pipeline/content_moderation_text"
  - "POST /characters/{id}/regenerate_image"
  - "moderation_flags"
features:
  - F-characters
  - X-security
---

# Decision: moderate-free-text-instructions-with-moderation-text-policy

## What we decided

Free-text user instructions (first use: the optional instruction on "draw again", `POST /characters/{id}/regenerate_image`) are moderated with the existing `moderation-text` policy through a general function:

- New `ai pipeline/content_moderation_text` with inputs `payload`, `users_id`, `entity`, `entity_id`. It loads the default active `moderation-text` data model and returns the raw result; callers decide what to do with it.
- Policies stay in `data models`, not in function code.
- For character images, anything but `enforcement: none` is refused; `flag_account` writes `moderation_flags`.

## Why

`moderation-name` is a names-only policy: it blocked "wearing a red scarf". A separate instruction policy would duplicate and drift from the Tomale content policy. Parental oversight cannot gate a household-wide image, so character images refuse anything not cleared outright.

## Alternatives considered

- A hard-coded instruction policy in a new function (rejected).
- Reusing `moderation-name` for instructions (it blocked a harmless instruction).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Built and published in Xano on 05/11 as part of the Characters backend prep. Kyle's Postman tests: "wearing a red scarf" worked; "make him hold Elsa's ice crown" was refused with a copyright reason. Postman folder 5D asserts `CONTENT_REJECTED` for a copyright instruction ([[test-suite]]). Later free-text inputs can call the same function and apply their own enforcement rule.

## Related notes

- [[2026-11-05-002]]
- [[moderate-names-in-two-stages]]
- [[characters-backend-prep-brief]]
- [[PRD-Characters]]
- [[test-suite]]
