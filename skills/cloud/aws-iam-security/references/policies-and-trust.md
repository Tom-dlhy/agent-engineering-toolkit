# AWS IAM policies, trust and evaluation

**Open when:** implementing an identity-based or resource-based policy, cross-account access, or diagnosing an AWS permission denial.

## Mental model

The trust policy answers **who may assume a role**. The role's permission policy answers **what it can do after assumption**. Cross-account access may require an identity policy in the calling account and a resource/trust policy in the target account. Permission boundaries, Organizations SCPs/RCPs, session policies and explicit denies can further constrain grants; absence of an allow is deny by default. KMS key policies have additional authorization semantics.

Do not conflate `iam:PassRole` (authorizing one service to receive a role) with `sts:AssumeRole` (assuming a role). `iam:PassRole` needs scope to specific roles and `iam:PassedToService` where applicable.

## Example read-only object access policy

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "ReadReportsOnly",
    "Effect": "Allow",
    "Action": ["s3:GetObject"],
    "Resource": ["arn:aws:s3:::EXAMPLE-REPORTS-BUCKET/reports/*"]
  }]
}
```

`s3:ListBucket` (if required) targets `arn:aws:s3:::EXAMPLE-REPORTS-BUCKET` and can be scoped with `s3:prefix` conditions. Do **not** put `ListBucket` on object ARNs. For SSE-KMS objects, also evaluate KMS decrypt permissions **and** the key policy.

## Example role trust for Lambda service

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

Service trust is not authorization to invoke a Lambda function; function/resource permissions and API authentication must be evaluated separately. Apply trust conditions only when supported for the intended principal/service.

## Policy review checklist

1. Principal uniquely identified, trusted account and allowed role session restricted.
2. Actions matched to SDK operation and exact AWS authorization reference (API name does not always equal IAM action).
3. Resources selected at the correct ARN scope; wildcard only if API explicitly requires it.
4. Conditions use **supported** action/resource condition keys; unsupported condition keys can have surprising effects.
5. Avoid embedding permanent credentials in build/test artifacts.
6. Access Analyzer policy validation for syntax, security warnings and actionable findings; perform integration negative test.

```bash
# Before running, verify target profile and account
aws sts get-caller-identity
aws accessanalyzer validate-policy --policy-type IDENTITY_POLICY --policy-document file://policy.json
```

## Common 403/AccessDenied causes

Wrong profile/account or region, role trust failure, missing resource policy, KMS key policy, SCP or boundary denial, session policy cap, explicit deny, VPC endpoint policy, bucket's Block Public Access, unrecognized resource ARN, propagation and missing action-specific permissions.

**Never "fix" AccessDenied by adding `Action: "*", Resource: "*"`.** Record failing operation, AWS request ID and exact assumed-role ARN; inspect policies via least-privileged tooling. Policy simulation is useful but cannot replace real cross-account/resource and KMS tests.

Official: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html and https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-reference-policy-checks.html .
