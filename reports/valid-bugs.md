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

- 3 lead(s) marked VALID at 2026-08-10 10:45:01 UTC
  - | VALID | 2 | npm `gladia`@0.1.3 impersonation + API key harvesting via WS URL query param |
  - | HOLD | 4 | SSRF (audio_url), IDOR (/{id}/file), WS token in URL, /v1/history query injection — all need AUTH_HELPED (valid API key) |
  - - GitHub repo 404 confirmed for alexisbouchez/gladia.ts — strengthens VALID verdict for npm impersonation

- 18 lead(s) marked VALID at 2026-08-10 12:38:42 UTC
  - | 1 | npm `gladia`@0.1.3 impersonation + API key exfil via WS URL | npm registry (MEDIUM) | **VALID** | Verified fact; passive proof complete; repo 404 (irrevocable); dist-tag latest static; key-in-UR
  - | 2 | SSRF via audio_url/video_url/callback_url server-side fetch | api.gladia.io (HIGHEST) | **HOLD** | In-scope, real impact, design confirmed — but proof requires AUTH_HELPED (valid API key + POST)
  - | 3 | IDOR on `/{id}/file` download endpoints | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID guessing infeasible without owned IDs |
  - | 4 | WebSocket auth token in URL query parameter | api.gladia.io (HIGHEST) | **HOLD** | Design confirmed via public spec; proving actual leakage requires valid key to init session |
  - | 11 | Query-param injection on `/v1/history` (custom_metadata, arrays) | api.gladia.io (HIGHEST) | **HOLD** | Spec confirms object/array query params; needs valid key to test injection — AUTH_HELPED 
  - | Q5 Novel? | YES — not previously reported to Gladia (per valid-bugs.md); the API key harvesting vector adds new dimension to prior VALID finding |
  - | Q6 Not rejected? | YES — supply-chain impersonation + credential harvesting is a valid vulnerability class |
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

- 5 lead(s) marked VALID at 2026-08-10 20:29:39 UTC
  - | Q5 Novel? | NO — already reported as VALID in triage-report-2026-08-08 (Lead 1) and 2026-08-10 (Leads 1+13) |
  - | Q6 Not rejected? | YES — supply-chain impersonation is a valid vulnerability class |
  - **Verdict: VALID (DUPLICATE)** — This is the same npm impersonation + API key harvesting finding already confirmed as VALID in two prior triage runs. Not novel.
  - | G | `registry.npmjs.org/gladia` → 200 | **VALID (DUPLICATE)** | Already reported as VALID in prior triage |
  - The only VALID finding remains the **npm `gladia`@0.1.3 impersonation + API key harvesting** (Lead G), which has already been reported with full passive proof. No new probe data changes any prior verd

- 4 lead(s) marked VALID at 2026-08-10 23:58:34 UTC
  - | Q5 Novel? | **NO — already reported as VALID in triage-report-2026-08-10 (Leads 1+13) and 8+ prior triage cycles** |
  - | Q6 Not rejected? | YES — valid vulnerability class |
  - **Verdict: VALID (DUPLICATE)** — Same npm `gladia`@0.1.3 impersonation + API key harvesting finding already confirmed as VALID. The probe data (npm registry 200, repo 404) is consistent evidence but d
  - | H | `registry.npmjs.org/gladia` (200) | **VALID (DUPLICATE)** | Already reported; not novel |

- 18 lead(s) marked VALID at 2026-08-11 04:12:29 UTC
  - | 1 | npm `gladia`@0.1.3 impersonation / supply-chain squat with API key exfil via WS URL | npm registry (MEDIUM) | **VALID** | Verified fact; passive proof complete; repo 404 (irrevocable); dist-tag 
  - | 2 | SSRF via audio_url/video_url/callback_url server-side fetch | api.gladia.io (HIGHEST) | **HOLD** | In-scope, real impact, design confirmed — but proof requires AUTH_HELPED (valid API key + POST)
  - | 3 | IDOR on `/{id}/file` download endpoints | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID guessing infeasible without owned IDs |
  - | 4 | WebSocket auth token in URL query parameter | api.gladia.io (HIGHEST) | **HOLD** | Design confirmed via public spec; proving actual leakage requires valid key |
  - | 5 | Query-param injection on `/v1/history` (custom_metadata, arrays) | api.gladia.io (HIGHEST) | **HOLD** | Spec confirms object/array params; needs valid key to test injection — AUTH_HELPED |
  - | Q5 Novel? | YES — not previously reported to Gladia (per valid-bugs.md, this is the only confirmed finding) |
  - | Q6 Not rejected? | YES — supply-chain impersonation + credential harvesting is a valid vulnerability class |
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

- 12 lead(s) marked VALID at 2026-08-11 05:35:29 UTC
  - **Verdict: VALID**
  - | **Q4** | **NO** — requires valid `x-gladia-key` to POST; cannot prove reachability of 169.254.169.254 or internal hosts without a key |
  - | **Q7** | **NO** — without a valid key, no triager can accept an unproven SSRF hypothesis |
  - **Verdict: HOLD** — AUTH_HELPED; cannot verify without valid API key. Request program-provided trial key or authorized testing window.
  - | **Q4** | **NO** — cannot observe token format/lifetime without valid API key |
  - **Verdict: HOLD** — AUTH_HELPED; architectural concern but cannot prove exploitation without valid key.
  - | **Q4** | **NO** — requires valid key + cross-user testing |
  - **Verdict: HOLD** — AUTH_HELPED; cannot verify without valid API key.
  - | 1 | npm `gladia@0.1.3` impersonation | **VALID** | Orphaned package, false "Official" claim, key-leak code path |
  - | 2 | SSRF via audio_url/video_url/callback_url | **HOLD** | AUTH_HELPED — needs valid API key |
  - | 6 | WebSocket token in URL | **HOLD** | AUTH_HELPED — needs valid key to prove leakage |
  - | 8 | IDOR on /{id}/file | **HOLD** | AUTH_HELPED — needs valid key |

- 1 lead(s) marked VALID at 2026-08-11 10:50:11 UTC
  - | G | `registry.npmjs.org/gladia` → 200 | **VALID (DUPLICATE)** | npm impersonation, already reported 9× |

- 1 lead(s) marked VALID at 2026-08-11 12:35:28 UTC
  - | G | `registry.npmjs.org/gladia` → 200 | **VALID (DUPLICATE)** | Supply-chain impersonation — already reported 9+ times since 2026-08-07 |

- 10 lead(s) marked VALID at 2026-08-11 14:16:08 UTC
  - | Q6 | **YES** | Supply-chain impersonation + credential-leak code is a valid class, not best-practice/self-XSS/info-disclosure-of-public-data. |
  - ### Verdict: **VALID (DUPLICATE)**
  - | Q6 | **YES** | SSRF is a valid class. |
  - ### Verdict: **HOLD** — Real SSRF surface confirmed by public OpenAPI spec (`format:uri`, no scheme allowlist), but requires AUTH_HELPED testing (valid API key + POST with internal URL) to prove. Per 
  - | Q6 | **YES** | Open redirect is valid class. |
  - | Q4 | **NO** | Requires valid key + cross-account {id} testing. AUTH_HELPED. Spec does not indicate per-resource ownership validation, but this is speculation. |
  - | Q6 | **YES** | IDOR is valid class. |
  - ### Verdict: **HOLD** — Plausible surface, requires AUTH_HELPED testing (valid key + known other-user {id}).
  - | Q6 | **YES** | Token-in-URL is a valid design-level security concern. |
  - | 1 | npm `gladia@0.1.3` impersonation + credential-leak | npm registry (SDK ecosystem) | **VALID (DUPLICATE)** | Supply-chain squat, orphaned repo, API key in WS URL. Already reported 9+ times. |

- 7 lead(s) marked VALID at 2026-08-11 18:45:05 UTC
  - **Verdict: HOLD — out of program scope.** Real supply-chain risk exists, but the asset (npm `gladia`) is not in scope. Should be reported to npm/GitHub directly, not Gladia's program. If operator expa
  - | **Q2 Reachable?** | Partially — OpenAPI spec is public (14 paths documented), but all data endpoints return 401 NestJS HttpException without valid `x-gladia-key`. |
  - **Verdict: HOLD — AUTH_HELPED.** Real SSRF surface exists per spec, but cannot be confirmed passively. Requires valid `x-gladia-key`. If operator provides a trial key or approves active testing, recla
  - | **Q4 Proof without invasive?** | **No** — confirming the actual redirect requires a valid authenticated session. Unauthenticated reflection alone is not exploitable (user isn't logged in). |
  - | **Q2 Reachable?** | Partially — endpoints are key-gated (401 without valid `x-gladia-key`). |
  - | **Q4 Proof without invasive?** | **No** — requires valid key to test cross-account isolation. |
  - **Verdict: HOLD — AUTH_HELPED.** Untestable without valid API key. Same gating issue as Lead 2.

- 17 lead(s) marked VALID at 2026-08-11 19:53:30 UTC
  - | 1 | npm `gladia`@0.1.3 impersonation + API key harvesting via WS URL query param | npm registry (MEDIUM) | **VALID (DUPLICATE)** | Already reported 9+ times since 2026-08-07; repo 404 (irrevocable);
  - | 2 | SSRF via audio_url/video_url/callback_url server-side fetch | api.gladia.io (HIGHEST) | **HOLD** | In-scope, real impact, design confirmed — but proof requires AUTH_HELPED (valid API key + POST 
  - | 3 | IDOR on `/{id}/file` download endpoints | api.gladia.io (HIGHEST) | **HOLD** | Needs valid key + cross-account test; UUID-based IDs make guessing infeasible without owned IDs |
  - | 5 | WebSocket auth token in URL query parameter | api.gladia.io (HIGHEST) | **HOLD** | Token-in-URL design confirmed via public OpenAPI spec; proving actual leakage (Referer, log, history) requires 
  - | 11 | Query-param injection on `/v1/history` (custom_metadata object, arrays) | api.gladia.io (HIGHEST) | **HOLD** | Spec confirms OBJECT-typed `additionalProperties:true` + array params; needs valid
  - | Q5 Novel? | NO — already confirmed VALID in 9+ prior triage runs (first validated 2026-08-07 21:04); reported multiple times |
  - | Q6 Not rejected? | YES — supply-chain impersonation + credential harvesting is a valid vulnerability class |
  - | Q4 Passive proof? | NO — OpenAPI spec confirms design (`format:uri`, no scheme allowlist). Proving actual server-side fetch requires POST with valid API key + canary/internal URL. Passive GET only s
  - | Q6 Not rejected? | YES — SSRF is a valid vulnerability class |
  - | Q7 Triager accept? | CONDITIONAL — only if reachability demonstrated with valid key |
  - | Q2 Reachable? | NO for cross-account — requires valid API key + known resource ID owned by another user; UUID-based IDs make guessing infeasible |
  - | Q6 Not rejected? | YES — IDOR is valid class |
  - | Q2 Reachable? | PARTIAL — token-in-URL design visible in public OpenAPI spec; actual token generation requires valid API key |
  - | Q4 Passive proof? | PARTIAL — design confirmed via public spec (`wss://api.gladia.io/v2/live?token=<uuid>`); proving actual leakage requires valid key |
  - | Q6 Not rejected? | YES — credential leakage via URL is a valid class |
  - | Q6 Not rejected? | YES — open redirect is a valid vulnerability class |
  - | VALID | 0 (1 duplicate of previously-reported finding) |

- 26 lead(s) marked VALID at 2026-08-11 23:31:23 UTC
  - | Q5 | **NO** | Already confirmed VALID in 9+ prior triage runs (first 2026-08-07 21:04). |
  - | Q6 | **YES** | Supply-chain impersonation + credential-leak code is a valid class, not info-disclosure/best-practice/self-XSS. |
  - ### Verdict: **VALID (DUPLICATE)** — Already reported 9+ times since 2026-08-07.
  - | Q2 | **PARTIAL** | All v2 endpoints are key-gated (401 without `x-gladia-key`). Reachable only by users with a valid API key (low-priv self-service). |
  - | Q4 | **NO** | Proving actual server-side fetch requires `POST` with valid key + canary/internal URL + observing error/timing. OpenAPI spec confirms *design* (`format:uri`, no scheme allowlist) but d
  - | Q6 | **YES** | SSRF is a valid class. |
  - | Q7 | **CONDITIONAL** | Triager accepts only IF reachability demonstrated with valid key. Without proof → HOLD. |
  - ### Verdict: **HOLD** — AUTH_HELPED. In-scope, real impact, design confirmed. Cannot prove with passive GET/HEAD only. Needs valid API key + non-destructive canary fetch.
  - | Q2 | **NO** | Key-gated (401 without key). Cross-account testing requires two valid keys. UUID-based IDs make unauthenticated guessing infeasible. |
  - | Q4 | **NO** | Requires valid key + owned resource ID + cross-account test. Spec does not expose ownership-binding logic. |
  - | Q6 | **YES** | IDOR is a valid class. |
  - ### Verdict: **HOLD** — AUTH_HELPED. Needs valid key + cross-account test. Spec is opaque on ownership binding.
  - | Q2 | **PARTIAL** | Token-in-URL design visible in public OpenAPI spec. Actual token generation requires valid `x-gladia-key`. |
  - | Q4 | **PARTIAL** | Design confirmed via public spec (no auth needed). Proving actual token theft/leakage requires valid key to init session and inspect Referer. |
  - | Q6 | **YES** | Credential leakage via URL is a valid class (not just "best practice"). |
  - ### Verdict: **HOLD** — Design confirmed via public spec. Architectural weakness with real implications, but proving actual token theft requires valid key. Lower priority than SSRF.
  - | Q4 | **NO** | Requires valid key to test injection strings (`custom_metadata[__proto__][x]=1`, etc.). |
  - | Q6 | **YES** | Injection is a valid class. |
  - | Q7 | **NO** | Spec-only; no evidence of actual injection without valid key. |
  - ### Verdict: **HOLD** — AUTH_HELPED. Spec confirms complex query parsing surface; needs valid key to test injection.

- 9 lead(s) marked VALID at 2026-08-12 00:47:54 UTC
  - | Q2 Reachability | ⚠️ Key-gated — all /v2 endpoints return 401 without valid `x-gladia-key`. Attacker needs a legitimate (paid/trial) API key to reach the fetch logic. |
  - | Q5 Novelty | Valid class for this asset type |
  - | Q7 Acceptable? | ❌ NO — AUTH_HELPED only; cannot be validated passively. Requires valid key + active POST. `passive_first: true` in scope.yml prohibits invasive testing without program approval. |
  - **Verdict: HOLD — plausible SSRF surface per OpenAPI spec, but untestable without a valid API key and POST submission. Does not pass Q4 (read-only proof). Defer to an authorized key-gated test with pr
  - | Q2 Reachability | ⚠️ Token only issued to authenticated users (valid `x-gladia-key` required to call `/v2/live/init`) |
  - | Q4 Proof (read-only) | ❌ NO — the OpenAPI spec *describes* the token-in-URL pattern, but actually observing a live token requires `POST /v2/live/init` with a valid key (write action). No passive GET
  - | Q2 Reachability | ⚠️ Key-gated — `/v2/transcription/{id}/file` returns 401 without valid key |
  - | Q4 Proof (read-only) | ❌ NO — requires: (1) a valid API key, (2) creating a transcription as User A, (3) attempting to download as User B. All involve state changes / authenticated actions. |
  - | Q5 Novelty | Valid class |

- 6 lead(s) marked VALID at 2026-08-21 22:48:03 UTC
  - | Q4 Provable read-only? | **No** — requires valid x-gladia-key (POST request with body); spec-only proof is insufficient |
  - **Verdict: HOLD** — Spec-level analysis is strong but invasive testing (POST with key) required for proof. No valid key available.
  - **Verdict: VALID**
  - | Q2 Reachable? | **No** — requires valid API key to initiate WS session and obtain token |
  - | Q2 Reachable? | Requires valid key + valid ID |
  - | 2 | npm `gladia@0.1.3` impersonation | **VALID** | 6.8 | **Report ready** — submit via gladia.io/bug-bounty-report |

- 3 lead(s) marked VALID at 2026-08-22 02:08:46 UTC
  - | Q2 Reachable? | **NO** — POST /v2/pre-recorded returns 401 without a valid `x-gladia-key`. Cannot reach the SSRF surface without auth. |
  - | Q4 Provable read-only? | **NO** — requires POST with valid API key (AUTH_HELPED) |
  - | Q2 Reachable? | **NO** — requires valid API key (401 without) |

- 4 lead(s) marked VALID at 2026-09-01 01:53:19 UTC
  - | **A. npm `gladia@0.1.3` impersonation + key-in-WS-URL** `inventory/gladia.md:32` `reports/SUBMISSION_gladia_npm_impersonation.md:1` `probe-results.md:294` `registry.npmjs.org/gladia ->200` + `api.gi
  - | **B. api.gladia.io SSRF via `audio_url/video_url/CallbackConfigDto.url` `format:uri` no scheme allowlist** `inventory/gladia.md:98` `probe-results.md:4` `api.gladia.io/v2/pre-recorded ->401` | ✅ YES
  - | **C. IDOR/BOLA `/{id}/file` download** `inventory/gladia.md:96` | ✅ YES HIGHEST | ❌ NO 401 unauth, needs valid key + victim UUID (un-guessable) | ✅ YES cross-tenant PII | ❌ NO needs 2 keys + owned I
  - | **F. `x-gladia-key` / `token` in `wss://api.gladia.io/v2/live?token=<uuid>` URL** `inventory/gladia.md:41` | ✅ YES HIGHEST | ❌ PARTIAL needs valid key to `POST /v2/live` to obtain token | ⚠️ LOW des

- 2 lead(s) marked VALID at 2026-09-01 12:38:56 UTC
  - **Verdict: VALID (npm registry) / HOLD (Gladia program - Q1/Q3 fail until WS query-param accepted server-side proven) -** One-line: orphaned impersonation locked 10+ reproductions, key-in-URL primitiv
  - **Verdict: HOLD (AUTH_HELPED - needs valid `x-gladia-key`) -** spec confirms `audio_url` forwarded verbatim (SDK `create/createUntyped` no allowlist), but auth gate blocks unauth proof.

- 1 lead(s) marked VALID at 2026-09-01 17:00:09 UTC
  - - **Verdict: VALID (DUPLICATE)** — One-line: locked orphaned impersonation + key-in-URL primitive across 10+ repros.

- 1 lead(s) marked VALID at 2026-09-01 19:59:36 UTC
  - - **VERDICT: HOLD — VALID for npm registry, HOLD for Gladia infra pending query-param proof** (`leads/lead-human.md:15`).

- 2 lead(s) marked VALID at 2026-09-01 22:39:57 UTC
  - - **Verdict: VALID (DUPLICATE) / HOLD for Gladia venue** - npm venue ACTIONABLE now; Gladia venue HOLD `lead-human.md:15` Q3 FAIL until `wss://api.gladia.io/v2/live?x-gladia-key=<KEY>` proven server a
  - - **Verdict: HOLD (AUTH_HELPED)** - design confirmed passive, proof needs program trial key. `reports/valid-bugs.md:17` PARKED 100+ cycles.

- 2 lead(s) marked VALID at 2026-09-02 00:36:02 UTC
  - **Verdict: HOLD (Gladia program) / VALID (npm registry venue)** One-line: impersonation+key-in-URL verified passive, but Gladia impact requires 1 valid key WSS proof; already reported awaiting vendor.
  - **Verdict: HOLD (AUTH_HELPED) downgraded** One-line: SSRF surface exists in spec but key-gated 401 with no bypass, needs valid key POC.

- 2 lead(s) marked VALID at 2026-09-02 05:10:14 UTC
  - - **Verdict: VALID (DUPLICATE) for npm Trust&Safety / HOLD for Gladia program** `leads/lead-human.md:15`. One-line: locked impersonation passive-proven, GladiaInfra key-in-URL primitive unproven witho
  - - **Verdict: HOLD (HUMAN_ONLY)** — needs `HUMAN: Google SSO login → GET /signin?redirect_to=https://evil.example.com` with follow-redirects=false capture `Location` header; expected 302→`/dashboard` o

- 8 lead(s) marked VALID at 2026-09-02 09:44:48 UTC
  - |Q5 Novel| **DUPLICATE** — `reports/valid-bugs.md:22` `reports/SUBMISSION_gladia_npm_impersonation.md:1` validated 2026-08-07, re-verified 10+ `npm pack` `3b23ec7d…7f2`/`cc96f84a…` `triage/run-2026-08
  - **Verdict: VALID (DUPLICATE) — one-line: orphaned impersonation at dist-tag latest + key-in-URL primitive locked passive.**
  - |Q4| **NO** — proving redirect requires authenticated `GET /signin?redirect_to=...` with valid Google session + observing `Location` (HUMAN_ONLY). `probe-results.md:5` shows `200` not `302`; `return-t
  - |Q6| YES — open redirect is valid class |
  - |Q2| **PARTIAL** — key-gated `401` `probe-results.md:4`; reachable only with valid `x-gladia-key` (low-priv trial key per `scope.yml:41 passive_first`). No unauth bypass in 100+ cycles |
  - |Q4| **NO** — requires `POST /v2/pre-recorded -H x-gladia-key:<valid> -d {"audio_url":"http://canary"}` + error/timing oracle. `OpenAPI 125131B/14 paths` only proves design, not fetch. Violates `no_da
  - |Q5| YES — hypothesis tracked `reports/valid-bugs.md:17` but unproven |
  - **Verdict: HOLD — one-line: design confirmed (`format:uri` no scheme allowlist, 7 webhooks), proof gated on valid x-gladia-key.**

- 7 lead(s) marked VALID at 2026-09-02 13:55:00 UTC
  - | Q4 GET/HEAD proof? | **YES for impersonation/orphan:** `curl -s https://registry.npmjs.org/gladia | jq .dist-tags,.maintainers`; `npm pack gladia@0.1.3; sha256=3b23ec7d7a763abc04c52db232d157a982fd3b
  - | Q5 Novel? | **NO — DUPLICATE** Already reported `2026-08-12 riteshekbote@gmail.com → security@gladia.io` `leads/lead-human.md:3`, confirmed `reports/valid-bugs.md` 9+ prior `VALID`. Re-verified fres
  - **Verdict: HOLD (VALID DUPLICATE for npm venue, HOLD for Gladia program)** — one-line: locked orphaned impersonation + key-in-URL primitive across 10+ `npm pack` repros, already reported 2026-08-12 aw
  - | Q6 | YES — open redirect is valid class. |
  - | Q2 | **NO — PARTIAL key-gated:** `GET /v2/pre-recorded →401` + `POST /v2/pre-recorded no key →401 NestJS` `inventory/gladia.md:318` ×100 cycles, no bypass found. Requires valid `x-gladia-key` (low-p
  - | Q4 | **NO** — requires `POST /v2/pre-recorded -H x-gladia-key:<valid> -d {"audio_url":"http://canary"}` vs `http://169.254.169.254/` comparing `error_message/status/duration` `leads/lead-bigpickle.m
  - | Q6 | YES — SSRF valid class. |

- 4 lead(s) marked VALID at 2026-09-02 17:58:16 UTC
  - | Q6 Not rejected? | YES — open redirect valid class, not `info disclosure/best practice` |
  - | Q5 | NO — **DUPLICATE**. `REPORTED 2026-08-12` `leads/lead-human.md:3` awaiting vendor, 9+ prior `VALID` triages `triage/triage-report-2026-08-11.md:12`. Novelty fails for re-report to same channel.
  - **Verdict: VALID (DUPLICATE) — HOLD for Gladia venue, ACTIONABLE for npm venue** — One-line: already reported impersonation+key-leak, re-report would be duplicate.
  - | E | `GET registry.npmjs.org/gladia` | 200 | **VALID (DUPLICATE)** | Impersonation+key-leak already reported 2026-08-12, duplicate if re-filed to Gladia |
