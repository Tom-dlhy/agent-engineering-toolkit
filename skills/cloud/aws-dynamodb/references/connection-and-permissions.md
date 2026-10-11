# Amazon DynamoDB — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: `boto3.resource('dynamodb')` Table API or low-level `boto3.client('dynamodb')`.
- Bootstrap: aws sts get-caller-identity; choose table + region + partition/sort key, verify `DescribeTable` separately if diagnosing.
- Authentication constraints: Default Boto3 credentials from role, account and explicit region. IAM permissions target table/index ARNs; Streams may require separate stream ARN actions.
- IAM actions: Grant only table ARN `dynamodb:Query`/`GetItem` to readers; `PutItem`/`UpdateItem` for writers and index ARNs where relevant. Conditional writes protect races; don't grant wildcard all tables.

~~~python
import boto3
from boto3.dynamodb.conditions import Key
table = boto3.resource("dynamodb", region_name="eu-west-3").Table(TABLE_NAME)
response = table.query(KeyConditionExpression=Key("tenant_id").eq(TENANT_ID), Limit=25)
items = response["Items"]
# Continue with LastEvaluatedKey for full pagination; query is not scan.
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
