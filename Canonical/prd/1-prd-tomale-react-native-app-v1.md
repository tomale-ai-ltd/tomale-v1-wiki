---
type: prd
title: 1-prd-tomale-react-native-app-v1
aliases:
  - "Tomale.ai Product & Technical Specification"
project: tomale-rn-v1
status: current
version: 1.0
date: 2025-06-01
last_verified: 2026-04-14
owner: vault
---

# Tomale.ai — Product & Technical Specification V1

## Core Mission
To build a love of reading in every child by putting them at the centre of the
learning experience.

## Primary Audience
- Parents with children aged 7 and under
- Primary education (EYFS / KS1)
- Private nurseries and childcare settings

## Problem Solved
Reading engagement in young people has fallen steadily since 2005. Reduced
engagement is linked to poor educational outcomes and increased mental health
risk. Children from deprived backgrounds are 4x more likely to fall behind
expected reading standards by age 5. Choice — not medium — is the largest
factor in engagement. Our core assumption: enabling children, families, and
educators to create bespoke stories at the relevant reading level will
encourage greater engagement.

## Unique Value Proposition
- Original stories created in minutes using custom characters
- Wide variety of narrative structures and image styles
- Characters reusable across multiple stories
- Stories linkable into sequels, prequels, or series
- Character model consistency retained across images within and across stories
- Hard copy ordering via print on demand in 2–3 days

---

## Feature Set & Scope

### User Authentication
| Feature | Version | Priority |
|---|---|---|
| Email / password login | MVP | Must Have |
| Session persistence via local storage | V1 | Must Have |
| Logout | MVP | Must Have |
| Password reset / magic link | MVP | Must Have |

### Onboarding
| Feature | Version | Priority |
|---|---|---|
| Walkthrough / tutorial | MVP | Must Have |
| Low-friction account creation | MVP | Must Have |

### User Profile
| Feature | Version | Priority |
|---|---|---|
| Account data (# stories, views) | V1 | Nice to Have |
| Settings — notifications | MVP | Must Have |

### Navigation
| Feature | Version | Priority |
|---|---|---|
| Quick create menu | MVP | Must Have |
| Subpage navigation | MVP | Must Have |
| Characters | MVP | Must Have |
| Bookshelf | MVP | Must Have |
| Library | V1 | Must Have |
| Store | V1 | Must Have |
| Settings / Help | MVP | Must Have |

### Stories
| Feature | Version | Priority |
|---|---|---|
| Create story — form based | MVP | Must Have |
| Select from themes / narrative structure | MVP | Must Have |
| Custom tags (topics) | V1 | Nice to Have |
| Select from artwork styles | MVP | Must Have |
| Create story — chatbot based | MVP | Must Have |
| Edit story | MVP | Must Have |
| Content moderation override | MVP | Must Have |
| E-reader in-app view | MVP | Must Have |
| Read to me mode | MVP | Must Have |
| Download / save as PDF | MVP | Must Have |
| Delete story | MVP | Must Have |
| Share / publish stories | V1 | Nice to Have |

### Characters
| Feature | Version | Priority |
|---|---|---|
| Create character — form based | MVP | Must Have |
| Create character — chatbot based | MVP | Must Have |
| Edit character | MVP | Must Have |
| Re-create image | MVP | Must Have |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React Native with Expo + Expo Router |
| Routing | File-based navigation via Expo Router |
| State / Auth | JWT via AsyncStorage + custom useAuth() |
| Backend | Xano (API builder, DB, auth) |
| Media Store | AWS S3 (via Xano vault) |
| Deployment | Expo Application Services (EAS) |
| Automation | Make.com (for OpenAI + DALL·E calls) |
| Versioning | GitHub + Cursor |

---

## App Architecture

| Area | Decision |
|---|---|
| Frontend Framework | React Native with Expo |
| Routing | Expo Router (structured routing) |
| Component Library | NativeBase |
| State Management | Zustand |
| Backend | Xano |
| Authentication | JWT-based auth via Xano |
| Storage (Media) | AWS S3 |
| Hosting (APIs) | Xano (serverless, globally deployed) |
| Persistent Client Storage | AsyncStorage |
| Dev Tools | Cursor (IDE), GitHub |
| Testing | Manual |
| CI/CD | EAS + GitHub |
| AI Text Generation | OpenAI ChatGPT 4o |
| AI Image Generation | OpenAI DALL·E 3 |

---

## Sections with detail in separate notes
The following sections exist in the PRD but are documented elsewhere in the vault:

- Navigation & Screen Design → [[1. Overview]]
- Data Model & Backend Schema → [[6. Backend - Xano]]
- Authentication & Session Management → [[7. Auth - Xano]]
- State Management Strategy → [[5. State Management - Zustand]]
- API Integration Design → [[6. Backend - Xano]]
- CI/CD & Release Strategy → [[12. CICD - EAS, GitHub]]
- Component Library & UI Design System → [[4. Frontend - UI]]
- Build Order / Slices → [[2-build-plan]]

---

## Related notes
- [[2-build-plan]]
- [[plan/cto-improvements]]
- [[Repos/tomale-rn-test/memory/data-model|data-model]]
- [[Repos/tomale-rn-test/memory/constitution|constitution]]