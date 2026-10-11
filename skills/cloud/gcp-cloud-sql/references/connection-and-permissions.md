# Google Cloud SQL for PostgreSQL — ADC, permissions and SDK usage

**Read when:** implementing application connectivity or debugging 401/403, project mismatch, IAM or API errors.

## Establish identity safely
Local: ADC login, explicitly set instance connection name PROJECT:REGION:INSTANCE, DB username/database and database credential mechanism.
Production: Service account with Cloud SQL Client role + Cloud SQL Connector using ADC; DB credentials/role (or IAM DB auth if configured) remain separate from Google IAM.
Common identity checks: `gcloud auth list` is **CLI**, while application code uses ADC; run `gcloud auth application-default print-access-token` only for authorized diagnostics and never record the token. `google.auth.default()` can reveal selected project without revealing secret; verify intended project and quota project. Use workload federation for CI/external hosts rather than persistent key files.

## Real service client
Cloud SQL Python Connector `google.cloud.sql.connector.Connector` + pg8000/asyncpg + SQLAlchemy. Required permissions: `roles/cloudsql.client` for connector; database user/privileges separate, use Secret Manager or IAM database authentication configuration. Private IP requires network reachability/VPC setup; connector isn't bypass of private routing.

~~~python
from google.cloud.sql.connector import Connector
# Instantiate Connector() once for application lifetime; it uses ADC
connector = Connector(refresh_strategy="LAZY")
conn = connector.connect(INSTANCE_CONNECTION_NAME, "pg8000",
                         user=DB_USER, password=DB_PASSWORD, db=DB_NAME)
try:
    conn.cursor().execute("SELECT 1")
finally:
    conn.close()
    connector.close()
~~~

Code is illustrative: identifiers are environment/project configuration, required package versions must be pinned, and network calls should only run on approved accounts. Do not print tokens, password, response payload containing PII or raw secrets.

## Fail-safe diagnosis
Pool connection fanout, auth token/DB TLS, instance/project mismatch, private IP/VPC egress, failover connections, migration/version compatibility, PITR/backups and read replica lag. Avoid DB master account in app.
Differentiate permission denied from disabled API, wrong project/region, missing network path and expired identity. Never grant Owner/Editor to work around an unknown AccessDenied.

## Official docs
- https://docs.cloud.google.com/sql/docs/postgres/connect-connectors
- https://docs.cloud.google.com/sql/docs/postgres/connect-run
- https://docs.cloud.google.com/docs/authentication/application-default-credentials
