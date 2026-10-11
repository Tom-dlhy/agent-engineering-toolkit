# AI safety and ACL contract fixture — NOT a production agent

No model calls, APIs, cloud provider, filesystem mutation or money.
The Python standard-library harness asserts pre-execution tool
authorization, exact approval digest and query-time tenant ACL.

Run:
~~~bash
python -m unittest discover -s tests -p 'test_ai_security_contract.py' -v
~~~

This is intentionally **in-memory** and lacks durable idempotency,
real authentication, approval expiry/revocation, user interface,
remote side-effect recovery, proper search relevance, and signed
audit logs. Treat it as a proof of contract shape, NOT a model
prompt-injection defense certification. A real agent must use a
durable store, authenticated actor and independent executor policy.
Sources: https://genai.owasp.org/llm-top-10/ and
https://modelcontextprotocol.io/specification/2026-07-28 .
