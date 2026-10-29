---
type: prd
title: 1-prd-tomale-react-native-app-v1
aliases:
  - "Tomale.ai Product & Technical Specification"
project: tomale-rn-v1
status: current
version: 2.0
date: 2025-06-01
last_verified: 2026-10-29
owner: vault
features:
  - F-auth
  - F-onboarding
  - F-account
  - F-profiles
  - F-notifications
  - F-characters
  - F-character-chatbot
  - F-story-create
  - F-story-chatbot
  - F-story-generation
  - F-parental-oversight
  - F-bookshelf
  - F-store
  - F-print-fulfilment
  - F-payments
  - F-subscriptions
related:
  - "[[v1-feature-map]]"
  - "[[roadmap]]"
  - "[[stack]]"
---

# Tomale.ai — Product & Technical Specification V1

> **Changes in 2.0 (B9, 29/10/2026):** feature tables updated:
> - **Added:** profiles, parental approval, subscriptions.
> - **Removed:** Library and PDF download.
> - **Moved post-V1:** push notifications and sharing.
>
> The tech stack and architecture tables are replaced by links to [[stack]], so they can't drift again. Status per feature lives in [[v1-feature-map]]; order and dates in [[roadmap]] (public UK launch targeted for late January 2027).
>
> **B9 review (29/10, with Kyle):** tables brought in line with the approved feature PRDs: iOS and Android at launch; subscriptions are Free and Creator through RevenueCat (Club is V2); AI character creation is in V1; a phonics focus in story creation (no tracking); edit story is V2; read-to-me uses generated narration; the form-based story create is dropped; everything deferred is listed in [[v2-backlog]].

## Core Mission
To build a love of reading in every child by putting them at the centre of the learning experience.

## Primary Audience
- Parents with children aged 7 and under
- Primary education (EYFS / KS1)
- Private nurseries and childcare settings

## Problem Solved
Reading engagement in young people has fallen steadily since 2005. Reduced engagement is linked to poor educational outcomes and increased mental health risk. Children from deprived backgrounds are 4x more likely to fall behind expected reading standards by age 5. Choice — not medium — is the largest factor in engagement. Our core assumption: enabling children, families, and educators to create bespoke stories at the relevant reading level will encourage greater engagement.

## Unique Value Proposition
- Original stories created in minutes using custom characters
- Wide variety of narrative structures and image styles
- Characters reusable across multiple stories
- Stories linkable into sequels, prequels, or series
- Character model consistency retained across images within and across stories
- Hard copy ordering via print on demand in 2–3 days

---

## Platforms
iOS and Android, launched together in the UK ([[roadmap]] M10).

## Feature Set & Scope

### User Authentication
| Feature | Version | Priority | PRD / note |
|---|---|---|---|
| Email / password login | MVP | Must Have | Built |
| Session persistence (secure storage, token refresh) | V1 | Must Have | [[use-expo-secure-store-for-client-tokens]] |
| Logout | MVP | Must Have | |
| Password reset / magic link | MVP | Must Have | Built |
| Account deletion | V1 | Must Have | App Store requirement; to build ([[roadmap]] M7) |
| Email verification before creating | V1 | Must Have | [[PRD-Chatbot-Story-Conversations]] |

### Onboarding
| Feature | Version | Priority |
|---|---|---|
| Walkthrough / tutorial | MVP | Must Have |
| Low-friction account creation | MVP | Must Have |
| Verify email → name the parent profile → set PIN → add children | V1 | Must Have |

### Profiles
| Feature | Version | Priority | PRD / note |
|---|---|---|---|
| Household profiles (1 adult, up to 6 children) | V1 | Must Have | [[PRD-Profiles]] |
| Avatars: presets or a household character image | V1 | Must Have | [[PRD-Profiles]] |
| PIN to switch from a child to a parent profile | V1 | Must Have | [[PRD-Profiles]] |

### Account & Settings
| Feature | Version | Priority |
|---|---|---|
| Account data (# stories, views) | V1 | Nice to Have |
| Preferences (email opt-in) | MVP | Must Have |
| In-app alerts inbox | V1 | Must Have |
| Transactional emails (orders, approvals) | V1 | Must Have |
| Push notifications | V2 | — |

### Navigation
| Feature | Version | Priority |
|---|---|---|
| Quick create menu | MVP | Must Have |
| Subpage navigation | MVP | Must Have |
| Characters | MVP | Must Have |
| Bookshelf | MVP | Must Have |
| Store | V1 | Must Have |
| Settings / Help | MVP | Must Have |
| Library (public story library) | V2 | — |

### Stories
| Feature | Version | Priority | PRD / note |
|---|---|---|---|
| Create story — chatbot based (with suggestion cards) | MVP | Must Have | [[PRD-Chatbot-Story-Conversations]] |
| Select from themes / narrative structure | MVP | Must Have | |
| Select from artwork styles | MVP | Must Have | Locked tiles by plan |
| Story builder (resume drafts) | V1 | Must Have | [[PRD-Chatbot-Story-Conversations]] |
| Create story — form based | — | Dropped | The chat's tap-cards cover it (Kyle, 29/10) |
| Custom tags (topics) | V2 | — | [[v2-backlog]] |
| Phonics focus (optional phase and stage choice) | V1 | Should Have | [[PRD-Chatbot-Story-Conversations]] §5c; no progress tracking |
| Edit story | V2 | — | [[v2-backlog]] (Kyle, 29/10) |
| Parental approval of sensitive stories | MVP | Must Have | [[PRD-Parental-Oversight-Content-Approval]] |
| E-reader in-app view | MVP | Must Have | [[PRD-E-Reader]] |
| Read to me mode (generated narration) | MVP | Must Have | [[PRD-E-Reader]] |
| Delete story | MVP | Must Have | |
| Download / save as PDF | — | Dropped | [[drop-library-and-pdf-download-from-v1]] |
| Share / publish stories | V2 | — | [[v2-backlog]] |

### Characters
| Feature | Version | Priority | PRD / note |
|---|---|---|---|
| Create character — form based | MVP | Must Have | [[PRD-Characters]] |
| Create character — chatbot based | V1 | Must Have | [[PRD-Chatbot-Create-Character]] (Slice 500, M6a; voice input flagged) |
| Shared across the household; favourites | V1 | Must Have | [[PRD-Characters]] |
| Re-create image | V1 | Must Have | [[PRD-Characters]]; counts against the monthly character image limit |
| Edit character name or description | V2 | — | [[v2-backlog]] |

### Store & Subscriptions
| Feature | Version | Priority | PRD / note |
|---|---|---|---|
| Order a printed book: A4 landscape paperback or hardback (preview, checkout, history, cancel) | V1 | Must Have | [[PRD-Store-Orders]], [[PRD-Order-PoD-System]] |
| Subscriptions: Free and Creator (monthly, annual, 1-month trial) | V1 | Must Have | [[PRD-Subscription-Entitlement-System]] |
| Club (monthly printed book) | V2 | — | [[v2-backlog]] |
| Billing events (Stripe for books; RevenueCat for Apple and Google subscriptions) | V1 | Must Have | [[PRD-transaction-webhooks-micro-prd]] |

---

## Tech Stack & Architecture
See [[stack]] (layers, versions, status), [[backend-xano]] and [[security-model]]. These replace the April tables, which had drifted (AsyncStorage tokens, Make.com, DALL·E 3, S3 via Xano).

## Sections with detail in separate notes
- Feature status → [[v1-feature-map]]
- Deferred from V1 → [[v2-backlog]]
- Build order and launch plan → [[roadmap]]
- Data model and backend → [[backend-xano]] and the generated [[Repos/tomale-rn-test/memory/data-model|data-model]]
- Authentication, access and API rules → [[security-model]]
- Observability → [[observability]]
- Tests → [[test-suite]]
- Before launch → [[pre-launch-checklist]]

## Related notes
- [[roadmap]]
- [[v1-feature-map]]
- [[Repos/tomale-rn-test/memory/constitution|constitution]]
