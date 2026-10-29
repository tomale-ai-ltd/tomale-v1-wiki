---
type: prd
title: PRD-E-Reader
project: tomale-rn-v1
status: current
version: 2.0
date: 2026-04-14
last_verified: 2026-10-29
owner: vault
features:
  - F-bookshelf
related:
  - "[[v1-feature-map]]"
  - "[[PRD-Store-Orders]]"
---

# 📘 PRD: Immersive E-Reader Experience

> **Changes in 2.0 (B9, 29/10/2026, reviewed with Kyle):**
> - Two reading layouts: a single-page view and a book-spread view with right-to-left page turns.
> - "Read to me" uses generated audio (`gpt-4o-mini-tts`), not device speech.
> - Reading is landscape-only; a story is marked read on reaching the last page.
> - Progress and read status are stored on the device.
> - No downloads or PDFs.
> - Child locked card for stories awaiting approval.
> - The reader doubles as the pre-payment order preview.
> - Backend prep listed.
>
> Slice 300 / expected speckit 009 ([[roadmap]] M5).

## 1. Overview
The current story view (6.2.1.1) is a static text/image display. For V1, we will deliver a **premium, immersive e-reader** that feels like a real book: fullscreen landscape reading, page-turn navigation, generated read-aloud narration and autoplay. The same reader previews a book before a printed copy is ordered.

## 2. Goals
- ✅ Fullscreen, landscape-only reading with minimal UI.
- ✅ Two layouts the reader can switch between: **single page** (image and text on one screen) and **book spread** (image left, text right).
- ✅ Page turns that feel like a book: swipe right-to-left, with a page-turn animation.
- ✅ Natural-sounding read-aloud with autoplay.
- ✅ Resume where you left off, and mark stories as read.
- ✅ Preview mode for orders (cover, pages, gift message).
- ✅ Groundwork for later features (word highlighting, synced narration, Toniebox).

## 3. Scope
### In-Scope
- Bookshelf index (the profile's visible stories, with a "Read" badge) and story detail.
- `read.tsx` under the bookshelf routes.
- **Landscape lock:** the reader opens only in landscape; a rotation prompt blocks until the device is turned. No portrait fallback.
- Fullscreen cover page (title, subtitle, play button).
- **Layouts:**
  - *Single page:* the page image with its text block on the same screen.
  - *Book spread:* image on the left half, text on the right, like an open book.
  - The reader toggles between them from the controls; the last choice is remembered on the device.
- **Navigation:** horizontal swipe right-to-left to go forward (left-to-right back), with a page-turn (curl/flip) animation. Tapping the page edge also turns the page.
- **Read to me:** plays the page's generated audio; autoplay turns the page when narration ends.
- Overlays: progress indicator, layout toggle, sound/autoplay toggles, close button.
- **Progress and read status** on the device, per profile: last page, and "read" once the last page is reached.
- **Preview mode** for the store: same reader, with the gift message shown on the first page (where it's printed), opened from checkout.
- Locked "Waiting for a grown-up" card for stories awaiting approval (child profiles).

### Out-of-Scope (V1)
- Downloads, PDFs or offline audio files.
- Word-level highlighting/sync with narration.
- Custom fonts / advanced accessibility options.
- Toniebox or external device integration.
- Server-side reading progress and reading stats (`reading_logs`).
- The public Library and story sharing.

## 4. Data Model
### **instant_stories** (live)
`id`, `title`, `subtitle`, `cover_image`, `status`, `status_moderation`, `parental_approval_required`, `parent_approved`, `completed_at`

### **instant_story_pages** (live)
`id`, `instant_stories_id`, `page_number`, `text`, `image`, timestamps. **To add:** `audio` (file) for the narration.

### On the device (per profile)
`{story_id: {last_page, read: bool}}` and the preferred layout, in Zustand persist.

## 5. API Endpoints (`app` group)
- `GET /instant_stories` → bookshelf cards (lightweight projection, [[split-list-and-detail-projections]]).
- `GET /instant_stories/{id}` → full story with ordered pages (detail projection); **to add:** each page's `audio` URL.
- `DELETE /instant_stories/{id}` → soft delete (parent or owner).

## 5a. Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live code)
**Live:** story list and detail endpoints; `ai_pipeline/create_tts_audio`, a prototype that calls OpenAI `gpt-4o-mini-tts` (voice "fable") and uploads the MP3 to a Google Cloud Storage bucket.

**To build:**
1. **`instant_story_pages.audio`** (file field).
2. **Narration jobs:** after the page text passes moderation, queue one narration job per page (a new `page-audio` job type on the existing job queue, so retries and logging come free). The executor calls TTS and saves the file to the page (not Google Drive). Narration is ready by the time the story is.
3. **`data_models` record** of type `page-audio`: voice, model and speaking instructions (warm, slow, child-friendly), so the voice can change without code.
4. **Detail projection** includes `audio` per page.
5. **Costs** recorded in `token_usage` like other AI calls; narration counts within the story's generation (no separate limit).
6. **Backfill:** a manual function to narrate existing finished stories.
7. **Postman `_tests`:** story detail returns audio for every page once Done.

## 6. Frontend Requirements
**Route:**
```
app/(tabs)/bookshelf/[id]/read.tsx
```
**Components:**
- **RotationPrompt**: blocking modal with blurred background, animated "turn your device" prompt.
- **CoverScreen**: fullscreen cover image + title/subtitle + play button + close button.
- **ReaderPager**: horizontal pager, right-to-left forward, with a page-turn animation.
- **PageSingle** / **PageSpread**: the two layouts.
- **ControlsOverlay**: hidden by default, tap to reveal; progress, layout toggle, autoplay, sound, close.
- **AudioPlayer**: plays the page audio (`expo-audio`), drives autoplay.
- **PreviewBanner** (preview mode): "Looks good → continue to payment"; the gift message appears on the first page.

**Libraries:** expo-screen-orientation, expo-blur, expo-audio, react-native-reanimated + react-native-gesture-handler (page-turn), zustand. A page-curl library to evaluate in the 009 plan.

## 7. User Flow
1. User taps **"Read"** on story detail.
2. If the device is in portrait, **RotationPrompt** blocks until it's turned; then **CoverScreen** loads.
3. On Play → **ReaderPager** opens at page 1 (or the saved page), in the last-used layout.
4. Swipe right-to-left (or tap the right edge) to turn the page; tap the middle to show controls.
5. Read to me: narration plays; with autoplay on, the page turns when it ends.
6. Reaching the last page marks the story read; the Bookshelf shows the badge.
7. Close → back to story detail; position saved.

**Preview mode:** from checkout, the same reader opens with the gift message; continuing returns to payment.

## 8. Open Questions
- Default layout: single page or book spread? (Spread may need a larger screen; on small phones single page may suit better.)
- Page-curl animation library vs a custom Reanimated turn: decide in the 009 plan after a quick prototype.
- Voice choice and speaking style for narration (test a few with children).

Resolved 29/10: generated audio for read-aloud; landscape only, no portrait fallback; read is marked on the last page; progress on the device.
