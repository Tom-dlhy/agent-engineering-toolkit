# AWS Secrets Manager — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: `boto3.client('secretsmanager').get_secret_value` or official client-side cache.
- Bootstrap: aws sts get-caller-identity; check correct secret ARN, region, stage/version, resource policy and KMS permissions.
- Authentication constraints: Use workload IAM role with secret-scoped `secretsmanager:GetSecretValue`; custom KMS key can require `kms:Decrypt`. Never commit or log payload.
- IAM actions: `secretsmanager:GetSecretValue` scoped to required secret ARN; add `kms:Decrypt` as applicable; rotation service role separate from reader. No broad ListSecrets for application reads.

~~~python
import boto3
secrets = boto3.client("secretsmanager", region_name="eu-west-3")
value = secrets.get_secret_value(SecretId=SECRET_ARN, VersionStage="AWSCURRENT")
secret_text = value.get("SecretString")
if secret_text is None: raise ValueError("Expected text secret")
# Parse only inside restricted application boundary, never print.
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets-python-sdk.html
- https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_cache-python.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
