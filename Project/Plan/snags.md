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
| S-005 | 18/11 (010 design) | Profile picker (902) | Add the Tomale book mark (`logo-tomale-square-no-bg.png`, about 96 px) above "Who's reading?". The picker is the welcome screen each time the app opens on a household with children. Drawn on the 009 canvas board 902 (not in the 009 export). Logo rule: book mark or combined logo only on splash, sign-in and sign-up, onboarding and the picker; never in tab headers, never recoloured or on the hero gradient. | Low | Snag polish pass after 009 | Open |
| S-006 | 18/11 (009 screenshots) | Profile picker | Pictures sit in one column, so the "Grown-ups need their PIN…" line lands on the bottom edge; use the board's grid. Page uses the theme surface instead of the board's cream, and the board's corner shapes aren't drawn. | Low | Snag polish pass after 009 | Open |
| S-007 | 18/11 (009 screenshots) | Add a child | No large picture preview in the header; the Pictures / Our characters tabs are plain labels instead of a pill toggle. | Low | Snag polish pass after 009 | Open |
| S-008 | 18/11 (009 screenshots) | PIN locked and Forgot PIN | Use the plain theme header band without the board's large lock / envelope picture. | Low | Snag polish pass after 009 | Open |
| S-009 | 18/11 (009 screenshots) | Set PIN | Eyebrow sits under the title; the board puts eyebrow, title and intro together in a gold band. | Low | Snag polish pass after 009 | Open |
| S-010 | 18/11 (009 screenshots) | Avatar menu (child) | "Switch profile" is a list row; the board draws it as a red pill button. | Low | Snag polish pass after 009 | Open |
| S-011 | 18/11 (009 phone pass) | PIN pad sheet | Only the X closes it; add swipe-down to dismiss. | Low | Snag polish pass after 009 | Open |
| S-012 | 18/11 (009 phone pass) | Profile picker, Manage profiles | No sign of which profile is active. Add an active indicator, e.g. a coral ring around the avatar or the row. | Medium | Snag polish pass after 009 | Open |
| S-013 | 18/11 (009 phone pass) | Change PIN | Title reads "Enter your current PIN" with "Change PIN" under it, which is confusing. Swap them: "Change PIN" as the eyebrow/title above "Enter your current PIN". See S-009. | Medium | Snag polish pass after 009 | Open |
| S-014 | 18/11 (009 phone pass) | Change PIN | After saving, returns to Manage profiles rather than Home. Decide which is right; Manage is fine if S-012 shows the active profile. | Low | Snag polish pass after 009 | Open |
| S-015 | 18/11 (009 phone pass) | Avatar picker (Add/Edit) | The black border on the selected animal makes that row hold 4 instead of 5, so the grid jumps. Draw the selection inside the cell (or reserve the border on every cell). | Medium | Snag polish pass after 009 | Open |
| S-016 | 18/11 (009 phone pass) | Offline state | "Try again" is small and sits below the avatar list. Move it to the top and make it larger. | Low | Snag polish pass after 009 | Open |
| S-017 | 18/11 (009 phone pass) | Tab headers | "Hello [name]" shows on every tab. Keep it on Home only; other tabs show just the avatar. Design rule change: record as a decision when fixed. | Medium | Snag polish pass after 009 | Open |
| S-018 | 18/11 (009 phone pass) | Header band, dark mode | A white area shows around the header shape in dark mode instead of the dark surface. | Medium | Snag polish pass after 009 | Open |
| S-019 | 19/11 (010 phone pass) | Toasts (approve, reject, keep, delete, Coming soon) | Plain text on a basic pill; give them the kit's richer toast styling (icon, weight, spacing). | Low | Snag polish pass after 010 | Open |
| S-020 | 19/11 (010 phone pass) | Network error on approve | "Try again" is a plain text link; use the kit Button (secondary), and show that the phone is offline (an icon or banner) rather than text alone. The fact that the error line stays after a successful retry is a bug, fixed in 010. | Low | Snag polish pass after 010 | Open |
| S-021 | 19/11 (010 phone pass) | Waiting sheet OK, picker highlight ring | Both use the danger red rather than the primary coral; check against the 010 boards (HomeChild, picker). Danger red stays on Reject story and Delete. | Low | Snag polish pass after 010 | Open |
| S-022 | 19/11 (010 phone pass) | Story cover placeholder, dark mode | The placeholder square on Home's Recent stories is almost black on the dark page; lift it to a visible surface tone. | Low | Snag polish pass after 010 | Open |
| S-023 | 23/11 (snag pass check) | Settings page | The back button shows "(tabs)" beside the back icon. | Low | Snag pass 23/11 | Open |
| S-024 | 23/11 (snag pass check) | Manage profiles | Pictures sit off centre since the active ring was added. | Low | Snag pass 23/11 | Open |
| S-025 | 23/11 (snag pass check) | Manage profiles | "Parent PIN" / "Change PIN" is plain text; make it a kit Button. | Low | Snag pass 23/11 | Open |
| S-026 | 23/11 (snag pass check) | Change PIN | No confirmation after the new PIN is saved; show a toast. | Low | Snag pass 23/11 | Open |
| S-027 | 23/11 (snag pass check) | Change PIN, Forgot PIN headers | The back button stretches across the header; it should be a small button top left as on other pages. | Medium | Snag pass 23/11 | Open |
| S-028 | 23/11 (snag pass check) | Who's reading? | The close X above the book mark is slightly off centre. | Low | Snag pass 23/11 | Open |
| S-029 | 23/11 (snag pass check) | Forgot PIN | Remove the envelope picture (Kyle doesn't like it); amends S-008. | Low | Snag pass 23/11 | Open |
| S-030 | 23/11 (snag pass check) | Who's reading?, offline | The book mark disappears on the offline state. | Low | Snag pass 23/11 | Open |
