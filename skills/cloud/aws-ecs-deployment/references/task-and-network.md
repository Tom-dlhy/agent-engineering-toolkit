# ECS task definitions, roles and network

**Read when:** setting up Fargate tasks/services, roles, environment/secrets, VPC networking or target groups.

## Workload boundaries

- ECS *task definition*: versioned desired container settings (image, ports, CPU/memory, logs, roles, secrets).
- ECS *service*: maintains desired count and performs replacements/deployments.
- Task role: credentials for application API calls (S3, SQS, Bedrock, etc.).
- Task execution role: ECS agent tasks such as pulling ECR images and pushing logs; some secrets retrieval during injection.
- ECS Task networking on Fargate: `awsvpc`; each task obtains its own network interface and applicable security groups.

## Task definition shape (partial, illustrative)

```json
{
  "family": "example-api",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024",
  "taskRoleArn": "arn:aws:iam::111122223333:role/example-api-app",
  "executionRoleArn": "arn:aws:iam::111122223333:role/example-api-execution",
  "containerDefinitions": [{
    "name": "api",
    "image": "111122223333.dkr.ecr.eu-west-3.amazonaws.com/example-api@sha256:REPLACE_WITH_REAL_DIGEST",
    "essential": true,
    "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/example-api",
        "awslogs-region": "eu-west-3",
        "awslogs-stream-prefix": "api"
      }
    }
  }]
}
```

Do not deploy placeholders. A real image digest is required, and the log group and permissions must be provisioned. Review CPU/memory valid combinations for Fargate and architecture/platform compatibility.

## Network decision table

| Access | Control |
|---|---|
| Public internet users → API | Prefer HTTPS ALB → private tasks, security group task ingress only from ALB SG |
| Task → RDS | Database SG ingress from task SG only |
| Task → AWS API | VPC endpoints where appropriate or NAT path; verify DNS/routes and endpoint policies |
| Task → Internet API | Scoped outbound route, egress logging/allowlist where justified |
| Admin operation | No public SSH; use ECS Exec only when explicitly enabled/authorized and logged |

Avoid public IP on tasks without a clear reason. Network reachability and authorization are distinct: SGs/VPC endpoint policies do not grant IAM permissions.

## Secrets

Use Secrets Manager/SSM parameter references with IAM grants and rotation plan, not plain sensitive `environment` strings or Docker image layers. Updating a secret does not necessarily update already-running tasks: review deploy/refresh strategy.

## Verify

Run a task in private subnet; assert app can reach intended S3 resource but not unrelated resources, health check succeeds and unauthenticated endpoints remain protected. Confirm IAM denies from execution role vs task role and log delivery works.

Official: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html and https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html .
