---
type: decision
title: defer-postman-monitor-until-launch
project: tomale-rn-v1
status: accepted
date: 2026-10-13
---

---

# Decision: defer-postman-monitor-until-launch

## What we decided

No Postman monitor before launch. Pre-launch, run the `_tests` collection manually in the Runner after backend changes and before go-live orders. At launch, set up a daily monitor with the run kept under the 10-minute Free-plan limit (B1 ~24 attempts, C1 ~6).

## Why

Monitors have a 10 min (Free) / 15 min (paid) run limit and only see shared variable values; a full order run takes ~3.5–5.7 min to Order Confirmed plus PDF generation of ~2–5 min, so it is tight.

## Alternatives considered

Running a monitor now was weighed against the limits above and deferred.

## Trade-offs accepted

No scheduled regression signal until launch; relies on manual runs.

## Workflow detail

Run `_tests` manually after backend changes. At launch, trim polling attempts to fit the limit.

## Related notes

- [[replace-manual-test-gates-with-bounded-polling]]
- [[simulate-stripe-payment-with-signed-postman-webhook]]
- [[2026-10-13-001]]
