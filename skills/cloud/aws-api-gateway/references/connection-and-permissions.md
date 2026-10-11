# Amazon API Gateway — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: AWS API Gateway v2 control-plane via boto3/CLI; ordinary clients call the deployed HTTPS URL with required JWT or IAM SigV4.
- Bootstrap: aws sts get-caller-identity; aws apigatewayv2 get-apis --region eu-west-3; verify chosen HTTP API vs REST API feature compatibility.
- Authentication constraints: Separate deployment principal (apigateway management actions) from end-user JWT/IAM authorizers. Verify issuer, audience, scopes, custom domain and certificate.
- IAM actions: Deployment role scopes `apigateway:GET`/POST/PATCH etc and IAM permission to create integration; resource/route authorizer controls runtime. JWT scopes must be enforced per route; Lambda permissions must allow API Gateway invocation.

~~~bash
# Read-only control-plane check
aws apigatewayv2 get-apis --region eu-west-3
# Runtime call: HTTP client → HTTPS invoke URL with bearer JWT
# validated by configured JWT authorizer; do not use deploy-role tokens as user identity.
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html
- https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
