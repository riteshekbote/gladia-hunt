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
