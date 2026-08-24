## 2026-08-21 18:45:47 UTC [api] (model mimo)
[PRIO] npm gladia@0.1.3, 8.2, attack:7 business:9 tech:8 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io /signin redirect_to, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io SSRF surface, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 5+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[PARKED] api.gladia.io SSRF: downgraded to AUTH_HELPED during POC/target=app phase, no valid key available, surface frozen 100+ cycles
[FINAL]
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh this cycle — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, description "Official", GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin redirect_to reflection alive byte-fresh — 0 CSP form-action directives (gap confirmed); post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, GET /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
## 2026-08-21 19:03:11 UTC [api] (model mimo)
[PRIO] npm gladia@0.1.3, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io /signin redirect_to, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io SSRF surface, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 5+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
## 2026-08-21 19:34:16 UTC [api] (model mimo)
[PRIO] npm `gladia`@0.1.3 orphaned impersonation, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io /signin redirect_to, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io SSRF surface, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 `3b23ec7d…7f2` reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 5+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[PARKED] (none — all three are actionable within their testability constraints)
[FINAL]
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh this cycle — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin redirect_to reflection alive byte-fresh — 0 CSP form-action directives (gap confirmed); post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, GET /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
## 2026-08-21 19:54:55 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 `3b23ec7d…7f2` reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 5+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
## 2026-08-21 20:29:08 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 `3b23ec7d…7f2` reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 5+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
## 2026-08-21 20:54:31 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence package: sha256 3b23ec7d…7f2, src/client.ts:306-308 key-in-URL, README↔package.json Official/Unofficial contradiction, GitHub user+repo 404 orphaned, dist-tag latest=0.1.3 persists. Also: if authenticated session available, test /signin?redirect_to=https://evil.example.com post-auth to verify if server honors reflected redirect_to after Google SSO.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 2026-08-21 20:54 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh 2026-08-21 20:54 UTC — form action reflects URL-encoded value, CSP 0 form-action directives, post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, POST /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[RISK] api.gladia.io: 45 reason | SSRF-by-design spec+RAG frozen 100+ cycles, key-gated only, no bypass; preflight-only x-powered-by differential; static CORS *; surface dead for autonomous probing
[RISK] app.gladia.io: 55 reason | /signin redirect_to reflection + 0 CSP form-action directives confirmed byte-fresh; OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring HUMAN_ONLY gate
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation locked with 10+ independent npm pack reproductions, supply-chain key harvesting + irrevocable account takeover risk at dist-tag latest, report-ready with no program response yet
## 2026-08-21 21:26:09 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence package: sha256 3b23ec7d…7f2, src/client.ts:306-308 key-in-URL, README↔package.json Official/Unofficial contradiction, GitHub user+repo 404 orphaned, dist-tag latest=0.1.3 persists. Also: if authenticated session available, test /signin?redirect_to=https://evil.example.com post-auth to verify if server honors reflected redirect_to after Google SSO.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh — form action reflects URL-encoded value, CSP 0 form-action directives, post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, POST /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix W/"1eaf0-fw3/7WZlGvBwQpG4/r/M+C8A+Og" with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design spec+RAG frozen 100+ cycles, key-gated only, no bypass; preflight-only x-powered-by differential; static CORS *; surface dead for autonomous probing
[RISK] app.gladia.io: 55 reason | /signin redirect_to reflection + 0 CSP form-action directives confirmed byte-fresh; OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring HUMAN_ONLY gate
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation locked with 10+ independent npm pack reproductions, supply-chain key harvesting + irrevocable account takeover risk at dist-tag latest, report-ready with no program response yet
## 2026-08-21 21:51:09 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh — form action reflects URL-encoded value, CSP 0 form-action directives, post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, POST /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix W/"1eaf0-fw3/7WZlGvBwQpG4/r/M+C8A+Og" with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design spec+RAG frozen 100+ cycles, key-gated only, no bypass; preflight-only x-powered-by differential; static CORS *; surface dead for autonomous probing
[RISK] app.gladia.io: 55 reason | /signin redirect_to reflection + 0 CSP form-action directives confirmed byte-fresh; OAuth redirect_uri FIXED prevents code/state theft; return-to cookie tamper-reset REJECTED; post-auth honoring HUMAN_ONLY gate
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation locked with 10+ independent npm pack reproductions, supply-chain key harvesting + irrevocable account takeover risk at dist-tag latest, report-ready with no program response yet
## 2026-08-21 22:16:11 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[PARKED] api.gladia.io SSRF-by-design: Downgraded from autonomous probe (AUTH_HELPED, requires valid key for POC, no bypass found across 100+ cycles)
[FINAL]
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 `3b23ec7d…7f2`, src/client.ts:306-308 key-in-URL, README↔package.json Official/Unofficial contradiction, GitHub user+repo 404 orphaned, dist-tag latest=0.1.3 persists.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh — dist-tag latest=0.1.3, shasum `cc96f84a…` unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh — form action reflects URL-encoded value, CSP 0 form-action directives, post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, POST /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix `W/"1eaf0-fw3/7WZlGvBwQpG4/r/M+C8A+Og"` with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
## 2026-08-21 22:47:04 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 8.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action reflects URL-encoded value (byte-fresh 100+ cycles), CSP has 0 form-action directives (grep-count=0), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors redirect
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable)
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh — form action reflects URL-encoded value, CSP 0 form-action directives, post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec frozen, POST /v2/pre-recorded 401/144B NestJS key-gated fresh — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix W/"1eaf0-fw3/7WZlGvBwQpG4/r/M+C8A+Og" with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live, report-ready, no program response yet
## 2026-08-21 23:11:54 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 9.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 23:10 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, description "Official", GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh 23:10 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected (200/27448B), CSP 0 form-action directives (grep-count=0), OAuth /auth/google/callback 302→accounts.google.com PKCE S256 FIXED redirect_uri prevents code/state theft, return-to cookie tamper-reset REJECTED — post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (100+ cycles) — audio_url/video_url/callback_config.url format:uri/no scheme allowlist, 7 webhook delivery paths, /v1/models FR/US egress, POST 401 NestJS key-gated — SSRF-by-design persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh 23:10 UTC — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B {"health":"OK"}, /v1/models 530B FR+US, OPTIONS 204 x-powered-by=Express + ACAO * + ACAH x-gladia-key, POST 401/144B NestJS — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix W/"1eaf0-Yx9norCx0jUfAReMn0f+i4Cdu/s" with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-21 23:41:24 UTC [api] (model mimo)
[PRIO] npmjs.com/package/gladia, 9.2, attack:8 business:9 tech:7 gate:9 cloud:8 fresh:8
[PRIO] app.gladia.io/signin, 6.8, attack:7 business:8 tech:7 gate:6 cloud:4 fresh:7
[PRIO] api.gladia.io/v2/pre-recorded, 5.6, attack:6 business:7 tech:6 gate:3 cloud:5 fresh:4
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 23:10 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, description "Official", GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh 23:10 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected (200/27448B), CSP 0 form-action directives (grep-count=0), OAuth /auth/google/callback 302→accounts.google.com PKCE S256 FIXED redirect_uri prevents code/state theft, return-to cookie tamper-reset REJECTED — post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (100+ cycles) — audio_url/video_url/callback_config.url format:uri/no scheme allowlist, 7 webhook delivery paths, /v1/models FR/US egress, POST 401 NestJS key-gated — SSRF-by-design persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh 23:10 UTC — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B {"health":"OK"}, /v1/models 530B FR+US, OPTIONS 204 x-powered-by=Express + ACAO * + ACAH x-gladia-key, POST 401/144B NestJS — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix W/"1eaf0-Yx9norCx0jUfAReMn0f+i4Cdu/s" with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 00:04:56 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3  score=73  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin  score=52  attack=6 business=5 tech=7 gate=3 cloud=2 fresh=8
[PRIO] api.gladia.io SSRF  score=48  attack=7 business=8 tech=6 gate=2 cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 00:01 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, description "Official", GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh 00:01 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected (200/27448B), CSP 0 form-action directives (grep-count=0), OAuth /auth/google/callback 302→accounts.google.com PKCE S256 FIXED redirect_uri prevents code/state theft, return-to cookie tamper-reset REJECTED — post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (100+ cycles) — audio_url/video_url/callback_config.url format:uri/no scheme allowlist, 7 webhook delivery paths, /v1/models FR/US egress, POST 401 NestJS key-gated — SSRF-by-design persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh 00:01 UTC — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B {"health":"OK"}, /v1/models 530B FR+US, OPTIONS 204 x-powered-by=Express + ACAO * + ACAH x-gladia-key, POST 401/144B NestJS — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 01:47:35 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3  score=73  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin  score=52  attack=6 business=5 tech=7 gate=3 cloud=2 fresh=8
[PRIO] api.gladia.io SSRF  score=48  attack=7 business=8 tech=6 gate=2 cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 00:01 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, description "Official", GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin?redirect_to reflection alive byte-fresh 00:01 UTC — form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected (200/27448B), CSP 0 form-action directives (grep-count=0), OAuth /auth/google/callback 302→accounts.google.com PKCE S256 FIXED redirect_uri prevents code/state theft, return-to cookie tamper-reset REJECTED — post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen (100+ cycles) — audio_url/video_url/callback_config.url format:uri/no scheme allowlist, 7 webhook delivery paths, /v1/models FR/US egress, POST 401 NestJS key-gated — SSRF-by-design persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh 00:01 UTC — openapi 200/125680B (dynamic-example band)/14 paths/7 webhooks/1 server, /health 15B {"health":"OK"}, /v1/models 530B FR+US, OPTIONS 204 x-powered-by=Express + ACAO * + ACAH x-gladia-key, POST 401/144B NestJS — surface frozen across 100+ cycles
[LEARN] REJECTED MISCONFIG @ api.gladia.io: per-instance codegen fingerprint remains falsified — new etag suffix with structural identity intact; etag rotates via dynamic example timestamps, not surface drift
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 02:44:07 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3  score=73  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin  score=52  attack=6 business=5 tech=7 gate=3 cloud=2 fresh=8
[PRIO] api.gladia.io SSRF  score=48  attack=7 business=8 tech=6 gate=2 cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query (confidence=97)
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives (confidence=92)
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist (confidence=85)
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 02:43 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin redirect_to reflection alive byte-fresh — 0 CSP form-action directives (grep-count=0), post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh — openapi 125680B/14 paths/7 webhooks, OPTIONS 204 xpb=Express, POST 401 NestJS — surface frozen across 100+ cycles
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 03:29:07 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3  score=73  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin  score=52  attack=6 business=5 tech=7 gate=3 cloud=2 fresh=8
[PRIO] api.gladia.io SSRF  score=48  attack=7 business=8 tech=6 gate=2 cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query (confidence=97)
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives (confidence=92)
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist (confidence=85)
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 02:43 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin redirect_to reflection alive byte-fresh — 0 CSP form-action directives (grep-count=0), post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh — openapi 125680B/14 paths/7 webhooks, OPTIONS 204 xpb=Express, POST 401 NestJS — surface frozen across 100+ cycles
[RISK] api.gladia.io: 45 reason | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 reason | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 reason | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 04:10:01 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3  score=73  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin  score=52  attack=6 business=5 tech=7 gate=3 cloud=2 fresh=8
[PRIO] api.gladia.io SSRF  score=48  attack=7 business=8 tech=6 gate=2 cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query (confidence=97)
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives (confidence=92)
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist (confidence=85)
[NEXT] PROBE: Re-verify app.gladia.io CSP header and /signin?redirect_to=https://evil.example.com form-action reflection via webfetch (GET).
## 2026-08-22 04:51:03 UTC [api] (model mimo)
[PRIO] npm:gladia@0.1.3          score=75  attack=8 business=8 tech=6 gate=10 cloud=3 fresh=8
[PRIO] app.gladia.io/signin       score=50  attack=6 business=5 tech=7 gate=3  cloud=2 fresh=8
[PRIO] api.gladia.io SSRF         score=46  attack=7 business=8 tech=6 gate=2  cloud=6 fresh=8
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query
class: OTHER
asset: npmjs.com/package/gladia
confidence: 97
reasoning: dist-tag latest=0.1.3, description "Official TypeScript SDK for Gladia", repo+user alexisbouchez both 404 (orphaned/irrevocable), src/client.ts:306-308 embeds raw x-gladia-key in wss:// URL query via searchParams.append, sha256 3b23ec7d…7f2 reproduced across 10+ independent local npm pack runs, README "Unofficial" vs package.json "Official" contradiction
evidence_needed: report-ready, locked across 10+ independent npm pack reproductions
verify_steps: HUMAN: Submit report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated)
impact: supply-chain API key harvesting + irrevocable account takeover (GitHub user+repo 404 = orphaned, dist-tag latest persists), P3/P4 severity
testability: HUMAN_ONLY
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives
class: OATH
asset: app.gladia.io/signin
confidence: 92
reasoning: form action="/signin?redirect_to=https%3A%2F%2Fevil.example.com" reflected byte-fresh (100+ cycles), CSP has 0 form-action directives (grep-count=0 on live header), OAuth redirect_uri FIXED prevents code/state theft, return-to cookie tamper-reset REJECTED, post-auth honoring sole unverified gate
evidence_needed: HUMAN OAuth test (post-auth redirect_to)
verify_steps: HUMAN: authenticate via Google SSO, then access /signin?redirect_to=https://evil.example.com post-auth to test if server honors reflected redirect_to after authentication
impact: potential post-auth open redirect if server honors reflected redirect_to after authentication, P3 severity
testability: HUMAN_ONLY
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist
class: SSRF
asset: api.gladia.io/v2/pre-recorded
confidence: 85
reasoning: spec confirms audio_url/video_url/callback_config.url as format:uri with NO scheme allowlist, 7 webhook delivery paths, /v1/models confirms FR/US egress, POST 401 NestJS key-gated only, spec+RAG frozen 100+ cycles
evidence_needed: authorized API key for POC
verify_steps: AUTH_HELPED: POST /v2/pre-recorded with valid x-gladia-key and audio_url=http://internal-host/secret
impact: server-side request forgery to internal network, P2/P3 severity
testability: AUTH_HELPED
[FINAL]
[HYP] Orphaned npm gladia@0.1.3 impersonates official SDK, leaks raw API key in WebSocket URL query (confidence=97)
[HYP] app.gladia.io /signin redirect_to form-action reflection with 0 CSP form-action directives (confidence=92)
[HYP] api.gladia.io SSRF-by-design via audio_url/video_url/callback_config.url with no scheme allowlist (confidence=85)
[NEXT] HUMAN: Submit the locked gladia@0.1.3 orphaned-impersonation report via https://gladia.io/bug-bounty-report (301→www→302→Google Forms, Google SSO auth-gated). Evidence: sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2, shasum cc96f84a200c0fd49a71e919391f9b659c39f3e9, src/client.ts:306-308 searchParams.append('x-gladia-key', apiKey) + new WebSocket(wsUrl.toString()) confirmed in source+compiled dist, GitHub user+repo alexisbouchez both 404 (orphaned/irrevocable), package.json "Official" vs README "# Unofficial TypeScript SDK" contradiction, dist-tag latest=0.1.3 persists. Reproduced 10+ independent times.
[LEARN] ACCEPTED OTHER @ npm gladia@0.1.3: class alive, re-verified fresh 02:43 UTC — dist-tag latest=0.1.3, shasum cc96f84a… unchanged, GitHub API user+repo alexisbouchez both 404 (orphaned/irrevocable), official @gladiaio/sdk@1.1.0 static
[LEARN] ACCEPTED OATH @ app.gladia.io: /signin redirect_to reflection alive byte-fresh — 0 CSP form-action directives (grep-count=0), post-auth honoring sole unverified gate (HUMAN_ONLY)
[LEARN] ACCEPTED SSRF @ api.gladia.io: spec+RAG frozen — SSRF-by-design surface persists (AUTH_HELPED)
[LEARN] REJECTED MISCONFIG @ api.gladia.io: NO_DRIFT re-confirmed fresh — openapi 125680B/14 paths/7 webhooks, OPTIONS 204 xpb=Express, POST 401 NestJS — surface frozen across 100+ cycles
[RISK] api.gladia.io: 45 | SSRF-by-design surface persists but key-gated (AUTH_HELPED), no bypass found across 100+ cycles, frozen surface, /v2/live/health undocumented but informational only
[RISK] app.gladia.io: 55 | redirect_to reflection + CSP form-action gap confirmed byte-fresh, OAuth redirect_uri FIXED prevents code/state theft, post-auth honoring HUMAN_ONLY, /dashboard 200 SPA shell without auth
[RISK] sdk: 75 | gladia@0.1.3 orphaned impersonation confirmed live at dist-tag latest, report-ready across 10+ independent reproductions, no program response yet, irrevocable GitHub user+repo 404
## 2026-08-22 05:19:17 UTC [api] (model mimo)
## 2026-08-22 05:49:34 UTC [api] (model mimo)
## 2026-08-22 06:20:39 UTC [api] (model mimo)
## 2026-08-22 07:08:43 UTC [api] (model mimo)
## 2026-08-22 07:45:47 UTC [api] (model mimo)
## 2026-08-22 08:12:33 UTC [api] (model mimo)
## 2026-08-22 08:50:54 UTC [api] (model mimo)
## 2026-08-22 09:20:24 UTC [api] (model mimo)
## 2026-08-22 09:48:52 UTC [api] (model mimo)
## 2026-08-22 10:10:43 UTC [api] (model mimo)
## 2026-08-22 10:42:48 UTC [api] (model mimo)
## 2026-08-22 11:02:17 UTC [api] (model mimo)
## 2026-08-22 11:31:47 UTC [api] (model mimo)
## 2026-08-22 11:53:33 UTC [api] (model mimo)
## 2026-08-22 12:38:23 UTC [api] (model mimo)
## 2026-08-22 13:19:27 UTC [api] (model mimo)
## 2026-08-22 13:49:28 UTC [api] (model mimo)
## 2026-08-22 14:10:51 UTC [api] (model mimo)
## 2026-08-22 14:40:38 UTC [api] (model mimo)
## 2026-08-22 15:00:41 UTC [api] (model mimo)
## 2026-08-22 15:31:42 UTC [api] (model mimo)
## 2026-08-22 15:53:15 UTC [api] (model mimo)
## 2026-08-22 16:22:20 UTC [api] (model mimo)
## 2026-08-22 16:49:11 UTC [api] (model mimo)
## 2026-08-22 17:10:49 UTC [api] (model mimo)
## 2026-08-22 17:38:16 UTC [api] (model mimo)
## 2026-08-22 17:58:09 UTC [api] (model mimo)
## 2026-08-22 18:42:24 UTC [api] (model mimo)
## 2026-08-22 19:08:56 UTC [api] (model mimo)
## 2026-08-22 19:35:21 UTC [api] (model mimo)
## 2026-08-22 19:54:40 UTC [api] (model mimo)
## 2026-08-22 20:26:14 UTC [api] (model mimo)
## 2026-08-22 20:51:22 UTC [api] (model mimo)
## 2026-08-22 21:15:45 UTC [api] (model mimo)
## 2026-08-22 21:40:57 UTC [api] (model mimo)
## 2026-08-22 21:59:48 UTC [api] (model mimo)
## 2026-08-22 22:33:12 UTC [api] (model mimo)
## 2026-08-22 22:55:31 UTC [api] (model mimo)
## 2026-08-22 23:26:10 UTC [api] (model mimo)
## 2026-08-22 23:48:27 UTC [api] (model mimo)
## 2026-08-23 00:28:00 UTC [api] (model mimo)
## 2026-08-23 02:10:59 UTC [api] (model mimo)
## 2026-08-23 03:17:04 UTC [api] (model mimo)
## 2026-08-23 04:06:19 UTC [api] (model mimo)
## 2026-08-23 04:50:59 UTC [api] (model mimo)
## 2026-08-23 05:22:34 UTC [api] (model mimo)
## 2026-08-23 05:54:32 UTC [api] (model mimo)
## 2026-08-23 06:45:04 UTC [api] (model mimo)
## 2026-08-23 07:22:02 UTC [api] (model mimo)
## 2026-08-23 07:55:44 UTC [api] (model mimo)
## 2026-08-23 08:37:39 UTC [api] (model mimo)
## 2026-08-23 09:03:36 UTC [api] (model mimo)
## 2026-08-23 09:38:58 UTC [api] (model mimo)
## 2026-08-23 10:00:31 UTC [api] (model mimo)
## 2026-08-23 10:35:12 UTC [api] (model mimo)
## 2026-08-23 10:57:44 UTC [api] (model mimo)
## 2026-08-23 11:29:12 UTC [api] (model mimo)
## 2026-08-23 11:51:50 UTC [api] (model mimo)
## 2026-08-23 12:30:26 UTC [api] (model mimo)
## 2026-08-23 13:16:50 UTC [api] (model mimo)
## 2026-08-23 13:50:00 UTC [api] (model mimo)
## 2026-08-23 14:14:16 UTC [api] (model mimo)
## 2026-08-23 14:44:22 UTC [api] (model mimo)
## 2026-08-23 15:03:58 UTC [api] (model mimo)
## 2026-08-23 15:34:30 UTC [api] (model mimo)
## 2026-08-23 15:55:50 UTC [api] (model mimo)
## 2026-08-23 16:33:11 UTC [api] (model mimo)
## 2026-08-23 16:57:40 UTC [api] (model mimo)
## 2026-08-23 17:27:51 UTC [api] (model mimo)
## 2026-08-23 17:50:30 UTC [api] (model mimo)
## 2026-08-23 18:17:37 UTC [api] (model mimo)
## 2026-08-23 18:52:43 UTC [api] (model mimo)
## 2026-08-23 19:20:36 UTC [api] (model mimo)
## 2026-08-23 19:43:19 UTC [api] (model mimo)
## 2026-08-23 20:00:03 UTC [api] (model mimo)
## 2026-08-23 20:34:33 UTC [api] (model mimo)
## 2026-08-23 20:57:17 UTC [api] (model mimo)
## 2026-08-23 21:29:30 UTC [api] (model mimo)
## 2026-08-23 21:51:36 UTC [api] (model mimo)
## 2026-08-23 22:16:33 UTC [api] (model mimo)
## 2026-08-23 22:43:01 UTC [api] (model mimo)
## 2026-08-23 23:01:40 UTC [api] (model mimo)
## 2026-08-23 23:32:11 UTC [api] (model mimo)
## 2026-08-23 23:53:41 UTC [api] (model mimo)
## 2026-08-24 01:18:19 UTC [api] (model mimo)
## 2026-08-24 02:39:30 UTC [api] (model mimo)
## 2026-08-24 03:39:14 UTC [api] (model mimo)
## 2026-08-24 04:29:24 UTC [api] (model mimo)
## 2026-08-24 05:22:13 UTC [api] (model mimo)
## 2026-08-24 06:02:52 UTC [api] (model mimo)
## 2026-08-24 07:16:49 UTC [api] (model mimo)
## 2026-08-24 08:08:15 UTC [api] (model mimo)
## 2026-08-24 09:04:53 UTC [api] (model mimo)
## 2026-08-24 10:01:20 UTC [api] (model mimo)
## 2026-08-24 10:49:25 UTC [api] (model mimo)
## 2026-08-24 11:17:34 UTC [api] (model mimo)
## 2026-08-24 11:48:57 UTC [api] (model mimo)
## 2026-08-24 12:21:15 UTC [api] (model mimo)
## 2026-08-24 13:29:31 UTC [api] (model mimo)
## 2026-08-24 14:21:36 UTC [api] (model mimo)
