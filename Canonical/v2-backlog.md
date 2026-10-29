---
type: living-doc
title: v2-backlog
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-29
last_verified: 2026-10-29
owner: vault
related:
  - "[[v1-feature-map]]"
  - "[[roadmap]]"
---

# V2 backlog

Everything deliberately left out of V1, in one place. A PRD's "Out of scope" section says *what* is excluded; this list is where those items wait. When an item is picked up, it moves into a PRD and the [[roadmap]]; when one is dropped for good, it's struck through here with the reason.

Grouped by feature id from [[v1-feature-map]]. **Why later** gives the reason or the thing it waits on.

## Stories and images
| Item | Feature | Why later | Source |
|---|---|---|---|
| Regenerate a story's images after creation (before ordering) | F-story-generation | Waits for the cheaper image pipeline (SDXL on AWS) and character/style training | Kyle 29/10, [[PRD-Order-PoD-System]] |
| Character and style training (LoRA / IP-adapter) for consistency | F-story-generation | Image pipeline track | [[roadmap]] §6 |
| Edit a story | F-story-create | Not specified; needs moderation on edit | [[1-prd-tomale-react-native-app-v1]] |
| Custom tags (topics) | F-story-chatbot | No table; Nice to Have | [[PRD-Chatbot-Story-Conversations]] |
| 16- and 20-page stories | F-story-chatbot | Planning only in V1 | [[PRD-Chatbot-Story-Conversations]] |
| Multi-user collaborative creation | F-story-chatbot | — | [[PRD-Chatbot-Story-Conversations]] |
| Conversation analytics (normalised messages table) | F-story-chatbot | — | [[PRD-Chatbot-Story-Conversations]] |
| Vector search over large libraries | F-story-chatbot | Context injected by Xano is enough for V1 | [[PRD-Chatbot-Story-Conversations]] |
| Public Library and story sharing, ratings | F-bookshelf | [[drop-library-and-pdf-download-from-v1]], [[remove-instant-story-reviews-endpoint]] | [[v1-feature-map]] |
| Join tables for per-child story visibility | F-bookshelf | Single `user_profiles_id` per story; revisit with sharing | [[roadmap]] §5 (CTO #29) |

## Reader
| Item | Feature | Why later | Source |
|---|---|---|---|
| Word-level highlighting synced to narration | F-bookshelf | — | [[PRD-E-Reader]] |
| Downloads, PDFs, offline audio | F-bookshelf | [[drop-library-and-pdf-download-from-v1]] | [[PRD-E-Reader]] |
| Custom fonts and advanced accessibility options | F-bookshelf | — | [[PRD-E-Reader]] |
| Server-side reading progress and stats (`reading_logs`) | F-bookshelf | Device storage is enough for V1 | [[PRD-E-Reader]] |
| Toniebox / external devices | F-bookshelf | — | [[PRD-E-Reader]] |

## Characters
| Item | Feature | Why later | Source |
|---|---|---|---|
| Edit a character's name or description | F-characters | Needs moderation on edit; re-create image covers visual changes | [[PRD-Characters]] |
| Character sharing / export | F-characters | — | [[PRD-Characters]] |
| AI-assisted editing of an existing character | F-character-chatbot | — | [[PRD-Chatbot-Create-Character]] |
| Multi-character relationships (family trees) | F-character-chatbot | — | [[PRD-Chatbot-Create-Character]] |
| Voice input for character creation (502), if cut from M6a | F-character-chatbot | First to cut if the date is at risk | [[roadmap]] |

## Profiles and oversight
| Item | Feature | Why later | Source |
|---|---|---|---|
| A distinct child UI (instead of locked areas) | F-profiles | V1 greys out parent-only areas | [[PRD-Profiles]] |
| Multiple adults; promote a child; delete the primary profile | F-profiles | — | [[PRD-Profiles]] |
| Restore a deleted profile | F-profiles | Stories move to the primary profile instead | [[PRD-Profiles]] |
| Per-profile plans or entitlements | F-profiles | Plans are account-level | [[PRD-Profiles]] |
| "Last used profile" on login | F-profiles | Fresh login lands on the primary profile | [[PRD-Profiles]] |
| Photos as avatars | F-profiles | Children's data minimisation | [[PRD-Profiles]] |
| Editing a story before approving it | F-parental-oversight | Approve or reject only in V1 | [[PRD-Parental-Oversight-Content-Approval]] |
| Approve from email (approval tokens) | F-parental-oversight | Approval only in the app, behind the PIN | [[PRD-Parental-Oversight-Content-Approval]] |

## Store and print
| Item | Feature | Why later | Source |
|---|---|---|---|
| **Club tier** (£20/month, a monthly A4 paperback at £0 with free standard shipping, 25% off extra books) | F-subscriptions, F-store | App Store rules on bundling a physical book with a digital subscription are unclear. Option to test: sell Club on the website (Stripe) as a book subscription that includes Creator, relying on the multiplatform rule (3.1.3(b)); ask App Review first. Needs £0 orders that skip Stripe | [[PRD-Subscription-Entitlement-System]], Kyle 29/10 |
| Library orders (8.3 series) | F-store | Library is post-V1 | [[PRD-Store-Orders]] |
| Teacher / classroom publishing | F-store | — | [[PRD-Store-Orders]] |
| Stripe subscriptions (web purchase, webhook branching on `mode`) | F-payments | Only needed for Club or web sign-up | [[defer-stripe-webhook-mode-branching-to-phase-2]] |
| Bulk orders | F-print-fulfilment | — | [[PRD-Order-PoD-System]] |
| Returns logistics; customer support tooling | F-print-fulfilment | Support handles by hand in V1 | [[PRD-Order-PoD-System]] |

## Platform
| Item | Feature | Why later | Source |
|---|---|---|---|
| Push notifications | F-notifications | [[defer-push-notifications-until-post-v1]] | [[v1-feature-map]] |
| Phonics progress tracking and assessment (per child, through a scheme) | F-phonics | V1 only uses phonics to shape story text; keeps V1 out of edtech | [[add-phonics-focus-to-story-creation]] |
| Automated decodability check on generated text | F-phonics | Prompt-only in V1 | [[PRD-Chatbot-Story-Conversations]] |
