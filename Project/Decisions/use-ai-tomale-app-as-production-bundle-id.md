---
type: decision
title: "use-ai-tomale-app-as-production-bundle-id"
project: tomale-rn-v1
status: accepted
date: "2026-11-01"
related:
  - "[[2026-11-01-001]]"
  - "[[use-per-build-variant-url-schemes]]"
affects:
  - "[[pre-launch-checklist]]"
  - app.config.js
features:
  - X-platform
---

# Decision: use-ai-tomale-app-as-production-bundle-id

## What we decided

The production iOS bundle id and Android package are both `ai.tomale.app`. The App ID is registered in the Apple Developer account (description "Tomale"). Development builds keep `com.tomaleai.tomalerntest`.

## Why

Not discussed in session notes. (The repo had no Android package set in `app.json`.)

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

The id is permanent once the first store build is uploaded.

## Workflow detail

Set in `app.config.js` per build variant (RS-2026-10-30-07, PR C in [[m1-cursor-briefs]]): `preview` and `production` use `ai.tomale.app`; `development` uses `com.tomaleai.tomalerntest`, so both builds install side by side.

## Related notes

- [[2026-11-01-001]]
- [[use-per-build-variant-url-schemes]]
- [[m1-cursor-briefs]]
