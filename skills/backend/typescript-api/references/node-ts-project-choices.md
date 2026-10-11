# Node.js TypeScript backend — choose runtime, framework and build

**Read when:** selecting Fastify, Express, NestJS, native Node HTTP
or TypeScript module/tooling conventions for a backend.

| Server | Good fit | Cost |
|---|---|---|
| Native node:http | Tiny no-framework service | Own routing, validation, errors |
| Fastify | Schema-first HTTP and encapsulated plugins | Ajv/JSON Schema and plugin lifecycles |
| Express | Broad compatible ecosystem | Set up validation, errors, typed integrations |
| NestJS | Modules and DI for bigger teams | Framework metadata and ceremony |
| Existing fullstack routes | App-local server actions | Runtime/deploy conventions constrain server |

Preserve a coherent project instead of rewriting because another
framework seems fashionable. Judge by route/data workload,
team ownership, dependencies and actual operational costs.

## Strict project setup
TypeScript strict enables strictNullChecks and noImplicitAny
among checks. Choose Node release/LTS, ESM vs CommonJS and
tsconfig module target based on actual deployment. TS types
are erased, not runtime input validation. Runtime type stripping
in recent Node doesn't typecheck and supports only erasable
syntax: still run compiler in a production pipeline.

Pin lockfile/toolchain. Resolve actual build artifacts and
native packages on target OS. CI must not blindly download
npm lifecycle scripts with privileged cloud secrets.
Measure capacity and latency under realistic DB and downstream
limits, not a number of registered users.

## Tests
Clean install, TS compiler/typecheck, Node test runner,
server lifecycle, public API contract, process termination
and actual deployment import/bundle smoke. Verify auth
and error behavior in live framework integration separately.

Official: https://nodejs.org/api/typescript.html ,
https://nodejs.org/api/test.html ,
https://www.typescriptlang.org/tsconfig/strict.html ,
https://fastify.dev/docs/latest/Reference/Validation-and-Serialization/ .
