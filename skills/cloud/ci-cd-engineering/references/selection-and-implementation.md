# CI/CD and federated cloud deployment — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Separate untrusted pull request verification from privileged deploy jobs. Pin actions immutable SHAs, constrain GITHUB_TOKEN, use environment approvals and repository/ref/environment claims for federated OIDC.

## Implementation decisions
GitHub OIDC `id-token: write` permits requesting identity JWT but does NOT itself give cloud permissions; AWS/GCP/Azure trust policy grants cloud role conditioned on issuer/audience/subject. Tokens must never appear in logs.

## Starter illustration
~~~text
permissions:
  contents: read
# Deployment job ONLY with trusted environment:
# id-token: write
# require cloud trust subject conditions and explicit approval
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers
- https://docs.github.com/en/actions/security-for-github-actions/security-guides/automatic-token-authentication
