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

## 2026-08-08 15:53:13 UTC

## 2026-08-08 17:05:52 UTC

## 2026-08-08 17:52:29 UTC

## 2026-08-08 18:18:19 UTC

## 2026-08-08 19:06:08 UTC

## 2026-08-08 19:45:02 UTC
- NEW npm registry: adjacent-namespace squat scan returned all-404 for `gladiaio`, `gladia-sdk`, `gladia-sdk-ts`, `gladiaio-sdk`, `gladia-ts`, `gladia-ai`, `gladia-stt`, `@gladia/sdk`, `@gladia/sdk-js`, `@g
- NEW npm registry: maintainer `softwarecitadel` controls only `@softwarecitadel/girouette` (AdonisJS decorators, unrelated) — no broader squat campaign by that account
- NEW api.gladia.io: surface re-probe byte-identical — openapi 200/125131B, /health 200/15B, /v1/models 200/530B (22nd frozen cycle)

## 2026-08-08 20:12:00 UTC

## 2026-08-08 20:49:54 UTC
- NEW api.gladia.io: OpenAPI 3.1 fully enumerated — 14 paths; every v2 operation declares security scheme `x_gladia_key` (header `x-gladia-key`); `/v1/models` inherits global `security: null` and returns 20
- NEW api.gladia.io: auth gate confirmed — unauthenticated GET on /v2/transcription, /v2/pre-recorded, /v2/live, /v2/transcription/{id} → 401 `{"message":"no gladia key provided","request_id":"G-…"}`
- NEW api.gladia.io: CORS preflight (OPTIONS, Origin: evil.example.com) → `access-control-allow-origin: *`, `allow-methods: GET,HEAD,PUT,PATCH,POST,DELETE`, `allow-headers: x-gladia-key`, and NO `access-con
- NEW npm `gladia` 0.1.3: registry `description` = "Official TypeScript SDK for Gladia" but packaged README title = "Unofficial TypeScript SDK"; maintainer `softwarecitadel` <softwarecitadel@gmail.com>, aut
- NEW app.gladia.io `/signin`: Google-only OAuth; `redirect_to` query param reflected URL-encoded into form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; post-auth redirect target handling 
- CHANGED app.gladia.io return-to cookie re-confirmed: `eyJ1cmwiOiIvIn0=` = unsigned base64url `{"url":"/"}` (plain JSON, NOT a signed JWT); `__sid` expired/empty; both HttpOnly/Secure/SameSite=Lax

## 2026-08-08 21:19:34 UTC

## 2026-08-08 21:52:34 UTC

## 2026-08-08 22:24:48 UTC

## 2026-08-08 22:57:51 UTC
- NEW api.gladia.io: NO_DRIFT across 25+ cycles (23:08→21:52 UTC) — OpenAPI 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface fro
- NEW app.gladia.io: /signin?redirect_to= reflection confirmed alive at 21:52 UTC — form action reflects URL-encoded value; CSP full set re-captured, NO form-action directive (gap confirmed)
- NEW npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) — gladia@0.1.3 is ISOLATED impersonator, no broader campaign
- CHANGED app.gladia.io: /auth/google/callback returns 200 text/html (SPA shell) — OAuth callback path live, expected by design

## 2026-08-08 23:36:12 UTC
- NEW api.gladia.io: OpenAPI 3.1 spec top-level `webhooks` key enumerates 7 outbound webhook topics (transcription.created/success/error + live.start_session/start_recording/end_recording/end_session) — pre
- NEW api.gladia.io: NO_DRIFT 27th cycle (23:33 UTC) — openapi 200/125131B/14 paths (structural sha256 a7fa3286… = normalization baseline), /health 15B, /v1/models 530B FR/US; spec servers=[https://api.glad
- NEW app.gladia.io: /signin?redirect_to=https://evil.example.com → 200, form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com` re-confirmed live 23:33 UTC; CSP full set re-captured — connect-src 
- CHANGED npm: gladia@0.1.3 static — dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", maintainer softwarecitadel@gmail.com, repo alexisbouchez/gladia.ts, shasum cc96f84a… unchanged; @gla

## 2026-08-09 00:03:26 UTC

## 2026-08-09 02:27:06 UTC

## 2026-08-09 04:00:40 UTC

## 2026-08-09 05:15:35 UTC

## 2026-08-09 06:05:04 UTC

## 2026-08-09 07:14:09 UTC

## 2026-08-09 08:05:31 UTC

## 2026-08-09 09:01:30 UTC

## 2026-08-09 09:53:30 UTC

## 2026-08-09 10:28:52 UTC

## 2026-08-09 11:08:07 UTC

## 2026-08-09 11:44:12 UTC

## 2026-08-09 12:17:53 UTC
- NEW app.gladia.io: /auth/google/callback now returns 302 → accounts.google.com (full OAuth initiation with client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, acces
- NEW api.gladia.io: OpenAPI spec `servers` array enumerates single entry https://api.gladia.io only — no staging/alternate host leakage confirmed; example URLs point to generic callback.example + out-of-sc
- NEW app.gladia.io: CSP connect-src includes *.gladia.io + wss://*.gladia.io + *.google.* + hotjar/contentsquare/hubspot/axeptio — infra fingerprint only, no action

## 2026-08-09 13:28:40 UTC
- NEW app.gladia.io: `/auth/google/callback` now returns 302 → accounts.google.com (full OAuth initiation with client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, acc
- NEW api.gladia.io: OpenAPI spec `servers` array enumerates single entry https://api.gladia.io only — no staging/alternate host leakage confirmed; example URLs point to generic callback.example + out-of-sc
- NEW app.gladia.io: CSP connect-src includes *.gladia.io + wss://*.gladia.io + *.google.* + hotjar/contentsquare/hubspot/axeptio — infra fingerprint only, no action
- CHANGED npm registry: `gladia@0.1.3` individual version endpoint returns 404 but package listing shows dist-tag latest=0.1.3 stable with shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (

## 2026-08-09 14:13:40 UTC
- NEW app.gladia.io: `/auth/google/callback` now returns 302 → accounts.google.com (full OAuth initiation with client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, acc
- NEW api.gladia.io: OpenAPI spec `servers` array enumerates single entry https://api.gladia.io only — no staging/alternate host leakage confirmed; example URLs point to generic callback.example + out-of-sc
- NEW app.gladia.io: CSP connect-src includes *.gladia.io + wss://*.gladia.io + *.google.* + hotjar/contentsquare/hubspot/axeptio — infra fingerprint only, no action
- CHANGED npm registry: `gladia@0.1.3` individual version endpoint returns 404 but package listing shows dist-tag latest=0.1.3 stable with shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (

## 2026-08-09 14:59:06 UTC
- NEW app.gladia.io: `/auth/google/callback` now returns 302 → accounts.google.com (full OAuth initiation with client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, acc
- NEW api.gladia.io: OpenAPI spec `servers` array enumerates single entry https://api.gladia.io only — no staging/alternate host leakage confirmed; example URLs point to generic callback.example + out-of-sc
- NEW app.gladia.io: CSP connect-src includes *.gladia.io + wss://*.gladia.io + *.google.* + hotjar/contentsquare/hubspot/axeptio — infra fingerprint only, no action
- CHANGED npm registry: `gladia@0.1.3` package listing shows dist-tag latest=0.1.3 stable with shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.js

## 2026-08-09 15:33:08 UTC

## 2026-08-09 16:04:13 UTC
- NEW app.gladia.io: `/auth/google/callback` now returns 302 → accounts.google.com with full OAuth initiation (client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, acc
- NEW app.gladia.io: CSP connect-src includes *.gladia.io + wss://*.gladia.io + *.google.* + hotjar/contentsquare/hubspot/axeptio — infra fingerprint only
- CHANGED npm registry: `gladia@0.1.3` dist-tag latest=0.1.3 stable, shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), README "Unofficial" vs package.json "Official" contradictio
- NEW api.gladia.io: OpenAPI spec `servers` array enumerates single entry https://api.gladia.io only — no staging/alternate host leakage; example URLs point to generic callback.example + out-of-scope files.

## 2026-08-09 16:53:50 UTC
- NEW None — surface frozen since 23:08 UTC (41+ NO_DRIFT cycles)
- CHANGED None — all observations re-confirmed byte-identical; npm `gladia@0.1.3` dist-tag/shasum/repo/user static

## 2026-08-09 17:25:48 UTC
- NEW NO_DELTA

## 2026-08-09 18:04:15 UTC

## 2026-08-09 18:58:02 UTC

## 2026-08-09 19:42:44 UTC

## 2026-08-09 20:05:14 UTC

## 2026-08-09 20:51:42 UTC

## 2026-08-09 21:38:12 UTC

## 2026-08-09 22:01:31 UTC

## 2026-08-09 22:41:42 UTC
- NEW app.gladia.io: /auth/google/callback now returns 302 → accounts.google.com (full OAuth initiation with client_id=352060113328-fnk8shoffbkh10imc3adc5lllclv21ha.apps.googleusercontent.com, PKCE S256, fi
- CHANGED npm registry: gladia@0.1.3 dist-tag latest=0.1.3 stable, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9 unchanged, repo alexisbouchez/gladia.ts + user alexisbouchez both 404 (orphaned), package.json 

## 2026-08-09 23:08:05 UTC

## 2026-08-09 23:47:02 UTC

## 2026-08-10 00:40:41 UTC

## 2026-08-10 03:06:26 UTC

## 2026-08-10 04:50:07 UTC

## 2026-08-10 06:23:21 UTC

## 2026-08-10 08:06:57 UTC

## 2026-08-10 09:49:22 UTC
- NEW api.gladia.io: OpenAPI 3.1 fully enumerated — 14 paths; every v2 operation declares security scheme `x_gladia_key` (header `x-gladia-key`); `/v1/models` inherits global `security: null` and returns 20
- NEW api.gladia.io: auth gate confirmed — unauthenticated GET on /v2/transcription, /v2/pre-recorded, /v2/live, /v2/transcription/{id} → 401 `{"message":"no gladia key provided","request_id":"G-…"}`
- NEW api.gladia.io: CORS preflight (OPTIONS, Origin: evil.example.com) → `access-control-allow-origin: *`, `allow-methods: GET,HEAD,PUT,PATCH,POST,DELETE`, `allow-headers: x-gladia-key`, and NO `access-con
- NEW npm `gladia` 0.1.3: registry `description` = "Official TypeScript SDK for Gladia" but packaged README title = "Unofficial TypeScript SDK"; maintainer `softwarecitadel` <softwarecitadel@gmail.com>, aut
- NEW app.gladia.io `/signin`: Google-only OAuth; `redirect_to` query param reflected URL-encoded into form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; post-auth redirect target handling 
- CHANGED app.gladia.io return-to cookie re-confirmed: `eyJ1cmwiOiIvIn0=` = unsigned base64url `{"url":"/"}` (plain JSON, NOT a signed JWT); `__sid` expired/empty; both HttpOnly/Secure/SameSite=Lax

## 2026-08-10 10:54:23 UTC

## 2026-08-10 11:45:54 UTC

## 2026-08-10 12:41:01 UTC

## 2026-08-10 14:08:36 UTC
- NEW npm `gladia@0.1.3` tarball `package/src/client.ts:307` confirms `wsUrl.searchParams.append('x-gladia-key', this.apiKey)` → `new WebSocket(wsUrl.toString())` — key leaked into wss:// URL query at runti
- NEW api.gladia.io OpenAPI `webhooks` key confirmed (7 topics: transcription.{created,success,error}, live.{start_session,start_recording,end_recording,end_session}) — all POST to client-supplied URLs, `fo
- NEW api.gladia.io POST /v2/pre-recorded (no key) → 401 `{"message":"no gladia key provided","request_id":"…"}` NestJS HttpException shape confirmed fresh (timestamp 2026-08-10T14:xx UTC)
- NEW app.gladia.io /signin?redirect_to=https://evil.example.com → 200, CSP captured full set, `0 form-action directives` confirmed (grep-count=0)
- NEW app.gladia.io /auth/google/callback (no params) → 302 → accounts.google.com full OAuth 2.0 PKCE S256 init (client_id, fixed redirect_uri, code_challenge, state) confirmed

## 2026-08-10 15:21:16 UTC
- NEW npm `gladia@0.1.3` tarball `package/src/client.ts:307` confirms `wsUrl.searchParams.append('x-gladia-key', this.apiKey)` → `new WebSocket(wsUrl.toString())` — API key leaked into wss:// URL query at r
- NEW api.gladia.io OpenAPI `webhooks` key confirmed (7 topics: transcription.{created,success,error}, live.{start_session,start_recording,end_recording,end_session}) — all POST to client-supplied URLs, `fo
- NEW api.gladia.io POST /v2/pre-recorded (no key) → 401 `{"message":"no gladia key provided","request_id":"…"}` NestJS HttpException shape confirmed fresh (timestamp 2026-08-10T14:xx UTC)
- NEW app.gladia.io /signin?redirect_to=https://evil.example.com → 200, CSP captured full set, `0 form-action directives` confirmed (grep-count=0)
- NEW app.gladia.io /auth/google/callback (no params) → 302 → accounts.google.com full OAuth 2.0 PKCE S256 init (client_id, fixed redirect_uri, code_challenge, state) confirmed

## 2026-08-10 16:16:07 UTC

## 2026-08-10 17:16:05 UTC

## 2026-08-10 18:17:03 UTC

## 2026-08-10 19:18:43 UTC
- NEW npm `gladia@0.1.3`: local `npm pack gladia@0.1.3` reproduced independently — tarball sha256 `3b23ec7d…7f2`, `package/src/client.ts:307` `wsUrl.searchParams.append('x-gladia-key', this.apiKey)` + `:318

## 2026-08-10 20:08:26 UTC
- NEW npm `gladia@0.1.3`: local `npm pack` reproduced independently — tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` verified; `src/client.ts:307` `wsUrl.searchParams.appe

## 2026-08-10 21:01:57 UTC
- NEW None — all surfaces match prior cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks frozen, app.gladia.io signin reflection + CSP gap confirmed, npm gladia@0.1.3 orphaned at latest with repo+use

## 2026-08-10 22:01:55 UTC
- NEW None — all surfaces match prior cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks frozen, app.gladia.io signin reflection + CSP gap confirmed, npm gladia@0.1.3 orphaned at latest with repo+use

## 2026-08-10 22:38:09 UTC

## 2026-08-10 23:18:54 UTC

## 2026-08-10 23:59:00 UTC

## 2026-08-11 02:13:06 UTC

## 2026-08-11 04:13:31 UTC

## 2026-08-11 05:32:28 UTC

## 2026-08-11 06:11:56 UTC

## 2026-08-11 07:41:23 UTC

## 2026-08-11 08:40:57 UTC

## 2026-08-11 09:44:28 UTC

## 2026-08-11 10:38:19 UTC
- NEW None since 09:43 UTC — surface remains frozen across all targets (80+ drift-negative cycles on api.gladia.io, byte-fresh signin reflection on app.gladia.io, static orphaned impersonation on npm)

## 2026-08-11 11:32:55 UTC

## 2026-08-11 12:44:23 UTC
- NEW None — all surfaces frozen (api.gladia.io openapi.json 125131B/14 paths/7 webhooks etag W/"1e8cb-...", app.gladia.io signin reflection + CSP gap byte-identical, npm gladia@0.1.3 shasum cc96f84a... unc

## 2026-08-11 14:00:51 UTC

## 2026-08-11 15:12:29 UTC
- NEW NO_DELTA — all surfaces frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io signin redirect_to reflection + CSP gap byte-identical;

## 2026-08-11 16:14:16 UTC
- NEW NO_DELTA — all surfaces frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io signin redirect_to reflection + CSP gap byte-identical;

## 2026-08-11 17:17:10 UTC

## 2026-08-11 18:13:44 UTC

## 2026-08-11 19:29:47 UTC

## 2026-08-11 20:13:39 UTC
- NEW None — all surfaces frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io signin redirect_to reflection + CSP gap byte-identical; npm
- NEW None — all surfaces frozen across 80+ drift-negative cycles.
- CHANGED None.

## 2026-08-11 21:09:21 UTC
- NEW None — all surfaces frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io signin redirect_to reflection + CSP gap byte-identical; npm

## 2026-08-11 22:05:24 UTC

## 2026-08-11 23:03:40 UTC
- CHANGED gladia.io/bug-bounty-report → 301 → www.gladia.io/bug-bounty-report → 302 → `https://docs.google.com/forms/d/1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI/viewform` (Google Forms, auth-gated via Google

## 2026-08-11 23:54:36 UTC
- NEW gladia.io/bug-bounty-report redirects 301→www.gladia.io/bug-bounty-report→302→Google Forms (https://docs.google.com/forms/d/1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI/viewform) — auth-gated via Goog
- CHANGED gladia.io/bug-bounty-report → 301 → www.gladia.io/bug-bounty-report → 302 → Google Forms `1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI` (auth-gated via Google, third-party out of scope) — submission c
- CHANGED gladia.io/bug-bounty-report → 301 → www.gladia.io/bug-bounty-report → 302 → `https://docs.google.com/forms/d/1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI/viewform` (Google Forms, auth-gated via Google

## 2026-08-12 01:47:46 UTC
- NEW gladia.io/bug-bounty-report redirects 301→www.gladia.io/bug-bounty-report→302→Google Forms (https://docs.google.com/forms/d/1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI/viewform) — auth-gated via Goog
- CHANGED gladia.io/bug-bounty-report submission channel fully mapped (301→www→302→Google Forms); no new in-scope surface, delivery path for locked report confirmed

## 2026-08-12 04:01:18 UTC
- NEW gladia.io/bug-bounty-report redirects 301→www.gladia.io/bug-bounty-report→302→Google Forms (https://docs.google.com/forms/d/1RiodROQSx9f7r_parjnEDqz6k_N7oZBvcgZ8scPrRgI/viewform) — auth-gated via Goog
- CHANGED gladia.io/bug-bounty-report submission channel fully mapped (301→www→302→Google Forms); no new in-scope surface, delivery path for locked report confirmed
- NEW None — surface frozen across 80+ cycles on all targets; no class newly proven dead or alive.
- CHANGED None — all observations re-confirmed byte-fresh this cycle: api.gladia.io openapi 125131B/CORS `*`/401 NestJS/x-powered-by Express (OPTIONS-only); app.gladia.io /signin form-action reflection + CSP 0 
- NEW None — surface frozen across 80+ cycles on all targets; no class newly proven dead or alive.
- CHANGED None — all observations re-confirmed byte-fresh this cycle: api.gladia.io openapi 125131B/CORS `*`/401 NestJS/x-powered-by Express (OPTIONS-only); app.gladia.io /signin form-action reflection + CSP 0 
- NEW None — surface frozen across 80+ cycles on all targets; no class newly proven dead or alive.
- CHANGED None — all observations re-confirmed byte-fresh this cycle.

## 2026-08-12 05:30:10 UTC

## 2026-08-12 06:56:33 UTC
- NEW None — surface frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io /signin redirect_to reflection + CSP gap byte-identical; npm gla

## 2026-08-12 08:24:49 UTC
- NEW None — surface frozen across 80+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io /signin redirect_to reflection + CSP gap byte-identical; npm gla

## 2026-08-12 09:45:37 UTC

## 2026-08-12 10:48:00 UTC
- NEW None — surface frozen across 90+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io /signin redirect_to reflection + CSP gap byte-identical; npm gla

## 2026-08-12 11:37:45 UTC

## 2026-08-12 12:36:36 UTC

## 2026-08-12 14:07:38 UTC

## 2026-08-12 15:15:18 UTC
- NEW None — all surfaces frozen across 90+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io /signin redirect_to reflection + CSP 0 form-action directiv
- CHANGED None — all observations re-confirmed byte-fresh this cycle

## 2026-08-12 16:29:58 UTC

## 2026-08-12 17:17:48 UTC

## 2026-08-12 18:15:37 UTC

## 2026-08-12 19:36:46 UTC

## 2026-08-12 20:24:09 UTC

## 2026-08-12 21:11:56 UTC
- NEW None — surface frozen across 90+ cycles (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app.gladia.io /signin redirect_to reflection + CSP 0 form-action; npm gladia@0
- CHANGED None — all observations re-confirmed byte-fresh this cycle; no new endpoints, headers, or npm metadata changes

## 2026-08-12 22:06:38 UTC

## 2026-08-12 23:00:40 UTC

## 2026-08-13 00:00:36 UTC

## 2026-08-13 01:56:33 UTC

## 2026-08-13 04:09:46 UTC
- NEW None — surface frozen across 80+ cycles on all targets (api openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B; app /signin redirect_to reflection + CSP gap byte-identical; npm gladia@0
- CHANGED None — all observations re-confirmed byte-fresh this cycle.

## 2026-08-13 05:46:06 UTC

## 2026-08-13 07:17:23 UTC

## 2026-08-13 08:43:40 UTC

## 2026-08-13 09:50:39 UTC

## 2026-08-13 10:56:25 UTC

## 2026-08-13 11:52:29 UTC

## 2026-08-13 12:34:12 UTC

## 2026-08-13 14:14:20 UTC

## 2026-08-13 15:19:59 UTC

## 2026-08-13 16:30:32 UTC

## 2026-08-13 17:22:21 UTC

## 2026-08-13 18:14:29 UTC

## 2026-08-13 19:32:45 UTC

## 2026-08-13 20:08:36 UTC

## 2026-08-13 21:06:12 UTC

## 2026-08-13 21:59:54 UTC

## 2026-08-13 22:58:45 UTC

## 2026-08-13 23:45:11 UTC

## 2026-08-14 00:46:13 UTC

## 2026-08-14 03:18:00 UTC

## 2026-08-14 05:19:07 UTC

## 2026-08-14 06:45:34 UTC

## 2026-08-14 08:07:50 UTC

## 2026-08-14 09:21:16 UTC

## 2026-08-14 10:31:22 UTC

## 2026-08-14 11:24:52 UTC

## 2026-08-14 12:11:04 UTC

## 2026-08-14 13:44:47 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → 12:11 2026-08-14 UTC).

## 2026-08-14 14:43:25 UTC

## 2026-08-14 15:37:39 UTC

## 2026-08-14 16:32:49 UTC

## 2026-08-14 17:39:21 UTC

## 2026-08-14 18:33:34 UTC

## 2026-08-14 19:35:21 UTC

## 2026-08-14 20:13:52 UTC

## 2026-08-14 20:46:41 UTC
- CHANGED 2026-08-14 20:13:52 UTC inventory timestamp registered; all prior knowledge + leads carried forward.
- CHANGED npm `gladia@0.1.3` confirmation block now references two local `npm pack` reproductions (18:17 + 20:08 UTC) of sha256 `3b23ec7d…7f2` — strengthens reproducibility claim.
- CHANGED `/auth/google/callback` confirmed as full OAuth 2.0 PKCE S256 initiation (302→accounts.google.com with client_id `3520…21ha`, FIXED redirect_uri, code_challenge S256, random state) — was earlier 200 S
- CHANGED oauth2 state cookie now observed as `oauth2:<uuid>` (per-request fresh UUID naming) with `HttpOnly; SameSite=Lax` but missing `Secure` flag (HSTS preload mitigates→informational).
- NEW `/api/v1/*` SPA catch-all endpoints (/api/v1/me, /api/v1/transcriptions, /api/v1/apikeys, /api/health) confirmed returning 200 text/html (no real authenticated API at unauth layer) — client-side enfor

## 2026-08-14 21:14:33 UTC
- NEW `/api/v1/*` SPA catch-all endpoints (/api/v1/me, /api/v1/transcriptions, /api/v1/apikeys, /api/health) confirmed returning 200 text/html — no real authenticated API at unauth layer, client-side enforc
- CHANGED `/auth/google/callback` confirmed as full OAuth 2.0 PKCE S256 initiation (302→accounts.google.com with client_id `3520…21ha`, FIXED redirect_uri, code_challenge S256, random state) — previously observ
- CHANGED oauth2 state cookie now observed as `oauth2:<uuid>` (per-request fresh UUID naming) with `HttpOnly; SameSite=Lax` but missing `Secure` flag (HSTS preload mitigates→informational)
- CHANGED npm `gladia@0.1.3` confirmation block now references two local `npm pack` reproductions (18:17 + 20:08 UTC) of sha256 `3b23ec7d…7f2` — strengthens reproducibility claim
- CHANGED npm `gladia@0.1.3` orphaned impersonation confirmation now references TWO independent local `npm pack` reproductions (both yielding sha256 `3b23ec7d…7f2`) at 20:08 + 21:12 UTC this cycle — strengthens
- CHANGED `/auth/google/callback` (app.gladia.io) confirmed as full OAuth 2.0 PKCE S256 initiation at 21:12 UTC (302→accounts.google.com with client_id `3520…21ha`, FIXED redirect_uri, code_challenge S256, rand
- CHANGED oauth2 state cookie naming now explicitly recorded as `oauth2:<uuid>` (per-request fresh UUID) with `HttpOnly; SameSite=Lax` but missing `Secure` flag confirmed this cycle at 21:12 UTC.
- NEW /api/v1/* SPA catch-all endpoints (/api/v1/me, /api/v1/transcriptions, /api/v1/apikeys, /api/health) confirmed returning 200 text/html at 21:12 UTC — client-side enforcement only, no real authenticate

## 2026-08-14 21:44:55 UTC

## 2026-08-14 22:03:16 UTC

## 2026-08-14 22:36:51 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → current 2026-08-14 UTC); all targets byte-identical to prior cycles

## 2026-08-14 23:02:53 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → current 2026-08-14 UTC); all targets byte-identical to prior cycles

## 2026-08-14 23:32:26 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → current 2026-08-14 UTC); all targets byte-identical to prior cycles

## 2026-08-14 23:57:51 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → current 2026-08-14 UTC); all targets byte-identical to prior cycles

## 2026-08-15 01:38:31 UTC

## 2026-08-15 02:39:41 UTC

## 2026-08-15 03:25:18 UTC

## 2026-08-15 04:06:12 UTC

## 2026-08-15 04:46:20 UTC

## 2026-08-15 05:12:44 UTC

## 2026-08-15 05:45:11 UTC

## 2026-08-15 06:04:42 UTC

## 2026-08-15 07:01:36 UTC
- NEW None — all targets byte-identical to prior cycles (90+ NO_DRIFT confirmed)

## 2026-08-15 07:35:39 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (23:08 2026-08-07 → current); all targets byte-identical

## 2026-08-15 07:59:08 UTC

## 2026-08-15 08:57:25 UTC

## 2026-08-15 09:07:27 UTC

## 2026-08-15 09:37:41 UTC

## 2026-08-15 09:59:18 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 09:37 UTC); all targets byte-identical to prior cycles

## 2026-08-15 10:32:31 UTC

## 2026-08-15 10:57:02 UTC

## 2026-08-15 11:26:31 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 11:24 UTC); all targets byte-identical to prior cycles

## 2026-08-15 11:47:30 UTC

## 2026-08-15 12:03:29 UTC

## 2026-08-15 12:57:10 UTC

## 2026-08-15 13:36:18 UTC

## 2026-08-15 13:58:27 UTC

## 2026-08-15 14:33:05 UTC

## 2026-08-15 14:56:14 UTC

## 2026-08-15 15:27:22 UTC

## 2026-08-15 15:50:35 UTC

## 2026-08-15 16:10:21 UTC

## 2026-08-15 16:42:49 UTC

## 2026-08-15 17:04:38 UTC

## 2026-08-15 17:33:38 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 17:04 UTC); all targets byte-identical to prior cycles

## 2026-08-15 17:55:31 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 17:04 UTC); all targets byte-identical to prior cycles

## 2026-08-15 18:32:52 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 17:55 UTC); all targets byte-identical to prior cycles
- NEW NO_DELTA — surface frozen across 90+ cycles; all targets byte-identical to 2026-08-15 17:55 UTC baseline (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection, n

## 2026-08-15 19:01:53 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 18:32 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, si

## 2026-08-15 19:31:16 UTC

## 2026-08-15 19:51:30 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 19:31 UTC); all targets byte-identical to prior cycles

## 2026-08-15 20:12:23 UTC

## 2026-08-15 20:42:18 UTC

## 2026-08-15 21:03:02 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 20:42 UTC); all targets byte-identical to prior cycles

## 2026-08-15 21:33:43 UTC

## 2026-08-15 21:54:17 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 21:33 UTC); all targets byte-identical to prior cycles

## 2026-08-15 22:20:30 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 21:54 UTC); all targets byte-identical to prior cycles

## 2026-08-15 22:44:37 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 22:20 UTC); all targets byte-identical to prior cycles

## 2026-08-15 23:03:03 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 22:44 UTC); all targets byte-identical to prior cycles

## 2026-08-15 23:32:39 UTC

## 2026-08-15 23:53:09 UTC

## 2026-08-16 01:06:52 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 23:53 UTC); all targets byte-identical to prior cycles

## 2026-08-16 02:35:07 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 23:53 UTC); all targets byte-identical to prior cycles

## 2026-08-16 03:32:59 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-15 23:53 UTC); all targets byte-identical to prior cycles

## 2026-08-16 04:20:03 UTC

## 2026-08-16 04:56:28 UTC

## 2026-08-16 05:33:13 UTC

## 2026-08-16 05:59:54 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 05:58 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin

## 2026-08-16 06:55:12 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 05:58 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin

## 2026-08-16 07:35:16 UTC

## 2026-08-16 07:57:37 UTC

## 2026-08-16 08:40:00 UTC

## 2026-08-16 09:05:14 UTC

## 2026-08-16 09:39:07 UTC

## 2026-08-16 10:00:39 UTC

## 2026-08-16 10:34:34 UTC
- NEW None — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 10:00 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin

## 2026-08-16 10:57:48 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 10:34 UTC); all targets byte-identical to prior cycles

## 2026-08-16 11:26:50 UTC

## 2026-08-16 11:51:03 UTC

## 2026-08-16 12:13:54 UTC

## 2026-08-16 13:05:03 UTC

## 2026-08-16 13:43:03 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 13:05 UTC); all targets byte-identical to prior cycles

## 2026-08-16 14:03:46 UTC

## 2026-08-16 14:35:57 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 14:03 UTC); all targets byte-identical to prior cycles

## 2026-08-16 14:59:14 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 14:35 UTC); all targets byte-identical to prior cycles

## 2026-08-16 15:32:30 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 14:59 UTC); all targets byte-identical to prior cycles

## 2026-08-16 15:55:17 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 14:59 UTC); all targets byte-identical to prior cycles

## 2026-08-16 16:23:06 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 15:55 UTC); all targets byte-identical to prior cycles

## 2026-08-16 16:50:03 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 15:55 UTC); all targets byte-identical to prior cycles

## 2026-08-16 17:11:10 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 15:55 UTC); all targets byte-identical to prior cycles

## 2026-08-16 17:35:50 UTC

## 2026-08-16 17:54:51 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 15:55 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, si

## 2026-08-16 18:30:06 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 18:28 UTC); all targets byte-identical to prior cycles (openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, si

## 2026-08-16 19:01:14 UTC

## 2026-08-16 19:29:36 UTC

## 2026-08-16 19:50:36 UTC

## 2026-08-16 20:09:41 UTC
- NEW NO_DELTA — surface frozen across 90+ cycles (2026-08-07 23:08 → 2026-08-16 20:07 UTC); all targets byte-identical to prior cycles

## 2026-08-16 20:40:05 UTC

## 2026-08-16 20:59:07 UTC

## 2026-08-16 21:30:36 UTC

## 2026-08-16 21:51:58 UTC

## 2026-08-16 22:12:21 UTC

## 2026-08-16 22:40:28 UTC

## 2026-08-16 22:59:43 UTC

## 2026-08-16 23:30:42 UTC

## 2026-08-16 23:52:40 UTC

## 2026-08-17 00:50:21 UTC

## 2026-08-17 02:12:09 UTC

## 2026-08-17 03:16:23 UTC

## 2026-08-17 04:08:56 UTC

## 2026-08-17 04:58:45 UTC

## 2026-08-17 05:53:23 UTC

## 2026-08-17 06:25:28 UTC

## 2026-08-17 07:33:02 UTC

## 2026-08-17 08:22:44 UTC

## 2026-08-17 09:10:16 UTC

## 2026-08-17 09:58:53 UTC

## 2026-08-17 10:41:20 UTC

## 2026-08-17 11:12:23 UTC

## 2026-08-17 11:38:08 UTC

## 2026-08-17 12:01:14 UTC

## 2026-08-17 13:04:47 UTC

## 2026-08-17 13:52:25 UTC

## 2026-08-17 14:21:37 UTC

## 2026-08-17 15:18:05 UTC

## 2026-08-17 15:47:37 UTC

## 2026-08-17 16:12:31 UTC

## 2026-08-17 16:49:02 UTC

## 2026-08-17 17:16:16 UTC

## 2026-08-17 17:51:35 UTC

## 2026-08-17 18:23:13 UTC

## 2026-08-17 19:09:12 UTC

## 2026-08-17 19:42:28 UTC

## 2026-08-17 20:04:42 UTC

## 2026-08-17 20:40:10 UTC

## 2026-08-17 21:09:13 UTC
- NEW None — surface frozen across 100+ drift-negative cycles (api.gladia.io OpenAPI 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, preflight-only x-powered-by, CORS static `*`; app.gladia.io /s

## 2026-08-17 21:39:50 UTC

## 2026-08-17 22:02:49 UTC

## 2026-08-17 22:38:57 UTC

## 2026-08-17 23:00:26 UTC

## 2026-08-17 23:32:36 UTC

## 2026-08-17 23:54:56 UTC

## 2026-08-18 01:16:57 UTC

## 2026-08-18 02:33:54 UTC
- NEW api.gladia.io: `/v2/live/health` — undocumented endpoint returning 401 NestJS `{"statusCode":401,"path":"/v2/live/health","message":"no gladia key provided"}` — NOT in OpenAPI spec (14 paths confirmed
- CHANGED api.gladia.io: OpenAPI size now 132834B (was 125131B) — the spec itself grew ~7.7KB; paths still 14. Need to check if structural content changed or just example timestamps.

## 2026-08-18 03:26:56 UTC
- NEW api.gladia.io: `/v2/live/health` — undocumented endpoint returning 401 NestJS `{"statusCode":401,"path":"/v2/live/health","message":"no gladia key provided"}` — NOT in OpenAPI spec (14 paths confirmed
- CHANGED api.gladia.io: OpenAPI size now 132834B (was 125131B) — the spec itself grew ~7.7KB; paths still 14. Need to check if structural content changed or just example timestamps.
- CHANGED api.gladia.io: OpenAPI spec grew from 125131B to 132834B (~7.7KB increase); paths still 14. Need to verify if structural content changed or just example timestamp drift.
- NEW api.gladia.io: `/v2/live/health` undocumented key-gated endpoint (401 NestJS, not in prior 14-path OpenAPI spec) — discovered in last cycle, informational only.

## 2026-08-18 04:13:47 UTC

## 2026-08-18 04:55:06 UTC
- NEW api.gladia.io: `/v2/live/health` — undocumented endpoint returning 401 NestJS `{"statusCode":401,"path":"/v2/live/health","message":"no gladia key provided"}` — NOT in OpenAPI spec (14 paths confirmed

## 2026-08-18 05:30:50 UTC
- NEW api.gladia.io: `/v2/live/health` — undocumented endpoint returning 401 NestJS `{"statusCode":401,"path":"/v2/live/health","message":"no gladia key provided"}` — NOT in OpenAPI spec (14 paths confirmed
- CHANGED None — OpenAPI size change to 132834B contradicted by fresh probes confirming 125131B; inventory entry was stale

## 2026-08-18 05:59:51 UTC

## 2026-08-18 07:00:05 UTC

## 2026-08-18 07:49:39 UTC

## 2026-08-18 08:20:17 UTC

## 2026-08-18 09:03:18 UTC

## 2026-08-18 09:46:35 UTC

## 2026-08-18 10:17:16 UTC

## 2026-08-18 10:51:54 UTC

## 2026-08-18 11:17:00 UTC

## 2026-08-18 11:47:46 UTC

## 2026-08-18 12:23:35 UTC

## 2026-08-18 13:18:23 UTC

## 2026-08-18 14:03:24 UTC

## 2026-08-18 14:50:04 UTC

## 2026-08-18 15:22:04 UTC

## 2026-08-18 15:56:04 UTC

## 2026-08-18 16:32:27 UTC

## 2026-08-18 17:02:58 UTC

## 2026-08-18 17:39:09 UTC

## 2026-08-18 18:05:13 UTC

## 2026-08-18 18:55:57 UTC
- NEW api.gladia.io: `/v2/live/health` undocumented key-gated endpoint (401 NestJS, not in OpenAPI 14-path spec) — discovered 2026-08-18, informational only

## 2026-08-18 19:28:03 UTC
- NEW api.gladia.io: `/v2/live/health` undocumented key-gated endpoint (401 NestJS, not in OpenAPI 14-path spec) — discovered 2026-08-18, informational only

## 2026-08-18 19:52:59 UTC

## 2026-08-18 20:21:09 UTC
- NEW api.gladia.io: `/v2/live/health` — undocumented key-gated endpoint returning 401 NestJS `{"statusCode":401,"path":"/v2/live/health","message":"no gladia key provided"}` — NOT in OpenAPI spec (14 paths
- CHANGED None — OpenAPI size remains 125131B; "132834B" inventory entry was stale/erroneous

## 2026-08-18 20:45:41 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles; all targets identical to prior probes

## 2026-08-18 21:07:51 UTC

## 2026-08-18 21:38:50 UTC

## 2026-08-18 22:00:27 UTC

## 2026-08-18 22:35:49 UTC

## 2026-08-18 22:59:37 UTC

## 2026-08-18 23:31:31 UTC

## 2026-08-18 23:54:15 UTC

## 2026-08-19 01:06:34 UTC

## 2026-08-19 02:24:35 UTC

## 2026-08-19 03:28:13 UTC

## 2026-08-19 04:11:30 UTC

## 2026-08-19 04:54:34 UTC

## 2026-08-19 05:28:37 UTC

## 2026-08-19 05:59:58 UTC
- NEW api.gladia.io: `/v2/live/health` undocumented key-gated endpoint (401 NestJS, not in OpenAPI spec) — informational only, properly gated
- CHANGED npm `gladia@0.1.3` evidence package: 5+ independent local `npm pack` reproductions confirm sha256 `3b23ec7d…7f2` + shasum `cc96f84a…`, src/client.ts:306-308 (`searchParams.append('x-gladia-key', apiKe

## 2026-08-19 07:02:14 UTC

## 2026-08-19 07:51:02 UTC

## 2026-08-19 08:22:26 UTC

## 2026-08-19 09:06:05 UTC

## 2026-08-19 09:48:38 UTC

## 2026-08-19 10:14:51 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 10:51:34 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 11:20:17 UTC

## 2026-08-19 11:47:12 UTC

## 2026-08-19 12:18:30 UTC

## 2026-08-19 13:20:40 UTC

## 2026-08-19 14:04:02 UTC
- NEW (none)
- CHANGED (none)

## 2026-08-19 14:50:12 UTC
- NEW None
- CHANGED None
- NEW (none)
- CHANGED (none)

## 2026-08-19 15:20:20 UTC

## 2026-08-19 15:57:06 UTC

## 2026-08-19 16:32:13 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 17:00:44 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 17:37:04 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 18:06:13 UTC

## 2026-08-19 18:49:07 UTC

## 2026-08-19 19:18:40 UTC

## 2026-08-19 19:51:11 UTC

## 2026-08-19 20:08:00 UTC

## 2026-08-19 20:43:08 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 21:20:17 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets
- CHANGED openapi.json byte-size 125131B→125680B (fresh probe 2026-08-19) — REJECTED as surface drift: structural identity preserved (14 paths, 7 webhooks, 1 server `https://api.gladia.io`), etag rotates via 36

## 2026-08-19 21:47:43 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 22:06:01 UTC
- NEW None — surface byte-frozen across 100+ drift-negative cycles on all targets (api.gladia.io openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B, signin 27448B reflection + CSP 0 form-acti
- CHANGED None — all ACCEPTED findings remain alive, all REJECTED classes remain dead; no new surface items discovered

## 2026-08-19 22:41:48 UTC
