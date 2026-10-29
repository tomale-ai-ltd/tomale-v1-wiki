---
type: prd
title: PRD-Chatbot-Story-Conversations
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-story-chatbot
  - F-story-create
related:
  - "[[story-creation-flow]]"
  - "[[v1-feature-map]]"
  - "[[PRD-Parental-Oversight-Content-Approval]]"
---

# 📘 PRD: Chatbot-Driven Story Creation

> **Changes in 2.0 (B9, 29/10/2026):**
> - Live `conversations` table and endpoints replace `story_conversations`.
> - The status lifecycle is the live one (Draft → Preparing → In Queue → Done, Blocked on a moderation fail).
> - No `user_id` in requests; the story belongs to the creating profile.
> - Stories are 12 pages (13 images).
> - Generation takes 10–15 minutes, so the UI waits and an alert announces completion.
> - The entitlement limit is handled from day one ([[gate-image-generation-with-entitlements-at-story-creation]]).
> - Parental approval applies.
> - Custom tags and the separate form are out of V1.
> - Reviewed with Kyle (29/10): email verification first, a Story builder for drafts, child-safe limit handling, a context-aware chatbot prompt from `data_models`, backend prep listed.
> - Phonics focus added (Kyle, 29/10, [[add-phonics-focus-to-story-creation]]): an optional phase and stage choice that shapes the story text; no progress tracking.
>
> Slice 200 / expected speckit 008 ([[roadmap]] M4).

## 1. Overview
We are replacing the legacy CRUD-style "Create Story" flow (6.1.1–6.1.5 in Adalo) with a conversational chatbot workflow. The chatbot guides the user through story setup (title idea, theme, characters, artwork style) using the profile's existing characters and the theme and art-style catalogues, then hands over to the generation pipeline.

This feature will:
- Provide a more natural, engaging UX.
- Store progress in `instant_stories` (status lifecycle) and the conversation in `conversations`.
- Let the AI propose structured suggestions (characters, themes, art styles) as cards the user accepts or rejects.

## 2. Goals
- ✅ Replace multi-step CRUD forms with a **single chat-based flow** (UI cards handle most choices).
- ✅ Keep users engaged while they keep control of the final details.
- ✅ Save progress incrementally and allow resuming.
- ✅ Make the long generation wait pleasant and clear.
- ✅ Respect plan limits, moderation and parental approval.

## 3. Scope
### In-Scope
- Chat UI screen in RN (`(main)/create-story/chat.tsx`).
- Conversation persistence (`conversations`, `conversation_type = story`).
- AI replies with text plus structured suggestion cards.
- Selecting existing characters (shared by the household, [[share-characters-across-the-household]]), creating a new character (opens the Slice 100 form), selecting a theme and an art style (locked tiles for styles outside the plan, [[return-full-artwork-catalogue-with-locked-tiles]]).
- Generation hand-off and a waiting state; completion alert.
- **Email verified first:** creating a story needs a verified account email.
- **Story builder:** unfinished stories (Draft, with their conversation) are listed in a "Story builder" area on the create screen, so a user can pick one up later. The Bookshelf shows finished stories only.
- **Limits, child-safe:** see §6a.
- **Context-aware chatbot:** the system prompt comes from a `data_models` record and is filled with the household's context (§5a).
- **Phonics focus (optional):** the user picks a scheme, phase and stage from suggestion cards (or skips it). The story text then favours the graphemes taught up to that stage and includes that stage's tricky words (§5c). It's a creative setting only: no tracking or assessment of a child's progress ([[v2-backlog]]).
- Starting from a character: the "Create a story with this character" action on the Characters screen opens the chat with that character already selected ([[PRD-Characters]]).

### Out-of-Scope (V1)
- Custom tags (topics): the umbrella PRD's "Nice to Have"; no table exists.
- Multi-user collaborative creation.
- Conversation analytics (a normalised messages table).
- Vector search over large libraries (context is injected by Xano).
- 16- and 20-page stories (planning only).
- A separate form-based create flow: dropped, the chat's tap-cards cover it (Kyle, 29/10).

## 4. Data Model
### **instant_stories** (live)
- `status`: Draft → Preparing → In Queue → Done; `Blocked` when moderation fails ([[formalise-story-status-lifecycle]])
- `status_moderation`: Pass, Fail, Parental Approval, Pending
- `title`, `subtitle`, `user_prompt` (the plot the user describes), `synopsis`, `theme_id`, `artwork_style_id`, `total_pages`, `images_remaining`
- `users_id`, `user_profiles_id` (set server-side from the token), `data_models_id`
- `parental_approval_required`, `parent_approved`
- Characters linked through `instant_story_characters` (many-to-many; `generate_story_page_text` needs at least one)

### **conversations** (live)
- `id`, `users_id`, `conversation_type` (story | character), `instant_stories_id`, `characters_id`
- `chat_messages` (object: history and suggestions)
- `status`: active | complete | abandoned | failed
- `created_at`, `last_modified_at`, `is_deleted`, `deleted_at`

## 5. API Endpoints (`app` group)
- `POST /instant_stories` → create the draft (Draft).
- `POST /conversations` → start a conversation linked to the draft (optionally with pre-selected `characters_ids`).
- `POST /instant_stories/{id}/characters` → link existing characters to the story (to build, [[PRD-Characters]] §4); no character record is patched.
- `POST /conversations/{id}/message` → append the user's message (explicit inputs: `id`, `user_message`), return the assistant reply and suggestion cards.
- `GET /conversations/{conversations_id}` → resume.
- `DELETE /conversations/{conversations_id}` → abandon.
- `POST /instant_stories/{id}/model` → build the story model with the LLM and start generation (page text → moderation → images).
- `GET /instant_stories/{id}` → poll status.
- Page text and images are produced by the pipeline (`page_text`, `cover_image`, `page_image` endpoints exist for retries).

## 5a. Chatbot prompt and context
- A `data_models` record of a new type (e.g. `story-chat`) holds the chatbot's system prompt template, model settings and output schema, like the existing generation records. Prompts can then change without code changes, and versions can be tried on test stories.
- At each turn Xano fills the template with context:
  - **V1:** the active profile's name and whether it's a child (to pitch language), the household's characters (names and short descriptions), the theme and art-style catalogues (with locked styles marked), and the draft story so far.
  - **Nice to have (V1 if cheap):** recent story titles and themes, to suggest sequels or avoid repeats.
- Context stays minimal (names and creative content only), in line with the ICO Children's Code.

## 5b. Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** `instant_stories` (lifecycle, moderation, approval flags, `user_profiles_id`), `conversations`, `instant_story_characters`; endpoints `POST /instant_stories`, `POST/GET/DELETE /conversations`, `POST /conversations/{id}/message`, `POST /instant_stories/{id}/model`, pipeline endpoints.

**To build:**
1. **Chat orchestration** in `conversations/{id}/message`: load the `story-chat` record, build the context (§5a), return the reply plus suggestion cards, and apply chosen actions to the draft (theme, art style, characters, title idea).
2. **`data_models` record** of type `story-chat` (system prompt, model, output schema with a `suggestions` array).
3. **`POST /instant_stories/{id}/characters`** (shared with [[PRD-Characters]]).
4. **Email check:** `POST /instant_stories` and `POST /conversations` refuse an unverified account (400 `EMAIL_NOT_VERIFIED`).
5. **Entitlement gate** before generation in `instant_stories/{id}/model` (400 `ENTITLEMENT_LIMIT_REACHED`, with when the allowance resets). Until M8 this is a simple per-account monthly cap. Remaining allowance also returned when the chat starts, so the app can warn early.
6. **Story builder list:** `GET /instant_stories?status=Draft` (or a dedicated `GET /story_builder`) returning drafts with their conversation id, scoped like other stories.
7. **Old drafts:** decide a clean-up (e.g. drafts untouched for 90 days are soft-deleted).
8. **Phonics focus:** add `phonics_phase_stage_id` (int, nullable) to `instant_stories`, accepted while Draft; the generation step builds the phonics block from the up-to-stage functions; the `story-text` prompt gains an optional phonics section.
9. **Postman `_tests`:** unverified email refused; limit reached leaves the story in Draft; resume a draft; context record loads.; a story with a phonics stage includes the stage's tricky words in its generation prompt.

## 5c. Phonics focus
- **Live:** tables `phonics_scheme`, `phonics_scheme_phase`, `phonics_phase_stage`, `phonics_grapheme`, `phonics_exceptions` and their stage links; endpoints `GET /phonics/phonics_schemes` and `GET /phonics/phonics_schemes/{id}/stages`; functions `phonics_graphemes_up_to_stage` and `phonics_exceptions_up_to_stage` (and the per-stage versions).
- **Selection:** by the user, through suggestion cards in the chat (scheme → phase → stage, with plain-language labels such as "Phase 2: first sounds"). The chatbot may suggest it ("Would you like this story to practise some sounds?") but never chooses for the user. Skipping it leaves generation unchanged.
- **Generation:** `instant_stories/{id}/model` loads the graphemes and tricky words **up to** the chosen stage and adds a phonics block to the user prompt of the `story-text` record: use words built from these graphemes where possible, include these tricky words, keep sentences short. No automated decodability check in V1.
- **Display:** the story detail shows the phonics focus (e.g. "Phase 3, week 2"); the reader shows nothing extra.

## 6. Frontend Requirements
- **Chat UI:** text bubbles and suggestion cards (themes, characters, art styles). Needs an engaging, child-friendly component library: the choice is open, see §8.
- **Story builder:** list of unfinished stories (title so far, characters, last edited), tap to resume the chat.
- **Waiting screen** after hand-off: progress based on `images_remaining`, and "we'll let you know" so the user can leave.
- Zustand: `conversation.messages[]`, `draftStory` (synced with `instant_stories`).
- Route: `app/(main)/create-story/chat.tsx`.

## 6a. Limit reached
The story and its conversation are kept as a **Draft** in the Story builder, so nothing is lost.

- **Child profile:** a friendly lock card: "You've made lots of stories this month! New ones unlock on <date>." No prices and no purchase buttons. An **"Ask a grown-up"** button goes to the profile picker → PIN → the parent's plan screen, using the route-resume rule in [[PRD-Parental-Oversight-Content-Approval]] §8a.
- **Parent profile:** the same message with the upgrade options ([[PRD-Subscription-Entitlement-System]]).

Apple and Google both expect purchases in apps used by children to sit behind a parental gate, and no purchase prompts aimed at children. The PIN is that gate. Exact wording to check against the current App Store and Google Play family policies before launch.

## 7. User Flow
1. User selects **"Create Story"** → draft `instant_stories` record (Draft).
2. `POST /conversations` starts a conversation linked to the draft.
3. The user chats and taps cards; each choice updates the draft.
4. When the minimum fields are present, the user confirms → `POST /instant_stories/{id}/model`.
5. The backend checks entitlements (limit reached → story stays in the Story builder, §6a), generates text, runs moderation and queues 13 images.
6. Moderation outcome: Pass → normal; Parental Approval → finished but locked for the child until a parent approves; Fail → Blocked with a kind message.
7. On completion (Done) an in-app alert links to the story, which appears on the Bookshelf.

## 8. Open Questions
- **Component library** for the chat and cards: the constitution names NativeBase, which isn't installed and, as far as I know, is no longer maintained (its successor is gluestack-ui). Choose before Slice 100 (roadmap M1): gluestack-ui, Tamagui, React Native Paper, or custom components on Reanimated.
- Clean-up period for untouched drafts.

Resolved 29/10: email verification required before creating; full chat history kept per story; no separate form; the child's waiting view is settled in [[PRD-Parental-Oversight-Content-Approval]].
