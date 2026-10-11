# AWS identity federation, STS and access diagnostics

**Open when:** creating identity for GitHub Actions, ECS/Lambda workloads, cross-account deployment or troubleshooting principal mismatch.

## Credential decision tree

- Developer: AWS IAM Identity Center SSO and local profile; avoid IAM user keys.
- Lambda: execution role scoped to needed APIs.
- ECS: task role for **application** calls; execution role for ECS agent actions (image pull, log writes, selected secret injection).
- CI: OpenID Connect federation to a role with restricted repository/environment trust claims; no stored long-lived AWS secret keys.
- Cross-account: STS AssumeRole with explicit trust and matching identity policy; scope external IDs where third-party access requires it.

## GitHub OIDC trust shape (illustrative)

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::111122223333:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
      "StringLike": {"token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:ref:refs/heads/main"}
    }
  }]
}
```

Replace account/repository; configure the OIDC provider and adapt `sub` when using GitHub environments (subject form differs). For protected deployment, restrict to the intended protected environment or ref and use GitHub environment approvals. Avoid `repo:*/*` broad trust.

## Troubleshooting sequence

1. Collect CLI `sts get-caller-identity` or SDK caller identity **without logging credentials**.
2. Identify operation, resource ARN, region, request ID, session context, role and all boundary layers.
3. Check role trust if assumption fails, identity/resource policies if operation denies, and resource-specific policy (e.g. S3 bucket or KMS key).
4. For CI: inspect OIDC subject and audience restrictions, workflow permissions and environment protections.
5. Run Access Analyzer policy validation; use policy simulation as a diagnostic aid, then integration test the exact action in a sandbox.
6. For drift: compare desired IaC policy with deployed role/policy and CloudTrail management/event records subject to logging configuration.

## What to test

- Allowed call to intended resource succeeds.
- Same call to another tenant/prefix/account is denied.
- Wrong GitHub repository/ref/environment cannot assume role.
- CI has minimal token scope; role session is short-lived; credentials expire/rotate.
- Service runtime uses correct task/execution role and does not fall back to unexpected local profiles.

Do not execute identity changes or grant additional permissions without authorization.

Official: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html and https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html .
