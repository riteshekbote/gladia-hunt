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
