# Azure Functions (Python v2) — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
Local Azure Functions Core Tools + `az login` for SDK access; deployed host managed identity for downstream connections. Connection bindings can use identity-based settings when extension supports. Runtime system-assigned MI with scoped storage/queue/etc roles; function host storage has separate permissions. Deployment principal needs publish/manage rights, not shared with function runtime.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
`azure-functions` Python v2 decorator `func.FunctionApp()` with host.json and application settings.

~~~python
import azure.functions as func
app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("ok", status_code=200)
# AuthLevel.FUNCTION is shared function key, not per-user authorization.
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python
- https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
