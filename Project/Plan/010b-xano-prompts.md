---
type: plan
title: "010b sign-up: Xano AI prompts (B1–B3)"
project: tomale-rn-v1
status: active
date: 2026-11-23
related:
  - "[[010b-auth-signup-micro-prd]]"
---

# 010b: Xano AI prompts

Paste one at a time, in order. Send Claude the Xano AI's summary (or the code) before publishing each. Refusals follow 009: `inputerror` (400) with `payload: {code, message}`.

## X1: schema
```
Schema change only. Don't change any endpoint or function.
Table "users": add terms_accepted_at (timestamp, nullable) and terms_version (text, nullable).
```

## X2: verification email as a function
```
Create a custom function auth/send_verification_email with input int users_id. Change nothing else yet.
It does exactly what the post_process block in POST /auth/signup does today for the verification email, and nothing more:
1. security.create_uuid as the token.
2. db.edit users (id = users_id): email_verification_token = token, email_ver_expires_at = now + 86400 seconds, last_modified_at = now.
3. function.run "admin/resend_dynamic_send" with the same template_id ("ddfd2586-fdce-4fec-bed4-97318a921e1b") and variables user_firstname and token, to the user's email.
Return {sent: true}.
```

## X3: sign-up (B2 + B3)
```
Change POST /auth/signup in the app API group. Change nothing else.
1. Add inputs: bool terms_accepted, text terms_version filters=trim.
2. Before db.add users, check in this order, each as inputerror (400) with payload {code, message}:
   - terms_accepted !== true, or terms_version empty → code "TERMS_REQUIRED", message "Please agree to the Terms and Privacy Notice."
   - the existing "email already in use" precondition: change it from accessdenied to inputerror with payload code "EMAIL_IN_USE", message "This email has already been used, please use another." Keep the lookup as it is.
   Don't add a password check: the users.password field already enforces the rule.
3. In db.add users, also set terms_accepted_at = now and terms_version = $input.terms_version.
4. In the post_process block, replace the token db.edit and the resend_dynamic_send call with function.run "auth/send_verification_email" {users_id: $new_user.id}. Keep the Stripe customer, the Stripe db.edit and the user log exactly as they are.
5. The response stays exactly as it is.
Strict comparisons; codes in payload.code.
```

## X4: resend the verification email (B1)
```
Add POST /auth/resend_verification in the app API group. Authentication required (users). No inputs. Change nothing else.
1. Load the user for $auth.id.
2. email_verified === true → inputerror (400) payload {code "ALREADY_VERIFIED", message "Your email is already confirmed."}.
3. email_ver_expires_at is set and later than now + 86340 seconds (so the last email went out less than 60 seconds ago) → inputerror (400) payload {code "TOO_SOON", message "Please wait a minute and try again."}.
4. Otherwise function.run "auth/send_verification_email" {users_id: $auth.id}.
5. Return {sent: true}. No user fields.
Strict comparisons; codes in payload.code.
```

## X5 (optional, two minutes): make the verify token required
```
In GET /auth/verify_email, make the token input required (text token filters=trim, not optional). Change nothing else.
```

## Postman checks (Kyle, by hand; use plus-addressed emails such as kaburke88+010b1@gmail.com)
- Sign-up with a new email, terms ticked → 200, email arrives, `terms_accepted_at` and `terms_version` = `2026-11-19` stored.
- Same email again → 400 `EMAIL_IN_USE`. Missing `terms_accepted` → `TERMS_REQUIRED`. Password `abcdefgh` → note the status and body the field-level rule returns (no code expected; the app shows its own line). Email `kyle@` → Xano's own input error (no code).
- Resend with the new account's token straight away → `TOO_SOON`; after 60 s → `{sent: true}` and a second email; after confirming → `ALREADY_VERIFIED`.
- Then `pnpm update:openapi`; Cursor adds overlay entries for the sign-up refusals and resend, with recorded fixtures (personal data replaced).
