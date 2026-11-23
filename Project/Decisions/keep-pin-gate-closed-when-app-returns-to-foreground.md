---
type: decision
title: keep-pin-gate-closed-when-app-returns-to-foreground
project: tomale-rn-v1
status: accepted
date: 2026-11-19
related:
  - "[[2026-11-19-002]]"
  - "[[parental-gate-on-profile-switch]]"
  - "[[ask-for-pin-when-first-needed]]"
affects:
  - "[[security-model]]"
features:
  - F-profiles
  - X-security
---

# Decision: keep-pin-gate-closed-when-app-returns-to-foreground

## What we decided

The app's profile gate only ever closes on its own: coming back to the foreground can raise the profile picker but can never lower it, and only entering through the PIN sets the gate to the app (`8db3f41`). The cold-start picker is decided once per sign-in, keyed on the sign-in rather than the user id, so a replacement token does not raise the picker again (`0254d21`, `31a5bba`).

## Why

Kyle's phone pass found a PIN bypass: returning from a brief background (the share sheet after a screenshot) dropped the picker over a parent token. A second bug raised the picker after every profile switch because the cold-start decision re-ran on each new token. A token can exist before the user id is stored, so keying on the user id never showed the app.

## Alternatives considered

Keying the cold-start picker on the user id (Cursor's first version, which waited for a user id and broke the existing gate test).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Fixed inside the 010 branch and merged in PR #32. A second tap on a child while a switch is running does nothing.

## Related notes

[[2026-11-19-002]], [[parental-gate-on-profile-switch]], [[ask-for-pin-when-first-needed]], [[security-model]]
