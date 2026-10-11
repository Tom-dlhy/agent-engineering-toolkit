# Transactional outbox and idempotent inbox

**Read when:** database state change must trigger an external event
without the dual-write lost-message window, or a consumer may
receive duplicates.

## Atomic local write

Without outbox, DB commit then publish can crash between steps,
and publish then DB commit can notify of rolled-back state.

~~~sql
BEGIN;
UPDATE orders SET status = 'confirmed', version = version + 1
  WHERE id = :id AND tenant_id = :tenant AND status = 'pending';
-- Check affected row count before inserting event.
INSERT INTO outbox(event_id, aggregate_id, event_type, body)
  VALUES (:event_id, :id, 'order.confirmed', :body);
COMMIT;
~~~

Conceptual SQL: parameter syntax/dialect/locking and error handling
depend on real driver. The publishing worker sends committed rows
and marks them sent. If it crashes after send before mark it sends
**again**. Outbox guarantees local atomic persistence of intent
when correctly implemented, not end-to-end exactly-once processing.

## Inbox consumer boundary

~~~text
receive message(event_id)
BEGIN
  insert (consumer_name,event_id) in processed_events
  if newly inserted:
      validate schema/tenant/sequence
      apply business mutation in same transaction
COMMIT
ACK broker after commit
~~~

Use a database unique constraint, not an in-memory set across replicas.
External payments/emails require their own stable idempotency key and
uncertain-outcome reconciliation; inbox dedupe alone cannot atomically
commit a third-party HTTP side effect.

## Required failure cases

DB insert rollback, publisher crash before send, crash after send,
consumer duplicate after commit-before-ack, out-of-order event,
poison message, DLQ recovery and old schema replay.
Observe oldest pending event age, retry rate and consumer lag.
Never leave an SQL transaction open across a slow LLM/network call.

Sources: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html and
https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-out-box-cosmos .
