---
type: decision
title: defer-stripe-webhook-mode-branching-to-phase-2
date: 2026-05-07
status: current
project: tomale-rn-v1
---

---

# Decision: replace-sendgrid-with-resend-for-transactional-email

## What we decided

To replace SendGrid with Resend as the transactional email provider for Tomale V1, and to scope email handling cleanly into transactional vs marketing.

**Transactional email (Resend):**
All app-triggered emails — sign up / email validation, password reset / OTP, subscription confirmation, book order confirmation / update / shipping, support ticket acknowledgements, content moderation alerts.

**Marketing email (HubSpot Marketing):**
Newsletters, product announcements, lifecycle / re-engagement campaigns, and any segmented broadcast email.

Both Resend sending endpoints have been migrated:

- `sendgrid_basic_send` refactored to call Resend's API
- `sendgrid_dynamic_send` refactored to use Resend's templates feature (template selected via object containing template ID + variables object)

Once SendGrid templates have been recreated in Resend and all callsites verified, the public Resend send endpoints will be converted to internal Xano custom functions and the endpoint group renamed from `integrations/sendgrid` to `integrations/resend`.

## Why

- SendGrid disabled its free plan following the Twilio acquisition, making continued use cost-prohibitive for V1 volume
- Resend's free tier (3,000 emails/month, 100/day) comfortably covers V1 launch needs
- Resend supports stored templates (confirmed working) — removes the need to inline HTML in Xano or build a separate rendering layer
- All transactional sends in V1 are server-triggered from inside Xano (in response to user actions or webhook events). No external system needs to call the send endpoints, so they can be internal-only — reducing public API surface per CTO plan section 2.5
- Marketing email is a separate concern with different requirements (subscription/unsubscribe, segmentation, broadcast scheduling) — HubSpot Marketing Email is purpose-built for this and already in place

## Alternatives considered

**HubSpot Transactional Email add-on** — rejected: paid add-on, disproportionate cost for V1 volume.

**HubSpot Marketing Email for transactional sends** — rejected: wrong tool, marketing compliance flows interfere with critical user journeys (OTPs, password resets).

**Postmark** — rejected: gold-standard deliverability but no meaningful free tier.

**AWS SES** — rejected: heavier setup (sandbox lifting, suppression lists, domain verification) not warranted for V1 volume.

**SendGrid paid plan** — rejected: ~$20/month minimum despite negligible V1 volume; migration to a more modern provider preferable to paying for a legacy integration.

**Inline HTML templates stored in Xano** — considered but unnecessary once Resend's templates feature was confirmed working.

**Keeping send endpoints public with shared-secret auth (for Make.com webhooks)** — rejected: Make.com is not part of V1 scope. The website "get access" entry point is replaced by App Store downloads and the existing HubSpot form. No external system needs to trigger transactional sends.

## Trade-offs accepted

- Resend's template selection model (template ID + variables object) means each email type may require a separate custom function or a shared router function that branches on email type. To be resolved during template implementation.
- Resend is younger than SendGrid or Postmark — shorter reliability track record, though current performance is strong
- Free tier limit of 100 emails/day means a sudden traffic spike could hit the cap. Acceptable for V1; revisit before public launch.
- Sender domain reputation must be re-established in Resend (new SPF / DKIM / DMARC records)
- SendGrid templates need to be recreated in Resend before the SendGrid endpoints can be retired

## Consequences

- `sendgrid_basic_send` and `sendgrid_dynamic_send` Xano endpoints both refactored to call Resend (complete)
- All callsites of these endpoints to be audited — none should be HTTP self-calls within Xano; in-app flows already use purpose-built endpoints (`/auth/request_otp` etc.)
- Once audit is clean, both endpoints to be converted to internal Xano custom functions and removed from the public API
- Endpoint group to be renamed `integrations/sendgrid` → `integrations/resend`
- SendGrid templates to be recreated in Resend
- Sender domain (`tomale.ai` or chosen subdomain) must be verified in Resend with SPF / DKIM / DMARC records before public launch
- Resend API key stored in Xano environment variables (per Phase 2 secrets management work)
- Make.com is confirmed out of V1 scope — no webhook integration with the website is required

## Related notes

- [[5-cto-implementation-plan|5-cto-implementation-plan]]
- [[6-api-security-model|6-api-security-model]]