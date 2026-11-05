---
type: decision
title: "use-corrected-tomale-brand-colours"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-001]]"
  - "[[deepen-brand-colours-for-accessible-ui-roles]]"
  - "[[use-glacial-indifference-for-live-app-text]]"
affects:
  - "Tomale design system (tokens)"
  - "global.css (UniWind/Tailwind v4 theme, via RS-2026-11-05-01)"
features:
  - X-platform
---

# Decision: use-corrected-tomale-brand-colours

## What we decided

The Tomale brand palette (Kyle, 05/11):

| Colour | Value |
|---|---|
| Coral | `#FF6666` |
| Mint | `#39C2C1` |
| Sunflower | `#FCCA37` |
| Book brown | `#A16959` (logo shadow `#7C4A3E`) |
| Grey | `#F8F8F8` |
| Hero gradient | `#FF3131 → #FF914D` |

## Why

The Canva brand guidelines PDF (summer 2025) had errors: it showed `#39C2C1` for sunflower, and olive `#A6A26A` for book brown while the logo itself uses `#A16959`. The palette above corrects these.

## Alternatives considered

Using the PDF's values as printed. Not otherwise discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

The palette is the base of the "Tomale Design System" Claude artifact (05/11) and reaches the app through RS-2026-11-05-01 (load the design system into the gluestack/UniWind theme before speckit 008). UI roles derived from these colours are in [[deepen-brand-colours-for-accessible-ui-roles]].

## Related notes

- [[2026-11-05-001]]
- [[deepen-brand-colours-for-accessible-ui-roles]]
- [[use-glacial-indifference-for-live-app-text]]
- [[RS-2026-11-05-01]]
