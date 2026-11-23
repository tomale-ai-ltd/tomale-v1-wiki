---
type: decision
title: "offer-sign-out-of-all-devices-in-v1"
project: tomale-rn-v1
status: accepted
date: "2026-11-19"
related:
  - "[[2026-11-19-002]]"
  - "[[retain-account-data-30-days-after-closing]]"
affects:
  - "[[pre-launch-checklist]]"
  - "[[roadmap]]"
  - "[[account-closing-micro-prd]]"
  - "user_sessions"
features:
  - F-auth
  - F-account
  - X-security
---

# Decision: offer-sign-out-of-all-devices-in-v1

## What we decided

A parent can sign the household out of every device in V1. Sessions are not revoked on app updates; a forced sign-out of everyone is an incident tool only. The detail is drafted in PU-2026-11-19-03 (proposed): a shared revoke function used by "sign out of all devices" and account closing, plus an emergency revoke-all in the incident runbook.

## Why

Kyle asked for "sign out of all devices" for V1. Revoking sessions on every update would mean every family needs a new magic link on each release.

## Alternatives considered

Revoking all sessions on every app update (rejected for the reason above).

## Trade-offs accepted

Not discussed in session notes. (The PU notes an open point: revoking stops refresh, so a 1-hour access token on another device keeps working until it expires.)

## Workflow detail

Queued after 010 merge alongside the B6 docs PU and RS-2026-11-17-02. Lands in M7 Settings per PU-2026-11-19-03.

## Related notes

[[2026-11-19-002]], [[retain-account-data-30-days-after-closing]], [[pre-launch-checklist]], [[account-closing-micro-prd]]
