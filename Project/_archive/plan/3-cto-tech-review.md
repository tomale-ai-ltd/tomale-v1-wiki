
---
# CTO Technical Review — Tomale AI

Prepared by Avayu Ltd. Review based on git commit `507a26ff` from 2025-11-19
(005: foundations zustand scaffolding #8).

> This review triggered a pause in Cursor development to implement the
> recommendations before continuing with feature slices.

---

## Current CI process

Minimal CI pipeline running on pull requests to `main`:
- `npm ci` — respects lockfile, good supply chain hygiene
- `npm run lint` and `npm run typecheck` — good consistency foundation
- `npm test -- --runInBand` — currently only a single smoke test placeholder

---

## App foundations

### Authentication & authorization

#### Critical findings

- Only `/auth/me` and the Stripe checkout endpoint require authentication
- All other endpoints are publicly accessible without a token
- Anonymous DELETE of `character_traits` confirmed successful in testing (2025-01-07)
- `GET /users` returns full user records including PII, profile photos, and
  password reset tokens — publicly accessible
- Image URLs in character records are publicly accessible

#### Recommendations

- Require authentication on all endpoints except unauthenticated user journeys
- Implement least-privilege authorization: default to `owner-or-deny-all`
  as a minimal ReBAC (Relationship-Based Access Control) foundation
- Use signed URLs for images and file resources (requires Xano Private File
  Storage add-on on Launch plan)
- For endpoints requiring user details (e.g. password change), derive user
  identity from the authenticated token — not from request parameters
- Enable Sensitive Data Flagging in Xano
- Add email validation for new user sign-up; block further interaction until
  validated

#### Authorization approach

ReBAC recommended over RBAC or ABAC for this project — balances
relationship-aware access control without full attribute-based complexity.
Implementation at Xano level:

```sql
SELECT * FROM character_traits WHERE owner_id='1234';
```

Where `owner_id` is taken from the authenticated user, not provided as input.

### State & data management

- Zustand selector pattern in use is correct and performant:
  `const authToken = useAuthStore((s) => s.authToken);`
- No significant concerns with Zustand choice

### Data model issues

- Table names should be singular (`user` not `users`) for consistency and
  sane foreign keys (`user_id` not `users_id`)
- Field names should be consistently `lower_case_hyphenated`
- All user-owned data should consistently have an `owner` user association —
  currently missing on `character_traits` and `character_types`
- Store tables in Standard SQL Format in Xano

### Security

- Enable Rate Limiting on all API endpoints (set ~10x expected traffic,
  IP-based, few hours cool-off)
- Enable MFA on Xano admin portal
- Use separate admin/root credentials not tied to daily-use email
- Use a password manager (BitWarden or 1Password)
- Separate dev and production environments — critical before any live users


---

## DevSecOps process

### Package management

- Switch from `npm` to `pnpm` — doesn't run scripts by default, faster,
  better supply chain security
- Set `minimumReleaseAge = 7 days` on pnpm to avoid bleeding-edge packages
- Use `pnpm audit` for vulnerability scanning
- Define a package update process: react to vulnerabilities individually;
  wider upgrades periodically (every few months)

#### Checklist when adding a new package

- No known vulnerabilities + history of patching
- No open security issues in GitHub PRs/issues
- Actively maintained by multiple people
- Optimised for mobile platforms (no mouse-click dependencies)
- Easy-to-use API working consistently on iOS and Android
- Acceptable open-source licence
- Has unit and integration tests

### Test suite

Current state: single smoke test placeholder only.

Recommended approach:
- Translate acceptance criteria from each PRD/spec into automated tests
- Tests should capture user stories without locking implementation details
- Enable code coverage with 85% failure threshold (start at 80%, ratchet up)
- Consider TDD: write intentionally failing tests first, review against spec,
  then implement

Example pattern (from auth spec):

> Given I am on the Auth screen with onboarding complete, When I submit valid credentials, Then the token is stored and I am replaced into Main/Home tab

Recommendation: add a section to `.specify/templates/tasks-template.md`
requiring failing tests as the first step of every implementation task.

### Automated scans

- Add SAST scanning (Sonarqube or Semgrep open source) to CI/CD
- Add Gitleaks for secrets scanning — ideally as pre-commit hook to prevent
  secrets ever appearing in git history
- Rotate any secrets detected in baseline scan
- Use MobSF to scan iOS/Android binaries before app store submission

### Logging & alerting (Sentry)

- Implement Source Maps for readable stack traces
- Implement Debug Symbols for full Android stack traces (part of build process)
- Enrich events with anonymized/pseudonymized user identifier (compliant with
  data protection)
- Set up Tracing + Profiling for user activity and device performance monitoring
- Sentry Seer ($20/month + $1/fix) worth evaluating alongside agentic workflows

---

## Mobile app stores

### Key submission requirements

- Apple review: 1–2 days. Android review: 3–7 days.
- **Android requires beta test with 12+ active users (not installs) for
  14 consecutive days** before first release submission — plan several weeks ahead
- Privacy policy and T&Cs must be hosted publicly and accessible within the app
- Provide detailed review notes with test account credentials and feature
  walkthrough for reviewers
- Test on real low-end devices for each platform — simulator is not sufficient
- Target SDK versions: Android API level 35; Apple iOS 16 minimum, 26 recommended
  (required from April 2026)
- Screenshots must be real, localised if relevant

### OTA updates (Expo Updates)

OTA updates are limited to TypeScript/JavaScript changes only — no native code.
Changes requiring native code or new permissions require full re-submission.

OTA-suitable changes:
- UI layout/design changes to existing screens
- User journey changes that don't introduce new data models

Not OTA-suitable:
- New data models or concepts
- New device permissions

### Versioning (SemVer modified)

- `major` — fundamental application rewrites (likely v1.x.x for a long time)
- `minor` — app store required updates (native code/permissions changes)
- `patch` — OTA updates

### Release channels (Expo)

- `dev` — feature development
- `staging` — current head of main branch
- `production` — latest app store release

### Git branching model

Trunk-based development. Short-lived branches for features and releases.

**New feature:**
1. Checkout `feat/ABC-description` from `main`
2. Develop + commit
3. Open PR; CI/CD checks pass
4. CI/CD determines OTA or store submission required
5. Merge into `main`, delete branch

**App store release:**
1. Branch `release/1.2.X` from `main`
2. Run release job; increment version numbers
3. Submit to app stores; tag `v1.2.0` on approval

**OTA release:**
1. Checkout `feat/DEF-description` from `main`
2. Develop; CI/CD approves for OTA
3. Cherry-pick onto current release branch
4. Run OTA release job targeting `production` channel
5. Tag `v1.2.1`

---

## Agent development (CTO notes — to evaluate)

Tools noted for evaluation — CTO has not yet tested these in production:

- **Claude Code Superpowers** — core skills library, extends spec-driven
  development approach with Claude
- **Claude Code Creator Setup** — Boris Cherny's personal setup (creator of
  Claude Code)
- **Gas Town** — multi-agent workspace manager for parallel feature development
- **GitHub Copilot PR review** — automatic code review if included in subscription
- **Greptile** — PR review that analyses whole codebase, not just diff
- **Xano VS Code extension** — XanoScript extension, works with Cursor/Windsurf;
  language server may be accessible for Claude Code (unconfirmed)

---

## References

- MobSF — Mobile Security Framework
- OWASP — Mobile Application Security
- OWASP — React Native
- Expo Updates documentation
- EAS CLI branch/channel management

## Related notes
- [[plan/cto-improvements-implementation-plan]]
- [[architecture/xano-schema]]
- [[stack/xano]]
- [[stack/deployment-eas]]
- [[separate-dev-prod-environments]]
- [[decisions/rebac-authorization-approach]]