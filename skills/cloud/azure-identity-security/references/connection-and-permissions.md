# Azure Identity, Entra and RBAC — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
`az login` locally for Azure CLI identity; verify `az account show` correct tenant/subscription. Deploy with system/user-assigned Managed Identity and exact Azure RBAC data/control plane role at resource scope; identify token audience. Data plane vs ARM management roles differ. Azure RBAC assignment can propagate with delay. `AZURE_TOKEN_CREDENTIALS=prod` (azure-identity >=1.23) narrows DefaultAzureCredential chain; explicit ManagedIdentityCredential reduces ambiguity further.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
`azure.identity.DefaultAzureCredential` for local; `ManagedIdentityCredential` with explicit client_id for intended production managed identity.

~~~python
from azure.identity import DefaultAzureCredential
cred = DefaultAzureCredential()  # local development; production prefer explicit ManagedIdentityCredential
token = cred.get_token("https://management.azure.com/.default")
# Token is sensitive; never print or use management token for storage data plane.
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/user-assigned-managed-identity
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
