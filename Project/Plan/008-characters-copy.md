---
type: plan
title: "008 Characters: screen copy"
project: tomale-rn-v1
status: active
date: 2026-11-12
related:
  - "[[008-characters-micro-prd]]"
---

# 008 Characters: screen copy

Every user-facing line for speckit 008, taken from the Characters mock-ups (Design canvas "Tomale Characters screens") plus the lines the mock-ups don't show (marked *added*). `[Name]` is the character's name. British spelling. Server error messages are shown as the server sends them.

## Characters (parent)
- Title: "Characters". Count line: "[n] characters in your family" (1: "1 character in your family").
- Header controls (accessibility labels): "Search characters", "Show as a grid" / "Show as cards", "New character".
- Search placeholder: "Search characters". Filters: "All", "Favourites", "Archived".
- Search, no match *added*: "No characters called '[text]'" and a "Clear search" control.
- Favourites empty *added*: "No favourites yet. Tap the star on a character to add one."
- Archived empty *added*: "Nothing archived."
- Active list empty while archived exist *added*: "No characters here. Find archived ones under Archived."

## Carousel (parent and child)
- Card accessibility label: "[Name]. Tap to see more". Position: "Character [i] of [n]".
- Story count: parent "In [n] stories" (1: "In 1 story"; 0 *added*: "Not in a story yet"); child "In [n] of your stories" (1: "In 1 of your stories"; 0 *added*: "Not in your stories yet").
- Hint under the card: parent "Swipe to meet others · tap [Name] to see more"; child "Swipe to meet the others. Tap [Name] to see more."
- Panel actions: "Make a story", "Favourite", "Draw again", "More" (parent only), "See more about [Name]" *added* (opens detail), "Close".
- Panel stories heading: "Stories with [Name]".
- Child title: "My characters".

## Picture states *added*
- Drawing: "Drawing [Name]…" (accessibility: "[Name]'s picture is being drawn").
- Failed: "We couldn't draw [Name]." with "Try again" (opens Draw again).
- Still drawing when the check-in window ends *added*: "Still drawing. Check back soon."

## Detail
- Back: "Back to characters". More: "More for [Name]".
- Lines: description; story count as above; "Made [d MMM yyyy]" (e.g. "Made 12 Oct 2026").
- Actions: "Create a story with [Name]", "Draw [Name] again". Section: "Stories with [Name]".
- A story with no title *added*: "Untitled story".
- Character no longer available (deleted, archived for a child, or not found) *added*: "This character isn't available." with "Back to characters". No reason given.

## More (parent)
- "Remove from favourites" / "Add to favourites" *added*, "Create a story with [Name]", "Draw [Name] again", "Archive" with hint "Hides [Name] from your children. You can bring [Name] back.", "Unarchive" (archived character), "Delete character", "Cancel".

## Delete confirmation
- Title: "Delete [Name]?"
- Body: "[Name] will be gone for everyone in your family and can't be used in new stories. Stories [Name] is already in won't change."
- "This can't be undone."
- "To hide [Name] from your children instead, archive [Name]." ("archive [Name]" is a link that archives).
- Buttons: "Delete [Name]", "Keep [Name]".

## Confirmations *added*
- "[Name] archived", "[Name] unarchived", "[Name] deleted". No undo.

## Draw again
- Title: "Draw [Name] again". Intro: "We'll use this picture as a starting point."
- Field: "What should change? (optional)". Help: "For example: "wearing a red scarf" or "on a sunny beach". Up to 200 characters."
- Already drawing: "[Name] is already being drawn." / "Try again in a few minutes."
- Note: "The new picture replaces the old one when it's ready."
- Buttons: "Draw again", "Cancel". A refused instruction shows the server's message.

## New character (form)
- Title: "New character"; close: "Close". Intro: "We'll draw your character once you save."
- "Name", help "A first name or a nickname."; refused: "That name isn't allowed. Please try another." (or the server's message).
- "What do they look like?", placeholder "A small, friendly green dragon with round glasses and a striped scarf.", help "Colours, clothes, anything special about them."
- Button: "Save character".

## Empty account
- Title "Characters"; heading "Your characters will live here"; body "Make a dragon, a grown-up, a best friend or someone brand new. They can star in any story."; button "Make your first character".

## Create tab menu
- "What shall we make?"; "Make a story" with "Coming soon" (until M4); "Make a character"; note "Story making is on its way. Make your characters ready for it."
- Story actions on characters ("Make a story", "Create a story with [Name]") show the same "Coming soon" state until M4.
