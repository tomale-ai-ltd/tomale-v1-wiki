---
type: decision
title: "check-every-screen-on-the-phone-before-done"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-002]]"
  - "[[RS-2026-11-12-05]]"
  - "[[build-ui-from-a-component-kit-with-a-screenshot-loop]]"
affects:
  - ".cursor/rules/ui.mdc"
  - "[[operating-model]]"
features:
  - F-design-system
  - X-testing
  - X-platform
---

# Decision: check-every-screen-on-the-phone-before-done

## What we decided

A screen is done only after Kyle sees it on the phone. With it, two native rules: no `var(--…)` strings in native colour props (theme tokens are resolved through `useThemeColor` in `constants/theme.ts`), and screens with inputs handle the keyboard. Approved by Kyle as RS-2026-11-12-05 and applied to `.cursor/rules/ui.mdc` (`0608924`, main `3229cc2`).

## Why

The 008 parent device check (T031) found native-only failures the web screenshots missed: blank icons and wrong text and chip colours on iOS (CSS variables in colour props work on web only), the old More sheet still in use, no keyboard handling, and the Create tab showing a mock-up backdrop as content. Web screenshots can't prove native rendering.

## Alternatives considered

Relying on the web-build screenshot loop alone (the simulator build fails on the Intel Mac), which is what let these failures through.

## Trade-offs accepted

Each screen needs a phone check by Kyle before it counts as done, which adds a step per review round.

## Workflow detail

The screenshot loop on the web build stays for visual matching; the phone check is the final gate. Mock-up backdrops (the page behind a sheet) must be labelled as such so they aren't built as content.

## Related notes

[[2026-11-12-002]], [[RS-2026-11-12-05]], [[build-ui-from-a-component-kit-with-a-screenshot-loop]], [[snags]]
