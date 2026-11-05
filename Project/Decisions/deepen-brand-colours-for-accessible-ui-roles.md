---
type: decision
title: "deepen-brand-colours-for-accessible-ui-roles"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-001]]"
  - "[[use-corrected-tomale-brand-colours]]"
affects:
  - "Tomale design system (role tokens)"
  - "global.css and gluestack Button/Input/Actionsheet styling (via RS-2026-11-05-01)"
features:
  - X-platform
---

# Decision: deepen-brand-colours-for-accessible-ui-roles

## What we decided

UI role tokens use contrast-checked variants of the brand colours (accepted with the design system, 05/11):

- Light-mode primary button: coral deepened to `#D63C3C` with white text (4.6:1). Dark mode uses brand coral with ink text.
- Links and selected states: mint deepened to `#1B7B7A` in light mode.
- Mint and sunflower fills always carry ink text.
- Brand coral is never used for errors; errors use `danger` `#B3261E`.
- App body text is 16px minimum.

## Why

The design system's role tokens were WCAG-checked for contrast in light and dark themes (the light-mode primary pair is 4.6:1). Not otherwise discussed in session notes.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Components use role tokens (`primary`, `on-primary`, `surface-card`, `ink`, `accent-text`, …) rather than raw brand colours or gluestack defaults; RS-2026-11-05-01 maps them into the app theme, and its Verify step checks the contrast pairs are unchanged.

## Related notes

- [[2026-11-05-001]]
- [[use-corrected-tomale-brand-colours]]
- [[use-glacial-indifference-for-live-app-text]]
- [[RS-2026-11-05-01]]
