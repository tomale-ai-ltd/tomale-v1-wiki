---
type: decision
title: migrate-image-storage-to-aws-s3-signed-urls
project: tomale-rn-v1
status: accepted
date: 2026-05-15
implementation: "not yet implemented (Phase 1.5: S3 + CloudFront)"
features:
  - X-platform
  - F-characters
  - F-story-generation
  - F-account
---


# Decision: Migrate image storage from Xano public files to AWS S3 + CloudFront with signed URLs

## What we decided

All user-facing image assets (user profile photos, character images, story cover and page images) will be migrated from Xano's built-in public file storage to AWS S3 with CloudFront in front, served via signed URLs.

Implementation deferred until after the `users` API group is complete in Phase 1 of the CTO implementation plan. Migration will be scheduled as a dedicated task in Phase 1 or Phase 2, ahead of public launch.

## Why

The CTO tech review flagged that current image URLs are permanently public — anyone with the link (or who can guess the URL pattern) can fetch any image indefinitely. For a children's product where images include personalised characters often modelled on the user's own child, this is a meaningful privacy issue, not a theoretical one.

Signed URLs solve this by:

- Issuing time-limited URLs (e.g. 1 hour TTL) tied to authenticated sessions
- Preventing link sharing from creating permanent public access
- Enabling actual revocation on account deletion (not just DB row removal)
- Providing an audit trail of access

## Alternatives considered

- **Xano Private File Storage add-on** — would solve the privacy issue and is the path of least resistance (already integrated with Xano). Rejected because: paid recurring add-on with no equivalent credit; less mature signed URL tooling than AWS; couples image storage tightly to the backend platform; no CDN included.
    
- **Keep public files, restrict by obscurity** — rejected. Security by URL obscurity is not security. Fails any reasonable pre-launch privacy review, especially for a children's product.
    
- **Cloudflare R2 + Cloudflare Workers** — viable alternative with no egress fees. Rejected for now because AWS credits cover S3 + CloudFront, and AWS SDKs are more universally documented for Xano function stack integration.
    

## Trade-offs accepted

- One-time migration work: ~1–2 sessions (set up S3 + CloudFront + IAM, build internal Xano functions, migrate existing files, update read endpoints)
- Slight added complexity on the read path: every API response containing images must generate signed URLs at response time, not just return stored paths
- React Native client must handle URL expiry (refresh on app foreground if data older than 30 min, or refetch on 403)
- New dependency on AWS as a critical-path service (low risk — AWS credits cover cost for years)

## Consequences

- All endpoints returning image fields will need a `_signed_url(path, ttl)` call inserted into their function stack at read time
- `_upload_image(file, folder)` internal function will be created during the migration and used by all resource-specific image upload endpoints (`PATCH /users/me/image`, future `PATCH /characters/{id}/image`, etc.)
- DB columns currently storing public URLs will be changed to store S3 object paths instead
- AWS credentials will need to be stored as Xano environment variables, and split by environment once dev/prod separation is in place (Phase 2)
- Storage backend becomes portable — if Tomale ever leaves Xano, image storage stays where it is

## Implementation notes

Upload pattern decision (proxy vs. presigned PUT): start with **proxy** (Frontend → Xano → S3) to match current upload behaviour and keep validation server-side. Switch to presigned PUT if upload volumes warrant it later.

Read TTL: **1 hour** signed URL TTL, with client refresh on stale data or 403. Aligns with industry convention (Notion, Slack, Linear).

Endpoint shapes agreed during the `users` group session (`PATCH /users/me/image` etc.) do not change with this migration — only the internals do.

## Related notes

- [[3-cto-tech-review]]
- [[5-cto-implementation-plan]]
- [[security-model]]