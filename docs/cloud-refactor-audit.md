# Cloud refactor — source-verified audit and quality limits

Date: 2026-10-11. Base: main after merged AI PR #18. Governance: user's Agent Engineering Toolkit Charter V2, **one uniform skill quality contract**, no maturity tiers; maximize knowledge available and minimize unnecessary loaded context. No third-party executable imported.

## Audit — reuse vs new

Starting: **19 Cloud skills**. Existing AWS integration, IAM, S3, SQS, Lambda, ECS, Bedrock were already deep with two on-demand references each; Azure Foundry and GCP Vertex had two deep references each. Retained those nine specialized skills unchanged as the authority for those services.

Extended **ten** shallow existing skills in place: azure-integration, gcp-integration, cloudflare-platform, cloud-provider-selection, terraform-iac, ci-cd-engineering, container-hardening, kubernetes-deployment, observability-sre, finops-engineering. Each gained two targeted references, concrete implementation criteria, release failure scenarios and official sources.

Added **22** task-independent service specialists: AWS 6 (RDS, DynamoDB, EventBridge, Secrets Manager, VPC, API Gateway); GCP 6 (IAM/ADC, Cloud Run, Storage, Pub/Sub, Secret Manager, Cloud SQL); Azure 6 (Entra/Managed Identity, Container Apps, Blob, Service Bus, Key Vault, Python Functions); Cloudflare 4 (Workers, R2, D1, Access).

Why new: each has a distinct service API, auth/permission boundary, data model/semantics, failure/retry behavior and reason for activation. Provider coordinators **route rather than duplicating**. Outcome: **41 Cloud skills**, **82 indexed on-demand references**, **141 catalog skills**, **19 profiles**. Two references per Cloud skill is a documentation organization, not a maturity tier or requirement imposed on unrelated categories.

## Official fact checking

### AWS
- Boto3 credential provider chain: https://docs.aws.amazon.com/boto3/latest/guide/credentials.html .
- STS identity returns principal/account even without explicit GetCallerIdentity permission: https://docs.aws.amazon.com/boto3/latest/reference/services/sts/client/get_caller_identity.html .
- RDS IAM login uses IAM rds-db:connect and PostgreSQL role rds_iam, plus TLS/network: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/database-authentication.html .
- EventBridge classic target model vs custom bus/subscriber evolution: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html .
- Secrets Manager caching and stale value caveat: https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html .
- API Gateway HTTP API JWT authorizer issuer/audience/scopes: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html .

### Google Cloud Platform
- Google ADC chain and developer CLI login are different: https://docs.cloud.google.com/docs/authentication/application-default-credentials .
- Workload Identity Federation avoids long-lived JSON keys: https://docs.cloud.google.com/iam/docs/workload-identity-federation .
- Private Cloud Run requires OIDC ID token bound to receiver audience and roles/run.invoker: https://docs.cloud.google.com/run/docs/authenticating/service-to-service .
- Pub/Sub exactly-once delivery is feature/region/subscription constrained, not global HTTP exactly-once: https://docs.cloud.google.com/pubsub/docs/exactly-once-delivery .
- Cloud SQL Python Connector uses ADC and separate DB access: https://docs.cloud.google.com/sql/docs/postgres/connect-connectors .
- Secret Manager per-secret Secret Accessor: https://docs.cloud.google.com/secret-manager/docs/access-secret-version .

### Microsoft Azure
- DefaultAzureCredential is a chain, and azure-identity >=1.23 supports AZURE_TOKEN_CREDENTIALS=prod; production ManagedIdentityCredential can be more explicit: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains .
- Container Apps managed identity vs revision/KEDA scales: https://learn.microsoft.com/en-us/azure/container-apps/managed-identity and https://learn.microsoft.com/en-us/azure/container-apps/scale-app .
- Blob data role distinct from Azure Resource Manager Contributor: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python .
- Service Bus message settlement and role specifics: https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues .
- Python Azure Functions v2 decorator vs legacy v1 function.json: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python .

### Cloudflare
- Workers binding/secret scope: https://developers.cloudflare.com/workers/configuration/secrets/ .
- R2 Worker binding API differs from S3 and public r2.dev is development-oriented: https://developers.cloudflare.com/r2/api/workers/workers-api-reference/ and https://developers.cloudflare.com/r2/buckets/public-buckets/ .
- D1 prepared statements and bind prevent interpolated SQL values: https://developers.cloudflare.com/d1/worker-api/prepared-statements/ .
- Cloudflare Access JWT origin signature and audience must be validated as required: https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/application-token/ .

### Cross-platform
- Terraform backend locking is not guaranteed for every backend: https://developer.hashicorp.com/terraform/language/state/backends .
- GitHub OIDC id-token:write enables token request but not cloud permission by itself: https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers .
- Kubernetes startup vs readiness vs liveness probes: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ .
- FinOps cost allocation/unit economics: https://www.finops.org/framework/capabilities/unit-economics/ .

**SOTA** here means version-aware, sourced, testable recommendations, not a guarantee that one architecture suits all workloads. Public docs cannot establish actual tenant permissions, service enablement, cloud pricing, regional quotas or working code against the user's accounts.

## Implementation / verification

- One connection-and-permissions and one operations-and-recovery reference per new provider service; ten existing cross-provider skills similarly split.
- docs/cloud-service-map.md is an explicit selector and identity matrix, not an automatically loaded prompt.
- evals/cloud-routing.yaml: **22 positive** service-specific and **10 negative** neighboring prompts, plus no-match.
- tests/test_cloud_expertise.py validates the 41-skill domain, 82 references, source links, provider IAM terms, readable paths, progressive context budget and Python code fence syntax **without importing SDKs or sending requests**.
- Profiles: aws-platform 20; gcp-platform 15; azure-platform 15; cloudflare-edge 12. cloud-engineering remains a lighter provider-agnostic profile. The minimal profile unchanged.
- All historical Core/Quality/Architecture/Backend/Data/AI and app integration tests remain required in CI.

## Not proven

No AWS/GCP/Azure/Cloudflare live account connection, real permissions, private networking, region quotas, billing, DR, API version compatibility in deployment, Cloudflare Access JWT verifier integration or full security penetration test. Code snippets are documented starting points, **not automatically executable production recipes**. CI lexical routing is not an autonomous Codex/Claude behavioral evaluation. Don't claim production readiness until authorized sandbox identity/SDK and load tests.

Future candidates: AWS KMS/SNS/Step Functions, GCP Cloud Tasks/Eventarc/Firestore, Azure Cosmos/Event Grid/SQL, Cloudflare KV/Queues/Durable Objects/Workflows, managed K8s EKS/GKE/AKS, provider-specific monitoring. Create only after a real separate use case and no-duplication audit.

**Draft PR only. No merging or cloud mutations.**
