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

## 2026-08-08 03:03:04 UTC

## 2026-08-08 04:03:29 UTC
- NEW npm gladia@0.1.3: source repository alexisbouchez/gladia.ts (GitHub user + repo) now returns 404 — package orphaned while dist-tag latest persists
- NEW api.gladia.io: NO_DRIFT confirmed across 6 probe cycles (23:08→23:48→00:44→02:50 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS static wi
- CHANGED npm gladia@0.1.3: artifact-level impersonation independently re-verified at 02:50 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json "Official" vs READM

## 2026-08-08 05:12:15 UTC
- NEW npm gladia@0.1.3: source repository alexisbouchez/gladia.ts (GitHub user + repo) now returns 404 — package orphaned while dist-tag latest persists
- NEW api.gladia.io: NO_DRIFT confirmed across 6 probe cycles (23:08→23:48→00:44→02:50→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS sta
- CHANGED npm gladia@0.1.3: artifact-level impersonation independently re-verified at 04:01 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json "Official" vs READM

## 2026-08-08 06:08:58 UTC
- NEW npm gladia@0.1.3: source repository alexisbouchez/gladia.ts (GitHub user + repo) now returns 404 — package orphaned while dist-tag latest persists
- NEW api.gladia.io: NO_DRIFT confirmed across 6 probe cycles (23:08→23:48→00:44→02:50→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS sta
- CHANGED npm gladia@0.1.3: artifact-level impersonation independently re-verified at 04:01 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json "Official" vs READM

## 2026-08-08 07:10:17 UTC
- NEW npm gladia@0.1.3: source repository alexisbouchez/gladia.ts (GitHub user + repo) now returns 404 — package orphaned while dist-tag latest persists
- NEW api.gladia.io: NO_DRIFT confirmed across 6 probe cycles (23:08→23:48→00:44→02:50→04:01 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS sta
- CHANGED npm gladia@0.1.3: artifact-level impersonation independently re-verified at 04:01 UTC (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2; package.json "Official" vs READM

## 2026-08-08 08:03:21 UTC

## 2026-08-08 08:56:52 UTC

## 2026-08-08 09:47:28 UTC
- CHANGED api.gladia.io /openapi.json: example-timestamp fingerprint is NOT a stable per-instance set — 3 fresh fetches returned 3 distinct values (21:00:25.976Z, 21:00:32.264Z, 21:00:26.548/9Z) vs prior-observ
- NEW api.gladia.io: structural hash (examples-stripped) STABLE at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across all 3 fetches → validated drift baseline replacing byte-hash

## 2026-08-08 10:19:38 UTC
- NEW api.gladia.io /openapi.json: example-timestamp fingerprint varies per fetch (3 distinct values across 3 fetches) — not a stable per-instance indicator
- NEW api.gladia.io: structural hash (examples-stripped) STABLE at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across 3 fetches — validated drift baseline

## 2026-08-08 10:58:11 UTC

## 2026-08-08 11:41:38 UTC
- CHANGED app.gladia.io CSP confirmed: base-uri 'self', object-src 'none', frame-src 'self'+*.gladia.io+billing+svix; NO form-action directive (gap enables unconstrained form-action reflection)

## 2026-08-08 12:03:43 UTC

## 2026-08-08 13:12:56 UTC

## 2026-08-08 14:04:58 UTC

## 2026-08-08 14:50:37 UTC

## 2026-08-08 15:21:19 UTC
