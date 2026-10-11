# Azure Key Vault — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
Local `az login`; production attached Managed Identity and correct tenant/vault URI. In apps prefer exact selected credential chain and separate identity for vault administration. `Key Vault Secrets User` (data-plane read) at vault or scoped resource where supported; `Key Vault Secrets Officer` needed to manage secrets; choose RBAC mode or legacy access policy per vault configuration, never assume both.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
`azure.keyvault.secrets.SecretClient` with `ManagedIdentityCredential` or `DefaultAzureCredential`.

~~~python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
client = SecretClient(vault_url=f"https://{VAULT_NAME}.vault.azure.net",
                      credential=DefaultAzureCredential())
secret = client.get_secret(SECRET_NAME)
secret_value = secret.value  # sensitive; never print/log
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python
- https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
