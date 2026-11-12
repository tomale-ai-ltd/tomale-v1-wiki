---
type: decision
title: "show-confirmations-as-toast-above-tab-bar"
project: tomale-rn-v1
status: accepted
date: "2026-11-12"
related:
  - "[[2026-11-12-001]]"
  - "[[RS-2026-11-12-03]]"
  - "[[build-ui-from-a-component-kit-with-a-screenshot-loop]]"
affects:
  - "specs/008-characters/spec.md"
  - ".cursor/rules/ui.mdc"
features:
  - F-characters
  - X-platform
---

# Decision: show-confirmations-as-toast-above-tab-bar

## What we decided
Kyle, 12/11, after 008 device testing: confirmations are a toast over the tab bar for about 3 seconds, announced to a screen reader, never inline. For characters: "[Name] archived" or "[Name] deleted", with no undo (restore is Unarchive from the archived filter).

## Why
Device testing found inline confirmations among five US6 bugs.

## Alternatives considered
Inline confirmations (as first built); an undo action (not offered).

## Trade-offs accepted
Not discussed in session notes.

## Workflow detail
Fixed in US6 (`2f1e20f`); Toast is one of the US7 kit components in `components/ui/`.

## Related notes
[[2026-11-12-001]], [[build-ui-from-a-component-kit-with-a-screenshot-loop]], [[RS-2026-11-12-03]]
