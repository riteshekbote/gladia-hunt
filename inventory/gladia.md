# Inventory: gladia

## Seed 2026-08-07 (passive recon)

### Hosts
- gladia.io -> 301 https://www.gladia.io/ (Vercel front; HSTS 63072000)
- www.gladia.io (marketing site, Vercel)
- api.gladia.io — API origin; / -> 404 JSON; CORS *; exposes x-gladia-request-id/traceparent/tracestate/x-request-id/x-correlation-id; HSTS preload; /openapi.json exists
- app.gladia.io — dashboard; / -> 302 /signin; cookies __sid + return-to (JWT-shaped); noindex; HSTS preload

### Code / SDK surface (in scope: Medium)
- github.com/gladiaio/sdk — monorepo: packages/sdk-js (@gladiaio/sdk), packages/sdk-python (gladiaio-sdk), packages/generator (fetches api.gladia.io/openapi.json)
- github.com/gladiaio/gladia-cli (Go)
- github.com/gladiaio/gladia-samples (Python)
- github.com/gladiaio/docs (MDX)
- github.com/gladiaio/gladiaflow (Rust)
- github.com/gladiaio/realtime-multilingual-asr-router (Python)
- github.com/gladiaio/n8n-nodes-gladia (TS)
- github.com/gladiaio/vercel-ai
- npm registry: @gladiaio/sdk (official), gladia 0.1.3 (repo alexisbouchez/gladia.ts — personal, VERIFY OWNERSHIP)
- PyPI: gladiaio-sdk

### Open questions
- Gladia API key format (for passive pattern matching)
- Disclosure/security channel for Gladia program
- Auth model of api.gladia.io (Bearer? x-api-key?)

## 2026-08-07 18:31:06 UTC
- NEW api.gladia.io: OpenAPI 3.1 fully enumerated — 14 paths; every v2 operation declares security scheme `x_gladia_key` (header `x-gladia-key`); `/v1/models` inherits global `security: null` and returns 20
- NEW api.gladia.io: auth gate confirmed — unauthenticated GET on /v2/transcription, /v2/pre-recorded, /v2/live, /v2/transcription/{id} → 401 `{"message":"no gladia key provided","request_id":"G-…"}`
- NEW api.gladia.io: CORS preflight (OPTIONS, Origin: evil.example.com) → `access-control-allow-origin: *`, `allow-methods: GET,HEAD,PUT,PATCH,POST,DELETE`, `allow-headers: x-gladia-key`, and NO `access-con
- NEW npm `gladia` 0.1.3: registry `description` = "Official TypeScript SDK for Gladia" but packaged README title = "Unofficial TypeScript SDK"; maintainer `softwarecitadel` <softwarecitadel@gmail.com>, aut
- NEW app.gladia.io `/signin`: Google-only OAuth; `redirect_to` query param reflected URL-encoded into form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; post-auth redirect target handling 
- CHANGED app.gladia.io return-to cookie re-confirmed: `eyJ1cmwiOiIvIn0=` = unsigned base64url `{"url":"/"}` (plain JSON, NOT a signed JWT); `__sid` expired/empty; both HttpOnly/Secure/SameSite=Lax

## 2026-08-07 18:51:57 UTC
- NEW api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
- NEW api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
- NEW api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
- NEW api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
- NEW api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
- NEW app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
- NEW app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
- NEW app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
- NEW npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
- CHANGED app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)
- NEW api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
- NEW api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
- NEW api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
- NEW api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
- NEW api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
- NEW app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
- NEW app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
- NEW app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
- NEW npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
- CHANGED app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)

## 2026-08-07 19:05:21 UTC
- NEW api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
- NEW api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
- NEW api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
- NEW api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
- NEW api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
- NEW app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
- NEW app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
- NEW app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
- NEW npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
- CHANGED app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)
- NEW api.gladia.io: /health endpoint returns 200 {"health":"OK"} — not in OpenAPI spec
- NEW api.gladia.io: OpenAPI spec fully enumerated — 14 paths, all v2 operations require x-gladia-key header; /v1/models has security: null (public)
- NEW api.gladia.io: CORS preflight confirms wildcard origin (*), allows x-gladia-key header, NO access-control-allow-credentials
- NEW api.gladia.io: Auth gate confirmed — unauthenticated POST /v2/live, GET /v2/transcription, /v2/pre-recorded, /v2/transcription/{id} → 401 "no gladia key provided"
- NEW api.gladia.io: InitStreamingResponse.url contains token as query param: wss://api.gladia.io/v2/live?token=<uuid>
- NEW app.gladia.io: /signin form action reflects redirect_to query param URL-encoded (e.g., action="/signin?redirect_to=https%3A%2F%2Fevil.example.com")
- NEW app.gladia.io: return-to cookie tampering test — server rejects tampered value and resets to default {"url":"/"}
- NEW app.gladia.io: /dashboard returns 200 HTML (SPA shell) without auth; auth enforced on API calls client-side
- NEW npm gladia@0.1.3: description claims "Official TypeScript SDK for Gladia" but repo=alexisbouchez/gladia.ts (personal), maintainer=softwarecitadel@gmail.com — ownership anomaly
- CHANGED app.gladia.io return-to cookie confirmed as unsigned base64url JSON (NOT a signed JWT)

## 2026-08-07 19:22:34 UTC

## 2026-08-07 20:00:21 UTC

## 2026-08-07 20:55:09 UTC
- NEW api.gladia.io: CORS wildcard returns static `*` (not reflecting request Origin) — contradicts prior hypothesis of Origin reflection
- NEW api.gladia.io: GET /v1/models w/ Origin:evil.test → ACAO:* (wildcard, not echo), expose-headers list, no credentials → CORS origin-reflection dead; wildcard confirmed on GET not just preflight
- NEW app.gladia.io: /signin re-probed 200; redirect_to still reflected into form action (surface stable)
- CHANGED reposcan 20:02/20:06: 0 new hits; compare-stt providers.ts hardcodes model name "Solaria-3" (marketing-facing, low); gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt)

## 2026-08-07 21:49:00 UTC
- NEW api.gladia.io: OpenAPI /v1/history declares `custom_metadata` as OBJECT-typed query param (additionalProperties:true) + `status`/`kind` as multi-value array params + date filters — key-gated query-par
- NEW api.gladia.io: CallbackConfigDto.url spec is `format: uri` only — no scheme enum/pattern/allowlist; client-side SSRF guard absent at schema level (confirmed this cycle)
- NEW api.gladia.io: /v1/models public payload confirms datacenters [{FR},{US}] + per-request pricing 0.000055 — cloud egress regions for SSRF targeting; `created:1730000000` is static
- NEW PyPI: gladiaio-sdk latest = 1.0.5 (version not previously recorded)
- CHANGED api.gladia.io: endpoint map stable at 14 paths; /v1/history and /v2/upload both confirmed key-gated (401 "no gladia key provided") — no unauthenticated history/upload exposure

## 2026-08-07 22:27:34 UTC
- NEW api.gladia.io: OpenAPI /v1/history declares `custom_metadata` as OBJECT-typed query param (additionalProperties:true) + `status`/`kind` as multi-value array params + date filters — key-gated query-par
- NEW api.gladia.io: CallbackConfigDto.url spec is `format: uri` only — no scheme enum/pattern/allowlist; client-side SSRF guard absent at schema level
- NEW api.gladia.io: /v1/models public payload confirms datacenters [{FR},{US}] + per-request pricing 0.000055 — cloud egress regions for SSRF targeting; `created:1730000000` is static
- NEW PyPI: gladiaio-sdk latest = 1.0.5 (version not previously recorded)
- CHANGED api.gladia.io: endpoint map stable at 14 paths; /v1/history and /v2/upload both confirmed key-gated (401) — no unauthenticated history/upload exposure
- NEW api.gladia.io: OpenAPI /v1/history declares `custom_metadata` as OBJECT-typed query param (additionalProperties:true) + `status`/`kind` as multi-value array params + date filters — key-gated query-par
- NEW api.gladia.io: CallbackConfigDto.url spec is `format: uri` only — no scheme enum/pattern/allowlist; client-side SSRF guard absent at schema level (confirmed this cycle)
- NEW api.gladia.io: /v1/models public payload confirms datacenters [{FR},{US}] + per-request pricing 0.000055 — cloud egress regions for SSRF targeting; `created:1730000000` is static
- NEW PyPI: gladiaio-sdk latest = 1.0.5 (version not previously recorded)
- CHANGED api.gladia.io: endpoint map stable at 14 paths; /v1/history and /v2/upload both confirmed key-gated (401 "no gladia key provided") — no unauthenticated history/upload exposure

## 2026-08-07 23:14:52 UTC

## 2026-08-07 23:50:17 UTC

## 2026-08-08 00:44:48 UTC
