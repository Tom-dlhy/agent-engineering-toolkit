# Unity Gateway monitoring, spend and legacy AI Gateway migration

Read when: auditing Databricks LLM/MCP costs and traces, replacing older AI Gateway endpoint governance or releasing new service policies.

## Separate services and spend
Unity Gateway model/service/provider route governance, MLflow trace/experiment evaluation, model-serving compute and external provider charges may be separate billing/telemetry dimensions. Do not assume a token count multiplied by a generic price covers provider, serving, gateway, judge and tool costs. Record actual consumption by model/service/principal/tenant, quotas, fallback rate, failures, latency and data category.

MLflow may capture model/agent traces; these can contain private prompt text, retrieved documents, tool parameters or identity information. Redact/minimize, scope grants, set retention and review data residency. A monitoring dashboard without verified event capture and alerts is not actual observability.

## Migration from legacy endpoint AI Gateway
1. Inventory current serving endpoint, gateway feature settings and installed clients, policies, logs, models and external provider credentials.
2. Compare Unity Gateway **capability/region** and role/service policies; map old endpoint identity to new service/route rather than blindly copying settings.
3. Pin endpoint contract, streaming events, response shapes, fallback, metrics and refused/unauthorized cases.
4. Rehearse in isolated dev service; measure paired answer behavior, token cost, latency and abuse-denial outcomes.
5. Plan reversible traffic routing and secret/provider controls; migration is a release requiring approval.
6. Monitor post-cutover quality and incidents by error category and policy deny; rollback if security/data residency or cost guardrails regress.

## Evaluation matrix
- correct model route, tool schema, refusal and safe fallback;
- denied tenant cannot access restricted MCP, documents or model;
- prompt injection doesn't override per-tool authorization;
- quotas prevent runaway token/tool-loop spend;
- telemetry fields redact input and contain correct version and identity;
- response contract survives provider failover or errors;
- operational metrics and user task correctness compared to baseline.

No actual gateway route, paid LLM call, policy change or cross-region transfer was executed here.

Sources: https://docs.databricks.com/aws/en/ai-gateway/ and https://docs.databricks.com/aws/en/ai-gateway/configure-ai-gateway-endpoints and https://docs.databricks.com/aws/en/unity-gateway and https://docs.databricks.com/aws/en/mlflow3/genai/eval-monitor/production-monitoring
