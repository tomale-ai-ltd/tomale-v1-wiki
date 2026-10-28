---
type: decision
title: use-per-build-variant-url-schemes
project: tomale-rn-v1
status: accepted
date: 2026-10-28
supersedes:
  - "[[use-custom-url-scheme-for-app-deep-links-v1]]"
related:
  - "[[v1-audit]]"
  - "[[return-from-stripe-checkout-via-in-app-browser-sheet]]"
affects:
  - app.json / app.config.js
  - eas.json
  - user_alerts.action_url
features:
  - X-platform
  - F-notifications
  - F-store
---

# Decision: use-per-build-variant-url-schemes

## What we decided

The app's URL scheme depends on the build: `tomalerntest://` for development builds and `tomale://` for production. One codebase produces both: an `app.config.js` reads the EAS build profile (e.g. `APP_VARIANT`) and sets the scheme, app name and bundle identifier, so both builds can sit on one device. No separate repo or Cursor project. Universal Links (`https://tomale.ai/app/*`) remain a pre-launch item.

Backend-generated links (alert `action_url`, checkout return) must use the scheme of the environment that produced them. Today they are hard-coded to `tomalerntest://` in `ai_pipeline_content_moderation_story_text` and `ai_pipeline_story_completion_check`. They move to a per-branch setting with the dev/prod split.

## Why

The two older notes disagreed (`tomale://` vs `tomalerntest://`). The live app uses `tomalerntest`. Separate schemes stop a dev build from catching production links and the reverse.

## Alternatives considered

A separate repo or project for production: rejected, as it duplicates the codebase.

## Trade-offs accepted

`app.config.js` replaces the static scheme in `app.json` (a repo-sync item when Slice 400 or the release setup starts).

## Related notes

- [[v1-audit]] (C1)
- [[use-action-url-for-user-alert-deep-linking]]
- [[use-xano-branches-for-dev-and-prod]]
