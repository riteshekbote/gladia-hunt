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
