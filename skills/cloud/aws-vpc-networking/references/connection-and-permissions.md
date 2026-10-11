# Amazon VPC networking — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: AWS CLI read-only `aws ec2 describe-route-tables`, `describe-security-groups`, `describe-vpc-endpoints` scoped by account/region.
- Bootstrap: aws sts get-caller-identity; aws ec2 describe-route-tables --region eu-west-3 --filters Name=vpc-id,Values=$VPC_ID
- Authentication constraints: Use STS identity and scoped EC2 Describe permissions for diagnostics; VPC resource changes require separate approved IaC role.
- IAM actions: Describe-only EC2 permissions for diagnostics; network changes may need `ec2:CreateRoute`, `AuthorizeSecurityGroupIngress` and IaC approval, not a blanket wildcard app role.

~~~bash
# Read-only diagnostic — never auto-create NAT routes or modify security groups
aws ec2 describe-security-groups --region eu-west-3 --group-ids "$GROUP_ID"
aws ec2 describe-vpc-endpoints --region eu-west-3 --filters Name=vpc-id,Values="$VPC_ID"
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html
- https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
