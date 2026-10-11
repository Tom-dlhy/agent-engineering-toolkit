# Stacks — source-reviewed decision audit and governance

**Date:** 2026-10-11. **Base:** `main` following Growth PR #24. **Charter:** Agent Engineering Toolkit governance v2. Domain decision: **3 EXTEND, 1 CREATE, 0 IMPORT / DELETE**. Product/implementation details belong to their existing specialist.

## Mandatory decision matrix

| Candidate | Verdict | Unique trigger and responsibility | Existing skill not to duplicate |
|---|---|---|---|
| `stack-advisor` | **EXTEND** | Select **coherent end-to-end stack** for a product under hard constraints, including compatibility matrix, cost, reversibility | `architecture/technology-tradeoffs` generic comparisons; `architecture/architecture-decision` ADR/system styles; `cloud/cloud-provider-selection` provider/compute fit |
| `database-selection` | **EXTEND** | Choose data store engine and managed operating model from transaction/query/concurrency/restore needs | `data/database-design` schema; `schema-migrations` rollout; `postgres-performance` plans; `cloud/cloudflare-d1-database` provider bindings |
| `ui-library-selection` | **EXTEND (selectively)** | Choose current-compatible component provider and explicitly requested migration with source/license/SSR and accessibility checks | 35 `skills/ui/*` vendor APIs; `design-system` tokens; `data-visualization-design` truthful chart representation |
| `authentication-solution-selection` | **CREATE (opt-in)** | Choose end-user identity/session solution, OIDC/SSO, library vs managed provider vs private edge gate, migration and safety gates | `cloud/aws-iam-security` workload IAM; `cloud/cloudflare-access-security` Access configuration; `secure-code-review` actual authorization audit; frontend/backend adapter code |

**After refactor:** Stacks **4 skills / 12 leaf references**, up from **3 / 1**; project **151** catalog entries. Unchanged **20 installation profiles**, no framework/provider migration or downloads.

## Checklist — why precisely one new skill?

1. **Useful?** Selecting end-user identity has standalone inputs/outputs, materially irreversible account/session data and security constraints. Yes.
2. **Already present?** Cloud IAM is service-to-service; Cloudflare Access is a single provider's edge implementation, not a provider-neutral end-user auth library/service selection. App authorization audit isn't identity strategy. No direct existing owner.
3. **Better extend?** The current stack-advisor handles whole-product choices but doesn't own full user identity/session/federation lifecycle. Distinct and expensive enough for independent selection and tests.
4. **Correct existing folder?** Under `skills/stacks` alongside database/UI choice. No new category.
5. **Trigger/exclusion?** Explicit when app identity selection versus IAM policy/route authorization/provider SDK fixed implementation.
6. **Dependencies?** No auth SDK or credentials auto-installed. User must authorize selection implementation separately.
7. **Validation?** Negative routing, isolated deterministic gate examples, references and context budgets; live integration and real security review remain unproven.

## Ideas deliberately not created

| Proposed skill | Decision | Rationale |
|---|---|---|
| `frontend-framework-selection` | **REFERENCE/EXTEND stack-advisor** | End-to-end rendering/build/runtime tradeoffs and `technology-tradeoffs` already cover comparative framework evidence. Framework skills own final APIs. Re-evaluate only after many independent held-out requests. |
| `orm-selection` | **REFERENCE database-selection** | Driver, dialect, migrations and query lifecycles depend on chosen engine/runtime. `backend/python-persistence` owns concrete ORM work. |
| `hosting-platform-selection` | **REUSE cloud-provider-selection** | Explicitly covers AWS/GCP/Azure/Cloudflare managed/serverless/container selection, regional/IAM/cost. Duplicate would compete for triggers. |
| `authjs`, `clerk`, `better-auth` vendor micro-skills | **DEFER** | First prove independent provider-specific implementation volume and SDK stability. A neutral selector does not become a provider cookbook. |
| `state-management-selection`, `css-framework-selection` | **REFERENCE stack-advisor/technology-tradeoffs** | Smaller product-level dependency decisions; only split if measurable distinct responsibility emerges. |
| `supabase-stack`, `neon-stack` | **REJECT** | Vendor stack shopping is not an independently useful generic discipline; prefer selected database and cloud specialists. |

## Official, source-reviewed facts and risks

**Architecture decisions:** AWS Well-Architected has six pillars and explicitly recommends evaluating tradeoffs; Google Cloud/Azure also favor documented workload-driven quality tradeoffs and ADRs, not picking by a vendor popularity score:
- https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html
- https://docs.aws.amazon.com/wellarchitected/2024-06-27/framework/ops_priorities_eval_tradeoffs.html
- https://docs.cloud.google.com/architecture/framework
- https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework

**Database semantics:** PostgreSQL transactional isolation needs actual conflict/serialization checks; SQLite WAL enables concurrent reading but only one writer at a time. Cloudflare D1 is SQLite-based but constrained by its provider/API/plan and per-database query serialization; dated numbers must be reverified when deciding.
- https://www.postgresql.org/docs/18/transaction-iso.html
- https://www.sqlite.org/wal.html
- https://developers.cloudflare.com/d1/platform/limits/
- https://neon.com/docs/connect/connection-pooling

**UI:** shadcn's July 2026 new-project default is Base UI while Radix remains supported. Never force migration of existing apps. Advanced Grid/chart component APIs and MUI X licensing are **provider-specific**, not generic design/UI selection truths.
- https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default
- https://mui.com/x/react-data-grid/
- https://www.w3.org/WAI/test-evaluate/

**Identity:** OIDC is an identity layer over OAuth2; identity ≠ authorization. OWASP covers secure browser sessions/CSRF and object authorization; NIST covers MFA and phishing resistance. Self-hosted identity vs managed Identity has different operational responsibility; no single vendor automatically proves normative compliance.
- https://openid.net/specs/openid-connect-core-1_0.html
- https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- https://pages.nist.gov/800-63-4/sp800-63b/introduction/
- https://better-auth.com/docs/concepts/session-management

Stack Overflow/community posts may reveal reproducible edge cases but do not override version-matched vendor docs, security standards or actual installed code. No third-party skill was vendored, no untrusted script executed.

## Ownership and negative routing map

| Request | Primary | Must not hijack |
|---|---|---|
| "Design a coherent SaaS stack under a strict EU hosting and budget envelope" | `stack-advisor` | all framework/UI provider bodies, generic inspiration |
| "Should we use PostgreSQL, SQLite WAL or Cloudflare D1 for concurrent writes?" | `database-selection` | database-design (schema) before engine choice |
| "We already have shadcn; migrate to MUI and check DataGrid licensing" | `ui-library-selection` | replacing existing stack without explicit approval |
| "Select a passkey/SSO/auth solution for a multi-tenant customer app" | `authentication-solution-selection` | AWS IAM or authentication code without selection |
| "Grant Lambda permission to read an S3 object" | `aws-iam-security` | end-user auth selection |
| "Configure Cloudflare Access app policy" | `cloudflare-access-security` | generic auth provider comparison |
| "Fix missing SQLAlchemy rollback" | `python-persistence` | database-selection |
| "Implement Base UI dialog composition" | `base-ui` | ui-library-selection |
| "Migrate SQL schema without downtime" | `schema-migrations` | database-selection |
| "Why did our p95 query regress on PostgreSQL?" | `postgres-performance` | stack advisor |

## Validation scope

CI/static assertions verify registry uniqueness, reference safety, deep routing, negative cases, unchanged profile budgets, provider reuse and isolated hard-veto examples. `evals/stacks-routing.yaml` specifies **future held-out real-agent evaluations** only; no model calls, live providers, auth federation tests, migration rehearsal or measured performance undertaken by this PR. `examples/stacks-selection` has a pure Python reference decision gate, **not** a security control or a replacement for engineering judgment.

### Next after all 12 categories
Cross-domain held-out agent benchmark: before/after toolkit on representative user jobs, routing/negative activation, true context tokens, real code quality/functional tests, browser/AT and authorized vendor auth/database migrations. Iterate only where real observed failures justify new skills or deep leaves; not a perpetual catalog growth campaign.
