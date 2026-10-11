---
name: gcp-integration
domain: cloud
version: "0.1.0"
description: >-
  Use when building integrations with Google Cloud services such as Cloud Run, Cloud Storage, Pub/Sub, BigQuery or Vertex AI. Do not use for AWS-only or Azure-only implementations.
---

# gcp-integration

## Identity and service boundaries
Use Application Default Credentials and workload identity federation where appropriate, not committed service-account JSON keys. Scope IAM at the smallest necessary resource and avoid primitive Owner/Editor roles. Keep google-cloud SDK calls outside domain logic.

## Reliability
Set API deadlines and retry only transient/idempotent calls; design Pub/Sub handlers for redelivery, ordering constraints and dead-letter behavior. Distinguish BigQuery analytical jobs from transactional storage. Check region, quotas, concurrency and cold-start assumptions for Cloud Run. Validate data residency and encryption requirements.

## Testing
Mock narrow adapter protocols for domain unit tests; use test projects and representative fixtures for integration tests. Log safely, export useful metrics and document quotas/cost/egress assumptions. Do not enable services, create resources or mutate IAM without permission.
