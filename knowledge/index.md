# Knowledge Base (seed)

## Program rules (from scope.yml)
- In scope: api.gladia.io (Highest), app.gladia.io (High), official SDKs npm/PyPI (Medium), gladia.io (Low)
- Out of scope: all other *.gladia.io subdomains, third parties, social engineering, physical, DoS, non-Gladia assets, physical access
- Scanner output alone is REJECTED — every finding must be manually validated
- Passive-first: GET/HEAD only, ≤1 rps, no account creation, no data modification
- Secrets in commits: sha256 only, never raw

## Baseline surface (2026-08-07 passive recon)
- gladia.io -> 301 to www.gladia.io (Vercel, HSTS max-age=63072000, x-vercel-id)
- api.gladia.io: 404 JSON on /, CORS access-control-allow-origin: *, exposes x-gladia-request-id, traceparent, tracestate, x-request-id, x-correlation-id; HSTS includeSubDomains preload; no WWW-Authenticate on 404
- api.gladia.io/openapi.json: OpenAPI schema consumed by official SDK code generator (gladiaio/sdk packages/generator)
- app.gladia.io: 302 -> /signin, sets __sid (expired) + return-to base64url JWT-ish cookie (eyJ1cmwiOiIvIn0%3D = {"url":"/"}), HttpOnly Secure SameSite=Lax, x-robots-tag noindex, HSTS preload
- GitHub org gladiaio (19 public repos): sdk (monorepo: sdk-js, sdk-python, generator), gladia-cli (Go), docs (MDX), gladia-samples (Python), gladiaflow (Rust), realtime-multilingual-asr-router (Python), n8n-nodes-gladia, vercel-ai, compare-stt (TS), skills, gladia-quiz-app, normalization, triton-inference-memory-allocation, gunicorn-fix-sigabort, uvicorn-fix-sigabort, 1password-scim, vllm_backend, transformers, cloudnative-pg
- npm: @gladiaio/sdk 1.1.0 (official, from gladiaio/sdk monorepo); `gladia` 0.1.3 claims "Official TypeScript SDK for Gladia" but repository = alexisbouchez/gladia.ts (PERSONAL account — flag, verify ownership)
- PyPI: gladiaio-sdk (Python SDK, sync + async)

## Rejected / parked
- (none yet)
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI spec publicly exposed at /openapi.json with full v2 surface
- 2026-08-07 ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per spec
- 2026-08-07 ACCEPTED AUTH @ app.gladia.io: return-to cookie uses JWT-shaped base64url value without visible signature
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- 2026-08-07 ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- 2026-08-07 REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- 2026-08-07 ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
- 2026-08-07 ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
- 2026-08-07 REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
- 2026-08-07 ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; framework fingerprint for CVE targeting
- 2026-08-07 REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
- 2026-08-07 REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
- 2026-08-07 REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
- 2026-08-07 REJECTED MISCONFIG @ api.gladia.io: CORS wildcard reflects arbitrary origin — probe shows static `*` not Origin reflection
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `x-gladia-key` header cross-origin (no credentials) — confirmed via OPTIONS probe
- 2026-08-07 ACCEPTED AUTH @ app.gladia.io: redirect_to parameter reflected in signin form action — confirmed via GET probe
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: CORS GET responses return wildcard `*` not origin echo; expose-headers list trace/request-id headers; no allow-credentials → origin-reflection probe CLOSED, wildcard-without-credentials not exploitable
- 2026-08-07 ACCEPTED OTHER @ npm registry: reposcan 20:02/20:06 flat (0 new hits, 5647 files) — gladia@0.1.3 anomaly remains sole reportable candidate; no new secrets
- 2026-08-07 ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, not plain Express
- 2026-08-07 ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
- 2026-08-07 ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflight-only fingerprint differential (freshness 2026-08-07 21:46 UTC).
- 2026-08-07 ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), and path-only variants — no host allowlist enforced on reflection (post-auth honoring remains AUTH_HELPED/unverified).
- 2026-08-07 CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-design path (freshly sampled).
