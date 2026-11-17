---
type: decision
title: "pass-app-scheme-to-web-intermediary-pages"
project: tomale-rn-v1
status: accepted
date: "2026-11-17"
related:
  - "[[2026-11-13-002]]"
  - "[[use-per-build-variant-url-schemes]]"
  - "[[use-https-web-intermediary-for-magic-link-redirect]]"
  - "[[separate-verify-email-deeplink-from-magic-link-path]]"
  - "[[use-xano-branches-for-dev-and-prod]]"
affects:
  - "Squarespace pages /app/approvals, /verify-email, magic-link page"
  - "Xano env approvals_url (and the other web-page links)"
  - "[[pre-launch-checklist]]"
features:
  - X-platform
  - F-notifications
  - F-auth
---

# Decision: pass-app-scheme-to-web-intermediary-pages

## What we decided

The Squarespace intermediary pages (`/app/approvals`, `/verify-email`, the magic-link page) stop hard-coding `tomalerntest://`. The link in each email carries the app to open as a query parameter, `?app=tomalerntest` or `?app=tomale`, set per Xano environment (dev: `tomalerntest`, production: `tomale`). The page accepts only those two values, falls back to `tomale` for anything else, and opens `<app>://<path>`. Done with the dev/prod Xano split, not before.

## Why

All three pages are shared by both environments. Hard-coded, they always open Tomale Dev, so once the production app is live, real users' emails would open the wrong app (or nothing), and testing on dev Xano with both apps on one phone would be ambiguous. This extends [[use-per-build-variant-url-schemes]] (backend links use the scheme of the environment that produced them) to the web pages.

## Alternatives considered

- Separate dev pages (e.g. `/app/approvals-dev`): works, but doubles the pages to maintain.
- Universal Links only: removes the extra tap for production (already a pre-launch item) but dev builds would still need a page.

## Trade-offs accepted

A small script change on three Squarespace pages, and each Xano environment's link env vars must carry the right `app` value. The allowlist and production fallback stop the page opening anything else.

## Related notes

- [[2026-11-13-002]]
- [[use-per-build-variant-url-schemes]]
- [[use-https-web-intermediary-for-magic-link-redirect]]
