# 📘 PRD: Characters Screen (10.0)

## 1. Overview
The current Characters screen is a static list in Adalo with basic search/filter and a create button. For V1, we will deliver an **animated, avatar-first experience** using a carousel/circular slider. The background dynamically updates with the active character image, and metadata (name, attributes) is displayed interactively. This screen becomes as engaging as the Bookshelf while staying performant with up to 50+ characters.

## 2. Goals
- ✅ Provide an engaging browsing experience for characters (animated carousel).
- ✅ Support search + filters for faster navigation.
- ✅ Allow creating new characters via FAB or inline card.
- ✅ Ensure smooth performance with 50+ characters.
- ✅ Enable offline metadata browsing with lazy image loading.

## 3. Scope

### In-Scope
- New animated carousel implementation (based on RN Reanimated demo).
- Fullscreen background transitions on active character.
- Prefetch of previous/next images for smooth transitions.
- FAB for creating new character.
- Search/filter screen.
- Local/global caching for offline metadata.

### Out-of-Scope (V1)
- Advanced character editing (handled in 10.1 detail page).
- AI-assisted character creation (future feature).
- Character sharing/export.

## 4. Data Model

### **characters** (existing)
- id
- name
- physical_description
- primary_attributes (age, category, gender, etc.)
- face_attributes, eyes_attributes, hair_attributes
- cover_image (url, meta)
- status (active | archived)
- created_at, last_modified_at
- users_id

## 5. API Endpoints
- `GET /characters?user_id={id}` → list all characters.  
- `GET /characters/{id}` → detail view.  
- `POST /characters` → create character.  
- `PATCH /characters/{id}` → update metadata or set `status=archived` (soft delete).  

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
  - Circular thumbnail + name.  
  - Tap → `(tabs)/characters/[id].tsx`.  
  - Long press → quick actions (edit/archive).  

- **SearchBar & Filters**:  
  - Inline at top or in separate screen `(tabs)/characters/search.tsx`.  

- **FAB (Create Character)**:  
  - Floating action button, bottom-right.  
  - Navigates to `(main)/characters/create.tsx`.  

**Libraries:**
- react-native-reanimated (carousel animations).  
- expo-blur (background blur).  
- react-native-fast-image or Expo Image with `cachePolicy="disk"` (lazy + cached loading).  
- zustand (cache `characters[]` globally).  

## 7. State Handling
- **Global (Zustand):**  
  - Store `characters[]` JSON (metadata only, ~150 KB for 50 characters).  
  - Updated whenever create/edit/archive API calls succeed.  

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
6. User taps FAB → goes to create-character flow.  
7. Optional: search/filter used for narrowing list.  
8. User long-presses character → quick actions include Archive (`PATCH status=archived`).  

## 9. Open Questions
- Should archived characters appear in search results, or be fully hidden?  
- Do we want a “favourites” tag for characters, to pin them in carousel?  
- Should characters also show a “used in X stories” badge on the card?  
