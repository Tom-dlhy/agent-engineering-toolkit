# Saga design, compensation and reconciliation

**Read when:** distributed business operation spans multiple
independently owned data stores and must recover from partial success.

## Local steps, not global rollback

ReserveInventory → ChargePayment → ConfirmOrder.
If payment fails, release reservation. Compensation is a new
business action that may itself fail. Sagas do not grant
database isolation across services and may show intermediate states.

| Pattern | Useful when | Main cost |
|---|---|---|
| Keep one database transaction | One consistent owner can cover invariant | No independent service deploy |
| Saga choreography | Few autonomous participants | Distributed control and troubleshooting |
| Saga orchestration | Many steps/approvals or explicit compensation | Durable coordinator and state handling |

~~~text
CREATED → INVENTORY_RESERVED → PAYMENT_AUTHORIZED → CONFIRMED
             |                       |
             v                       v
      RELEASE_PENDING          REFUND_PENDING
             |                       |
             v                       v
          CANCELLED               CANCELLED
~~~

Track operation_id, step, durable status, tenant ownership,
idempotency keys, retry attempts and compensation state. A
payment timeout can conceal success; query provider/ledger
before recharging. Reconciliation and human escalation need
explicit support, not silent "retry until green".

## Validate uncertainty

Crash before/after each step, after remote payment succeeded,
before local persist, duplicate command, stale event, temporary
compensation failure, worker restart and stuck terminal state.
Define customer-facing eventual consistency and maximum delay.

## Avoid

Spinning up saga for two operations that fit one SQL transaction,
pretending compensation undoes time or notifications, global
in-memory coordinator, SQL lock held during remote provider call,
and exact-once claims without an end-to-end invariant test.

Sources:
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-patterns.html ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html ,
https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html .
