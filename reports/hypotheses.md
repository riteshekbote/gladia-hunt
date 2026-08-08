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
