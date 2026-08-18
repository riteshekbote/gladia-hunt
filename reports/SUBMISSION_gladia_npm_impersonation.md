# Gladia Bounty Submission — Impersonated `gladia` npm package (0.1.3, dist-tag latest) with API-key-in-URL leak

## METADATA

| Field | Value |
|---|---|
| **Asset** | `gladia` (npm registry) — declared in-scope in program scope.yml (`npm_packages: @gladiaio/sdk, gladia`) |
| **Class** | Supply-chain impersonation (orphaned/unofficial package squatting the official SDK name) + credential disclosure in URL |
| **Severity** | High (CVSS 3.1 ~7.5–8.1: AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N) — any consumer of the package name is affected; API keys are transmitted in cleartext-visible URL queries |
| **Package** | `gladia@0.1.3` — dist-tag `latest` |
| **Tarball sha256** | `3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2` |
| **npm shasum** | `cc96f84a200c0fd49a71e919391f9b659c39f3e9` |
| **Last re-verified** | 2026-08-17 22:38 UTC (byte-fresh, unchanged since 2026-08-07) |

## SUMMARY

The npm package name `gladia` — the natural install name for Gladia's TypeScript SDK — is occupied by an **orphaned, unofficial package** whose metadata claims to be the official SDK ("Official TypeScript SDK for Gladia") while its README admits it is unofficial. The registered maintainer (`softwarecitadel@gmail.com`) and linked repository (`alexisbouchez/gladia.ts`) are not affiliated with Gladia; the GitHub user and repo are now 404 (orphaned/irrevocable). The package is published under dist-tag `latest`, so `npm install gladia` silently installs third-party code that claims to be official Gladia software.

## EVIDENCE

1. **Metadata impersonation** — `npm view gladia`:
   - description: "Official TypeScript SDK for Gladia"
   - repository: `alexisbouchez/gladia.ts` (personal account, now 404)
   - maintainers: `softwarecitadel@gmail.com` (personal, not `gladiaio`)
   - dist-tags: `latest: 0.1.3`
   - Contradiction: package.json claims "Official"; README of the same tarball claims "Unofficial".

2. **Official package comparison** — the legitimate SDK lives at `@gladiaio/sdk` (org `gladiaio`, latest 1.1.0). The un-scoped `gladia` name is NOT owned by Gladia.

3. **Credential disclosure in code (src/client.ts:306-308)**:
   ```typescript
   searchParams.append('x-gladia-key', apiKey);      // line 307
   wsUrl.searchParams.append('token', ...);          // line ~308
   new WebSocket(wsUrl.toString())                    // line 318
   ```
   Any application that configures this package with a Gladia API key sends the raw `x-gladia-key` as a **query-string parameter in the WebSocket URL** — the key is then visible in access logs, proxies, browser history, and any URL-collecting middleware, and is transmittable to a third-party WebSocket endpoint.

4. **Reproducibility** — `npm pack gladia@0.1.3` reproduces tarball sha256 `3b23ec7d…7f2` on three independent local runs (100+ check cycles, 2026-08-07 → 2026-08-17), shasum unchanged. Dist-tag `latest` unchanged.

## IMPACT

- **Name squatting / impersonation of the official SDK**: any user, CI pipeline, or downstream dependency that installs `gladia` believes it is running official Gladia code; the actual publisher is an unrelated third party with full control of the published artifact.
- **API-key disclosure**: keys handed to this package are embedded in `wss://` URL queries (`x-gladia-key=...`), leaking them to every hop that sees the URL — a vector that the official `@gladiaio/sdk` does not have.
- **Persistence**: the publisher account/repo are orphaned (404), so the package cannot be fixed, transferred, or removed by anyone except the npm owner; only Gladia (or npm support acting for the brand owner) can reclaim or request takedown.

## RECOMMENDATION

1. Request npm takedown/transfer of `gladia` to the `gladiaio` org (or publish a deprecation notice pointing to `@gladiaio/sdk`).
2. Claim the un-scoped name so `npm install gladia` resolves to official code.
3. If consumers are expected to keep using `gladia`, republish official code at that name and rotate any keys already passed to the impersonating package.

## REPRO

```
npm view gladia                  # description/repo/maintainer/dist-tags (see Evidence 1)
npm pack gladia@0.1.3            # tarball sha256 3b23ec7d7a763abc04c52db232d157a982fd3bd969c9f703af3eecad5fa802f2
tar xzf gladia-0.1.3.tgz && grep -n "x-gladia-key" package/src/client.ts   # line 307
```

Evidence package: sha256-verified tarball + `npm view` JSON captured in repo knowledge base (2026-08-07 → 2026-08-17, byte-fresh each check).
