# **PRD — Parental Oversight & Content Approval**

Product: Tomale

Feature: Parental Oversight & Content Approval

Version: V1 (Launch-Grade)

1\. Purpose

Tomale allows children to create AI-generated stories. Some stories may include sensitive but appropriate themes (e.g. bullying, illness, grief).

This PRD defines a parental oversight system that locks sensitive content until a parent explicitly approves it, enforced server-side and suitable for app store review.

2\. Design Principles

\- Moderation outcomes do not change story lifecycle state

\- Enforcement is driven by explicit boolean flags

\- Household account with multiple profiles

\- Backend-first enforcement

3\. User Model

Users represent the household account (email, subscription, legal responsibility).

User profiles represent parent or child usage under the same account.

4\. Moderation Model

Moderation returns:

moderation\_status.enforcement \= parental\_oversight\_required

5\. Core Data Model (Instant Story)

Fields:

\- lifecycle\_status \= draft

\- parental\_oversight\_required (boolean)

\- parent\_approved (boolean)

\- oversight\_reason

\- approved\_by\_profile\_id

\- approved\_at

Rule:

If parental\_oversight\_required \= true AND parent\_approved \= false, child access is locked.

6\. Functional Flow

\- Child creates story

\- Moderation flags parental oversight

\- Story remains draft

\- parental\_oversight\_required set true

\- Alert \+ email sent to parent

\- Parent approves or rejects

7\. Backend Function Logic (Xano)

7.1 get\_instant\_story

If child profile and parental\_oversight\_required \= true and parent\_approved \= false:

Return redacted payload only.

7.2 approve\_instant\_story

Preconditions:

\- Caller is parent profile

\- Same household

\- parental\_oversight\_required \= true

\- parent\_approved \= false

Effects:

\- parent\_approved \= true

\- approved\_by\_profile\_id set

\- approved\_at set

7.3 reject\_instant\_story

Story remains locked. Alert resolved.

7.4 consume\_approval\_token

Validate token, apply decision, invalidate token.

8\. UI Requirements

Child UI:

\- Locked state

\- Awaiting approval message

Parent UI:

\- Approvals inbox

\- Full story visibility

\- Approve / reject actions

9\. Security & Compliance

\- No locked payload sent to child

\- Email tokens are single-use and time-limited

\- Full audit trail

10\. Verdict

This is a launch-grade parental oversight system that decouples moderation from lifecycle state, prevents trivial bypass, and satisfies app store expectations.

