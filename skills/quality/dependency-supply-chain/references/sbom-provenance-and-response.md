# SBOM, artifact provenance and compromise response

**Read when:** publishing packages/containers, generating SBOM,
evaluating SLSA, verifying build attestations or investigating compromise.

## What each artifact actually proves

- SBOM: inventory of declared/detected package components (CycloneDX/SPDX).
  It doesn't prove integrity, provenance or absence of vulnerability.
- Attestation: verifiable statement about an artifact digest and signer;
  security depends on trusted identity and policy validation.
- Provenance: how/where/from which inputs a specific artifact was built.
- Immutable digest: identifies bytes; mutable tags are not sufficient.
- Reproducibility: useful when build sources/outputs can be compared,
  but doesn't by itself demonstrate source code is safe.

## SLSA Build track

Official SLSA v1.2 distinguishes Build L1 (provenance present),
Build L2 (signed provenance produced by trusted hosted builder)
and L3 (stronger hardened builder controls). These are security
**claims about builds**, not skill maturity labels. Validate builder
identity, expected source revision/workflow, trusted signer and output digest.
Don't claim levels solely from a generated JSON file.

## GitHub build attestations

When appropriate and supported for the repo plan/visibility,
GitHub's documented artifact attestation pattern requires
`id-token: write`, `contents: read`, `attestations: write` plus
a supported attestation action and an **actual** artifact path/digest.
Don't grant extra write access to every CI job just to "enable security."
Verify generated provenance with expected publisher/builder before release.

## Incident recovery

Suspend trusted publishing, enumerate affected digests and deployed
versions, isolate compromised token/runner, preserve logs, rotate known
credentials, rebuild with trusted inputs, verify attestations, roll
out safely and notify consumers if necessary. Know whether a suspicious
dependency was executed before deciding exposure.

## Evidence report

Digest, source SHA, builder identity, checked attestation and verifier
output, SBOM coverage, missing components, residual unknowns.

Official: https://slsa.dev/spec/v1.2/ ,
https://slsa.dev/spec/v1.2/build-track-basics ,
https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations .
