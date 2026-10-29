---
type: prd
title: PRD-Profiles
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-29
last_verified: 2026-10-29
owner: vault
features:
  - F-profiles
related:
  - "[[v1-feature-map]]"
  - "[[PRD-Parental-Oversight-Content-Approval]]"
  - "[[security-model]]"
---

# PRD: Household profiles

> **New in B9 (29/10/2026), reviewed with Kyle.** Written from decisions made between May and October 2026, the live backend, and Kyle's review. The backend is mostly built; the PIN and the items in §5 are not. There are no app screens yet. Milestone M3 in the [[roadmap]].

## 1. Overview
One Tomale account is a household. The account (`users`) holds login, billing and legal responsibility, and belongs to the parent. Each person who uses the app has a **profile** (`user_profiles`): one adult (primary) profile and up to six child profiles. Profiles carry the displayable identity (name and avatar) and decide what a person sees and can do.

**Responsibility model:** the parent owns the account and its password. The app protects the way from a child profile into a parent profile (the PIN) and keeps parent-only areas out of the child UI. What the parent does with an unlocked parent profile is on their watch, with sensible defaults (§3) to reduce accidental hand-overs.

## 2. Goals
- Let a parent add their children and switch between profiles quickly.
- Keep children's content separate, and keep parent-only actions (approvals, purchases, settings, deletes) out of a child's reach.
- Minimise children's personal data (ICO Children's Code): names and preset or character avatars only, no photos.

## 3. Rules
| Rule | Detail | Source |
|---|---|---|
| One table | Adults and children share `user_profiles`, with `is_child` | [[adopt-unified-user-profiles-table]] |
| Caps | 1 adult (primary) + up to 6 children per account; free on every plan. Deleted profiles don't count | [[cap-profiles-at-one-adult-and-six-children]] |
| Fixed type | `is_child` is set by the server at creation and can't change | [[cap-profiles-at-one-adult-and-six-children]] |
| Primary adult | Created at sign-up with the name "default" (`is_primary = true`); renamed during onboarding; can't be deleted or demoted in V1 | [[cap-profiles-at-one-adult-and-six-children]] |
| Fresh login | A login with the password lands on the primary profile (the person who typed the password is the parent) | [[log-in-to-the-primary-profile]] |
| Reopening the app | If the account has child profiles, a restored session opens the **profile picker**, and the parent profile needs the PIN. The same happens after 15 minutes in the background. Accounts without children skip the picker | Kyle, 29/10 |
| PIN | 4 digits, set during onboarding after email verification. Needed to enter a parent profile from a child profile or from the picker. 5 wrong attempts lock it; unlocking needs a password reset, which also sets a new PIN | [[parental-gate-on-profile-switch]], Kyle 29/10 |
| Profile context | Carried in the token (`active_profile`: id, name, is_child); a switch issues a new token | [[carry-active-profile-in-token-extras]] |
| Fail closed | No `active_profile` in the token → re-login, never a fallback | [[fail-closed-active-profile-resolution]] |
| Parent-only areas | Store, orders, subscriptions, approvals, profile management and character deletion are hidden or locked in the child UI **and** refused by the backend for child profiles (`PARENT_PROFILE_REQUIRED`) | Kyle 29/10 |
| Avatars | Preset avatars (adult and child, with colour options) plus any of the household's character images | [[use-bundled-preset-avatars-for-profiles]], Kyle 29/10 |
| Names | Two-stage moderation on create and rename | [[moderate-names-in-two-stages]] |
| Delete | Soft delete; not the primary profile, not the profile in use. The profile's stories move to the primary profile | [[prevent-deleting-active-profile-via-soft-delete]], Kyle 29/10 |
| Visibility | Stories: a child sees their own; parents see the household's. Characters: shared by the household | [[per-child-story-visibility]], [[share-characters-across-the-household]] |

## 4. Deleting a profile: what happens
- Today `DELETE` sets `deleted_at` and `is_active = false` on the profile only; nothing cascades.
- **To add:** in the same request, the profile's stories are reassigned to the primary ("default") profile (`instant_stories.user_profiles_id`, a single value). Nothing is lost and there's no restore.
- From a story's detail page, a parent can then **assign the story** to any active profile on the account ("Who's this story for?").
- Characters (household-wide), orders and subscriptions (account-level) are unaffected.

## 5. Backend prep (from the generated [[Repos/tomale-rn-test/memory/data-model|data-model]] and the live endpoints)
**Live:** `user_profiles` (`id` uuid, `name`, `users_id`, `avatar_key`, `is_child`, `is_primary`, `is_active`, timestamps, `deleted_at`); endpoints `GET/POST /users/user_profiles`, `PATCH/DELETE /users/user_profiles/{id}`, `POST /auth/select_profile`.

**To build:**
1. **PIN fields on `users`:** `parental_pin_hash`, `parental_pin_failed_attempts`, `parental_pin_locked_until` (or a locked flag), `parental_pin_set_at`.
2. **Set PIN:** `POST /users/me/pin`: parent profile, email verified, PIN not yet set (onboarding). Change PIN requires the current PIN.
3. **`auth/select_profile`:** require `pin` when the target is a parent profile and the caller isn't already on a parent profile; check the hash; count failures; lock at 5 (400 `PIN_REQUIRED`, `PIN_INVALID`, `PIN_LOCKED`).
4. **Password reset clears the lock** and returns the user to "set a new PIN" (extends `auth/reset_password` / magic-link flow).
5. **Parent-only checks** (`active_profile.is_child = false`, else 400 `PARENT_PROFILE_REQUIRED`) on: `store_orders` (all), `stripe/create_checkout_session`, `stripe/check_order_paid`, `subscriptions`, profile create/delete, character archive/delete, story approve/reject.
6. **Delete reassigns stories:** `DELETE /users/user_profiles/{id}` also moves that profile's stories to the primary profile.
7. **Assign a story:** `POST /instant_stories/{id}/assign` (parent; target is any active profile on the account).
8. **Avatars:** `avatar_key` accepts `preset:<key>` or `character:<id>`; the server checks the character belongs to the account. If a character is deleted, the app falls back to a preset.
9. **`auth/me`:** stop returning `users.profile_photo`; add `pin_set` (bool) for onboarding.
10. **Postman `_tests`:** PIN set, wrong PIN, lock-out, reset; child refused on parent-only endpoints; delete moves stories; assign.

## 6. Frontend Requirements
- **Profile picker:** full-screen avatars and names; shown on app reopen (with children) and after 15 minutes in the background; tapping a parent profile opens the PIN pad.
- **Onboarding:** verify email → name the adult profile → set PIN → optionally add children.
- **Add child:** name + avatar (presets with colour options, or a household character image); no adult/child toggle.
- **Manage profiles** (parent only): rename, change avatar, delete with confirmation ("their stories will move to your profile").
- **Story detail** (parent): "Who's this story for?" to assign it to a profile.
- **Child UI:** store, orders, subscriptions, approvals and settings are locked (greyed out with a lock icon) in V1. A distinct child UI is a later option.
- **PIN lock:** after 5 failures, a "reset your password to unlock" screen.
- **After a switch:** clear profile-scoped caches (stories) and refetch.

## 7. User Flow
1. Sign-up → verify email → name the adult profile (from "default") → set the 4-digit PIN.
2. The parent adds child profiles (name + avatar).
3. The parent hands the device over: switch to the child's profile (no PIN).
4. The child creates and reads their own stories; shared characters are available.
5. Back to a parent profile: PIN. Reopening the app later: picker, and PIN for the parent.

## 8. Out of Scope (V1)
- Multiple adults, promoting a child, deleting the primary profile, restoring a deleted profile.
- Per-profile entitlements or plans.
- "Last used profile" on login.
- Photos as avatars; a fully separate child UI.

## 9. Open Questions
None. Resolved 29/10: 15-minute background timeout; no extra check on character avatars (already moderated); deleted profiles' stories move to the primary profile, no restore.
