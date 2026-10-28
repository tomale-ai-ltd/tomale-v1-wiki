---
type: decision
title: enforce-server-side-image-validation
project: tomale-rn-v1
status: accepted
date: 2026-05-21
features:
  - F-account
---

# Decision: Enforce server-side image validation with client-side resize

## What we decided

Image uploads are validated server-side: MIME type restricted to
`jpeg` / `png` / `webp`, a 5 MB size cap, and dimensions between 200×200 (min)
and 2048×2048 (max). Image resizing and EXIF stripping are performed client-side
via `expo-image-manipulator`; the server validates the result rather than
transforming it.

## Why

The current Xano plan has no image-transform capability, so resize and EXIF
strip cannot run server-side. Doing them on the client with
`expo-image-manipulator` is the available path. The server still enforces MIME,
size, and dimension limits so it never trusts the client blindly — this keeps
defence-in-depth on the upload path even though the transform happens off-server.

## Alternatives considered

- Server-side image transform in Xano — unavailable on the current plan.
- Edge transform via Lambda@Edge / CloudFront Functions — deferred; to be
  re-evaluated after the S3 storage migration when those become available.

## Trade-offs accepted

- Resizing depends on the client behaving correctly. The server validates
  dimensions and size but does not itself resize, so a non-conforming upload is
  rejected rather than corrected.
- EXIF privacy is de-prioritised for V1: the only user-uploaded images are
  parent avatars (kid images are AI-generated), and EXIF coordinates in a
  parent's own photo are exposed only to themselves until storage becomes
  public-facing.

## Workflow detail

Client apps must run `expo-image-manipulator` before upload. `PATCH /users/me/image`
performs the MIME, size, and dimension checks server-side and rejects anything
out of bounds. Edge-based transform should be revisited at the S3 migration,
when CloudFront Functions / Lambda@Edge become available.

## Related notes

- [[Sessions/2026-05-21-001|2026-05-21-001]]
- [[6-api-security-model|6-api-security-model]]
- [[migrate-image-storage-to-aws-s3-signed-urls|migrate-image-storage-to-aws-s3-signed-urls]]
- [[defer-explicit-profile-avatar-endpoint-until-kid-profiles|defer-explicit-profile-avatar-endpoint-until-kid-profiles]]
- [[collapse-bool-preference-endpoints-into-users-me|collapse-bool-preference-endpoints-into-users-me]]
- [[make-username-user-editable|make-username-user-editable]]
- [[separate-verify-email-deeplink-from-magic-link-path|separate-verify-email-deeplink-from-magic-link-path]]
