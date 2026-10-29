---
type: prd
title: PRD-Chatbot-Create-Character
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-character-chatbot
related:
  - "[[PRD-Characters]]"
  - "[[PRD-Chatbot-Story-Conversations]]"
  - "[[v1-feature-map]]"
---

# 📘 PRD: Create Character (10.2.1)

> **Changes in 2.0 (B9, 29/10/2026):** uses the live `conversations` table and endpoints (not `story_conversations`); no `user_id` in requests; the chatbot works from the character data model and asks Q&A or tap/swipe questions (Kyle, 29/10); the Slice 100 form is the fallback; household-wide characters and name moderation from [[PRD-Characters]]; image generation counts against entitlements. Slice 500, after story creation is stable ([[roadmap]]).
>
> **B9 review (29/10, approved by Kyle):** in the January launch as milestone M6a ([[include-ai-character-creation-in-v1]]); the image is generated once, after saving (no draft image in the chat); re-creation uses the character's "re-create image" and counts against the monthly character image limit (Free 4, Creator 30), so there's no per-character cap; email verification is required (as for story chat); the chat prompt lives in a `character-chat` `data_models` record; user messages are moderated; voice input needs speech-to-text, not `expo-speech`; archive exists (the earlier "soft delete only" note was wrong); backend prep added.

## 1. Overview
The Slice 100 create flow is a simple form (name, description). This feature adds an **AI-assisted, child-friendly character builder** that turns natural language (typed or spoken) and simple tap/swipe choices into the structured character model and a generated cover image. It reuses the story chatbot's chat UI and the `conversations` backend.

## 2. Goals
- ✅ Offer a chatbot alongside the form (the form stays as the fallback).
- ✅ Know the character data model and fill it in: ask follow-up questions in plain language, or present quick choices (hair length, eye shape, clothing) as tap/swipe options.
- ✅ Support optional voice dictation for children.
- ✅ Generate the character image on save; re-create it later within the monthly character image limit ([[PRD-Subscription-Entitlement-System]]).
- ✅ Child safety: each user message moderated; name and description moderated on save; the bot never asks for personal data (real names, school, location, photos).
- ✅ Save to `characters` and update the global cache.

## 3. Scope
### In-Scope
- Chat flow for creating characters (`conversation_type = character`).
- Draft attribute model built up turn by turn, with a preview card.
- Quick-choice chips for attribute values (from the attribute schema).
- Persist the approved character with `POST /characters`, which queues the image job (the "picture on its way" state from [[PRD-Characters]]).
- Re-create the image afterwards from the character page (`POST /characters/{id}/regenerate_image`).
- Voice input behind a feature flag (502).

### Out-of-Scope (V1)
- AI-assisted editing of an existing character.
- Multi-character relationships (family trees, etc.).
- Offline creation.

## 4. Data Model
### **characters** (see [[PRD-Characters]] §4)
Attribute groups the chatbot fills: `name`, `physical_description`, `primary_attributes` (age, category, subcategory, gender, ethnicity), `face_attributes` (shape, nose, cheeks), `eyes_attributes` (colour, shape, size), `hair_attributes` (colour, length, style), `clothing_attributes` (headgear, top, bottom, shoes, accessories). Shared across the household ([[share-characters-across-the-household]]).

### **conversations** (live)
- `id`, `users_id`, `conversation_type` (story | character), `characters_id`, `instant_stories_id`
- `chat_messages` (object: message history and the draft model)
- `status` (active | complete | abandoned | failed)
- `created_at`, `last_modified_at`, `is_deleted`, `deleted_at`

## 5. API Endpoints (`app` group)
- `POST /conversations` → start a character conversation.
- `GET /conversations/{conversations_id}` → resume.
- `POST /conversations/{id}/message` → append a user message (explicit inputs: `id`, `user_message`), returns the assistant reply plus suggested quick choices.
- `POST /characters/{id}/model` → structured model from free text.
- `POST /characters` → save; name moderation; queues the image job.
- `DELETE /conversations/{conversations_id}` → abandon.

The chat orchestration (system prompt built from the attribute schema, quick-choice generation) is to build; the endpoints above exist.

## 5a. Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** `conversations` (`conversation_type` story | character, `chat_messages`, status), the conversation endpoints, `POST /characters/{id}/model`, `POST /characters`, name moderation, the character image job.

**To build:**
1. **`data_models` record** of a new type `character-chat`: system prompt built from the character attribute schema (`output_schema` = the attribute groups and their allowed values), tone (warm, simple, short questions), the rule to never ask for personal data, and model settings.
2. **Message handler for `conversation_type = character`:** each turn moderates the user message, updates the draft model in `chat_messages`, and returns the reply plus `quick_choices` (attribute key and allowed values) for the next missing attribute. Same LLM wrapper and `token_usage` logging as story chat.
3. **Completion:** when required attributes are filled, return `ready: true` and the preview; on confirm the app calls `POST /characters` with the model and `conversations_id`; the conversation becomes `complete` with `characters_id` set.
4. **Gates:** `POST /conversations` already refuses an unverified email (`EMAIL_NOT_VERIFIED`, [[PRD-Chatbot-Story-Conversations]]); `POST /characters` runs the character image entitlement check (`ENTITLEMENT_LIMIT_REACHED`) before saving, so a child or parent at the limit is told before the chat finishes. Add `GET /me/entitlements` to the start of the chat so the app can warn up front.
5. **Voice (502):** speech-to-text, either on-device (`expo-speech-recognition` or similar) or an OpenAI transcription endpoint; decide in the 502 plan. No audio is stored.
6. **Postman `_tests`:** a character conversation reaches `ready`; a blocked message is refused; limit reached on save; the conversation links to the saved character.

## 6. Frontend Requirements
**Route:**
```
app/(main)/characters/create.tsx
```
**Shared with the story chatbot:** ChatWindow, MessageBubble, SuggestionChips (quick choices), PreviewCard, ConfirmButton.

**Character-specific:**
- **AttributeChoice**: tap/swipe selector for one attribute (e.g. hair length: short / medium / long).
- **VoiceInputButton**: speech-to-text dictation (feature flag).
- **PreviewCard (character)**: the attributes as a friendly card before saving.
- **RevealScreen**: after saving, a splash/reward animation while the image is generated, then the character's picture revealed (Kyle, 29/10). If the image takes too long, the user can leave and the character shows "picture on its way" in the carousel.
- **"Use the form instead"** link to the Slice 100 form.

**Libraries:** react-native-reanimated, a speech-to-text library (502; `expo-speech` is text-to-speech only), expo-image, zustand.

## 7. State Handling
- **Local:** chat state, draft model, draft image.
- **Global (Zustand):** `characters[]` cache updated on save.
- **Errors:** retries with backoff for AI calls; the generic moderation message ("That isn't allowed — please try something else"); "limit reached" handled as in [[PRD-Subscription-Entitlement-System]] (child: "Ask a grown-up"; parent: what's left and upgrade options).

## 8. User Flow
1. User taps **FAB (+)** on the Characters screen and chooses "Create with help".
2. The chatbot greets: "Let's make a new character! Who is it?"
3. The user replies (typed, spoken, or by tapping a quick choice).
4. The chatbot fills the model and asks about missing attributes, offering quick choices where the schema has fixed values.
5. When the model is complete, the preview card shows it.
6. On confirm → `POST /characters` → name moderated, limit checked, saved; the image job is queued.
7. A reward animation plays while the image is generated, then reveals the character's picture; the user returns to the carousel with the new character.
8. Later, "Re-create image" on the character page if they want a different picture (within the monthly limit).

## 9. Open Questions
None.

Resolved: the image is always generated, on save, and revealed with a reward animation (Kyle, 29/10); in the January launch (M6a), voice input (502) behind a flag and cut first if the date is at risk (Kyle, 29/10); a "skip AI" option exists (the Slice 100 form); archive and soft delete both exist ([[PRD-Characters]]); no per-character regeneration cap, the monthly character image limit applies (29/10).
