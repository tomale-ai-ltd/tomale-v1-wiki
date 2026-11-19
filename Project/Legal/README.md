---
type: index
title: Legal documents
project: tomale-rn-v1
date: 2026-11-19
related:
  - "[[pre-launch-checklist]]"
  - "[[010b-auth-signup-micro-prd]]"
  - "[[retain-account-data-30-days-after-closing]]"
---

# Legal documents

Public legal pages for tomale.ai and the app, plus internal policies behind them. Each published version is kept in a dated folder and never edited afterwards, so we can always show what a parent agreed to. The folder date is the "Last updated" date on the pages, and the Terms date is `terms_version` recorded at sign-up (010b, B2).

## Current version: `2026-11-19/` (live on Squarespace since 19/11/2026)

| Page | File | Squarespace URL | Editable draft (Claude Docs) |
|---|---|---|---|
| Terms and Conditions | `2026-11-19/terms.md` | `/terms` | https://claude.ai/artifact/7wAdXup2Q4sTQbS3EkfQyn |
| Content Guidelines | `2026-11-19/content-guidelines.md` | `/content-guidelines` | https://claude.ai/artifact/3jvV7hCeE1WtALGyRiwQhj |
| Privacy Notice | `2026-11-19/privacy-notice.md` | `/privacy-notice` (replaces the Termly notice of 7 April 2025) | https://claude.ai/artifact/Vwp3cYouDQkNcWRqZtwBdw |
| Cookie Policy | `2026-11-19/cookie-policy.md` | `/cookie-policy` | https://claude.ai/artifact/RpJxRFfi3FV4c9kwoJuDXu |
| EULA | `2026-11-19/eula.md` | `/eula` (also App Store Connect → License Agreement) | https://claude.ai/artifact/2hffsptxPErgtbtQZY1GkT |

Internal, never published: `internal/content-moderation-policy-v1.0.md` (the policy the Xano moderation prompts follow; the Content Guidelines are its public summary, so change both together).

## Status

Published 19/11/2026 (Kyle): all five pages live at the URLs above, Markdown blocks with the table CSS in Custom CSS. Backup period set to 35 days in the Privacy Notice §7.

Still open (not blocking the pages):
- Solicitor review before launch (pre-launch checklist §6, PU-2026-11-19-01).
- Cookie Policy: confirm the banner type is "Opt in and out" and run the live-site scan; correct the cookie table if it differs.
- Moderation record retention: 2 years as published; the Xano side still keeps them indefinitely until the purge job ([[account-closing-micro-prd]]).
- The 30-day delete promised in the Terms and Privacy Notice needs the backend job before launch.
- Page titles: set each page's SEO title (e.g. "Privacy Notice | Tomale") instead of the URL slug.

## How to publish (Squarespace)

1. One page per document at the URL above. Add a **Markdown block** and paste the whole file (tables need the Markdown block; a text block flattens them).
2. One Markdown block per page; Squarespace merges neighbouring Markdown blocks.
3. If tables look cramped, add borders and padding for `table`, `th`, `td` in Design → Custom CSS.
4. Publish all five together so the links between them work.
5. Footer links: Terms, Privacy Notice, Cookie Policy, Content Guidelines, Cookie settings.

## Changing a document later

Edit the Claude Docs draft, export it, strip the draft notes, and save as a new dated folder (`YYYY-MM-DD/`) with only the changed files plus a line here saying what changed. Update the "Last updated" date. If the Terms change, the app's `terms_version` config changes to the new date. Never edit a published folder.

## Version history

| Date | Change |
|---|---|
| 2026-11-19 | First versions of all five, drafted by Claude from the vault; published on Squarespace 19/11 (Kyle). Solicitor review before launch (pre-launch checklist §6, PU-2026-11-19-01). |
