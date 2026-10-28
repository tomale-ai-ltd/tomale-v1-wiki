---
type: plan
title: v1-audit
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-28
owner: vault
related:
  - "[[knowledge-architecture]]"
  - "[[knowledge-inventory]]"
  - "[[documentation-refresh-backlog]]"
---

# V1 audit (B7)

Every session note (43), decision (103) and PRD (10) read and traced to V1 features. Claims were checked against the live system where it was cheap to do so: the Xano mirror (`tomale-xano`, last sync 24/10 15:18) and the app repo (`wip/pre-restructure-2026-10-24`). This report feeds B8 (canonical docs, `v1-feature-map`, roadmap) and B9 (PRD reconciliation). Reviewed by Kyle on 28/10. His rulings are below and were applied on branch `b7-v1-audit`.

## Headlines

1. **The decisions are concentrated where the frontend isn't going next.** Of the 103 decisions, 30 concern store, print or payments (and 33 are purely process or testing). Characters (Slice 100) has 1, story chatbot (200) has 0, bookshelf/reader (300) has 3, and AI character creation (500) has 0. The next slices will raise most of their decisions during `/speckit.specify`, which is the right place, but Slice 100 has open questions to settle first (§7).
2. **Two PRDs contradict the system as built.** `PRD-Order-PoD-System` requires images to be generated only after payment or entitlement, but images are generated when the story is created. `PRD-Store-Orders` still names Mixam, uses old statuses, and has no cancellation window, refunds or approval gate. This is a product decision, not a doc fix (§6, P1).
3. **The subscription and entitlement system is the largest unbuilt V1 backend feature.** The PRD makes entitlements, usage counters, `GET /me/entitlements` and Apple/Google in-app purchase V1 requirements. None of it exists in Xano.
4. **Parental controls are half built.** The PIN gate on profile switching is accepted but not built, and the oversight approve/reject flow doesn't exist (P8). Separately, profiles have no PRD and six profile decisions exist only in session notes (§4, G1–G6). The unified `user_profiles` model, the profile caps, avatar presets, two-stage name moderation and the token-extras pattern are recorded only in sessions (§4).
5. **Eleven decision conflicts need your ruling (§2), and six notes need fixing in place (§3).** Most rulings are formalities. Three matter: URL schemes, dev/prod separation, and the branching model.

## Rulings (Kyle, 28/10)

| Item | Ruling | Applied as |
|---|---|---|
| C1 | Stripe Checkout opens in an in-app browser sheet that closes itself and returns to an in-app confirmation screen. Schemes per build: `tomalerntest://` for dev, `tomale://` for production, from one codebase. | [[return-from-stripe-checkout-via-in-app-browser-sheet]], [[use-per-build-variant-url-schemes]] (both supersede the old scheme notes) |
| C2 | Xano branches for dev/prod; env vars duplicated with suffixes where needed. | [[use-xano-branches-for-dev-and-prod]] (supersedes [[separate-dev-prod-environments]]) |
| C3 | Keep trunk-based; record the real naming. | [[name-branches-by-speckit-feature-number]] (supersedes [[trunk-based-git-branching]]) |
| C4–C7 | As proposed. | Dated amendments in the notes |
| C8 | As proposed (compatible). | B9: align PRD wording and field name |
| C9 | As proposed. Avatars are about 50 presets in `assets/avatars` with free commercial use; flexible avatars (even characters) are a future idea. | [[use-bundled-preset-avatars-for-profiles]] (accepted; supersedes the avatar deferral) |
| C10, C11 | As proposed. | Backlog (B12, B9) |
| PDFs | No downloadable PDFs; read in the e-reader, buy for a hard copy. | [[drop-library-and-pdf-download-from-v1]] |
| Characters | Name moderation runs in a custom function on create, which is why PATCH was removed. The chatbot (Slice 500) should know the character data model and prompt for richer descriptions, by Q&A or simple tap/swipe choices (hair length, eye shape). | B9 PRD input |
| Parental approval | Could take several forms: switch profile, push to the parent's device, email, push with PIN entry. | B9 input (open) |
| Pre-payment preview | E-reader preview with page swipe/scroll, including the cover and `order.message`. | [[use-e-reader-preview-before-order-payment]] |
| P1, P2 | Images are created in the app before any order; generation is limited by entitlements; preference is to launch with subscriptions. | [[gate-image-generation-with-entitlements-at-story-creation]] |
| P3, P5, P7, P8 | OK. | B8 roadmap, B9 PRDs |
| P4 | Phonics in V1 depends on how complex it is to reveal during text generation. | Open: B8 roadmap |
| P6 | Drop Library; reading progress only if there's no major backend overhaul. | [[drop-library-and-pdf-download-from-v1]] |
| §7 | Characters per profile; soft delete; no PATCH for now (it would need the profanity check); names moderated on create; drop `instant_stories_id`. | [[scope-characters-per-profile-with-soft-delete]] |
| §8 | OK. G1–G3 and G5–G9 filed as `proposed`; G4 accepted (C9). | 9 notes |

## 1. V1 features (provisional ids)

These are the ids for the `features:` frontmatter field. B8 formalises them in `v1-feature-map`. Counts are decisions tagged with each id (one decision can carry several).

| Id | Feature | PRD | Slice | Decisions | State in Xano |
|---|---|---|---|---|---|
| F-auth | Sign-up, login, verify email, magic link, refresh | V1 umbrella | 000 | 7 | Built, tested |
| F-onboarding | Walkthrough, account creation | V1 umbrella | ? | 0 | `complete_onboarding` endpoint only |
| F-account | Account settings, preferences, username, photo, support | V1 umbrella | ? | 5 | Built |
| F-profiles | Household profiles, child profiles, PIN gate, avatars | **none** | ? | 6 | Built, except the PIN gate on profile switch (no PIN field; `select_profile` has no check) |
| F-notifications | In-app alerts inbox, deep links, email; push deferred | V1 umbrella | ? | 4 | Inbox built |
| F-characters | Characters screen and CRUD | PRD-Characters | 100 | 1 | Partial (no PATCH, §7) |
| F-character-chatbot | AI-assisted character creation | PRD-Chatbot-Create-Character | 500 | 0 | Not started |
| F-story-create | Form-based create: themes, art styles, tags | V1 umbrella | ? | 0 | Themes/styles built; tags not |
| F-story-chatbot | Chatbot story creation | PRD-Chatbot-Story-Conversations | 200 | 0 | `conversations` table and message endpoint only |
| F-story-generation | AI text and image pipeline, moderation, status lifecycle | none (stack notes 13/14) | n/a | 6 | Built, slow (Phase 2) |
| F-parental-oversight | Approval of sensitive stories | PRD-Parental-Oversight | ? | 2 | Partial: flags and the order gate are built; no approve/reject endpoints |
| F-bookshelf | Bookshelf, story detail, e-reader, read-to-me, PDF | PRD-E-Reader | 300 | 3 | Stories built; `reading_logs` missing |
| F-store | Checkout, orders, cancel/refund | PRD-Store-Orders | 400 | 14 | Built, tested |
| F-print-fulfilment | PDF (Papermill), HPBC/Pureprint | PRD-Order-PoD-System | 400 | 15 | Built, tested |
| F-payments | Stripe, transactions, webhooks | PRD-transaction-webhooks | 400 | 12 | Book payments built; subscriptions not |
| F-subscriptions | Tiers, entitlements, in-app purchases | PRD-Subscription-Entitlement | ? | 1 | Not started |
| F-phonics | Phonics schemes and graphemes | **none** | ? | 0 | Tables and 2 endpoints built |

Cross-cutting (not features): `X-security` (14), `X-platform` (10), `X-testing` (11), `X-process` (23).

## 2. Decision conflicts (ruling needed)

| # | Decisions | Conflict | Evidence | Proposed ruling |
|---|---|---|---|---|
| C1 | [[use-custom-url-scheme-for-stripe-checkout-redirect-v1]] vs [[use-custom-url-scheme-for-app-deep-links-v1]] vs live | The first says `tomale://`; the second says `tomalerntest://`. Live Stripe redirects use neither: they go to `https://www.tomale.ai/checkout-stripe-success` and `…-cancelled`. | `app.json` scheme `tomalerntest`; mirror `stripe_create_checkout_session_GET.xs:74` | New decision: Stripe redirects use the https web intermediary (same pattern as magic link) until Universal Links. Supersede the Stripe scheme note. Keep `tomalerntest://` for dev builds and decide the production scheme pre-launch. |
| C2 | [[separate-dev-prod-environments]] vs [[knowledge-architecture]] §9 | The decision says separate Xano **instances**; the plan uses dev/prod **branches** in one workspace. | — | You decide. Branches are cheaper and are what the plan assumes; the instance split is stronger isolation (data, env vars). Supersede whichever loses. |
| C3 | [[trunk-based-git-branching]] vs practice | `feat/XXX-description` naming vs speckit `NNN-name`, plus `wip/`, `repo-sync/` and `b6/`. Ruleset now requires PRs and linear history. | Repo branches | New decision recording the actual model (speckit `NNN-` features, `repo-sync/`, `wip/`, PR to `main`, squash/rebase). Supersede. |
| C4 | [[adopt-rebac-auth-model]] vs [[ratify-users-id-as-ownership-field-standard]] | The rule is `WHERE owner_user_id = auth.user.id`; the field was ratified as `users_id`. | Mirror tables use `users_id` | Keep ReBAC accepted; add a one-line amendment pointing at the ratification. The model stands; only the field name changed. |
| C5 | [[prevent-deleting-active-profile-via-soft-delete]] vs the error-code convention (RS-01) | "Fails with 422" vs "400, Xano has no 422". Live preconditions use `error_type = "inputerror"` (400) with `error = 422` as the **message** in 14 places. | Mirror: `store_orders_POST`, `…PATCH` (4), `…cancel`, `user_profiles` POST (3), DELETE (2), PATCH (3) | Correct the note to "400 with code `CANNOT_DELETE_ACTIVE`". Add the stray `error = 422` messages to the pre-launch sweep. Harmless but misleading. |
| C6 | [[avoid-column-named-function-inputs-in-xano]] vs [[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]] | "Fix by renaming, not by enabling `enforce_hidden_fields`" vs the later sweep that enables it everywhere. | Session 15/10 vs 22/10 | Both stand: renaming is naming hygiene; the flag is the systematic guard. Amend the earlier note to drop "not by enabling". |
| C7 | [[run-real-fulfilment-cascade-against-staging-sku]] vs [[delay-hpbc-submission-with-30-minute-cancellation-window]] | The cascade described (DB trigger → `hpbc_create_order`) no longer exists. Submission now runs in the `hpbc_submit_due_orders` task after `submit_after`. | Mirror: `submit_after` in the Stripe webhook | Amend the mechanism line. The principle (real cascade, staging SKU, no simulated callback) stands. |
| C8 | [[formalise-story-status-lifecycle]] vs PRD-Parental-Oversight §2 | "Blocked set from moderation" vs "moderation outcomes do not change story lifecycle state". | — | Likely compatible: Blocked is a hard moderation fail, oversight uses flags. Confirm; then B9 aligns the PRD wording and the field name (`parental_approval_required`, not `parental_oversight_required`). |
| C9 | [[defer-explicit-profile-avatar-endpoint-until-kid-profiles]] vs session 29/06 | The trigger ("until kid profiles") has happened, and the approach changed: child avatars are bundled presets (`avatar_key`), with no upload. | Session 2026-06-29-001 | Supersede with the backfilled avatar decision (§4, G4). |
| C10 | [[place-frontend-development-on-hold]] | Still accepted; the frontend resumes after B12. | — | At B12, a new decision "resume frontend at Slice 100" supersedes it. |
| C11 | [[defer-documentation-refresh-until-after-phase-1-signoff]] | Its scope includes the retired `api-spec`; it is being carried out by B7–B9. | — | No change now; mark it done in the B9 close-out. |

## 3. Decision defects (fix in place)

| # | Note | Defect | Fix |
|---|---|---|---|
| D1 | [[defer-stripe-webhook-mode-branching-to-phase-2]] | Body is the Resend email-scoping text. | Restore the original body from the 07/05 chat: defer branching the Stripe webhook on `mode` (payment vs subscription) to Phase 2 with the transaction-webhooks build; `stripe/webhook_payment_confirmation` handles book orders only. |
| D2 | 4 notes dated `2025-01-01` (semver, dev/prod, trunk branching, ReBAC) | Placeholder date. Source docs (CTO tech review, DevTools stack note) carry no date. | Set `date: 2025-12-27` (CTO tech review period, same as the frontend hold) and note "date approximate" in the body. |
| D3 | [[add-order-status-guard-to-stripe-checkout]] and others | `affects`/body point at the retired `api-spec`. | Repoint to `security-model` once it exists (B8). |
| D4 | [[mark-order-error-on-hpbc-rejection-and-clear-lock]] | Accepted, but the body says the change is "proposed in the pending `.xs`". | Check the mirror's `hpbc_create_order` in B8; reword to past tense or flag as not built. |
| D5 | [[key-hpbc-environment-switch-off-stripe-test-mode]] | Field names "need reconciling" (`hpbc_sku_test` vs `hpbc_sku_staging`). | Check the generated `data-model.md` from B6; record the live name. |
| D6 | Most decisions | Empty second `---` block after the frontmatter (renders as a horizontal rule). | Remove it in the same pass as the `features` tags. |

## 4. Decisions made in sessions but never filed

These shape V1 features but exist only in session notes. I propose filing the first nine as **proposed** decisions for you to accept. The rest stay as session history.

| # | Decision (session) | Feature | File? |
|---|---|---|---|
| G1 | Unified `user_profiles` with `is_child` (Model B), replacing `user_child_profiles` (11/05) | F-profiles | Yes |
| G2 | Profile context in token extras (`active_profile`, `is_child`); `select_profile` updates `user_sessions` (08/05) | F-profiles, F-auth | Yes |
| G3 | Profile caps: 1 adult + 6 children, free; `is_child` immutable; the primary adult can't be deleted (29/06) | F-profiles | Yes |
| G4 | Child avatars are bundled presets (`avatar_key`, DiceBear CC BY 4.0, credited in-app); `users.profile_photo` retired in favour of profile avatars (11/05, 29/06) | F-profiles | Yes (supersedes C9) |
| G5 | Two-stage name moderation: word list as a signal, AI as the arbiter (29/06) | F-profiles, F-characters | Yes (Slice 100 may reuse it for character names) |
| G6 | Login lands on the primary profile (11/05) | F-profiles, F-auth | Yes |
| G7 | `store_orders`: SKU-level products; PATCH Draft-only; totals server-derived (03/07) | F-store | Yes |
| G8 | `transaction_webhook_events` is a generic ingress log; `transactions` is money-only (03/07) | F-payments | Yes |
| G9 | `artwork_style` returns the full catalogue and the client shows locked tiles (08/05) | F-story-create, F-subscriptions | Yes |
| G10 | Token-overwrite pattern: never decode the JWT client-side; `/auth/me` is the source of truth (11/05) | F-auth | No: partly superseded by refresh tokens and the 401 interceptor. B8 covers the current client auth model in `stack.md`. |
| G11 | Email verification pattern: single-use UUID token, 1-hour expiry, Squarespace page (11/05) | F-auth | No (implemented; B8 records it in `backend-xano`) |
| G12 | EAS env in `eas.json`, dashboard for secrets only (15/05) | X-platform | No (B8 `stack.md`) |
| G13 | Staging HPBC terminal status is Order Confirmed (13/10) | X-testing | No (B8 `test-suite.md`) |
| G14 | No completion alert for character creation in V1 (02/07) | F-notifications | No (B9 PRD-Characters) |
| G15 | Order number format `{id}-{yyyymmdd}-{users_id}-{instant_stories_id}` (16/04) | F-store | No (B8 `backend-xano`) |

## 5. PRD findings (input to B9)

| PRD | Conflicts with decisions or live system | Gaps |
|---|---|---|
| **V1 umbrella** | Tech stack: AsyncStorage → SecureStore; "AWS S3 via Xano vault" → Xano storage for V1 with S3 deferred; Make.com and DALL·E 3 → Xano-native OpenAI pipeline; "Testing: Manual" → Postman `_tests` + jest. "Settings — notifications" (MVP) vs push deferred post-V1. "Share / publish stories" vs no sharing in V1. | No profiles, parental oversight, subscriptions or phonics in the feature table. "Library" (V1 Must Have) is undefined. "Download / save as PDF": user-facing download not specified (PDFs today are print files made after payment). |
| **Characters** | `GET /characters?user_id=` (identity comes from the token, never input); PATCH listed but not built; "AI-assisted creation out of scope" vs PRD-Chatbot-Create-Character in V1 (Slice 500). | Profile- or account-level ownership; deletion model (§7); image regeneration ("Re-create image" is MVP in the umbrella PRD); character-name moderation. |
| **Chatbot-Create-Character** | Uses `story_conversations` (live table is `conversations`); `user_id` as input. | Moderation and entitlement gates on image generation. |
| **Chatbot-Story-Conversations** | Status `draft/in_progress/complete` vs live Draft → Preparing → In Queue → Done/Blocked; `story_conversations` vs `conversations`; `user_id` in the request body. | `tags`/`story_draft_tags` not built (custom tags are V1 Nice to Have); open question on email verification before creation. |
| **E-Reader** | `GET /instant_stories/{id}?include=pages` vs the curated detail projection. | `reading_logs` table and endpoint don't exist; child locked state for unapproved stories not in the flow. |
| **Parental-Oversight** | Field `parental_oversight_required` vs live `parental_approval_required`; C8. | Not built: approve/reject endpoints, single-use approval email tokens, approvals inbox. |
| **Store-Orders** | Mixam → HPBC/Pureprint; statuses; pricing "from Stripe" vs Xano as source of truth; push on confirm/ship vs push deferred. | 30-minute cancellation window, self-service refund, no cancel once in production, approval gate, tracking, gift message. The **pre-payment preview** that [[disallow-cancelling-personalised-orders-once-in-production]] relies on legally is unspecified and unbuilt. |
| **Order-PoD-System** | `orders`/`order_assets`/`payments` tables vs `store_orders`/`pdf_jobs`/`transactions`; state machine; image generation after payment (P1); refund policy vs [[split-refund-model-into-self-service-and-support-paths]]. | Regeneration cap; non-refundable image fee. |
| **Subscription-Entitlement** | Tiers inconsistent within the PRD (Free/Creator/Club vs `creator`/`delivery` vs Creator £6.99 / Book Delivery £20). | Everything unbuilt (P2). |
| **transaction-webhooks** | Endpoints `/webhooks/stripe` etc. vs the live `webhooks` group; dedup by `event_id` vs `dedup_key`; ack-unknown and ingest/processing responses are decided but not in the PRD; HPBC callbacks absent. | Subscription events, Apple, Google: unbuilt; [[defer-stripe-webhook-mode-branching-to-phase-2]]. |

## 6. Product gaps (your decisions, feed the roadmap in B8)

- **P1. When are images generated?** The PoD and Subscription PRDs gate image generation behind payment or entitlement ("no irreversible cost before payment"). Today every story generates images at creation. This decides the story-creation flow (Slice 200), the order flow (400) and the business model. It's the biggest open question in V1.
- **P2. Subscriptions and entitlements.** Is the full PRD (entitlements, counters, IAP) V1, or does V1 launch with book purchases only and subscriptions as a fast follow? This sets the roadmap size.
- **P3. Profiles PRD.** Write a short one (B9) from G1–G6 so profiles stop living in sessions.
- **P4. Phonics.** Built in Xano, absent from every PRD. Is it V1?
- **P5. Pre-payment preview.** Needed for the personalised-goods cancellation exemption. Specify it in PRD-Store-Orders.
- **P6. Library, PDF download, reading progress.** Define or drop them for V1.
- **P7. Rate limiting phase and backend observability.** Both are decided as launch requirements but are unestimated (roadmap).
- **P8. Parental controls are only half built.** [[parental-gate-on-profile-switch]] (PIN) is accepted but not built, and the oversight approve/reject flow doesn't exist. Both are child-safety and app-review items: they need a slot on the roadmap before any slice that lets a child profile reach parent content.

## 7. Slice 100 (Characters) readiness

Live `characters` table: account-scoped (`users_id`, no `user_profiles_id`); three overlapping deletion fields (`status` active/archived, `is_deleted`, `deleted_at`); `instant_stories_id`, `data_models_id`, `cover_image`. Endpoints: GET list, GET one, POST, DELETE, `characters/{id}/model` POST; no PATCH. Settle these before `/speckit.specify` (007):

1. Are characters shared across a household's profiles, or per profile like stories? Can a child see characters a parent made?
2. Which deletion model: archive (PRD), soft delete, or both? Reduce the three fields to one.
3. Edit: build `PATCH /characters/{id}` with an allowlist (PRD needs it), and decide whether regenerating the image is in Slice 100.
4. Should character names go through the two-stage name moderation (G5)?
5. Is the `instant_stories_id` column on `characters` still meaningful, given `instant_story_characters` exists?

## 8. On approval (B7 apply, branch `b7-v1-audit`)

1. Add `features:` to all 103 decisions (Appendix A) and the 10 PRDs; remove the empty `---` blocks (D6).
2. Fix D1 and D2; apply your rulings on C1–C9 (amend, or add `superseded_by` plus new notes).
3. File G1–G9 as `status: proposed`; you accept them in the PR review.
4. Add this report's B8 and B9 items to [[documentation-refresh-backlog]].
5. Move this report to `status: current`.

Sessions get no frontmatter changes (history). Appendix B records their effect instead.

## Appendix A. Decision → features

| Date | Decision | Features |
|---|---|---|
| 2025-01-01 | [[adopt-modified-semver-versioning]] | X-process |
| 2025-01-01 | [[adopt-rebac-auth-model]] | X-security |
| 2025-01-01 | [[separate-dev-prod-environments]] | X-platform |
| 2025-01-01 | [[trunk-based-git-branching]] | X-process |
| 2025-10-01 | [[adopt-spec-driven-development]] | X-process |
| 2025-12-27 | [[place-frontend-development-on-hold]] | X-process |
| 2026-05-07 | [[defer-stripe-webhook-mode-branching-to-phase-2]] | F-payments, F-subscriptions |
| 2026-05-07 | [[replace-sendgrid-with-resend-for-transactional-email]] | F-auth, X-platform |
| 2026-05-07 | [[use-custom-url-scheme-for-stripe-checkout-redirect-v1]] | F-store |
| 2026-05-15 | [[consolidate-xano-api-groups-into-app-and-webhooks]] | X-platform |
| 2026-05-15 | [[enforce-strict-env-validation-at-startup]] | X-platform |
| 2026-05-15 | [[migrate-image-storage-to-aws-s3-signed-urls]] | X-platform, F-characters, F-story-generation, F-account |
| 2026-05-15 | [[use-https-web-intermediary-for-magic-link-redirect]] | F-auth |
| 2026-05-21 | [[collapse-bool-preference-endpoints-into-users-me]] | F-account |
| 2026-05-21 | [[defer-explicit-profile-avatar-endpoint-until-kid-profiles]] | F-profiles |
| 2026-05-21 | [[enforce-server-side-image-validation]] | F-account |
| 2026-05-21 | [[make-username-user-editable]] | F-account |
| 2026-05-21 | [[separate-verify-email-deeplink-from-magic-link-path]] | F-auth |
| 2026-06-22 | [[fail-closed-active-profile-resolution]] | F-profiles, X-security |
| 2026-06-22 | [[parental-gate-on-profile-switch]] | F-profiles |
| 2026-06-22 | [[per-child-story-visibility]] | F-profiles, F-bookshelf, F-parental-oversight |
| 2026-06-22 | [[split-list-and-detail-projections]] | F-bookshelf |
| 2026-06-30 | [[adopt-openapi-import-for-postman-collection-sync]] | X-testing |
| 2026-06-30 | [[defer-push-notifications-until-post-v1]] | F-notifications |
| 2026-06-30 | [[prevent-deleting-active-profile-via-soft-delete]] | F-profiles |
| 2026-06-30 | [[remove-instant-story-reviews-endpoint]] | F-bookshelf |
| 2026-06-30 | [[remove-user-activities-endpoint]] | X-security |
| 2026-06-30 | [[rename-user-profiles-is-default-to-is-primary]] | F-profiles |
| 2026-06-30 | [[replace-support-requests-endpoint-with-mailto-ops-inbox]] | F-account |
| 2026-06-30 | [[scope-user-alerts-as-in-app-inbox]] | F-notifications |
| 2026-06-30 | [[use-action-url-for-user-alert-deep-linking]] | F-notifications |
| 2026-06-30 | [[use-custom-url-scheme-for-app-deep-links-v1]] | F-notifications, X-platform |
| 2026-07-14 | [[ack-unknown-webhook-event-types-with-200]] | F-payments |
| 2026-07-14 | [[adopt-unique-index-dedup-for-webhook-ingest]] | F-payments, F-print-fulfilment |
| 2026-07-14 | [[adopt-uuid-primary-key-for-transaction-webhook-events]] | F-payments |
| 2026-07-14 | [[differentiate-ingest-vs-processing-failure-responses-for-webhooks]] | F-payments, F-print-fulfilment |
| 2026-07-14 | [[elevate-backend-observability-to-launch-requirement]] | X-platform |
| 2026-07-15 | [[authenticate-hpbc-webhooks-with-shared-secret-bearer-token]] | F-print-fulfilment, X-security |
| 2026-07-15 | [[confirm-hpbc-webhook-dedup-key-format]] | F-print-fulfilment |
| 2026-07-15 | [[create-architecture-folder-for-system-flow-docs]] | X-process |
| 2026-07-15 | [[record-transactions-drop-checkout-session-object]] | F-payments |
| 2026-07-15 | [[scope-hpbc-callbacks-to-six-customer-facing-statuses]] | F-print-fulfilment, F-store |
| 2026-07-15 | [[split-refund-model-into-self-service-and-support-paths]] | F-store, F-payments |
| 2026-07-15 | [[store-money-as-integer-minor-units]] | F-payments |
| 2026-07-16 | [[ratify-users-id-as-ownership-field-standard]] | X-security |
| 2026-08-04 | [[defer-image-pipeline-throughput-to-phase-2]] | F-story-generation |
| 2026-10-08 | [[key-hpbc-environment-switch-off-stripe-test-mode]] | F-print-fulfilment |
| 2026-10-08 | [[run-real-fulfilment-cascade-against-staging-sku]] | X-testing, F-print-fulfilment |
| 2026-10-09 | [[avoid-recreating-removed-endpoints-for-testing]] | X-testing |
| 2026-10-09 | [[replace-manual-test-gates-with-bounded-polling]] | X-testing |
| 2026-10-09 | [[simulate-stripe-payment-with-signed-postman-webhook]] | X-testing |
| 2026-10-09 | [[use-fixture-story-for-order-flow-test]] | X-testing |
| 2026-10-12 | [[formalise-story-status-lifecycle]] | F-story-generation |
| 2026-10-12 | [[replace-long-done-poll-with-stuck-story-check]] | X-testing |
| 2026-10-12 | [[verify-stripe-checkout-totals-against-xano-prices]] | F-store, F-payments |
| 2026-10-13 | [[defer-postman-monitor-until-launch]] | X-testing |
| 2026-10-13 | [[make-hpbc-create-order-a-single-fail-closed-request]] | F-print-fulfilment |
| 2026-10-13 | [[omit-preflight-timescales-and-unit-prices-from-hpbc-orders]] | F-print-fulfilment |
| 2026-10-13 | [[purge-stuck-stories-with-manual-admin-function]] | F-story-generation |
| 2026-10-13 | [[store-hpbc-tracking-on-store-orders]] | F-store, F-print-fulfilment |
| 2026-10-14 | [[add-temporary-audit-trigger-on-store-orders]] | F-store, X-platform |
| 2026-10-14 | [[automate-full-refund-on-self-service-cancel]] | F-store, F-payments |
| 2026-10-14 | [[defer-documentation-refresh-until-after-phase-1-signoff]] | X-process |
| 2026-10-14 | [[delay-hpbc-submission-with-30-minute-cancellation-window]] | F-store, F-print-fulfilment |
| 2026-10-14 | [[disable-request-history-on-credential-functions]] | X-security |
| 2026-10-14 | [[disallow-cancelling-personalised-orders-once-in-production]] | F-store |
| 2026-10-14 | [[enforce-forward-only-hpbc-callback-status-transitions]] | F-print-fulfilment |
| 2026-10-14 | [[mark-order-error-on-hpbc-rejection-and-clear-lock]] | F-print-fulfilment, F-store |
| 2026-10-15 | [[avoid-column-named-function-inputs-in-xano]] | X-platform |
| 2026-10-15 | [[find-executor-runs-by-id-not-timestamp]] | F-story-generation, F-print-fulfilment |
| 2026-10-15 | [[restrict-store-orders-message-to-buyer-gift-message]] | F-store |
| 2026-10-21 | [[add-per-endpoint-rate-limiting-in-xano]] | X-security |
| 2026-10-21 | [[log-only-small-status-fields-in-executor-runs]] | X-security, F-story-generation, F-print-fulfilment |
| 2026-10-21 | [[make-simulate-test-switch-inputs-optional]] | X-testing |
| 2026-10-21 | [[return-401-invalid-refresh-token-from-auth-refresh]] | F-auth |
| 2026-10-21 | [[use-axios-401-interceptor-for-client-auth-session-handling]] | F-auth |
| 2026-10-21 | [[use-expo-secure-store-for-client-tokens]] | F-auth, X-security |
| 2026-10-22 | [[block-ordering-of-stories-awaiting-parental-approval]] | F-store, F-parental-oversight |
| 2026-10-22 | [[defer-workspace-hidden-fields-setting-to-pre-launch-sweep]] | X-security |
| 2026-10-22 | [[migrate-store-orders-money-fields-to-integer-pence]] | F-store, F-payments |
| 2026-10-22 | [[replace-dblink-inputs-with-explicit-allowlists]] | X-security |
| 2026-10-22 | [[use-run-scoped-postman-token-in-tests-login]] | X-testing |
| 2026-10-23 | [[add-order-status-guard-to-stripe-checkout]] | F-store, F-payments |
| 2026-10-23 | [[add-propose-only-reconcile-and-staleness-automations]] | X-process |
| 2026-10-23 | [[adopt-frontmatter-lifecycle-schema]] | X-process |
| 2026-10-23 | [[adopt-repo-vault-ownership-split-for-project-knowledge]] | X-process |
| 2026-10-23 | [[adopt-tiered-vault-structure-with-canonical-folder]] | X-process |
| 2026-10-23 | [[defer-postman-suite-ci-until-suite-split]] | X-testing |
| 2026-10-23 | [[generate-data-model-and-api-contract-from-xano]] | X-process |
| 2026-10-23 | [[keep-request-history-on-auth-endpoints-until-pre-launch]] | X-security, F-auth |
| 2026-10-23 | [[retire-obsidian-llm-wiki-plugin]] | X-process |
| 2026-10-23 | [[scope-agent-context-per-tool]] | X-process |
| 2026-10-23 | [[version-the-vault-with-git]] | X-process |
| 2026-10-24 | [[adopt-order-of-authority-for-project-knowledge]] | X-process |
| 2026-10-24 | [[classify-and-batch-repo-sync-changes]] | X-process |
| 2026-10-24 | [[consolidate-github-repos-in-tomale-ai-ltd-org]] | X-process |
| 2026-10-24 | [[follow-knowledge-architecture-stage-order-before-slice-100]] | X-process |
| 2026-10-24 | [[keep-agents-out-of-xano-no-mcp]] | X-process, X-security |
| 2026-10-24 | [[mirror-xano-workspace-to-github-read-only]] | X-process |
| 2026-10-24 | [[promote-pnpm-migration-ahead-of-slice-100]] | X-security, X-platform |
| 2026-10-24 | [[protect-speckit-and-generated-spec-documents]] | X-process |
| 2026-10-24 | [[relocate-project-folders-out-of-icloud]] | X-process |
| 2026-10-24 | [[upgrade-github-org-to-team-for-main-protection]] | X-process |

## Appendix B. Session → features

| Session | Features | Effect on V1 |
|---|---|---|
| 2026-04-14-001, 04-15-001 | X-process | LLM-wiki setup (retired, [[retire-obsidian-llm-wiki-plugin]]) |
| 2026-04-16-001 | F-story-generation, F-store, F-payments, X-security | ai_pipeline and commerce hardening; image jobs queued for the worker tick; order number format (G15); transactions CRUD removed |
| 2026-04-16-002 | X-process | Xano MCP research (superseded by [[keep-agents-out-of-xano-no-mcp]]) |
| 2026-04-17-001, 04-17-002 | X-process | Session-note automation |
| 2026-04-20-001 → 2026-05-07-002 (8 notes), 05-12-001, 05-14-001, 05-15-001 | none | Empty "no activity" runs |
| 2026-05-07-003 | F-payments, F-store, F-auth, X-security | Integrations hardening; Resend; Stripe redirect scheme (C1); webhook mode deferral (D1) |
| 2026-05-08-001 | F-profiles, F-story-create, X-security | `system` group; `select_profile` and token extras (G2); artwork catalogue (G9) |
| 2026-05-11-001 | F-profiles, F-auth | Unified `user_profiles` (G1); signup/login rebuild; email verification (G11); token overwrite (G10); login to primary (G6) |
| 2026-05-15-002 | F-auth, X-platform | Magic link; OpenAPI codegen; env validation; API groups; EAS env (G12) |
| 2026-05-21-001 | F-account, F-auth, F-profiles | `users` group restructure; verify-email deeplink; image upload |
| 2026-06-22-001 | F-profiles, F-bookshelf, F-parental-oversight | Per-child story visibility; profile backfill migrations |
| 2026-06-29-001 | F-profiles | Profile POST; caps (G3); avatar presets (G4); name moderation (G5) |
| 2026-06-30-001 | F-profiles, F-notifications, X-security | Profiles closed; `user_alerts`; endpoint removals |
| 2026-07-02-001 | F-notifications, F-phonics | Alerts closed; phonics endpoints; no character alert (G14) |
| 2026-07-03-001 | F-store, F-payments | `store_orders` refactor (G7); webhook ingress design (G8) |
| 2026-07-14-001 | F-payments, X-platform | Webhook events rebuild; Stripe payment webhook; observability as launch requirement |
| 2026-07-15-001 | F-payments, F-print-fulfilment | `transactions` restructure; HPBC callbacks; refund model |
| 2026-07-16-001 | F-payments, X-security, X-testing | Phase 1 items closed; `users_id` ratified; reconciliation task; Postman suite |
| 2026-08-03-001, 08-04-001 | F-story-generation | Image pipeline duplication fixes; throughput deferred to Phase 2 |
| 2026-09-14-001 | X-testing, F-story-generation | Flow-test harness |
| 2026-10-08-001 | F-print-fulfilment, X-testing | Fulfilment test design; HPBC environment switch |
| 2026-10-09-001 | X-testing, F-payments | Polling gates; signed simulated Stripe webhook |
| 2026-10-12-001 | F-store, F-story-generation, X-security | Checkout key leak fixed; price verification; story lifecycle |
| 2026-10-13-001 | F-print-fulfilment, F-story-generation, X-testing | Pureprint alignment; first green run; stuck-story purge; G13 |
| 2026-10-14-001 | F-store, F-print-fulfilment, F-payments | Cancellation window; self-service refunds; forward-only HPBC statuses |
| 2026-10-15-001 | F-store, X-platform | Hidden-fields overwrites; gift message; executor lookups |
| 2026-10-21-001 | F-store, F-auth, X-security | Cancel/refund tests; `auth/refresh` 401; SecureStore and 401 interceptor |
| 2026-10-22-001 | F-store, F-parental-oversight, X-security | Money in pence; dblink removal; approval gate |
| 2026-10-23-001 | X-security, X-testing, X-process | Phase 1 signed off (86/86); knowledge-architecture decisions |
| 2026-10-24-001 | X-process | Restructure B0–B5; GitHub organisation |
