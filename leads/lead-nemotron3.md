# LEADS nemotron3 (seed)
- 2026-08-07 SEED: no model output yet; pipeline starts on first run.
## 2026-08-07 18:30:17 UTC [app] (model nemotron3)
[PRIO] api.gladia.io, 8.9, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=9
[PRIO] app.gladia.io, 6.8, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=8
[PRIO] @gladiaio/sdk (npm), 5.2, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] gladiaio-sdk (PyPI), 4.8, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[HYP] OpenAPI shadow endpoints / undocumented v2 paths
class: MISCONFIG
asset: api.gladia.io
confidence: 70
reasoning: OpenAPI spec at /openapi.json is 125KB and drives official SDK generator; spec may omit internal/admin/debug paths; CORS wildcard with exposed correlation IDs suggests debug-friendly surface
evidence_needed: Diff between spec paths and actual 200/401/403 responses on common suffixes (/admin, /debug, /health, /metrics, /v1/, /internal/)
verify_steps: PROBE: HEAD https://api.gladia.io/v2/transcription (expect 401/403), HEAD https://api.gladia.io/v1/ (expect 404), HEAD https://api.gladia.io/health, HEAD https://api.gladia.io/metrics, HEAD https://api.gladia.io/debug
impact: Undocumented endpoints could leak internal state, admin controls, or bypass auth; severity Medium-High
testability: PASSIVE
[HYP] WebSocket token in URL leakage via referer/logs
class: AUTH
asset: api.gladia.io
confidence: 65
reasoning: OpenAPI shows InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>; tokens in URLs leak via browser history, referer headers, server logs, proxy logs
evidence_needed: Confirm token is bearer-equivalent and long-lived; check if token rotates or is single-use; verify Referrer-Policy on WS upgrade
verify_steps: PROBE: POST https://api.gladia.io/v2/live/init (expect 401 without auth) to observe response shape; check Response headers for Referrer-Policy; inspect any Set-Cookie on WS handshake
impact: Token theft enables unauthorized live transcription sessions, audio data access; severity High
testability: AUTH_HELPED (needs valid API key to init session)
[HYP] return-to cookie JWT parsing without signature verification
class: AUTH
asset: app.gladia.io
confidence: 55
reasoning: Cookie return-to=eyJ1cmwiOiIvIn0%3D decodes to {"url":"/"}; JWT-shaped but no signature segment visible; if app trusts this blindly for redirect, open redirect or auth bypass possible
evidence_needed: Check if cookie value is ever signed/verified; test redirect with tampered payload (e.g., {"url":"https://evil.com"}) and observe Location header
verify_steps: PROBE: GET https://app.gladia.io/ with Cookie: return-to=eyJ1cmwiOiJodHRwczovL2V2aWwuY29tIn0%3D (base64url of {"url":"https://evil.com"}); observe 302 Location
impact: Open redirect to arbitrary domain; phishing, token theft via OAuth flow manipulation; severity Medium
testability: PASSIVE
[FINAL] 1) WebSocket token in URL leakage via referer/logs (api.gladia.io, 65, AUTH) 2) OpenAPI shadow endpoints / undocumented v2 paths (api.gladia.io, 70, MISCONFIG) 3) return-to cookie JWT parsing without signature verification (app.gladia.io, 55, AUTH)
[NEXT] PROBE: POST https://api.gladia.io/v2/live/init -H "Content-Type: application/json" -d '{}' (observe auth requirement, response shape, token format)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI spec publicly exposed at /openapi.json with full v2 surface
[LEARN] ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per spec
[LEARN] ACCEPTED AUTH @ app.gladia.io: return-to cookie uses JWT-shaped base64url value without visible signature
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; no auth on spec endpoint; high business value (core transcription API)
[RISK] app.gladia.io: 60 reason: Dashboard behind auth but return-to cookie handling unverified; noindex/nofollow limits exposure; HSTS preload strong; lower direct API surface
[RISK] sdk: 45 reason: Official SDKs generated from public spec; npm/PyPI packages legitimate; third-party `gladia` pkg on personal repo is ownership anomaly but not Gladia code
## 2026-08-07 18:50:39 UTC [app] (model nemotron3)
[NEW] api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
[NEW] api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
[NEW] api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
[NEW] api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
[NEW] api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
[NEW] app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
[NEW] app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
[NEW] app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
[NEW] npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
[CHANGED] app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)
[PRIO] api.gladia.io, 8.9, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=9
[PRIO] app.gladia.io, 6.8, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=8
[PRIO] npm @gladiaio/sdk, 5.2, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] PyPI gladiaio-sdk, 4.8, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] npm gladia (typosquat candidate), 4.5, attack_surface=4 business_value=5 tech_exposure=4 gate_ease=9 cloud_surface=2 freshness=5
[HYP] Undocumented /health endpoint on api.gladia.io leaks runtime status
class: MISCONFIG
asset: api.gladia.io
confidence: 80
reasoning: /health returns 200 {"health":"OK"} but is absent from OpenAPI spec (14 documented paths); health endpoints often expose version, build info, dependency status in other environments
evidence_needed: Compare /health response across environments; check if verbose mode exists via query params (e.g., ?full=true, ?format=json)
verify_steps: PROBE: GET https://api.gladia.io/health (already 200); GET https://api.gladia.io/health?full=true; GET https://api.gladia.io/health?format=json; HEAD https://api.gladia.io/actuator/health (Spring Boot pattern)
impact: Information disclosure — aids reconnaissance, may reveal version/internal state; severity Low-Medium
testability: PASSIVE
[HYP] WebSocket auth token in URL query parameter leaks via Referer/logs
class: AUTH
asset: api.gladia.io
confidence: 75
reasoning: OpenAPI spec shows InitStreamingResponse.url = "wss://api.gladia.io/v2/live?token=<uuid>"; tokens in URLs leak via browser history, Referer headers on WS upgrade, server/proxy logs; token is bearer-equivalent for live session
evidence_needed: Confirm token is long-lived/session-scoped; check Referrer-Policy on WS handshake response; verify token rotation/invalidation on disconnect
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/live -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{}' → observe response.url token format; initiate WS connection and inspect upgrade request headers for Referer; check if token works after session close
impact: Token theft enables unauthorized live transcription sessions, access to real-time audio stream; severity High
testability: AUTH_HELPED
[HYP] npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 70
reasoning: Package description claims "Official TypeScript SDK for Gladia" but repository=github.com/alexisbouchez/gladia.ts (personal account), maintainer=softwarecitadel@gmail.com; official SDK is @gladiaio/sdk from gladiaio/sdk monorepo; users may install wrong package
evidence_needed: Verify if alexisbouchez/softwarecitadel is affiliated with Gladia; check package code for malicious behavior; compare API surface with official SDK
verify_steps: RAG: Read github.com/alexisbouchez/gladia.ts source; diff against @gladiaio/sdk; check install scripts, network calls, data exfiltration; HUMAN: Contact Gladia security to confirm ownership
impact: Supply chain risk — developers may install impersonated SDK leading to credential theft or malicious code execution; severity Medium-High
testability: RAG
[PARKED] return-to cookie JWT parsing without signature verification: Server rejects tampered cookie and resets to default; no open redirect observed; confidence < 40 after validation
[FINAL] 1) WebSocket auth token in URL query parameter leaks via Referer/logs (api.gladia.io, 75, AUTH) 2) Undocumented /health endpoint on api.gladia.io leaks runtime status (api.gladia.io, 80, MISCONFIG) 3) npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace (npm registry, 70, OTHER)
[NEXT] PROBE: GET https://api.gladia.io/health?full=true — check for verbose health output
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
[LEARN] ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
[LEARN] REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
[LEARN] ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; undocumented /health endpoint; no auth on spec endpoint; high business value (core transcription API)
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but no open redirect; HSTS preload strong; Google-only OAuth limits attack surface
[RISK] sdk: 40 reason: Official SDKs (@gladiaio/sdk, gladiaio-sdk) generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
[NEW] api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
[NEW] api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
[NEW] api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
[NEW] api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
[NEW] api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
[NEW] app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
[NEW] app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
[NEW] app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
[NEW] npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
[CHANGED] app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)
[PRIO] api.gladia.io, 8.9, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=9
[PRIO] app.gladia.io, 6.8, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=8
[PRIO] npm @gladiaio/sdk, 5.2, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] PyPI gladiaio-sdk, 4.8, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] npm gladia (typosquat candidate), 4.5, attack_surface=4 business_value=5 tech_exposure=4 gate_ease=9 cloud_surface=2 freshness=5
[HYP] Undocumented /health endpoint on api.gladia.io leaks runtime status
class: MISCONFIG
asset: api.gladia.io
confidence: 80
reasoning: /health returns 200 {"health":"OK"} but is absent from OpenAPI spec (14 documented paths); health endpoints often expose version, build info, dependency status in other environments
evidence_needed: Compare /health response across environments; check if verbose mode exists via query params (e.g., ?full=true, ?format=json)
verify_steps: PROBE: GET https://api.gladia.io/health (already 200); GET https://api.gladia.io/health?full=true; GET https://api.gladia.io/health?format=json; HEAD https://api.gladia.io/actuator/health (Spring Boot pattern)
impact: Information disclosure — aids reconnaissance, may reveal version/internal state; severity Low-Medium
testability: PASSIVE
[HYP] WebSocket auth token in URL query parameter leaks via Referer/logs
class: AUTH
asset: api.gladia.io
confidence: 75
reasoning: OpenAPI spec shows InitStreamingResponse.url = "wss://api.gladia.io/v2/live?token=<uuid>"; tokens in URLs leak via browser history, Referer headers on WS upgrade, server/proxy logs; token is bearer-equivalent for live session
evidence_needed: Confirm token is long-lived/session-scoped; check Referrer-Policy on WS handshake response; verify token rotation/invalidation on disconnect
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/live -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{}' → observe response.url token format; initiate WS connection and inspect upgrade request headers for Referer; check if token works after session close
impact: Token theft enables unauthorized live transcription sessions, access to real-time audio stream; severity High
testability: AUTH_HELPED
[HYP] npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 70
reasoning: Package description claims "Official TypeScript SDK for Gladia" but repository=github.com/alexisbouchez/gladia.ts (personal account), maintainer=softwarecitadel@gmail.com; official SDK is @gladiaio/sdk from gladiaio/sdk monorepo; users may install wrong package
evidence_needed: Verify if alexisbouchez/softwarecitadel is affiliated with Gladia; check package code for malicious behavior; compare API surface with official SDK
verify_steps: RAG: Read github.com/alexisbouchez/gladia.ts source; diff against @gladiaio/sdk; check install scripts, network calls, data exfiltration; HUMAN: Contact Gladia security to confirm ownership
impact: Supply chain risk — developers may install impersonated SDK leading to credential theft or malicious code execution; severity Medium-High
testability: RAG
[PARKED] return-to cookie JWT parsing without signature verification: Server rejects tampered cookie and resets to default; no open redirect observed; confidence < 40 after validation
[FINAL] 1) WebSocket auth token in URL query parameter leaks via Referer/logs (api.gladia.io, 75, AUTH) 2) Undocumented /health endpoint on api.gladia.io leaks runtime status (api.gladia.io, 80, MISCONFIG) 3) npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace (npm registry, 70, OTHER)
[NEXT] PROBE: GET https://api.gladia.io/health?full=true — check for verbose health output
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
[LEARN] ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
[LEARN] REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
[LEARN] ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; undocumented /health endpoint; no auth on spec endpoint; high business value (core transcription API)
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but no open redirect; HSTS preload strong; Google-only OAuth limits attack surface
[RISK] sdk: 40 reason: Official SDKs (@gladiaio/sdk, gladiaio-sdk) generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
## 2026-08-07 19:17:08 UTC [app] (model nemotron3)
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
## 2026-08-07 19:59:30 UTC [app] (model nemotron3)
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
[PARKED] IDOR on transcription file download endpoints /{id}/file: confidence < 40 after validation; no evidence of object-level authorization bypass; requires valid key + valid ID owned by attacker — not cross-user
[FINAL] 1) CORS wildcard reflects arbitrary origin enabling cross-origin API reads (api.gladia.io, 75, MISCONFIG) 2) SSRF via audio_url/video_url server-side fetch (api.gladia.io, 65, SSRF) 3) npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace (npm registry, 70, OTHER)
[NEXT] PROBE: curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models — confirm access-control-allow-origin reflects https://evil.test
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; undocumented /health endpoint; no auth on spec endpoint; high business value (core transcription API); potential SSRF via audio_url/video_url
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but no open redirect; HSTS preload strong; Google-only OAuth limits attack surface
[RISK] sdk: 40 reason: Official SDKs (@gladiaio/sdk, gladiaio-sdk) generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
## 2026-08-07 20:54:57 UTC [app] (model nemotron3)
[NEW] api.gladia.io: CORS wildcard returns static `*` (not reflecting request Origin) — contradicts prior hypothesis of Origin reflection
[PRIO] api.gladia.io, 8.5, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=8
[PRIO] app.gladia.io, 6.3, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] npm @gladiaio/sdk, 5.0, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] PyPI gladiaio-sdk, 4.7, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] npm gladia (typosquat candidate), 4.3, attack_surface=4 business_value=5 tech_exposure=4 gate_ease=9 cloud_surface=2 freshness=5
[HYP] SSRF via audio_url/video_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io
confidence: 72
reasoning: OpenAPI shows /v2/pre-recorded and /v2/live accept audio_url/video_url; callback_url parameter documented for async notifications; server likely fetches these URLs server-side; no SSRF protections in spec; Express backend (x-powered-by) may follow redirects
evidence_needed: Confirm server-side fetch behavior; test with internal metadata URLs (169.254.169.254), localhost, private CIDRs; check for redirect following and callback_url SSRF
verify_steps: AUTH_HELPED: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/","callback_url":"http://169.254.169.254/latest/meta-data/"}'
impact: Cloud metadata access, internal service enumeration, potential data exfiltration via callback; severity High
testability: AUTH_HELPED
[HYP] OAuth redirect_to parameter reflected in form action without validation
class: AUTH
asset: app.gladia.io
confidence: 60
reasoning: /signin?redirect_to= reflects URL-encoded value into form action attribute; Google-only OAuth limits exploitability but open redirect post-auth could chain with other issues; no evidence of allowlist validation in passive recon
evidence_needed: Confirm server-side validation of redirect_to against allowlist post-Google-OAuth; test if arbitrary external domains accepted after successful auth
verify_steps: HUMAN: Complete Google OAuth flow with redirect_to=https://evil.example.com and observe final redirect target; PASSIVE: Check CSP frame-ancestors and form-action directives for restrictions
impact: Post-auth open redirect to arbitrary domain; severity Low-Medium (requires user interaction + Google auth)
testability: HUMAN_ONLY
[HYP] npm package gladia@0.1.3 impersonates official SDK namespace
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 70
reasoning: Package claims "Official TypeScript SDK for Gladia" but repo=github.com/alexisbouchez/gladia.ts (personal account), maintainer=softwarecitadel@gmail.com; official SDK is @gladiaio/sdk from gladiaio/sdk monorepo; typosquatting risk for developers
evidence_needed: Verify affiliation of alexisbouchez/softwarecitadel with Gladia; diff package code against @gladiaio/sdk for malicious behavior (install scripts, network calls, data exfiltration)
verify_steps: RAG: Read github.com/alexisbouchez/gladia.ts source; compare API surface, dependencies, install scripts with @gladiaio/sdk; HUMAN: Contact Gladia security to confirm ownership/affiliation
impact: Supply chain risk — developers may install impersonated SDK leading to credential theft or malicious code execution; severity Medium-High
testability: RAG
[PARKED] CORS wildcard reflects arbitrary origin enabling cross-origin API reads: confidence dropped — probe confirms static `access-control-allow-origin: *` (no Origin reflection); wildcard without credentials is standard misconfig not exploitable for cross-origin reads of authenticated endpoints
[FINAL] 1) SSRF via audio_url/video_url server-side fetch + callback_url outbound POST (api.gladia.io, 72, SSRF) 2) npm package gladia@0.1.3 impersonates official SDK namespace (npm registry, 70, OTHER) 3) OAuth redirect_to parameter reflected in form action without validation (app.gladia.io, 60, AUTH)
[NEXT] RAG: Read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url/callback_url flows into api.gladia.io (any client-side validation, SSRF protections documented)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: CORS wildcard reflects arbitrary origin — probe shows static `*` not Origin reflection
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `x-gladia-key` header cross-origin (no credentials) — confirmed via OPTIONS probe
[LEARN] ACCEPTED AUTH @ app.gladia.io: redirect_to parameter reflected in signin form action — confirmed via GET probe
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with auth header allowed; WebSocket token-in-URL design; undocumented /health endpoint; Express backend; high business value; potential SSRF via audio_url/video_url/callback_url
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but Google-only OAuth limits exploitability; HSTS preload strong; CSP restrictive
[RISK] sdk: 40 reason: Official SDKs generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
