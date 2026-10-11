# PR workflow security — trusted events and artifact promotion

**Read when:** a PR edits GitHub workflow YAML, pull_request_target,
external actions, job permissions, caches or build artifacts.

## High-risk boundaries

A workflow running on pull_request_target is evaluated in the base
repository's trust context. Checking out and executing untrusted PR
code with write token or secrets can cause repository compromise.
A normal pull_request with read-only token is usually safer for
building code from forks, but actual repository policies must be checked.

## Audit checklist

1. Events: pull_request, push, workflow_run, pull_request_target,
   dispatch, each with specific trust origin.
2. Minimal permissions: default contents: read, write only on
   audited publisher jobs and approved refs/environments.
3. Pin external actions to reviewed immutable 40-char commit SHA,
   verify their dependencies, scripts and provenance.
4. OIDC cloud identities: cloud-side trust conditions constrain
   repository/ref/environment; short-lived id-token alone does not
   grant authorization.
5. Avoid untrusted PR text interpolated directly in shell commands;
   variables are still untrusted data.
6. Cache and downloaded artifact contamination across different
   trust zones; never execute untrusted artifact in privileged job
   without independent verification.
7. Self-hosted runners require strong isolation for fork contributions.

## Safer publishing split

Build/test untrusted PR with no secrets. Only a separate trusted
tag/release workflow on protected ref can publish artifacts after
checks, with minimal write scope and output provenance.

## Validation and proof

Examine actual workflow triggers, token permissions, base/head
checkout, branch protection and whether secrets are exposed to PR
code. Use YAML/action lint and isolated test repository where
authorized. CI passing one path doesn't prove fork scenario safe.

Official: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target and
https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect .
