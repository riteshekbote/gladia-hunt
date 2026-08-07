# LEADS laguna (seed)
- 2026-08-07 SEED: no model output yet; pipeline starts on first run.
## 2026-08-07 18:29:33 UTC [app] (model laguna)
[PRIO] api.gladia.io (CORS+wildcard + openapi.json), score 8.2 | attack:9, business:8, tech:7 (CORS misconfig), gate:9 (no auth on 404), cloud:8 (HSTS), freshness:10
[PRIO] api.gladia.io/openapi.json (full spec exposure), score 7.4 | attack:8, business:8, tech:7 (spec exposure), gate:10, cloud:6, freshness:8
[PRIO] app.gladia.io (return-to cookie JWT-shaped), score 6.8 | attack:7, business:6, tech:7 (JWT-ish cookie), gate:8, cloud:5, freshness:6
[PRIO] npm `gladia` 0.1.3 vs @gladiaio/sdk ownership conflict, score 5.1 | attack:6, business:5, tech:5, gate:9, cloud:4, freshness:7
[HYP] CORS wildcard reflects origin
class: MISCONFIG
asset: api.gladia.io
confidence: 75
reasoning: Known CORS `access-control-allow-origin: *` already confirmed; need to verify if it reflects a credentialed origin or sets Access-Control-Allow-Credentials. Seed explicitly asks "verify actual behavior."
evidence_needed: Origin header reflected in ACAO, or Access-Control-Allow-Credentials: true with credentials
verify_steps: passive PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json`
impact: Attacker can read API spec + 404 details cross-origin; possible credentialed exfiltration if credentials allowed
testability: PASSIVE
[HYP] OpenAPI spec contains undocumented or shadow endpoints
class: MISCONFIG
asset: api.gladia.io/openapi.json
confidence: 55
reasoning: Spec is consumed by official SDK generator; seed says "check for undocumented/shadow endpoints." Spec lists 14 paths but may contain internal, deprecated, or test routes not documented externally.
evidence_needed: Path in spec that returns 200 with valid (or different) behavior vs. documented expectation, or path absent from public docs
verify_steps: passive PROBE: compare every path in spec against public docs; request a few obscure paths (e.g., /v1/history) to confirm reachability
impact: Unknown API surface, potential unauthenticated access to sensitive operations
testability: PASSIVE
[HYP] return-to cookie has weak/no signature validation
class: AUTH
asset: app.gladia.io/signin (redirect flow)
confidence: 45
reasoning: Cookie `return-to=eyJ1urwiOiIvIn0%3D` decodes to `{"url":"/"}` with no dot-separated signature segment (no alg). Seed asks to "check signature/alg handling."
evidence_needed: Server accepts crafted return-to value and redirects to attacker-controlled or unintended target
verify_steps: AUTH_HELPED: requires interactive signin flow test; not feasible passively without credential
impact: Open redirect / auth bypass in SSO flow
testability: AUTH_HELPED
[FINAL]
[NEXT] PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json` — check if `access-control-allow-origin` reflects `https://evil.test` and if `access-control-allow-credentials: true` is present.
[RISK] api.gladia.io: 72 reason: CORS wildcard exposure + full OpenAPI spec + x-api-key auth only | app.gladia.io: 55 reason: JWT-shaped unsigned cookie in redirect flow | sdk: 45 reason: npm ownership discrepancy (gladia vs @gladiaio/sdk)
## 2026-08-07 18:51:46 UTC [app] (model laguna)
[HYP] CORS wildcard enables cross-origin read of API data/spec (no credential support)
class: MISCONFIG
asset: api.gladia.io (all responses, incl. /openapi.json and /v1/models)
confidence: 65
reasoning: Passive OPTIONS/GET probes confirm static `access-control-allow-origin: *` with NO `access-control-allow-credentials`. Any origin can read the public OpenAPI spec, 404 bodies, exposed trace headers, and the unauthenticated /v1/models response cross-origin. Credentialled exfiltration is NOT enabled, but cross-origin readability broadens attacker reach.
evidence_needed: `access-control-allow-origin: *` in response headers; absence of `access-control-allow-credentials`
verify_steps: passive PROBE (already observed): `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json`; `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models`
impact: Low-severity info disclosure — malicious site reads full API surface + model list + trace headers cross-origin; no credential theft since creds disallowed
testability: PASSIVE
[HYP] return-to cookie is unsigned base64url JSON enabling post-auth redirect manipulation
class: AUTH
asset: app.gladia.io /signin (return-to cookie + redirect_to form action)
confidence: 60
reasoning: Passive probe confirms root `/` sets `return-to=eyJ1cmwiOiIvIn0%3D` which decodes to plain JSON `{"url":"/"}` with 0 dots (no JWT signature). `/signin` reflects `redirect_to=https%3A%2F%2Fevil.example.com` into the OAuth form `action`. A crafted return-to/redirect_to could steer the Google OAuth post-auth redirect to an attacker-controlled host.
evidence_needed: Server honors attacker-supplied return-to/redirect_to and redirects post-authentication (HTTP 302 Location) to an external host
verify_steps: AUTH_HELPED: complete Google OAuth signin with `?redirect_to=https://evil.example.com` and observe the post-auth HTTP 302 Location; passive pre-check: `curl -sS "https://app.gladia.io/signin?redirect_to=https%3A%2F%2Fevil.example.com" | grep -o 'action="[^"]*"'` (already reflects)
impact: Open redirect / post-auth redirect to attacker site for credential capture or phishing; severity medium
testability: AUTH_HELPED
[HYP] npm `gladia` package impersonates official SDK from personal repo
class: OATH
asset: npm `gladia@0.1.3` (github.com/alexisbouchez/gladia.ts)
confidence: 55
reasoning: Passive `npm view` confirms `description` = "Official TypeScript SDK for Gladia" yet `repository.url` points to the personal account alexisbouchez/gladia.ts (not the official gladiaio org). Maintainer is `softwarecitadel <softwarecitadel@gmail.com>`. This is an ownership/typosquat anomaly that can mislead users into importing an unofficial package.
evidence_needed: npm registry metadata (description, repository.url, maintainer) mismatched against the official @gladiaio/sdk
verify_steps: passive PROBE: `npm view gladia@0.1.3 description repository.url maintainer homepage` (already run)
impact: Supply-chain confusion — developers install an unofficial/misattributed SDK thinking it is official; severity medium-high
testability: PASSIVE
[FINAL] (reranked, top first)
[NEXT] PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-origin: *` (escalation check: can an attacker origin read the unauthenticated models payload, not just the preflight).
