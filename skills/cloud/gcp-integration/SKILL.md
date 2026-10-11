---
name: gcp-integration
domain: cloud
version: "0.2.0"
description: >-
  Use when coordinating more than one Google Cloud service, project IAM, SDK clients and cross-service reliability. Do not use for a single GCP service that already has an individual skill.
---

# GCP integration coordinator

## Decision path
1. Identify actual task, environment, owner, runtime, provider/version, safety and operational consequence.
2. Route IAM/ADC to gcp-iam-identity, Cloud Run to gcp-cloud-run, Storage to gcp-cloud-storage, Pub/Sub to gcp-pubsub, Secret Manager to gcp-secret-manager, Cloud SQL to gcp-cloud-sql and model inference to gcp-vertex-ai.
3. Distinguish local gcloud CLI login from ADC in Python; distinguish OAuth access tokens for API calls from OIDC ID tokens and service URL audience when calling private Cloud Run; keep projects, regions and scopes explicit.
4. A deployed Cloud Run runtime service identity might differ from CI deployer, gcloud user and Cloud SQL DB user. End-to-end authorization includes IAM roles, resource ACL/policy, network VPC and database privileges. Do not grant project Owner to fix 403.
5. Verify deterministic checks first, then only authorized sandbox connectivity or dry-run. Any real infra apply/deletion requires separate explicit approval.

## Progressive references
- [Decisions and implementation](references/selection-and-implementation.md) — **read when** choosing tools, access, configuration or development workflow.
- [Safety, failures and release evidence](references/security-operations-and-tests.md) — **read when** hardening, operating, scaling, testing or releasing.

## Boundaries
Use a dedicated provider service skill for AWS/GCP/Azure/Cloudflare SDK operations. This skill owns GCP integration coordinator cross-service method only.

## Completion
Concrete decision, current-version limitations, scoped authorization, negative tests and measured or explicitly unknown operating evidence.
