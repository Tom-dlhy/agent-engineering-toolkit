# Cloud service routing and connection playbooks

Research review: 2026-10-11. This is a maintainer navigation map; **do not globally load it into an agent**. Select one provider, one skill and the relevant two references. All real access, IAM changes, deploys, charges, data writes or deletes require explicit authorization.

## Universal connection path

1. Select provider/service, operation (read/write/deploy), execution context and region.
2. Identify caller without printing tokens. AWS: STS ARN/account; GCP: ADC project/workload identity; Azure: subscription/tenant plus intended Managed Identity; Cloudflare: account/zone and Worker bindings.
3. Match *data-plane* permissions to resource (separately from deploy/control-plane roles). Database roles and application tenant permissions are additional boundaries.
4. Resolve endpoint/ARN/FQDN, TLS, network/security group/VPC/private endpoint and exact SDK/API version.
5. Prefer workload/federated short-lived identities; local interactive login is not a production deployment identity.
6. Use bounded deadlines/retries, dedupe or conditional operations for side effects, data/secret redaction and measurable observability.
7. Test mocked contract first and live connection only in an explicitly authorized sandbox; report evidence, quotas/cost and unknowns.

## AWS — aws-platform

| Skill | Target service | Authentication/connection |
|---|---|---|
| aws-integration | Cross-service AWS SDK | Boto3 provider chain and STS identity |
| aws-iam-security | IAM/STS | Roles, trust, resource policy, permission boundaries |
| aws-s3-storage | S3 | Boto3 S3, bucket/object grants and KMS |
| aws-sqs-messaging | SQS | Boto3 queue URL, producer/consumer scope |
| aws-lambda-runtime | Lambda | Execution role, event source/triggers |
| aws-ecs-deployment | ECS/Fargate | Task role versus execution role |
| aws-bedrock | Bedrock | Converse runtime model, region, role grants |
| aws-rds-postgres | RDS/Aurora Postgres | IAM rds-db:connect + DB rds_iam + TLS |
| aws-dynamodb | DynamoDB | Boto3 Table and table/index IAM |
| aws-eventbridge | EventBridge | events.PutEvents, bus/target policies |
| aws-secrets-manager | Secrets Manager | scoped GetSecretValue, KMS if required |
| aws-vpc-networking | VPC/NAT/PrivateLink | Route, security group, endpoint policy |
| aws-api-gateway | API Gateway | Management role vs end-user JWT/IAM auth |

AWS docs: https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
and https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/database-authentication.html .

## Google Cloud — gcp-platform

| Skill | Target service | Authentication/connection |
|---|---|---|
| gcp-integration | Multi-service | Google auth ADC; project/quota project |
| gcp-iam-identity | IAM and Workload Identity | ADC, workload SA, federation |
| gcp-cloud-run | Cloud Run private HTTP | OIDC ID token matching audience, Run Invoker |
| gcp-cloud-storage | Cloud Storage | Storage Client, bucket scoped roles |
| gcp-pubsub | Pub/Sub | Topic Publisher and Subscription Subscriber |
| gcp-secret-manager | Secret Manager | Accessor on specific secret version |
| gcp-cloud-sql | Cloud SQL PostgreSQL | Cloud SQL Connector + ADC AND DB credentials |
| gcp-vertex-ai | Gemini/Vertex AI | google-genai SDK, ADC, region and model |

The GCP CLI login and Application Default Credentials login are different. Calling a private Cloud Run URL requires an ID token for its audience; an API access token is not interchangeable. Docs: https://docs.cloud.google.com/docs/authentication/application-default-credentials and https://docs.cloud.google.com/run/docs/authenticating/service-to-service .

## Microsoft Azure — azure-platform

| Skill | Target service | Authentication/connection |
|---|---|---|
| azure-integration | Multi-service | Entra tenant/subscription, Azure Identity |
| azure-identity-security | Entra/Managed Identity/RBAC | Local DefaultAzureCredential; deployed explicit ManagedIdentityCredential |
| azure-container-apps | Container Apps | Deployer identity vs runtime MI, KEDA revisions |
| azure-blob-storage | Blob | BlobServiceClient and Blob **Data** role |
| azure-service-bus | Service Bus | ServiceBusClient, Data Sender/Receiver |
| azure-key-vault | Key Vault | SecretClient, Secrets User/Officer |
| azure-functions-runtime | Python Functions v2 | Functions decorators, identity-based bindings |
| azure-ai-foundry | Foundry managed inference | Azure deployment, Entra token and API version |

Contributor/control-plane roles are not automatically data-plane roles. DefaultAzureCredential may select a developer identity unexpectedly in production if unrestricted. Docs: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains and https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python .

## Cloudflare — cloudflare-edge

| Skill | Target service | Authentication/connection |
|---|---|---|
| cloudflare-platform | Multi-service coordinator | Account, zone, Wrangler env bindings |
| cloudflare-workers-runtime | Workers/Pages | Runtime binding, deployment token separately |
| cloudflare-r2-storage | R2 buckets | Worker R2Bucket or bucket-scoped S3 token |
| cloudflare-d1-database | D1 SQLite | Worker env DB, prepared bind query |
| cloudflare-access-security | Access protected apps | Identity-aware policy and signed JWT validation |

Worker runtime bindings are not Cloudflare management API tokens. R2 public r2.dev is intended for development use; D1 is SQLite, not Postgres; Access must not substitute for in-app object authorization.
Docs: https://developers.cloudflare.com/r2/api/workers/workers-api-reference/ and https://developers.cloudflare.com/d1/worker-api/ and https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/ .

## Cross-provider

cloud-provider-selection compares workloads; terraform-iac owns reviewed infra plans and state; ci-cd-engineering owns OIDC release governance; container-hardening owns OCI; kubernetes-deployment owns cluster workloads; observability-sre owns SLIs/SLOs; finops-engineering owns cost/unit economics.

## Unimplemented service candidates (explicit)

These are **not** covered by a dedicated skill: AWS Step Functions/SNS/KMS key policy/CloudWatch APIs; GCP Cloud Tasks/Eventarc/Firestore; Azure Event Grid/Cosmos DB/Azure SQL; Cloudflare KV/Queues/Durable Objects/Workflows; EKS/GKE/AKS cluster provisioning. Add only after charter duplicate/necessity review. This refactor is broad, not a claim to document every cloud product ever offered.
