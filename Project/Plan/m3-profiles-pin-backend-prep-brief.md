---
type: plan
title: "M3 backend prep, part A: profiles and the parental PIN"
project: tomale-rn-v1
status: active
date: 2026-11-12
related:
  - "[[PRD-Profiles]]"
  - "[[parental-gate-on-profile-switch]]"
  - "[[log-in-to-the-primary-profile]]"
  - "[[cap-profiles-at-one-adult-and-six-children]]"
  - "[[use-bundled-preset-avatars-for-profiles]]"
  - "[[prevent-deleting-active-profile-via-soft-delete]]"
  - "[[security-model]]"
---

# M3 backend prep, part A: profiles and the parental PIN

Goal: every backend change [[PRD-Profiles]] §5 needs, done and tested in Postman before `/speckit.specify` for M3, so the speckit run is frontend only (same pattern as [[characters-backend-prep-brief]]). Part B (approvals inbox, approve/reject, [[PRD-Parental-Oversight-Content-Approval]] §7a) follows in its own brief; it depends on the PIN.

## Kyle's decisions (12/11)
- **PIN unlock and "Forgot PIN" use the emailed login link** (magic link), not a rebuilt password reset. The email proves the parent owns the account.
- **Profile names: 1–18 characters** (was 3–18), still moderated.

## Findings in the live endpoints (mirror f83c2a6, 11/11)
- `auth/select_profile`: no PIN; accepts a **deleted or inactive** profile; accepts a **revoked or expired session**, so a token from a logged-out session can keep minting fresh tokens.
- `auth/reset_password`: public, never asks for the emailed code, checks a `temp_login` field that doesn't exist on `users` (so it currently always refuses), and returns the whole user record (password hash included) if it ever succeeds. Unsafe by design.
- `auth/request_magic_link`: the rate-limit precondition fails when an account has never had a link (`magic_link.expiration` null), so the **first link ever requested is refused** with a 429 message; an unknown email also gets the 429 instead of the generic reply.
- Profile endpoints (`/users/user_profiles` GET/POST, `/{id}` PATCH/DELETE): loose `is_child == false` checks (null counts as parent); code `PROFILE_NOT_PARENT` instead of `PARENT_PROFILE_REQUIRED`; names 3–18; one-stage moderation (profanity only); `avatar_key` regex `^[a-z0-9-]{1,30}$` rejects `preset:`/`character:` keys; POST can't set an avatar and outputs `avatar.*` fields that no longer exist; GET sorts by the old `is_default` field.
- Parent-only checks exist only on character archive/delete. Store, Stripe and subscriptions endpoints accept a child profile.
- Login and refresh tokens carry `active_profile` {id, name, is_child}; select_profile adds `is_primary`. Harmless; make them match.

## Change set 1: PIN storage and set/change
- `users`: `parental_pin` (Xano **password** type, hidden, never output), `pin_failed_attempts` (int, default 0), `pin_locked` (bool, default false), `pin_set_at` (timestamp, nullable).
- `POST /users/me/pin` {`pin`, `current_pin?`}: parent profile only (strict `=== false`, else 400 `PARENT_PROFILE_REQUIRED`); `email_verified` true (else 400 `EMAIL_NOT_VERIFIED`); `pin` matches `^[0-9]{4}$` (else 400 `PIN_FORMAT`); if a PIN is already set, `current_pin` must match (a wrong one counts towards the lock, same rules as change set 2); `pin_locked` true → 400 `PIN_LOCKED`. Saves the hash, `pin_set_at`, resets attempts. Response `{pin_set: true}`.

## Change set 2: `auth/select_profile`
- Session: must belong to the caller, `status == "active"` and not past `expires_at` (else 401).
- Target profile: same account, `deleted_at` null, `is_active` true (else 404).
- **PIN whenever the target is a parent profile** (`is_child === false`), whoever the caller is. A fresh password login still lands on the primary profile without a PIN ([[log-in-to-the-primary-profile]]); the only way into a parent profile after that is through this check, which also covers the picker when the app is reopened.
  - PIN not set → 400 `PIN_NOT_SET`; locked → 400 `PIN_LOCKED`; missing → 400 `PIN_REQUIRED`; wrong → increment attempts, 400 `PIN_INVALID` with `attempts_remaining`; the 5th wrong attempt sets `pin_locked` and returns `PIN_LOCKED`; right → reset attempts.
- Child targets need no PIN. Token extras: `active_profile` {id, name, is_child, is_primary} (same shape in login, refresh, magic link).
- Known limit (V1): a restored session refreshes into the last active profile, which may be the parent; the app holds that token but shows the picker and must call select_profile (with the PIN) before using a parent profile. Server-side enforcement of "PIN on reopen" would need refresh to downgrade the token; not in V1.

## Change set 3: unlock and "Forgot PIN" by email link
- `auth/request_magic_link` {`email`, `purpose?` = `login` | `reset_pin`, default `login`}: fix the rate limit (only refuse when a link was issued less than 60 s ago; never for a first request); unknown email gets the same generic reply as a known one; store `purpose` on `users.magic_link`.
- `auth/complete_magic_link`: when `purpose == "reset_pin"`, clear `parental_pin`, `pin_set_at`, `pin_failed_attempts`, `pin_locked`; always land on the **primary** profile (by `is_primary`, not oldest). The app then sees `pin_set: false` and shows "Set a new PIN".
- **Delete `auth/reset_password`.** Forgotten password = email link login (V1). Changing a password is out of this brief (no endpoint exists today; add with Settings if needed).

## Change set 4: profile endpoints
- All: strict parent checks, code `PARENT_PROFILE_REQUIRED` (400, `payload.code`), consistent 400/404 codes.
- Names: trim, 1–18; two-stage moderation as in `POST /characters` (profanity signal, then `content_moderation_name` in a `try_catch`, `.pass === true`, else 400 `NAME_NOT_ALLOWED`).
- `avatar_key`: `preset:<key>` (`^preset:[a-z0-9-]{1,30}$`) or `character:<id>` (character on this account, not deleted), else 400 `INVALID_AVATAR_KEY`. POST accepts it; outputs `avatar_key`, not `avatar.*`.
- POST: parent only; **PIN must be set** (400 `PIN_NOT_SET`), so no child profile exists without a PIN; cap 6 children (existing); `is_child` true, `is_primary` false.
- PATCH: parent, or a child editing their own profile (strict).
- GET: sort `is_primary` desc, then `created_at`.
- DELETE (change set 6 adds the story move).

## Change set 5: parent-only checks
Add the strict parent precondition (400 `PARENT_PROFILE_REQUIRED`) to: `store_orders` GET, POST, GET {id}, PATCH, cancel; `stripe/create_checkout_session`; `stripe/check_order_paid`; `subscriptions` GET and GET {id}. (Approve/reject come in part B.)

## Change set 6: delete moves stories
`DELETE /users/user_profiles/{id}`: after the existing guards, move every `instant_stories` row with that `user_profiles_id` to the primary profile, then soft delete. Response `{deleted: true, stories_moved: n}`.

## Change set 7: assign a story
`POST /instant_stories/{id}/assign` {`user_profiles_id`}: parent only; story on this account and not deleted; target an active, non-deleted profile on this account (else 404). Sets `user_profiles_id`. Response: the story id and new profile id.

## Change set 8: `auth/me`
Drop `users.profile_photo`; add `pin_set` (bool) and `pin_locked` (bool). No PIN data otherwise.

## Order and testing
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8, publishing and testing each before the next. Strict `=== false` checks; guard `$list.field` with a count; nullable optional inputs (`bool? x?`).

Postman folder 6 (Profiles and PIN):
- 6A set PIN: wrong format, unverified-email account (if a test account exists), set, change with wrong/right current PIN.
- 6B select_profile: child target without PIN; parent target without PIN (`PIN_REQUIRED`), wrong (`PIN_INVALID`, attempts_remaining 4), right; deleted profile (404); logged-out session (401).
- 6C lock: 5 wrong → `PIN_LOCKED`; right PIN still refused; magic link `reset_pin` (simulate by calling complete with a token from a test hook, or verify manually once) → `pin_set` false → set again.
- 6D profiles: 1-character name ok, 19 refused, blocked name `NAME_NOT_ALLOWED`, `preset:` and `character:` avatars, another account's character avatar refused, child can't create/delete, create refused without PIN.
- 6E parent-only: child token refused on store_orders, checkout session, subscriptions.
- 6F delete moves stories; assign (parent ok, child refused, other account's profile 404).
- Reset state at the end (PIN back to the test value, attempts 0).

## Pre-launch notes
- Legacy accounts with child profiles but no PIN: the app sends them to "Set a PIN" (pin_set false) before the picker.
- A child can deliberately lock the PIN with 5 wrong tries; the parent unlocks by email. Accepted in the PRD.
