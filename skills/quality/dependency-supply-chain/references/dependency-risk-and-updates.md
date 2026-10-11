# Dependency security — resolve, audit, evaluate and update

**Read when:** introducing/upgrading packages, investigating a vulnerability
or reviewing an indirect dependency.

## Inventory the resolved graph

A manifest is only declared direct dependencies. Review lockfile and resolved
transitive/runtime/build dependencies, images and scripts. Record source registry,
immutable release identity, version, license and known security advisories.

| Ecosystem | Evidence | Caveat |
|---|---|---|
| Python uv/pip | uv.lock + installed graph, pip-audit | May resolve/install; not malware detection |
| Node pnpm | pnpm-lock + lifecycle scripts | Postinstall may run untrusted code |
| Container | SHA256 image digest and OS package inventory | Tag is mutable; backports matter |
| GitHub Actions | Immutable commit SHA, scoped permissions | SHA pin alone cannot prove safety |

The official pip-audit project explicitly warns that auditing arbitrary
requirements can involve dependency resolution similar to installation
and that known-CVE scanning is NOT a malware detector. Don't run scans
against untrusted manifests on privileged hosts without isolation.

## Triaging an advisory

Confirm affected and fixed ranges, distribution backports, code reachability,
entrypoint, impact, actual deployed version and compensating controls.
CVSS describes characteristics, not automatically the exposure of your
application. Unknown or unreported vulnerabilities remain possible.

## Controlled upgrade

1. Snapshot lockfile and current artifacts.
2. Read primary advisory and vendor migration guide.
3. Resolve smallest safe upgrade with deterministic lock.
4. Run build, unit/integration, security regression and license review.
5. Inspect transitive graph/image after build.
6. Stage, deploy with rollback and record exception expiry if deferred.

Avoid blanket "upgrade to latest" advice, unchecked auto-fix, or treating
a green scanner as proof of no malicious code.

Official:
https://github.com/pypa/pip-audit ,
https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action ,
https://openssf.org/projects/scorecard/ .
