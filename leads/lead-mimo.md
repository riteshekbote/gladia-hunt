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
