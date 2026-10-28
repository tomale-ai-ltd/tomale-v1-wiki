---
type: plan
title: 2-build-plan
project: tomale-rn-v1
status: historical
version: 1.0
date: 2026-04-15
last_verified: 2026-04-15
owner: vault
superseded_by: "[[roadmap]]"
---

> **Archived 28/10/2026 (B8).** Superseded by [[roadmap]], which carries every open item from this plan.

## Build Plan

- [x] 000\-  Foundations \(ship first, tiny\)
    - [x] 001 \- Expo Router shell \+ tabs \(bookshelf, characters, store, settings\)
    - [x] 002 \- Auth baseline \(login, token store, guarded routes, logout\)
    - [x] 003 \- DevOps \(pinned tooling, basic CI lint&#x2F;type&#x2F;test, pre\-commit checks\)
    - [x] 004 \- Observability &amp; OTA \(basic crash reporting and OTA updates\)
    - [x] 005 \- Zustand scaffolding \(auth, characters, stories stores, empty actions\)
    - [x] 006 \- HTTP client \+ OpenAPI excerpt \(freeze just the endpoints used per slice\)\.
- [ ] 100 \- Characters \(fast wins\)
    - [ ] 101 \- Characters index \(read\-only\) — list \+ cached metadata
    - [ ] 102 \- Character detail \(read\-only\) — \[id\]\.tsx
    - [ ] 103 \- Create \(simple form\) — POST path proven before AI\.
    - [ ] 104 \- Carousel upgrade — reanimated carousel \+ blurred bg \+ image prefetch\.
    - [ ] 105 \- Archive&#x2F;quick actions — long\-press → status=archived \(optimistic UI\)\.
- [ ] 200 \- Story creation via chatbot \(golden path first\)
    - [ ] 201 \- Draft bootstrap — create instant\_stories \(status=draft\)\.
    - [ ] 202 \- Start conversation — create story\_conversations, render chat UI\.
    - [ ] 203 \- Suggestion cards → actions — theme&#x2F;artwork&#x2F;character chips that update the draft\.
    - [ ] 204 \- Complete story — minimal fields → status=complete → appears on Bookshelf\.
- [ ] 300 \- Bookshelf \+ E\-reader
    - [ ] 301 \- Bookshelf index — completed stories list\.
    - [ ] 302 \- E\-reader v1 — cover screen, swipe pager, TTS, progress indicator\.
    - [ ] 303 \- Resume progress — PATCH reading\_logs on page turn \+ resume\.
- [ ] 400 \- Store \(checkout → history\) 
    - [ ] 401 \- Store index — explainer \+ CTA\.
    - [ ] 402 \- Checkout v1 \(happy path\) — select story&#x2F;options → Stripe checkout session via Xano → success\.
    - [ ] 403 \- Order history — list \+ detail \+ status updates\.
    - [ ] 404 \- Failure&#x2F;retry — handle payment\_failed&#x2F;cancel\.
- [ ] 500 \- AI Create\-Character \(after story chatbot is stable\) 
    - [ ] 501 \- Chatbot create\-character — JSON preview card \+ image regenerate → POST &#x2F;characters\.
    - [ ] 502 \- Voice input — gated flag; speech\-to\-text where available\.

# Build Order — Slices

## Ordering (dependency-aware)

1. Foundations (001–004)
2. Characters read-only + create form (101–103)
3. Story chatbot golden path (201–204)
4. Bookshelf + E-reader (301–303)
5. Characters carousel polish (104–105)
6. Store (401–404)
7. AI create-character (501–502)

---

## Slice 000 — Foundations

> Ship first. Small slices. Unblocks everything else.

- **001** — Expo Router shell + tabs: `(tabs)/bookshelf`, `(tabs)/characters`,
  `(tabs)/store`, `(tabs)/settings`. Pull palette/components into a design tokens file.
- **002** — Auth baseline: login → token store → guarded routes; `useAuth()` and token
  refresh; logout.
- **003** — Zustand scaffolding: auth, characters, stories stores with empty selectors
  and mocked actions (real endpoints wired later).
- **004** — HTTP client + OpenAPI snapshot: import minimal OpenAPI for first two
  endpoints; freeze per slice to avoid drift.

---

## Slice 100 — Characters

> Fast wins, visible progress.

- **101** — Characters index (read-only): fetch + cache list; grid list first.
  Route: `app/(tabs)/characters/index.tsx`
- **102** — Character detail (read-only): `[id].tsx` shows image, core attributes,
  actions disabled.
- **103** — Create (form fallback): simple create with POST (no AI yet) to prove write
  path. Route: `app/(main)/characters/create.tsx`
- **104** — Animated carousel upgrade: swap grid for reanimated carousel + blurred
  background, image prefetch.
- **105** — Archive / quick actions: long-press → PATCH `status=archived`, optimistic UI.

---

## Slice 200 — Story Creation via Chatbot

> Golden path first.

- **201** — Draft story bootstrap: create draft `instant_stories` with `status=draft`;
  show "Continue in Chat" CTA.
- **202** — Start conversation: create `story_conversations` row; render chat UI with
  assistant hello.
- **203** — Suggestions → actions: render card chips for theme / art style / characters;
  posting a chip updates the draft incrementally.
- **204** — Complete story: when minimal fields present, flip `status=complete` and push
  to Bookshelf.

> Keep LLM prompts short and strongly structured. UI cards handle most choices.

---

## Slice 300 — Bookshelf + E-reader

> Engagement loop.

- **301** — Bookshelf index: show user's completed stories; open detail.
- **302** — E-reader v1: `read.tsx` with swipe pager, cover screen, progress
  persistence, and basic TTS (play/pause).
- **303** — Resume progress: PATCH `reading_logs` on page turn; resume on reopen.

---

## Slice 400 — Store

> Checkout → order history.

- **401** — Store index: explainer + CTA (hidden if no completed stories).
- **402** — Checkout v1 (happy path): select story + options → create Stripe checkout
  session via Xano; success screen.
- **403** — Order history: list orders + statuses; detail screen with updates.
- **404** — Failure / retry flow: handle cancelled / `payment_failed` with retry CTA.

---

## Slice 500 — AI Create Character

> After chatbot is stable.

- **501** — Chatbot create-character: reuse chat UI; produce JSON preview card + image
  regenerate; POST `/characters`.
- **502** — Voice input: gated feature flag; Expo speech-to-text where supported.

---

## Related notes

- [[1-prd-tomale-react-native-app-v1]]
- [[Repos/tomale-rn-test/memory/constitution|constitution]]
- [[sdd-flow]]