---
type: decision
title: use-run-scoped-postman-token-in-tests-login
project: tomale-rn-v1
status: accepted
date: 2026-10-22
related:
  - "[[2026-10-22-001]]"
  - "[[2026-10-21-001]]"
---

# Decision: use-run-scoped-postman-token-in-tests-login

## What we decided

In the Postman `_tests` suite, login request 1A also sets the token as a run-scoped variable (`pm.variables.set("bearerToken", …)`), which overrides the environment value for the rest of the run. The legacy `app` folder auto-login script was deleted.

## Why

On the first run 1B failed with "token expired": it read the previous run's token because 1A's `pm.environment.set` wasn't visible within the same run. The legacy `app` script used the same variables; deleting it alone didn't fix the first-run failure.

## Alternatives considered

Making `bearerToken` a default (not secret) environment variable, or using a `{{runToken}}` collection variable (both raised 21/10).

## Trade-offs accepted

Not discussed in session notes.

## Workflow detail

Recorded as a working rule: Postman tokens are run-scoped in 1A. Requests in the run pick up the fresh token from 1A without relying on the environment write.

## Related notes

- [[2026-10-22-001]]
- [[2026-10-21-001]]
- [[defer-postman-suite-ci-until-suite-split]]
- [[return-401-invalid-refresh-token-from-auth-refresh]]
