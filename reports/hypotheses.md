# Ranked Hypotheses

## SEED 2026-08-07 (from passive recon, not model-generated yet)
- [60] api.gladia.io: OpenAPI spec exposure at /openapi.json — check for undocumented/shadow endpoints (from inventory seed)
- [55] api.gladia.io: CORS wildcard with credentials on API origin — verify actual Access-Control-Allow-Credentials behavior (from inventory seed)
- [50] app.gladia.io: return-to cookie JWT-shaped value — check signature/alg handling in redirect flow (from inventory seed)
- [45] npm `gladia` 0.1.3: "Official TS SDK" published from personal repo alexisbouchez/gladia.ts — ownership/typosquat anomaly, verify before reporting (from inventory seed)

## RANKED HYPOTHESES 2026-08-07 18:31:06 UTC
- [75] api.gladia.io: CORS wildcard reflects origin (from reports/hypotheses-laguna.txt)
- [70] api.gladia.io: OpenAPI shadow endpoints / undocumented v2 paths (from reports/hypotheses-nemotron3.txt)
- [58] api.gladia.io: SSRF via file-URL ingestion in transcription/upload endpoints (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): PROBE: POST https://api.gladia.io/v2/live/init -H "Content-Type: application/json" -d '{}' (observe auth requirement, response shape, token format)
- NEXT(hypotheses-bigpickle.txt): RAG: read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any c
- NEXT(hypotheses-laguna.txt): PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json` — check if `access-control-allow-origin` reflects `https://evi
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI spec publicly exposed at /openapi.json with full v2 surface
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per spec
- LEARN: ACCEPTED AUTH @ app.gladia.io: return-to cookie uses JWT-shaped base64url value without visible signature

## RANKED HYPOTHESES 2026-08-07 18:51:57 UTC
- [80] api.gladia.io: Undocumented /health endpoint on api.gladia.io leaks runtime status (from reports/hypotheses-nemotron3.txt)
- [65] api.gladia.io: SSRF via audio_url/video_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [65] api.gladia.io: CORS wildcard enables cross-origin read of API data/spec (no credential support) (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): PROBE: GET https://api.gladia.io/health?full=true — check for verbose health output
- NEXT(hypotheses-laguna.txt): PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-ori
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification

## RANKED HYPOTHESES 2026-08-07 19:05:21 UTC
- [80] api.gladia.io: Undocumented /health endpoint on api.gladia.io leaks runtime status (from reports/hypotheses-nemotron3.txt)
- [65] api.gladia.io: SSRF via audio_url/video_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [65] api.gladia.io: CORS wildcard enables cross-origin read of API data/spec (no credential support) (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): PROBE: GET https://api.gladia.io/health?full=true — check for verbose health output
- NEXT(hypotheses-laguna.txt): PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-ori
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification

## RANKED HYPOTHESES 2026-08-07 19:22:34 UTC
- [70] api.gladia.io: SSRF via audio_url/video_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [50] api.gladia.io: IDOR on transcription file download endpoints /{id}/file (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any c
- NEXT(hypotheses-bigpickle.txt): HUMAN: with a program-provided or personal trial `x-gladia-key`, POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` then `{"a
- NEXT(hypotheses-laguna.txt): PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-glad
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli

## RANKED HYPOTHESES 2026-08-07 20:00:21 UTC
- [72] api.gladia.io: SSRF via audio_url fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- [65] api.gladia.io: SSRF via audio_url/video_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- [55] npm: npm `gladia` package impersonates official SDK from personal repo (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): PROBE: curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models — confirm access-control-allow-origin reflects https://evil.test
- NEXT(hypotheses-bigpickle.txt): HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest
- NEXT(hypotheses-laguna.txt): PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-ori
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli

## RANKED HYPOTHESES 2026-08-07 20:55:09 UTC
- [72] api.gladia.io: SSRF via audio_url/video_url server-side fetch + callback_url outbound POST (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url/callback_url flows into api.gla
- NEXT(hypotheses-bigpickle.txt): HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest
- LEARN: REJECTED MISCONFIG @ api.gladia.io: CORS wildcard reflects arbitrary origin — probe shows static `*` not Origin reflection
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `x-gladia-key` header cross-origin (no credentials) — confirmed via OPTIONS probe
- LEARN: ACCEPTED AUTH @ app.gladia.io: redirect_to parameter reflected in signin form action — confirmed via GET probe
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS GET responses return wildcard `*` not origin echo; expose-headers list trace/request-id headers; no allow-credentials →
- LEARN: ACCEPTED OTHER @ npm registry: reposcan 20:02/20:06 flat (0 new hits, 5647 files) — gladia@0.1.3 anomaly remains sole reportable candidate; no new secrets

## RANKED HYPOTHESES 2026-08-07 21:49:00 UTC
- [72] api.gladia.io: SSRF via audio_url server-side fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- [52] app.gladia.io: Post-OAuth open redirect via redirect_to without host allowlist (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-bigpickle.txt): HUMAN: request a program-provided or personal trial `x-gladia-key`; then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest
- NEXT(hypotheses-laguna.txt): HUMAN: with an authorized/verified session (Google SSO or program-supplied trial key), GET /signin?redirect_to=https://evil.example.com then complete OAuth, cap
- LEARN: ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, 
- LEARN: ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflig
- LEARN: ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), a
- LEARN: CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-

## RANKED HYPOTHESES 2026-08-07 22:27:34 UTC
- [75] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-laguna.txt)
- [75] api.gladia.io: SSRF via audio_url/video_url server-side fetch + callback_url outbound POST (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url server-side fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Read github.com/alexisbouchez/gladia.ts source code (packages/gladia.ts if monorepo) and compare against @gladiaio/sdk (gladiaio/sdk/packages/sdk-js) for i
- NEXT(hypotheses-bigpickle.txt): HUMAN: request a program-provided or personal trial `x-gladia-key`; then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest
- NEXT(hypotheses-laguna.txt): RAG: Read gladiaio/sdk monorepo (packages/sdk-js, packages/sdk-python, packages/generator) and gladia-samples to trace how audio_url → POST /v2/pre-recorded and
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI /v1/history exposes OBJECT-typed custom_metadata query param with additionalProperties:true — complex query parsing 
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CallbackConfigDto.url lacks scheme allowlist/pattern at schema level — SSRF guard absent by design in spec
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v1/models public endpoint leaks datacenter regions (FR/US) and static pricing metadata — aids SSRF egress targeting
- LEARN: ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, 
- LEARN: ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflig
- LEARN: ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), a
- LEARN: CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-
- LEARN: ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, 
- LEARN: ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- LEARN: ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- LEARN: ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; fra
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata d
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no cr
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then cli
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflig
- LEARN: ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), a
- LEARN: CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed OPTIONS /v2/transcription → x-powered-by: Express present, ACAO:*, Access-Control-Allow-Headers: x-gladia-key (2
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed GET /v2/transcription → 401 no gladia key provided, x-powered-by absent (preflight-only fingerprint confirmed, 2
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, 125KB, CORS *) exposes InitTranscriptionRequest.audio_url as format:uri with no scheme allowlist + depre
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /health returns 200 {"health":"OK"}; /health?full=true returns identical payload — no verbose disclosure via query param (RE
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /metrics (404), /debug (404), /admin (404), /actuator/health (404) — no Prometheus, no debug panel, no Spring Boot Actuator 
- LEARN: ACCEPTED AUTH @ api.gladia.io: POST /v2/live → 401 key-gated; POST /v2/live/init → 404 "Cannot POST" — WebSocket session created via POST /v2/live then wss://ap
- LEARN: ACCEPTED OATH @ app.gladia.io: live-probed /signin?redirect_to=https://evil.example.com → form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" — ser
- LEARN: REJECTED AUTH @ app.gladia.io: return-to cookie tampering does NOT lead to open redirect — server resets tampered value to {"url":"/"} (REJECTED as redirect vec
- LEARN: ACCEPTED OTHER @ npm: gladia@0.1.3 registry metadata stable (description "Official TypeScript SDK", repo alexisbouchez/gladia.ts personal, maintainer softwareci
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 14 OpenAPI paths stable (no new endpoints since 21:46 UTC); /v1/models public (security: not set), all other v2 paths key-ga

## RANKED HYPOTHESES 2026-08-07 23:14:52 UTC
- [80] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-laguna.txt)
- [75] api.gladia.io: SSRF via audio_url/video_url server-side fetch + callback_url outbound POST (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url server-side fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Read github.com/alexisbouchez/gladia.ts source code (packages/gladia.ts if monorepo) and compare against @gladiaio/sdk (gladiaio/sdk/packages/sdk-js) for i
- NEXT(hypotheses-bigpickle.txt): HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://1
- NEXT(hypotheses-laguna.txt): HUMAN: Request a program-provided or authorized trial `x-gladia-key` to perform the AUTH_HELPED SSRF verification: (1) POST https://api.gladia.io/v2/pre-recorde
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI /v1/history exposes OBJECT-typed custom_metadata query param with additionalProperties:true — complex query parsing 
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CallbackConfigDto.url lacks scheme allowlist/pattern at schema level — SSRF guard absent by design in spec
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v1/models public endpoint leaks datacenter regions (FR/US) and static pricing metadata — aids SSRF egress targeting
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 14 OpenAPI paths stable (no new endpoints since 21:46 UTC); /v1/models public (security: not set), all other v2 paths key-ga
- LEARN: REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surf
- LEARN: ACCEPTED SSRF @ api.gladia.io: RAG of SDK source (packages/sdk-js/client.ts + packages/sdk-python/v2/prerecorded/core.py) confirms is_url()/uploadFile() only ga
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed OPTIONS /v2/pre-recorded → x-powered-by: Express present; POST → 401 x-powered-by absent — confirmed preflight-o
- LEARN: ACCEPTED AUTH @ api.gladia.io: POST /v2/pre-recorded with invalid key → 401 NestJS HttpException shape {statusCode,timestamp,path,message,request_id} — no x-pow
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com verified live 23:09 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.exampl
- LEARN: ACCEPTED OTHER @ npm: gladia@0.1.3 registry metadata stable 23:09 UTC (description="Official TypeScript SDK for Gladia", repo=alexisbouchez/gladia.ts personal, 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /v2/live/init confirmed 404 "Cannot POST" — not a real endpoint; WebSocket session created via POST /v2/live then wss://api.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, CORS *) exposes video_url as plain string field with no format/scheme validation in /video/text/video-tr

## RANKED HYPOTHESES 2026-08-07 23:50:17 UTC
- [80] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url server-side fetch + callback_url outbound POST (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Read github.com/alexisbouchez/gladia.ts source code (packages/gladia.ts if monorepo) and compare against @gladiaio/sdk (gladiaio/sdk/packages/sdk-js) for i
- NEXT(hypotheses-bigpickle.txt): HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://1
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI /v1/history exposes OBJECT-typed custom_metadata query param with additionalProperties:true — complex query parsing 
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: CallbackConfigDto.url lacks scheme allowlist/pattern at schema level — SSRF guard absent by design in spec
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /v1/models public endpoint leaks datacenter regions (FR/US) and static pricing metadata — aids SSRF egress targeting
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: 14 OpenAPI paths stable (no new endpoints since 21:46 UTC); /v1/models public (security: not set), all other v2 paths key-ga
- LEARN: REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surf
- LEARN: ACCEPTED SSRF @ api.gladia.io: RAG of SDK source (packages/sdk-js/client.ts + packages/sdk-python/v2/prerecorded/core.py) confirms is_url()/uploadFile() only ga
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live-probed OPTIONS /v2/pre-recorded → x-powered-by: Express present; POST → 401 x-powered-by absent — confirmed preflight-o
- LEARN: ACCEPTED AUTH @ api.gladia.io: POST /v2/pre-recorded with invalid key → 401 NestJS HttpException shape {statusCode,timestamp,path,message,request_id} — no x-pow
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com verified live 23:09 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.exampl
- LEARN: ACCEPTED OTHER @ npm: gladia@0.1.3 registry metadata stable 23:09 UTC (description="Official TypeScript SDK for Gladia", repo=alexisbouchez/gladia.ts personal, 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: /v2/live/init confirmed 404 "Cannot POST" — not a real endpoint; WebSocket session created via POST /v2/live then wss://api.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, CORS *) exposes video_url as plain string field with no format/scheme validation in /video/text/video-tr
- LEARN: REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surf
- LEARN: REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surf
- LEARN: REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:48Z byte-identical to 23:08Z (openapi 125131B/14 paths, /v1/models 530B, /health 15B, 401 gate, pre
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk@1.1.0 metadata static 23:48Z — supply-chain surface unchanged.
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com form-action reflection re-confirmed 23:48Z — reflection surface persists, post-auth 

## RANKED HYPOTHESES 2026-08-08 00:44:48 UTC
- [85] npm: `gladia`@0.1.3 ships internal README titled "Unofficial" while package.json/npm-search says "Official" — active impersonation, plus raw API key in WS URL query (diverges from official SDK's token-in-URL after /v2/live init) (from reports/hypotheses-bigpickle.txt)
- [80] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-bigpickle.txt): RAG: document the `gladia`@0.1.3 artifact-level finding for the report — tarball README "Unofficial" vs package.json "Official" contradiction + `x-gladia-key` r
- NEXT(hypotheses-laguna.txt): HUMAN: api.gladia.io is HIGHEST-priority with the top-ranked SSRF hypothesis gated only by a valid API key. Request a program-provided / authorized trial `x-gla
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /health returns 200 `{"health":"OK"}` (x-powered-by ABSENT on GET) — undocumented endpoint + preflight-only fingerprint conf
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: OPTIONS /v2/transcription 204 `x-powered-by: Express` + ACAO `*` + allow `x-gladia-key`, POST 401 no`x-powered-by` — preflig
- LEARN: ACCEPTED AUTH @ api.gladia.io: POST /v2/transcription (no key) → 401 — key-gated surface confirmed; @gladiaio/key header is the sole auth model
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: /openapi.json (200, 125131B, CORS `*`, expose-headers trace ids) + /v1/models (200 public CORS `*`) fully exposed — surface 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com → form action reflects URL-encoded value — reflection confirmed fresh 23:5x UTC
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 text/html (SPA shell) without auth — client-side enforcement confirmed fresh
- LEARN: ACCEPTED OTHER @ npm: `gladia`@0.1.3 description "Official TypeScript SDK…", repo alexisbouchez/gladia.ts (personal), maintainer softwarecitadel@gmail.com — imp
- LEARN: (no new REJECTED class this cycle; surface re-confirmed byte-identical to 23:08 per 23:48 prior re-probe — drift negative)

## RANKED HYPOTHESES 2026-08-08 03:03:04 UTC
- [88] npm: `gladia`@0.1.3 is now an orphaned impersonation package — source repo alexisbouchez/gladia.ts returns 404 while dist-tag latest persists (from reports/hypotheses-bigpickle.txt)
- [85] npm: Artifact-level package impersonation + WebSocket API-key leakage in npm `gladia`@0.1.3 (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-bigpickle.txt): RAG: finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-laguna.txt): HUMAN: Request an authorized Google SSO session for app.gladia.io to close the #3 open-redirect POC — complete the OAuth sign-in with `?redirect_to=https://evil
- LEARN: CONFIRMED OTHER @ npm gladia@0.1.3: artifact-level impersonation independently re-verified 02:50 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 02:50 UTC across protocol-relative //evil, bare-host, app.gladia.io.evil confusin
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→23:48→00:44→02:50 UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, x-powered-by
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 02:50 UTC (OPTIONS /v2/transcription 204 xpb
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec/spec+RAG unchanged 02:50 UTC (audio_url/video_url/callback_url format:uri no scheme allowlist, no client-side guard) — SSRF-

## RANKED HYPOTHESES 2026-08-08 04:03:29 UTC
- [85] npm: Artifact-level package impersonation + WebSocket API-key leakage in npm `gladia`@0.1.3 (from reports/hypotheses-laguna.txt)
- [85] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via the official `gladia.io/bug-bounty-report` form (evidence: tarball sha256 3b23ec7d..., README "Unofficial" vs packag
- NEXT(hypotheses-laguna.txt): HUMAN: phase is POC, target is app. The reflection surface for `redirect_to` on app.gladia.io `/signin` is confirmed unauthenticated (04:01 UTC), but post-auth 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: artifact-level impersonation independently re-verified 02:50 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 02:50 UTC across protocol-relative //evil, bare-host, app.gladia.io.evil confusin
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→23:48→00:44→02:50 UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, x-powered-by
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 02:50 UTC (OPTIONS /v2/transcription 204 xpb
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec/spec+RAG unchanged 02:50 UTC (audio_url/video_url/callback_url format:uri no scheme allowlist, no client-side guard) — SSRF-
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→23:48→00:44→02:50→04:01 UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, x-powe
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 04:01 UTC (OPTIONS /v2/transcription 204 xpb
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: GET /v2/transcription (no key) → 401 NestJS HttpException shape confirmed fresh 04:01 UTC (timestamp 2026-08-08T04:01:14.742
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 04:01 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: CONFIRMED OTHER @ npm `gladia`@0.1.3: orphaned impersonation re-verified 04:01 UTC — `npm view` 4 versions [0.1.0–0.1.3], latest=0.1.3; GitHub API + web `alexis
- LEARN: ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 04:01 UTC — form action reflects URL-encoded value; no host allowlist at unauthe

## RANKED HYPOTHESES 2026-08-08 05:12:15 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via the confirmed disclosure channel gladia.io/bug-bounty-report (Google Form, live this cycle; NOT security.txt which i
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 04:01
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 04:01 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 04:01 UTC — form action reflects URL-encoded value; no host allowlist at unauthen

## RANKED HYPOTHESES 2026-08-08 06:08:58 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [72] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d…, README "Unofficial" vs package.json "Official", r
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. The `redirect_to` reflection surface on app.gladia.io `/signin` is confirmed unauthenticated + fresh (06:00 UTC) for https:/
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 04:01
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 04:01 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 04:01 UTC — form action reflects URL-encoded value; no host allowlist at unauthen

## RANKED HYPOTHESES 2026-08-08 07:10:17 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [65] app.gladia.io: Post-auth open redirect via reflected redirect_to on signin form action (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d…, README "Unofficial" vs package.json "Official" in
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. The `redirect_to` reflection surface on app.gladia.io `/signin` is confirmed unauthenticated + fresh (07:0x UTC) for `https:
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 04:01
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 04:01 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 04:01 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01→07:0x UTC); openapi 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-p
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential confirmed fresh 07:0x UTC (OPTIONS /v2/transcription 204 xpb
- LEARN: ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 07:0x UTC — form action reflects URL-encoded value; no host allowlist at u
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 07:0x UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: ACCEPTED OTHER @ npm: gladia@0.1.3 sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` confirmed unchanged fresh 07:0x UTC; repo alexisbou

## RANKED HYPOTHESES 2026-08-08 08:03:21 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [65] app.gladia.io: app.gladia.io /signin post-auth open redirect / OAuth redirect_uri injection via reflected redirect_to (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): PROBE: confirm the dynamic-spec observation is systemic — three fetches of https://api.gladia.io/openapi.json spaced 30s apart must each yield a distinct sha256
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target app. Authorized Google SSO session required to verify the sole unverified gate for the top app hypothesis: app.gladia.io /signin?red
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 07:59
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 7 cycles (23:08→07:59 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 07:59 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 07:59 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 07:59 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 6 cycles (23:08→04:01→07:0x UTC) — surface frozen, nothing new this cycle
- LEARN: ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 07:0x UTC — form action reflects URL-encoded value; no host allowlist at u
- LEARN: ACCEPTED OTHER @ npm: gladia@0.1.3 orphaned impersonation re-verified — sha256 `3b23ec7d…7f2` unchanged; source repo alexisbouchez/gladia.ts + GitHub user 404 (

## RANKED HYPOTHESES 2026-08-08 08:56:52 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via the gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eeca
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 07:59
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 7 cycles (23:08→07:59 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 07:59 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 07:59 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 07:59 UTC — client-side enforcement confirmed; server-side 302 gate on /a

## RANKED HYPOTHESES 2026-08-08 09:47:28 UTC
- [95] npm: npm `gladia@0.1.3` orphaned impersonation leaks API key in WebSocket URL query (from reports/hypotheses-laguna.txt)
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): RAG: Finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure p
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa8
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. The npm `gladia@0.1.3` finding is PASSIVE-verified (sha256 `3b23ec7d…7f2`, src/client.ts:307 key-in-URL, README↔package.json
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 09:45
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 8 cycles (23:08→09:44 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 09:44 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 09:44 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 09:44 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: REJECTED OTHER @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches → 3 distinct example timestamps (25.976/32.264/26.548Z) 
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: structural hash 9a326c92… (examples-stripped) stable across 3 fetches → validated drift baseline; raw byte hash varies per f
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (09:44 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by 

## RANKED HYPOTHESES 2026-08-08 10:19:38 UTC
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- [65] app.gladia.io: app.gladia.io /signin post-auth open redirect via reflected redirect_to (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via the gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eeca
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across
- LEARN: REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.26
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (09:44 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 09:45
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 8 cycles (23:08→09:44 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 09:44 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 09:44 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 09:44 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-po
- LEARN: ACCEPTED OTHER @ api.gladia.io: recorded structural-hash baseline `9a326c92…` is not reproducible without the original strip recipe — my normalization yields `a
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum `cc96f84a…` current dist-shasum, source repo alexisbouchez/gladia.ts + user 404, di
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists fresh 10:16 UTC — description "Official", orphaned repo/user 404, sha256 3b23ec7d…7f2, README↔package.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 10:16 UTC — openapi 125131B/14 paths, /health 15B {health:OK}, /v1/models 530B public, preflight-only x-power
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed fresh 10:16 UTC (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP has 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard 200 text/html SPA shell without auth confirmed fresh — client-side enforcement; server-side 302 gate intact on /a
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists fresh 10:16 UTC — description "Official", orphaned repo/user 404, sha256 3b23ec7d…7f2, README↔package.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 10:16 UTC — openapi 125131B/14 paths, /health 15B {health:OK}, /v1/models 530B public, preflight-only x-power
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed fresh 10:16 UTC (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP has 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard 200 text/html SPA shell without auth confirmed fresh — client-side enforcement; server-side 302 gate intact on /a

## RANKED HYPOTHESES 2026-08-08 10:58:11 UTC
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [65] app.gladia.io: Post-auth open redirect via reflected redirect_to on signin form action (from reports/hypotheses-nemotron3.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across
- LEARN: REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.26
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (10:16 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 10:16
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→10:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 10:16 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 10:16 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 10:16 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.

## RANKED HYPOTHESES 2026-08-08 11:41:38 UTC
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- [65] app.gladia.io: Post-auth open redirect via reflected redirect_to on signin form action (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 11:36 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` + integrity sha512-56NWQ9pEVyd/… unchanged, repo alexisbouchez/gladia.ts + user 4
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across
- LEARN: REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.26
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (10:16 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 10:16
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→10:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 10:16 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 10:16 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 10:16 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: structural hash (examples-stripped) stable at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across
- LEARN: REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches returned 3 distinct example timestamps (25.976/32.26
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (10:16 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — source repo alexisbouchez/gladia.ts + user 404 while dist-tag latest persists (fresh 10:16
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→10:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powere
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG unchanged 10:16 UTC; audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/model
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 10:16 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 (SPA shell) without auth at 10:16 UTC — client-side enforcement confirmed; server-side 302 gate on /a
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.
- LEARN: ACCEPTED OATH @ app.gladia.io: POST /signin intent=google initiates OAuth carrying redirect_to (302→accounts.google.com) at unauth layer — reflection confirmed 
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABS
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real 

## RANKED HYPOTHESES 2026-08-08 12:03:43 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 11:36 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABS
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real 
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no 

## RANKED HYPOTHESES 2026-08-08 13:12:56 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→13:10 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 13:10 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABS
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real 
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 12 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 stati
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 11:36 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest 
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP directive set verified fresh — base-uri 'self', object-src 'none', frame-src 'self'+allowlist; form-action directive ABS
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org + /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all) — no real 
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: Orphaned impersonation confirmed fresh — src/client.ts:307 embeds raw x-gladia-key into wss://api.gladia.io/v2/live?token=<ke
- LEARN: ACCEPTED SSRF @ api.gladia.io: /openapi.json spec confirms audio_url/video_url/callback_url as format:uri with NO scheme allowlist on /v2/pre-recorded — gated o
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT at 13:10 UTC — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by, CORS stat
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection persists — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.co
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org & /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html SPA catch-all; real server
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback; no OAut
- LEARN: REJECTED MISCONFIG @ app.gladia.io: return-to cookie tampering does NOT lead to open redirect — server resets tampered value to {"url":"/"} (REJECTED, confirmed

## RANKED HYPOTHESES 2026-08-08 14:04:58 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-laguna.txt)
- [95] npm: Orphaned npm package gladia@0.1.3 actively impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and 
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 12 cycles (23:08→13:10 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive 13:10 UTC — form action reflects URL-encoded value; no host allowlist at unauthen
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum cc96f84a… unchanged, repo alexisbouchez/gladia.ts + user 404 while dist-tag latest 
- LEARN: REJECTED OATH @ app.gladia.io: redirect_to is NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback → no 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 13 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — dist-tag latest=0.1.3, shasum `cc96f84a…` + integrity stable, repo alexisbouchez/gladia.ts + user 40
- LEARN: REJECTED MISCONFIG @ api.gladia.io: 14:02 UTC fresh probe byte-identical to 13:10 UTC (openapi 125131B/14 paths, /health 15B no x-powered-by on GET, /v1/models 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 14:02 UTC (200, form action reflects URL-encoded va
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti

## RANKED HYPOTHESES 2026-08-08 14:50:37 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: 14:02 UTC fresh probe byte-identical to 13:10 UTC — 13th NO_DRIFT cycle, surface frozen
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 14:02 UTC — form action reflects URL-encoded value;
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 14 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive 14:48 UTC — form action reflects URL-encoded value; no ho
- LEARN: REJECTED MISCONFIG @ api.gladia.io: 14:02 UTC fresh probe byte-identical to 13:10 UTC — 13th NO_DRIFT cycle, surface frozen.
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 14:02 UTC — form action reflects URL-encoded value;
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflection unc
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 `3b23ec7d…7f2` unchanged, repo alexisbouchez/gladia.ts + user 404, src/client.ts:307 e
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec confirms audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; key-gated 401 — 
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=http://app.gladia.io/auth/google/callback; no OAut

## RANKED HYPOTHESES 2026-08-08 15:21:19 UTC
- [95] npm: Orphaned npm package `gladia@0.1.3` impersonates official SDK leaking API key in WebSocket URL (from reports/hypotheses-laguna.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-nemotron3.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-laguna.txt): HUMAN — Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=ht
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 14 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive 14:48 UTC — form action reflects URL-encoded value; no ho
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: fresh probe confirms NO_DRIFT (15th cycle) — openapi 125131B/14 paths, /health `{"health":"OK"}`, /v1/models 530B, preflight
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host a
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: /dashboard returns 200 SPA shell without auth — client-side enforcement; server-side 302 gate intact on /apikeys,/transcript
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 `3b23ec7d…7f2` unchanged, repo alexisbouchez/gladia.ts + user 404, src/client.ts:307 e
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec unchanged (15th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; 
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu

## RANKED HYPOTHESES 2026-08-08 15:53:13 UTC

## RANKED HYPOTHESES 2026-08-08 17:05:52 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. With program authorization, complete the Google OAuth (or email/password) flow on `https://app.gladia.io/signin?redirect_to=
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 15 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive 14:48 UTC — form action reflects URL-encoded value; no ho
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses fixed redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec unchanged (15th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 16 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host a
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 15+ cycles (23:08→17:0x UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation re-verified fresh 17:0x UTC — sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu

## RANKED HYPOTHESES 2026-08-08 17:52:29 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK, leaking API key in WebSocket URL (from reports/hypotheses-laguna.txt)
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs p
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target app. With program authorization, complete the Google OAuth (or email/password) flow on https://app.gladia.io/signin?redirect_to=http
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 16 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:43 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec unchanged (16th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation re-verified fresh 17:0x UTC — sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 17 cycles (23:08→17:43 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC M-bM-^@M-^T form action reflects URL-enco
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri M-bM-^@M-^T server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callba
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/m
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/m
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→17:44 UTC) — openapi 125131B/14 paths, /health `{"health":"OK"}` 15B, /v1/models 530B FR/U
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 `3b23ec7d…7f2` unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/m
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu

## RANKED HYPOTHESES 2026-08-08 18:18:19 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec unchanged (20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 17:52 UTC (openapi 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 17:52 UTC — form action reflects URL-encoded value; no host allowlist at un
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 16 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:43 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec unchanged (16th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/models confirms FR/US egress; 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation re-verified fresh 17:0x UTC — sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 17 cycles (23:08→17:43 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:0x UTC M-bM-^@M-^T form action reflects URL-enco
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri M-bM-^@M-^T server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callba
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->17:44 UTC) — openapi 125131B/14 paths, /health {"health":"OK"} 15B, /v1/models 530B FR/US
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 17:44 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG confirmed fresh 17:44 UTC (NO_DRIFT 20th cycle) — audio_url/video_url/callback_url format:uri no scheme allowlist; /v1/m
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 17:44 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 18 probe cycles (23:08→18:00 UTC) — openapi 125131B/14 paths, /health `{"health":"OK"}` 15B (x-powered-by AB
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint differential re-confirmed fresh (OPTIONS 204 x-powered-by=Express, GET/PO
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (17th cycle) — audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/mode
- LEARN: ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation confirmed fresh — dist-tag latest=0.1.3 stable (sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed byte-fresh (action="/signin?redirect_to=https%3A%2F%2Fevil.exam
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no code/state thef
- LEARN: REJECTED OAUTH @ app.gladia.io: return-to cookie tampering does NOT yield open redirect — server resets to {"url":"/"} (tamper-reset confirmed).
- LEARN: CONFIRMED MISCONFIG @ app.gladia.io: /dashboard & /org & /api,/oauth,/auth,/oid4,/api/v1,/api/health,/api/me all return 200 text/html (SPA catch-all); real serv

## RANKED HYPOTHESES 2026-08-08 19:06:08 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK, leaking API key in WebSocket URL (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shas
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→18:18 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 `3b23ec7d…7f2`, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.
- LEARN: ACCEPTED OAUTH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive at 18:18 UTC; CSP lacks form-action directive (base-uri 
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (21st cycle) — audio_url/video_url/callback_url/CallbackConfig.url format:uri no scheme allowlist; /v1/models con

## RANKED HYPOTHESES 2026-08-08 19:45:02 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Phase is POC, target is app. Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target po
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→18:18 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 18:18 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (21st cycle) — audio_url/video_url/callback_url/CallbackConfig.url format:uri no scheme allowlist; /v1/models con
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 18:18 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED OTHER @ npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) and mainta
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh (openapi 125131B/14 paths, /health 15B, /v1/models 530B) — 22nd frozen cycle, nothing new to report
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT at 19:10 UTC (20th+ cycle) — openapi 125131B/14 paths, /health 15B no x-powered-by on GET, /v1/models 530B FR/US, p
- LEARN: ACCEPTED MISCONFIG @ api.gladia.io: preflight-only `x-powered-by: Express` fingerprint confirmed fresh — OPTIONS /v2/pre-recorded 204 x-powered-by=Express; POST
- LEARN: ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation alive & byte-fresh 19:10 UTC — dist-tag latest=0.1.3 stable, sha256 `3b23ec7d…7f2`, repo+user alexis
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed byte-fresh 19:10 UTC — form action reflects URL-encoded value; CSP verified fresh: base
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen — audio_url/video_url/callback_url/CallbackConfig.url all `format:uri` no scheme allowlist; /v1/models confirms F

## RANKED HYPOTHESES 2026-08-08 20:12:00 UTC
- [95] npm: npm gladia@0.1.3 orphaned impersonation + API-key-in-WSS-URL (from reports/hypotheses-laguna.txt)
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gat
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→18:18 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 18:18 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (21st cycle) — audio_url/video_url/callback_url/CallbackConfig.url format:uri no scheme allowlist; /v1/models con
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 18:18 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED OTHER @ npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) and mainta
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no cod
- LEARN: REJECTED MISCONFIG @ app.gladia.io: return-to cookie tampering does NOT yield open redirect — server resets tampered value to {"url":"/"} (tamper-reset confirme
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08->19:10 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-pow
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation stable — sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, dist-tag latest=0.1.

## RANKED HYPOTHESES 2026-08-08 20:49:54 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- [58] api.gladia.io: SSRF via file-URL ingestion in transcription/upload endpoints (from reports/hypotheses-laguna.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gat
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa
- NEXT(hypotheses-laguna.txt): RAG: read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any c
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→18:18 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 18:18 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (21st cycle) — audio_url/video_url/callback_url/CallbackConfig.url format:uri no scheme allowlist; /v1/models con
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 18:18 UTC — sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, repo alexisbouchez
- LEARN: ACCEPTED OTHER @ npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) and mainta

## RANKED HYPOTHESES 2026-08-08 21:19:34 UTC
- [95] npm: Orphaned npm package gladia@0.1.3 impersonates official SDK with API key leakage in WebSocket URL (from reports/hypotheses-nemotron3.txt)
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-nemotron3.txt): HUMAN: Complete Google OAuth flow on app.gladia.io/signin?redirect_to=https://evil.example.com and observe final redirect target post-auth — sole unverified gat
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 20+ cycles (23:08→21:16 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only 
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 21:16 UTC — form action reflects URL-encoded value;
- LEARN: REJECTED OAUTH @ app.gladia.io: redirect_to NOT usable as OAuth redirect_uri — server uses FIXED redirect_uri=https://app.gladia.io/auth/google/callback; no OAu
- LEARN: ACCEPTED MISCONFIG @ app.gladia.io: CSP verified fresh — base-uri 'self', object-src 'none', frame-src allowlist, NO form-action directive; form-action reflecti
- LEARN: ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (21st cycle) — audio_url/video_url/callback_url/CallbackConfig.url format:uri no scheme allowlist; /v1/models con
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh 21:16 UTC — sha1 cc96f84a, sha256 3b23ec7d...7f2 unchanged, dist-tag latest=0.1.3, rep
- LEARN: ACCEPTED OTHER @ npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) and mainta

## RANKED HYPOTHESES 2026-08-08 21:52:34 UTC
- [73] api.gladia.io: SSRF via audio_url/video_url/callback_url server-side fetch (from reports/hypotheses-bigpickle.txt)
- NEXT(hypotheses-bigpickle.txt): HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json 
- LEARN: REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 24 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-p
- LEARN: ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host a
- LEARN: ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), di
