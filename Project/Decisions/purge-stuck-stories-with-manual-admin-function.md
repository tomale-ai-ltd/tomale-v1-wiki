---
type: decision
title: purge-stuck-stories-with-manual-admin-function
project: tomale-rn-v1
status: accepted
date: 2026-10-13
---

---

# Decision: purge-stuck-stories-with-manual-admin-function

## What we decided

Delete, rather than recover, the ~50 trial-data stories stuck in Preparing / In Queue, using a manually-run Xano function `admin_purge_stuck_stories` with no endpoint. It defaults to a dry run, skips story 613, stories with orders and stories with active image jobs, and can optionally include old Drafts. It deletes `image_jobs` → `instant_story_characters` → `instant_story_pages` → `instant_stories` in that order. `characters` and `store_orders` are never deleted.

## Why

The stuck stories were trial data and were blocking test 1C. Having no endpoint means it cannot be called by clients; the dry-run default and the skip rules protect the fixture story and any real orders.

## Alternatives considered

Recovering the stuck stories was considered and rejected in favour of deletion (the session plan said "recover or retire").

## Trade-offs accepted

Page image files are not deleted by the function (deferred). A runtime sweeper for stuck stories (with a `Failed` status and allowance refund) is also deferred.

## Workflow detail

Run manually from Xano when stuck stories accumulate. The run completed on 2026-10-13 and 1C passes.

## Related notes

- [[story-creation-flow]]
- [[use-fixture-story-for-order-flow-test]]
- [[replace-long-done-poll-with-stuck-story-check]]
- [[2026-10-13-001]]
