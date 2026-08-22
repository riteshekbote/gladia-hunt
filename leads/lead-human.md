## 2026-08-22 HUMAN-VALIDATED (external deep-dive, model ox-alpha-free)

[NEXT] HUMAN: Submit gladia@0.1.3 orphaned-impersonation + key-in-URL report via https://www.gladia.io/bug-bounty-report (Google Forms, SSO auth-gated). Full evidence below.

[HYP] Orphaned npm package gladia@0.1.3 impersonates official SDK and leaks raw API keys in WebSocket URLs
class: OTHER
asset: npmjs.com/package/gladia
confidence: 95
reasoning: (1) IMPERSONATION: description claims "Official TypeScript SDK for Gladia" but maintainer is softwarecitadel@gmail.com (third party); homepage/repo point to github.com/alexisbouchez/gladia.ts which is HTTP 404 (user also 404) — dead provenance. Real official SDK is @gladiaio/sdk@1.1.0 published by bot-npmjs-gladiaio under Gladia's org. dist-tag latest=0.1.3, shasum cc96f84a… stable across cycles. (2) KEY EXPOSURE: src/client.ts:307 does wsUrl.searchParams.append('x-gladia-key', this.apiKey) then new WebSocket(wsUrl.toString()) — raw API key embedded in WS query string for wss://api.gladia.io/v2/live. Official @gladiaio/sdk never puts the key in URLs: REST init with x-gladia-key header, then connects to short-lived session.url issued per session. Keys in query strings leak via TLS-terminating proxy logs, server access logs, browser devtools/history, and any URL-sharing bug.
evidence_needed: none further — registry metadata + tarball source verified directly (tarball inspected 2026-08-22)
verify_steps: PASSIVE: curl -s https://registry.npmjs.org/gladia | jq '.maintainers,.dist-tags'; note maintainer softwarecitadel vs official @gladiaio org; download tarball, read package/src/client.ts line ~307 showing searchParams.append('x-gladia-key', apiKey); compare with @gladiaio/sdk dist/v2/live/session.js connectToWebSocket() which connects to server-issued session.url with no credential material.
impact: Developers installing the impersonating "official" SDK embed raw Gladia API keys in every live-transcription WebSocket URL; keys persist in proxy/access logs enabling account takeover of the Gladia account (billing audio data). Package abandonment (dead repo) means no fix will ship. Secondary: typosquat copy @andrea_ztn/gladia@0.1.3 exists at same version. Severity: MEDIUM-HIGH supply-chain + credential exposure.
testability: PASSIVE

[UNVALIDATED] npmjs.com/package/gladia: orphaned gladia@0.1.3 impersonates official SDK ('Official TypeScript SDK', maintainer softwarecitadel, repo/user 404) + leaks raw API key in WS URL query string (client.ts:307 searchParams x-gladia-key) vs official @gladiaio/sdk session-url design | MEDIUM-HIGH | PASSIVE-PROVEN
