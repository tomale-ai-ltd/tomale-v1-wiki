# 010b-auth-signup -- Sign up, sign in, confirm email, name yourself #

<!--
Micro-PRD for speckit 010b, drafted by Claude 19/11, Kyle's answers 19/11 and review notes 23/11 folded in; approved by Kyle 23/11. Runs straight after 010, before M4 story creation.
Cursor copies it to `.docs/prd/010b-auth-signup.md` before `/speckit.specify`. No mock-ups: Cursor builds from the kit (Kyle, 19/11); visual differences go on [[snags]].
Why now: the app has no sign-up screen, so nobody outside the household can create an account (blocks a closed beta). A new account has `onboarding_complete = false`, and `app/index.tsx` sends it to the `(onboarding)` placeholder: a dead end.
Sources: [[1-prd-tomale-react-native-app-v1]] (F-auth; "email verification before creating"; "verify email → name the parent profile → set PIN"), [[PRD-Profiles]] §6–§7 (greyed-out lock), [[ask-for-pin-when-first-needed]], [[separate-verify-email-deeplink-from-magic-link-path]], [[use-https-web-intermediary-for-magic-link-redirect]], [[security-model]] (auth rows), [[snags]] S-003 and S-005 (logo rule).
Repo today (read 19/11): `app/(auth)/login.tsx` (platform buttons), `send-login-link.tsx`, `app/auth/complete.tsx`; no sign-up screen; no `auth/verified` route; `(onboarding)` is a placeholder. `users.username` is required and not unique; `users.email` is unique.
Kyle's answers 19/11: number 010b; username = first + last name; sign-up sends the verification email (dynamic send in a post-process custom function); no resend endpoint yet, can be added; existing email returns "this email has already been used, please use another"; password rule enforced by the table (min 8, at least 1 letter, at least 1 digit); creation blocked until confirmed, with the existing greyed-out lock; Termly links, tick-box.
-->

## Goal

A new parent can download the app, create an account, confirm their email, tell us their name and land on Home without help. Creating stories and characters waits until the email is confirmed. An existing parent signs in from a screen that looks like Tomale. The full onboarding walkthrough stays in M7.

## Screen flow

- Launch: the existing splash stays as it is, then opens Sign in when signed out, or the app when signed in (Kyle, 23/11).
- Sign in (restyled, replaces `login.tsx`): book mark logo (S-005 rule), email, password (show/hide), "Sign in" (kit Button, loading = full colour plus spinner, S-003), "Email me a sign-in link" (existing magic-link screen, restyled), "Forgot your password?" (same magic-link screen: no password reset in V1, `auth/reset_password` was deleted 12/11), and "New to Tomale? Create an account".
- Create account: first name, last name, email, password (show/hide; the rule "At least 8 characters, with a letter and a number" under the field, ticking off as it's met), tick-box "I agree to the [Terms] and [Privacy Notice]" (links open in the in-app browser; URLs in one config constant: Terms `https://www.tomale.ai/terms`, EULA `https://www.tomale.ai/eula`, Privacy Notice `https://www.tomale.ai/privacy-notice`, all live; the EULA link sits under the tick-box as "End-user licence agreement"); "Create account" stays disabled until every field is valid and the box is ticked. On success the session is stored exactly as after login (007 rules) and the app goes to Check your email.
- Check your email: "We've sent a link to [email]. Tap it to confirm your email address." Primary "Continue" (on to the Name step), "Send it again", and "Wrong email? Start again" (signs out, back to Create account).
- Email confirmed: the link opens the live Squarespace `/verify-email` page, which confirms the email and shows its own thank-you or "invalid verification link" page (Kyle, 23/11). The app learns about it by refetching `/auth/me` whenever it comes back to the foreground while unconfirmed; when `email_verified` turns true it shows the toast "Email confirmed" and unlocks creating. The app also handles `tomalerntest://auth/verified?status=success|error&reason=…` / `tomale://…` ([[separate-verify-email-deeplink-from-magic-link-path]]) the same way (refetch, toast on success; on error the confirm sheet with "Send it again"), so an "Open Tomale" button can be added to the thank-you page later without app changes. An expired or invalid link is handled by the web page; the app's "Send it again" covers it.
- Name step (replaces the `(onboarding)` placeholder while `onboarding_complete` is false): "What should we call you?", pre-filled with the primary profile's name (sign-up already names it from the first name; an empty field if the name is blank or "default"), optional picture with 009's avatar picker. "Continue" saves any change, completes onboarding, then opens Home.
- An existing account with `onboarding_complete = false` also lands on the Name step after sign-in.
- Creation gate while `email_verified` is false: every way into creating (the Create tab, "New character" on Home, the Characters "create" button, and "New story" once it exists) is drawn greyed out with the lock icon already used for child-locked items. Tapping one opens a sheet: "Confirm your email to start creating. We sent a link to [email]." with "Send it again" and OK. Reading, profiles and settings work as normal. Parent Home shows a slim banner "Confirm your email to start creating" (tap = same sheet) until confirmed.

## Scope (this slice only)

- `POST /auth/signup {first_name, last_name, username, email, password, sessionContext}`. `username` = first name + last name as typed, joined with a space (not unique in the table, not shown anywhere). `sessionContext` as for login.
- `POST /auth/login`, `POST /auth/request_magic_link`: restyled only.
- `GET /auth/me` on start, after sign-up, after the `auth/verified` return and when the app comes back to the foreground while unconfirmed: `email_verified`, `onboarding_complete`, `auth.active_profile`.
- Resend: `POST /auth/resend_verification` (backend B1 below). Button disabled for 60 seconds after a send, with "Sent. Check your inbox." Refusals show "Please wait a minute and try again."
- Name step: `PATCH /users/user_profiles/{primary id} {name, avatar_key?}` (009's call), then `POST /users/me/complete_onboarding`, then refetch `/auth/me`. If the PATCH succeeds and the complete call fails, the step stays with "Try again" and the name kept.
- `auth/verified` route reads `status` and `reason` only, then refetches `/auth/me`; never calls `verify_email` (the web page already did).
- Routing: the root layout moves from `<Slot />` to a `Stack` with `Stack.Protected` guards (expo-router 58.0.30): `(auth)` when signed out, the Name step when signed in with `onboarding_complete` false, `(main)` otherwise. Sign-in, sign-up and the Name step must never be reachable by Back once passed; this replaces the hand-built `replaceSignedIn` handover from 010 (`89ddcec`), keeping 010's saved-route resume and gate behaviour.
- Errors: the app checks the password rule and email format before sending, so the server's password error is a fallback ("That password doesn't meet the rule above"). Existing email (B3 `EMAIL_IN_USE`; sign-up already refuses it) → "There's already an account with this email" with "Sign in instead". Branch on `payload.code` (B3), never on message text. Login keeps the single "Invalid credentials" message. Anything else: "Something went wrong. Please try again."
- PIN is not asked here ([[ask-for-pin-when-first-needed]]).
- Copy follows the design-system README; British English.

## Backend (Kyle, before or during 010b)

- **B1 (needed): `POST /auth/resend_verification`**, auth required, no input: calls the existing verification custom function for `$auth.id` if `email_verified` is false; returns `{sent: true}`; refuses with `ALREADY_VERIFIED` if confirmed, and `TOO_SOON` if one was sent in the last 60 seconds (worked out from `email_ver_expires_at`, which is set to send time + 24 hours; no new column). Needed because the gate and the expired-link case otherwise leave a parent stuck.
- **B2 (in, Kyle 19/11): record acceptance.** `users.terms_accepted_at` (timestamp) and `terms_version` (text), sent by sign-up as `terms_accepted: true` and `terms_version` (the "Last updated" date printed on the published Terms: `2026-11-19`), refused without them. The app holds the current version in the same config constant as the URLs. Gives a record of what each parent agreed to and when.
- **B3 (in, Kyle 23/11): codes on sign-up refusals** (`EMAIL_IN_USE`, `TERMS_REQUIRED`; the password rule is enforced by the `users.password` field itself, so no code; a malformed email is refused by Xano's `email` input type before the stack, with no code, so the app checks the format first) at `payload.code`, like 009's typed refusals, so the app doesn't match on message text.
- **Pre-launch, not 010b:** the same `email_verified` check on the create endpoints (characters, stories), so the gate isn't app-only. Add to [[pre-launch-checklist]].
- Then `pnpm update:openapi` and an overlay entry for B1 (and B2/B3 if done), with recorded Postman fixtures.

## Design notes

- No mock-ups: kit components only. Auth screens have no `ScreenHeader` (no profile yet). Light and dark.
- Keyboard: fields scroll above the keyboard; Return moves to the next field; the last field submits. Email field: email keyboard, no autocapitalise or autocorrect. Autofill hints: email (`username`/`emailAddress`) and new password (`newPassword`) on Create account, current password on Sign in, so iOS and Android offer to save and fill the password.
- No system pop-ups are involved: the tick-box is in-app; there's no tracking prompt (we don't track), and no push permission in this slice.

## State Management

No new store. The session goes through 007's `AuthStore` and SecureStore as login does; `email_verified` and `onboarding_complete` come from `/auth/me` as today. The resend cooldown lives in memory. The Name step reads the primary profile from 009's `profilesStore`.

## Endpoints

POST /auth/signup (public) `{first_name, last_name, username, email, password, terms_accepted, terms_version, sessionContext}` → 200 `{userid, authToken, refreshToken, session_id}`; 400 `EMAIL_IN_USE` | `TERMS_REQUIRED` (plus Xano's own input errors for a malformed email or a password that fails the field rule).

POST /auth/resend_verification (B1, auth) → 200 `{sent: true}`; 400 `ALREADY_VERIFIED` | `TOO_SOON`.

POST /auth/login · POST /auth/request_magic_link · POST /auth/complete_magic_link: unchanged.

GET /auth/me → `user.email_verified`, `user.onboarding_complete`, `auth.active_profile`.

PATCH /users/user_profiles/{user_profiles_id} → 009 shape. POST /users/me/complete_onboarding → 200 `{}`.

## Acceptance (Given/When/Then)

Happy path
- Given a person with no account
- When they create an account, confirm the email from the phone's Mail app, give their name and tap Continue
- Then Home opens with "Hello [name]", the primary profile is named [name], and creating is unlocked

Edge
- Given a new account that hasn't confirmed its email
- When the parent taps the Create tab or "New character"
- Then nothing opens; the confirm-your-email sheet shows, and "Send it again" sends a new email (then waits 60 seconds)

Error
- Given an email that already has an account
- When someone tries to create an account with it
- Then they see "There's already an account with this email" with "Sign in instead", and no second account is made

Device checks (Kyle, phone): new account with a new email; Terms and Privacy open and close; tick-box required; password rule ticks off; confirm from Mail, then return to the app (toast and unlock); expired link (web page message, then Send it again); resend and the 60-second wait; locked Create tab and "New character" before confirming, unlocked after; leave and reopen between sign-up and the Name step (lands on Name); existing email; wrong password; magic-link sign-in; password manager offers to save; light and dark; small and tall phone.

## Out of scope

- The onboarding walkthrough, "add your first child" prompt and PIN step (M7).
- Sign in with Apple or Google (only required if a third-party login is offered).
- Account deletion (App Store requirement, M7), changing email or password, password reset by code.
- Marketing-email consent (add as a separate, unticked box when there's a mailing list).
- Universal Links (the web intermediary stays).

## Open questions (for Kyle)

None. Terms published 19/11/2026 at `https://www.tomale.ai/terms`, so `terms_version` = `2026-11-19`; Privacy Notice at `https://www.tomale.ai/privacy-notice` ([[Project/Legal/README|Legal README]]).
