---
name: terraform-iac
domain: cloud
version: "0.1.0"
description: >-
  Use when writing or reviewing Terraform or OpenTofu modules for reproducible cloud infrastructure. Do not use to apply infrastructure changes without authorization.
---

# terraform-iac

## Modules and state
Design module interfaces around stable capabilities. Pin provider and module versions. Store encrypted state in an appropriate remote backend with restricted access and locking. Never commit terraform.tfstate, tfvars containing secrets or plan artifacts with sensitive content.
## Least privilege
Plan infrastructure in disposable environments; separate state and IAM roles per trust boundary. Use workload federation for CI instead of long-lived cloud credentials.
## CI
Run format, validate, static checks and plan on PR. Require explicit approval and scoped credentials for apply. Inspect drift, replacements, deleted resources and cost deltas before rollout. Use policy-as-code for critical controls.
## Verify
Check idempotence, no unexpected resources, workspace targeting, encryption, tags and rollback/migration strategy. Avoid presuming all providers support identical semantics.
