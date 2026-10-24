---
type: decision
title: separate-dev-prod-environments
date: 2025-01-01
status: current
project: tomale-rn-v1
---

---

# Decision: Separate Dev and Production Environments

## What we decided

Maintain two distinct environments — `dev` and `prod` — with full separation
of Xano instances, API keys, databases, and webhook endpoints.

Manual promotion from dev to prod. No staging environment. No automated
deployments at this stage.

## Why

The CTO review identified that development and testing was happening against
production data. This creates several compounding risks:
- Test actions (including destructive ones) affect real user data
- Accidental emails or payments triggered during development reach real users
- No safe place to test security changes (Phase 1 of the implementation plan)
  before they affect live data

The Phase 1 security work cannot safely be tested without environment
separation in place first — which is why this became Phase 2 priority 1.

## Alternatives considered

- **Single environment** — rejected: unacceptable risk once real users exist,
  demonstrated risk during CTO review testing
- **Three environments (dev / staging / prod)** — deferred: adds operational
  overhead not justified at solo V1 stage; can be introduced when a team grows
- **Automated deployment pipeline** — deferred: premature at this stage,
  introduces risk of uncontrolled releases

## Trade-offs accepted

- Manual dev → prod promotion adds a step to every release
- Maintaining two Xano instances has a cost implication
- Some bugs may only surface in prod due to environment differences

## Consequences

- Separate Xano workspaces for dev and prod
- All API keys (Stripe, OpenAI, SendGrid) duplicated per environment with
  separate credentials
- Stripe and HPBC webhook endpoints must be environment-specific
- Frontend uses development builds against dev, production builds against prod
- All Phase 1 security changes tested in dev before promotion to prod

## Related notes

- [[3-cto-tech-review]]
- [[4-cto-improvements-list]]
- [[6. Backend - Xano]]
- [[12. CICD - EAS, GitHub]]
