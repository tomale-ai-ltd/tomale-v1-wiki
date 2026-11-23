---
type: decision
title: "replace-sign-in-with-the-app-on-handover"
project: tomale-rn-v1
status: accepted
date: "2026-11-20"
related:
  - "[[2026-11-20-001]]"
  - "[[2026-11-19-002]]"
affects:
  - "app code: useAuth.login, auth/complete, resumePendingRoute"
features:
  - F-auth
  - F-parental-oversight
---

# Decision: replace-sign-in-with-the-app-on-handover

## What we decided

On sign-in (password login, bootstrap and the magic-link `auth/complete` path) the auth screens are dropped and the app replaces the focused screen (`replaceSignedIn`). A saved route resumes inside the main app: `resumePendingRoute` replaces Home and pushes the route, without `dismissAll()`. The stack is reset on every pending-route resume, so Back reaches Home. No "picker already passed" memory was added (`89ddcec`, after `9a36c1e`).

## Why

On the signed-out approvals link, Back reached sign-in, and then a second picker appeared with a jump to Home, because `dismissAll()` popped to sign-in and remounted the main layout. Kyle agreed that was the cause and asked to fix the handover first.

## Alternatives considered

Remembering that the PIN had already been entered, so the remounted layout would not ask again (Kyle chose to fix the handover instead).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

A longer-term option is noted, not decided: moving the root from `<Slot />` to guarded stacks with expo-router's `Stack.Protected`, which would remove this class of auth-history bug (polish-pass candidate).

## Related notes

[[2026-11-20-001]], [[2026-11-19-002]]
