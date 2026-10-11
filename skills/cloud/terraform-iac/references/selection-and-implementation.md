# Terraform/OpenTofu infrastructure as code — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Modules should express narrow capabilities, typed variables/outputs, pinned providers and isolated state by environment/security boundary; do not use workspaces as automatic tenant isolation.

## Implementation decisions
Remote backend with access policy and locking where supported; backends have **optional locking**, don't claim every backend locks. Terraform plans and state can expose sensitive values including when CLI hides them; secure artifact retention.

## Starter illustration
~~~bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
# Never terraform apply here; plan requires controlled backend/account.
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://developer.hashicorp.com/terraform/language/state/backends
- https://developer.hashicorp.com/terraform/language/block/terraform
