# FinOps spend and unit economics — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Measure compute idle/burst, storage and snapshots, networking/NAT/egress, managed DB, monitoring, queues, API calls and provider model tokens. Use cost per successful request/job as denominator instead of just total monthly spend.

## Implementation decisions
Budgets/alerts are not always hard spend cutoffs; compare actual provider billing exports and list prices with commitments, regional fees, free tiers and data egress. Separate estimate vs observed spend vs forecast.

## Starter illustration
~~~bash
# Evidence plan: export anonymized billing cost grouped by service and owner.
# Never authorize billable cloud resources merely to test a calculator.
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://www.finops.org/framework/capabilities/allocation/
- https://www.finops.org/framework/capabilities/unit-economics/
