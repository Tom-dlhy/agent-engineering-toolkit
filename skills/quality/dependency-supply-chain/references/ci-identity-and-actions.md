# GitHub Actions — trust boundaries, tokens and supply-chain review

**Read when:** reviewing PR workflows, fork contributions, cloud OIDC,
action dependencies, caches or self-hosted runners.

## Separate event privilege

The `pull_request_target` event runs in base repository security
context. Executing untrusted PR head or artifacts in that context can
expose repo secrets/write permissions. Regular fork PR workflows tend
to run with restricted token; always inspect actual repo/org policies.

~~~yaml
name: verify
on: [pull_request]
permissions:
  contents: read
jobs:
  tests:
    runs-on: ubuntu-latest
    steps:
      # Replace with an audited FULL immutable commit SHA.
      - uses: actions/checkout@<VERIFIED_40_CHAR_SHA>
      - run: python -m unittest discover -s tests
~~~

The example is illustrative and **not executable** until SHA placeholder
and job dependencies are fixed. Pin actions to verified full commit IDs,
not mutable tags; verify source, nested actions, scripts and build inputs.

## Security checklist

1. Default GITHUB_TOKEN read-only; grant write only to jobs needing it.
2. For clouds use OIDC short-lived identity with constrained issuer,
   subject, repository/ref/environment on cloud trust policy. Enabling
   `id-token: write` alone does not grant cloud access.
3. Don't pass secrets to untrusted workflow/scripts; don't interpolate
   untrusted PR titles into shell snippets.
4. Avoid cross-trust cache poisoning and privileged workflow_run chains
   consuming unverified untrusted artifacts.
5. On self-hosted runners, require ephemeral isolation and credential
   separation before executing forked code.
6. Evaluate pull_request_target/checkout as a *combined* execution path,
   not two independent YAML lines.

## Verification

Review triggers, token scope, checkout SHA/ref, dependency scripts,
environment protection, external shell/network and untrusted artifact
promotion. Test permission-denied path with synthetic fork in safe repo
if warranted. Never adjust org secret policies as a side effect of review.

Official:
https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target ,
https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication ,
https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect .
