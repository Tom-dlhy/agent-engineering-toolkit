/** Educational service ONLY. No persistent database or real identity provider. */
export type Actor = { tenantId: string; scopes: ReadonlySet<string> };
export type Order = { id: string; tenantId: string; quantity: number };

export class ForbiddenError extends Error {}
export class InvalidInputError extends Error {}

export function parseCreateOrder(input: unknown): { id: string; quantity: number } {
  if (typeof input !== "object" || input === null || Array.isArray(input)) {
    throw new InvalidInputError("expected object");
  }
  const data = input as Record<string, unknown>;
  if (typeof data.id !== "string" ||
      !/^[a-zA-Z0-9_-]{1,36}$/.test(data.id) ||
      typeof data.quantity !== "number" ||
      !Number.isSafeInteger(data.quantity) || data.quantity <= 0 ||
      Object.keys(data).some((key) => !["id", "quantity"].includes(key))) {
    throw new InvalidInputError("invalid order data");
  }
  return { id: data.id, quantity: data.quantity };
}

export class OrderService {
  private readonly orders = new Map<string, Order>();
  private readonly requests = new Map<string, string>();

  create(actor: Actor, input: unknown, idempotencyKey: string): Order {
    if (!actor.scopes.has("orders:write")) throw new ForbiddenError("denied");
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(idempotencyKey)) {
      throw new InvalidInputError("invalid idempotency key");
    }
    const body = parseCreateOrder(input);
    const operation = actor.tenantId + ":" + idempotencyKey;
    const priorId = this.requests.get(operation);
    if (priorId) {
      const prior = this.orders.get(actor.tenantId + ":" + priorId);
      if (!prior || prior.id !== body.id || prior.quantity !== body.quantity) {
        throw new InvalidInputError("idempotency payload changed");
      }
      return prior;
    }
    const key = actor.tenantId + ":" + body.id;
    if (this.orders.has(key)) throw new InvalidInputError("order id already exists");
    const result: Order = { id: body.id, tenantId: actor.tenantId, quantity: body.quantity };
    this.orders.set(key, result);
    this.requests.set(operation, body.id);
    return result;
  }

  get(actor: Actor, id: string): Order | null {
    if (!actor.scopes.has("orders:read")) throw new ForbiddenError("denied");
    return this.orders.get(actor.tenantId + ":" + id) ?? null;
  }

  count(): number { return this.orders.size; }
}
