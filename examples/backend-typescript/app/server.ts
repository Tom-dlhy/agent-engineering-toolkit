/** HTTP adapter with injected authentication; no real credentials, database or network. */
import { createServer } from "node:http";
import { ForbiddenError, InvalidInputError, OrderService, type Actor } from "./service.ts";

export function makeServer(
  service: OrderService,
  authenticate: (request: import("node:http").IncomingMessage) => Promise<Actor | null>,
) {
  return createServer(async (request, response) => {
    function send(status: number, payload: object) {
      response.writeHead(status, { "content-type": "application/json" });
      response.end(JSON.stringify(payload));
    }
    try {
      if (request.method === "GET" && request.url === "/health") {
        send(200, { status: "ok" }); return;
      }
      const actor = await authenticate(request);
      if (!actor) { send(401, { code: "unauthorized" }); return; }
      const parsed = new URL(request.url ?? "/", "http://localhost");
      if (request.method === "GET" && /^\/orders\/[A-Za-z0-9_-]{1,36}$/.test(parsed.pathname)) {
        const order = service.get(actor, parsed.pathname.slice("/orders/".length));
        send(order ? 200 : 404, order ?? { code: "not_found" });
        return;
      }
      if (request.method === "POST" && parsed.pathname === "/orders") {
        const chunks: Buffer[] = [];
        let length = 0;
        for await (const chunk of request) {
          const buf = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
          length += buf.length;
          if (length > 16_384) { send(413, { code: "too_large" }); return; }
          chunks.push(buf);
        }
        let input: unknown;
        try { input = JSON.parse(Buffer.concat(chunks).toString("utf-8")); }
        catch { send(400, { code: "invalid_json" }); return; }
        const key = request.headers["idempotency-key"];
        if (typeof key !== "string") { send(400, { code: "missing_idempotency_key" }); return; }
        const created = service.create(actor, input, key);
        send(201, created);
        return;
      }
      send(404, { code: "route_not_found" });
    } catch (error) {
      if (error instanceof ForbiddenError) send(403, { code: "forbidden" });
      else if (error instanceof InvalidInputError) send(422, { code: "invalid_input" });
      else send(500, { code: "internal_error" });
    }
  });
}
