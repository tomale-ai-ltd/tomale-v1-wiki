---
type: decision
title: "draw-header-bands-under-the-status-bar"
project: tomale-rn-v1
status: proposed
date: "2026-11-17"
related:
  - "[[2026-11-17-001]]"
  - "[[build-ui-from-a-component-kit-with-a-screenshot-loop]]"
  - "[[snags]]"
affects:
  - "`.cursor/rules/ui.mdc`"
  - "kit ScreenHeader"
features:
  - F-design-system
---

# Decision: draw-header-bands-under-the-status-bar

## What we decided
Coloured header bands (the curved-bottom bands in the mock-ups) are one kit component, `ScreenHeader`. The band runs edge to edge under the status bar; its height is the top safe-area inset plus its content, never a fixed number. Two forms: compact (back or close, title) for utility screens, and tall (with a picture) only where the picture helps. Content never sits under the status bar. Fixes snag S-001 from 009 onwards.

## Why
008's bands started below the app's top bar and stopped in a straight line (S-001), and fixed heights wasted space on smaller phones. One component makes every screen behave the same.

## Alternatives considered
Dropping the curved bands (loses the brand look); a fixed-height band per screen (the 008 problem).

## Trade-offs accepted
Screens built in 008 change when they move onto the kit header (the snag polish pass).
