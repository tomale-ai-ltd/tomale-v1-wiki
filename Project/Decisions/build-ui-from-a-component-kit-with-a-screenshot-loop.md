---
type: decision
title: build-ui-from-a-component-kit-with-a-screenshot-loop
project: tomale-rn-v1
status: proposed
date: 2026-11-12
related:
  - "[[RS-2026-11-12-02]]"
  - "[[RS-2026-11-12-03]]"
  - "[[2026-11-12-001]]"
features:
  - F-design-system
---
# Decision: build-ui-from-a-component-kit-with-a-screenshot-loop

## What we decided
UI work in the app follows one method from 008 onwards:
1. **The agent sees its own screens:** a simulator screenshot script (`pnpm shot`) lets Cursor capture a screen, compare it with the mock-up PNG and fix differences before reporting ([[RS-2026-11-12-02]]).
2. **Component kit first:** shared components (card, action tile, sheet, toast, pressable, button with loading state) are built and checked in isolation on a dev-only kit screen, then screens are composed from them.
3. **Exact values from the design source:** each feature's `specs/<feature>/design/` holds the mock-up PNGs and their HTML source; values map to theme tokens.
4. **A UI rule** (`.cursor/rules/ui.mdc`) sets the standards every screen meets ([[RS-2026-11-12-03]]).
5. **One screen per review round**, with the build and mock-up screenshots side by side; Claude lists the differences.

## Why
008's first build met every functional requirement but looked like plain text rows: Cursor had the spec and copy but had never seen the mock-ups, and nothing let it check its own output. Device testing also found missing pressed states, inline confirmations, a safe-area overlap and cropped pictures, all things a kit and a rule prevent once.

## Alternatives considered
Kyle reviewing every screen by eye with no agent screenshots (slow, misses detail); Figma handoff (no Figma in the workflow; the Design canvas plus HTML source covers it); automated visual regression with Maestro now (worth it later, once several slices exist).

## Trade-offs accepted
About half a day of setup before 008's visual pass; a simulator development build on Kyle's Mac.
