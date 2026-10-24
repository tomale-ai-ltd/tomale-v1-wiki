
---

# CTO Improvements — Implementation Checklist

> Evaluation key:
> Priority: 1 = Immediate/Critical · 2 = High · 3 = Desirable/Future
> Benefit / Difficulty / Cost: 1 = Low · 5 = High (estimated relative to others, not absolute)

---

## Authentication & Authorization

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Require auth on all endpoints (except unauthed journeys) | 1 | 5 | 3 | 2 | [ ] |
| Implement owner-or-deny-all ReBAC foundation | 1 | 5 | 3 | 2 | [ ] |
| Derive user identity from token, not request params | 1 | 4 | 2 | 1 | [ ] |
| Rotate detected secrets + add Gitleaks to CI | 1 | 5 | 2 | 2 | [ ] |
| Enable MFA on Xano admin portal + separate admin creds | 1 | 5 | 1 | 1 | [ ] |

## Security & Data Model

| Item                                                    | Priority | Benefit | Difficulty | Cost | Done |
| ------------------------------------------------------- | -------- | ------- | ---------- | ---- | ---- |
| Enable Rate Limiting on API endpoints                   | 2        | 4       | 2          | 2    | [ ]  |
| Enable Sensitive Data Flagging in Xano                  | 1        | 3       | 1          | 1    | [ ]  |
| Add owner_user to all user data (character_traits etc.) | 2        | 4       | 2          | 1    | [ ]  |
| Separate dev and production environments                | 1        | 5       | 3          | 3    | [ ]  |

## Package & CI/CD

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Switch to pnpm | 2 | 4 | 2 | 1 | [ ] |
| Add minimumReleaseAge (7 days) + pnpm audit | 2 | 4 | 1 | 1 | [ ] |
| Define package update process | 3 | 3 | 1 | 1 | [ ] |

## Testing

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Enable code coverage at 85% threshold | 2 | 3 | 2 | 1 | [ ] |
| Translate acceptance criteria into automated tests | 2 | 4 | 3 | 2 | [ ] |

## Automated Scans

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Add Sonarqube or Semgrep to CI/CD | 2 | 4 | 2 | 1 | [ ] |

## Logging & Alerting (Sentry)

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Implement Source Maps + Debug Symbols | 2 | 3 | 3 | 3 | [ ] |
| Enrich events with anonymized user identifier | 2 | 4 | 2 | 1 | [ ] |
| Set up Tracing + Profiling | 2 | 4 | 2 | 1 | [ ] |

## Other

| Item | Priority | Benefit | Difficulty | Cost | Done |
|---|---|---|---|---|---|
| Signed URLs for images (Xano Private File Storage) | 2 | 4 | 2 | 2 | [ ] |
| Require email validation for new user sign-up | 2 | 3 | 2 | 2 | [ ] |

---

## Related notes
- [[plan/cto-tech-review]]
- [[stack/xano]]
- [[stack/deployment-eas]]