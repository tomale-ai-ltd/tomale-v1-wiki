---
type: prd
title: PRD-Chatbot-Create-Character
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-04-14
last_verified: 2026-04-14
owner: vault
features:
  - F-character-chatbot
---

# 📘 PRD: Create Character (10.2.1)

## 1. Overview
The current create-character flow is a static form (name, age, description). For V1, we want an **AI-assisted, child-friendly character builder** that turns natural language (typed or spoken) into a structured JSON model and a generated cover image. This flow reuses the story chatbot architecture, adapted for characters.

## 2. Goals
- ✅ Replace static form with a chatbot agent.  
- ✅ Support natural language and optional voice dictation for children.  
- ✅ Generate a structured JSON model from user input (attributes, appearance, metadata).  
- ✅ Provide an AI-generated cover image, with regenerate option.  
- ✅ Ensure child safety with moderation and terms-of-use checks.  
- ✅ Integrate with existing `characters` table and global state.  

## 3. Scope

### In-Scope
- New chatbot-like flow for creating characters.  
- Draft JSON model generation and user confirmation.  
- Cover image generation and retry.  
- Persist final approved character with `POST /characters`.  
- Update global `characters[]` cache on success.  

### Out-of-Scope (V1)
- AI-assisted edit character (10.1.1).  
- Complex multi-character relationships (family trees, etc.).  
- Offline-first character creation (requires AI).  

## 4. Data Model

### **characters** (existing)
- id  
- name  
- physical_description  
- primary_attributes (age, category, gender, ethnicity, etc.)  
- face_attributes, eyes_attributes, hair_attributes  
- cover_image (url, meta)  
- status (active | archived)  
- created_at, last_modified_at  
- users_id  

### **story_conversations** (reuse from chatbot)
- id  
- user_id  
- type = "character"  
- messages[] (chat history for transparency)  
- draft_json (character JSON candidate)  
- status (in-progress | completed | rejected)  

## 5. API Endpoints
- `POST /characters` → persist approved character JSON + image.  
- `PATCH /characters/{id}` → regenerate image, update metadata.  
- `GET /characters?user_id={id}` → fetch existing characters (for MCP-style suggestions).  
- `POST /story_conversations` → start character creation chat.  
- `PATCH /story_conversations/{id}` → append chat messages / update draft JSON.  

## 6. Frontend Requirements

**Route:**
```
app/(main)/characters/create.tsx
```

**Core Shared Components (with Story Chatbot):**
- **ChatWindow** → main scrollable container for chat.  
- **MessageBubble** → user + AI messages (text + optional images).  
- **SuggestionChips** → quick-reply buttons (e.g. “Add eagle”, “Make older”).  
- **JSONPreviewCard** → structured preview of draft character JSON.  
- **ConfirmButton** → final commit (“Save Character”).  

**Character-Specific Additions:**
- **VoiceInputButton** → speech-to-text dictation for children.  
- **ImagePreviewCard** → AI-generated cover image with “Regenerate” option.  

**Libraries:**
- react-native-reanimated (chat animations).  
- expo-speech / native speech-to-text (voice dictation).  
- expo-image or FastImage (cover image preview).  
- zustand (update global `characters[]`).  

## 7. State Handling
- **Local:** chat state, draft JSON, draft image.  
- **Global (Zustand):** `characters[]` cache updated on create success.  
- **Error handling:** exponential backoff retries for AI calls; surface error if moderation rejects.  

## 8. User Flow
1. User taps **FAB (+)** on characters/index.tsx.  
2. `create.tsx` opens → chatbot greets: “Let’s make a new character! Who is it?”  
3. User replies (typed or spoken via **VoiceInputButton**).  
4. AI suggests structured JSON → refines with follow-up questions.  
5. Once JSON complete → AI generates preview + cover image (**ImagePreviewCard**).  
6. User reviews → can regenerate image if needed.  
7. On confirm → `POST /characters` → persisted to DB.  
8. Global `characters[]` updated → user returns to carousel with new character visible.  

## 9. Open Questions
- Should there be a **“skip AI” fallback form** for parents who want control?  
- Should image generation always run, or be optional (e.g., text-only characters)?  
- Should archived characters appear in AI suggestions (e.g., “reuse archived character”)?  
