---
type: decision
title: use-bundled-preset-avatars-for-profiles
project: tomale-rn-v1
status: accepted
date: 2026-06-29
supersedes:
  - "[[defer-explicit-profile-avatar-endpoint-until-kid-profiles]]"
related:
  - "[[2026-06-29-001]]"
  - "[[v1-audit]]"
affects:
  - user_profiles.avatar_key
  - tomale-rn-test assets/avatars
  - users.profile_photo
features:
  - F-profiles
---

# Decision: use-bundled-preset-avatars-for-profiles

## What we decided

Profile avatars are bundled presets: `user_profiles.avatar_key` (text) is stored and the app resolves it to an image in `assets/avatars` (about 50 options from a free avatar generator). There are no avatar uploads for profiles. `users.profile_photo` is retired in favour of profile avatars; `auth/me` still returns it, which is cleaned up in B9.

The generator's licence allows free commercial use (Kyle). Check whether it requires attribution (DiceBear's CC BY 4.0 does) and add an in-app credit if so.

Future idea: more flexible avatars, possibly a child's own characters.

## Why

Data minimisation under the ICO Children's Code, no upload moderation surface, and on-brand.

## Alternatives considered

A dedicated `PATCH /user_profiles/{id}/avatar` upload endpoint (the earlier deferral): rejected.

## Related notes

- [[2026-06-29-001]] (backfilled in B7)
- [[v1-audit]] (C9)
