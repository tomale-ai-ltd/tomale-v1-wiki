---
type: decision
title: consolidate-xano-api-groups-into-app-and-webhooks
project: tomale-rn-v1
status: accepted
date: 2026-05-15
---

---

# Decision: consolidate-xano-api-groups-into-app-and-webhooks

## What we decided

Collapse the previous seven Xano API groups (`auth`, `commerce`, `content`, `integrations`, `system`, `users`, `utilities`) into two:

- `app` — everything the RN app calls. New base URL: `https://api.tomale.ai/api:1pgd39RE`.
- `webhooks` — Stripe + HPBC server-to-server callbacks.

Stripe `create_checkout_session` is reclassified to `app`; webhook receivers route to `webhooks`. `sendgrid/*` and `stability/generate_image` are flagged for follow-up classification (likely internal Xano functions rather than API endpoints).

## Why

The OpenAPI client generator assumes a single `servers:` URL, and the previous seven-group topology forced workarounds in codegen and call sites. The two-axis split — RN-app traffic vs. webhook traffic — cleanly matches how endpoints are actually consumed and authenticated, and a single `app` base URL simplifies env configuration and the runtime base URL read in `api/http.ts`.

## Alternatives considered

- **Keep the seven-group structure.** Rejected — incompatible with the chosen OpenAPI codegen workflow and obscures the more meaningful app-vs-webhook distinction.
- **Three groups (`app`, `webhooks`, `internal`)** for the SendGrid / Stability items. Deferred until those endpoints' classification is confirmed; if they are true internal Xano functions, they don't need an API group at all.

## Trade-offs accepted

- `api-spec` and `data-model` now lag reality (new topology, new base URL, reclassified endpoints). A batch reconciliation is queued for end of Phase 1.
- Xano's swagger for the `app` group is currently public — endpoints enforce auth, but the surface is advertised. Must be made private before launch.
- Lost the new `app` group once during the restructure (accidental delete); restored from Xano's previous-night automated workspace snapshot. A "manual Xano snapshot before structural changes" step has been added to the session-start checklist as a result.

## Workflow detail

The new base URL `https://api.tomale.ai/api:1pgd39RE` is read by the frontend via `config/env.ts` (`EXPO_PUBLIC_API_BASE_URL`). OpenAPI regeneration workflow is unchanged at the entry point — `npm run update:openapi` — but now runs against a single-server spec: re-export from Xano → overwrite `api/openapi/xano.yaml` → `npm run update:openapi` → typecheck → fix call sites. Codegen affects the generated client only; runtime base URL is a separate env read.

## Related notes

- [[use-https-web-intermediary-for-magic-link-redirect]]
- [[enforce-strict-env-validation-at-startup]]
- [[separate-dev-prod-environments]]
