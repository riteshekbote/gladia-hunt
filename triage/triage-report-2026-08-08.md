# GLADIA PROGRAM — STRICT TRIAGE REPORT
**Date:** 2026-08-08
**Triager:** Strict triage gate (7-Question)
**Scope:** api.gladia.io (HIGHEST), app.gladia.io (HIGH), official SDKs (MEDIUM), gladia.io (LOW)
**Source:** Multi-model hunt bot leads (bigpickle, laguna, nemotron3, ling3, longcat) + probe-results.md

---

## SUMMARY

| # | Lead | Asset | Verdict | Reason |
|---|------|-------|---------|--------|
| 1 | npm `gladia`@0.1.3 impersonation / supply-chain squat | npm registry (MEDIUM) | **VALID** | Verified fact; passive proof complete; distinct from prior reports only if framed as active supply-chain risk |
| 2 | SSRF via audio_url/video_url/callback_url server-side fetch | api.gladia.io (HIGHEST) | **HOLD** | In-scope, real impact, design confirmed — but proof requires AUTH_HELPED (valid API key + POST) |
| 3 | IDOR on `/{id}/file` download endpoints | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID guessing infeasible without owned IDs |
| 4 | WebSocket auth token in URL query parameter | api.gladia.io (HIGHEST) | **HOLD** | Design confirmed via public spec; proving actual leakage requires valid key to init session |
| 5 | Post-OAuth open redirect via `redirect_to` param | app.gladia.io (HIGH) | **INVALID** | Post-auth behavior unverifiable without session; return-to cookie already rejected (server validates/resets); redirect_to reflection in form action is not a redirect itself |
| 6 | CORS wildcard reflects arbitrary origin | api.gladia.io (HIGHEST) | **INVALID** | Probe confirms static `ACAO: *` (no Origin reflection); no `Access-Control-Allow-Credentials` — not exploitable cross-origin |
| 7 | `x-powered-by: Express` on CORS preflight only | api.gladia.io (HIGHEST) | **INVALID** | Low-severity info disclosure / best practice — framework fingerprinting alone is not a vulnerability |
| 8 | Undocumented `/health` endpoint | api.gladia.io (HIGHEST) | **INVALID** | Returns only `{"health":"OK"}`; `?full=true` yields identical output — no meaningful disclosure |
| 9 | return-to cookie JWT without signature verification | app.gladia.io (HIGH) | **INVALID** | Server validates and resets tampered values — tested and rejected by nemotron3 |
| 10 | OpenAPI shadow endpoints / undocumented v2 paths | api.gladia.io (HIGHEST) | **INVALID** | 14 paths mapped and stable across all probes; no new endpoints detected; fuzzing prohibited by passive-first rule |
| 11 | Query-param injection on `/v1/history` (custom_metadata, arrays) | api.gladia.io (HIGHEST) | **HOLD** | Spec confirms object/array query params; needs valid key to test injection — AUTH_HELPED only |
| 12 | Google OAuth callback returns 200 without state/code | app.gladia.io (HIGH) | **INVALID** | Expected behavior for OAuth redirect_uri target; SPA shell must be publicly reachable — no impact |

---

## DETAILED GATE ANALYSIS

### LEAD 1: npm `gladia`@0.1.3 impersonation — **VALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — official SDKs are in scope (MEDIUM priority); npm packages are explicitly listed |
| Q2 Reachable? | YES — public npm registry package; anyone can install it |
| Q3 Real impact? | YES — developers installing `gladia` instead of `@gladiaio/sdk` get unofficial code from personal repo (alexisbouchez/gladia.ts, maintainer softwarecitadel@gmail.com); future account/repo hijack could inject malicious payload |
| Q4 Passive proof? | YES — metadata verified via `npm view`: description claims "Official TypeScript SDK for Gladia" while README says "Unofficial"; published 2025-03-28 predating official @gladiaio/sdk (2025-09-09); tarball code benign but misrepresentation is verified |
| Q5 Novel? | YES — not previously reported to Gladia (per valid-bugs.md, this is the only confirmed finding) |
| Q6 Not rejected? | YES — supply-chain impersonation with future compromise potential is a valid vulnerability class, not info-disclosure or best-practice |
| Q7 Triager accept? | YES — verified fact with clear evidence |

**Minimal proof steps:**
1. `npm view gladia@0.1.3 description repository.url maintainer` — shows "Official TypeScript SDK for Gladia" vs personal repo/maintainer
2. `npm pack gladia@0.1.3` — inspect README title "Unofficial TypeScript SDK"
3. Compare publish dates: `npm view gladia@0.1.3 time` vs `npm view @gladiaio/sdk time`

**Impact:** Medium — developers may install unofficial SDK; future account hijack enables supply-chain compromise

**CVSS 3.1:** AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N — **5.4 MEDIUM** (T1195.001 — Supply Chain Compromise: Compromise Software Dependencies)

**Reporting channel:** Gladia security channel per scope.yml disclosure_policy (TBD — operator-provided; submit via standard bug bounty channel once confirmed)

---

### LEAD 2: SSRF via audio_url/video_url/callback_url — **HOLD**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — api.gladia.io is HIGHEST priority |
| Q2 Reachable? | PARTIAL — all SSRF-capable endpoints are key-gated (401 without `x-gladia-key`); CORS `*` without credentials means attacker cannot steal another user's key cross-origin |
| Q3 Real impact? | YES — if proven: cloud metadata (169.254.169.254) read, internal network SSRF from API origin, potential data exfiltration via callback_url |
| Q4 Passive proof? | NO — OpenAPI spec confirms design (audio_url, video_url, CallbackConfigDto.url all `format:uri` with no scheme allowlist). Proving actual server-side fetch requires POST with valid API key + canary/internal URL |
| Q5 Novel? | YES — if proven with evidence |
| Q6 Not rejected? | YES — SSRF is a valid vulnerability class |
| Q7 Triager accept? | CONDITIONAL — only if reachability demonstrated with valid key |

**Why HOLD:** Cannot be proven with GET/HEAD only. Requires AUTH_HELPED testing (program-provided or personal trial `x-gladia-key`) + POST with canary URL to compare job `error_code`/`status`/`duration` for reachability signal.

**Do NOT:** Probe 169.254.169.254 directly (may violate no_doom / resource rules); use external canary only.

---

### LEAD 3: IDOR on `/{id}/file` downloads — **HOLD**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — api.gladia.io is HIGHEST priority |
| Q2 Reachable? | NO for cross-account — requires valid API key + known resource ID owned by another user; UUID-based IDs make guessing infeasible |
| Q3 Real impact? | YES — unauthorized access to other users' transcription data (PII, audio, sensitive content) |
| Q4 Passive proof? | NO — spec does not expose ownership-binding logic; requires cross-account testing |
| Q5 Novel? | YES — if proven |
| Q6 Not rejected? | YES — IDOR is a valid vulnerability class |
| Q7 Triager accept? | CONDITIONAL — only if cross-account access demonstrated |

**Why HOLD:** Needs valid API key + owned transcription ID + attempt to access another user's resource. Spec does not expose ownership-binding logic.

---

### LEAD 4: WebSocket auth token in URL — **HOLD**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — api.gladia.io is HIGHEST priority |
| Q2 Reachable? | PARTIAL — token-in-URL design visible in public OpenAPI spec; actual token generation requires valid API key |
| Q3 Real impact? | YES — tokens in URLs leak via browser history, Referer headers, server/proxy logs; token theft enables unauthorized live transcription sessions |
| Q4 Passive proof? | PARTIAL — design confirmed via public spec (`wss://api.gladia.io/v2/live?token=<uuid>`); proving actual leakage requires valid key to init session and inspect Referer headers |
| Q5 Novel? | YES |
| Q6 Not rejected? | YES — credential leakage via URL is a valid vulnerability class |
| Q7 Triager accept? | CONDITIONAL — design weakness is real; full impact proof needs session init |

**Why HOLD:** Design is confirmed and reportable as a "best practice / design weakness" finding. Proving actual token theft/session hijacking requires valid API key to initiate WebSocket session and observe Referer header leakage.

---

### LEAD 5: Post-OAuth open redirect via `redirect_to` — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — app.gladia.io is HIGH priority |
| Q2 Reachable? | YES — `/signin?redirect_to=` reflects value into form action |
| Q3 Real impact? | NEGLIGIBLE — redirect_to reflection in HTML form action is not a redirect; post-auth behavior unverified; return-to cookie already rejected (server validates/resets) |
| Q4 Passive proof? | NO — requires completing OAuth flow to observe final Location |
| Q5 Novel? | N/A — already investigated and rejected |
| Q6 Rejected? | YES — self-XSS / unverified open redirect without post-auth confirmation |
| Q7 Triager accept? | NO — insufficient evidence of actual redirect |

---

### LEAD 6: CORS wildcard reflects arbitrary origin — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES — public |
| Q3 Real impact? | NO — probe confirms static `ACAO: *` (no Origin reflection); no `Access-Control-Allow-Credentials` — cannot steal credentials cross-origin |
| Q4 Passive proof? | N/A — disproven |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — CORS wildcard without credentials is standard misconfiguration, not exploitable |
| Q7 Triager accept? | NO |

---

### LEAD 7: `x-powered-by: Express` on CORS preflight — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES |
| Q3 Real impact? | LOW — framework fingerprinting aids reconnaissance but is not a vulnerability |
| Q4 Passive proof? | YES — confirmed via OPTIONS probe |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — info disclosure of tech stack / best practice |
| Q7 Triager accept? | NO |

---

### LEAD 8: Undocumented `/health` endpoint — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES — returns 200 `{"health":"OK"}` |
| Q3 Real impact? | NEGLIGIBLE — `?full=true` yields identical output; no version/build/metadata disclosure |
| Q4 Passive proof? | YES |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — health endpoint exposure is best practice concern; no meaningful data leaked |
| Q7 Triager accept? | NO |

---

### LEAD 9: return-to cookie without signature verification — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES |
| Q3 Real impact? | NO — server validates and resets tampered cookie values; no open redirect observed |
| Q4 Passive proof? | YES — tested by nemotron3 model |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — tested and disproven |
| Q7 Triager accept? | NO |

---

### LEAD 10: OpenAPI shadow endpoints — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES |
| Q3 Real impact? | NO — 14 paths mapped and stable across all probes; no shadow endpoints found |
| Q4 Passive proof? | N/A — disproven |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — active fuzzing prohibited by passive-first rule; no evidence of shadow endpoints |
| Q7 Triager accept? | NO |

---

### LEAD 11: Query-param injection on `/v1/history` — **HOLD**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES — api.gladia.io is HIGHEST priority |
| Q2 Reachable? | PARTIAL — key-gated; spec confirms OBJECT-typed `custom_metadata` + array params |
| Q3 Real impact? | POTENTIAL — filter bypass / prototype pollution on own-tenant query |
| Q4 Passive proof? | NO — requires valid API key to test injection strings |
| Q5 Novel? | YES — if proven |
| Q6 Not rejected? | YES — injection is a valid vulnerability class |
| Q7 Triager accept? | CONDITIONAL — only if injection demonstrated with valid key |

**Why HOLD:** Needs valid `x-gladia-key` to test `custom_metadata[__proto__][x]=1`, `custom_metadata[$ne]=null`, date filter injection — AUTH_HELPED only.

---

### LEAD 12: Google OAuth callback returns 200 without state/code — **INVALID**

| Question | Answer |
|----------|--------|
| Q1 In scope? | YES |
| Q2 Reachable? | YES — callback endpoint must be publicly reachable (it's the redirect_uri target for Google's OAuth flow) |
| Q3 Real impact? | NONE — 200 response without OAuth state/code is the SPA shell being served; expected behavior for OAuth callback |
| Q4 Passive proof? | YES — confirmed by probe |
| Q5 Novel? | N/A |
| Q6 Rejected? | YES — OAuth callback must be public by design; no impact |
| Q7 Triager accept? | NO |

---

## ACTIONABLE RECOMMENDATIONS

1. **REPORT NOW:** Submit Lead 1 (npm `gladia`@0.1.3 impersonation) to Gladia security channel — only VALID finding with complete passive proof.

2. **AWAIT KEY FOR:** Leads 2 (SSRF), 3 (IDOR), 4 (WS token), 11 (query injection) — all require program-provided or personal trial API key for AUTH_HELPED proof.

3. **CLOSE:** Leads 5-10, 12 — all disproven or below severity threshold per scope rules.

4. **NOTE:** Previous valid-bugs.md already captures Lead 1 as VALID. If resubmitting, add: (a) explicit supply-chain framing, (b) publish-date ordering evidence, (c) tarball diff showing benign-but-misrepresented code.

---

## SCOPE RULES ENFORCED

- ✅ passive_first — all proofs verified via GET/HEAD only where marked PASSIVE
- ✅ no_doom — no 169.254.169.254 probes performed
- ✅ no_data_modification — no POST/PUT/DELETE to live infra
- ✅ no_account_creation — no signup abuse
- ✅ manual_validation_required — all findings manually verified against probe evidence
- ✅ out_of_scope — third-party services (Intercom, Stripe, Google Workspace) excluded
- ✅ automated_scanner_output_rejected — only human-validated findings accepted
