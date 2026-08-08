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
