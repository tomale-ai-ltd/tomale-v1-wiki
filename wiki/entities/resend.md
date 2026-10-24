---
type: entity
entity-type: tool
name: Resend
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/tool
source-count: 6
date-updated: 2026-10-24
cssclasses: []
---


# Resend

## Facts

- Resend's free tier comfortably covers V1 launch needs with 3,000 emails/month, 100/day.
- Resend is being used as the transactional email provider for Tomale V1.
- Resend supports stored templates, which removes the need to inline HTML in Xano.
- Decision made to replace SendGrid with Resend for transactional email.
- Resend has been chosen as the transactional email provider for Tomale V1.
- Resend is used for sending email verification tokens.
- Resend is utilized for sending email verification tokens.

## Connections

- [[transactional-email]] *(applies-to)*
- [[sendgrid]] *(contrasts-with)*
- [[email-verification]] *(uses)*
- [[sendgrid]] *(related-to)*
- [[tomale-v1]] *(uses)*
- [[xano]] *(uses)*
- [[tomale]] *(uses)*
- [[email-verification]] *(uses)*

## Sources

- [[Project/Decisions/migrate-image-storage-to-aws-s3-signed-urls.md]]
- [[Project/Decisions/defer-stripe-webhook-mode-branching-to-phase-2.md]]
- [[Sessions/2026-05-07-003.md]]
- [[Project/Decisions/replace-sendgrid-with-resend-for-transactional-email.md]]
- [[_raw/Chat Sessions/_archive/2026-05-11-001.md]]
- [[Sessions/2026-05-11-001.md]]
