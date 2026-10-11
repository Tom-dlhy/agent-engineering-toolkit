# TypeScript runtime schemas, public DTOs and authorization

**Read when:** accepting API JSON, implementing Fastify validation,
mapping public responses or checking tenant/security boundaries.

## Type erasure demands actual validation
TypeScript interface assertions don't validate HTTP body;
parse untrusted values as unknown at the runtime boundary.

~~~typescript
type CreateOrder = { resourceId: string; quantity: number };
function parseOrder(input: unknown): CreateOrder {
  if (typeof input !== "object" || input === null || Array.isArray(input)) {
    throw new Error("invalid body");
  }
  const value = input as Record<string, unknown>;
  if (typeof value.resourceId !== "string" || !value.resourceId.trim() ||
      typeof value.quantity !== "number" ||
      !Number.isSafeInteger(value.quantity) || value.quantity <= 0) {
    throw new Error("invalid order");
  }
  return { resourceId: value.resourceId, quantity: value.quantity };
}
~~~

Handwritten guard is appropriate for narrow contracts. Complex nested
inputs may justify a schema library or JSON Schema/Ajv. Fastify
uses Ajv v8 and fast-json-stringify for validation and serialization;
official examples use JSON Schema Draft 7. It compiles schemas into
executable functions, so **never compile untrusted user-provided schema**.

## Safe route boundaries
Authentication identifies the caller; application logic must
authorize object/tenant access, not merely trust a tenant ID from JSON.
PATCH omission differs from explicit null/undefined depending on
wire contract. Allowlist response DTO fields: don't spread every
ORM/DB column including secret or internal state.

## Failure matrix
Array where object expected, unknown extra key, null vs absent,
wrong enum, guessed ID, cross-tenant list/update, invalid token,
untrusted error string and response accidentally serializing secret.

A schema-valid ID isn't evidence its object belongs to caller.
Errors should expose stable public status/code, not stack traces
or raw partner SDK exception contents.

Official: https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/ ,
https://www.typescriptlang.org/docs/handbook/2/basic-types.html ,
https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html .
