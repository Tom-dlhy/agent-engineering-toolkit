# Kubernetes workload deployment — practical decision and configuration

**Read when:** selecting a production implementation, composing multiple services or checking how to configure the relevant tool.

## Architecture / method
Differentiate startup probe (initialization), readiness (receive traffic) and liveness (restart deadlocked process). A failing readiness stops routing; a failing liveness triggers restart, not a trivial interchangeable health check.

## Implementation decisions
Use service accounts with bounded RBAC, namespace policy, restricted PodSecurity, resource requests/limits, admission and NetworkPolicy provider support. Plan disruption/rollout/termination and storage migration separately.

## Starter illustration
~~~bash
kubectl config current-context
kubectl apply --dry-run=client -f ./k8s # local syntax only; NOT a live-cluster proof
~~~

Examples are illustrative, use no real customer credentials and may require a project-specific runtime, account policy or pinned dependency. No cloud mutation is authorized by reading a skill. Keep service-specific code in the service specialist rather than guessing common SDK semantics.

## Evaluation criteria
Compare simpler alternative first; document input sizes, failure consequences, developer experience, provider/account version, regional availability, test costs and reversibility. Benchmark meaningful workloads rather than prescribing microservices or instance count from number of users.

## Official references
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://kubernetes.io/docs/concepts/security/rbac-good-practices/
