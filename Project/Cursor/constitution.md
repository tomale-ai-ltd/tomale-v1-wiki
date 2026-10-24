---
type: foundation
title: constitution
project: tomale-rn-v1
status: current
date: 2026-04-14
---

<!--

Sync Impact Report

- Version change: 1.3.0 → 1.4.0

- Modified sections:

✅ Core Principles — Principle 5 expanded with crash reporting, error boundaries, and OTA update requirements

✅ Additional Constraints & Technology Standards — updated Expo SDK to 54; added DevOps & CI/CD standards; added Observability standards

✅ Development Workflow & Quality Gates — added CI/CD gate and branch protection requirements

- Added sections: none

- Removed sections: none

- Templates requiring updates:

✅ specs/003-foundations-devops/spec.md — DevOps standards now documented in constitution

✅ specs/004-foundations-observability/spec.md — Observability standards now documented in constitution

- Follow-up TODOs:

- Harden /instant_stories to require Authorization; add client interceptor in HTTP slice

- Configure Renovate/Dependabot for automated dependency updates (mentioned in 003 spec, not yet implemented)

-->

  

# Tomale-rn-v1 Constitution

  

## Core Principles

  

### 1. Safety, Privacy, and Moderation (NON-NEGOTIABLE)

- All content involving children MUST pass automated and manual moderation before sharing/export.

- The app MUST implement privacy-by-design: collect minimum data, store only what is necessary,

and use anonymization/pseudonymization for analytics.

- Compliance with COPPA and GDPR-K MUST be observed; parental consent flows are REQUIRED where

applicable.

- Media and PII MUST be retained only as long as required for functionality; deletion/export

requests MUST be honored.

Rationale: Although the app is designed to be used principally by parents FOR their children, the audience may include children ages 0–7; so safety and privacy are foundational.

  

### 2. Assistant-Style UX and Accessibility

- The UX MUST be conversational and guided, supporting step-by-step story & character creation via the chatbot feature.

- Accessibility MUST include large tap targets, high-contrast theming, dynamic type, and voice-

friendly flows. Text-to-Speech (Expo Speech) integration is PLANNED and tracked.

- E-reader controls MUST support landscape via Expo Screen Orientation where needed. This will be enforced in the UI when e-reader view is launched.

Rationale: Parents, caregivers, and young children benefit from simple, guided, and accessible flows. Stories are visually more appealing in landscape mode.

  

### 3. Character Consistency and Story Continuity

- Story and illustration generation MUST maintain consistent characters across steps and sessions

(e.g., seeds, prompts, and state saved per character).

- Users MUST be able to re-use characters and styles in new stories; persistence MUST survive reloads.

- Outputs MUST be reproducible given the same inputs and saved state where the backend permits.

Rationale: Consistent, magical characters are core to the product’s delight and brand.

  

### 4. Offline-First Reliability and Sync

- Global state MUST use Zustand with persist middleware; AsyncStorage is the persistence layer for

auth tokens, preferences, and lightweight data.

- The app MUST operate with degraded but functional offline behavior; network calls to Xano MUST be

idempotent where feasible, with retries, backoff, and safe pagination.

- Critical user actions (create, edit, read) MUST provide clear optimistic UI and conflict handling

guidance.

Rationale: Parents and kids frequently use the app on the go; offline resilience is required.

  

### 5. Quality, Observability, and Versioning

- Errors MUST be surfaced with user-appropriate messaging and captured with structured logs.

- Crash reporting MUST use privacy-preserving tools (e.g., Sentry) with PII scrubbing enabled.

- Root error boundaries MUST provide friendly fallback UI; crashes MUST NOT expose stack traces to end users.

- Crash events MUST be tagged with app version for correlation.

- Key flows (auth, story creation, illustration generation, reading) MUST have automated checks

(unit/integration or E2E, as feasible for RN/Expo).

- Breaking changes MUST follow semantic versioning; user-visible changes MUST be documented.

- Analytics MUST be privacy-preserving; no tracking of children's PII.

- OTA updates SHOULD be enabled for rapid hotfixes; background checks MUST not block app startup.

Rationale: Reliability and trust are essential to family experiences and physical book conversion.

  

## Additional Constraints & Technology Standards

  

- UI Components: NativeBase for UI primitives; Lucide React Native for icons.

- Navigation: Expo Router for file-based routing on top of React Navigation (stacks, tabs, modals).

- State: Zustand + Persist Middleware; AsyncStorage for local persistence.

- Animation & Interaction: React Native Reanimated, Gesture Handler; Lottie for micro-animations.

- Core Expo SDK: Expo SDK 54; Splash Screen, Font, and System UI for startup visuals and typography;

Screen Orientation for reader modes; Expo Speech and Notifications are PLANNED.

- Backend Integration: Xano REST API for auth, stories, orders, and AI orchestration; Axios/Fetch

with interceptors for auth, error handling, and retries.

- Developer Tools: Cursor IDE + SpecKit for specification driven development and documentation generation.

  

Standards (MUST):

- Use Expo Router file-based routing under `app/` with groups like `(auth)`, `(main)`, and modals.

- Use Axios interceptors for auth headers and consistent error normalization.

- Persist auth tokens and preferences only; never store sensitive child PII beyond what is required.

- Keep animations smooth (target 60fps where possible); avoid blocking the JS thread.

- Canonical API contract path is `api/openapi/xano.yaml`; generate types client with `npm run update:openapi` which outputs to `api/client.ts`.

- Data Model Source of Truth: `.specify/memory/data-model.md` MUST mirror the Xano schema. Any backend schema change MUST be reflected in this document and the OpenAPI file.

- Auth routing MUST rely on `/auth/me` for onboarding state; fallback endpoints MUST NOT be used for routing decisions.

- Runtime configuration SHOULD provide the backend base URL via `EXPO_PUBLIC_API_BASE_URL`; default to the OpenAPI server URL if unset.

- Content endpoints SHOULD require Authorization; clients attach Bearer tokens via interceptors.

- DevOps & CI/CD:

- Node version MUST be pinned in `.nvmrc`; CI MUST use this version.

- CI gates MUST run sequentially: lint → typecheck → unit tests (Jest).

- Pre-commit hooks MUST run `lint-staged` (eslint, prettier) on staged files.

- Main branch MUST be protected: PR required, passing CI checks, ≥1 review.

- Dependency versions SHOULD be pinned (exact versions preferred for runtime deps).

- Single lockfile (`package-lock.json`) is authoritative and MUST be checked in.

- Observability:

- Sentry (@sentry/react-native) for crash reporting; PII scrubbing via `beforeSend` hook.

- Error Boundaries: Root `Sentry.ErrorBoundary` MUST wrap app shell; fallback UI MUST be user-friendly.

- OTA Updates: Expo Updates for over-the-air updates; background check on app start (non-blocking).

- Source Maps: CI SHOULD upload source maps to Sentry for production releases (release id: `<version>+<shortsha>`).

Note: Source map upload functionality is intended but not active until EAS builds are performed.

  

## Development Workflow & Quality Gates

  

- Constitution Check GATE (Phase 0): every plan/spec MUST confirm alignment with Principles 1–5.

Include explicit notes on: moderation/privacy approach, accessibility, character continuity,

offline-first behavior, and API idempotency.

- Contracts & Data Model GATE: confirm `.specify/memory/data-model.md` matches the current Xano schema and `api/openapi/xano.yaml`; confirm `npm run update:openapi` has been run and `api/client.ts` updated.

- Confirm `/auth/me` includes `onboarding_complete` (and any UI-dependent fields such as `first_name`).

- Planning: Use `/speckit.plan` and `/speckit.spec` to author `plan.md` and `spec.md`. User stories

MUST be independently testable and prioritized (P1, P2, P3...).

- Tasks: Use `/speckit.tasks` to generate user-story-grouped tasks; tests are optional unless the

constitution marks a flow as critical.

- Reviews: PRs MUST show Constitution Check evidence; reviewers MUST block on violations or provide

documented exceptions with rationale.

- CI/CD GATE: All PRs MUST pass CI gates (lint, typecheck, tests) before merge.

- Branch Protection: Direct pushes to `main` MUST be blocked; all changes via PR.

- CODEOWNERS: Repository MAY include CODEOWNERS file to enforce review requirements for `specs/` vs `app/` code (optional).

- Code Quality: TypeScript strict mode where applicable; ESLint/Prettier; avoid deep component

nesting; prefer predictable state transitions.

- Documentation: Update README or docs with any user-visible changes and feature quickstarts.

  

## Governance

  

- Authority: This constitution supersedes other practices where conflicting.

- Amendments: Propose changes via PR updating this file; include migration/retrofit notes. Approval

requires at least one maintainer review.

- Versioning: Semantic versioning for this document.

- MAJOR: Backward-incompatible governance/principle removals or redefinitions.

- MINOR: New principle/section added or materially expanded guidance.

- PATCH: Clarifications and non-semantic refinements.

- Compliance: Every feature’s plan/spec/review MUST reference the Constitution Check. Exceptions

MUST be documented with scope and sunset date.

- Changes to the constitution must be explicitly approved by the document owner

- Backend schema change procedure (REQUIRED for merge): 1) update `.specify/memory/data-model.md`; 2) export/update `api/openapi/xano.yaml`; 3) run `npm run update:openapi` to refresh `api/client.ts`.

  

**Version**: 1.4.0 | **Ratified**: 2025-10-21 | **Last Amended**: 2025-11-14 | **Document Owner**: Kyle Burke