---
type: plan-task
id: IP-16
title: "Xano Session B: cut-over"
status: todo
owner: "Kyle"
depends:
  - "[[IP-12-load-test]]"
  - "[[IP-13-chaos-tests]]"
  - "[[IP-14-security-and-well-architected-review]]"
  - "[[IP-15-printed-proof]]"
gate: "G2"
effort_days: 1
target: 2027-01-13
scoping: checklist
project: tomale-rn-v1
---

# IP-16: Xano Session B: cut-over

**Goal:** Apply fixes from shadow mode; make the gateway records default for page, then cover; watch 48 hours; rewrite [[image-generation-flow]] from [[image-pipeline-future-state]].

**Done when:** G2: live SLOs met for 48 hours; decisions accepted; canonical docs updated.

**Notes:** Rollback: the OpenAI fallback record back to default.

Plan: [[image-pipeline-plan]] · Scope: [[PRD-Image-Pipeline]]
