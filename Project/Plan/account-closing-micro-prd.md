# account-closing -- Close your account, come back within 30 days, then delete #

<!--
Micro-PRD, DRAFT by Claude 19/11, not approved. Roadmap M7 (account, onboarding, notifications); App Store guideline 5.1.1(v) requires in-app account deletion. Speckit number decided when M7 is planned.
Sources: [[retain-account-data-30-days-after-closing]] (proposed 19/11), Terms §9 and Privacy Notice §7 (Claude Docs drafts 19/11), [[roadmap]] M7, [[pre-launch-checklist]] §1 (account deletion endpoint), [[backend-xano]] (soft delete with `deleted_at`), [[security-model]].
Needs a backend change set (B1–B5 below) built by Kyle in Xano before the app slice.
-->

## Goal

A parent can close the household's account from the app. Nothing is lost for 30 days, so signing in again in that time reopens it. After 30 days the account and everything in it is deleted from Tomale's systems, apart from the order and payment records the law makes us keep. The same job also finishes off items a parent deleted more than 30 days ago.

## Screen flow

- Settings (parent only, behind the PIN like other parent settings) → "Close account".
- Close account screen: what happens ("Your account, profiles, stories and characters will be kept for 30 days in case you change your mind, then deleted. Orders already being printed will still be delivered."), a warning if a subscription is active ("Cancel Creator or Book Club in your Apple or Google settings, or you'll keep being charged") with a button that opens the store's subscription page, then "Close my account" (destructive) and Cancel. Confirmation sheet: type or re-enter the PIN.
- Done: signed out, back to Sign in, with "Your account is closed. Sign in within 30 days to reopen it." Confirmation email sent.
- Signing in to a closed account within 30 days: "Reopen your account?" with the deletion date; "Reopen" restores everything; "Not now" signs out.
- After 30 days: sign-in fails as for an unknown account; a "Your account has been deleted" email goes out when the job runs.

## Backend (Kyle, Xano)

- **B1 `users.closed_at`** (timestamp, nullable) and `users.delete_after` (timestamp). Auth rules: a closed account can sign in only to reach reopen (`auth/login` and the magic link return `ACCOUNT_CLOSED` with `delete_after`, plus a short-lived token that can call reopen only), and refresh is refused.
- **B2 `POST /users/me/close`**: parent profile only (`PARENT_PROFILE_REQUIRED`), PIN required if set (`PIN_INVALID`); sets `closed_at = now`, `delete_after = now + 30 days`; revokes every `user_sessions` row; unsubscribes and deletes the HubSpot contact; sends the confirmation email (Resend). Returns `{closed_at, delete_after}`.
- **B3 `POST /users/me/reopen`**: allowed while `now < delete_after`; clears both fields; returns a normal session.
- **B4 scheduled task `purge_closed_accounts`** (daily): for each user past `delete_after`, delete `user_profiles`, `instant_stories` (and `instant_story_pages`, `instant_story_characters`), `characters`, `conversations`, `user_alerts`, `user_sessions`, uploaded and generated files (images, audio, PDFs), the RevenueCat subscriber, then the `users` row; keep `store_orders` and `transactions` (owner reference kept until the 6-year purge); send the "deleted" email first. Same task: hard-delete rows whose `deleted_at` is over 30 days old; delete `store_orders`/`transactions` over 6 years old; delete `moderation_flags` past the agreed retention. Idempotent, batched, logs counts to `executor_runs`, errors to Sentry.
- **B5 Postman `_tests`**: close → refresh refused; login → `ACCOUNT_CLOSED`; reopen restores; purge with a test clock (or `delete_after` set in the past) removes the rows and files and keeps the order.

## Scope (app, this slice)

- Settings row, Close account screen, PIN confirm, signed-out state with message, reopen prompt on sign-in, error codes `ACCOUNT_CLOSED`, `PARENT_PROFILE_REQUIRED`, `PIN_INVALID`.
- Subscription warning from the current plan (`/auth/me` or entitlements); deep link to Apple or Google subscription management.
- Copy follows the design-system README; never on a child profile.

## Out of scope

- Exporting data before closing (rights requests by email for now).
- Deleting one child profile (already in 009).
- Cancelling the store subscription for the parent (Apple and Google don't allow it).

## Acceptance (Given/When/Then)

Happy path
- Given a parent on their profile
- When they close the account and enter the PIN
- Then they're signed out on every device, get the email, and signing in within 30 days offers Reopen, which brings everything back

Edge
- Given a closed account 31 days later
- When the purge runs
- Then profiles, stories, characters and files are gone, the order records remain, and sign-in fails as for an unknown email

Error
- Given a child profile is active
- When anyone tries to reach Close account
- Then the PIN gate applies; the endpoint refuses with `PARENT_PROFILE_REQUIRED`

## Open questions (for Kyle)

1. Moderation record retention (decision note proposes 2 years).
2. Does Apple accept a 30-day grace period if the app states it clearly? Check guideline 5.1.1(v) and Apple's account-deletion guidance before App Review.
3. Xano backup period, so the Privacy Notice can state how long deleted data stays in backups.
