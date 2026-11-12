---
type: decision
title: adopt-animatereactnative-components-via-the-kit
project: tomale-rn-v1
status: proposed
date: 2026-11-12
related:
  - "[[build-ui-from-a-component-kit-with-a-screenshot-loop]]"
  - "[[keep-release-age-gate-when-adding-packages]]"
  - "[[2026-11-12-001]]"
features:
  - F-design-system
  - F-characters
  - F-rewards
---
# Decision: adopt-animatereactnative-components-via-the-kit

## What we decided
Kyle has paid access to the animatereactnative.com components and their Cursor MCP (`https://www.animatereactnative.com/mcp`). Cursor may use them as a source for motion-heavy UI:
1. **Into the kit, not as black boxes:** a component's source is copied into `components/ui/`, mapped to theme tokens, given Reduce Motion support, and screens use the kit version.
2. **Dependencies through the gate:** most components need only Reanimated, Gesture Handler and SVG (already installed). Anything else (Skia, Lottie, gradients) is a dependency change: Cursor asks Kyle and the release-age gate applies.
3. **Licence:** Kyle confirms commercial use with the code in a private repo before the first component lands.
4. **MCP setup:** `.cursor/mcp.json` is git-ignored in `tomale-rn-test`, so the MCP is Kyle's local Cursor setting; no repo-sync item. The MCP only supplies code; everything still lands through a PR Kyle reviews.

First use: the 008 parallax carousel in US7b (compare with Cursor's own build; keep whichever is closer to the mock-up). Later candidates: the 501 reveal, child celebrations and badges, sheet and toast motion.

## Why
High-quality motion is a large part of how the app should feel for children, and these components cover the carousel, reveal and celebration moments already in the designs, mostly on libraries the app already uses.

## Alternatives considered
Hand-building every animation (slower, less polished); importing the components as a package (unreviewed code and no token mapping).

## Trade-offs accepted
Copied code is ours to maintain; a third-party MCP is a source of code suggestions, mitigated by PR review.
