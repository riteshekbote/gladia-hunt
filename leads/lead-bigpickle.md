# LEADS bigpickle (seed)
- 2026-08-07 SEED: no model output yet; pipeline starts on first run.
## 2026-08-07 18:30:55 UTC [api] (model bigpickle)
[NEW] api.gladia.io: OpenAPI 3.1 fully enumerated — 14 paths; every v2 operation declares security scheme `x_gladia_key` (header `x-gladia-key`); `/v1/models` inherits global `security: null` and returns 200 with model+pricing data with no key
[NEW] api.gladia.io: auth gate confirmed — unauthenticated GET on /v2/transcription, /v2/pre-recorded, /v2/live, /v2/transcription/{id} → 401 `{"message":"no gladia key provided","request_id":"G-…"}`
[NEW] api.gladia.io: CORS preflight (OPTIONS, Origin: evil.example.com) → `access-control-allow-origin: *`, `allow-methods: GET,HEAD,PUT,PATCH,POST,DELETE`, `allow-headers: x-gladia-key`, and NO `access-control-allow-credentials`
[NEW] npm `gladia` 0.1.3: registry `description` = "Official TypeScript SDK for Gladia" but packaged README title = "Unofficial TypeScript SDK"; maintainer `softwarecitadel` <softwarecitadel@gmail.com>, author Alexis Bouchez, repo alexisbouchez/gladia.ts (personal), published 2025-03-28 (predates official @gladiaio/sdk 2025-09-09); tarball source benign — only baseUrl api.gladia.io, no eval/exec/exfil
[NEW] app.gladia.io `/signin`: Google-only OAuth; `redirect_to` query param reflected URL-encoded into form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`; post-auth redirect target handling untestable without session
[CHANGED] app.gladia.io return-to cookie re-confirmed: `eyJ1cmwiOiIvIn0=` = unsigned base64url `{"url":"/"}` (plain JSON, NOT a signed JWT); `__sid` expired/empty; both HttpOnly/Secure/SameSite=Lax
[PRIO] api.gladia.io | score 6.35 | attack_surface 6 business 9 tech 8 gate 2 cloud 3 fresh 8 (14 endpoints, SSRF-prone audio_url/video_url ingestion, uniform x-gladia-key gate, /v1/models public)
[PRIO] app.gladia.io /signin | score 5.85 | attack_surface 5 business 7 tech 7 gate 6 cloud 2 fresh 7 (OAuth sign-in, reachable redirect_to param, effect needs post-auth session)
[PRIO] npm `gladia` 0.1.3 | score 5.05 | attack_surface 4 business 5 tech 5 gate 9 cloud 1 fresh 6 (public package, "Official" claim contradicts README, personal maintainer)
[HYP] SSRF via file-URL ingestion in transcription/upload endpoints
class: SSRF
asset: api.gladia.io /v2/upload, /v2/pre-recorded, /v2/transcription, /audio/text/audio-transcription, /video/text/video-transcription (audio_url/video_url params per OpenAPI)
confidence: 58
reasoning: All five endpoints accept audio_url/video_url in spec; server-side fetch of user-supplied URLs is the canonical SSRF class in transcription APIs. Auth gate is a uniform 401 header check (no scope/id binding visible in spec). Public /v1/models shows the stack returns unauthenticated data, so key-holder fetch logic is plausible.
evidence_needed: fetch of an internal address (169.254.169.254 metadata, internal host) reflected/observable via status/error/duration; needs a valid x-gladia-key
verify_steps: AUTH_HELPED — POST /v2/upload with JSON body `{"audio_url":"http://<attacker-canary>"}`, then POST with `http://169.254.169.254/latest/meta-data/`; compare error text/timeouts to detect server-side reachability; only with a program-provided or personal trial key
impact: SSRF → cloud-metadata/internal-network read; High (key-gated)
testability: AUTH_HELPED
[HYP] Post-OAuth open redirect via redirect_to parameter
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 52
reasoning: /signin accepts redirect_to and persists it into the form action; app is Google-only OAuth; unsigned return-to cookie shows the redirect concept is server-driven. If redirect_to is honored post-OAuth without host allowlist, it's an open redirect; if also reused as OAuth redirect_uri, worse.
evidence_needed: after completing OAuth with a session, observe final Location for a cross-origin redirect_to
verify_steps: AUTH_HELPED — complete sign-in flow (HUMAN/session), then GET /signin?redirect_to=https://evil.example.com and observe where the post-auth browser lands; also test redirect_to values like `//evil.example.com` and `https://evil.example.com.evil.io`
impact: phishing/OAuth-flow manipulation; Low-Med (High only if redirect_uri injection proven)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package with false "Official" claim
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 78
reasoning: Registry description claims "Official TypeScript SDK for Gladia" while the package's own README says "Unofficial"; maintainer is a personal gmail (softwarecitadel) and repo is alexisbouchez/gladia.ts; published 5+ months before the real official package @gladiaio/sdk. Tarball code currently benign (no exfil), so this is misrepresentation, not malicious payload.
evidence_needed: none beyond the verified metadata; report as supply-chain hygiene/impersonation (Medium)
verify_steps: PASSIVE — already done (registry metadata + tarball inspection); document description-vs-README contradiction, maintainer mismatch, publish-date ordering
impact: developers installing `gladia` instead of @gladiaio/sdk get unofficial code; if account/repo later hijacked → supply-chain compromise; Medium
testability: PASSIVE
[PARKED] CORS wildcard-with-credentials (seed [55]): dropped — preflight shows `access-control-allow-origin: *` with NO `access-control-allow-credentials`; cross-site requests cannot carry the x-gladia-key header on the victim's behalf; not exploitable
[PARKED] OpenAPI shadow-endpoint enumeration (seed [60]): dropped — 14 documented paths mapped and auth gate is uniform; detecting undocumented endpoints requires active fuzzing, prohibited under passive-first
[PARKED] return-to cookie JWT handling (seed [50]): dropped — cookie proven to be unsigned base64url JSON, not JWT; the redirect surface moved to the redirect_to query param (now H2)
[PARKED] IDOR on /{id}/file download endpoints: dropped — spec-only, confidence < 40, needs a valid key to test cross-account resource isolation
[FINAL] ranked: 1) H1 SSRF @ api.gladia.io (highest-scope asset, real impact if true) | 2) H3 npm impersonation (verified fact, PASSIVE) | 3) H2 open redirect @ app.gladia.io (needs session)
[NEXT] RAG: read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any client-side validation/allowlist, default endpoints, timeout/redirect behavior) to harden H1 before any key-gated testing
[RISK] api.gladia.io: 45 | public OpenAPI (14 paths), uniform key gate, CORS * without credentials (low), audio_url/video_url SSRF surface gated behind keys, request-id headers leak nothing sensitive
[RISK] app.gladia.io: 40 | Google-only OAuth, reachable redirect_to param with unvalidated post-auth behavior, cookies correctly flagged (HttpOnly/Secure/SameSite=Lax)
[RISK] sdk: 50 | `gladia` npm package actively claims "Official" while unofficial (impersonation active); official @gladiaio/sdk metadata clean; tarball of `gladia` benign so far
## 2026-08-07 18:48:44 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/transcription, /v2/upload (audio_url/video_url params per OpenAPI)
confidence: 65
reasoning: Official SDK's create/createUntyped forward audio_url to POST /v2/pre-recorded with no scheme/allowlist check (client-side uploadFile restriction only); /v1/models proves unauthenticated responses exist, so key-gated fetch logic is plausible; datacenters FR/US suggest regional internal nets + metadata service reachable.
evidence_needed: fetch of internal address (169.254.169.254, internal host) reflected via error text/timing/duration on a key-gated request
verify_steps: AUTH_HELPED — POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `http://169.254.169.254/latest/meta-data/`; compare error/duration for reachability signal; key-gated, needs program/trial key
impact: cloud-metadata/internal-network read → High (key-gated)
testability: AUTH_HELPED
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 52
reasoning: redirect_to reflected URL-encoded into the POST form action server-side (verified GET), not stripped/allowlisted client-side; now applies to email/password login path too, widening the trigger surface.
evidence_needed: after a real session, final Location for cross-origin redirect_to (https://evil.example.com, //evil.example.com)
verify_steps: AUTH_HELPED — complete sign-in (session), then submit intent=email-password|google with redirect_to=https://evil.example.com and observe post-auth Location; test `//` and domain-prefix variants
impact: phishing / OAuth-flow manipulation → Low-Med (High only if reused as OAuth redirect_uri)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 78
reasoning: Registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts, published 2025-03-28 before @gladiaio/sdk (2025-09-09); tarball code benign (baseUrl api.gladia.io only).
evidence_needed: none — metadata verified; report as supply-chain hygiene/impersonation (Medium)
verify_steps: PASSIVE — already done (registry metadata + tarball); document description-vs-README contradiction, maintainer mismatch, publish-date ordering
impact: developers installing `gladia` get unofficial code; future account/repo hijack → supply-chain compromise; Medium
testability: PASSIVE
## 2026-08-07 19:17:25 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/upload, legacy /audio/text/audio-transcription + /video/text/video-transcription (audio_url/video_url)
confidence: 70
reasoning: SDK RAG confirms zero client-side validation (audio_url forwarded verbatim; is_url check only in uploadFile helper); OpenAPI spec confirms external-URL fetch is by design; legacy /audio|/video/* endpoints add a second fetch path with NestJS-shaped legacy service; /v1/models proves unauthenticated responses exist, so key-gated fetch logic is real.
evidence_needed: fetch of 169.254.169.254 or internal host reflected via error text/timing/job status on a key-gated request.
verify_steps: AUTH_HELPED — with a valid x-gladia-key: (1) POST /v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` → observe job error_code/timing; (2) same with `http://169.254.169.254/latest/meta-data/`; (3) repeat via /video/text/video-transcription `video_url` to compare legacy-path behavior; compare error/duration for reachability signal.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (verified GET); applies to both email/password and Google OAuth paths; unsigned return-to cookie proves server-driven redirect concept; only post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin redirect_to (https://evil.example.com, //evil.example.com, https://evil.example.com.evil.io).
verify_steps: AUTH_HELPED — complete sign-in (session), submit intent=email-password|google with redirect_to variants, capture post-auth Location and cookie set; escalate only if redirect_to is reused as OAuth redirect_uri.
impact: phishing / OAuth-flow manipulation → Low-Med (High only if redirect_uri injection proven)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 78
reasoning: registry description "Official TypeScript SDK" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts, published 2025-03-28 before @gladiaio/sdk (2025-09-09); tarball benign (baseUrl api.gladia.io only).
evidence_needed: none — metadata verified; report as supply-chain hygiene/impersonation (Medium)
verify_steps: PASSIVE — already done (registry metadata + tarball inspection); document description-vs-README contradiction, maintainer mismatch, publish-date ordering
impact: developers installing `gladia` get unofficial code; account/repo hijack later → supply-chain compromise; Medium
testability: PASSIVE
[NEXT] HUMAN: with a program-provided or personal trial `x-gladia-key`, POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://<attacker-canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; compare job error_code/status/timing for reachability signal; then repeat via https://api.gladia.io/video/text/video-transcription `video_url` to test the legacy fetch path.
