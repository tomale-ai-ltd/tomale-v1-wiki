---
type: entity
entity-type: org
name: Squarespace
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/org
source-count: 11
date-updated: 2026-10-24
cssclasses: []
---


# Squarespace

## Facts

- Squarespace is used for the email verification landing page.
- A Squarespace page is used for email verification, rendering success states after token validation.
- Squarespace is used for hosting the email verification landing page.
- A Squarespace page is used for email verification, rendering success or error states.
- The Squarespace `/verify-email` JS contains a hardcoded placeholder that needs to be replaced.
- Squarespace is mentioned in relation to the '/verify-email' JS.
- Magic link emails contain a standard https:// URL to the Squarespace site.
- The Squarespace site is used as an intermediary for magic link redirection.
- Replaced 'YOUR_AUTH_GROUP_ID' placeholder with actual auth group ID in the Squarespace '/verify-email' page.
- The Squarespace `/verify-email` page was updated with the actual auth group ID.
- The Squarespace `/verify-email` page was integrated.
- The Squarespace page is used for email verification.
- Email verification is done through the Squarespace intermediary.
- Squarespace is used as an intermediary for email verification.

## Connections

- [[email-verification]] *(applies-to)*
- [[users-group-endpoint-restructuring]] *(related-to)*
- [[users-endpoint-group-restructuring]] *(related-to)*
- [[tomale]] *(uses)*
- [[email-verification]] *(uses)*

## Sources

- [[_raw/Chat Sessions/_archive/2026-05-11-001.md]]
- [[Sessions/2026-05-11-001.md]]
- [[Sessions/2026-05-12-001.md]]
- [[Sessions/2026-05-14-001.md]]
- [[Sessions/2026-05-15-001.md]]
- [[_raw/Chat Sessions/_archive/2026-05-14-002.md]]
- [[Project/Decisions/use-https-web-intermediary-for-magic-link-redirect.md]]
- [[_raw/Chat Sessions/_archive/2026-05-21-001.md]]
- [[Sessions/2026-05-21-001.md]]
- [[Project/Decisions/separate-verify-email-deeplink-from-magic-link-path.md]]
- [[Project/Plan/6-api-security-model.md]]
