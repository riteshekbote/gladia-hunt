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
## 2026-08-07 21:47:22 UTC [api] (model bigpickle)
[NEW] api.gladia.io: OpenAPI /v1/history declares `custom_metadata` as OBJECT-typed query param (additionalProperties:true) + `status`/`kind` as multi-value array params + date filters — key-gated query-parsing surface not previously itemized (re-probed 21:46Z)
[NEW] api.gladia.io: CallbackConfigDto.url spec is `format: uri` only — no scheme enum/pattern/allowlist; client-side SSRF guard absent at schema level (confirmed this cycle)
[NEW] api.gladia.io: /v1/models public payload confirms datacenters [{FR},{US}] + per-request pricing 0.000055 — cloud egress regions for SSRF targeting; `created:1730000000` is static
[NEW] PyPI: gladiaio-sdk latest = 1.0.5 (version not previously recorded)
[CHANGED] api.gladia.io: endpoint map stable at 14 paths; /v1/history and /v2/upload both confirmed key-gated (401 "no gladia key provided") — no unauthenticated history/upload exposure
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url + callback/callback_config) — 7.2 (attack 8, business 9, tech 6, gate 3, cloud 9, fresh 7)
[PRIO] npm registry `gladia` 0.1.3 (dist-tag latest) — 5.9 (attack 5, business 8, tech 4, gate 9, cloud 2, fresh 5)
[PRIO] api.gladia.io GET /v1/history (object/array query params) — 5.5 (attack 6, business 6, tech 7, gate 3, cloud 4, fresh 6)
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: CallbackConfigDto.url is format:uri with no scheme/allowlist (spec re-read this cycle); /v1/models confirms egress regions FR/US (cloud-hosted); docs warn "callback_url not localhost" implying internal targets reachable; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare status/error_message/duration; (2) same via /video/text/video-transcription video_url; (3) POST {"callback":{"url":"http://169.254.169.254:80/"}}; include localhost/file:// variants.
impact: cloud-metadata + internal-network read, internal POST via callback → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; published 2025-04-07 pre-dating @gladiaio/sdk (2025-09-09); verified passive, tarball benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field re-confirmed)
impact: developers installing `gladia` run unofficial code; future repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Query-param parsing injection on /v1/history
class: BUSLOGIC
asset: api.gladia.io GET /v1/history (custom_metadata, status/kind arrays, date filters)
confidence: 48
reasoning: spec declares custom_metadata as object (additionalProperties:true) and status/kind as arrays in the QUERY STRING — non-native, server must parse via JSON/querystring; NestJS-style deep-parse foot-gun; date filters are string->Date coercion points.
evidence_needed: with a key, injection string in custom_metadata/status/date yields 500, altered filter results, or timing skew.
verify_steps: AUTH_HELPED — GET /v1/history?custom_metadata[__proto__][x]=1 and ?custom_metadata[$ne]=null and ?date[gt]=... ; observe 400/500 vs baseline; compare result set with legit filters.
impact: filter bypass / prototype pollution on own-tenant query → Low-Med (key-gated)
testability: AUTH_HELPED
[FINAL] 1. npm `gladia` impersonation (80, PASSIVE, ready to report) 2. SSRF via audio_url/callback (72, AUTH_HELPED, active POC target) 3. /v1/history query-param injection (48, AUTH_HELPED)
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`; then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}`, compare `status`/`error_message`/duration; then repeat with `video_url` on /video/text/video-transcription, then `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe outbound POST. Local SDK RAG is not possible (reposcan-raw/gladiaio/sdk empty stub) — the key is the only gate.
[LEARN] ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, not plain Express
[LEARN] ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
[RISK] api.gladia.io: 55 — large key-gated attack surface (SSRF-capable audio_url/callback fetch+POST, /v1/history query-injection candidate, NestJS fingerprinting) but every high-impact path sits behind x-gladia-key; public items (/v1/models, /health, /openapi.json) benign; SSRF would be High if a key is obtained
[RISK] app.gladia.io: 35 — SPA shell serving /dashboard unauthenticated, redirect_to reflected into form action (open redirect unconfirmed, server-side auth on APIs), unsigned return-to cookie; no confirmed high-severity flaw, moderate phishing surface
[RISK] sdk: 40 — confirmed name-squat gladia@0.1.3 on `latest` tag (reportable ownership anomaly) plus official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5; tarballs benign, residual supply-chain risk from maintainer sprawl
## 2026-08-07 22:24:30 UTC [api] (model bigpickle)
[NEW] api.gladia.io: OpenAPI /v1/history declares `custom_metadata` as OBJECT-typed query param (additionalProperties:true) + `status`/`kind` as multi-value array params + date filters — key-gated query-parsing surface not previously itemized (re-probed 21:46Z)
[NEW] api.gladia.io: CallbackConfigDto.url spec is `format: uri` only — no scheme enum/pattern/allowlist; client-side SSRF guard absent at schema level (confirmed this cycle)
[NEW] api.gladia.io: /v1/models public payload confirms datacenters [{FR},{US}] + per-request pricing 0.000055 — cloud egress regions for SSRF targeting; `created:1730000000` is static
[NEW] PyPI: gladiaio-sdk latest = 1.0.5 (version not previously recorded)
[CHANGED] api.gladia.io: endpoint map stable at 14 paths; /v1/history and /v2/upload both confirmed key-gated (401 "no gladia key provided") — no unauthenticated history/upload exposure
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url + callback/callback_config) — 7.2 (attack 8, business 9, tech 6, gate 3, cloud 9, fresh 7)
[PRIO] npm registry `gladia` 0.1.3 (dist-tag latest) — 5.9 (attack 5, business 8, tech 4, gate 9, cloud 2, fresh 5)
[PRIO] api.gladia.io GET /v1/history (object/array query params) — 5.5 (attack 6, business 6, tech 7, gate 3, cloud 4, fresh 6)
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: CallbackConfigDto.url is format:uri with no scheme/allowlist (spec re-read this cycle); /v1/models confirms egress regions FR/US (cloud-hosted); docs warn "callback_url not localhost" implying internal targets reachable; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed hitting an internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare status/error_message/duration; (2) same via /video/text/video-transcription video_url; (3) POST {"callback":{"url":"http://169.254.169.254:80/"}}; include localhost/file:// variants.
impact: cloud-metadata + internal-network read, internal POST via callback → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; published 2025-04-07 pre-dating @gladiaio/sdk (2025-09-09); verified passive, tarball benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field re-confirmed)
impact: developers installing `gladia` run unofficial code; future repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Query-param parsing injection on /v1/history
class: BUSLOGIC
asset: api.gladia.io GET /v1/history (custom_metadata, status/kind arrays, date filters)
confidence: 48
reasoning: spec declares custom_metadata as object (additionalProperties:true) and status/kind as arrays in the QUERY STRING — non-native, server must parse via JSON/querystring; NestJS-style deep-parse foot-gun; date filters are string->Date coercion points.
evidence_needed: with a key, injection string in custom_metadata/status/date yields 500, altered filter results, or timing skew.
verify_steps: AUTH_HELPED — GET /v1/history?custom_metadata[__proto__][x]=1 and ?custom_metadata[$ne]=null and ?date[gt]=... ; observe 400/500 vs baseline; compare result set with legit filters.
impact: filter bypass / prototype pollution on own-tenant query → Low-Med (key-gated)
testability: AUTH_HELPED
[FINAL] 1. npm `gladia` impersonation (80, PASSIVE, ready to report) 2. SSRF via audio_url/callback (72, AUTH_HELPED, active POC target) 3. /v1/history query-param injection (48, AUTH_HELPED)
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`; then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}`, compare `status`/`error_message`/duration; then repeat with `video_url` on /video/text/video-transcription, then `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe outbound POST. Local SDK RAG is not possible (reposcan-raw/gladiaio/sdk empty stub) — the key is the only gate.
[LEARN] ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, not plain Express
[LEARN] ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
[RISK] api.gladia.io: 55 — large key-gated attack surface (SSRF-capable audio_url/callback fetch+POST, /v1/history query-injection candidate, NestJS fingerprinting) but every high-impact path sits behind x-gladia-key; public items (/v1/models, /health, /openapi.json) benign; SSRF would be High if a key is obtained
[RISK] app.gladia.io: 35 — SPA shell serving /dashboard unauthenticated, redirect_to reflected into form action (open redirect unconfirmed, server-side auth on APIs), unsigned return-to cookie; no confirmed high-severity flaw, moderate phishing surface
[RISK] sdk: 40 — confirmed name-squat gladia@0.1.3 on `latest` tag (reportable ownership anomaly) plus official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5; tarballs benign, residual supply-chain risk from maintainer sprawl
[PRIO] api.gladia.io: 8.4 — a9/b10/tech8/gate7/cloud7/fresh7 — OpenAPI+14 paths public, CORS wildcard, Express fingerprint, ws token in URL query, audio_url fetch SSRF surface
[PRIO] app.gladia.io: 7.1 — a7/b9/tech6/gate8/cloud2/fresh8 — /dashboard 200 w/o auth (SPA), Google OAuth self-service, redirect_to reflected across all variant classes w/o allowlist
[PRIO] npm `gladia`@0.1.3: 5.95 — a5/b6/tech6/gate10/cloud2/fresh6 — "Official" claim vs personal repo/maintainer; pubdate precedes @gladiaio/sdk
[HYP] Post-OAuth open redirect via redirect_to without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 52
reasoning: Live-confirmed: redirect_to is reflected URL-encoded into the OAuth form action for https://evil, //evil, bare-host, confusing-subdomain (app.gladia.io.evil), and path-only variants — server-side reflection with no visible host allowlist; return-to cookie unsigned base64url JSON confirms server-driven redirect concept.
evidence_needed: Final post-auth HTTP 302 Location resolving to external host after completing sign-in with ?redirect_to=https://evil.example.com.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in with ?redirect_to=https://evil.example.com, //evil.example.com, and https://app.gladia.io.evil.example.com/ variants; capture post-auth Location + Set-Cookie; test redirect_to reuse as OAuth redirect_uri injection.
impact: Post-auth phishing redirect to attacker host; OAuth code/state theft if redirect_uri injectable → Medium (High only if redirect_uri proven injectable).
testability: AUTH_HELPED
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/upload, /video/text/video-transcription
confidence: 72
reasoning: OpenAPI spec (sampled /openapi.json, live 200) shows audio_url accepted verbatim with no client-side validation; SDK RAG confirms is_url only in upload helper, not transcription path; legacy /video|/audio/* endpoints add a second fetch path.
evidence_needed: 169.254.169.254 or internal-host fetch reflected via error_code/status/timing on a key-gated request.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat via /video/text/video-transcription video_url to compare legacy-path behavior; compare error_code/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated).
testability: AUTH_HELPED
[HYP] Framework fingerprint via x-powered-by: Express on CORS preflight only
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Live-verified this round: OPTIONS /v2/transcription with Origin returns x-powered-by: Express (204); GET /v2/transcription returns 401 with no x-powered-by — confirmed backend-specific header leakage on preflight only, enabling targeted Node/Express CVE scanning alongside CORS wildcard + exposed trace headers.
evidence_needed: x-powered-by: Express in OPTIONS response, absent in GET response (both observed live).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` vs `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription`; diff header sets.
impact: Aids reconnaissance → known CVE targeting; Low.
testability: PASSIVE
[PARKED] IDOR on transcription file download /{id}/file: confidence 50 < live-verify; spec does not expose ownership-binding logic; no key available → remain PARKED (already retained as such, no action).
[FINAL] (re-ranked top→bottom)
[NEXT] HUMAN: with an authorized/verified session (Google SSO or program-supplied trial key), GET /signin?redirect_to=https://evil.example.com then complete OAuth, capture final post-auth 302 Location & Set-Cookie to determine if redirect_to is honored to an external host; test //evil.example.com and https://app.gladia.io.evil.example.com/ variants; attempt redirect_to-as-redirect_uri injection to escalate to OAuth state/code theft.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflight-only fingerprint differential (freshness 2026-08-07 21:46 UTC).
[LEARN] ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), and path-only variants — no host allowlist enforced on reflection (post-auth honoring remains AUTH_HELPED/unverified).
[LEARN] CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-design path (freshly sampled).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express fingerprint, websocket token in URL query, /health undocumented, audio_url/video_url SSRF surface, single key-gated auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); return-to cookie signed-reset (REJECTED); CSP strict present; redirect_to form-action reflection unverified post-auth
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; npm `gladia`@0.1.3 impersonation anomaly (personal repo, pre-dates official package) remains sole reportable supply-chain candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg
impact: cloud-metadata + internal-network read, internal POST via callback → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; published 2025-04-07 pre-dating @gladiaio/sdk (2025-09-09); verified passive, tarball benign.
evidence_needed: none — metadata verified
verify_steps: PASSIVE — done (registry metadata + publish times + repo field re-confirmed)
impact: developers installing `gladia` run unofficial code; future repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Query-param parsing injection on /v1/history
class: BUSLOGIC
asset: api.gladia.io GET /v1/history (custom_metadata, status/kind arrays, date filters)
confidence: 48
reasoning: spec declares custom_metadata as object (additionalProperties:true) and status/kind as arrays in the QUERY STRING — non-native, server must parse via JSON/querystring; NestJS-style deep-parse foot-gun; date filters are string->Date coercion points.
evidence_needed: with a key, injection string in custom_metadata/status/date yields 500, altered filter results, or timing skew.
verify_steps: AUTH_HELPED — GET /v1/history?custom_metadata[__proto__][x]=1 and ?custom_metadata[$ne]=null and ?date[gt]=... ; observe 400/500 vs baseline; compare result set with legit filters.
impact: filter bypass / prototype pollution on own-tenant query → Low-Med (key-gated)
testability: AUTH_HELPED
[FINAL] 1. npm `gladia` impersonation (80, PASSIVE, ready to report) 2. SSRF via audio_url/callback (72, AUTH_HELPED, active POC target) 3. /v1/history query-param injection (48, AUTH_HELPED)
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key`; then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}`, compare `status`/`error_message`/duration; then repeat with `video_url` on /video/text/video-transcription, then `{"callback":{"url":"http://169.254.169.254:80/"}}` to probe outbound POST. Local SDK RAG is not possible (reposcan-raw/gladiaio/sdk empty stub) — the key is the only gate.
[LEARN] ACCEPTED AUTH @ api.gladia.io: /v1/history and /v2/upload confirmed key-gated (401) — no unauthenticated history/upload path
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI map stable at 14 paths (re-check 21:46Z) — no new endpoints since 20:55
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: 401 error body {statusCode,timestamp,path,message,request_id} is NestJS HttpException shape → backend is NestJS-on-Express, not plain Express
[LEARN] ACCEPTED OTHER @ npm registry: PyPI gladiaio-sdk latest 1.0.5; npm @gladiaio/sdk 1.1.0 unchanged — supply-chain surface static
[RISK] api.gladia.io: 55 — large key-gated attack surface (SSRF-capable audio_url/callback fetch+POST, /v1/history query-injection candidate, NestJS fingerprinting) but every high-impact path sits behind x-gladia-key; public items (/v1/models, /health, /openapi.json) benign; SSRF would be High if a key is obtained
[RISK] app.gladia.io: 35 — SPA shell serving /dashboard unauthenticated, redirect_to reflected into form action (open redirect unconfirmed, server-side auth on APIs), unsigned return-to cookie; no confirmed high-severity flaw, moderate phishing surface
[RISK] sdk: 40 — confirmed name-squat gladia@0.1.3 on `latest` tag (reportable ownership anomaly) plus official @gladiaio/sdk 1.1.0 / gladiaio-sdk 1.0.5; tarballs benign, residual supply-chain risk from maintainer sprawl
[PRIO] api.gladia.io (CORS+wildcard + openapi.json), score 8.2 | attack:9, business:8, tech:7 (CORS misconfig), gate:9 (no auth on 404), cloud:8 (HSTS), freshness:10
[PRIO] api.gladia.io/openapi.json (full spec exposure), score 7.4 | attack:8, business:8, tech:7 (spec exposure), gate:10, cloud:6, freshness:8
[PRIO] app.gladia.io (return-to cookie JWT-shaped), score 6.8 | attack:7, business:6, tech:7 (JWT-ish cookie), gate:8, cloud:5, freshness:6
[PRIO] npm `gladia` 0.1.3 vs @gladiaio/sdk ownership conflict, score 5.1 | attack:6, business:5, tech:5, gate:9, cloud:4, freshness:7
[HYP] CORS wildcard reflects origin
class: MISCONFIG
asset: api.gladia.io
confidence: 75
reasoning: Known CORS `access-control-allow-origin: *` already confirmed; need to verify if it reflects a credentialed origin or sets Access-Control-Allow-Credentials. Seed explicitly asks "verify actual behavior."
evidence_needed: Origin header reflected in ACAO, or Access-Control-Allow-Credentials: true with credentials
verify_steps: passive PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json`
impact: Attacker can read API spec + 404 details cross-origin; possible credentialed exfiltration if credentials allowed
testability: PASSIVE
[HYP] OpenAPI spec contains undocumented or shadow endpoints
class: MISCONFIG
asset: api.gladia.io/openapi.json
confidence: 55
reasoning: Spec is consumed by official SDK generator; seed says "check for undocumented/shadow endpoints." Spec lists 14 paths but may contain internal, deprecated, or test routes not documented externally.
evidence_needed: Path in spec that returns 200 with valid (or different) behavior vs. documented expectation, or path absent from public docs
verify_steps: passive PROBE: compare every path in spec against public docs; request a few obscure paths (e.g., /v1/history) to confirm reachability
impact: Unknown API surface, potential unauthenticated access to sensitive operations
testability: PASSIVE
[HYP] return-to cookie has weak/no signature validation
class: AUTH
asset: app.gladia.io/signin (redirect flow)
confidence: 45
reasoning: Cookie `return-to=eyJ1urwiOiIvIn0%3D` decodes to `{"url":"/"}` with no dot-separated signature segment (no alg). Seed asks to "check signature/alg handling."
evidence_needed: Server accepts crafted return-to value and redirects to attacker-controlled or unintended target
verify_steps: AUTH_HELPED: requires interactive signin flow test; not feasible passively without credential
impact: Open redirect / auth bypass in SSO flow
testability: AUTH_HELPED
[FINAL]
[NEXT] PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json` — check if `access-control-allow-origin` reflects `https://evil.test` and if `access-control-allow-credentials: true` is present.
[RISK] api.gladia.io: 72 reason: CORS wildcard exposure + full OpenAPI spec + x-api-key auth only | app.gladia.io: 55 reason: JWT-shaped unsigned cookie in redirect flow | sdk: 45 reason: npm ownership discrepancy (gladia vs @gladiaio/sdk)
[HYP] CORS wildcard enables cross-origin read of API data/spec (no credential support)
class: MISCONFIG
asset: api.gladia.io (all responses, incl. /openapi.json and /v1/models)
confidence: 65
reasoning: Passive OPTIONS/GET probes confirm static `access-control-allow-origin: *` with NO `access-control-allow-credentials`. Any origin can read the public OpenAPI spec, 404 bodies, exposed trace headers, and the unauthenticated /v1/models response cross-origin. Credentialled exfiltration is NOT enabled, but cross-origin readability broadens attacker reach.
evidence_needed: `access-control-allow-origin: *` in response headers; absence of `access-control-allow-credentials`
verify_steps: passive PROBE (already observed): `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/openapi.json`; `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models`
impact: Low-severity info disclosure — malicious site reads full API surface + model list + trace headers cross-origin; no credential theft since creds disallowed
testability: PASSIVE
[HYP] return-to cookie is unsigned base64url JSON enabling post-auth redirect manipulation
class: AUTH
asset: app.gladia.io /signin (return-to cookie + redirect_to form action)
confidence: 60
reasoning: Passive probe confirms root `/` sets `return-to=eyJ1cmwiOiIvIn0%3D` which decodes to plain JSON `{"url":"/"}` with 0 dots (no JWT signature). `/signin` reflects `redirect_to=https%3A%2F%2Fevil.example.com` into the OAuth form `action`. A crafted return-to/redirect_to could steer the Google OAuth post-auth redirect to an attacker-controlled host.
evidence_needed: Server honors attacker-supplied return-to/redirect_to and redirects post-authentication (HTTP 302 Location) to an external host
verify_steps: AUTH_HELPED: complete Google OAuth signin with `?redirect_to=https://evil.example.com` and observe the post-auth HTTP 302 Location; passive pre-check: `curl -sS "https://app.gladia.io/signin?redirect_to=https%3A%2F%2Fevil.example.com" | grep -o 'action="[^"]*"'` (already reflects)
impact: Open redirect / post-auth redirect to attacker site for credential capture or phishing; severity medium
testability: AUTH_HELPED
[HYP] npm `gladia` package impersonates official SDK from personal repo
class: OATH
asset: npm `gladia@0.1.3` (github.com/alexisbouchez/gladia.ts)
confidence: 55
reasoning: Passive `npm view` confirms `description` = "Official TypeScript SDK for Gladia" yet `repository.url` points to the personal account alexisbouchez/gladia.ts (not the official gladiaio org). Maintainer is `softwarecitadel <softwarecitadel@gmail.com>`. This is an ownership/typosquat anomaly that can mislead users into importing an unofficial package.
evidence_needed: npm registry metadata (description, repository.url, maintainer) mismatched against the official @gladiaio/sdk
verify_steps: passive PROBE: `npm view gladia@0.1.3 description repository.url maintainer homepage` (already run)
impact: Supply-chain confusion — developers install an unofficial/misattributed SDK thinking it is official; severity medium-high
testability: PASSIVE
[FINAL] (reranked, top first)
[NEXT] PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-origin: *` (escalation check: can an attacker origin read the unauthenticated models payload, not just the preflight).
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
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
verify_steps: AUTH_HELPED: complete Google OAuth signin with `?redirect_to=https://evil.example.com` and observe the post-auth HTTP 302 Location; passive pre-check: `curl -sS "https://app.gladia.io/signin?redirect_to=https%3A%2F%2Fevil.example.com" | grep -o 'action="[^"]*"'` (already reflects)
impact: Open redirect / post-auth redirect to attacker site for credential capture or phishing; severity medium
testability: AUTH_HELPED
[HYP] npm `gladia` package impersonates official SDK from personal repo
class: OATH
asset: npm `gladia@0.1.3` (github.com/alexisbouchez/gladia.ts)
confidence: 55
reasoning: Passive `npm view` confirms `description` = "Official TypeScript SDK for Gladia" yet `repository.url` points to the personal account alexisbouchez/gladia.ts (not the official gladiaio org). Maintainer is `softwarecitadel <softwarecitadel@gmail.com>`. This is an ownership/typosquat anomaly that can mislead users into importing an unofficial package.
evidence_needed: npm registry metadata (description, repository.url, maintainer) mismatched against the official @gladiaio/sdk
verify_steps: passive PROBE: `npm view gladia@0.1.3 description repository.url maintainer homepage` (already run)
impact: Supply-chain confusion — developers install an unofficial/misattributed SDK thinking it is official; severity medium-high
testability: PASSIVE
[FINAL] (reranked, top first)
[NEXT] PROBE: `curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models` — confirm the GET response also carries `access-control-allow-origin: *` (escalation check: can an attacker origin read the unauthenticated models payload, not just the preflight).
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
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
[PRIO] api.gladia.io, 8.5, attack_surface=9 business_value=9 tech_exposure=8 gate_ease=10 cloud_surface=8 freshness=8
[PRIO] app.gladia.io, 6.3, attack_surface=7 business_value=8 tech_exposure=6 gate_ease=6 cloud_surface=6 freshness=7
[PRIO] npm @gladiaio/sdk, 5.0, attack_surface=5 business_value=6 tech_exposure=5 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] PyPI gladiaio-sdk, 4.7, attack_surface=4 business_value=6 tech_exposure=4 gate_ease=8 cloud_surface=3 freshness=6
[PRIO] npm gladia (typosquat candidate), 4.3, attack_surface=4 business_value=5 tech_exposure=4 gate_ease=9 cloud_surface=2 freshness=5
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io
confidence: 65
reasoning: OpenAPI shows transcription endpoints accept audio_url/video_url parameters; server likely fetches these URLs server-side; no SSRF protections documented in spec; v2/live init may also accept URL inputs
evidence_needed: Confirm server-side fetch behavior; test with internal metadata URLs (169.254.169.254), localhost, private CIDRs; check for redirect following
verify_steps: RAG: read gladiaio/sdk packages/sdk-js + packages/sdk-python + generator and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io; PROBE: POST https://api.gladia.io/v2/pre-recorded -H "x-gladia-key: <valid_key>" -H "Content-Type: application/json" -d '{"audio_url":"http://169.254.169.254/latest/meta-data/"}' (AUTH_HELPED)
impact: Cloud metadata access, internal service enumeration, potential data exfiltration; severity High
testability: AUTH_HELPED
[HYP] CORS wildcard reflects arbitrary origin enabling cross-origin API reads
class: MISCONFIG
asset: api.gladia.io
confidence: 75
reasoning: Preflight shows access-control-allow-origin: * with allow-headers: x-gladia-key but NO access-control-allow-credentials; wildcard reflects request Origin header value per prior probe; allows unauthenticated cross-origin reads of public endpoints (/v1/models, /openapi.json, /health)
evidence_needed: Confirm Origin reflection on credentialed endpoints; verify no credential leakage via wildcard
verify_steps: PROBE: curl -H "Origin: https://evil.test" -D - -o /dev/null https://api.gladia.io/v1/models — confirm access-control-allow-origin reflects https://evil.test; PROBE: curl -H "Origin: https://evil.test" -H "x-gladia-key: test" -D - -o /dev/null https://api.gladia.io/v2/transcription — observe 401 but check CORS headers
impact: Data exposure from public endpoints; aids reconnaissance; severity Low-Medium
testability: PASSIVE
[HYP] npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace
class: OTHER
asset: npm registry (gladia@0.1.3)
confidence: 70
reasoning: Package description claims "Official TypeScript SDK for Gladia" but repository=github.com/alexisbouchez/gladia.ts (personal account), maintainer=softwarecitadel@gmail.com; official SDK is @gladiaio/sdk from gladiaio/sdk monorepo; users may install wrong package
evidence_needed: Verify if alexisbouchez/softwarecitadel is affiliated with Gladia; check package code for malicious behavior; compare API surface with official SDK
verify_steps: RAG: Read github.com/alexisbouchez/gladia.ts source; diff against @gladiaio/sdk; check install scripts, network calls, data exfiltration; HUMAN: Contact Gladia security to confirm ownership
impact: Supply chain risk — developers may install impersonated SDK leading to credential theft or malicious code execution; severity Medium-High
testability: RAG
[FINAL] 1) SSRF via audio_url/video_url server-side fetch (api.gladia.io, 65, SSRF) 2) CORS wildcard reflects arbitrary origin enabling cross-origin API reads (api.gladia.io, 75, MISCONFIG) 3) npm package gladia@0.1.3 typosquats official @gladiaio/sdk namespace (npm registry, 70, OTHER)
[NEXT] RAG: Read gladiaio/sdk (packages/sdk-js + packages/sdk-python + generator) and gladia-samples to confirm how audio_url/video_url flows into api.gladia.io (any client-side validation, SSRF protections documented)
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: Undocumented /health endpoint returns 200 (not in OpenAPI spec)
[LEARN] ACCEPTED AUTH @ api.gladia.io: WebSocket auth uses token in URL query parameter per OpenAPI spec
[LEARN] REJECTED AUTH @ app.gladia.io: return-to cookie tampering does not lead to open redirect (server validates/resets)
[LEARN] ACCEPTED OTHER @ npm registry: gladia@0.1.3 ownership anomaly (personal repo, unofficial maintainer) — requires affiliation verification
[RISK] api.gladia.io: 85 reason: Public OpenAPI spec reveals full attack surface; CORS wildcard with credential-exposed headers; WebSocket token-in-URL design; undocumented /health endpoint; no auth on spec endpoint; high business value (core transcription API); potential SSRF via audio_url/video_url
[RISK] app.gladia.io: 55 reason: Dashboard SPA served without auth (client-side enforcement); return-to cookie validated server-side; redirect_to reflected in form action but no open redirect; HSTS preload strong; Google-only OAuth limits attack surface
[RISK] sdk: 40 reason: Official SDKs (@gladiaio/sdk, gladiaio-sdk) generated from public spec; third-party gladia@0.1.3 is ownership anomaly but not Gladia code; no malicious behavior observed in package metadata
[PRIO] api.gladia.io, 9.1, attack_surface=10 business_value=9 tech_exposure=8 (Express/Mongo/S3/WSS) gate_ease=10 cloud_surface=9 freshness=10
[PRIO] app.gladia.io /signin, 6.5, attack_surface=6 business_value=8 tech_exposure=6 (OAuth2/React/HttpOnly cookies) gate_ease=6 cloud_surface=5 freshness=8
[PRIO] npm `gladia` 0.1.3 (registry), 5.5, attack_surface=4 business_value=5 tech_exposure=5 (supply-chain) gate_ease=9 cloud_surface=1 freshness=7
[HYP] IDOR on transcription file download endpoints /{id}/file
class: IDOR
asset: api.gladia.io /v2/transcription/{id}/file, /v2/pre-recorded/{id}/file, /v2/live/{id}/file
confidence: 50
reasoning: OpenAPI spec defines three GET {id}/file endpoints for downloading transcription audio/text files; authorization model (object-level access control) is opaque in the spec; endpoint names follow a pattern where {id} is a UUID — if the server does not bind the resource owner to the x-gladia-key scope, cross-account file access is possible. No spec property indicates per-resource ownership validation.
evidence_needed: Successful file download (200 with content) using a valid x-gladia-key belonging to a different user/session than the {id} target; error 403/404 when key does not match owner would disprove it.
verify_steps: AUTH_HELPED — obtain a trial/test API key from Gladia (authorized), POST /v2/transcription with a test audio_url, GET /v2/transcription/{other_user_id}/file with own key; observe 200 (IDOR) vs 403 (protected). Compare against /v2/pre-recorded/{id}/file and /v2/live/{id}/file.
impact: Unauthorized access to other users' transcription data (PII, audio, sensitive content); High
testability: AUTH_HELPED
[HYP] Post-OAuth redirect_to open redirect without host allowlist
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
[PRIO] api.gladia.io: 8.4 — a9/b10/tech8/gate7/cloud7/fresh7 — OpenAPI+14 paths public, CORS wildcard, Express fingerprint, ws token in URL query, audio_url fetch SSRF surface
[PRIO] app.gladia.io: 7.1 — a7/b9/tech6/gate8/cloud2/fresh8 — /dashboard 200 w/o auth (SPA), Google OAuth self-service, redirect_to reflected across all variant classes w/o allowlist
[PRIO] npm `gladia`@0.1.3: 5.95 — a5/b6/tech6/gate10/cloud2/fresh6 — "Official" claim vs personal repo/maintainer; pubdate precedes @gladiaio/sdk
[HYP] Post-OAuth open redirect via redirect_to without host allowlist
class: OATH
asset: app.gladia.io /signin?redirect_to=
confidence: 52
reasoning: Live-confirmed: redirect_to is reflected URL-encoded into the OAuth form action for https://evil, //evil, bare-host, confusing-subdomain (app.gladia.io.evil), and path-only variants — server-side reflection with no visible host allowlist; return-to cookie unsigned base64url JSON confirms server-driven redirect concept.
evidence_needed: Final post-auth HTTP 302 Location resolving to external host after completing sign-in with ?redirect_to=https://evil.example.com.
verify_steps: AUTH_HELPED — complete Google OAuth sign-in with ?redirect_to=https://evil.example.com, //evil.example.com, and https://app.gladia.io.evil.example.com/ variants; capture post-auth Location + Set-Cookie; test redirect_to reuse as OAuth redirect_uri injection.
impact: Post-auth phishing redirect to attacker host; OAuth code/state theft if redirect_uri injectable → Medium (High only if redirect_uri proven injectable).
testability: AUTH_HELPED
[HYP] SSRF via audio_url/video_url server-side fetch
class: SSRF
asset: api.gladia.io /v2/pre-recorded, /v2/upload, /video/text/video-transcription
confidence: 72
reasoning: OpenAPI spec (sampled /openapi.json, live 200) shows audio_url accepted verbatim with no client-side validation; SDK RAG confirms is_url only in upload helper, not transcription path; legacy /video|/audio/* endpoints add a second fetch path.
evidence_needed: 169.254.169.254 or internal-host fetch reflected via error_code/status/timing on a key-gated request.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat via /video/text/video-transcription video_url to compare legacy-path behavior; compare error_code/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated).
testability: AUTH_HELPED
[HYP] Framework fingerprint via x-powered-by: Express on CORS preflight only
class: MISCONFIG
asset: api.gladia.io (OPTIONS responses)
confidence: 90
reasoning: Live-verified this round: OPTIONS /v2/transcription with Origin returns x-powered-by: Express (204); GET /v2/transcription returns 401 with no x-powered-by — confirmed backend-specific header leakage on preflight only, enabling targeted Node/Express CVE scanning alongside CORS wildcard + exposed trace headers.
evidence_needed: x-powered-by: Express in OPTIONS response, absent in GET response (both observed live).
verify_steps: PROBE: `curl -sS -D - -o /dev/null -X OPTIONS -H "Origin: https://evil.test" -H "Access-Control-Request-Headers: x-gladia-key" https://api.gladia.io/v2/transcription` vs `curl -sS -D - -o /dev/null https://api.gladia.io/v2/transcription`; diff header sets.
impact: Aids reconnaissance → known CVE targeting; Low.
testability: PASSIVE
[PARKED] IDOR on transcription file download /{id}/file: confidence 50 < live-verify; spec does not expose ownership-binding logic; no key available → remain PARKED (already retained as such, no action).
[FINAL] (re-ranked top→bottom)
[NEXT] HUMAN: with an authorized/verified session (Google SSO or program-supplied trial key), GET /signin?redirect_to=https://evil.example.com then complete OAuth, capture final post-auth 302 Location & Set-Cookie to determine if redirect_to is honored to an external host; test //evil.example.com and https://app.gladia.io.evil.example.com/ variants; attempt redirect_to-as-redirect_uri injection to escalate to OAuth state/code theft.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live-probed /v2/transcription OPTIONS → `x-powered-by: Express` present; GET 401 → `x-powered-by` absent — confirmed preflight-only fingerprint differential (freshness 2026-08-07 21:46 UTC).
[LEARN] ACCEPTED OATH @ app.gladia.io: redirect_to reflected into form action for protocol-relative (`//evil`), bare-host, confusing-subdomain (`app.gladia.io.evil`), and path-only variants — no host allowlist enforced on reflection (post-auth honoring remains AUTH_HELPED/unverified).
[LEARN] CONFIRMED @ api.gladia.io: /openapi.json (200, 125KB, CORS *) publicly exposes full v2 surface incl. audio_url field accepted verbatim — confirms SSRF fetch-by-design path (freshly sampled).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express fingerprint, websocket token in URL query, /health undocumented, audio_url/video_url SSRF surface, single key-gated auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); return-to cookie signed-reset (REJECTED); CSP strict present; redirect_to form-action reflection unverified post-auth
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; npm `gladia`@0.1.3 impersonation anomaly (personal repo, pre-dates official package) remains sole reportable supply-chain candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2 on unpkg
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config), legacy /audio|/video/text/*
confidence: 72
reasoning: CallbackConfigDto.url is `format:uri` with no scheme enum/pattern/allowlist (re-verified this cycle from live /openapi.json); InitTranscriptionRequest.audio_url accepted verbatim with zero client-side validation; /v1/models confirms FR/US cloud egress; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 or internal host reflected in error_message/status/duration; or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: (1) POST /v2/pre-recorded {"audio_url":"http://<attacker-canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}, compare status/error_message/duration; (2) same via /video/text/video-transcription video_url; (3) POST {"callback_config":{"url":"http://169.254.169.254:80/"},"callback":true}; include localhost/file:// variants.
impact: cloud-metadata + internal-network read, internal POST via callback → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; created 2025-03-28/0.1.3-published 2025-04-07, both pre-dating @gladiaio/sdk (2025-09-09); reposcan 22:03 flat re-confirmed, tarball benign.
evidence_needed: none — metadata verified; affiliation check via Gladia disclosure channel pending.
verify_steps: PASSIVE — done (registry metadata + publish times + repo field + PyPI twin absence re-confirmed 22:24Z)
impact: developers installing `gladia` run unofficial code; future repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] Query-param parsing injection on /v1/history
class: BUSLOGIC
asset: api.gladia.io GET /v1/history (custom_metadata, status/kind arrays, date filters)
confidence: 48
reasoning: spec still declares custom_metadata as object (additionalProperties:true) and status/kind as arrays in the QUERY STRING (re-verified 22:22Z) — non-native, server must deep-parse via JSON/querystring; NestJS-style foot-gun; date filters are string→Date coercion points.
evidence_needed: with a key, injection string in custom_metadata/status/date yields 500, altered filter results, or timing skew.
verify_steps: AUTH_HELPED — GET /v1/history?custom_metadata[__proto__][x]=1 and ?custom_metadata[$ne]=null and ?date[gt]=...; observe 400/500 vs baseline; compare result set with legit filters.
impact: filter bypass / prototype pollution on own-tenant query → Low-Med (key-gated)
testability: AUTH_HELPED
[NEXT] HUMAN: request a program-provided or personal trial `x-gladia-key` (standing blocker for both api hypotheses); then POST https://api.gladia.io/v2/pre-recorded `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` vs `{"audio_url":"http://<attacker-canary>"}`, compare `status`/`error_message`/duration; repeat with `video_url` on /video/text/video-transcription, then `{"callback":true,"callback_config":{"url":"http://169.254.169.254:80/"}}`. Passive recon is now saturated (14-path map stable, PyPI twin absent, dashboard bundles negative) — the key is the only remaining gate.
## 2026-08-07 23:09:07 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url + callback SSRF fetch): 6.6 = attack7 business9 tech6 gate2 cloud9 fresh5
[PRIO] app.gladia.io /signin (OAuth redirect_to reflection): 6.1 = attack6 business8 tech7 gate7 cloud1 fresh4
[PRIO] npm registry `gladia`@0.1.3: 5.5 = attack5 business7 tech4 gate10 cloud1 fresh3
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback_config) + legacy /video|/audio/text/*
confidence: 72
reasoning: live spec re-verified this cycle — audio_url accepted verbatim (`format:uri`, no allowlist), CallbackConfigDto.url same; /v1/models confirms FR/US cloud egress; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 / internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback":true,"callback_config":{"url":"http://169.254.169.254:80/"}}; compare error/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial / hijack risk
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; both pre-date @gladiaio/sdk (2025-09-09); re-confirmed live 23:08Z, tarball benign.
evidence_needed: none — metadata verified; affiliation check via Gladia disclosure channel pending.
verify_steps: PASSIVE — done (registry metadata + publish times + repo field re-confirmed 23:08Z)
impact: developers installing `gladia` run unofficial code; repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: live re-probe 23:08Z — /signin?redirect_to=... returns 200, param reflected URL-encoded into form action (all variants: https://, //, bare-host, confusing-subdomain); return-to cookie is unsigned base64url JSON {"url":"/"} confirming server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: final post-auth HTTP 302 Location resolving to external host after Google sign-in with redirect_to set; or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[PARKED] /v1/history query-param deep-parsing injection (BUSLOGIC, conf 48): deprioritized vs standing key blocker — key-gated, marginal ROI, confidence near floor; retained in leads.
[FINAL] 1) SSRF audio_url/callback (72, High impact) 2) `gladia` npm impersonation (80, Medium) 3) redirect_to post-auth OATH (60, Medium/High-if-redirect_uri).
[NEXT] HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://169.254.169.254/latest/meta-data/"} vs {"audio_url":"http://<attacker-canary>"}, compare status/error_message/duration; repeat video_url on /video/text/video-transcription, then callback_config to internal port. Passive surface saturated and frozen — the key is the only gate remaining.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-powered-by differential) — no drift, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surface persists (re-verified 23:08Z).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths/125KB), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express preflight fingerprint, WS token in URL query, undocumented /health, audio_url/callback SSRF-by-design (key-gated), single-key auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); redirect_to form-action reflection post-auth unverified; strict CSP; return-to signed-reset (REJECTED)
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; `gladia`@0.1.3 impersonation anomaly sole reportable candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2
## 2026-08-07 23:49:21 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url + callback SSRF fetch): 6.6 = attack7 business9 tech6 gate2 cloud9 fresh5
[PRIO] app.gladia.io /signin (OAuth redirect_to reflection): 6.1 = attack6 business8 tech7 gate7 cloud1 fresh4
[PRIO] npm registry `gladia`@0.1.3: 5.5 = attack5 business7 tech4 gate10 cloud1 fresh3
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback_config) + legacy /video|/audio/text/*
confidence: 72
reasoning: live spec re-verified this cycle — audio_url accepted verbatim (`format:uri`, no allowlist), CallbackConfigDto.url same; /v1/models confirms FR/US cloud egress; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 / internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback":true,"callback_config":{"url":"http://169.254.169.254:80/"}}; compare error/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial / hijack risk
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; both pre-date @gladiaio/sdk (2025-09-09); re-confirmed live 23:08Z, tarball benign.
evidence_needed: none — metadata verified; affiliation check via Gladia disclosure channel pending.
verify_steps: PASSIVE — done (registry metadata + publish times + repo field re-confirmed 23:08Z)
impact: developers installing `gladia` run unofficial code; repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: live re-probe 23:08Z — /signin?redirect_to=... returns 200, param reflected URL-encoded into form action (all variants: https://, //, bare-host, confusing-subdomain); return-to cookie is unsigned base64url JSON {"url":"/"} confirming server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: final post-auth HTTP 302 Location resolving to external host after Google sign-in with redirect_to set; or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[PARKED] /v1/history query-param deep-parsing injection (BUSLOGIC, conf 48): deprioritized vs standing key blocker — key-gated, marginal ROI, confidence near floor; retained in leads.
[FINAL] 1) SSRF audio_url/callback (72, High impact) 2) `gladia` npm impersonation (80, Medium) 3) redirect_to post-auth OATH (60, Medium/High-if-redirect_uri).
[NEXT] HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://169.254.169.254/latest/meta-data/"} vs {"audio_url":"http://<attacker-canary>"}, compare status/error_message/duration; repeat video_url on /video/text/video-transcription, then callback_config to internal port. Passive surface saturated and frozen — the key is the only gate remaining.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-powered-by differential) — no drift, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surface persists (re-verified 23:08Z).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths/125KB), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express preflight fingerprint, WS token in URL query, undocumented /health, audio_url/callback SSRF-by-design (key-gated), single-key auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); redirect_to form-action reflection post-auth unverified; strict CSP; return-to signed-reset (REJECTED)
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; `gladia`@0.1.3 impersonation anomaly sole reportable candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2
impact: developers installing `gladia` run unofficial code; repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: live re-probe 23:08Z — /signin?redirect_to=... returns 200, param reflected URL-encoded into form action (all variants: https://, //, bare-host, confusing-subdomain); return-to cookie is unsigned base64url JSON {"url":"/"} confirming server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: final post-auth HTTP 302 Location resolving to external host after Google sign-in with redirect_to set; or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[PARKED] /v1/history query-param deep-parsing injection (BUSLOGIC, conf 48): deprioritized vs standing key blocker — key-gated, marginal ROI, confidence near floor; retained in leads.
[FINAL] 1) SSRF audio_url/callback (72, High impact) 2) `gladia` npm impersonation (80, Medium) 3) redirect_to post-auth OATH (60, Medium/High-if-redirect_uri).
[NEXT] HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://169.254.169.254/latest/meta-data/"} vs {"audio_url":"http://<attacker-canary>"}, compare status/error_message/duration; repeat video_url on /video/text/video-transcription, then callback_config to internal port. Passive surface saturated and frozen — the key is the only gate remaining.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:08Z byte-identical to 22:22Z (openapi 125131B/14 paths, /v1/models, /health, /v2/live 401, CORS, x-powered-by differential) — no drift, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk 1.1.0 metadata static 23:08Z — supply-chain surface unchanged.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: live spec still shows audio_url + CallbackConfigDto.url as `format:uri` with no scheme allowlist — SSRF-by-design fetch surface persists (re-verified 23:08Z).
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths/125KB), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express preflight fingerprint, WS token in URL query, undocumented /health, audio_url/callback SSRF-by-design (key-gated), single-key auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); redirect_to form-action reflection post-auth unverified; strict CSP; return-to signed-reset (REJECTED)
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; `gladia`@0.1.3 impersonation anomaly sole reportable candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url + callback SSRF fetch): 6.6 = attack7 business9 tech6 gate2 cloud9 fresh5
[PRIO] app.gladia.io /signin (OAuth redirect_to reflection): 6.1 = attack6 business8 tech7 gate7 cloud1 fresh4
[PRIO] npm registry `gladia`@0.1.3: 5.5 = attack5 business7 tech4 gate10 cloud1 fresh3
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback_config) + legacy /video|/audio/text/*
confidence: 72
reasoning: live spec re-verified 23:48Z — audio_url accepted verbatim (format:uri, no allowlist), CallbackConfigDto.url same; /v1/models confirms FR/US egress; jobs return status/error_message/duration = measurable reachability signal; SDK source shows is_url()/uploadFile() only gates upload-vs-direct path, no host/scheme guard.
evidence_needed: key-gated fetch of 169.254.169.254 / internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback":true,"callback_config":{"url":"http://169.254.169.254:80/"}}; compare error/timing.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] Name-squat `gladia` npm package is unofficial / hijack risk
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 80
reasoning: registry description "Official TypeScript SDK for Gladia" vs packaged README "Unofficial"; maintainer softwarecitadel (personal gmail), repo alexisbouchez/gladia.ts; published 2025-04-07 pre-dating @gladiaio/sdk; re-confirmed live 23:48Z, tarball benign.
evidence_needed: none — metadata verified; affiliation check via Gladia disclosure channel pending.
verify_steps: PASSIVE — done (registry metadata + publish times + repo field + maintainer re-confirmed 23:48Z)
impact: developers installing `gladia` run unofficial code; repo/account hijack → supply-chain compromise; Medium
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: live re-probe 23:48Z — /signin?redirect_to=https://evil.example.com returns 200, param reflected URL-encoded into form action; return-to cookie is unsigned base64url JSON {"url":"/"} confirming server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: final post-auth HTTP 302 Location resolving to external host after Google sign-in with redirect_to set; or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[PARKED] /v1/history query-param deep-parsing injection (BUSLOGIC, conf 48): key-gated, marginal ROI, confidence at floor; retained in leads only.
[FINAL] 1) SSRF audio_url/callback (72, High impact) 2) `gladia` npm impersonation (80, Medium) 3) redirect_to post-auth OATH (60, Medium/High-if-redirect_uri).
[NEXT] HUMAN: request program-provided or personal trial `x-gladia-key` (sole standing blocker — passive recon is saturated and frozen at 23:48Z); then POST https://api.gladia.io/v2/pre-recorded {"audio_url":"http://169.254.169.254/latest/meta-data/"} vs {"audio_url":"http://<attacker-canary>"}, compare status/error_message/duration; repeat video_url on /video/text/video-transcription, then callback_config to internal port. Secondary (parallel passive): RAG diff of alexisbouchez/gladia.ts source vs @gladiaio/sdk for code-level impersonation evidence.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: full surface re-probe 23:48Z byte-identical to 23:08Z (openapi 125131B/14 paths, /v1/models 530B, /health 15B, 401 gate, preflight x-powered-by differential) — no drift, nothing new to report.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 (softwarecitadel, alexisbouchez/gladia.ts) + @gladiaio/sdk@1.1.0 metadata static 23:48Z — supply-chain surface unchanged.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com form-action reflection re-confirmed 23:48Z — reflection surface persists, post-auth honoring still AUTH_HELPED.
[RISK] api.gladia.io: 82 — public OpenAPI (14 paths/125KB), CORS wildcard + x-gladia-key permitted cross-origin (no creds), x-powered-by Express preflight fingerprint, WS token in URL query, undocumented /health, audio_url/callback SSRF-by-design (key-gated), single-key auth model
[RISK] app.gladia.io: 52 — Google-only OAuth limits bypass; /dashboard 200 SPA w/o auth (client-side enforcement); redirect_to form-action reflection post-auth unverified; strict CSP; return-to signed-reset (REJECTED)
[RISK] sdk: 45 — official @gladiaio/sdk 1.1.0 + gladiaio-sdk PyPI clean; `gladia`@0.1.3 impersonation anomaly sole reportable candidate; gladia-quiz-app pins old @gladiaio/sdk@0.5.2
## 2026-08-08 00:43:25 UTC [api] (model bigpickle)
[HYP] `gladia`@0.1.3 ships internal README titled "Unofficial" while package.json/npm-search says "Official" — active impersonation, plus raw API key in WS URL query (diverges from official SDK's token-in-URL after /v2/live init)
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 85
reasoning: tarball RAG this cycle — README.md line 3 "Unofficial TypeScript SDK" vs package.json description "Official TypeScript SDK for Gladia" in the SAME shipped artifact; client.ts:307 `wsUrl.searchParams.append('x-gladia-key', this.apiKey)` puts live key in WS query string; official sdk-1.1.0 session.ts:140-146 instead POSTs init and connects to returned token URL; no malicious code found (no postinstall/eval/exec).
evidence_needed: none — artifact-level contradiction and WS-key-in-URL verified from tarball; affiliation check still needs Gladia disclosure channel.
verify_steps: PASSIVE — done (tarball extraction + source diff this cycle, 2026-08-08 00:42Z)
impact: developers installing `gladia` run unofficial code; raw API keys exposed in WS URLs (access-log/history/proxy capture) on every realtime session → Medium (impersonation) + Medium (key-hygiene)
testability: PASSIVE
[HYP] SSRF via audio_url server-side fetch + callback_url outbound POST
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, callback/callback_config) + legacy /video|/audio/text/*
confidence: 72
reasoning: spec live 2026-08-08 00:42Z still shows audio_url/CallbackConfigDto.url format:uri with no scheme allowlist; official SDK prerecorded/client.ts:15-16 only isUrl() gates upload-vs-direct (URLs forwarded verbatim to API); /v1/models confirms FR/US egress; jobs return status/error_message/duration = measurable reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254 / internal host reflected in error_message/status/duration; or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: re-probed 200 2026-08-08 00:42Z — redirect_to reflected URL-encoded into form action; unsigned base64url return-to cookie {"url":"/"} confirms server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: final post-auth HTTP 302 Location resolving to external host after Google sign-in with redirect_to set; or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[NEXT] RAG: document the `gladia`@0.1.3 artifact-level finding for the report — tarball README "Unofficial" vs package.json "Official" contradiction + `x-gladia-key` raw-in-WS-URL (client.ts:307) vs official SDK token-in-URL-after-init (session.ts:140); then request program `x-gladia-key` for the standing SSRF POST test (sole remaining gate — passive surface frozen 3 consecutive cycles).
## 2026-08-08 02:47:01 UTC [api] (model bigpickle)
[HYP] `gladia`@0.1.3 is now an orphaned impersonation package — source repo alexisbouchez/gladia.ts returns 404 while dist-tag latest persists
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 88
reasoning: this cycle — `api.github.com/repos/alexisbouchez/gladia.ts` AND `api.github.com/users/alexisbouchez` both 404 with x-ratelimit-remaining 50 (real, not throttled); registry still lists repo field `git+https://github.com/alexisbouchez/gladia.ts.git`, description "Official TypeScript SDK for Gladia", maintainer softwarecitadel@gmail.com; tarball re-extracted: README.md:3 "Unofficial" vs package.json:4 "Official". Repo deletion removes the only public source for disclosure/verification — package is unfixable and untrackable at source level.
evidence_needed: none at registry level — repo 404 + artifact contradiction verified fresh; residual unknown = whether account was renamed (fork/search check) vs deleted; affiliation check pending Gladia disclosure channel.
verify_steps: PASSIVE — done (registry metadata 0.1.3, tarball README/package.json diff, GitHub API repo+user 404, web 404, rate-limit confirmed); optional follow-up: GitHub search for renamed `gladia.ts` forks.
impact: developers installing `gladia` (dist-tag latest, top search result) run unofficial code from a now-unreachable repo; repo/account hijack impossible to remediate at source; raw `x-gladia-key` in WS query string (client.ts:307) leaks key to access-log/proxy on every realtime session → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 72
reasoning: spec live shows audio_url/CallbackConfigDto.url `format:uri` with no scheme allowlist; official SDK prerecorded client only isUrl() gates upload-vs-direct (URLs forwarded verbatim); /v1/models confirms FR/US egress; jobs return status/error_message/duration reachability signal. Unchanged 4 cycles.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: re-probed 200 — redirect_to reflected URL-encoded into form action; unsigned base64url return-to cookie {"url":"/"} confirms server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: post-auth 302 Location resolving to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[NEXT] RAG: finalize the `gladia`@0.1.3 report writeup with this cycle's delta — (a) source repo alexisbouchez/gladia.ts + user account now 404 (orphaned, disclosure path severed), (b) tarball README "Unofficial" vs package.json "Official" contradiction (re-verified), (c) client.ts:307 raw `x-gladia-key` in WS query vs official sdk session.ts:140 token-after-init; output report section + disclosure-readiness summary for human; then escalate HUMAN for program `x-gladia-key` to unblock SSRF POST test (ranked #2, sole remaining gate, surface frozen 4 cycles).
## 2026-08-08 04:01:08 UTC [api] (model bigpickle)
[FINAL] 1) SSRF audio_url (api, 72) 2) `gladia`@0.1.3 impersonation (npm, 88→report-ready) 3) redirect_to OATH (app, 60)
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via the official `gladia.io/bug-bounty-report` form (evidence: tarball sha256 3b23ec7d..., README "Unofficial" vs package.json "Official", repo alexisbouchez/gladia.ts 404, client.ts:307 raw-key-in-WS-URL) — this cycle's security.txt discovery closes the long-pending affiliation/disclosure gap; in parallel, request an authorized `x-gladia-key` from security@gladia.io citing the program page (SSRF is a qualifying class; "contact security@gladia.io if in doubt about authorization") to run the single-key /v2/pre-recorded canary test on own data only — sole remaining gate for the top-ranked SSRF POC, frozen surface for 7 cycles.
## 2026-08-08 05:08:26 UTC [api] (model bigpickle)
[PRIO] api.gladia.io — priority 6.55 — attack 8, business 9, tech 6, gate 2 (key-gated), cloud 8 (FR/US egress, SSRF-by-design), fresh 3
[PRIO] npm `gladia`@0.1.3 — priority 5.75 — attack 3, business 7, tech 5, gate 10 (no auth), cloud 2, fresh 8 (re-verified)
[PRIO] app.gladia.io — priority 5.60 — attack 6, business 7, tech 6 (OAuth SSO), gate 5 (unauth reflection / post-auth gate), cloud 2, fresh 5
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 72
reasoning: spec live (openapi 125131B, sha256 979f3731…) still shows audio_url/CallbackConfigDto.url format:uri with no scheme allowlist; official SDK prerecorded client only isUrl() gates upload-vs-direct (URLs forwarded verbatim); /v1/models confirms FR/US egress; jobs return status/error_message/duration reachability signal. Unchanged 8 cycles.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 is an orphaned impersonation package at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3 (dist-tag latest)
confidence: 88
reasoning: npm view fresh — description "Official TypeScript SDK for Gladia", repo git+https://github.com/alexisbouchez/gladia.ts.git, maintainer softwarecitadel; repo + user 404 (orphaned); tarball sha256 3b23ec7d… has README "Unofficial" vs package.json "Official"; client.ts:307 raw x-gladia-key appended to WS query vs official sdk-1.1.0 session.ts:140 token-after-init. Disclosure channel now confirmed as bug-bounty-report Google Form (login-gated).
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia confirmation via form.
verify_steps: PASSIVE — done (npm view, tarball diff, GitHub API repo/user 404); submission via form is the only remaining step.
impact: devs on `gladia` run unofficial code; raw keys in WS URLs (access-log/proxy capture) → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: re-probed this cycle — ?redirect_to=https://evil.example.com reflected into form action (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"), no host allowlist at unauthenticated layer; unsigned base64url return-to cookie confirms server-driven redirect concept; distinct from REJECTED cookie-tampering vector.
evidence_needed: post-auth 302 Location resolving to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] 1) `gladia`@0.1.3 impersonation (npm, 88) 2) SSRF audio_url (api, 72) 3) redirect_to OATH (app, 60)
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via the confirmed disclosure channel gladia.io/bug-bounty-report (Google Form, live this cycle; NOT security.txt which is 404) — evidence: tarball sha256 3b23ec7d…, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 (orphaned), client.ts:307 raw key in WS URL vs official token-after-init; in the same engagement request an authorized `x-gladia-key` to run the /v2/pre-recorded canary POST on own data only (sole remaining gate for top-impact SSRF, surface frozen 8 cycles).
[RISK] api.gladia.io: 55 — live SSRF-by-design fetch surface (audio_url/video_url/callback_url, no scheme allowlist) + undocumented /health + CORS wildcard-with-x-gladia-key, all key-gated; exploit depends on key procurement
[RISK] app.gladia.io: 45 — unauthenticated redirect_to reflection (post-auth honoring unverified) + client-side-only auth on /dashboard SPA; OAuth SSO in path
[RISK] sdk: 50 — orphaned impersonation `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern; official @gladiaio/sdk@1.1.0 clean
## 2026-08-08 05:58:52 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 72
reasoning: openapi 125131B sha256 979f3731 unchanged (cycle 9) — audio_url/video_url/CallbackConfigDto.url `format:uri`, no scheme allowlist; SDK forwards URLs verbatim; /v1/models confirms FR/US egress; storage host files.gladia.io in spec. Jobs expose status/error_message/duration reachability signal.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key: POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 is an orphaned impersonation package at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 88
reasoning: fresh npm view this cycle — dist-tag latest=0.1.3, 4 versions [0.1.0-0.1.3], repo git+github.com/alexisbouchez/gladia.ts (repo+user 404, orphaned), author alexisbouchez, maintainer softwarecitadel; tarball sha256 3b23ec7d… README "Unofficial" vs package.json "Official"; client.ts:307 raw x-gladia-key in WS query vs official token-after-init.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia via bug-bounty form.
verify_steps: PASSIVE — done (npm view, tarball diff, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed alive (form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com", no host allowlist at unauth layer); unsigned base64url return-to cookie confirms server-driven redirect concept; protected routes are server-side 302 (auth gate real, not client-only).
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d…, README "Unofficial" vs package.json "Official", repo+account 404 orphaned, client.ts:307 raw key in WS URL) AND in the same submission request an authorized `x-gladia-key` for a self-own-data /v2/pre-recorded canary (169.254.169.254) — sole remaining gate for the top-impact SSRF; surface frozen 9 cycles, this cycle added only out-of-scope files.gladia.io reference and a clean-app-bundle negative.
## 2026-08-08 07:10:02 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: live spec this cycle unchanged — audio_url/video_url/CallbackConfigDto.url `format:uri`, no scheme allowlist; SDK forwards URLs verbatim (isUrl() gates upload-vs-direct only); /v1/models confirms FR/US egress; new: ≥2 backend instances confirmed, so the fetch pool/egress is split — two canary targets needed per instance.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; repeat across ≥2 requests to cover both instances; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 is an orphaned impersonation package at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 88
reasoning: fresh this cycle — dist-tag latest=0.1.3, 4 versions [0.1.0–0.1.3], maintainer softwarecitadel <softwarecitadel@gmail.com>; source repo alexisbouchez/gladia.ts + user 404 (orphaned); tarball sha256 3b23ec7d… README "Unofficial" vs package.json "Official"; client.ts:307 raw x-gladia-key in WS query vs official token-after-init.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission via gladia.io/bug-bounty-report form is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed fresh this cycle (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com", no host allowlist at unauth layer); unsigned base64url return-to cookie confirms server-driven redirect concept; protected routes are real 302 (auth gate server-side).
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation (npm, 88) 2) SSRF audio_url (api, 73) 3) redirect_to OATH (app, 60)
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d…, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw key in WS URL vs official token-after-init) AND request in the same submission an authorized `x-gladia-key` for a self-own-data /v2/pre-recorded canary (169.254.169.254) — sole remaining gate for top-impact SSRF; new this cycle: run the canary ≥2x to cover the confirmed dual-instance egress pool.
## 2026-08-08 08:00:04 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: structure-sans-examples re-verified unchanged this cycle — audio_url/video_url/CallbackConfigDto.url `format:uri`, no scheme allowlist; SDK forwards URLs verbatim (isUrl() gates upload-vs-direct only); /v1/models confirms FR/US egress; spec is generated live by the backend (request_id format matches runtime).
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url on /video/text/video-transcription; then {"callback_config":{"url":"http://169.254.169.254:80/"}}; run ≥2x to cover the dual-instance egress pool; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 is an orphaned impersonation package at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 88
reasoning: fresh npm view — dist-tag latest=0.1.3, integrity sha512-56NWQ9pEVyd… unchanged; source repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official"; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 3b23ec7d…, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed fresh (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com", no host allowlist at unauth layer); unsigned base64url return-to cookie confirms server-driven redirect concept; protected routes are real server-side 302.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google OAuth with ?redirect_to=https://evil.example.com and //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[NEXT] PROBE: confirm the dynamic-spec observation is systemic — three fetches of https://api.gladia.io/openapi.json spaced 30s apart must each yield a distinct sha256 while structure-sans-examples stays identical; if so, replace all future drift checks with a examples-stripped structural hash and record the generated `request_id`/`created_at` examples as a live-backend fingerprint (ties spec to runtime). Standing HUMAN dependency unchanged: submit gladia@0.1.3 report + request authorized key for the SSRF canary.
[RISK] api.gladia.io: 45 — frozen key-gated v2 surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; preflight-only x-powered-by fingerprint + dynamic spec generation aid targeting, but no proven exploitable path without a key | app.gladia.io: 35 — confirmed unauth redirect_to reflection without host allowlist, but post-auth honoring unproven; SPA client-side /dashboard gate; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern; official @gladiaio/sdk@1.1.0 clean
## 2026-08-08 08:56:36 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged — URL fields `format:uri`, no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; ≥2 backend instances confirmed (prior), now independently supported by 2 distinct frozen example timestamps in dynamic spec.
evidence_needed: key-gated fetch of 169.254.169.254 reflected in error/status/duration, or callback POST at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"}, then http://169.254.169.254/latest/meta-data/; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress; compare status/error_message/duration.
impact: cloud-metadata + internal-net read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed fresh (form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`); dual email-password + Google SSO paths now visible in form (`name="intent"`); protected routes are real server-side 302; unsigned return-to cookie confirms server-driven redirect concept.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[HYP] openapi.json example values fingerprint per-instance backend codegen
class: OTHER
asset: api.gladia.io /openapi.json
confidence: 55
reasoning: 3 fetches → 2 distinct byte hashes, only `offset` example timestamps differ; values frozen at 2026-08-07T21:00:31/35Z (not now-tracking) — consistent with per-instance swagger generation across the ≥2 confirmed backend instances, not request-time generation.
evidence_needed: sampling showing the same 2 (not more) distinct example values recurring, correlated with distinct backend identity.
verify_steps: PASSIVE — fetch /openapi.json N=10, group by example timestamp value; if exactly 2 stable values recur, per-instance codegen is the mechanism → use one canary target per distinct value for SSRF egress coverage.
impact: instance-correlation only — sharpens dual-instance SSRF canary targeting → Low (intel)
testability: PASSIVE
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via the gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/) — sole remaining gate for the top-impact finding; run the canary ≥2x to cover the dual-instance egress pool.
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; dynamic spec + per-instance fingerprint improve targeting but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path (email-password + Google SSO) widens redirect_uri injection surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern; official @gladiaio/sdk@1.1.0 clean, tarball hash unchanged
## 2026-08-08 09:45:10 UTC [api] (model bigpickle)
[CHANGED] api.gladia.io /openapi.json: example-timestamp fingerprint is NOT a stable per-instance set — 3 fresh fetches returned 3 distinct values (21:00:25.976Z, 21:00:32.264Z, 21:00:26.548/9Z) vs prior-observed 31Z/35Z; ≥4 distinct values now recorded → prior "2 stable values = per-instance codegen" model falsified
[NEW] api.gladia.io: structural hash (examples-stripped) STABLE at sha256 9a326c924644b59854b0cafddb5f477c23d6d1cfb8c220f0ff5bf689c3c61c7b across all 3 fetches → validated drift baseline replacing byte-hash (byte hash differs every fetch due to timestamp examples)
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged — URL fields `format:uri`, no scheme allowlist; SDK forwards verbatim (isUrl() gates upload-vs-direct only); /v1/models confirms FR/US egress; ≥2 backend instances confirmed; structural-hash baseline now validated for clean drift detection.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error_message/status/duration, or callback POST observed at internal listener.
verify_steps: AUTH_HELPED — with x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"}, then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress; compare status/error_message/duration.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 is an orphaned impersonation package at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; source repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 raw x-gladia-key in WS query; tarball sha256 3b23ec7d…802f2 unchanged.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 3b23ec7d…, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium (impersonation) + Medium (key hygiene)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed (form `action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"`); dual email-password + Google SSO intent paths visible; protected routes are real server-side 302; unsigned return-to cookie confirms server-driven redirect concept.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[PARKED] openapi.json example timestamps fingerprint per-instance codegen: FALSIFIED by fresh data — 3 fetches → 3 distinct values (25.976/32.264/26.548Z) beyond the 2 recorded (31/35Z); timestamp cluster is a single-deploy-window artifact, not instance identity; structural hash is the correct drift metric
[FINAL] re-ranked:
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED OTHER @ api.gladia.io: per-instance codegen fingerprint hypothesis falsified — 3 fresh fetches → 3 distinct example timestamps (25.976/32.264/26.548Z) beyond recorded 31/35Z; values are a deploy-window artifact, not instance identity
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: structural hash 9a326c92… (examples-stripped) stable across 3 fetches → validated drift baseline; raw byte hash varies per fetch due to timestamp examples
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT this cycle (09:44 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline now validated but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path (email-password + Google SSO) widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball hash unchanged
## 2026-08-08 10:17:13 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; 14-path frozen surface, key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback observed at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 raw x-gladia-key in WS query; tarball sha256 `3b23ec7d…7f2` unchanged.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed (form action URL-encodes redirect_to); dual email-password + Google SSO intent paths; protected routes real server-side 302; unsigned return-to cookie.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[HYP] SSRF (73): survives — not on REJECTED list, concrete AUTH_HELPED steps, sole gate is a key. RETAINED #1.
[HYP] npm impersonation (95): survives — PASSIVE-verified end-to-end, submission pending. RETAINED #2.
[HYP] redirect_to OATH (60): survives — weakest, post-auth honoring unproven across 9 cycles; keep but deprioritize until a key frees the SSRF path. RETAINED #3.
[PARKED] none dropped (all ≥40, none on REJECTED list, all have concrete verify_steps).
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (60, AUTH_HELPED).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via the gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 9 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, signin reflection, /dashboard 200 — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ api.gladia.io: recorded structural-hash baseline `9a326c92…` is not reproducible without the original strip recipe — my normalization yields `a7fa3286…`; size+path count remain the robust drift check until the recipe is pinned
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed — shasum `cc96f84a…` current dist-shasum, source repo alexisbouchez/gladia.ts + user 404, dist-tag latest persists; @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven across 9 cycles; dual auth path (email-password + Google SSO) widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 10:56:17 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged 10th cycle — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (packages/sdk-js/client.ts, sdk-python/v2/prerecorded/core.py); /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback observed at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; shasum `cc96f84a…` unchanged; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed across cycles (form action URL-encodes redirect_to); dual email-password + Google SSO intent paths; protected routes real server-side 302; unsigned return-to cookie.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (60, AUTH_HELPED, weakest).
[PARKED] none dropped — all ≥40, none on REJECTED list, all have concrete verify_steps.
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: NO_DRIFT across 10 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 10 cycles but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 11:36:48 UTC [api] (model bigpickle)
[PRIO] npm registry `gladia`@0.1.3 (orphaned impersonation): score 6.55 | attack 6 business 7 tech 6 gate 10 cloud 1 fresh 8
[PRIO] api.gladia.io POST /v2/pre-recorded (SSRF fetch surface): score 6.75 | attack 8 business 8 tech 7 gate 2 cloud 8 fresh 6
[PRIO] app.gladia.io /signin (redirect_to reflection/OATH): score 5.80 | attack 6 business 6 tech 6 gate 8 cloud 1 fresh 6
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged 11th cycle — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; shasum `cc96f84a…`/integrity stable; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed 11:36Z (form action URL-encodes redirect_to); dual email-password + Google SSO intent paths; protected routes real server-side 302; unsigned return-to cookie.
evidence_needed: post-auth 302 Location to external host, or redirect_to reused as OAuth redirect_uri.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie; test redirect_to-as-redirect_uri.
impact: post-auth phishing redirect; OAuth code/state theft if redirect_uri injectable → Medium (High if proven)
testability: AUTH_HELPED
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (60, AUTH_HELPED, weakest).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a200c0fd49a71e919391f9b659c39f3e9`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 11 cycles (23:08→11:36 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — shasum `cc96f84a…` + integrity sha512-56NWQ9pEVyd/… unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest persists, @gladiaio/sdk@1.1.0 static (fresh 11:36 UTC)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 11 cycles but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; dual auth path widens redirect_uri surface; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 12:01:45 UTC [api] (model bigpickle)
## 2026-08-08 13:10:45 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec unchanged 12th cycle — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 (re-verified live); repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in WS query; @gladiaio/sdk@1.1.0 official unchanged.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect / OAuth redirect_uri injection)
class: OATH
asset: app.gladia.io /signin
confidence: 60
reasoning: reflection re-confirmed (form action URL-encodes redirect_to); OAuth initiation path carries redirect_to; server uses fixed redirect_uri for Google callback (redirect_uri injection already falsified); CSP lacks form-action.
evidence_needed: post-auth 302 Location to external host, or redirect_to honored on credential-callback return.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 12 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — dist-tag latest=0.1.3, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 12 cycles but no proven exploitable path without a key | app.gladia.io: 35 — unauth redirect_to reflection confirmed, post-auth honoring unproven; redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 14:02:04 UTC [api] (model bigpickle)
[PRIO] api.gladia.io: 6.15 — attack 7 / business 8 / tech 6 (OpenAPI+NestJS+WS, SSRF-by-design fields) / gate 4 (key-only) / cloud 7 (FR/US egress, IMDS reachable if key) / fresh 2
[PRIO] npm `gladia`@0.1.3: 5.30 — attack 4 / business 5 / tech 6 (raw key in WS URL) / gate 10 (public registry) / cloud 2 / fresh 5
[PRIO] app.gladia.io: 4.75 — attack 4 / business 7 / tech 5 (OAuth/SSO, form-action reflection) / gate 5 (unauth reflection, post-auth gated) / cloud 2 / fresh 3
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec frozen 13 cycles — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3, shasum `cc96f84a…` stable this cycle; repo alexisbouchez/gladia.ts + user 404; README "Unofficial" vs package.json "Official"; client.ts:307 raw x-gladia-key in WS query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed; CSP lacks form-action; OAuth redirect_uri injection already falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host header injection angle remains)
testability: AUTH_HELPED
[PARKED] none — all three survive: npm (95, submission-ready), api SSRF (73, only gate is key), app OATH (55, lowest — retained for completeness, confidence dropped from 60 on weakened impact case).
[FINAL] re-ranked: 1) npm `gladia`@0.1.3 impersonation (95, submission-ready) 2) api SSRF-by-design (73, key-gated) 3) app redirect_to OATH (55, AUTH_HELPED, weakest).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 13 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: impersonation persists — dist-tag latest=0.1.3, shasum `cc96f84a…` + integrity stable, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 static (fresh this cycle)
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 13 cycles but no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 14:49:09 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config)
confidence: 73
reasoning: spec frozen 14 cycles — URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (RAG of sdk-js + sdk-python core); /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x to cover dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed live 14:48 UTC (form action URL-encodes redirect_to); CSP lacks form-action; OAuth redirect_uri injection already falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. Standing gate for the top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 14 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive 14:48 UTC — form action reflects URL-encoded value; no host allowlist at unauth layer; post-auth honoring sole unverified gate
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields (audio_url/video_url/callback_url) gated solely by key; drift baseline validated across 14 cycles but no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 15:18:10 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 15 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key is sole gate; GET {id}/file key-gated so no unauthenticated retrieval.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" same artifact; client.ts:307 raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 14:48 UTC; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
## 2026-08-08 15:52:12 UTC [api] (model bigpickle)
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 15 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key is sole gate; GET {id}/file key-gated so no unauthenticated retrieval.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 14:48 UTC; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
## 2026-08-08 17:03:15 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 16 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key is sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback to internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh this cycle; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
[FINAL] 1) npm impersonation [95] 2) api SSRF [73] 3) app redirect_to post-auth [55]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL) and request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); run the canary ≥2x to cover the dual-instance egress pool. This unblocks both the [95] report and the [73] SSRF top finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 16 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen, nothing new to report
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; post-auth honoring sole unverified gate
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields gated solely by key; drift baseline validated across 16 cycles but no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 17:43:55 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 17 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key is sole gate (401 NestJS shape confirmed).
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 14:48 UTC; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium (Low-Medium given no Host-header angle remains)
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" contradiction, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query) and in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); on approval run the canary ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool — this unblocks both the [95] report and the [73] top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 17 cycles (23:08→17:43 UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential (OPTIONS 204 xpb=Express, GET/POST 401 xpb absent), CORS static wildcard — surface frozen, nothing new to report
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields gated solely by key; drift baseline validated across 17 cycles, no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 18:15:03 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 20+ cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key sole gate (401 NestJS shape re-confirmed this cycle).
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh this cycle; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query) and in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); on approval run the canary ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool — this unblocks both the [95] report and the [73] top api finding.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh 17:52 UTC (openapi 125131B/14 paths, /health 15B, /v1/models 530B, preflight-only x-powered-by differential, CORS static wildcard) — 20+ cycles frozen, no new endpoints or headers
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection confirmed alive fresh 17:52 UTC — form action reflects URL-encoded value; no host allowlist at unauth layer; post-auth honoring sole unverified gate
[RISK] api.gladia.io: 45 — frozen 14-path key-gated surface with SSRF-by-design fetch fields gated solely by key; drift baseline validated across 20+ cycles, no proven exploitable path without a key | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 19:05:56 UTC [api] (model bigpickle)
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ /video/text/video-transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 20+ cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim (sdk-js/sdk-python RAG); /v1/models confirms FR/US egress; key sole gate (401 NestJS shape re-confirmed).
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3; repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs (access-log/proxy capture) → Medium impersonation + Medium key hygiene
testability: PASSIVE
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 17:52 UTC; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); unsigned return-to cookie resets on tamper.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/); on approval run the canary ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool — unblocks both [95] and [73].
[RISK] api.gladia.io: 46 — frozen key-gated surface (20+ cycles) with SSRF-by-design fetch fields gated solely by key and SSRF canary unproven; new nginx/1.28.2 banner + public Swagger UI mirror add marginal fingerprint surface only | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection falsified, return-to cookie tamper-reset REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 19:42:37 UTC [api] (model bigpickle)
[NEW] npm registry: adjacent-namespace squat scan returned all-404 for `gladiaio`, `gladia-sdk`, `gladia-sdk-ts`, `gladiaio-sdk`, `gladia-ts`, `gladia-ai`, `gladia-stt`, `@gladia/sdk`, `@gladia/sdk-js`, `@gladiaio/transcription`, `@gladiaio/client` — no NEW impersonators beyond `gladia`@0.1.3
[NEW] npm registry: maintainer `softwarecitadel` controls only `@softwarecitadel/girouette` (AdonisJS decorators, unrelated) — no broader squat campaign by that account
[NEW] api.gladia.io: surface re-probe byte-identical — openapi 200/125131B, /health 200/15B, /v1/models 200/530B (22nd frozen cycle)
[PRIO] api.gladia.io POST /v2/pre-recorded: score 6.4 — attack 8, business 9, tech 6, gate 1 (key-gated), cloud 8 (FR/US metadata egress), fresh 3
[PRIO] npm `gladia`@0.1.3: score 5.8 — attack 5, business 7, tech 5, gate 10 (public install), cloud 0, fresh 5
[PRIO] app.gladia.io /signin redirect_to: score 5.0 — attack 3, business 7, tech 4, gate 10, cloud 0, fresh 4
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 22 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress (re-probed this cycle); key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 (re-verified); repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query; adjacent-namespace scan confirms isolated, no campaign.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed prior cycles; CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback URI); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" in same artifact, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool, unblocking both [95] and [73].
[LEARN] ACCEPTED OTHER @ npm registry: adjacent-namespace squat scan all-404 (gladiaio, gladia-sdk, gladia-ts, gladia-ai, gladia-stt, @gladia/*, @gladiaio/*) and maintainer softwarecitadel controls only unrelated @softwarecitadel/girouette — `gladia`@0.1.3 is an ISOLATED impersonator, no broader campaign
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT fresh (openapi 125131B/14 paths, /health 15B, /v1/models 530B) — 22nd frozen cycle, nothing new to report
[RISK] api.gladia.io: 46 — frozen key-gated surface with SSRF-by-design fetch fields gated solely by key, canary unproven without authorized token | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, sole impersonator confirmed isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 20:10:01 UTC [api] (model bigpickle)
## 2026-08-08 20:48:53 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 23 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress (re-probed this cycle); key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 (re-verified this cycle); repo alexisbouchez/gladia.ts + user 404 (orphaned); README "Unofficial" vs package.json "Official" in same artifact; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query; adjacent-namespace scan confirms isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed this cycle (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report Google Form (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official" contradiction, source repo+account 404 orphaned, client.ts:307 raw x-gladia-key in WS URL query, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover the FR/US egress pool, unblocking both [95] and [73].
[RISK] api.gladia.io: 46 — frozen key-gated surface (23 cycles) with SSRF-by-design fetch fields gated solely by key and SSRF canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 21:16:57 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 24 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; GET/POST + /{id} all 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded {"audio_url":"http://<canary>"} then {"audio_url":"http://169.254.169.254/latest/meta-data/"}; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3, description "Official" vs README "Unofficial" in same artifact; repo alexisbouchez/gladia.ts + user 404 (orphaned); shasum `cc96f84a…`; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query; adjacent-namespace scan confirms isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
## 2026-08-08 21:51:14 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 24 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed this cycle (shasum `cc96f84a…`); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss://.../v2/live?token query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback `https://app.gladia.io/auth/google/callback`, returns 200); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+account 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (http://169.254.169.254/latest/meta-data/) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 24 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP full set re-captured, form-action directive still absent; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (24 cycles) with SSRF-by-design fetch fields gated solely by key and canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 22:21:19 UTC [api] (model bigpickle)
[PRIO] api.gladia.io /v2/pre-recorded (audio_url/video_url/callback_url): 5.95 = attack7/biz8/tech6/gate2/cloud8/fresh2
[PRIO] npm `gladia`@0.1.3: 5.30 = attack3/biz7/tech6/gate10/cloud2/fresh2
[PRIO] app.gladia.io /signin redirect_to: 4.85 = attack5/biz6/tech5/gate7/cloud1/fresh2
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 25 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed this cycle (shasum `cc96f84a…`, repo alexisbouchez/gladia.ts); README "Unofficial" vs package.json "Official"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh this cycle (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+account 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 25 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP lacks form-action; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (25 cycles) with SSRF-by-design fetch fields gated solely by key and canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 22:55:39 UTC [api] (model bigpickle)
[PRIO] api.gladia.io /v2/pre-recorded (audio_url/video_url/callback_url): 5.85 = attack7/biz8/tech6/gate2/cloud8/fresh1
[PRIO] npm `gladia`@0.1.3: 5.20 = attack3/biz7/tech6/gate10/cloud2/fresh1
[PRIO] app.gladia.io /signin redirect_to: 4.75 = attack5/biz6/tech5/gate7/cloud1/fresh1
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url)
confidence: 73
reasoning: spec frozen 26 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed this cycle (shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 26 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP lacks form-action; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` + integrity sha512-56NW… unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (26 cycles) with SSRF-by-design fetch fields gated solely by key and canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-08 23:34:48 UTC [api] (model bigpickle)
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 26 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP lacks form-action; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` + integrity sha512-56NW… unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (26 cycles) with SSRF-by-design fetch fields gated solely by key and canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
confidence: 73
reasoning: spec frozen 26 cycles; URL fields `format:uri` no scheme allowlist; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed this cycle (shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 26 cycles (23:08→current) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; no host allowlist at unauth layer; CSP lacks form-action; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` + integrity sha512-56NW… unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (26 cycles) with SSRF-by-design fetch fields gated solely by key and canary unproven without authorized token; fingerprint surface limited to preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[NEW] api.gladia.io: OpenAPI 3.1 spec top-level `webhooks` key enumerates 7 outbound webhook topics (transcription.created/success/error + live.start_session/start_recording/end_recording/end_session) — previously unenumerated within the frozen 125131B spec; each posts to a client-supplied URL → reinforces callback-delivery SSRF/exfil surface. No `x-` vendor extensions anywhere in spec (components scanned clean). info.version=1.0.
[NEW] api.gladia.io: NO_DRIFT 27th cycle (23:33 UTC) — openapi 200/125131B/14 paths (structural sha256 a7fa3286… = normalization baseline), /health 15B, /v1/models 530B FR/US; spec servers=[https://api.gladia.io/], securitySchemes=[x_gladia_key] only.
[NEW] app.gladia.io: /signin?redirect_to=https://evil.example.com → 200, form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com` re-confirmed live 23:33 UTC; CSP full set re-captured — connect-src includes wss://*.gladia.io, frame-src includes billing.gladia.io + app.svix.com (webhook portal), NO form-action directive.
[CHANGED] npm: gladia@0.1.3 static — dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", maintainer softwarecitadel@gmail.com, repo alexisbouchez/gladia.ts, shasum cc96f84a… unchanged; @gladiaio/sdk@1.1.0 + gladiaio-sdk@1.0.5 static.
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url; webhooks key confirms outbound delivery)
confidence: 73
reasoning: spec frozen 27 cycles; URL fields `format:uri` no scheme allowlist; webhooks key adds 7 outbound POST topics to client-supplied URL; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback/webhook at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed (shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh 23:33 UTC (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 27 cycles (23:08→23:33 UTC) — openapi 125131B/14 paths (structural sha256 a7fa3286…), /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI 3.1 `webhooks` key enumerates 7 outbound webhook topics (transcription.* + live.*) posting to client-supplied URLs — part of frozen 125131B spec, no callback scheme allowlist; reinforces callback-delivery SSRF surface.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 23:33 UTC — form action reflects URL-encoded value; CSP re-captured full set, NO form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 + gladiaio-sdk@1.0.5 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (27 cycles) with SSRF-by-design fetch fields + 7 webhook callback topics gated solely by key and canary unproven without authorized token; fingerprint surface preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url; webhooks key confirms outbound delivery)
confidence: 73
reasoning: spec frozen 27 cycles; URL fields `format:uri` no scheme allowlist; webhooks key adds 7 outbound POST topics to client-supplied URL; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback/webhook at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed (shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh 23:33 UTC (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
## 2026-08-09 00:01:09 UTC [api] (model bigpickle)
reasoning: reflection re-confirmed fresh 23:33 UTC (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] 1) gladia@0.1.3 impersonation [95, PASSIVE, report-ready] 2) SSRF-by-design fetch [73, AUTH_HELPED] 3) post-auth redirect_to honoring [55, AUTH_HELPED]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 27 cycles (23:08→23:33 UTC) — openapi 125131B/14 paths (structural sha256 a7fa3286…), /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard, key-gated v2 — surface frozen, nothing new to report.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: OpenAPI 3.1 `webhooks` key enumerates 7 outbound webhook topics (transcription.* + live.*) posting to client-supplied URLs — part of frozen 125131B spec, no callback scheme allowlist; reinforces callback-delivery SSRF surface.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 23:33 UTC — form action reflects URL-encoded value; CSP re-captured full set, NO form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: orphaned impersonation confirmed fresh — shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts + user 404 (orphaned), dist-tag latest=0.1.3 persists, @gladiaio/sdk@1.1.0 + gladiaio-sdk@1.0.5 static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (27 cycles) with SSRF-by-design fetch fields + 7 webhook callback topics gated solely by key and canary unproven without authorized token; fingerprint surface preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection and cookie tamper both REJECTED; no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report ready, isolated impersonator); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[HYP] SSRF via audio_url/video_url/callback_url server-side fetch
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (+ video_transcription, callback_config.url; webhooks key confirms outbound delivery)
confidence: 73
reasoning: spec frozen 27 cycles; URL fields `format:uri` no scheme allowlist; webhooks key adds 7 outbound POST topics to client-supplied URL; SDK forwards verbatim; /v1/models confirms FR/US egress; all v2 ops 401 key-gated — key sole gate.
evidence_needed: key-gated fetch of 169.254.169.254/internal host reflected in error/status/duration, or callback/webhook at internal listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}`; repeat video_url + callback_config.url; run ≥2x for dual-instance egress.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed (shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission is the only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + Medium key hygiene
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh 23:33 UTC (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[HYP] SSRF-by-design via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_url, CallbackConfig/CallbackConfigDto.url; 7 webhook topics POST to same)
confidence: 73
reasoning: spec frozen 28 cycles; all URL fields `format:uri` with no scheme/host allowlist; webhooks mined this cycle confirm full transcript payloads POSTed to key-selected host; /v1/models confirms FR+US egress; every v2 op 401 key-gated — key is the sole gate.
evidence_needed: key-gated fetch of cloud-metadata/internal host reflected in error_code/timing, or transcript/status delivered to a canary listener.
verify_steps: AUTH_HELPED — with authorized key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` (self-own-data only); repeat video_url + callback_config.url; run ≥2x for FR/US egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed across cycles (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action directive; OAuth redirect_uri injection falsified (fixed `/auth/google/callback`); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (shasum `cc96f84a…`, integrity sha512-56NW…, tarball sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated; triage 23:17 marked VALID.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission is only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/` plus a private canary listener to receive a webhook POST) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [95] and [73].
[RISK] api.gladia.io: 46 — frozen key-gated surface (28 cycles), SSRF-by-design fetch + 7 callback/webhook POST topics gated solely by key, canary unproven without authorized token, fingerprint surface preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, isolated, VALID per triage); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 02:24:53 UTC [api] (model bigpickle)
testability: PASSIVE
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh 23:33 UTC (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action; OAuth redirect_uri injection falsified (fixed callback); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear); in the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/`) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress pool, unblocking [95] and [73].
[HYP] SSRF-by-design via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_url, CallbackConfig/CallbackConfigDto.url; 7 webhook topics POST to same)
confidence: 73
reasoning: spec frozen 28 cycles; all URL fields `format:uri` with no scheme/host allowlist; webhooks mined this cycle confirm full transcript payloads POSTed to key-selected host; /v1/models confirms FR+US egress; every v2 op 401 key-gated — key is the sole gate.
evidence_needed: key-gated fetch of cloud-metadata/internal host reflected in error_code/timing, or transcript/status delivered to a canary listener.
verify_steps: AUTH_HELPED — with authorized key POST /v2/pre-recorded `{"audio_url":"http://<canary>"}` then `{"audio_url":"http://169.254.169.254/latest/meta-data/"}` (self-own-data only); repeat video_url + callback_config.url; run ≥2x for FR/US egress pool.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed across cycles (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action directive; OAuth redirect_uri injection falsified (fixed `/auth/google/callback`); return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (shasum `cc96f84a…`, integrity sha512-56NW…, tarball sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + GitHub user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated; triage 23:17 marked VALID.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission is only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` for a self-own-data SSRF canary (`http://169.254.169.254/latest/meta-data/` plus a private canary listener to receive a webhook POST) — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [95] and [73].
[RISK] api.gladia.io: 46 — frozen key-gated surface (28 cycles), SSRF-by-design fetch + 7 callback/webhook POST topics gated solely by key, canary unproven without authorized token, fingerprint surface preflight-only x-powered-by | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, isolated, VALID per triage); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url/video_url/callback fetch+delivery): 6.45 — attack 6, business 10, tech 7 (NestJS/OpenAPI fetch-by-design), gate 2 (key sole gate), cloud 10 (metadata+internal egress FR/US), fresh 1
[PRIO] app.gladia.io /signin (redirect_to reflection → post-auth honoring): 5.20 — attack 4, business 8, tech 6 (OAuth/SSO), gate 8 (reflection at unauth layer), cloud 0, fresh 1
[PRIO] npm registry `gladia` 0.1.3 (orphaned impersonation at dist-tag latest): 4.75 — attack 3, business 6, tech 7 (supply-chain), gate 9 (public), cloud 0, fresh 1
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhooks topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 29 cycles (openapi 125131B/14 paths re-fetched 02:24Z); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated — key is sole gate.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}` (no_doom: metadata endpoint only if program explicitly authorizes); repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-own-data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 02:24Z (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP re-captured, no form-action directive; redirect_uri injection falsified (fixed `/auth/google/callback`); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 re-confirmed 02:24Z (shasum `cc96f84a…`, tarball sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated; triage 2026-08-08 VALID.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[PARKED] none — all three ≥40 confidence, classes not on REJECTED list, concrete verify_steps present.
[FINAL]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report to gladia.io/bug-bounty-report per triage-report recommendation (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, plus requested publish-date ordering + tarball diff evidence). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT across 29 cycles (23:08→02:24 UTC) — openapi 125131B/14 paths/7 webhooks, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static `*`+ACAH x-gladia-key — surface frozen, nothing new to report.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to= reflection re-confirmed alive 02:24 UTC — form action reflects URL-encoded value; CSP lacks form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 orphaned impersonation stable — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, repo+user alexisbouchez 404; @gladiaio/sdk@1.1.0 official static.
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (29th cycle) — audio_url/video_url/callback_config.url `format:uri` no scheme allowlist; webhooks 7 topics; /v1/models FR/US egress; key sole gate — SSRF-by-design persists (AUTH_HELPED).
[RISK] api.gladia.io: 46 — frozen key-gated surface (29 cycles); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 03:59:15 UTC [api] (model bigpickle)
## 2026-08-09 05:14:18 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhooks topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 30th cycle (openapi 125131B/14 paths re-fetched 05:13Z); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated — key sole gate.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}` (no_doom: metadata endpoint only if program explicitly authorizes); repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-own-data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed 05:13Z (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action directive; OAuth initiation now confirms PKCE+state+fixed redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (shasum `cc96f84a…`, tarball sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss URL query; adjacent-namespace scan all-404 → isolated; triage 2026-08-08 VALID.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73].
[RISK] api.gladia.io: 46 — frozen key-gated surface (30 cycles); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, OAuth hardening now verified (PKCE/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 06:03:19 UTC [api] (model bigpickle)
[PRIO] npm/sdk registry surface: 6.2 (attack 5, business 9, tech 6, gate 10, cloud 1, fresh 2) — public, gate-free, report-ready impersonation
[PRIO] api.gladia.io SSRF fetch+delivery surface: 5.6 (attack 7, business 8, tech 6, gate 1, cloud 7, fresh 1) — high-impact but key-gated only
[PRIO] app.gladia.io /signin redirect_to: 5.3 (attack 4, business 7, tech 5, gate 10, cloud 2, fresh 1) — unauth reflection confirmed, honoring unproven
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (shasum `cc96f84a…`, tarball sha256 `3b23ec7d…7f2`); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace scan all-404 → isolated; triage 2026-08-08 VALID.
evidence_needed: none at registry level — artifact contradiction + orphan verified; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 31st cycle (125131B re-fetched fresh); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated — key sole gate; no staging/alternate server leaked in spec.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}` (no_doom: metadata endpoint only if program explicitly authorizes); repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-own-data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 55
reasoning: reflection re-confirmed fresh 200 (form action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`); CSP lacks form-action directive; OAuth initiation PKCE+state+fixed redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[PARKED] none — all three ≥55, no class on REJECTED list, concrete verify_steps present.
[FINAL]
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 31st cycle (fresh probes 06:0x UTC) — openapi 125131B/14 paths, /health 15B, /v1/models 530B FR/US, OPTIONS 204 x-powered-by=Express + ACAO `*` + ACAH x-gladia-key, POST/GET 401 xpb absent — surface frozen.
[LEARN] ACCEPTED MISCONFIG @ api.gladia.io: spec `servers` enumerates single entry https://api.gladia.io only — no staging/alternate host leakage; example URLs point to generic callback.example + out-of-scope files.gladia.io example asset (no action).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh 200 — form action reflects URL-encoded value; CSP lacks form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm: `gladia`@0.1.3 orphaned impersonation stable — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, repo+user alexisbouchez 404; @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (31 cycles); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven, OAuth hardening verified (PKCE/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 07:12:17 UTC [api] (model bigpickle)
[PRIO] npm/sdk registry surface: 6.2 (attack 5, business 9, tech 6, gate 10, cloud 1, fresh 2) — public, gate-free, report-ready orphaned impersonation, sole action item not blocked by auth
[PRIO] api.gladia.io SSRF fetch+delivery surface: 5.6 (attack 7, business 8, tech 6, gate 1, cloud 7, fresh 1) — high-impact but gated solely by key; canary unproven without authorized token
[PRIO] app.gladia.io /signin redirect_to: 5.3 (attack 4, business 7, tech 5, gate 10, cloud 2, fresh 1) — unauth reflection confirmed 32nd cycle, post-auth honoring unproven
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists; repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace scan all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 32nd cycle (re-fetched 125131B this cycle); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh this cycle (action=/signin?redirect_to=https%3A%2F%2Fevil.example.com); CSP lacks form-action; OAuth initiation PKCE+state+fixed redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[PARKED] redirect_to post-auth honoring: not dropped (no REJECTED class, has steps, conf 50) but demoted to a tracking row — requires account creation/SSO completion which the program's passive-first rule ("no account creation") bars; 32 cycles with zero new evidence on the post-auth leg; revisit only if program authorizes an authenticated session. [FINAL] ranking: [1] npm impersonation 95 (report-ready) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on auth permission).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking the SSRF and OATH legs.
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 32nd cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 530B FR/US, preflight-only x-powered-by differential, CORS static wildcard — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; CSP has zero form-action occurrences (directive still absent); post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation stable — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, repo+user alexisbouchez 404; @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (32 cycles); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardening verified (PKCE/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 08:04:56 UTC [api] (model bigpickle)
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists; repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 33rd cycle (125131B re-fetched this cycle); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh (action=/signin?redirect_to=https%3A%2F%2Fevil.example.com); CSP lacks form-action; this cycle's OAuth-initiation probe re-confirms PKCE+state+fixed redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 33rd cycle (fresh probes this cycle) — openapi 200/125131B/14 paths, /health 15B no xpb on GET, /v1/models 530B FR/US, OPTIONS 204 x-powered-by=Express + ACAO `*` + ACAH x-gladia-key, GET 401 xpb absent — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /auth/google/callback now 302 → accounts.google.com full OAuth initiation (client_id, PKCE S256, fixed redirect_uri=https://app.gladia.io/auth/google/callback, state, access_type=offline) — previously 200; OAuth redirect_uri-injection class re-confirmed REJECTED; oauth2:<uuid> state cookie HttpOnly SameSite=Lax, Secure flag absent (site HSTS, trivial).
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; CSP lacks form-action directive; post-auth honoring sole unverified gate.
[RISK] api.gladia.io: 46 — frozen key-gated surface (33 cycles); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed, post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardening re-confirmed live this cycle (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged
## 2026-08-09 08:59:54 UTC [api] (model bigpickle)
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists; repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url/callback fetch+delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 34th cycle (125131B re-fetched this cycle, 14 paths/7 webhooks/single server); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh (200, action=/signin?redirect_to=https%3A%2F%2Fevil.example.com); CSP re-captured full set, form-action directive still ABSENT; OAuth initiation PKCE S256 + state + fixed redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] ranking: [1] npm impersonation 95 (report-ready) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on account-creation rule; 34 cycles zero new post-auth evidence).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 34th cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 530B, OPTIONS 204 x-powered-by=Express + ACAO `*`, GET 401 xpb absent — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com → 200 reflection alive fresh; CSP full set re-captured (connect-src incl. *.gladia.io + wss://*.gladia.io + google/hotjar/contentsquare/hubspot/axeptio; script-src nonce+strict-dynamic; object-src 'none'; base-uri 'self') — NO form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation stable — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, repo+user alexisbouchez 404, @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (34 cycles, byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 09:52:00 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url/video_url/callback fetch+delivery): score 6.2 | attack 7 business 9 tech 6 gate 2 cloud 8 fresh 2
[PRIO] app.gladia.io /signin redirect_to reflection: score 5.1 | attack 4 business 7 tech 5 gate 8 cloud 2 fresh 2
[PRIO] npm registry `gladia`@0.1.3: score 4.9 | attack 3 business 6 tech 4 gate 10 cloud 2 fresh 3
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 35th cycle (125131B re-fetched, 14 paths/7 webhooks/single server); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh this cycle (200/27448B, action=/signin?redirect_to=https%3A%2F%2Fevil.example.com); CSP form-action directive still absent; OAuth initiation PKCE S256 + state + FIXED redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (re-verified this cycle, shasum `cc96f84a…`, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts + user 404 (orphaned); package.json "Official" vs README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (npm view, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[FINAL] ranking: [1] npm impersonation 95 (report-ready, PASSIVE) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on no-account-creation rule; 35 cycles zero new post-auth evidence).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 35th cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 200/530B FR/US, /v2/pre-recorded 401 xpb absent, signin reflection 200/27448B — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; CSP lacks form-action directive; OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation stable — shasum `cc96f84a…` + integrity sha512-56NW… unchanged, dist-tag latest=0.1.3 persists, repo alexisbouchez/gladia.ts + user 404 (orphaned), @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (35 cycles byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified this cycle), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 10:27:10 UTC [api] (model bigpickle)
[PRIO] api.gladia.io POST /v2/pre-recorded (audio_url/video_url/callback fetch+delivery): score 6.2 | attack 7 business 9 tech 6 gate 2 cloud 8 fresh 2
[PRIO] app.gladia.io /signin redirect_to reflection: score 5.1 | attack 4 business 7 tech 5 gate 8 cloud 2 fresh 2
[PRIO] npm registry `gladia`@0.1.3: score 4.9 | attack 3 business 6 tech 4 gate 10 cloud 2 fresh 3
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 36th cycle (125131B re-fetched, 14 paths/7 webhooks/single server); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh this cycle (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP form-action directive still absent; OAuth initiation PKCE S256 + state + FIXED redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (re-verified this cycle, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts 404; description "Official" vs packaged README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (registry metadata, tarball sha256 3b23ec7d…, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[FINAL] ranking: [1] npm impersonation 95 (report-ready, PASSIVE) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on no-account-creation rule; 36 cycles zero new post-auth evidence). All three survive critique: conf ≥40, classes not on REJECTED list, concrete verify_steps present. No [PARKED] this cycle.
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…7f2`, shasum `cc96f84a…`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 36th cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 530B FR/US, /v2/pre-recorded 401/144 xpb absent — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; CSP lacks form-action directive; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation stable — latest=0.1.3, shasum cc96f84a… + integrity sha512-56NW… unchanged, repo alexisbouchez/gladia.ts 404, maintainer softwarecitadel@gmail.com, @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (36 cycles byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 11:04:40 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 37th cycle (125131B re-fetched, 14 paths/7 webhooks/single server); all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery; /v1/models confirms FR+US egress; every v2 op 401 key-gated.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh this cycle (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP form-action directive still absent; OAuth initiation PKCE S256 + state + FIXED redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (re-verified this cycle, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, integrity sha512-56NW… unchanged); repo alexisbouchez/gladia.ts 404; description "Official" vs packaged README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (registry metadata, tarball sha256 3b23ec7d…, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[FINAL] ranking: [1] npm impersonation 95 (report-ready, PASSIVE) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on no-account-creation rule; 37 cycles zero new post-auth evidence).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a200c0fd49a71e919391f9b659c39f3e9`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 37th cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 530B FR/US, OPTIONS 204 x-powered-by=Express + ACAO `*` + ACAH x-gladia-key, GET 401 xpb absent — surface frozen.
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to=https://evil.example.com reflection confirmed alive fresh — form action reflects URL-encoded value; CSP form-action directive still absent; post-auth honoring sole unverified gate.
[LEARN] ACCEPTED MISCONFIG @ app.gladia.io: CSP frame-src embeds out-of-scope third parties (svix.com, hyperline.co, billing.gladia.io/portal) — infra fingerprint only, no action.
[RISK] api.gladia.io: 46 — frozen key-gated surface (37 cycles byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 11:41:52 UTC [api] (model bigpickle)
[PRIO] api.gladia.io /v2/pre-recorded (audio_url/video_url/callback_config.url): score 6.9 = attack 7 + business 8 + tech 6 + gate 5 + cloud 7 + fresh 8
[PRIO] app.gladia.io /signin (redirect_to reflection): score 5.3 = attack 5 + business 7 + tech 6 + gate 9 + cloud 1 + fresh 5
[PRIO] npm `gladia`@0.1.3: score 5.8 = attack 6 + business 8 + tech 3 + gate 10 + cloud 2 + fresh 6
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec re-fetched this cycle — 14 paths/7 webhooks/single server frozen; all URL fields `format:uri` no scheme/host allowlist; webhooks key confirms outbound delivery to client-supplied URLs; /v1/models confirms FR+US egress; every v2 op 401 key-gated (re-confirmed 401/204 this cycle).
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of a self-owned canary, or webhook/callback POST received at a private canary listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; run ≥2x for FR/US egress pool; all self-owned data.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed across 38 cycles (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com"); CSP form-action directive still absent; OAuth initiation PKCE S256 + state + FIXED redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after completing Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists; repo alexisbouchez/gladia.ts + user 404 (orphaned); description "Official" vs packaged README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (registry metadata, tarball sha256 `3b23ec7d…`, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[FINAL] ranking: [1] npm impersonation 95 (report-ready, PASSIVE) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key) → [3] redirect_to 50 (tracking, blocked on no-account-creation rule; 38 cycles zero new post-auth evidence).
[NEXT] HUMAN: Submit the `gladia`@0.1.3 report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2`, shasum `cc96f84a200c0fd49a71e919391f9b659c39f3e9`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:307 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [73] and [50].
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT 38th cycle (fresh probes this cycle) — openapi 200/125131B/14 paths/7 webhooks/single server, /health 15B, /v1/models 530B FR/US, POST 401 xpb absent vs OPTIONS 204 x-powered-by=Express + ACAO `*` + ACAH x-gladia-key — surface frozen.
[LEARN] ACCEPTED OTHER @ npm `gladia`@0.1.3: orphaned impersonation stable — latest=0.1.3, shasum `cc96f84a…` unchanged, repo alexisbouchez/gladia.ts 404, maintainer softwarecitadel@gmail.com, @gladiaio/sdk@1.1.0 official static.
[RISK] api.gladia.io: 46 — frozen key-gated surface (38 cycles byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 12:16:24 UTC [api] (model bigpickle)
## 2026-08-09 13:26:45 UTC [api] (model bigpickle)
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec re-fetched this cycle — 125131B/14 paths/7 webhooks/single server frozen; all URL fields `format:uri` no scheme/host allowlist; /v1/models 530B confirms FR+US egress; OPTIONS 204 key-gated CORS + POST/GET 401 NestJS shape re-confirmed.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of self-owned canary, or webhook/callback POST received at private listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; ≥2x for FR/US egress pool; self-owned data only.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed fresh 13:25 UTC (action="/signin?redirect_to=https%3A%2F%2Fevil.example.com", 27448B); CSP form-action directive still absent; OAuth PKCE S256 + state + FIXED redirect_uri; return-to cookie tamper-reset REJECTED.
evidence_needed: post-auth 302 Location to external host after Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[HYP] `gladia`@0.1.3 orphaned impersonation at dist-tag latest
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists fresh (shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9); repo alexisbouchez/gladia.ts + user 404 (orphaned); description "Official" vs packaged README "Unofficial"; src/client.ts:307 embeds raw x-gladia-key in wss:// URL query; adjacent-namespace all-404 → isolated; triage VALID.
evidence_needed: none at registry level; affiliation verdict pending Gladia.
verify_steps: PASSIVE — done (metadata, tarball sha256 `3b23ec7d…7f2`, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with raw API keys in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
## 2026-08-09 14:09:50 UTC [api] (model bigpickle)
[HYP] `gladia@0.1.3` orphaned impersonation at dist-tag latest (raw API key in WS URL)
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists (fresh npm view this cycle); repo alexisbouchez/gladia.ts + user 404 (orphaned); description "Official" vs packaged README "Unofficial"; src/client.ts:306–308 embeds raw x-gladia-key into wss://api.gladia.io/v2/live query (diverges from official POST /v2/live→token flow); tarball sha256 `3b23ec7d…` + shasum `cc96f84a…` stable; adjacent-namespace all-404 → isolated.
evidence_needed: affiliation verdict from Gladia (registry ownership).
verify_steps: PASSIVE — done (metadata, tarball, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with API keys exposed in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen 40th cycle (125131B/14 paths/7 webhooks/single server); all URL fields `format:uri` no scheme/host allowlist; /v1/models confirms FR+US egress; POST /v2/pre-recorded re-confirmed 401/144 NestJS shape — key is sole gate.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of self-owned canary, or webhook/callback POST received at private listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; ≥2x for FR/US egress pool; self-owned data only.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed byte-fresh (action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`, 27448B, 0 form-action occurrences); OAuth PKCE S256 + state + FIXED redirect_uri (hardened); return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
[FINAL] ranking: [1] npm impersonation 95 (report-ready, PASSIVE, no AUTH gate) → [2] SSRF 73 (AUTH_HELPED, blocked on authorized key, highest impact) → [3] redirect_to 50 (tracking; 39 cycles zero new post-auth evidence, blocked by no-account-creation rule).
[NEXT] HUMAN: Submit the `gladia@0.1.3` report via gladia.io/bug-bounty-report (tarball sha256 `3b23ec7d…`, shasum `cc96f84a200c0fd49a71e919391f9b659c39f3e9`, README "Unofficial" vs package.json "Official", orphaned repo+user 404, src/client.ts:306–308 raw x-gladia-key in WS URL, adjacent-namespace all-clear, triage VALID). In the same submission request an authorized `x-gladia-key` + permission for a self-owned SSRF canary listener — on approval run ≥2x via POST /v2/pre-recorded audio_url/video_url/callback_config.url to cover FR/US egress, unblocking [2] and [3].
[RISK] api.gladia.io: 46 — frozen key-gated surface (40 cycles byte-identical); SSRF-by-design fetch+delivery fields + 7 webhook topics gated solely by key, canary unproven without authorized token; preflight-only x-powered-by fingerprint only; no staging host leak | app.gladia.io: 33 — unauth redirect_to reflection confirmed (CSP form-action gap re-verified 0 occurrences), post-auth honoring unproven (blocked by no-account-creation rule), OAuth hardened (PKCE S256/state/fixed redirect_uri), redirect_uri injection + cookie tamper REJECTED, no confirmed vuln | sdk: 50 — orphaned `gladia`@0.1.3 at dist-tag latest with raw-API-key-in-WS-URL pattern (report-ready, triage VALID, isolated); official @gladiaio/sdk@1.1.0 clean, tarball unchanged.
## 2026-08-09 14:54:16 UTC [api] (model bigpickle)
[HYP] `gladia@0.1.3` orphaned impersonation at dist-tag latest (raw API key in WS URL)
class: OTHER
asset: npm registry `gladia` 0.1.3
confidence: 95
reasoning: dist-tag latest=0.1.3 persists fresh this cycle; repo alexisbouchez/gladia.ts + user 404 (orphaned); description "Official" vs packaged README "Unofficial"; src/client.ts:306–308 embeds raw x-gladia-key into wss://api.gladia.io/v2/live query (diverges from official POST /v2/live→token flow); tarball sha256 `3b23ec7d…7f2` + shasum `cc96f84a200c0fd49a71e919391f9b659c39f3e9` stable; adjacent-namespace all-404 → isolated.
evidence_needed: affiliation verdict from Gladia (registry ownership).
verify_steps: PASSIVE — done (metadata, tarball, GitHub API 404); submission only remaining step.
impact: devs run unofficial code with API keys exposed in WS URLs → Medium impersonation + key hygiene
testability: PASSIVE
[HYP] SSRF via audio_url/video_url fetch + webhook/callback delivery
class: SSRF
asset: api.gladia.io POST /v2/pre-recorded (audio_url, video_url, callback_config.url; 7 webhook topics POST to client-supplied URL)
confidence: 73
reasoning: spec frozen (40+ cycles) — all URL fields `format:uri` no scheme/host allowlist; /v1/models confirms FR+US egress; POST /v2/pre-recorded re-confirmed 401/144 NestJS shape — key is sole gate.
evidence_needed: key-gated fetch where server-side error/timing reflects reachability of self-owned canary, or webhook/callback POST received at private listener.
verify_steps: AUTH_HELPED — with authorized x-gladia-key, POST /v2/pre-recorded `{"audio_url":"http://<self-owned-canary>"}`; repeat video_url + callback_config.url + webhook URL; ≥2x for FR/US egress pool; self-owned data only.
impact: cloud-metadata + internal-network read from API origin → High (key-gated)
testability: AUTH_HELPED
[HYP] redirect_to honored post-auth to external host (open redirect)
class: OATH
asset: app.gladia.io /signin
confidence: 50
reasoning: reflection re-confirmed byte-fresh (action=`/signin?redirect_to=https%3A%2F%2Fevil.example.com`, 27448B, 0 form-action occurrences); OAuth PKCE S256 + state + FIXED redirect_uri; return-to cookie tamper-reset REJECTED — only post-auth honoring unverified.
evidence_needed: post-auth 302 Location to external host after Google SSO with redirect_to set.
verify_steps: AUTH_HELPED — complete Google SSO with ?redirect_to=https://evil.example.com + //evil + app.gladia.io.evil variants; capture post-auth Location + Set-Cookie.
impact: post-auth phishing redirect → Medium
testability: AUTH_HELPED
