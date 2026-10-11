# Amazon RDS for PostgreSQL — connection and least-privilege permissions

**Read when:** connecting to this AWS service from local Python, ECS/Lambda/EC2, diagnosing credentials or designing permissions.

## Local versus production identity
Local developer: `aws sso login --profile dev` if IAM Identity Center is configured, then `AWS_PROFILE=dev aws sts get-caller-identity` and explicit region. Production: use attached ECS task role/Lambda execution role/EC2 role or approved federated workload identity. `boto3.Session()` uses the documented provider chain and refresh mechanism; do not export developer keys to production. Beware environment variables overriding the intended role.

## Service-specific API
- Client/driver: boto3 RDS signer plus psycopg 3/SQLAlchemy; DB driver executes SQL.
- Bootstrap: AWS_PROFILE=dev aws sts get-caller-identity; verify account/region and DB endpoint; on Lambda/ECS use workload role, not developer profile.
- Authentication constraints: Use runtime IAM Role via boto3 Session; DB connection still requires PostgreSQL database role and TLS; `rds-db:connect` is distinct from `rds:DescribeDBInstances`. IAM auth requires role `rds_iam` on PostgreSQL DB user, explicit RDS host:port and short-lived generated token.
- IAM actions: `rds-db:connect` on specific DB-user resource ARN for IAM login; additional AWS RDS describe permissions only for management/diagnostic actions; DB GRANT/role must independently allow SQL.

~~~python
import boto3
session = boto3.Session(region_name="eu-west-3")
rds = session.client("rds")
token = rds.generate_db_auth_token(DBHostname=DB_HOST, Port=5432, DBUsername=DB_USER)
# Pass token to psycopg.connect(password=token, sslmode="verify-full",
# sslrootcert=AWS_RDS_CA_PATH). Do not log token; exact CA must be trusted.
~~~

Identifiers (`DB_HOST`, `TABLE_NAME`, `EVENT_BUS_ARN` etc.) must be supplied from validated application config. Snippet is illustrative and should be adapted to exact installed SDK/version. No mutation snippets should be executed against real accounts without explicit review.

## Diagnose denial
Compare caller ARN/account, assumed role/permission boundary, organization SCP, identity policy, resource policy, region and network endpoint; service-level authorization may require **both** AWS IAM and database/target-service permissions. Do not propose universal AdministratorAccess or wildcard fixes.

## Sources
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.Connecting.Python.html
- https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/database-authentication.html
- https://docs.aws.amazon.com/boto3/latest/guide/credentials.html
