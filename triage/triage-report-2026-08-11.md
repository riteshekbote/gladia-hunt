# Triage Report — 2026-08-11 10:38 UTC

## Scope Recap (scope.yml)
- HIGHEST: api.gladia.io
- HIGH: app.gladia.io
- MEDIUM: Official SDKs (npm @gladiaio/sdk, PyPI gladiaio-sdk)
- LOW: gladia.io
- OUT OF SCOPE: all other *.gladia.io subdomains, third-party services, automated scanner output without manual validation
- Rules: passive_first (GET/HEAD only), manual_validation_required, no_data_modification

## Prior Art (from valid-bugs.md — for Q5 duplicate check)
- npm `gladia`@0.1.3 impersonation → VALID (reported 9+ times since 2026-08-07)
- SSRF via audio_url/video_url/callback_url → HOLD (needs valid API key)
- IDOR on /{id}/file → HOLD (needs valid key + cross-account)
- WS token in URL → HOLD (design confirmed, proof needs key)
- Query injection on /v1/history → HOLD (needs valid key)
- Google OAuth callback 200 → previously assessed as NEGLIGIBLE (SPA shell, expected)
- Open redirect via redirect_to → previously assessed as BORDERLINE (needs body/Location confirmation)

---

## LEAD A — `https://app.gladia.io/auth/google/callback` → HTTP 200 (no OAuth params)

**Q1 Scope?** YES — app.gladia.io is HIGH priority asset.
**Q2 Reachable?** YES — publicly reachable, returns 200 without any OAuth state/code params.
**Q3 Real impact?** NO — The Google OAuth callback URL must be publicly reachable (it is the `redirect_uri` target for Google's OAuth flow). A 200 response without valid OAuth params is the SPA shell rendering the login page. This is normal behavior for SPA-based OAuth callbacks. No security impact from the status code alone.
**Q4 Passive proof?** YES — GET returns 200, but this proves nothing beyond "page loads."
**Q5 Novel?** NO — previously assessed in valid-bugs.md (2026-08-09 19:54) and explicitly called NEGLIGIBLE.
**Q6 Not rejected?** NO — falls under "best practice / expected behavior" for OAuth callback endpoints. A 200 on the callback URL without valid params is how SPAs handle the OAuth redirect (the client-side JS parses the fragment). Not a vulnerability.
**Q7 Triager accept?** NO — no reasonable triager accepts "OAuth callback returns 200" as a vuln.

### Verdict: **INVALID** — Expected SPA behavior; OAuth callback must be publicly reachable; previously assessed and rejected.

---

## LEAD B — `https://app.gladia.io/signin?redirect_to=https://evil.example.com` → HTTP 200

**Q1 Scope?** YES — app.gladia.io is HIGH priority.
**Q2 Reachable?** YES — publicly reachable, no auth required.
**Q3 Real impact?** UNCERTAIN — An open redirect would allow phishing (user clicks a Gladia URL, lands on attacker site). However, a 200 status code alone does NOT prove the redirect fires. The page may render with the param ignored, or the redirect may happen client-side only after auth.
**Q4 Passive proof?** NO — A 200 response does not confirm the redirect actually fires. Need to inspect response body for `Location` header or `<meta refresh>` / JS redirect to evil.example.com. Probe data only shows status code, not body.
**Q5 Novel?** PARTIALLY — open redirect was previously flagged as BORDERLINE (2026-08-09 19:54) but never confirmed. This is a new probe attempt but same underlying hypothesis.
**Q6 Not rejected?** YES — open redirect is a valid vulnerability class.
**Q7 Triager accept?** NO — not without evidence that the redirect actually fires (Location header or body content showing redirect).

### Verdict: **HOLD** — Potential open redirect, but 200 status alone is insufficient proof. Need response body / Location header inspection to confirm. Manual validation required.

---

## LEAD C — `https://app.gladia.io/auth/google/callback?code=fake123&state=abc` → HTTP 500

**Q1 Scope?** YES — app.gladia.io is HIGH priority.
**Q2 Reachable?** YES — publicly reachable.
**Q3 Real impact?** LOW — A 500 on invalid OAuth params could indicate verbose error handling, but without the response body we cannot confirm stack trace / internal path / DB error leakage. A 500 by itself is an availability concern (which is out of scope per scope.yml: "Denial of Service").
**Q4 Passive proof?** PARTIAL — GET is passive, but probe data only shows status code 500, not the body. Cannot confirm information disclosure without body content.
**Q5 Novel?** YES — this specific 500-on-fake-params observation has not been previously triaged.
**Q6 Not rejected?** BORDERLINE — verbose error messages can be a valid info-disclosure class, but a 500 status alone without body evidence is insufficient. Also borders on "best practice" (error handling).
**Q7 Triager accept?** NO — no reasonable triager accepts "500 on fake OAuth params" as a vuln without body content showing stack trace, internal IP, or sensitive data leakage.

### Verdict: **HOLD** — 500 on invalid params is interesting but unproven. Need response body to confirm information disclosure. Manual body inspection required.

---

## LEAD D — `https://api.gladia.io/v2/pre-recorded` → HTTP 401

**Q1 Scope?** YES — api.gladia.io is HIGHEST priority.
**Q2 Reachable?** YES — endpoint is reachable, returns 401 (key-gated).
**Q3 Real impact?** NONE — 401 is the expected response for an unauthenticated request to a protected endpoint. This is correct behavior.
**Q4 Passive proof?** YES — GET returns 401, proving the auth gate works.
**Q5 Novel?** NO — this 401 has been observed consistently across all probe runs since 2026-08-08. It is the baseline auth-gate confirmation.
**Q6 Not rejected?** NO — "endpoint requires auth" is not a vulnerability. This is expected behavior.
**Q7 Triager accept?** NO — a 401 on an unauthenticated request is correct auth behavior, not a vuln.

### Verdict: **INVALID** — 401 is expected auth-gate behavior; not a vulnerability.

---

## LEAD E — `https://api.gladia.io` → HTTP 404

**Q1 Scope?** YES — api.gladia.io is HIGHEST priority.
**Q2 Reachable?** YES — reachable, returns 404.
**Q3 Real impact?** NONE — 404 on the base path is normal routing behavior. No content disclosed.
**Q4 Passive proof?** YES — GET returns 404.
**Q5 Novel?** NO — previously observed in probe runs (2026-08-09 23:36, 2026-08-10 09:49, etc.).
**Q6 Not rejected?** NO — 404 is not a vulnerability.
**Q7 Triager accept?** NO — 404 on base path is normal.

### Verdict: **INVALID** — 404 is expected routing behavior; not a vulnerability.

---

## LEAD F — `https://gladia.io/bug-bounty-report` → HTTP 401

**Q1 Scope?** YES — gladia.io is LOW priority.
**Q2 Reachable?** YES — reachable, returns 401.
**Q3 Real impact?** NONE — 401 is expected for a protected resource. The path name suggests an internal bug bounty reporting endpoint, but without auth it simply returns 401.
**Q4 Passive proof?** YES — GET returns 401.
**Q5 Novel?** NO — previously observed (2026-08-10 23:59, 2026-08-11 05:32, 2026-08-11 06:11).
**Q6 Not rejected?** NO — 401 is expected behavior for a protected endpoint.
**Q7 Triager accept?** NO — 401 on a protected path is correct.

### Verdict: **INVALID** — 401 is expected auth behavior; not a vulnerability.

---

## LEAD G — `https://registry.npmjs.org/gladia` → HTTP 200 (npm `gladia` package)

**Q1 Scope?** MEDIUM — npm packages are in scope (official SDKs are MEDIUM; this is the impersonating package).
**Q2 Reachable?** YES — public npm registry, no auth required.
**Q3 Real impact?** YES — supply-chain impersonation. The `gladia` package (v0.1.3) claims "Official TypeScript SDK" but is published from a personal repo (alexisbouchez/gladia.ts) that 404s. Contains credential-leakage code pattern (API key in WS URL query param).
**Q4 Passive proof?** YES — registry metadata is publicly readable via GET. Repo 404 confirmed via GitHub API.
**Q5 Novel?** NO — this is the same npm impersonation finding already confirmed as VALID in 9+ prior triage runs (first confirmed 2026-08-07 21:04).
**Q6 Not rejected?** YES — supply-chain impersonation is a valid class.
**Q7 Triager accept?** YES — but it is a DUPLICATE.

### Verdict: **VALID (DUPLICATE)** — Already reported. Verified supply-chain squat with credential-leak code pattern. Not novel.

---

## LEAD H — `https://api.github.com/repos/alexisbouchez/gladia.ts` → HTTP 404

**Q1 Scope?** NO — GitHub is a third-party service, explicitly out of scope per scope.yml ("Third-party services").
**Q2 Reachable?** YES — public GitHub API.
**Q3 Real impact?** NONE — the repo 404s, which is evidence supporting the npm impersonation finding (Lead G), but GitHub itself is not a Gladia asset.
**Q4 Passive proof?** YES — GitHub API returns 404.
**Q5 Novel?** NO — repo 404 has been consistently observed across all probe runs.
**Q6 Not rejected?** N/A — out of scope.
**Q7 Triager accept?** NO — GitHub is not a Gladia asset.

### Verdict: **INVALID** — OUT OF SCOPE. GitHub is a third-party service. The 404 is evidence for Lead G (npm impersonation) but is not itself a Gladia vulnerability.

---

## LEAD I — `https://app.gladia.io.evil.example.com` → ERR (DNS resolution fails)

**Q1 Scope?** NO — `app.gladia.io.evil.example.com` is not a Gladia asset. It is a non-existent subdomain of evil.example.com (or a malformed hostname). Not in scope.yml.
**Q2 Reachable?** NO — DNS resolution fails.
**Q3 Real impact?** NONE — not a real asset.
**Q4 Passive proof?** N/A — unreachable.
**Q5 Novel?** N/A — not a real target.
**Q6 Not rejected?** N/A — out of scope.
**Q7 Triager accept?** NO — not a Gladia asset.

### Verdict: **INVALID** — OUT OF SCOPE. Not a Gladia asset. DNS failure confirms it does not exist.

---

## Summary Table

| Lead | URL | Verdict | Reason |
|------|-----|---------|--------|
| A | app.gladia.io/auth/google/callback → 200 | INVALID | Expected SPA behavior; OAuth callback must be public |
| B | app.gladia.io/signin?redirect_to=evil → 200 | HOLD | Possible open redirect; needs body/Location confirmation |
| C | app.gladia.io/auth/google/callback?code=fake → 500 | HOLD | 500 on fake params; needs body to confirm info disclosure |
| D | api.gladia.io/v2/pre-recorded → 401 | INVALID | Expected auth-gate behavior |
| E | api.gladia.io → 404 | INVALID | Expected routing behavior |
| F | gladia.io/bug-bounty-report → 401 | INVALID | Expected auth behavior |
| G | registry.npmjs.org/gladia → 200 | VALID (DUPLICATE) | Already reported; supply-chain impersonation |
| H | api.github.com/repos/alexisbouchez/gladia.ts → 404 | INVALID | OUT OF SCOPE (third-party) |
| I | app.gladia.io.evil.example.com → ERR | INVALID | OUT OF SCOPE (not a Gladia asset) |

## Action Items

1. **Lead B** — Manual validation needed: fetch response body for `app.gladia.io/signin?redirect_to=https://evil.example.com` and check for `Location` header or JS/meta redirect to evil.example.com. If confirmed, this is a valid open redirect (CVSS ~6.1 Medium, AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N). Report to Gladia security channel.
2. **Lead C** — Manual validation needed: fetch response body for the 500 response and check for stack traces, internal paths, or sensitive data. If confirmed, this is information disclosure.
3. **Lead G** — Already reported. No further action needed unless new evidence emerges.
4. All other leads: no action required.
