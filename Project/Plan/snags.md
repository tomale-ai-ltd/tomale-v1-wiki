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
| S-003 | 12/11 (008) | Sign-in and magic-link screens | Still use the platform button: greys out while waiting, no spinner. Switch to the kit Button (loading = full colour plus spinner). | Low | When the auth screens get their visual pass | Open |
| S-004 | 17/11 (M3 prep) | Profile avatars | Kyle doesn't like the bundled preset avatar set (`assets/avatars`). Replace it with a set that fits the brand. Keep the existing `preset:<key>` names, or map old keys to new images, so stored `avatar_key` values still resolve. Recheck the licence and any attribution for the new set. | Low | Before launch (not blocking 009) | Fix ready: 30 animal avatars approved 18/11, RS-2026-11-18-01 |
