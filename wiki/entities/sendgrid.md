---
type: entity
entity-type: tool
name: SendGrid
aliases: []
tags:
  - llm-wiki/entity
  - llm-wiki/entity/tool
source-count: 7
date-updated: 2026-10-24
cssclasses: []
---


# SendGrid

## Facts

- SendGrid is used for API keys in the environment variables.
- All API keys, including SendGrid, are duplicated per environment with separate credentials.
- SendGrid API keys are duplicated per environment with separate credentials.
- All API keys for SendGrid are duplicated per environment with separate credentials.
- SendGrid disabled its free plan following the Twilio acquisition, making continued use cost-prohibitive for V1 volume.
- SendGrid is being replaced due to the disabling of its free plan following the Twilio acquisition.
- SendGrid templates need to be recreated in Resend before the SendGrid endpoints can be retired.
- SendGrid is being replaced by Resend due to the discontinuation of its free plan.
- SendGrid endpoints are being refactored to call Resend's API.
- SendGrid endpoints need to be retired after migration to Resend.

## Connections

- [[environment-separation]] *(part-of)*
- [[resend]] *(related-to)*
- [[xano]] *(uses)*
- [[tomale-v1]] *(uses)*
- [[tomale-v1]] *(critiques)*
- [[resend]] *(contrasts-with)*

## Sources

- [[Project/Stack/6. Backend - Xano.md]]
- [[Project/Decisions/separate-dev-prod-environments.md]]
- [[Project/Decisions/place-frontend-development-on-hold.md]]
- [[Project/Decisions/migrate-image-storage-to-aws-s3-signed-urls.md]]
- [[Project/Decisions/defer-stripe-webhook-mode-branching-to-phase-2.md]]
- [[Sessions/2026-05-07-003.md]]
- [[Project/Decisions/replace-sendgrid-with-resend-for-transactional-email.md]]
