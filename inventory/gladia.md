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
