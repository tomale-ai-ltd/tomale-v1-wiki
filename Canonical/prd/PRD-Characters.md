---
type: prd
title: PRD-Characters
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-characters
related:
  - "[[v1-feature-map]]"
  - "[[share-characters-across-the-household]]"
  - "[[PRD-Chatbot-Create-Character]]"
---

# 📘 PRD: Characters Screen (10.0)

> **Changes in 2.0 (B9, 29/10/2026, reviewed with Kyle):**
> - Characters are shared by the whole household; only parents delete or archive them.
> - Characters link to any number of stories through `instant_story_characters`.
> - Archive and soft delete are both kept, as built.
> - Names are moderated on create, with a generic message.
> - New: favourites, richer cards, "create a story with this character", and "re-create image" (image-to-image).
> - No text edit in V1.
> - Endpoints match the live `app` group.
> - AI-assisted creation is its own feature, [[PRD-Chatbot-Create-Character]] (Slice 500).
>
> Built as **Slice 100 / speckit 007** ([[roadmap]] M2).

## 1. Overview
The current Characters screen is a static list in Adalo with basic search/filter and a create button. For V1, we will deliver an **animated, avatar-first experience** using a carousel/circular slider. The background dynamically updates with the active character image, and metadata (name, attributes) is displayed interactively. This screen becomes as engaging as the Bookshelf while staying performant with up to 50+ characters.

Characters are **shared by the whole household** ([[share-characters-across-the-household]]): every profile sees every character on the account. Names and descriptions are moderated on create. Only parent profiles can archive or delete a character.

A character can appear in **any number of stories**: the link lives in `instant_story_characters`, a many-to-many table.

## 2. Goals
- ✅ Provide an engaging browsing experience for characters (animated carousel).
- ✅ Support search + filters for faster navigation.
- ✅ Allow creating new characters via FAB or inline card (simple form in V1).
- ✅ Ensure smooth performance with 50+ characters.
- ✅ Enable offline metadata browsing with lazy image loading.

## 3. Scope
### In-Scope
- Characters index (grid first, then the animated carousel based on the RN Reanimated demo).
- Character detail page (read-only).
- Create character with a simple form (name + description). The name goes through two-stage moderation on submit ([[moderate-names-in-two-stages]]). A blocked name shows a generic message ("That name isn't allowed — please try another"); the reason is logged, never shown.
- Fullscreen background transitions on the active character; prefetch of previous/next images.
- Archive (hide, keep) and delete (soft delete) from the detail page or a long-press quick action, **parent profiles only**.
- **Favourite** a character (pinned first in the carousel).
- Richer cards: "used in X stories" (from `instant_story_characters`) and created date.
- **Create a story with this character:** a quick action that starts the story chat with the character already selected (needs Slice 200; the button ships with 200).
- **Re-create image:** regenerate the character image, optionally with a short instruction, using the current image as a reference (image-to-image). Counts against plan limits.
- Search/filter screen.
- Local/global caching for offline metadata.
- A "picture on its way" state while the character image is generated (image jobs run in the background).

### Out-of-Scope (V1)
- **Editing a character's name or description** (no PATCH in V1; an edit would need the moderation check). Re-create image covers the visual changes.
- AI-assisted character creation: its own feature, [[PRD-Chatbot-Create-Character]] (Slice 500).
- Character sharing/export, sharing characters between profiles.

## 4. Data Model
### **characters** (live, generated [[Repos/tomale-rn-test/memory/data-model|data-model]] 28/10/2026)
- `id`
- `name`, `physical_description`
- `primary_attributes` (age, category, subcategory, gender, ethnicity)
- `face_attributes`, `eyes_attributes`, `hair_attributes`, `clothing_attributes`
- `cover_image` (image)
- `users_id` (account owner), `data_models_id`
- `status` (active | archived), `is_deleted`, `deleted_at` (kept as built: archive and soft delete; the delete endpoint keeps them in step)
- `instant_stories_id`: the story the character was created in, if any. Kept, but **not** the link used for stories: `instant_story_characters` is.
- `created_at`, `last_modified_at`

### **instant_story_characters** (live, many-to-many)
`instant_stories_id`, `characters_id`. `POST /characters` with an `instant_stories_id` adds the first link; `generate_story_page_text` reads the story's characters from here and errors if there are none.

### Backend prep before 007
1. Visibility stays account-scoped (`users_id`), as built: no new ownership column, no backfill.
2. Delete and archive check that the active profile is a parent (`is_child = false`); a child gets 400 `PARENT_PROFILE_REQUIRED`.
3. Add `is_favourite` (bool).
4. New endpoint to link existing characters to a story: `POST /instant_stories/{id}/characters` (`characters_ids[]`; each must be visible to the caller). Used by the story chat and the quick action, so no character record is ever patched to join a story.
5. New endpoint `POST /characters/{id}/regenerate_image` (optional `instruction`; uses the current image as a reference; entitlement-gated).
6. Archive and favourite need a small update endpoint, limited to `status` and `is_favourite` (no text fields, so no moderation needed).
7. Postman `_tests`: add tests for the new endpoints and for a child profile being refused delete/archive ([[test-suite]]).

## 5. API Endpoints (`app` group)
- `GET /characters` → the caller's visible characters (identity from the token, never from inputs).
- `GET /characters/{characters_id}` → detail view.
- `POST /characters` → create; runs name moderation; queues the character image job.
- `DELETE /characters/{characters_id}` → soft delete.
- `POST /characters/{id}/model` → turns a free-text description into the structured attribute model (used by create).
- **To build:** `PATCH /characters/{id}/flags` (`status`, `is_favourite` only), `POST /characters/{id}/regenerate_image`, `POST /instant_stories/{id}/characters`.

## 6. Frontend Requirements
**Route:**
```
app/(tabs)/characters/index.tsx
```
**Components:**
- **CharacterCarousel** (adapted from demo):  
  - Circular slider with avatars.  
  - Active character enlarged + white border.  
  - Background = full-screen blurred version of active character image.  
  - Prefetch next/prev character images.  
- **CharacterCard**:  
  - Circular thumbnail + name; a placeholder while the image is pending.  
  - Tap → `(tabs)/characters/[id].tsx`.  
  - Long press → quick actions (favourite, create a story; parents also archive and delete, with confirmation).  
  - Shows "used in X stories".  
- **SearchBar & Filters**:  
  - Inline at top or in separate screen `(tabs)/characters/search.tsx`.  
- **FAB (Create Character)**:  
  - Floating action button, bottom-right.  
  - Navigates to `(main)/characters/create.tsx` (simple form).  

**Libraries:**
- react-native-reanimated (carousel animations).  
- expo-blur (background blur).  
- `expo-image` with `cachePolicy="disk"` (lazy + cached loading).  
- zustand (cache `characters[]` globally).  

## 7. State Handling
- **Global (Zustand):**  
  - Store `characters[]` JSON (metadata only, ~150 KB for 50 characters).  
  - Updated whenever create/delete calls succeed.  
- **Local:**  
  - `activeIndex` (carousel state).  
  - Search query / filters.  
  - Prefetch state (previous/next images cached).  

## 8. User Flow
1. User opens Characters tab.  
2. Cached metadata loads instantly; API fetch updates list.  
3. Carousel displays circular avatars; background updates dynamically.  
4. User scrolls horizontally → activeIndex updates, background prefetches ±1 image.  
5. User taps a character → navigates to `[id].tsx` detail page.  
6. User taps FAB → create form → name moderated → character saved; the image appears when its job completes.  
7. Optional: search/filter used for narrowing list.  
8. User long-presses character → favourite / create a story with it (parents: archive / delete).  
9. From detail, "Re-create image" → optional instruction → the new image replaces the old one when ready.

## 9. Open Questions
- Should archived characters still be offered when creating a story?

Resolved (29/10): characters are household-wide, parents archive/delete; favourites and richer cards are in; moderation message is generic; visual changes via re-create image, no text edit in V1; characters are reusable across stories through the join table; re-creations count against the monthly character image limit (Free 4, Creator 30, [[PRD-Subscription-Entitlement-System]]), no per-character cap.
