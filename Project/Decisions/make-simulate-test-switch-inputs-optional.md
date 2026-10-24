---
type: decision
title: make-simulate-test-switch-inputs-optional
project: tomale-rn-v1
status: accepted
date: 2026-10-21
---

---

# Decision: make-simulate-test-switch-inputs-optional

## What we decided

Test switches (`simulate_*`) are always optional inputs, never required. In XanoScript, `bool? x` is nullable but still required, so they are declared as `bool x?`.

## Why

Image functions refused to start with "Missing param: simulate_*" because `bool? x` was still required.

## Alternatives considered

Not discussed in session notes.

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Applies to all functions with test inputs. Related hidden-fields behaviour: inputs or variables named like table columns can clash (a `$attempt` clash reset image attempt counts), covered by the Xano AI sweep still pending.

## Related notes

- [[avoid-column-named-function-inputs-in-xano]]
- [[find-executor-runs-by-id-not-timestamp]]
- [[2026-10-21-001]]
