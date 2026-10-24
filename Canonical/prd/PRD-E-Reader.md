---
type: prd
title: PRD-E-Reader
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-04-14
last_verified: 2026-04-14
owner: vault
---

# 📘 PRD: Immersive E-Reader Experience

## 1. Overview
The current story-view (6.2.1.1) is a static text/image display. For V1, we will deliver a **premium, immersive e-reader experience** with swipe-based navigation, fullscreen mode, text-to-speech narration, and autoplay.

This feature transforms story consumption from a simple list into an engaging, multimedia reading experience aligned with Tomale’s mission.

## 2. Goals
- ✅ Deliver fullscreen immersive reading (landscape orientation, minimal UI).
- ✅ Introduce page-by-page navigation (vertical swipe with parallax).
- ✅ Support read-aloud (TTS baseline) + optional autoplay with auto-scroll.
- ✅ Provide progress tracking so users can resume where they left off.
- ✅ Lay groundwork for future features (highlighting, synced narration, Toniebox).

## 3. Scope

### In-Scope
- New `read.tsx` screen under bookshelf routes.
- Fullscreen cover page (title, subtitle, play button).
- Page navigation: vertical swipe with parallax scroll animation.
- Orientation lock to landscape with pre-launch rotation prompt.
- Text-to-speech (expo-speech) with autoplay mode.
- Basic UI overlays: progress indicator, sound/autoplay toggles, close button.
- Progress persistence (`PATCH /reading_logs`).

### Out-of-Scope (V1)
- Word-level highlighting/sync with narration.
- Custom fonts / advanced accessibility options.
- Toniebox or external device integration.
- Offline audio file downloads.

## 4. Data Model

### **instant_stories** (existing)
- id, title, subtitle, cover_image

### **instant_story_pages** (existing)
- id
- story_id (FK → instant_stories)
- page_number
- text
- image_url
- characters[] (contextual, read-only)

### **reading_logs** (new)
- id
- user_id (FK → users)
- story_id (FK → instant_stories)
- last_page_read
- completed: boolean
- updated_at

## 5. API Endpoints

### `GET /instant_stories/{id}?include=pages`
- Fetch full story with ordered pages.

### `PATCH /reading_logs`
- Input: `{ story_id, last_page_read, completed }`
- Output: `{ success: true }`

### `GET /audio/{story_id}` *(optional for future pre-generated narration)*
- Not required in V1.

## 6. Frontend Requirements

**Route:**
```
app/(tabs)/bookshelf/[id]/read.tsx
```

**Components:**
- **RotationPrompt**: modal with blurred background, animated “rotate to landscape” prompt.
- **CoverScreen**: fullscreen cover image + title/subtitle + play button + close button.
- **ReaderPager**: vertical swipe container for pages (react-native-pager-view / reanimated carousel).
- **PageCard**: image (zoomable) + text block.
- **ControlsOverlay**: hidden by default, tap to reveal; contains progress indicator, autoplay toggle, sound toggle, close button.

**Libraries:**
- expo-speech (TTS)
- expo-screen-orientation (lock/rotate)
- expo-blur (rotation prompt background)
- react-native-reanimated + react-native-pager-view (animated swipe/parallax)
- zustand (reading state)

## 7. User Flow
1. User taps **“Read”** on story-detail.
2. **RotationPrompt** appears (blurred background).
3. Once rotated to landscape, load **CoverScreen**.
4. Cover shows image + title/subtitle + large “Play” button.
5. On Play → **ReaderPager** opens, starting at Page 1.
6. User swipes up/down to navigate pages; progress indicator shows on tap.
7. Optional: user taps autoplay → TTS reads page → auto-scrolls when narration ends.
8. Exit via close button → return to story-detail.
9. Reading progress auto-saved (`PATCH /reading_logs`).

## 8. Open Questions
- Should users be able to manually mark story complete, or only when last page is reached?
- Do we want to support portrait fallback if device rotation is locked, or block reading until landscape?
- Should stories cached offline (downloaded) include narration/audio, or just text/images for V1?
