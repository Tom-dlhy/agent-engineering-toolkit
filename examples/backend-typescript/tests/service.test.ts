import assert from "node:assert/strict";
import test from "node:test";
import { ForbiddenError, InvalidInputError, OrderService, parseCreateOrder } from "../app/service.ts";

const actor = { tenantId: "tenant-a", scopes: new Set(["orders:write", "orders:read"]) };

test("runtime schema rejects invalid input independently from TS types", () => {
  for (const value of [null, [], { id: "x", quantity: 0 }, { id: "x", quantity: 2, secret: "oops" }]) {
    assert.throws(() => parseCreateOrder(value), InvalidInputError);
  }
  assert.deepEqual(parseCreateOrder({ id: "one", quantity: 2 }), { id: "one", quantity: 2 });
});

test("tenant isolation and read scope enforced by service", () => {
  const service = new OrderService();
  service.create(actor, { id: "one", quantity: 1 }, "unique-request");
  const other = { tenantId: "tenant-b", scopes: new Set(["orders:read"]) };
  assert.equal(service.get(other, "one"), null);
  assert.throws(() => service.get({ tenantId: "tenant-a", scopes: new Set() }, "one"), ForbiddenError);
});

test("replayed key is idempotent in memory, changed payload rejected", () => {
  const service = new OrderService();
  const first = service.create(actor, { id: "one", quantity: 1 }, "same");
  assert.strictEqual(service.create(actor, { id: "one", quantity: 1 }, "same"), first);
  assert.throws(() => service.create(actor, { id: "one", quantity: 2 }, "same"), InvalidInputError);
  assert.equal(service.count(), 1);
});

test("duplicate ID with a new key rejected", () => {
  const service = new OrderService();
  service.create(actor, { id: "one", quantity: 1 }, "first");
  assert.throws(() => service.create(actor, { id: "one", quantity: 1 }, "second"), InvalidInputError);
});
