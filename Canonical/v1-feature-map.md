---
type: living-doc
title: v1-feature-map
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
last_verified: 2026-10-28
owner: vault
related:
  - "[[roadmap]]"
  - "[[v1-audit]]"
  - "[[1-prd-tomale-react-native-app-v1]]"
---

# V1 feature map

One row per V1 feature: where it is specified, which slice builds it, which backend endpoints it uses, and how far it has got. The ids are the values used in the `features:` frontmatter of decisions and PRDs. Cross-cutting ids (`X-security`, `X-platform`, `X-testing`, `X-process`) are not features and are not listed here.

**Sources:** the `app` and `webhooks` groups in the Xano mirror (`Repos/tomale-xano`, synced 24/10/2026), [[Repos/tomale-rn-test/memory/data-model|data-model]] (generated 28/10), the app repo (`wip/pre-restructure-2026-10-24`) and [[v1-audit]]. Speckit numbers from 007 onwards are assigned when `/speckit.specify` runs; the ones below are the expected order, not yet created.

**Status key:** **Built** = backend done and covered by `_tests` · **Backend only** = endpoints exist, no app screens · **Partial** = some backend missing · **Not started**.

## Features

| Id | Feature | PRD | Slice / spec | Backend (endpoints in `app` unless noted) | Status | Key decisions |
|---|---|---|---|---|---|---|
| F-auth | Sign-up, login, verify email, magic link, refresh, logout | [[1-prd-tomale-react-native-app-v1]] | 000 (002 auth baseline, 006 HTTP client) | `auth/signup`, `auth/login`, `auth/me`, `auth/refresh`, `auth/verify_email`, `auth/request_magic_link`, `auth/complete_magic_link`, `auth/reset_password` | Backend built and tested. App: login and magic-link screens exist; SecureStore and the 401 interceptor not yet built | [[use-expo-secure-store-for-client-tokens]], [[use-axios-401-interceptor-for-client-auth-session-handling]], [[return-401-invalid-refresh-token-from-auth-refresh]], [[use-https-web-intermediary-for-magic-link-redirect]] |
| F-onboarding | Walkthrough, account creation | umbrella | not slotted | `users/me/complete_onboarding` | Backend only (app has an `(onboarding)` route stub) | — |
| F-account | Settings, preferences, username, support | umbrella | not slotted | `users/me` PATCH, `users/me/image`, `utilities/upload_image` | Backend only. **No account-deletion endpoint** (App Store requirement) | [[collapse-bool-preference-endpoints-into-users-me]], [[make-username-user-editable]], [[replace-support-requests-endpoint-with-mailto-ops-inbox]] |
| F-profiles | Household profiles, child profiles, avatars, PIN gate on switching | **none** (B9 writes one) | not slotted | `users/user_profiles` GET/POST, `users/user_profiles/{id}` PATCH/DELETE, `auth/select_profile` | Partial: profiles built; **PIN gate not built** | [[adopt-unified-user-profiles-table]], [[carry-active-profile-in-token-extras]], [[cap-profiles-at-one-adult-and-six-children]], [[use-bundled-preset-avatars-for-profiles]], [[parental-gate-on-profile-switch]] |
| F-notifications | In-app alerts inbox, deep links, transactional email | umbrella | not slotted | `user_alerts` GET, `user_alerts/{id}` GET/PATCH, `users/user_alerts/mark_all_read`; Resend functions | Backend only. Push deferred post-V1 | [[scope-user-alerts-as-in-app-inbox]], [[defer-push-notifications-until-post-v1]], [[use-per-build-variant-url-schemes]] |
| F-characters | Characters screen, create (form), view, delete | [[PRD-Characters]] | 100 → expected **007** | `characters` GET/POST, `characters/{id}` GET/DELETE, `characters/{id}/model` | Partial: account-scoped today; per-profile scoping and soft-delete clean-up needed before 007 | [[scope-characters-per-profile-with-soft-delete]], [[moderate-names-in-two-stages]] |
| F-character-chatbot | AI-assisted character creation | [[PRD-Chatbot-Create-Character]] | 500 | (reuses `conversations`, `characters/{id}/model`) | Not started | — |
| F-story-create | Themes, art styles, story setup | umbrella | part of 200 | `themes` GET, `artwork_style` GET (+ `{id}`), `instant_stories` POST | Backend only | [[return-full-artwork-catalogue-with-locked-tiles]] |
| F-story-chatbot | Chatbot story creation | [[PRD-Chatbot-Story-Conversations]] | 200 → expected **008** | `conversations` GET/POST, `conversations/{id}` GET/DELETE, `conversations/{id}/message` | Partial: message endpoint exists; chat orchestration and suggestion cards not built | — |
| F-story-generation | Story text and images, moderation, status lifecycle | none (architecture: [[story-creation-flow]], [[image-generation-flow]]) | background for 200 | `instant_stories/{id}/model`, `…/page_text`, `…/cover_image`, `…/page_image`; tasks `image_worker_tick`, `pdf_worker_tick` | Built (slow: 10–15 min per story, Phase 2) | [[formalise-story-status-lifecycle]], [[defer-image-pipeline-throughput-to-phase-2]], [[gate-image-generation-with-entitlements-at-story-creation]] |
| F-parental-oversight | Approval of sensitive stories | [[PRD-Parental-Oversight-Content-Approval]] | not slotted | flags on `instant_stories`; order gate in `store_orders` POST and checkout | Partial: **approve/reject flow not built** | [[per-child-story-visibility]], [[block-ordering-of-stories-awaiting-parental-approval]] |
| F-bookshelf | Bookshelf, story detail, e-reader, read-to-me | [[PRD-E-Reader]] | 300 → expected **009** | `instant_stories` GET, `instant_stories/{id}` GET/DELETE | Backend only. Reading progress (`reading_logs`) not built, and only in scope if cheap | [[split-list-and-detail-projections]], [[drop-library-and-pdf-download-from-v1]] |
| F-store | Store, checkout, order history, cancel | [[PRD-Store-Orders]] | 400 → expected **010** | `products`, `shipping_options` (+ `{id}`), `store_orders` GET/POST, `store_orders/{id}` GET/PATCH, `store_orders/{id}/cancel`, `stripe/create_checkout_session`, `stripe/check_order_paid` | Built and tested; e-reader preview and in-app checkout return are app work | [[use-e-reader-preview-before-order-payment]], [[return-from-stripe-checkout-via-in-app-browser-sheet]], [[delay-hpbc-submission-with-30-minute-cancellation-window]] |
| F-print-fulfilment | Print PDFs (Papermill), HPBC/Pureprint submission and callbacks | [[PRD-Order-PoD-System]] | background for 400 | `webhooks`: `hpbc/webhook_statusCallbackUrl`, `…_Error`; task `hpbc_submit_due_orders` | Built and tested (staging SKU) | [[make-hpbc-create-order-a-single-fail-closed-request]], [[enforce-forward-only-hpbc-callback-status-transitions]] |
| F-payments | Stripe payments, transactions, refunds, webhooks | [[PRD-transaction-webhooks-micro-prd]] | background for 400 | `webhooks`: `stripe/webhook_payment_confirmation`; tasks `reconcile_order_refunds`, `reconcile_stripe_customers` | Built for book orders; subscription events not handled | [[store-money-as-integer-minor-units]], [[split-refund-model-into-self-service-and-support-paths]], [[defer-stripe-webhook-mode-branching-to-phase-2]] |
| F-subscriptions | Tiers, entitlements, usage limits, in-app purchase | [[PRD-Subscription-Entitlement-System]] | not slotted (backend track, [[roadmap]]) | `subscriptions` GET (+ `{id}`) only | Not started | [[gate-image-generation-with-entitlements-at-story-creation]] |
| F-phonics | Phonics schemes and stages | **none** | not slotted | `phonics/phonics_schemes` GET, `…/{id}/stages` GET | Backend only. **V1 scope undecided** | — |

## Not in V1

- **Library** (the public, shared story library) and **downloadable PDFs**: [[drop-library-and-pdf-download-from-v1]].
- **Push notifications**: [[defer-push-notifications-until-post-v1]].
- **Story sharing and reviews**: [[remove-instant-story-reviews-endpoint]].

## Endpoints with no feature

`activities` GET and `fact/random` GET (home-screen content) belong to no PRD. They stay as small extras until a PRD claims them or they're removed.
