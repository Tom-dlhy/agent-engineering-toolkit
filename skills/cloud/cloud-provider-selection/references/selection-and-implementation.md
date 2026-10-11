# Cloud provider selection and workload placement — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Compare explicit deployment options (managed serverless vs container vs DB/queue), compliance/region, team knowledge, latency, SLA, integration, cost, egress and lock-in; never compare brand adjectives.

## Implementation decisions
Use current official capabilities/prices by region and account terms; map IAM, networking, quotas and data migration costs. Include non-production/staging, incident ownership, platform maintenance and exit path.

## Starter illustration
~~~bash
# Comparison worksheet: candidate, region, identity, state, peak, egress, SLO, monthly range, exit cost.
# No deployment without explicit owner approval.
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/
