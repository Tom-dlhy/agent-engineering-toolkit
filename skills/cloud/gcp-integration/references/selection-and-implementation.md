# GCP integration coordinator — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Route IAM/ADC to gcp-iam-identity, Cloud Run to gcp-cloud-run, Storage to gcp-cloud-storage, Pub/Sub to gcp-pubsub, Secret Manager to gcp-secret-manager, Cloud SQL to gcp-cloud-sql and model inference to gcp-vertex-ai.

## Implementation decisions
Distinguish local gcloud CLI login from ADC in Python; distinguish OAuth access tokens for API calls from OIDC ID tokens and service URL audience when calling private Cloud Run; keep projects, regions and scopes explicit.

## Starter illustration
~~~bash
gcloud auth application-default login # local ONLY
 gcloud config get-value project # not proof of ADC project; confirm separately
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service
