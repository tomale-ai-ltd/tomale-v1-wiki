---
type: decision
title: keep-help-on-parent-avatar-menu
project: tomale-rn-v1
status: accepted
date: "2026-11-18"
related:
  - "[[2026-11-18-002]]"
  - "[[2026-11-18-001]]"
  - "[[009-profiles-pin-micro-prd]]"
affects:
  - "specs/009-profiles-pin/spec.md"
features:
  - F-profiles
---

# Decision: keep-help-on-parent-avatar-menu

## What we decided

Keep the Help row on the parent's header avatar menu for now, as built in `940818c` (merged in PR #31). It closes the sheet and opens no screen until Help content arrives in M7. This reverses the 18/11 morning plan-review correction that hid Help until M7.

## Why

Claude asked Cursor to add Help per the 009 micro-PRD after the plan review had agreed to hide it. Kyle, 18/11: "not a big deal, keep it for now."

## Alternatives considered

Hide the Help row until M7 (the plan-review correction, still written in the 009 `spec.md`, `plan.md` and `research.md`).

## Trade-offs accepted

A parent can tap a Help row that opens nothing until M7.

## Workflow detail

The 009 spec, plan and research still say Help is hidden; they need bringing into line with the shipped menu (repo-sync item).

## Related notes

[[2026-11-18-002]], [[2026-11-18-001]], [[009-profiles-pin-micro-prd]], [[PRD-Profiles]]
