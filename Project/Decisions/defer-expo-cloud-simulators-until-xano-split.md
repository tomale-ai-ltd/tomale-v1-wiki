---
type: decision
title: defer-expo-cloud-simulators-until-xano-split
project: tomale-rn-v1
status: proposed
date: "2026-11-18"
related:
  - "[[2026-11-18-002]]"
  - "[[check-every-screen-on-the-phone-before-done]]"
affects: []
features:
  - X-testing
---

# Decision: defer-expo-cloud-simulators-until-xano-split

## What we decided

Don't adopt Expo Simulators (cloud) now. Revisit them for PR checks after the dev/prod Xano split.

## Why

Each change would need a new build, the agent would have to sign in with real credentials, and access is gated.

## Alternatives considered

Using Expo Simulators now for screen checks.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Screen checks stay on the local simulator and Kyle's phone pass for now.

## Related notes

[[2026-11-18-002]], [[check-every-screen-on-the-phone-before-done]]
