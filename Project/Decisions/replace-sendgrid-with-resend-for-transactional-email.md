---
type: decision
title: replace-sendgrid-with-resend-for-transactional-email
project: tomale-rn-v1
status: accepted
date: 2026-05-07
features:
  - F-auth
  - X-platform
---

# Decision: replace-sendgrid-with-resend-for-transactional-email

## What we decided

To replace SendGrid with Resend as the transactional email provider for Tomale V1.

Both core sending endpoints have been migrated:

- `sendgrid_basic_send` refactored to call Resend's API
- `sendgrid_dynamic_send` refactored to use Resend's templates feature (template selected via object containing template ID + variables object)

Once the SendGrid endpoints are retired, the endpoint group will be renamed from `integrations/sendgrid` to `integrations/resend`.

## Why

- SendGrid disabled its free plan following the Twilio acquisition, making continued use cost-prohibitive for V1 volume
- Resend's free tier (3,000 emails/month, 100/day) comfortably covers V1 launch needs
- Resend supports stored templates (confirmed working) — removes the need to inline HTML in Xano or build a separate rendering layer
- HubSpot Marketing Email was rejected as inappropriate for transactional sends (subscription/unsubscribe and marketing compliance flows interfere with critical user journeys)
- HubSpot Transactional Email add-on was rejected as disproportionate cost for V1 volume

## Alternatives considered

**HubSpot Transactional Email add-on** — rejected: paid add-on, disproportionate cost for V1 volume.

**HubSpot Marketing Email** — rejected: wrong tool for transactional sends.

**Postmark** — rejected: gold-standard deliverability but no meaningful free tier.

**AWS SES** — rejected: heavier setup (sandbox lifting, suppression list, domain verification) not warranted for V1 volume.

**SendGrid paid plan** — rejected: ~$20/month minimum despite negligible V1 volume.

**Inline HTML templates stored in Xano** — considered but unnecessary once Resend's templates feature was confirmed working.

## Trade-offs accepted

- Resend's template selection model (template ID + variables object) means each email type may require either a separate custom function or a more complex shared function stack that branches on email type. To be resolved during template implementation.
- Resend is a younger company than SendGrid or Postmark — reliability track record is shorter, current performance is strong
- Free tier limit of 100 emails/day means a sudden traffic spike could hit the cap. Acceptable for V1; revisit for paid plan before public launch.
- Sender domain reputation must be re-established in Resend (new SPF/DKIM/DMARC records)

## Consequences

- `sendgrid_basic_send` and `sendgrid_dynamic_send` Xano endpoints both refactored to call Resend (complete)
- SendGrid templates need to be re-created in Resend before SendGrid endpoints can be retired
- Per-email-type wrapper functions (or a unified router function) need to be designed — open question
- Resend API key stored in Xano environment variables (per Phase 2 secrets management work)
- Sender domain (`tomale.ai` or chosen subdomain) must be verified in Resend with SPF/DKIM/DMARC records
- Endpoint group naming to be updated from `integrations/sendgrid` to `integrations/resend`

## Related notes

- [[5-cto-implementation-plan|5-cto-implementation-plan]]
- [[6-api-security-model|6-api-security-model]]