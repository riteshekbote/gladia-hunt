## 2026-08-22 STATUS: REPORTED BY HUMAN — AWAITING VENDOR RESPONSE

- REPORTED: 2026-08-12 (10 days ago) by riteshekbote@gmail.com -> security@gladia.io, full report + PoC attachments
- RE-CHECKED 2026-08-22: NO vendor action yet. Package still live: latest=0.1.3, maintainer softwarecitadel unchanged, NOT unpublished, time.modified=2025-04-07 (pre-report). Repo+user still 404 -> takeover risk OPEN.
- CLAIM VERIFIED INDEPENDENTLY: README.md line 3 says "Unofficial TypeScript SDK for Gladia" while registry description says "Official..." - the contradiction is real.
- Typosquat ecosystem still up: @andrea_ztn/gladia@0.1.3 (200), also noted new namespace squatter candidate @keystrokehq/gladia@0.1.6.
- FOLLOW-UP DUE: 2026-08-26 (14-day mark) -> send ONE polite status request to security@gladia.io.
- PARALLEL TRACK: report was promised to npm Trust & Safety (npmjs.com/support) - CONFIRM whether actually sent; if not, send now (venue split per triage: root cause is npm's).
- DO-NOT-REDO: bots must not re-flag this lead or draft new reports; this file is the single source of truth.

## 2026-08-22 TRIAGE UPDATE (7-Question Gate, strict mode)

VERDICT MATRIX:
- VENUE npm registry -> ACTIONABLE NOW (impersonation report, see DRAFT below)
- VENUE gladia.io form -> HOLD: Q3 FAILS as standalone vuln (root cause lives in softwarecitadel's package, not a Gladia asset). Becomes a Gladia-side bug ONLY if wss://api.gladia.io/v2/live accepts x-gladia-key query param (legacy compat). Needs 1 valid key to prove. Until then: primitive present, not submittable.
- Severity correction: earlier MEDIUM-HIGH / confidence 95 was pre-triage. Post-gate: npm-venue report = registry policy case ($0, removes harm); Gladia-venue = conditional, unproven end-to-end (Pre-Severity Gate #3 fail).

RETRACTED CLAIM: "key leak = Gladia vulnerability". Disproving reasoning: vulnerable code is not served by Gladia infra; if the v2/live WS rejects query-param auth, the fake SDK leaks keys to an endpoint that never accepts them (broken SDK, not vuln).


[HUMAN-ACTION] To unlock Gladia-venue leg: register free Gladia account, obtain API key, open WSS handshake to wss://api.gladia.io/v2/live?x-gladia-key=<KEY> vs header-auth control. If query-param auth succeeds -> server-side key-in-URL design flaw (keys land in proxy/access logs for ALL custom integrations) -> then submit to gladia.io form as their bug.

DRAFT: NPM IMPERSONATION REPORT (copy-paste ready):
Package: https://www.npmjs.com/package/gladia (v0.1.3, dist-tag latest)
Issue: Impersonation of Gladia (gladia.io) official SDK.
Evidence:
1. Description claims "Official TypeScript SDK for Gladia - State-of-the-art Speech to Text API".
2. Maintainer: softwarecitadel (softwarecitadel@gmail.com) - no affiliation with Gladia.
3. Linked repository github.com/alexisbouchez/gladia.ts returns 404; user alexisbouchez does not exist (404).
4. Genuine SDK is published under Gladia's scoped namespace: @gladiaio/sdk (publisher bot-npmjs-gladiaio).
Requested action: transfer name to Gladia / unpublish for impersonation + abandoned-package policy.
Note: additionally the package embeds raw API keys into WebSocket URLs (src/client.ts:307), a credential-hygiene hazard for anyone misled into using it.

--- ORIGINAL EVIDENCE (verified 2026-08-22, still accurate) ---
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
