# Azure Blob Storage — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
Local `az login` and assigned Storage Blob Data Reader/Contributor; production ManagedIdentityCredential. Management role Contributor isn't necessarily Blob *data* access. Reader: Storage Blob Data Reader; writer: Storage Blob Data Contributor scoped container/account as supported. SAS signing/service permissions differ; avoid account shared keys, grant user delegation key only where needed.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
`azure.storage.blob.BlobServiceClient` and `DefaultAzureCredential`.

~~~python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
client = BlobServiceClient(
    account_url=f"https://{STORAGE_ACCOUNT}.blob.core.windows.net",
    credential=DefaultAzureCredential(),
)
properties = client.get_blob_client(container=CONTAINER, blob=KEY).get_blob_properties()
# Separate write path must use conditions/ETag and authorized Data Contributor.
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python
- https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-upload-python
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
