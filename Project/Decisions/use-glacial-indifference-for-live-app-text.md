---
type: decision
title: "use-glacial-indifference-for-live-app-text"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-001]]"
  - "[[use-corrected-tomale-brand-colours]]"
affects:
  - "Tomale design system (type scale)"
  - "assets/fonts/ and app/_layout.tsx font loading (via RS-2026-11-05-01)"
features:
  - X-platform
---

# Decision: use-glacial-indifference-for-live-app-text

## What we decided

- **More Sugar** (the logo font) is used only inside static logo artwork.
- **Glacial Indifference** (SIL OFL 1.1; Regular, Medium, SemiBold, Bold) is used for all live app text.
- Books keep their per-theme open-source Google Fonts.

## Why

The Canva licence for More Sugar covers static images, not live text. Glacial Indifference is open-licensed (OFL), so it can be bundled in the app.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The TTFs and `OFL.txt` (from github.com/marcologous/glacial-indifference) are saved in `Project/Research/brand/fonts/` and used in the design system's type scale. RS-2026-11-05-01 bundles them in the app and loads them with `expo-font`. App body text is 16px minimum ([[deepen-brand-colours-for-accessible-ui-roles]]).

## Related notes

- [[2026-11-05-001]]
- [[use-corrected-tomale-brand-colours]]
- [[deepen-brand-colours-for-accessible-ui-roles]]
- [[RS-2026-11-05-01]]
