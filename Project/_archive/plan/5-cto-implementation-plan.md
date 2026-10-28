---
type: plan
title: 5-cto-implementation-plan
project: tomale-rn-v1
status: historical
version: 1.1
date: 2026-04-14
last_verified: 2026-10-24
owner: vault
superseded_by: "[[roadmap]]"
---

> **Archived 28/10/2026 (B8).** Superseded by [[roadmap]], which carries every open item from this plan.

---

# CTO Improvements — Implementation Plan

> This plan defines the detailed requirements and phased implementation order
> for addressing findings from the CTO technical review.
> Development in Cursor was paused to implement these before continuing with
> feature slices.

---

## Requirements

### 1. CI / DevSecOps Foundations

#### 1.1 CI Baseline (retain existing)
- Maintain current CI steps: `npm ci`, lint, typecheck, test

#### 1.2 Dependency Security
- Add dependency vulnerability scanning to CI using `npm audit` (or `pnpm audit`
  post-migration)
- Configure to fail on `high` and `critical` vulnerabilities only
- Enforce `minimumReleaseAge = 7 days` when using pnpm
- Avoid installing newly published packages immediately

#### 1.3 Secrets Management
- Integrate Gitleaks into CI pipeline — fail build on detected secrets
- Run initial full-repo scan and rotate any exposed secrets
- Optional: add Gitleaks as pre-commit hook to prevent secrets entering git history

#### 1.4 Static Application Security Testing (SAST)
- Integrate Semgrep (open source) into CI
- Use OWASP Top 10 rule set
- Configure to fail on high severity issues only (initially)

#### 1.5 CI Enforcement & Structure
- Make CI checks mandatory for merge into `main`
- Refactor CI into logical jobs:
  - `install`
  - `lint + typecheck`
  - `test`
  - `security` (audit + gitleaks + semgrep)

#### 1.6 Testing (Initial Position)
- Keep test step in CI
- Do NOT enforce coverage thresholds yet
- Add placeholder for future coverage reporting (non-blocking)

---

### 2. API, Authentication & Authorization

#### 2.1 Authentication Enforcement
- Require authentication on all endpoints by default
- Explicitly allow unauthenticated access only for:
  - auth endpoints (login, signup, OTP, magic link)
  - validated webhooks
  - explicitly public content endpoints (if any)

#### 2.2 Identity Handling (Critical)
- Remove all user identifiers from request inputs (`user_id`, `users_id`,
  email-based targeting)
- Replace with `auth.user.id` derived from authentication context only

#### 2.3 Authorization Model (Owner-Based)
- Implement strict owner-based access control across ALL user-owned data:
  `WHERE owner_user_id = auth.user.id`
- Apply to: characters, stories, pages, orders, subscriptions, etc.

#### 2.4 Child Profile Access Model
- All data owned by parent user (`owner_user_id`)
- Child profiles do not own data and do not authenticate independently
- Each content record must include child visibility reference:
  - `child_profile_id` (single) or `visible_to_child_profiles[]` (multi)
- Parent access: `WHERE owner_user_id = auth.user.id`
- Child access: `WHERE owner_user_id = auth.user.id AND child_profile_id = selected_child_profile`
- Content assignment handled during creation or via simple edit controls
- No dedicated sharing or permissions interface required for V1
- Future extensibility (do NOT build now): public library, cross-user sharing,
  fine-grained permissions

#### 2.5 API Surface Reduction

> **TO DO**: Create spreadsheet listing all Xano tables as rows with columns:
> `table | used by app | exposure type | C | R | U | D | endpoint type | should exist?`
[[security-model]]

- API endpoints should represent application capabilities, not database tables
- Do NOT expose CRUD endpoints for all tables by default
- Only expose endpoints required by frontend or external integrations
- Tables not required by frontend: accessible only via backend functions,
  not via public API
- Replace generic CRUD with purpose-built endpoints:
  - Use `GET /phonics/by-stage/{id}` not `GET /phonics_exceptions`

#### 2.6 Endpoint Security Rules
- User endpoints: require authentication + enforce ownership filtering
- System endpoints (workers): use internal API key / environment secret, not user auth
- Webhooks: require signature validation (Stripe) or shared secret verification

#### 2.7 Data Exposure Protection
- Remove public access to user records, character data, story data
- No endpoint returns data without ownership validation

#### 2.8 Sensitive Operations Hardening
- Password reset and email change must use authenticated user context,
  not request parameters

#### 2.9 File / Asset Security
- Replace public file access with signed URLs where applicable

#### 2.10 Admin Access
- Do NOT implement in-app admin access for V1
- Use Xano admin interface for debugging, support, and data inspection

---

### 3. State & Data Management

#### 3.1 Ownership Standardisation
- Introduce consistent ownership field across all relevant tables: `owner_user_id`
- Apply to: characters, character_traits (if user-generated), instant_stories,
  instant_story_pages, conversations, orders, etc.

#### 3.2 Remove Inconsistent Foreign Keys
- Replace `users_id`, `userId`, and other variations with `owner_user_id`

#### 3.3 Enforce Ownership in All Queries
- All queries must include `WHERE owner_user_id = auth.user.id`
- No exceptions for user-owned data

#### 3.4 Child Profile Visibility Model
- Replace array-based visibility with join tables:
  - `story_child_profiles`
  - `character_child_profiles` (if needed)

#### 3.5 Child Profile Validation Layer
- Validate child profile ownership once per request:

```sql
SELECT 1 FROM user_child_profiles
WHERE id = active_child_profile_id
AND user_id = auth.user.id
```

#### 3.6 Naming Conventions
- Enforce `snake_case`, singular table names, `_id` suffix for foreign keys
- e.g. `user` not `users`, `owner_user_id` not `users_id`

#### 3.7 Data Exposure Protection
- `GET /characters/{id}` must always enforce:

```sql
WHERE id = input.id AND owner_user_id = auth.user.id
```

#### 3.8 Table Classification
- User-owned: must have `owner_user_id`
- System/internal: no user ownership required, must not be publicly accessible
- Static/reference: can be public read-only

#### 3.9 Xano Configuration
- Ensure database uses Standard SQL format
- Review indexing on `owner_user_id` and frequently queried fields

---

### 4. Security

#### 4.1 Rate Limiting
- Enable on all public/auth endpoints:
  - `/auth/login`, `/auth/request_otp`, `/auth/reset_password`
  - Suggested: 10–20 req/min per IP, 1–4 hour cooldown
- General endpoints: 100–200 req/min per IP
- Do NOT over-tune — avoid blocking legitimate users

#### 4.2 MFA
- Enable MFA (authenticator app, not SMS) on: Xano admin, GitHub, Stripe,
  SendGrid, any cloud provider
- Create separate admin/root account not tied to daily email

#### 4.3 Secrets Management
- Store all secrets in Xano environment variables — NOT in code or function stacks
- Rotate: OpenAI, Stripe, SendGrid, and any API keys found in repo
- Integrate Gitleaks into CI (see Section 1)

#### 4.4 Environment Separation
- Implement two environments: `dev` and `prod`
- Separate Xano instances for: database, API endpoints, environment variables
- Frontend: development builds on dev branch, production builds on main
- Develop and test in dev, manually promote to prod, validate production behaviour
- Do NOT introduce staging at this stage
- Do NOT automate deployments prematurely
- Ensure separation of: API keys (Stripe, OpenAI, SendGrid), databases,
  webhook endpoints

#### 4.5 Admin Account Hygiene
- Use password manager (Bitwarden / 1Password)
- Unique passwords per service, long random credentials
- No shared logins or reused passwords

#### 4.6 Sensitive Data Handling
- Enable Sensitive Data Flagging in Xano
- Review user table fields — remove exposure of password reset tokens and
  internal flags

#### 4.7 Internal Endpoint Protection
- Add internal key validation to `/images/worker_tick` and any executor endpoints:

```javascript
if (input.internal_key != ENV.INTERNAL_KEY) { throw error }
```

---

### 5. Package Management & Supply Chain

#### 5.1 Package Manager Strategy
- Migrate from npm to pnpm (safer dependency handling, no auto script execution)
- Migration steps: install pnpm, regenerate lockfile, update CI

#### 5.2 Dependency Security Scanning
- Enable `pnpm audit`, configure CI to fail on high/critical only

#### 5.3 Delayed Dependency Adoption
```json
"pnpm": { "minimumReleaseAge": 7 }
```

#### 5.4 Dependency Update Policy
- Reactive updates for security issues only
- Periodic review monthly or ad hoc — do NOT auto-update all packages

#### 5.5 Package Selection Criteria
Before adding any package: actively maintained, widely used, no known
vulnerabilities, reasonable docs, compatible with React Native

#### 5.6 Avoid Over-Reliance on Packages
- Prefer simple internal logic over adding packages for trivial functionality

---

### 6. Testing

> **TO DO**: Identify tests based on critical user journeys and high impact failures.
> Step 1 — map core user journeys: login, story creation, story moderation,
> parental approval, child profile experience.

#### 6.1 Testing Strategy
- Focus on critical user flows and high-risk backend logic
- Do NOT aim for full coverage

#### 6.2 Minimum Coverage Areas

**Authentication**
- Valid login, invalid login, token persistence, protected route access

**Story Pipeline**
- Story creation, page generation, retrieval with correct ownership filtering

**Moderation & Approval**
- Moderation outcomes (pass / parental review / fail)
- Approval logic — visibility unlocked only after approval

**Payments / Orders**
- Stripe webhook: successful payment, duplicate prevention, order creation

#### 6.3 Test Implementation Approach
- Lightweight integration-style tests, mock external dependencies where needed
- Prefer testing flows (end-to-end logic) over unit-level micro tests

#### 6.4 Coverage Policy
- Do NOT enforce coverage thresholds initially
- Add coverage tracking (non-blocking)
- Introduce thresholds post-launch or on team expansion

#### 6.5 Core Journey Test Map

**Rule**: if a journey breaks the app, blocks users, affects money, or affects
safety → it gets tested.

| Journey | Checkpoints | Test |
|---|---|---|
| Authentication | login → token stored → route guarded | valid + invalid login |
| Story creation | prompt → record created → pages generated → retrieved | given valid input, pages exist and belong to user |
| Moderation + approval | flagged → parent notified → approved → visible | given flagged story, when parent approves, child can see story |
| Child experience | select profile → view assigned stories | — |
| Payment / order | checkout → webhook → order created | successful payment + duplicate prevention |

---

### 7. Automated Scans & Secrets

#### 7.1 Secrets Scanning
- Integrate Gitleaks into CI — scan every PR, fail build if detected
- Run initial full scan: `gitleaks detect --source .`
- Rotate any exposed keys: OpenAI, Stripe, SendGrid, Xano
- Optional: add pre-commit hook

#### 7.2 SAST
- Integrate Semgrep (open source) with OWASP Top 10 rules
- Fail on high severity only

#### 7.3 CI Security Stage
```yaml
security:
  - gitleaks
  - semgrep
  - audit
```
Failures must block merge. Developers must resolve before merging.

---

### 8. Observability, Logging & Alerting

#### 8.1 Error Tracking (Sentry)
- Integrate Sentry into React Native app (backend if feasible via Xano hooks)
- Capture: runtime errors, failed API calls, crashes

#### 8.2 Context Enrichment
Include in every event:
```json
{
  "user_id": "anon_id",
  "child_profile_id": "active_child_profile_id",
  "feature": "story_creation",
  "entity_id": "story_id"
}
```

#### 8.3 Basic Alerting
- Enable alerts for repeated errors and crash spikes
- Send to email (sufficient for now)

#### 8.4 Logging Strategy
- Log key backend events: story generation started/failed, moderation result,
  payment success/failure
- Do NOT log everything or build complex dashboards

---

## Implementation Phases

### Phase 1 — Security & Data Integrity

> **✅ Phase 1 signed off — 2026-10-23.** Items 5–9 closed 2026-07-16; items 1–4 closed 2026-10-14; close-out fixes (money in integer pence, parental-approval order gate, hidden-fields fixes) completed 2026-10-22/23.
> Evidence: final `_tests` regression run 2026-10-23, **86/86 passed** (auth and refresh, cross-user and invalid-input negatives, full order flow to Shipped, cancel and refund).
> Full record: the close-out section in [[security-model]]. Session notes: [[2026-10-22-001]], [[2026-10-23-001]].
> Carried forward: pre-launch items (hidden-fields sweep, rate limiting, parental PIN, request history off on token-issuing auth endpoints) and Phase 2 below.
> Already done from later phases: #13 MFA on Xano (2FA); #14 secrets in env vars; much of Phase 4's backend journey coverage now exists as the Postman `_tests` suite (frontend tests still to do).

| # | Task | Section | Why |
|---|---|---|---|
| 1 | Require auth on all endpoints (default deny) | 2 | API is currently exposed — single biggest risk |
| 2 | Remove user_id from inputs → use auth.user.id | 2 | Auth without this is meaningless. Prevents privilege escalation |
| 3 | Enforce ownership in all queries | 2/3 | Stops users accessing other users' data via ID guessing |
| 4 | Classify endpoints (internal / public / user_owned) | 2/3 | Prevents accidental exposure, defines security model |
| 5 | Remove unused / unnecessary endpoints | 2 | Shrinks attack surface immediately |
| 6 | Secure webhooks (Stripe + HPBC validation) | 2 | Open webhooks = direct system compromise vector |
| 7 | Protect internal endpoints with internal keys | 4 | Workers should never be user-accessible |
| 8 | Define table ownership model (owner_user_id) | 3 | Foundation for all future queries and auth logic |
| 9 | Implement soft delete (deleted_at) for core tables | 3 | Prevents irreversible data loss during bugs or misuse |

### Phase 2 — Environments & Observability

| # | Task | Section | Why |
|---|---|---|---|
| 10 | Create dev + prod environments (Xano) | 4 | Cannot safely test Phase 1 changes in prod |
| 11 | Separate API keys + services per environment | 4 | Prevents accidental real-world actions (payments, emails) |
| 12 | Establish manual dev → prod promotion flow | 4 | Prevents uncontrolled releases and accidental breakage |
| 13 | Enable MFA on all critical services | 4 | High impact, low effort |
| 14 | Move all secrets to environment variables | 4 | Prevents credential leakage |
| 15 | Integrate Sentry (frontend minimum) | 8 | Visibility into real user failures |
| 16 | Add user_id + child_profile_id to logs | 8 | Critical for debugging multi-profile model |
| 17 | Add basic error alerting (email) | 8 | Need to know when things break |

### Phase 3 — CI & Security Automation

| # | Task | Section | Why |
|---|---|---|---|
| 18 | Add Gitleaks to CI | 1/7 | Prevents catastrophic secret leaks automatically |
| 19 | Run initial secret scan + rotate keys | 7 | Likely already have exposure risk |
| 20 | Add dependency audit (pnpm audit) | 1/5 | Catches known vulnerabilities cheaply |
| 21 | Add Semgrep (SAST, high severity only) | 7 | Basic code-level security guardrail |
| 22 | Make CI blocking for merges | 1 | Ensures standards enforced consistently |

### Phase 4 — Testing

| # | Task | Section | Why |
|---|---|---|---|
| 23 | Map core user journeys | 6 | Foundation for all test work |
| 24 | Write auth journey tests | 6 | Highest risk, most foundational flow |
| 25 | Write story creation + ownership tests | 6 | Core product value + data integrity |
| 26 | Write moderation + payment tests | 6 | Safety and money — must not break |

### Phase 5 — Performance Improvement

| # | Task | Section | Why |
|---|---|---|---|
| 27 | Migrate to pnpm | 5 | Performance + security. **Promoted 2026-10-24: do before Slice 100**, together with dependency audit #20 ([[promote-pnpm-migration-ahead-of-slice-100]]) |
| 28 | Apply naming conventions across schema | 3 | Improves maintainability once system stabilised |
| 29 | Introduce join tables for child visibility | 3 | Scales better than arrays — do after core works |

---

## Related notes
- [[3-cto-tech-review]]
- [[4-cto-improvements-list]]
- [[Repos/tomale-rn-test/memory/data-model|data-model]]
- [[6. Backend - Xano]]
- [[adopt-rebac-auth-model]]
- [[separate-dev-prod-environments]]
- [[trunk-based-git-branching]]
- [[adopt-modified-semver-versioning]]