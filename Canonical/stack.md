---
type: living-doc
title: stack
project: tomale-rn-v1
status: current
version: 1.0
date: 2026-10-24
last_verified: 2026-10-28
owner: vault
related:
  - "[[backend-xano]]"
  - "[[observability]]"
  - "[[roadmap]]"
---

# Stack overview

One row per layer: what's used, what for, where its rules live, and its status on 28/10/2026. Checked against the app repo (`package.json`, `eas.json`, CI on `wip/pre-restructure-2026-10-24`) and the Xano mirror. Replaces the 15 April stack notes in `Project/_archive/stack/`. Engineering rules for the app stay in the [[Repos/tomale-rn-test/memory/constitution|constitution]]; where it is out of date, the repo-sync item is named.

| Layer | Technology | Used for | Rules live in | Status (28/10) |
|---|---|---|---|---|
| App framework | Expo SDK 54, React Native 0.81, managed workflow | iOS and Android app | constitution | In use |
| Routing | Expo Router 6 (file-based) | `(auth)`, `(onboarding)`, `(main)/(tabs)` route groups | constitution | In use (001) |
| UI | NativeBase (per constitution), Lucide icons, Reanimated 4, `expo-image` | Primitives, icons, animation, cached images | constitution | NativeBase **not yet installed**; decide at Slice 100 whether it stays |
| State | Zustand 5 with persist middleware | Auth, characters, stories stores | constitution | Scaffolding in place (005) |
| Client storage | AsyncStorage for persisted state; **`expo-secure-store` for tokens** | Tokens out of AsyncStorage | [[use-expo-secure-store-for-client-tokens]] | SecureStore **not yet installed**; constitution amendment queued (RS-01) |
| HTTP | Axios 1.9 + types generated from OpenAPI (`openapi-typescript`) | Calls to the `app` group | [[generate-data-model-and-api-contract-from-xano]], [[use-axios-401-interceptor-for-client-auth-session-handling]] | Client on `wip/` (006); 401 interceptor to build (M1) |
| Auth (client) | Xano JWE access token (1 h) + rotating refresh token | Session; never decode the token; `auth/me` gives profile context | [[security-model]] | Login and magic link screens exist |
| Backend | Xano (`tomale.ai` workspace, Launch plan) | API, database, auth, background tasks | [[backend-xano]] | Phase 1 signed off |
| AI | OpenAI: text and moderation (model per `data_models` record, e.g. `gpt-4o-mini`), images `gpt-image-1.5` (character consistency across pages is a known weakness), TTS `gpt-4o-mini-tts` | Stories, moderation, images, read-aloud audio | [[backend-xano]] | In use; throughput work later on Bedrock |
| Media storage | Xano file storage (public URLs) | Story, character and profile images; PDFs | [[migrate-image-storage-to-aws-s3-signed-urls]] | S3 + CloudFront signed URLs decided, not built |
| Payments | Stripe Checkout (books); in-app purchase for subscriptions (planned) | Book orders, refunds | [[backend-xano]] §4 | Books built; subscriptions not started |
| Print | HP Brand Centre / Pureprint, Papermill PDFs | Printed books | [[order-fulfilment-flow]] | Built (test SKU) |
| Email | Resend (transactional); HubSpot (marketing) | Verification, magic link, orders | [[replace-sendgrid-with-resend-for-transactional-email]] | Resend in use; domain verification pre-launch |
| Website | Squarespace (www.tomale.ai) | Email-verification, magic-link and checkout landing pages | — | In use |
| Observability | Sentry (`@sentry/react-native` ~7.2); Xano request history, `executor_runs` | Crashes and errors | [[observability]] | App done (004); backend reporting to build |
| Build and release | EAS (development, preview, production profiles), OTA via `expo-updates` | Builds, store submission, OTA | [[adopt-modified-semver-versioning]] | `eas.json` points at the old API group (`api:T6T6tF5a`): fix in M1 |
| CI | GitHub Actions: lint, typecheck, test on PRs to `main` | Quality gate | CTO plan §1 | Security stage (Gitleaks, Semgrep, audit) not yet added |
| Package manager | npm today → pnpm | Supply-chain safety | [[promote-pnpm-migration-ahead-of-slice-100]] | Migration queued (RS-03) |
| Tests | jest-expo (app); Postman `_tests` (backend) | Regression | [[test-suite]] | Backend suite 86/86 |
| Dev tools | Cursor (frontend agents), Claude (co-founder/review), GitHub (`tomale-ai-ltd`), Obsidian vault | Build and knowledge | [[operating-model]] | In use |

## Environments

- **App:** one codebase; build profile decides the scheme (`tomalerntest` for dev, `tomale` for production) and API base URL ([[use-per-build-variant-url-schemes]]). `config/env.ts` throws at startup if a required variable is missing ([[enforce-strict-env-validation-at-startup]]).
- **Backend:** one live Xano branch (`v1`) today; dev/prod branches planned ([[use-xano-branches-for-dev-and-prod]]). Per-user `test_mode` selects Stripe test keys and the HPBC test SKU.
