---
type: foundation
title: api-spec
project: tomale-rn-v1
status: current
date: 2026-04-14
---

---

# Xano API — Baseline Spec

## Summary

> ⚠️ MID-CTO-CHANGES BASELINE — This spec reflects the API as it existed part way through the CTO implementation plan.
> It is intentionally incomplete from a security perspective. Most endpoints listed as "auth: not required" will require authentication after Phase 1 is complete as per the [[Project/Plan/6-api-security-model|6-api-security-model]]
> 
> Note: Replace this file with a fresh export once Phase 1 and Phase 2 are done.
>
> See [[Project/Plan/6-api-security-model|6-api-security-model]] for the target state and [[cto-improvements-implementation-plan]] for the task breakdown and order of execution.

---
## auth

### auth/auth

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/auth/login` | Login and retrieve authentication token | not required |
| GET | `/auth/me` | Get user record for authentication token | **required** |
| POST | `/auth/refresh` | Refresh authentication token | not required |
| GET | `/auth/request_otp` | Generate temporary password and trigger email | not required |
| POST | `/auth/reset_password` | Reset user password | not required |
| POST | `/auth/signup` | Signup and retrieve authentication token | not required |
| POST | `/auth/submit_otp` | Check OTP submission vs OTP on user record | not required |

---

## content

Core CRUD operations for user-owned content.

### content/characters

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/characters` | Add characters record | **required** |
| GET | `/characters` | Query all characters records | **required** |
| GET | `/characters/{characters_id}` | Get characters record | **required** |
| DELETE | `/characters/{characters_id}` | Delete characters record | **required** |

### content/instant_stories

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/instant_stories` | Add instant stories record | **required** |
| GET | `/instant_stories` | Query all instant stories records | **required** |
| GET | `/instant_stories/{id}` | Get instant stories record | **required** |
| DELETE | `/instant_stories/{id}` | Delete instant stories record | **required** |

---

## ai pipeline

AI-powered generation endpoints. All authenticated except the image worker tick.

### ai pipeline/characters

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/characters/{id}/model` | Turn user prompt into standardised JSON character model via LLM | **required** |

### ai pipeline/conversations

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/conversations` | Create new chatbot conversation | **required** |
| GET | `/conversations` | Query all conversations records | **required** |
| GET | `/conversations/{conversations_id}` | Get conversations record | **required** |
| POST | `/conversations/{id}/message` | Append chat message to existing conversation | **required** |
| DELETE | `/conversations/{conversations_id}` | Delete conversations record | **required** |

### ai pipeline/instant_stories

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/instant_stories/{id}/model` | Turn user prompt into JSON story model via LLM | **required** |
| POST | `/instant_stories/{id}/cover_image` | Trigger creation of story cover image via LLM | **required** |
| POST | `/instant_stories/{id}/page_text` | Turn user prompt into JSON story page text via LLM | **required** |
| POST | `/instant_stories/{id}/page_image` | Trigger creation of story page images via LLM | **required** |

### ai pipeline/images

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/images/worker_tick` | Trigger worker to execute image_jobs | ⚠️ not required |

---

## commerce

### commerce/orders

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/orders` | Add orders record | ⚠️ not required |
| GET | `/orders` | Query all orders records | ⚠️ not required |
| GET | `/orders/{orders_id}` | Get orders record | ⚠️ not required |
| PATCH | `/orders/{orders_id}` | Edit orders record | ⚠️ not required |
| DELETE | `/orders/{orders_id}` | Delete orders record | ⚠️ not required |

### commerce/products

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/products` | Add product record | ⚠️ not required |
| GET | `/products` | Query all products | ⚠️ not required |
| GET | `/products/{products_id}` | Get product record | ⚠️ not required |
| PATCH | `/products/{products_id}` | Edit product record | ⚠️ not required |
| DELETE | `/products/{products_id}` | Delete product record | ⚠️ not required |

### commerce/shipping_options

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/shipping_options` | Add shipping option | ⚠️ not required |
| GET | `/shipping_options` | Query all shipping options | ⚠️ not required |
| GET | `/shipping_options/{shipping_options_id}` | Get shipping option | ⚠️ not required |
| PATCH | `/shipping_options/{shipping_options_id}` | Edit shipping option | ⚠️ not required |
| DELETE | `/shipping_options/{shipping_options_id}` | Delete shipping option | ⚠️ not required |

### commerce/subscriptions

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/subscriptions` | Add subscription | ⚠️ not required |
| GET | `/subscriptions` | Query all subscriptions | ⚠️ not required |
| GET | `/subscriptions/{subscriptions_id}` | Get subscription | ⚠️ not required |
| PATCH | `/subscriptions/{subscriptions_id}` | Edit subscription | ⚠️ not required |
| DELETE | `/subscriptions/{subscriptions_id}` | Delete subscription | ⚠️ not required |

### commerce/transaction_webhook_events
> ⚠️ Internal logging only — delete endpoints per CTO plan

| Method | Endpoint | Auth |
|---|---|---|
| POST | `/transaction_webhook_events` | ⚠️ not required |
| GET | `/transaction_webhook_events` | ⚠️ not required |
| GET | `/transaction_webhook_events/{id}` | ⚠️ not required |
| PATCH | `/transaction_webhook_events/{id}` | ⚠️ not required |
| DELETE | `/transaction_webhook_events/{id}` | ⚠️ not required |

### commerce/transactions
> ⚠️ Internal logging only — delete endpoints per CTO plan

| Method | Endpoint | Auth |
|---|---|---|
| POST | `/transactions` | ⚠️ not required |
| GET | `/transactions` | ⚠️ not required |
| GET | `/transactions/{transactions_id}` | ⚠️ not required |
| PATCH | `/transactions/{transactions_id}` | ⚠️ not required |
| DELETE | `/transactions/{transactions_id}` | ⚠️ not required |

---

## integrations

All integration endpoints currently unauthenticated — webhooks require signature
validation per CTO plan.

### integrations/hpbc

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| POST | `/hpbc/webhook_order_submission` | Triggered when payment confirmed via store order | ⚠️ not required |
| POST | `/hpbc/webhook_statusCallbackUrl` | Triggered when order status changes | ⚠️ not required |
| POST | `/hpbc/webhook_statusCallbackUrl_Error` | Triggered when order status change errors | ⚠️ not required |

### integrations/stripe

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/stripe/create_checkout_session` | Create Stripe checkout session | **required** |
| GET | `/stripe/check_order_paid` | Check if order has been paid | ⚠️ not required |
| POST | `/stripe/webhook_payment_confirmation` | Stripe payment confirmation webhook | ⚠️ not required |

### integrations/sendgrid

| Method | Endpoint | Summary | Auth | Params |
|---|---|---|---|---|
| POST | `/sendgrid/dynamic-send` | Send email from Xano via SendGrid | ⚠️ not required | to_email, template_id, data |
| POST | `/sendgrid/validate` | Validate SendGrid is working | ⚠️ not required | to_email, subject, body |

### integrations/stability

| Method | Endpoint | Summary | Auth | Params |
|---|---|---|---|---|
| POST | `/stability/generate_image` | Send image generation request | ⚠️ not required | prompt, instant_stories_id |

---

## system

Reference/lookup data. All currently unauthenticated — target state is read-only
for authenticated users, no write endpoints exposed.

### system/artwork_style

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/artwork_style` | Query all artwork styles | ⚠️ not required |
| GET | `/artwork_style/{artwork_style_id}` | Get artwork style record | ⚠️ not required |
| POST | `/artwork_style` | Add artwork style | ⚠️ not required |
| PATCH | `/artwork_style/{artwork_style_id}` | Edit artwork style | ⚠️ not required |
| DELETE | `/artwork_style/{artwork_style_id}` | Delete artwork style | ⚠️ not required |

### system/themes

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/themes` | Query all themes | ⚠️ not required |
| GET | `/themes/{themes_id}` | Get theme record | ⚠️ not required |
| POST | `/themes` | Add theme | ⚠️ not required |
| PATCH | `/themes/{themes_id}` | Edit theme | ⚠️ not required |
| DELETE | `/themes/{themes_id}` | Delete theme | ⚠️ not required |

### system/activities

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/activities` | Query all activities records | ⚠️ not required |
| GET | `/activities/{activities_id}` | Get activities record | ⚠️ not required |
| POST | `/activities` | Add activities record | ⚠️ not required |
| PATCH | `/activities/{activities_id}` | Edit activities record | ⚠️ not required |
| DELETE | `/activities/{activities_id}` | Delete activities record | ⚠️ not required |

### system/fact

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/fact` | Query all fact records | ⚠️ not required |
| GET | `/fact/{fact_id}` | Get fact record | ⚠️ not required |
| POST | `/fact` | Add fact record | ⚠️ not required |
| PATCH | `/fact/{fact_id}` | Edit fact record | ⚠️ not required |
| DELETE | `/fact/{fact_id}` | Delete fact record | ⚠️ not required |

---

## users

### users/users

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/users` | Query all users records | ⚠️ not required |
| GET | `/users/{users_id}` | Get users record | ⚠️ not required |
| POST | `/users` | Add users record | ⚠️ not required |
| PATCH | `/users/{users_id}` | Edit users record | ⚠️ not required |
| DELETE | `/users/{users_id}` | Delete users record | ⚠️ not required |
| PATCH | `/users/{users_id}/image` | Edit user profile image | ⚠️ not required |
| POST | `/users/{users_id}/bool_email_alerts` | Edit email alerts preference | ⚠️ not required |
| POST | `/users/{users_id}/bool_email_verified` | Edit email verified status | ⚠️ not required |
| POST | `/users/{users_id}/bool_notifications` | Edit notifications preference | ⚠️ not required |
| POST | `/users/{users_id}/bool_onboarding` | Edit onboarding status | ⚠️ not required |
| POST | `/users/{users_id}/bool_subscription` | Edit subscription status | ⚠️ not required |

### users/user_activities

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/user_activities` | Query all user activities | ⚠️ not required |
| GET | `/user_activities/{user_activities_id}` | Get user activities record | ⚠️ not required |
| POST | `/user_activities` | Add user activities record | ⚠️ not required |
| PATCH | `/user_activities/{user_activities_id}` | Edit user activities record | ⚠️ not required |
| DELETE | `/user_activities/{user_activities_id}` | Delete user activities record | ⚠️ not required |

### users/user_alerts

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/user_alerts` | Query all user alerts | ⚠️ not required |
| GET | `/user_alerts/{user_alerts_id}` | Get user alert | ⚠️ not required |
| POST | `/user_alerts` | Add user alert | ⚠️ not required |
| PATCH | `/user_alerts/{user_alerts_id}` | Edit user alert | ⚠️ not required |
| DELETE | `/user_alerts/{user_alerts_id}` | Delete user alert | ⚠️ not required |
| POST | `/user_alerts/broadcast` | Publish system alert to all users | ⚠️ not required |
| POST | `/user_alerts/mark-all-read` | Mark all user alerts as read in bulk | ⚠️ not required |

### users/support_requests

| Method | Endpoint | Summary | Auth |
|---|---|---|---|
| GET | `/support_requests` | Query all support requests | ⚠️ not required |
| GET | `/support_requests/{support_requests_id}` | Get support request | ⚠️ not required |
| POST | `/support_requests` | Add support request | ⚠️ not required |
| PATCH | `/support_requests/{support_requests_id}` | Edit support request | ⚠️ not required |
| DELETE | `/support_requests/{support_requests_id}` | Delete support request | ⚠️ not required |

---

## Summary

| Group | Subgroup | Endpoints | Auth status |
|---|---|---|---|
| auth | auth | 7 | Mixed — only `/auth/me` requires auth |
| content | characters | 4 | ✅ All authenticated |
| content | instant_stories | 4 | ✅ All authenticated |
| ai pipeline | characters | 1 | ✅ Authenticated |
| ai pipeline | conversations | 5 | ✅ All authenticated |
| ai pipeline | instant_stories | 4 | ✅ All authenticated |
| ai pipeline | images | 1 | ⚠️ Not authenticated |
| commerce | orders | 5 | ⚠️ None authenticated |
| commerce | products | 5 | ⚠️ None authenticated |
| commerce | shipping_options | 5 | ⚠️ None authenticated |
| commerce | subscriptions | 5 | ⚠️ None authenticated |
| commerce | transaction_webhook_events | 5 | ⚠️ Delete per CTO plan |
| commerce | transactions | 5 | ⚠️ Delete per CTO plan |
| integrations | hpbc | 3 | ⚠️ Needs signature validation |
| integrations | stripe | 3 | Mixed — only checkout requires auth |
| integrations | sendgrid | 2 | ⚠️ Not authenticated |
| integrations | stability | 1 | ⚠️ Not authenticated |
| system | artwork_style | 5 | ⚠️ None authenticated |
| system | themes | 5 | ⚠️ None authenticated |
| system | activities | 5 | ⚠️ None authenticated |
| system | fact | 5 | ⚠️ None authenticated |
| users | users | 11 | ⚠️ None authenticated |
| users | user_activities | 5 | ⚠️ None authenticated |
| users | user_alerts | 7 | ⚠️ None authenticated |
| users | support_requests | 5 | ⚠️ None authenticated |

**Total endpoints: ~102**
**Currently authenticated: ~19 (content, ai pipeline, stripe checkout)**
**Target after Phase 1: all non-webhook endpoints require authentication**

---

## Related notes

- [[Project/Plan/6-api-security-model|6-api-security-model]]
- [[Project/Plan/5-cto-implementation-plan|5-cto-implementation-plan]]
- [[Project/Plan/3-cto-tech-review|3-cto-tech-review]]
- [[Project/Stack/6. Backend - Xano|6. Backend - Xano]]

