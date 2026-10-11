# Azure integration coordinator — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Route Entra/IAM to azure-identity-security, Container Apps to azure-container-apps, Blob to azure-blob-storage, Service Bus to azure-service-bus, Key Vault to azure-key-vault, Functions to azure-functions-runtime, Azure Foundry to azure-ai-foundry.

## Implementation decisions
Use `DefaultAzureCredential` for local dev where suitable; prefer intended explicit `ManagedIdentityCredential` in deployed service with user-assigned identity. Check actual azure-identity version before use of AZURE_TOKEN_CREDENTIALS=prod. Ensure correct audience (data plane vs ARM).

## Starter illustration
~~~bash
az login
az account show --query '{subscription:id,tenant:tenantId}' # only CLI identity
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/user-assigned-managed-identity
