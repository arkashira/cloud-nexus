Generated `partner-targets.md` for **cloud-nexus**. (The existing file held a stale `multi-model-tester` pack from a prior run — replaced it.)

Key calls in the deliverable:

- **8 partners, ranked rev-share → distribution → stickiness**, mapped to cloud-nexus's actual position *above* the IaC/ops layer (connective tissue, not another Terraform/Datadog).
- **The money:** AWS Marketplace co-sell (~0–3% fee + AWS-sourced pipeline) is framed as the go-to-market itself, not a feature. Azure second. Jira + Datadog marketplaces (75% vendor share) are the only true affiliate-grade SaaS economics in the space.
- **4-phase sequence:** cheap MVP loop (Slack/Terraform/GitHub, no partner bureaucracy) → monetize (AWS + Jira) → prove ROI + expand (Datadog + Azure) → enterprise FinOps only on pull.
- **Opinionated risk flags for PRD:** start partner-cert applications early (6–10 wk lead), don't parallelize both clouds, tag every resource with a milestone ID (cost-attribution is the differentiating-and-fragile core), read-only integrations first.

One note worth surfacing upstream: the `Market data: {}` field came in empty — the free-tier limits and fee percentages here are from general knowledge, not fed market data, so they should be verified against live partner terms before they land in a binding business pack.