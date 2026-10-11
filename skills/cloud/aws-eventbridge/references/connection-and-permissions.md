# Amazon EventBridge — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: `boto3.client('events')` and `put_events`, target registration via IaC.
- Bootstrap: aws sts get-caller-identity; select event bus (default/custom), source + detail-type namespace, region and authorized producer role.
- Authentication constraints: Role-based AWS SDK to chosen account, bus ARN and region. Producer and target invoke roles/resource policies are different permission layers.
- IAM actions: Producer `events:PutEvents` on bus; cross-account bus resource policy may additionally need principal/conditions; target permissions/roles vary by target service. Restrict bus and target scope.

~~~python
import boto3, json
events = boto3.client("events", region_name="eu-west-3")
result = events.put_events(Entries=[{
    "EventBusName": EVENT_BUS_ARN, "Source": "acme.orders",
    "DetailType": "OrderCreated", "Detail": json.dumps({"order_id": ORDER_ID}),
}])
if result.get("FailedEntryCount"): raise RuntimeError("Partial event publication")
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-targets.html
- https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-perms.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
