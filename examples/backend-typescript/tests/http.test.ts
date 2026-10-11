import assert from "node:assert/strict";
import test from "node:test";
import { once } from "node:events";
import { makeServer } from "../app/server.ts";
import { OrderService, type Actor } from "../app/service.ts";

test("HTTP route, lifecycle, auth, invalid body and tenant isolation", async () => {
  const service = new OrderService();
  let principal: Actor | null = null;
  const server = makeServer(service, async () => principal);
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const address = server.address();
  if (!address || typeof address === "string") throw new Error("no address");
  const base = "http://127.0.0.1:" + address.port;
  try {
    assert.equal((await fetch(base + "/health")).status, 200);
    assert.equal((await fetch(base + "/orders/one")).status, 401);

    principal = { tenantId: "tenant-a", scopes: new Set(["orders:write", "orders:read"]) };
    const headers = { "content-type": "application/json", "idempotency-key": "request1" };
    let response = await fetch(base + "/orders", { method: "POST", headers, body: JSON.stringify({ id: "one", quantity: 1 }) });
    assert.equal(response.status, 201);
    assert.deepEqual(await response.json(), { id: "one", tenantId: "tenant-a", quantity: 1 });
    assert.equal((await fetch(base + "/orders/one")).status, 200);
    response = await fetch(base + "/orders", { method: "POST", headers, body: JSON.stringify({ id: "one", quantity: 1 }) });
    assert.equal(response.status, 201);
    assert.equal(service.count(), 1);
    assert.equal((await fetch(base + "/orders", { method: "POST", headers, body: "{" })).status, 400);
    assert.equal((await fetch(base + "/orders", { method: "POST", headers, body: JSON.stringify({ id: "two", quantity: -1 }) })).status, 422);

    principal = { tenantId: "tenant-b", scopes: new Set(["orders:read"]) };
    assert.equal((await fetch(base + "/orders/one")).status, 404);
    principal = { tenantId: "tenant-a", scopes: new Set() };
    assert.equal((await fetch(base + "/orders/one")).status, 403);
  } finally {
    server.closeAllConnections();
    await new Promise<void>((resolve, reject) => server.close(error => error ? reject(error) : resolve()));
  }
});
