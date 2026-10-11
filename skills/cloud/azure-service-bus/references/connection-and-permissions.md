# Azure Service Bus — connect, authenticate and authorize

**Read when:** implementing a service client or investigating Azure RBAC/Entra/Managed Identity failures.

## Developer versus deployed workload
Local `az login` and proper namespace resource; production Managed Identity with Azure Service Bus Data Sender or Data Receiver. Never log connection string. `Azure Service Bus Data Sender` for send and `Azure Service Bus Data Receiver` for settlement/receive; manage entities with separate control-plane role. Sessions, queues and topic subscriptions require corresponding permissions.

General identity boundary: `az account show` identifies CLI subscription and tenant, not the chosen production Managed Identity. `DefaultAzureCredential` may attempt environment/workload/developer credentials; pin `ManagedIdentityCredential(client_id=...)` in production where a user-assigned identity is intended, or use supported `AZURE_TOKEN_CREDENTIALS=prod` only on a verified azure-identity version. Token scopes/audience differ between management and data plane.

## SDK/CLI entrypoint
`azure.servicebus.aio.ServiceBusClient` with `azure.identity.aio.DefaultAzureCredential`.

~~~python
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
async with DefaultAzureCredential() as credential:
    async with ServiceBusClient(FULLY_QUALIFIED_NAMESPACE, credential=credential) as bus:
        async with bus.get_queue_sender(queue_name=QUEUE_NAME) as sender:
            await sender.send_messages(ServiceBusMessage("synthetic"))
~~~

All identifiers are validated app config; samples may require packages or a real authorized resource. Write-capable examples are illustrative and **must not be executed against live subscriptions** without authorization. Sensitive tokens, connection strings and keys must not be logged.

## First diagnostics
Compare actual caller object ID/tenant, credential-chain resolution, assigned identity, Azure RBAC data-plane role vs Contributor, propagation time, firewall/private endpoint and correct service URL. Grant only minimal service-scoped roles.

## Official docs
- https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-python-how-to-use-queues
- https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement
- https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/credential-chains
