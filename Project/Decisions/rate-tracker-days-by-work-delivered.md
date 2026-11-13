---
type: decision
title: "rate-tracker-days-by-work-delivered"
project: tomale-rn-v1
status: accepted
date: "2026-11-13"
related:
  - "[[2026-11-13-001]]"
affects:
  - "Project/Automation/launch-tracker/days.json"
features:
  - X-process
---

# Decision: rate-tracker-days-by-work-delivered

## What we decided

Kyle chose "work delivered" as the measure of a working day on the launch tracker, shown as day cards in a "Days worked" section. Each day is scored as estimated days delivered (each milestone's mid estimate × the progress it made that day) and rated 🐢 (<0.5), 👍 (0.5–1.5) or 🔥 (>1.5).

## Why

Not discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Source data is `Project/Automation/launch-tracker/days.json`; past days were scored by Claude. The daily pipeline (step 7) adds one `days.json` row per new working day and uploads it to the dashboard.

## Related notes

[[2026-11-13-001]], [[CURRENT]]
