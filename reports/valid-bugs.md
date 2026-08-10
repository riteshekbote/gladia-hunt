# Validated Bugs

- 2026-08-07 ~17:50 UTC — SEED STATE: 0 valid bugs. Pipeline not yet run; initial hypotheses in reports/hypotheses.md are recon-based and UNVALIDATED.

- 8 lead(s) marked VALID at 2026-08-07 21:04:32 UTC
  - | Q2 | ⚠️ PARTIAL | Endpoints are key-gated (401 without x-gladia-key); need valid key to reach fetch logic |
  - | Q4 | ❌ NO | Verify steps require `POST` with valid x-gladia-key + canary/metadata URLs — not GET/HEAD only |
  - **Verdict: HOLD** — In-scope (HIGHEST asset), real security impact, but cannot be proven with passive GET/HEAD only. Requires AUTH_HELPED testing: valid API key + POST with canary/metadata URLs to det
  - | Q2 | ⚠️ PARTIAL | Endpoints are key-gated (401 without key); need valid key + cross-user resource to test |
  - | Q4 | ❌ NO | Cannot prove without valid API key + owned resource IDs to test cross-account access |
  - **Verdict: HOLD** — In-scope (HIGHEST asset), real security impact (cross-account data access), but requires AUTH_HELPED testing: valid API key + owned transcription ID + attempt to access another use
  - | Q2 | ⚠️ PARTIAL | Token-in-URL design is visible in public OpenAPI spec, but actual token generation requires valid API key |
  - | 1 | SSRF via audio_url/video_url | api.gladia.io | **HOLD** | In-scope, real impact, but requires AUTH_HELPED (valid key + POST) |

- 14 lead(s) marked VALID at 2026-08-08 06:01:23 UTC
  - | Q2 | Reachable? | ⚠️ PARTIAL — Endpoints return 401 without x-gladia-key; fetch logic only reachable with valid API key |
  - | Q4 | Passive proof? | ❌ NO — Verify steps require `POST` with valid x-gladia-key + canary/metadata URLs to detect server-side fetch behavior. OpenAPI spec confirms design (format:uri, no scheme allo
  - **Verdict: HOLD** — In-scope (HIGHEST asset), real security impact, but cannot be proven with passive GET/HEAD only. Requires AUTH_HELPED testing: valid API key + POST with canary/metadata URLs to det
  - | Q2 | Reachable? | ⚠️ PARTIAL — Key-gated; need valid key + cross-user resource ID to test |
  - | Q4 | Passive proof? | ❌ NO — Cannot prove without valid API key + owned resource IDs to test cross-account access |
  - **Verdict: HOLD** — In-scope (HIGHEST asset), real security impact (cross-account data access), but requires AUTH_HELPED testing: valid API key + owned transcription ID + attempt to access another use
  - **Verdict: VALID** — Verified supply-chain impersonation. The npm `gladia` package (v0.1.3, dist-tag latest) claims "Official TypeScript SDK for Gladia" in its registry description, but its README say
  - | Q2 | Reachable? | ⚠️ PARTIAL — Token-in-URL design visible in public OpenAPI spec, but actual token generation requires valid API key |
  - | Q4 | Passive proof? | ❌ NO — Requires valid API key to test injection |
  - **Verdict: HOLD** — In-scope, real potential impact, but requires AUTH_HELPED testing with valid API key to confirm injection.
  - | 1 | SSRF via audio_url/callback_url | api.gladia.io | **HOLD** | Requires AUTH_HELPED (valid key + POST) |
  - | 2 | IDOR on /{id}/file | api.gladia.io | **HOLD** | Requires AUTH_HELPED (valid key + cross-user resource) |
  - | 4 | npm `gladia` impersonation | npm registry | **VALID** | Verified fact, supply-chain risk, passive proof complete |
  - | 10 | /v1/history query injection | api.gladia.io | **HOLD** | Requires AUTH_HELPED (valid key) |

- 16 lead(s) marked VALID at 2026-08-08 07:21:35 UTC
  - **Verdict: ✅ VALID**
  - | **Q2 Reachability** | **PARTIAL** — all SSRF-capable endpoints are key-gated (401 without `x-gladia-key`). CORS `*` allows cross-origin but **without credentials**, so an attacker cannot present a v
  - | **Q4 Proof (read-only)** | **NO** — requires a valid `x-gladia-key` to POST `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` and observe reachability signal. Cannot prove without AUTH_HELP
  - | **Q7 Reasonable triager** | **CONDITIONAL** — a triager would accept IF a valid key is obtained and reachability is demonstrated. Without proof, HOLD. |
  - | **Q4 Proof (read-only)** | **PARTIAL** — the *design* is confirmed via OpenAPI spec (`wss://api.gladia.io/v2/live?token=<uuid>`). Proving actual token theft/leakage requires a valid key to init a se
  - **Verdict: ⏸️ HOLD** — Design confirmed via public OpenAPI spec (no auth needed to read spec). The token-in-URL pattern is a genuine weakness. However, proving actual token theft or session hijacking 
  - | **Q2 Reachability** | **NO** — all `/{id}/file` endpoints are key-gated (401 without key). Cross-account testing requires two valid keys. |
  - | **Q4 Proof (read-only)** | **NO** — requires valid key + cross-account testing. AUTH_HELPED. |
  - | **Q6 Not rejected** | **YES** — IDOR is a valid vulnerability class. |
  - **Verdict: ⏸️ HOLD** — Cannot verify without valid API key and a second account to test cross-account access. Spec does not expose ownership-binding logic.
  - | **Q4 Proof (read-only)** | **NO** — requires valid key to test `custom_metadata[__proto__][x]=1` etc. |
  - **Verdict: ⏸️ HOLD** — Gated on valid API key.
  - | 1 | npm `gladia`@0.1.3 impersonation + WS key-in-URL | npm registry (MEDIUM) | **✅ VALID** | Verified impersonation, orphaned repo, credential leakage in WS URL |
  - | 2 | SSRF via audio_url/video_url/callback_url | api.gladia.io (HIGHEST) | **⏸️ HOLD** | Gated on valid API key for AUTH_HELPED proof |
  - | 8 | IDOR on `/{id}/file` downloads | api.gladia.io (HIGHEST) | **⏸️ HOLD** | Gated on valid key + cross-account test |
  - | 9 | Query-param injection on `/v1/history` | api.gladia.io (HIGHEST) | **⏸️ HOLD** | Gated on valid key |

- 4 lead(s) marked VALID at 2026-08-08 09:07:00 UTC
  - | 1 | npm `gladia`@0.1.3 impersonation + WS key-in-URL | **✅ VALID** | Verified impersonation, orphaned repo, credential leakage via WS URL query |
  - | 2 | SSRF via audio_url/video_url/callback_url | **⏸️ HOLD** | In-scope design confirmed; proof gated on valid API key (AUTH_HELPED) |
  - | 5 | IDOR on `/{id}/file` | **⏸️ HOLD** | Needs valid key + cross-account test |
  - | 6 | Query-param injection on `/v1/history` | **⏸️ HOLD** | Needs valid key |

- 19 lead(s) marked VALID at 2026-08-08 17:56:08 UTC
  - | Q6 Not rejected? | YES — supply-chain impersonation with credential-leakage code pattern is a valid vulnerability class, not info-disclosure of public data or best-practice. |
  - ### **Verdict: VALID**
  - | Q2 Reachable? | PARTIAL — all SSRF-capable endpoints are key-gated (401 without `x-gladia-key`). Only reachable by users with a valid API key (low-priv registered developer). |
  - | Q4 Passive proof? | NO — the *design* (fetch-by-design, no allowlist) is confirmed via OpenAPI spec and SDK source. But proving actual server-side fetch of an internal address requires POST with a v
  - | Q6 Not rejected? | YES — SSRF is a valid vulnerability class. |
  - | Q7 Triager accept? | CONDITIONAL — a triager would accept IF a valid key is obtained and reachability is demonstrated. Without proof, HOLD. |
  - ### **Verdict: HOLD** — In-scope (HIGHEST asset), real security impact (SSRF to cloud metadata/internal net), design confirmed by spec + SDK. Cannot be proven with passive GET/HEAD only. Requires AUTH
  - | Q2 Reachable? | NO for cross-account — requires two valid API keys (attacker + victim). Single-key attacker cannot reach another user's resource ID without knowing it (UUID). |
  - | Q4 Passive proof? | NO — spec does not expose ownership binding; cannot prove without valid key + owned resource ID + cross-account test. |
  - | Q6 Not rejected? | YES — IDOR is a valid vulnerability class. |
  - ### **Verdict: HOLD** — Cannot verify without valid API key and a second account to test cross-account access. Spec does not expose ownership-binding logic. UUID-based IDs make unauthenticated guessin
  - | Q2 Reachable? | PARTIAL — token issuance requires valid `x-gladia-key` (POST /v2/live). Token-in-URL design visible in public spec, but actual token generation requires auth. |
  - | Q4 Passive proof? | PARTIAL — the *design* (token in URL) is confirmed via public OpenAPI spec (no auth needed to read spec). Proving actual token theft/leakage requires a valid key to init a sessio
  - | Q6 Not rejected? | YES — credential leakage via URL is a valid vulnerability class, not just "best practice." |
  - ### **Verdict: HOLD** — Design confirmed via public OpenAPI spec (no auth needed to read). The token-in-URL pattern is a genuine weakness. However, proving actual token theft or session hijacking requ
  - | Q3 Real impact? | NEGLIGIBLE — Google OAuth callback endpoint must be publicly reachable (it's the redirect_uri target for Google's OAuth flow). 200 response without OAuth state/code is the SPA shel
  - | 1 | npm `gladia`@0.1.3 impersonation + orphaned repo + raw key in WS URL | npm registry (MEDIUM) | **VALID** | Verified supply-chain impersonation, orphaned repo, credential-leak code pattern |
  - | 2 | SSRF via audio_url/video_url/callback_url | api.gladia.io (HIGHEST) | **HOLD** | In-scope, real impact, design confirmed; proof gated on valid API key (AUTH_HELPED) |
  - | 3 | IDOR on /{id}/file downloads | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID guessing infeasible |

- 3 lead(s) marked VALID at 2026-08-08 19:52:44 UTC
  - | Q4 Proof w/o invasive? | **No** — requires valid API key + canary/internal-URL fetch (AUTH_HELPED, violates no_data_modification / passive-first) |
  - **Verdict: HOLD** — AUTH_HELPED only; needs program-provided or personal trial key + non-destructive canary fetch (audio_url → http://<your-canary>) to compare job error_code/timing. Do NOT probe 169.
  - | Q4 Proof w/o invasive? | **No** — requires valid API key + second account / known other-{id} to test cross-owner fetch |

- 4 lead(s) marked VALID at 2026-08-08 20:56:11 UTC
  - | **1. npm `gladia`@0.1.3 impersonation** | npm registry (MEDIUM) | ✅ **VALID** — Verified supply-chain squat; passive proof complete |
  - | 2. SSRF via audio_url/video_url/callback_url | api.gladia.io (HIGHEST) | ⏸️ **HOLD** — Needs valid API key (AUTH_HELPED) |
  - | 3. IDOR on `/{id}/file` downloads | api.gladia.io (HIGHEST) | ⏸️ **HOLD** — Needs valid key + cross-account test |
  - | 11. Query injection on `/v1/history` | api.gladia.io | ⏸️ **HOLD** — Needs valid key |

- 2 lead(s) marked VALID at 2026-08-08 22:25:56 UTC
  - | Q4 proof w/o invasive testing | NO — spec-only; ownership-binding logic is opaque, requires a valid key to test cross-account access. |
  - **Verdict: HOLD (parked)** — retained as AUTH_HELPED; not reportable without a valid key. Below the confidence floor for a spec-only IDOR.

- 4 lead(s) marked VALID at 2026-08-08 23:17:09 UTC
  - | **Q4 Read-only proof?** | ❌ NO — requires `POST` with a valid `x-gladia-key` to test; invasive. Passive probes confirm the *surface* (spec says `format:uri` with no scheme allowlist; SDK forwards `a
  - | **Q7 Triager accept?** | ⚠️ CONDITIONAL — a triager would accept this *only* with a key-gated POC. Without a valid key, it remains a strong hypothesis |
  - **Verdict: VALID**
  - | 2 | npm `gladia@0.1.3` impersonation | npm registry | **VALID** | 85 | 5.4 |

- 7 lead(s) marked VALID at 2026-08-09 03:12:30 UTC
  - | Q2 Reachability | ⚠️ Key-gated — all v2 endpoints return 401 without `x-gladia-key`. An attacker needs a valid API key. |
  - | Q4 Proof without invasive testing | ❌ **No** — requires `POST` with a valid `x-gladia-key` and canary/internal-URL comparison. Purely AUTH_HELPED. |
  - | Q7 Reasonable triager | ❌ **No** — cannot be validated without a valid API key. Per `rules.passive_first` and `rules.no_data_modification`, this cannot be proven with GET/HEAD alone. Per `rules.manu
  - | Q7 Reasonable triager | ❌ **No** — no reasonable triager accepts `x-powered-by: Express` as a valid vulnerability. |
  - | Q4 Proof without invasive testing | ❌ **No** — requires two different valid API keys to test cross-account access. AUTH_HELPED. |
  - | 1 | SSRF via audio_url/video_url/callback_url | api.gladia.io | **HOLD** | AUTH_HELPED — unverifiable without valid API key |
  - | 5 | IDOR on /{id}/file downloads | api.gladia.io | **HOLD** | AUTH_HELPED — needs two valid keys to test |

- 1 lead(s) marked VALID at 2026-08-09 05:39:02 UTC
  - | Q6 Not rejected? | ✅ YES — supply-chain impersonation is a valid class |

- 10 lead(s) marked VALID at 2026-08-09 08:28:05 UTC
  - | Q2 | ✅ Yes — reachable with any valid `x-gladia-key` (low-priv self-service key) |
  - | Q4 | ❌ No — proof requires `POST` with a valid key (state-changing, paid action). Cannot prove with GET/HEAD only |
  - **Verdict: VALID** — fully provable, passive-only, in-scope (official SDK scope, counterfeit asset).
  - | Q2 | ⚠️ Requires valid key on both sides (attacker + victim resource) |
  - | Q4 | ❌ No — requires two valid sessions + owned resources; spec does not expose ownership-binding |
  - | Q2 | ⚠️ Token is bearer-equivalent for a live session; obtainable only with a valid `x-gladia-key` |
  - **Verdict: HOLD** — design smell with real implications (token in URL leaks via logs/Referer), but requires a valid key to demonstrate, and the design is spec-documented (intentional). Lower priority 
  - | Q2 | ⚠️ Requires valid key (endpoint returns 401 unauthenticated) |
  - | 1 | SSRF via audio_url/video_url/callback_url | api.gladia.io | **HOLD** | Needs valid key + POST; cannot prove passive-only |
  - | 3 | npm `gladia`@0.1.3 impersonation | npm registry | **VALID** | Fully provable passive; metadata contradiction confirmed |

- 12 lead(s) marked VALID at 2026-08-09 09:28:12 UTC
  - | **Q6 Not rejected?** | ✅ YES — supply-chain impersonation is a valid class, not info-disclosure of public data or best-practice |
  - ### **Verdict: ✅ VALID**
  - | **Q4 Passive proof?** | ❌ NO — OpenAPI spec confirms `format:uri` with no scheme allowlist; SDK source confirms verbatim forwarding. But proving actual server-side fetch requires `POST` with valid k
  - | **Q6 Not rejected?** | ✅ YES — SSRF is a valid class |
  - | **Q6 Not rejected?** | ✅ YES — open redirect is a valid class |
  - | **Q2 Reachable?** | ⚠️ PARTIAL — endpoints key-gated; cross-account testing requires two valid keys |
  - | **Q6 Not rejected?** | ✅ YES — IDOR is valid |
  - | **Q2 Reachable?** | ⚠️ PARTIAL — token issuance requires valid `x-gladia-key`; design visible in public spec |
  - | **Q4 Passive proof?** | ⚠️ PARTIAL — design confirmed via OpenAPI spec (`wss://api.gladia.io/v2/live?token=<uuid>`); actual token theft/leakage requires valid key |
  - | **Q7 Triager accept?** | ❌ NO — no reasonable triager accepts this as a valid vuln |
  - | 1 | npm `gladia@0.1.3` impersonation | npm registry (MEDIUM) | ✅ **VALID** |
  - | 2 | SSRF via audio_url/video_url/callback_url | api.gladia.io (HIGHEST) | ⏸️ HOLD — needs valid key |

- 5 lead(s) marked VALID at 2026-08-09 14:25:07 UTC
  - | npm `gladia`@0.1.3 impersonation | **VALID** | Supply-chain squat, verified fact, passive proof complete — report to Gladia security channel |
  - | SSRF via audio_url/video_url/callback_url | **HOLD** | AUTH_HELPED only — requires valid API key + POST |
  - | IDOR on `/{id}/file` downloads | **HOLD** | AUTH_HELPED only — requires valid key + cross-account test |
  - | WebSocket auth token in URL | **HOLD** | Design confirmed via public spec; proof of leakage requires valid key |
  - | Query-param injection on `/v1/history` | **HOLD** | AUTH_HELPED only — requires valid key to test injection |

- 2 lead(s) marked VALID at 2026-08-09 19:54:26 UTC
  - | Q7 Reasonable triager? | **BORDERLINE** — 200 on signin page is expected even with valid redirect_to param; need body/Location header to confirm redirect actually fires |
  - | Q3 Real impact? | **UNLIKELY** — callback without valid OAuth state/code typically renders the login page (normal behavior). 500 on fake params could be verbose error but no body to confirm |

- 8 lead(s) marked VALID at 2026-08-09 21:57:23 UTC
  - ### Verdict: **VALID** ✅
  - | Q2 | **PARTIAL** — all v2 endpoints require `x-gladia-key` (401 unauthenticated). Attacker needs a valid key |
  - | Q4 | **NO** — proving SSRF requires POST with canary/internal URLs and observing error/timing; requires a valid API key (AUTH_HELPED). Cannot prove with GET/HEAD only |
  - | Q2 | **NO** — requires valid `x-gladia-key` to test; cross-account testing needs two keys |
  - | Q4 | **NO** — cannot prove without two valid API keys and owned resources |
  - | Q2 | **PARTIAL** — token is bearer-equivalent but requires valid `x-gladia-key` to generate |
  - | Q4 | **NO** — cannot prove token leakage without generating a valid session (AUTH_HELPED); the OpenAPI spec confirms the design but doesn't prove exploitation |
  - | 1 | npm `gladia@0.1.3` impersonation | npm (MEDIUM) | **VALID** ✅ | Verified ownership anomaly, real supply-chain risk |

- 20 lead(s) marked VALID at 2026-08-09 22:57:20 UTC
  - valid-bugs.md
  - | Q6 | Not rejected? | ✅ YES — supply-chain impersonation with a credential-handling SDK is a valid class; it is not "info disclosure of public data" (the package handles API keys) |
  - ### **Verdict: VALID ✅**
  - | Q2 | Reachable? | ⚠️ PARTIAL — all `/v2/*` endpoints return `401 "no gladia key provided"` (uniform gate per probe-results.md). Fetch logic only reachable with a valid `x-gladia-key` |
  - | Q4 | Passive proof? | ❌ NO — OpenAPI spec confirms *design* (`audio_url`/`video_url`/`CallbackConfigDto.url` all `format:uri` with no scheme allowlist), and SDK source forwards verbatim. But proving
  - | Q6 | Not rejected? | ✅ YES — SSRF is a valid class |
  - | Q7 | Triager accept? | ⚠️ CONDITIONAL — would accept only with a key-gated POC. Without a valid key, remains a strong hypothesis |
  - | Q2 | Reachable? | ⚠️ PARTIAL — endpoints return 401 without key; cross-account testing needs two valid keys |
  - | Q4 | Passive proof? | ❌ NO — spec does not expose ownership-binding logic; cannot prove without valid key + cross-account test |
  - | Q6 | Not rejected? | ✅ YES — IDOR is a valid class |
  - | Q2 | Reachable? | ⚠️ PARTIAL — token issuance requires valid `x-gladia-key`; design visible in public OpenAPI spec |
  - | Q4 | Passive proof? | ⚠️ PARTIAL — the *design* (`wss://api.gladia.io/v2/live?token=<uuid>`) is confirmed via public OpenAPI spec (no auth needed to read spec). Proving actual token theft requires a
  - | Q6 | Not rejected? | ⚠️ BORDERLINE — "credential in URL" is a valid weakness, but many cloud APIs do this by design. Absent evidence of long-lived tokens or actual leakage, this leans toward "best p
  - | Q6 | Not rejected? | ✅ YES — open redirect is a valid class |
  - | Q2 | Reachable? | ⚠️ PARTIAL — `/v1/history` returns 401 without key (probe-results.md consistent); injection testing requires a valid `x-gladia-key` |
  - | Q4 | Passive proof? | ❌ NO — spec confirms `custom_metadata` as `additionalProperties:true` object param, but proving injection requires `GET /v1/history?custom_metadata[__proto__][x]=1` with a vali
  - | Q6 | Not rejected? | ✅ YES — injection is a valid class |
  - | Q7 | Triager accept? | ❌ NO — spec-only; no evidence of actual injection without a valid key |
  - | Q7 | Triager accept? | ❌ NO — no reasonable triager accepts `x-powered-by: Express` as a valid vulnerability |
  - | 1 | npm `gladia`@0.1.3 impersonation | npm registry (MEDIUM) | **✅ VALID** | 4.3 Med |

- 20 lead(s) marked VALID at 2026-08-10 07:30:06 UTC
  - | 1 | npm `gladia`@0.1.3 impersonation / supply-chain squat | npm registry (MEDIUM) | **VALID** | Verified fact; passive proof complete; metadata contradiction confirmed |
  - | 2 | SSRF via audio_url/video_url/callback_url server-side fetch | api.gladia.io (HIGHEST) | **HOLD** | Design confirmed (spec + SDK); proof requires AUTH_HELPED (valid key + POST) |
  - | 3 | IDOR on `/{id}/file` download endpoints | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID guessing infeasible |
  - | 4 | WebSocket auth token in URL query parameter | api.gladia.io (HIGHEST) | **HOLD** | Design confirmed via public spec; proving leakage requires valid key |
  - | 11 | Query-param injection on `/v1/history` (custom_metadata, arrays) | api.gladia.io (HIGHEST) | **HOLD** | Spec confirms object/array params; needs valid key to test injection |
  - | Q5 Novel? | YES — not previously reported to Gladia (per valid-bugs.md, this is the only confirmed finding) |
  - | Q6 Not rejected? | YES — supply-chain impersonation with future compromise potential is a valid vulnerability class, not info-disclosure or best-practice |
  - | Q4 Passive proof? | NO — OpenAPI spec confirms design (audio_url, video_url, CallbackConfigDto.url all `format:uri` with no scheme allowlist). Proving actual server-side fetch requires POST with val
  - | Q6 Not rejected? | YES — SSRF is a valid vulnerability class |
  - | Q7 Triager accept? | CONDITIONAL — only if reachability demonstrated with valid key |
  - | Q2 Reachable? | NO for cross-account — requires valid API key + known resource ID owned by another user; UUID-based IDs make guessing infeasible |
  - | Q6 Not rejected? | YES — IDOR is a valid vulnerability class |
  - | Q2 Reachable? | PARTIAL — token-in-URL design visible in public OpenAPI spec; actual token generation requires valid API key |
  - | Q4 Passive proof? | PARTIAL — design confirmed via public spec (`wss://api.gladia.io/v2/live?token=<uuid>`); proving actual leakage requires valid key to init session and inspect Referer headers |
  - | Q6 Not rejected? | YES — credential leakage via URL is a valid vulnerability class |
  - | Q4 Passive proof? | NO — requires valid API key to test injection strings |
  - | Q6 Not rejected? | YES — injection is a valid vulnerability class |
  - | Q7 Triager accept? | CONDITIONAL — only if injection demonstrated with valid key |
  - | `https://app.gladia.io.evil.example.com` | ERR | DNS resolution fails — not a valid Gladia asset |
  - | **VALID** | 1 | npm `gladia`@0.1.3 impersonation |
