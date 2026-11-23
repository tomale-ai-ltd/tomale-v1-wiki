---
type: decision
title: "show-greeting-on-home-only"
project: tomale-rn-v1
status: accepted
date: "2026-11-23"
related:
  - "[[2026-11-23-001]]"
  - "[[snags]]"
  - "[[use-profile-aware-bottom-tabs-with-home-dashboard]]"
affects:
  - ".cursor/rules/ui.mdc"
features:
  - F-home
  - F-profiles
---

# Decision: show-greeting-on-home-only

## What we decided

Kyle decided the "Hello [name]" greeting in the header shows on Home only. Other tabs show the profile avatar without the greeting. Fixed in the snag polish pass as S-017 (`3041b9e`).

## Why

Not discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Recorded as a design rule in the app repo's `.cursor/rules/ui.mdc` on branch `polish-snags` (applied in session). New tab screens follow it.

## Related notes

[[2026-11-23-001]], [[snags]], [[use-profile-aware-bottom-tabs-with-home-dashboard]], [[PRD-Home-Dashboard]]
