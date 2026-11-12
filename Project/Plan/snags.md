---
type: plan
title: "Snag list"
project: tomale-rn-v1
status: active
date: 2026-11-12
---

# Snag list

Small visual or UX defects found in device checks that don't block a merge. Each gets fixed in a polish pass or with the next slice that touches the area. Bugs (wrong behaviour, broken or placeholder content, accessibility failures) are not snags: they're fixed before merge.

| ID | Found | Area | Snag | Severity | Target | Status |
|---|---|---|---|---|---|---|
| S-001 | 12/11 (008 T031) | App header, all tabs | The coloured page bands (coral Characters header, mint detail header) start below the app's top bar (profile avatar row) and stop in a straight line, instead of running to the top of the screen behind the status bar. Jarring on rounded-corner phones. Fix in the shared tab header: let the page band extend under the status bar and top bar (transparent top bar over the band). | Medium | Polish pass after 008, before M3 screens | Open |
| S-002 | 12/11 (008 T031) | Characters grid and carousel | "Drawing [Name]…" during a redraw sits directly on top of the existing picture with no background, so it's hard to read. Give it a soft pill or scrim. | Low | Polish pass | Open |
