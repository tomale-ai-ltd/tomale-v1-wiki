---
type: decision
title: "upgrade-expo-to-sdk-58-and-use-gluestack-v5-with-uniwind"
project: tomale-rn-v1
status: accepted
date: "2026-11-01"
related:
  - "[[2026-11-01-001]]"
  - "[[m1-cursor-briefs]]"
affects:
  - constitution
  - "[[stack]]"
  - "[[roadmap]]"
features:
  - X-platform
---

# Decision: upgrade-expo-to-sdk-58-and-use-gluestack-v5-with-uniwind

## What we decided

Upgrade Expo SDK 54 → 58 during M1, then use gluestack-ui v5 (current stable, 5.0.15, June 2026) styled with UniWind on Tailwind CSS v4 as the UI component library. This replaces an earlier same-day choice of gluestack-ui v3 and the constitution's NativeBase. Lucide React Native stays for icons (RS-2026-11-01-01).

## Why

gluestack v3's overlays (Modal, ActionSheet, Popover) break or crash on Expo SDK 54 with Reanimated 4 (gluestack issue #3200, no clean fix), and overlays are needed from Slice 100. v4 never left alpha. v5 moves most overlays to Reanimated (ActionSheet, Select, Tooltip still use Legend Motion). v5 needs Tailwind v4 via NativeWind v5 (still RC) or UniWind (stable, Expo-only), so UniWind. gluestack's Expo starter runs SDK 56 / Reanimated 4.3 and Expo's latest is SDK 58 (29/09/2026); upgrading now, with no feature screens built, is the cheapest it will be.

## Alternatives considered

- Expo SDK 56 (gluestack's tested version; shorter support window).
- Re-open the library choice (e.g. Tamagui).
- NativeWind v5 instead of UniWind (still RC).

## Trade-offs accepted

- 1–2 days added to M1.
- gluestack repo activity has slowed since July; mitigated because components are copied into our repo.
- SDK 58 needs Node ≥ 22.13 (Node 22 landed first in PR A).

## Workflow detail

Delivered through repo-sync: RS-2026-11-01-04 (Expo SDK 54 → 58) and RS-2026-11-01-01 (constitution 1.6.0) in PR B; RS-2026-11-01-03 (install gluestack-ui v5 + UniWind) in PR C ([[split-m1-into-four-ordered-cursor-prs]]).

## Related notes

- [[2026-11-01-001]]
- [[m1-cursor-briefs]]
- [[split-m1-into-four-ordered-cursor-prs]]
- [[Repos/tomale-rn-test/memory/constitution]]
