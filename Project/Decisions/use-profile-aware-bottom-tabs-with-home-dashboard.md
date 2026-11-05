---
type: decision
title: "use-profile-aware-bottom-tabs-with-home-dashboard"
project: tomale-rn-v1
status: accepted
date: "2026-11-05"
related:
  - "[[2026-11-05-002]]"
  - "[[parental-gate-on-profile-switch]]"
  - "[[PRD-Home-Dashboard]]"
affects:
  - "[[1-prd-tomale-react-native-app-v1]]"
  - "[[roadmap]]"
  - "Tomale design system (TabBar)"
  - "app/(main)/(tabs)/_layout.tsx"
features:
  - F-home
  - F-profiles
---

# Decision: use-profile-aware-bottom-tabs-with-home-dashboard

## What we decided

The app uses a standard bottom tab bar, the same app for parents and children, with tabs that depend on the active profile:

| Profile | Tabs | Header |
|---|---|---|
| Parent | Home · Create · Bookshelf · Characters · Store | Avatar and greeting → switch profile, Settings, Help |
| Child | Home · Create · Bookshelf · Characters | Avatar and greeting → switch profile (PIN to reach a parent profile) |

- Every tab is a colourful illustrated brand icon **with** a text label; nothing is icon-only.
- **Home is a dashboard**: a greeting band with the profile's avatar, recent stories, favourite characters, and an announcements slot (new artwork styles, themes, offers). On a child profile the slot shows creative news only, never prices or offers ([[PRD-Home-Dashboard]]).
- **Create** is a tab and acts as the quick create menu (story, character).
- Settings is not a tab: it sits behind the avatar, parent profile only.

## Why

Kyle (05/11): children already know the basic tab pattern, so it is fine as long as it is colourful and playful, with text and pictures together. A profile split with a broadly similar app (as Netflix, Disney+ and YouTube Kids do) fits the existing profiles and PIN gate. Apple and Google both recommend 3–5 bottom tabs, so a parent's five is the ceiling. Hiding Store on child profiles also keeps purchases behind the parental gate, as the Apple Kids category requires.

## Alternatives considered

- Characters pushed from Home (four tabs): hides one of the most-loved areas for children.
- Characters inside Bookshelf (segments): mixes two collections and adds a control children must learn.
- A child-first app with a separate gated parent area (Khan Academy Kids, Toca Boca): two navigation systems to build and maintain.

## Trade-offs accepted

- New brand icons are needed for Home and Characters.
- The tab bar changes when the profile changes, so the layout must react to the active profile from `auth/me`.
- The design system TabBar drawn on 05/11 (Home, Create, Bookshelf, Store) and the scaffold `(tabs)/_layout.tsx` (Home, Bookshelf, Characters, Store, Settings) are both superseded by this.
