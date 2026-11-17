# 009-profiles-pin -- Profiles and PIN -- Switch, protect, manage #

<!--
Micro-PRD for speckit 009 (roadmap M3, first of two specs: [[split-m3-into-specs-009-and-010]]). Drafted by Claude 17/11; corrected 17/11 after specify (statuses 404/429, PIN auto-submit, forgot PIN, add-child save rules, header bands).
Cursor copies it to `.docs/prd/009-profiles-pin.md` before `/speckit.specify`.
Sources: [[PRD-Profiles]] (with PU-2026-11-17-03), [[parental-gate-on-profile-switch]], [[ask-for-pin-when-first-needed]],
[[use-profile-aware-bottom-tabs-with-home-dashboard]], [[use-bundled-preset-avatars-for-profiles]], [[moderate-names-in-two-stages]],
[[m3-profiles-pin-backend-prep-brief]] (backend built 12/11, Postman folder 6), RS-2026-11-12-04 (client and overlay, 17/11), [[pre-launch-checklist]] "Restored session and the PIN".
Mock-ups: "Tomale Profiles and PIN screens (009)" Design canvas (https://claude.ai/artifact/SBbqZ7ALuQRSauL9cNUUuE, 901–908); build follows [[build-ui-from-a-component-kit-with-a-screenshot-loop]].
-->

## Goal

A household can hand the device between parent and children safely. Anyone can switch profile from the header avatar; reaching a parent profile always needs the 4-digit PIN. Parents add, rename, re-avatar and delete child profiles, and set or change the PIN when it's first needed.

## Screen flow

- Header avatar (every profile, on every tab) → avatar menu sheet: Switch profile (everyone); parent also: Manage profiles, Settings, Help (Settings and Help keep today's behaviour).
- Profile picker (full screen): avatars and names, primary first. Opens from Switch profile; on a cold start with a restored session when the account has child profiles; and when the app returns after 15 minutes or more in the background.
- PIN pad (sheet over the picker): 4 digits; shown when the chosen profile is a parent profile.
- PIN locked screen: after `PIN_LOCKED`; "Email me a link to unlock".
- Set PIN (enter, then confirm): opens when first needed ([[ask-for-pin-when-first-needed]]): adding a child while `auth/me` says `pin_set: false`, or after an unlock link has cleared the PIN.
- Manage profiles (parent): list; Add child; tap a profile → Edit profile (name, avatar, Delete); Change PIN.
- Add / Edit profile: name, avatar picker (preset avatars with colour options, or a household character's picture).
- Delete confirmation: "Their stories will move to your profile."

## Scope (this slice only)

- Header avatar for every profile (returns for children; hidden since PR #23) using the profile's `avatar_key`; tapping opens the avatar menu.
- Switching: `POST /auth/select_profile {profile_id, session_id, pin?}` → new token saved through the existing session store (007); then refetch `auth/me`, clear profile-scoped caches (stories list, character counts) and land on Home. Tabs follow the new profile (parent five, child four).
- PIN pad: submits on the fourth digit (no button). Right PIN: the dots turn green with a tick for a moment, then Home (no modal). Wrong PIN: the dots clear (a short shake unless reduce motion is on) and "That's not right. N tries left" from `attempts_remaining`; fifth wrong → PIN locked screen. "Forgot PIN?" opens the same email screen with the title "Forgot your PIN?" (no separate page).
- PIN locked: `POST /auth/request_magic_link {email, purpose: "reset_pin"}`; confirmation "Check your email"; `RATE_LIMITED` shows "We've just sent one. Try again in a minute." The emailed link opens the app through the existing magic-link route (007); after completion `pin_set` is false, so the app shows Set PIN.
- Set PIN: `POST /users/me/pin {pin}`; two entries must match before sending. `EMAIL_NOT_VERIFIED` → "Verify your email first" with a resend option if the app already has one (else message only). Change PIN: `{pin, current_pin}`.
- Manage profiles: `GET /users/user_profiles`; Add child `POST /users/user_profiles {name, avatar_key}`, sent only when the parent taps the save button (labelled "Add [typed name]", disabled while the name is empty), so leaving the form never creates a profile; if Set PIN comes first, only the PIN is saved before the form; Edit `PATCH /users/user_profiles/{id} {name?, avatar_key?}`; Delete `DELETE /users/user_profiles/{id}`. Server refusals shown on the field or as a toast (codes below). The primary profile shows no Delete; the active profile can't be deleted.
- Avatars: `avatar_key` = `preset:<key>` or `character:<id>`. The picker offers active characters with a picture only (no archived characters, none still drawing) (Kyle, 17/11). If a `character:` avatar's character is later deleted or archived, show a preset fallback. With no such characters, the "Our characters" tab shows an empty state with no create button.
- Restored session: a cold start that restores a session on an account with child profiles shows the picker first, even if the token is for the parent; choosing the parent needs the PIN ([[pre-launch-checklist]]). Accounts without children skip the picker.
- 15-minute background rule: same as a restored session.
- Typed error responses: add an error response schema to the OpenAPI overlay (`payload.code`, `payload.message`, optional `payload.attempts_remaining`) and use it for every refusal in this slice.
- The 008 child device checks (child Characters view) run with this slice's device checks.
- Header bands run edge to edge under the status bar (fixes snag S-001 for these screens): one kit `ScreenHeader` whose height is the top safe-area inset plus its content, never a fixed height; utility screens use the compact form (back or close, title).
- Copy follows the design-system README (sentence case, warm, no jargon).

## Out of scope

- Approvals inbox, review, waiting card and the email deep-link resume (010). The avatar menu's Approvals entry and badge arrive in 010.
- Onboarding walkthrough (M7; it reuses Set PIN). Settings and Help content (M7).
- "Who's this story for?" assign (story detail is the bookshelf slice, 012).
- Biometric unlock; per-profile PINs; profile photos.

## State Management

Active profile comes from `auth/me` (`auth.active_profile`: id, name, is_child, is_primary) after every switch; nothing profile-scoped is trusted from before a switch. `store/profilesStore.ts` (Zustand): `profiles[]` (from `GET /users/user_profiles`), loading and error state; `lastBackgroundAt` for the 15-minute rule (memory only). PIN digits are never stored or logged (not in Sentry breadcrumbs).

## Endpoints (contracts in `api/openapi/xano.yaml` + overlay, regenerated by RS-2026-11-12-04)

GET /auth/me → 200: user {…, pin_set, pin_locked}, auth.active_profile {id, name, is_child, is_primary}.

GET /users/user_profiles → 200: Profile[] {id, name, is_child, is_primary, avatar_key, created_at}, primary first.

POST /auth/select_profile {profile_id, session_id, pin?} → 200 {authToken}. 400 `PIN_REQUIRED` | `PIN_INVALID` (+ `attempts_remaining`) | `PIN_LOCKED` | `PIN_NOT_SET`; 404 `PROFILE_NOT_FOUND`; 401 (session ended; treat as signed out).

POST /users/me/pin {pin, current_pin?} → 200 {pin_set: true}. 400 `PIN_FORMAT` | `PIN_REQUIRED` (change without current) | `PIN_INVALID` | `PIN_LOCKED` | `EMAIL_NOT_VERIFIED` | `PARENT_PROFILE_REQUIRED`.

POST /auth/request_magic_link {email, purpose: "reset_pin"} → 200 (same reply for unknown emails). 429 `RATE_LIMITED`.

POST /users/user_profiles {name, avatar_key?} → 200 Profile. 400 `NAME_NOT_ALLOWED` | `INVALID_NAME` (1–18 characters) | `INVALID_AVATAR_KEY` | `ACCOUNT_LIMIT_REACHED` (6 children) | `PIN_NOT_SET` | `PARENT_PROFILE_REQUIRED`.

PATCH /users/user_profiles/{id} {name?, avatar_key?} → 200 Profile + last_modified_at. 400 `NAME_NOT_ALLOWED` | `INVALID_NAME` | `INVALID_AVATAR_KEY` | `NOTHING_TO_UPDATE` | `PARENT_PROFILE_REQUIRED`; 404 `PROFILE_NOT_FOUND`.

DELETE /users/user_profiles/{id} → 200 {deleted: true, stories_moved}. 400 `CANNOT_DELETE_PRIMARY` | `CANNOT_DELETE_ACTIVE` | `PARENT_PROFILE_REQUIRED`; 404 `PROFILE_NOT_FOUND`.

GET /characters (default `status=active`) → household characters for the avatar picker; only those with `picture_status: ready` are offered.

Domain error codes are in `payload.code`; the user-facing text is `message` unless this PRD gives copy.

## Acceptance (Given/When/Then)

Happy path
- Given a parent with a PIN and one child profile
- When they switch to the child, then back to themselves with the right PIN
- Then each switch lands on Home with that profile's tabs and avatar, and the child sees only their own stories

Edge
- Given a parent with no PIN yet
- When they add their first child
- Then Set PIN opens first, and the child is created once the PIN is saved

Edge
- Given a restored session on an account with children (or the app back after 15 minutes in the background)
- When the app opens
- Then the picker shows, and choosing the parent needs the PIN

Error
- Given a child on the PIN pad
- When they enter a wrong PIN five times
- Then they see the tries left each time, then the locked screen; the unlock email's link clears the PIN and the parent sets a new one

Error
- Given a parent in Manage profiles
- When they try a blocked name, a seventh child, or deleting the primary or active profile
- Then the server's refusal shows on the field or as a toast and nothing changes

Device checks (Kyle, phone): switch parent → child → parent; wrong PIN to lock-out and email unlock; add, rename, re-avatar (preset and character) and delete a child (its stories move to the parent); kill and reopen the app with children (picker + PIN); background 15+ minutes; child header avatar; 008 child Characters checks; light and dark mode readable.
