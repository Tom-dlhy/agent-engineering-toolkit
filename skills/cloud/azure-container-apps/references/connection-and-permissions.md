# Azure Container Apps — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
`az login` selects dev subscription; use `az account set --subscription` only when requested. Runtime app uses attached Managed Identity, distinct from deployer and registry pull identity. Deployer requires approved Container Apps/resource group scope; runtime MI receives narrow Key Vault/Blob/Service Bus data roles. Container registry pull requires correct AcrPull/identity; secrets references and ingress policy separate.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
Azure CLI management-plane `az containerapp show` and runtime application SDK with Managed Identity.

~~~bash
# Read-only Azure CLI commands. The app container uses ManagedIdentityCredential for its data calls.
az account show --query "{subscription:id,tenant:tenantId}"
az containerapp show --resource-group "$RG" --name "$APP" --query "{id:id,provisioningState:properties.provisioningState}"
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/container-apps/managed-identity
- https://learn.microsoft.com/en-us/azure/container-apps/scale-app
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
