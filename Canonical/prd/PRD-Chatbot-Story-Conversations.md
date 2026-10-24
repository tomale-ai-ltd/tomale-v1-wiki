# 📘 PRD: Chatbot-Driven Story Creation

## 1. Overview
We are replacing the legacy CRUD-style “Create Story” flow (6.1.1–6.1.5 in Adalo) with a conversational chatbot workflow.  
The chatbot guides the user through story creation (title, theme, characters, artwork style, tags) while integrating contextual awareness of the user’s profile, existing characters, and preferences.

This feature will:
- Provide a more natural, engaging UX.
- Store incremental progress directly in the `instant_stories` table (using a `status` lifecycle).
- Persist conversation history in a new `story_conversations` table.
- Allow the AI to propose structured suggestions (e.g., characters, themes, tags) that the user can accept or reject.

## 2. Goals
- ✅ Replace multi-step CRUD forms with a **single chat-based flow**.  
- ✅ Keep users engaged with conversational AI while retaining control over final story details.  
- ✅ Ensure incremental story data is saved (drafts, in-progress, complete).  
- ✅ Support **interactive suggestions** (cards in chat UI) for structured choices like characters or artwork.  
- ✅ Allow reuse of existing DB relationships (characters, themes, artwork_styles).

## 3. Scope

### In-Scope
- New **chat UI screen** in RN (`(main)/create-story/chat.tsx`).
- Backend support for conversation persistence (`story_conversations` table).
- AI integration that returns both text and structured UI suggestions.
- Support for selecting existing characters, creating new characters, selecting themes/artwork styles, and tagging stories.
- Status-driven lifecycle inside `instant_stories` (`draft → in_progress → complete`).

### Out-of-Scope (V1)
- Multi-user collaborative story creation.
- Advanced analytics of conversations (may come later with normalized `conversation_messages`).
- Vector search for large libraries (manual Xano context injection will be used for now).

## 4. Data Model

### **instant_stories** (existing, extended)
- `status`: enum → `draft`, `in_progress`, `complete`, `archived`
- Fields (`title`, `theme_id`, `characters[]`, `artwork_style_id`, `tags[]`) updated incrementally by chatbot.

### **story_conversations** (new)
- `id`: UUID/int (PK)
- `user_id`: FK → users
- `instant_story_id`: FK → instant_stories
- `messages`: JSON (array of `{ role, content, ui_suggestions? }`)
- `status`: enum → `active`, `complete`, `abandoned`
- `created_at`, `updated_at`

### **tags** (new)
- `id`, `label`, `created_at`

### **story_draft_tags** (new, join table)
- `instant_story_id` (FK)
- `tag_id` (FK)

## 5. API Endpoints

### `POST /story-conversations`
- Start new conversation linked to `instant_story`.
- Input: `{ user_id, instant_story_id }`
- Output: `{ conversation_id, status }`

### `POST /story-conversations/{id}/message`
- Append user message, return assistant reply.
- Input:
```json
{
  "role": "user",
  "content": "I'd like to create an action story about Noah.",
  "action": { "type": "character_select", "id": 12 }
}
```
- Output:
```json
{
  "role": "assistant",
  "content": "Great! Let's confirm the theme.",
  "ui_suggestions": [
    { "type": "theme_select", "options": [ { "id": 1, "label": "Action & Adventure" } ] }
  ]
}
```

### `GET /story-conversations/{id}`
- Fetch full history for resuming.

### `PATCH /story-conversations/{id}`
- Update status (`complete`, `abandoned`).

## 6. Frontend Requirements
- **Chat UI** component (NativeBase + GiftedChat or custom).
- Render both **text bubbles** and **interactive suggestion cards** (themes, characters, tags, artwork).
- Zustand global store:
  - `conversation.messages[]`
  - `draftStory` (synced with `instant_stories`)
- Navigation:
  - New route `app/(main)/create-story/chat.tsx`.

## 7. User Flow
1. User selects **“Create Story”** → RN creates draft in `instant_stories` (`status = draft`).
2. `POST /story-conversations` starts a conversation linked to draft.
3. User message → `POST /story-conversations/{id}/message`.
4. Backend:
   - Stores message
   - Fetches context (user profile, characters, prefs)
   - Calls GPT → reply text + `ui_suggestions`
   - Saves reply in `messages`
   - Updates `instant_stories` incrementally
5. RN renders assistant reply + cards.
6. User confirms selections (actions) → API call updates DB.
7. Loop continues until `status = complete`.
8. Story appears in Bookshelf tab.

## 8. Open Questions
- Should **email verification** be required before story creation?
- How much history should be stored in `messages` (truncate after X messages to save space)?
- Will we need analytics later (if yes, normalize into `conversation_messages`)?
