# auth-signup -- Sign up, sign in, confirm email, name yourself #

<!--
Micro-PRD, DRAFT by Claude 19/11, not approved. Speckit number to decide (see Open questions); goes straight after 010, before M4 story creation.
Why now: the app has no sign-up screen, so nobody outside the household can create an account, which blocks any closed beta after the Slice 100 checkpoint. Also, a new account has `onboarding_complete = false`, and `app/index.tsx` sends it to the `(onboarding)` placeholder: a dead end.
Sources: [[1-prd-tomale-react-native-app-v1]] (F-auth, "verify email → name the parent profile → set PIN"), [[PRD-Profiles]] §7, [[ask-for-pin-when-first-needed]], [[separate-verify-email-deeplink-from-magic-link-path]], [[use-https-web-intermediary-for-magic-link-redirect]], [[security-model]] (auth rows), [[snags]] S-003 and S-005 (logo rule).
Backend: all endpoints below are built and tested (Postman `_tests`); no Xano change expected unless an open question says otherwise.
Repo today (read 19/11): `app/(auth)/login.tsx` (email + password, platform buttons), `send-login-link.tsx` (magic link), `app/auth/complete.tsx` (magic-link return); no sign-up screen; no `auth/verified` route; `(onboarding)` is a placeholder.
-->

## Goal

A new parent can download the app, create an account, confirm their email, tell us their name and land on Home, without help. An existing parent signs in from a screen that looks like Tomale. The full onboarding walkthrough stays in M7; this slice is the minimum to get a stranger in.

## Screen flow

- Sign in (restyled, replaces `login.tsx`): book mark logo (S-005 rule), email, password (show/hide), "Sign in" (kit Button, loading = full colour plus spinner, S-003), "Email me a sign-in link" (existing magic-link screen, restyled), "Forgot your password?" (goes to the same magic-link screen: there is no password reset in V1, `auth/reset_password` was deleted 12/11), and "New to Tomale? Create an account".
- Create account: first name, last name, email, password (show/hide, the rule shown under the field), the terms and privacy line (see Open questions), "Create account". On success the session is stored exactly as after login (007 rules) and the app goes to Check your email.
- Check your email: "We've sent a link to [email]. Tap it to confirm your email address." Primary "Continue"; the parent can carry on without confirming (see Open questions for any gate). Secondary "Wrong email? Start again" signs out and returns to Create account.
- Email confirmed return (`tomalerntest://auth/verified?status=success|error&reason=…` / `tomale://…`): a new route, separate from `auth/complete`. Success: toast "Email confirmed" and carry on to wherever the person was (Name step or Home). Error, expired: "That link has expired" plus how to get a new one; other errors: "We couldn't confirm your email".
- Name step (replaces the `(onboarding)` placeholder, shown while `onboarding_complete` is false): "What should we call you?" with the name field filled with nothing (the primary profile starts as "default"; never show "default"). Optional picture using 009's avatar picker. "Continue" renames the primary profile, then completes onboarding, then opens Home.
- An existing account with `onboarding_complete = false` (signed in on another device, or left halfway) also lands on the Name step.

## Scope (this slice only)

- `POST /auth/signup {first_name, last_name, username, email, password, sessionContext}` → `{authToken, refreshToken, session_id, userid}`. `username` is required by the endpoint; the app sends the email (Open question 2). `sessionContext` as for login.
- `POST /auth/login` (existing) and `POST /auth/request_magic_link` (existing), restyled only.
- `GET /auth/me` after sign-up and on start: `email_verified`, `onboarding_complete`, `auth.active_profile` (primary).
- Name step: `PATCH /users/user_profiles/{primary id} {name, avatar_key?}` (009's call and checks), then `POST /users/me/complete_onboarding`, then refetch `/auth/me` so the gate in `app/index.tsx` sends the person to Home. If the PATCH succeeds and the complete call fails, the step stays with "Try again" and the name kept.
- `auth/verified` route: reads `status` and `reason` only; never calls `verify_email` (the web page already did).
- Errors: show the server's message for sign-up input errors (email already in use, password rule) mapped to plain copy; login keeps the single "Invalid credentials" message (no hint whether the email exists). Codes to confirm from a live response (Open question 3).
- Copy follows the design-system README; British English; no exclamation marks on errors.
- PIN is not asked here: it is asked when first needed ([[ask-for-pin-when-first-needed]]).

## Design notes

- No mock-ups yet (Open question 4). Kit components only: `ScreenHeader` is not used on auth screens (no profile yet); fields, Button and links from the kit; light and dark.
- Keyboard: fields scroll above the keyboard; Return moves to the next field; the last field's Return submits. Email field: email keyboard, no autocapitalise, autofill hints for email and new password (iOS password manager).

## State Management

No new store. The session goes through 007's `AuthStore` and SecureStore exactly as login does. The sign-up form keeps its state in the screen; nothing persisted. The Name step reads the primary profile from 009's `profilesStore`.

## Endpoints

POST /auth/signup (public) → 200 `{userid, authToken, refreshToken, session_id}`; 400 input errors.

POST /auth/login (public) · POST /auth/request_magic_link (public) · POST /auth/complete_magic_link (public): unchanged.

GET /auth/me → `user.email_verified`, `user.onboarding_complete`, `auth.active_profile`.

PATCH /users/user_profiles/{user_profiles_id} → 009 shape. POST /users/me/complete_onboarding → 200 `{}`.

## Acceptance (Given/When/Then)

Happy path
- Given a person with no account
- When they create an account, tap "Continue", give their name and tap "Continue"
- Then Home opens with "Hello [name]", and the primary profile is named [name], not "default"

Edge
- Given a new account that hasn't confirmed its email
- When the person taps the link in the email on the phone
- Then the app opens, shows "Email confirmed" and carries on where they were; `/auth/me` reports `email_verified: true`

Error
- Given an email that already has an account
- When someone tries to create an account with it
- Then they see "There's already an account with this email" with a "Sign in instead" link, and no second account is made

Device checks (Kyle, phone): create an account with a new email; confirm it from the Mail app on the phone (dev scheme); leave and reopen the app between sign-up and the Name step (lands on the Name step); expired verification link; existing email; wrong password; magic-link sign-in; password manager offers to save the new password; light and dark; small and tall phone.

## Out of scope

- The onboarding walkthrough, "add your first child" prompt and PIN step (M7).
- Sign in with Apple or Google (only needed if we add a third-party login; email and password don't trigger Apple's rule).
- Account deletion (App Store requirement, M7), changing email or password, password reset by code.
- Universal Links (the web intermediary stays).

## Open questions (for Kyle)

1. **Number and slot:** take 011 and move story creation to 012 (the 010 copy says "Coming soon until 011", which is only a label), or call this one 010b to leave the later numbers alone.
2. **`username`:** the sign-up endpoint requires it but nothing in the app uses it. Send the email as the username (no Xano change), or make it optional in Xano.
3. **Backend checks (Kyle in Xano or Postman):** does `auth/signup` send the verification email itself, and through which template? Is there an endpoint to resend it (none in the client today)? What does an existing email return (code and message)? Is there a password rule enforced server-side?
4. **Verification gate:** the app PRD has "email verification before creating" as Must Have. Gate story and character creation on `email_verified` in this slice, or leave the gate for M4/M7 and only nudge here?
5. **Terms and privacy:** do we have terms and privacy URLs to link on Create account, and is a tick-box needed (UK GDPR, a parent creating an account for a child's data), or is "By creating an account you agree to…" enough?
6. **Mock-ups:** draw three boards (Sign in, Create account, Name step) on the Design canvas before specify, or go kit-only and log visual differences on [[snags]].
