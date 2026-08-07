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
## 2026-08-07 20:00:00 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: Spec exposes audio_url + CallbackConfigDto.url with no scheme/allowlist in schema; official SDK forwards audio_url verbatim and docs confirm external-URL fetch by design; docs troubleshooting tells users "callback_url not localhost", implying internal targets considered reachable unless server-side-blocked; jobs return status/error_message/timing giving a measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare error_message/status/duration; (2) same via /video/text/video-transcription video_url (legacy path); (3) POST with {"callback":{"url":"http://169.254.169.254:80/"}} to test outbound POST surface; include localhost/file:// variants.
impact: cloud-metadata + internal-network read (and internal POST via callback) from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; 0.1.3 published 2025-04-07, pre-dating @gladiaio/sdk (2025-09-09); re-verified this session; tarball code benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field)
impact: developers installing `gladia` run unofficial code; future account/repo hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (verified GET) across email/password and Google paths; unsigned return-to cookie proves server-driven redirect; post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin variants (https://evil.example.com, //evil.example.com)
verify_steps: AUTH_HELPED — complete sign-in then submit redirect_to=https://evil.example.com; capture post-auth Location; escalate only if reused as OAuth redirect_uri
impact: phishing/OAuth-flow manipulation → Low-Med
testability: AUTH_HELPED
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}` and compare `status`/`error_message`/duration; repeat with `video_url` on /video/text/video-transcription, then with `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe the outbound POST surface.
## 2026-08-07 20:54:19 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: Spec exposes audio_url + CallbackConfigDto.url with no scheme/allowlist in schema; official SDK forwards audio_url verbatim and docs confirm external-URL fetch by design; docs troubleshooting tells users "callback_url not localhost", implying internal targets considered reachable unless server-side-blocked; jobs return status/error_message/timing giving a measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare error_message/status/duration; (2) same via /video/text/video-transcription video_url (legacy path); (3) POST with {"callback":{"url":"http://169.254.169.254:80/"}} to test outbound POST surface; include localhost/file:// variants.
impact: cloud-metadata + internal-network read (and internal POST via callback) from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; 0.1.3 published 2025-04-07, pre-dating @gladiaio/sdk (2025-09-09); re-verified this session; tarball code benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field)
impact: developers installing `gladia` run unofficial code; future account/repo hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (verified GET) across email/password and Google paths; unsigned return-to cookie proves server-driven redirect; post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin variants (https://evil.example.com, //evil.example.com)
verify_steps: AUTH_HELPED — complete sign-in then submit redirect_to=https://evil.example.com; capture post-auth Location; escalate only if reused as OAuth redirect_uri
impact: phishing/OAuth-flow manipulation → Low-Med
testability: AUTH_HELPED
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}` and compare `status`/`error_message`/duration; repeat with `video_url` on /video/text/video-transcription, then with `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe the outbound POST surface.
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 48
reasoning: /signin reflects redirect_to URL-encoded into the OAuth form action server-side (verified passively: action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); return-to cookie confirmed as unsigned base64url JSON {"url":"/"} with no allowlist enforced on the cookie; Google-only OAuth flow; if redirect_to is honored post-auth without host validation, the signed-in user lands on attacker domain, enabling phishing or OAuth state theft. Return-to cookie tampering itself was rejected (server resets), but redirect_to is a separate parameter not tested interactively.
evidence_needed: After completing Google OAuth with ?redirect_to=https://evil.example.com, final HTTP 302 Location resolves to external host; redirect_to=//evil.example.com, ?redirect_to=evil.com variants also accepted.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in (authorized/human session), GET /signin?redirect_to=https://evil.example.com, observe post-auth Location header; test protocol-relative and prefix-match variants
impact: Post-auth phishing redirect to attacker-controlled host; potential OAuth code/state interception if redirect_uri is also injectable; Medium
testability: AUTH_HELPED
[HYP] Tech stack disclosure via x-powered-by: Express on CORS preflight
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Confirmed via passive probe: OPTIONS preflight on /v2/pre-recorded returns `x-powered-by: Express`, revealing Node.js/Express.js; this header is absent from GET response headers but present on CORS preflight, enabling targeted framework-specific exploit scanning; combined with CORS wildcard and exposed trace headers, this lowers the bar for finding framework-level misconfigurations.
evidence_needed: `x-powered-by: Express` header in OPTIONS preflight response (observed); absent on GET responses (observed).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription`; `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` and compare headers for x-powered-by presence/absence
impact: Aids attacker reconnaissance (framework fingerprinting → known CVE targeting); Low
testability: PASSIVE
[PARKED] IDOR on transcription file download endpoints: confidence 50, AUTH_HELPED — cannot verify without valid API key; downgraded from 55 to 50 after confirming spec does not expose ownership-binding logic. Retained as actionable with key.
[PARKED] Post-OAuth redirect_to open redirect: confidence 48, AUTH_HELPED — return-to cookie REJECTED but redirect_to param is distinct; borderline on 40 threshold but retained due to distinct vector and prior laguna findings.
[FINAL] 1) Tech stack disclosure via x-powered-by: Express on CORS preflight (api.gladia.io, 90, MISCONFIG, PASSIVE)
[FINAL] 2) IDOR on transcription file download endpoints /{id}/file (api.gladia.io, 50, IDOR, AUTH_HELPED)
[FINAL] 3) Post-OAuth redirect_to open redirect without host allowlist (app.gladia.io /signin, 48, OATH, AUTH_HELPED)
[NEXT] PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` then `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription` — compare header sets to confirm `x-powered-by: Express` is present on preflight but absent on GET, and enumerate all framework/fingerprinting headers (e.g., `x-request-id`, `x-correlation-id`, `traceparent`).
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: `x-powered-by: Express` header present on CORS preflight (OPTIONS) responses only — confirms Node.js/Express.js backend; framework fingerprint for CVE targeting
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /health?full=true does NOT leak verbose output — returns identical `{"health":"OK"}` to /health; no build/version/metadata disclosure via query params
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /metrics endpoint does NOT exist — returns 404 (no Prometheus exposition endpoint)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: /debug, /admin, /actuator/health, /v1 paths do NOT exist or return 404 — no Spring Boot Actuator, no debug panel, no catch-all admin
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS preflight allows `Access-Control-Request-Headers: x-gladia-key` — auth header permitted in cross-origin requests (no credential support though)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: /v2/live/init is NOT a real endpoint — confirmed 404 "Cannot POST"; WebSocket session is created via POST /v2/live, then client connects to returned `url` (wss://api.gladia.io/v2/live?token=<uuid>)
[RISK] api.gladia.io: 82 reason: Express/Node.js backend fingerprinted via x-powered-by on CORS preflight; full OpenAPI 3.1 spec (14 paths) publicly readable without auth; CORS wildcard with x-gladia-key permitted in cross-origin preflight but no credentials; /health endpoint undocumented and exposed with CORS *; WebSocket auth token in URL query param per spec (wss://api.gladia.io/v2/live?token=<uuid>); 401 error responses leak request_id + trace headers; all v2 endpoints uniformly key-gated (single security model, no MFA/scopes); SSTI/SSRF surface via audio_url/video_url (key-gated)
[RISK] app.gladia.io: 52 reason: Google-only OAuth limits auth bypass surface; /dashboard SPA shell served 200 without auth (client-side enforcement only); return-to cookie is unsigned base64url JSON (server resets on tampering, REJECTED open redirect); redirect_to param reflected in form action but post-auth behavior unverified without session; cookies correctly flagged HttpOnly/Secure/SameSite=Lax; HSTS preload in effect; /signin redirects 302 with noindex/nofollow
[RISK] sdk: 45 reason: Official @glidiaio/sdk 1.1.0 + gladiaio-sdk PyPI verified clean (reposcan: no secrets, no malicious code); npm `gladia` 0.1.3 ownership anomaly ACCEPTED (description claims "Official" but repo is personal alexisbouchez/gladia.ts, maintainer softwarecitadel@gmail.com, published before official package) — supply-chain impersonation risk remains; gladia-quiz-app loads @glidiaio/sdk@0.5.2 from unpkg CDN (version pinning on CDN)
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
[HYP] SSRF via audio_url fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: Spec exposes audio_url + CallbackConfigDto.url with no scheme/allowlist; SDK forwards audio_url verbatim; docs note "callback_url not localhost" implying internal targets considered reachable unless blocked; jobs return status/error_message/timing = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare error_message/status/duration; (2) same via /video/text/video-transcription video_url (legacy path); (3) POST {"callback":{"url":"http://169.254.169.254:80/"}}; include localhost/file:// variants.
impact: cloud-metadata + internal-network read (and internal POST via callback) from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; 0.1.3 published 2025-04-07 pre-dating @gladiaio/sdk (2025-09-09); reposcan 20:06 re-confirmed, tarball benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field)
impact: developers installing `gladia` run unofficial code; future account/repo hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (re-probed 200, action contains full URL-encoded value) across email/password and Google paths; unsigned return-to cookie proves server-driven redirect concept; post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin variants (https://evil.example.com, //evil.example.com)
verify_steps: AUTH_HELPED — complete sign-in then submit redirect_to=https://evil.example.com; capture post-auth Location; escalate only if reused as OAuth redirect_uri
impact: phishing/OAuth-flow manipulation → Low-Med
testability: AUTH_HELPED
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}` and compare `status`/`error_message`/duration; repeat with `video_url` on /video/text/video-transcription, then with `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe the outbound POST surface.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: CORS GET responses return wildcard `*` not origin echo; expose-headers list trace/request-id headers; no allow-credentials → origin-reflection probe CLOSED, wildcard-without-credentials not exploitable
[LEARN] ACCEPTED OTHER @ npm registry: reposcan 20:02/20:06 flat (0 new hits, 5647 files) — gladia@0.1.3 anomaly remains sole reportable candidate; no new secrets
[NEW] api.gladia.io: GET /v1/models w/ Origin:evil.test → ACAO:* (wildcard, not echo), expose-headers list, no credentials → CORS origin-reflection dead; wildcard confirmed on GET not just preflight
[NEW] app.gladia.io: /signin re-probed 200; redirect_to still reflected into form action (surface stable)
[CHANGED] reposcan 20:02/20:06: 0 new hits; compare-stt providers.ts hardcodes model name "Solaria-3" (marketing-facing, low); gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg (maintenance debt)
[HYP] SSRF via audio_url fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: Spec exposes audio_url + CallbackConfigDto.url with no scheme/allowlist; SDK forwards audio_url verbatim; docs warn "callback_url not localhost" implying internal targets reachable unless blocked; jobs return status/error_message/timing = measurable signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare error_message/status/duration; (2) same via /video/text/video-transcription video_url; (3) POST {"callback":{"url":"http://169.254.169.254:80/"}}; include localhost/file:// variants.
impact: cloud-metadata + internal-network read (and internal POST via callback) → High (key-gated)
testability: AUTH_HELPED
[HYP] Impersonation/name-squat `gladia` npm package
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; published 2025-04-07 pre-dating @gladiaio/sdk (2025-09-09); tarball benign; reposcan 20:06 re-confirmed.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field)
impact: developers installing `gladia` run unofficial code; future account/repo hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Post-auth open redirect via redirect_to
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 55
reasoning: redirect_to reflected server-side into form action (re-probed 200 this cycle) across email/password and Google paths; unsigned return-to cookie proves server-driven redirect concept; post-auth final Location unobserved.
evidence_needed: with a real session, final Location for cross-origin variants (https://evil.example.com, //evil.example.com)
verify_steps: AUTH_HELPED — complete sign-in then submit redirect_to=https://evil.example.com; capture post-auth Location; escalate only if reused as OAuth redirect_uri
impact: phishing/OAuth-flow manipulation → Low-Med
testability: AUTH_HELPED
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`, then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}` and compare `status`/`error_message`/duration; repeat with `video_url` on /video/text/video-transcription, then with `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe the outbound POST surface.
