# Roadmap

## Bootstrap (current)

- Compact rules and 3 workflow levels
- First-party skills across architecture, backend, cloud, design, data, AI, quality
- Curated install profiles for Codex and Claude Code
- CI with deterministic validation and unit tests
- No vendor code copied, no third-party dependencies automatically executed

## Planned: external Skill Package Manager

- Search, inspect, import, update and remove audited skills
- Pin exact SHA, track copyright/license/NOTICE and modifications in sources.lock.yaml
- Detect duplicate and contradictory activation triggers
- Validate scripts, tool permissions, dependencies and prompt-injection risk
- Evaluate candidate behavior before accepting updates

Candidates: obra/superpowers, affaan-m/ECC, mukul975/Anthropic-Cybersecurity-Skills, latent-spaces/brag.

## Planned: quality evaluation

- Scenario-based skill evaluations: accuracy, correctness, latency and activated skill count
- Real input/output token measurements only when exposed by the host
- Optional deep review, agent specialization, independent risk gates
- Expanding skills only when evidence shows benefit
