# Identity architecture, federation, provider choices and make/buy

Read when: selecting app end-user authentication, SSO, hosted vs integrated session libraries or restricting a private one-user web application.

## First select the trust boundary
| User/application context | Possible fit | Red flag |
|---|---|---|
| Private internal/admin tool with fixed membership | Existing organization IdP or edge access gate (e.g. Cloudflare Access) | Edge proxy alone assumed to enforce tenant/document permissions |
| Customer web app with standard identity | Maintained framework-native auth library or managed IdP | Building custom password system |
| B2B organizations + enterprise SSO | OIDC/SAML-capable provider with org/tenant models | One global user role used as all tenant ACLs |
| Native/public API ecosystem | OIDC/OAuth with correct client registration and scopes | Treat OAuth access token as proof of identity without validation |
| Machine-to-machine | Workload identity / client credentials / service principals | Reuse end-user browser session or permanent shared secret |

**OIDC** is an identity layer on top of OAuth 2.0: `ID Token` is about authentication claims; OAuth access tokens authorize access to protected resources under defined audience and scopes. Neither gives automatic permission to arbitrary application objects. Follow the chosen provider SDK for exact validation. Source: https://openid.net/specs/openid-connect-core-1_0.html

## Provider shortlist discipline
Read lockfile, runtime and deployment topology first. Shortlist existing provider, one managed product, one maintained self-hostable/framework library as warranted. Examples to evaluate, not endorsements: Better Auth, Auth.js, Clerk, managed cloud identity (Cognito/Firebase/Auth0 etc), corporate IdP and Cloudflare Access for private apps. Provider compatibility, legal region, fees and entitlements change; official docs and actual support tickets are evidence, third-party blogs are leads only.

- **Managed** may reduce maintenance for password resets/SSO/abuse monitoring, at a cost in pricing and lock-in; validate exact plan and support obligations.
- **Library/self-hosted** can offer ownership/control, but team runs key rotation, email/reset, DB schema, abuse, audit and incidents.
- **Edge/private gate** can simplify private access but doesn't define all application-level authorization or replace identity for a consumer SaaS.

## Knockout criteria
Required organizations/SCIM/SAML, passkeys, MFA policy, phishing resistance, region/retention, session revocation speed, identity migration/export, account linking, audit trails, SDK support for the exact framework and end-to-end owner. Do not claim a provider meets NIST AAL simply because passkey or MFA marketing material exists.

Sources: https://openid.net/specs/openid-connect-core-1_0.html and https://pages.nist.gov/800-63-4/sp800-63b/introduction/ and https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Patterns_Cheat_Sheet.html
