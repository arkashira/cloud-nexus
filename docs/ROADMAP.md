# ROADMAP.md – cloud‑nexus

**Product Vision**  
A unified platform that translates high‑level business objectives into concrete, repeatable cloud‑migration and transformation plans, then drives automated execution, governance, and cost‑optimization across multi‑cloud environments.

---

## 📅 Milestones Overview

| Milestone | Target Date | Scope | MVP‑Critical? |
|-----------|-------------|-------|---------------|
| **MVP – “Launch‑Ready Planner”** | **2026‑09‑30** | Core planning UI, objective‑to‑architecture mapping, execution engine prototype, basic cost‑model, security & compliance guardrails. | ✅ |
| **v1 – “Enterprise Orchestrator”** | 2027‑03‑31 | Full‑featured execution engine, policy engine, multi‑cloud connectors, audit & reporting, role‑based access control. | – |
| **v2 – “Intelligent Optimizer & Marketplace”** | 2027‑10‑31 | AI‑driven recommendation engine, continuous cost‑optimization loop, marketplace for reusable patterns, integration with Axentx’s BRAIN for data‑driven insights. | – |

> **Note:** All dates are *planned* and will be revisited each sprint cycle. MVP‑critical items are highlighted with a ✅ and must be shipped before any public launch.

---

## 🚀 MVP – “Launch‑Ready Planner” (Target 2026‑09‑30)

| Feature | Description | Acceptance Criteria |
|---------|-------------|----------------------|
| **Business Objective Capture** | Guided wizard to input strategic goals (e.g., “Reduce latency < 50 ms”, “Cut cloud spend 20 %”). | • Objectives stored in normalized schema.<br>• Validation rules prevent contradictory inputs. |
| **Objective‑to‑Architecture Mapping Engine** | Rules‑based engine (leveraging Axentx BRAIN) that produces a high‑level target architecture (services, regions, data stores). | • Generates a diagram (Mermaid/PlantUML) and JSON spec.<br>• Mapping covers compute, storage, networking, security. |
| **Execution Blueprint Generator** | Translates architecture spec into IaC (Terraform) and CI/CD pipelines (GitHub Actions). | • Blueprint passes `terraform validate`.<br>• Pipeline YAML is syntactically correct and runnable in a sandbox. |
| **Cost‑Estimation Module** | Uses Axentx pricing data to produce a first‑order cost model (monthly & annual). | • Estimates within ±15 % of cloud provider calculators for test cases. |
| **Security & Compliance Guardrails** | Built‑in checks for IAM least‑privilege, data‑at‑rest encryption, and regional compliance (GDPR, HIPAA). | • CI lint fails on policy violations.<br>• Report generated for each blueprint. |
| **Minimal Viable UI** | React + Tailwind front‑end with dark/light mode; responsive for desktop. | • All MVP flows reachable in ≤ 3 clicks.<br>• No critical UI bugs (severity ≥ P2). |
| **AuthN/AuthZ** | Single‑sign‑on via OAuth2 (Google & Azure AD) with role‑based access (Owner, Editor, Viewer). | • Token validation enforced on every API endpoint.<br>• RBAC enforced in UI. |
| **Automated Tests & CI** | Unit, integration, and end‑to‑end tests covering 80 % of codebase; GitHub Actions CI pipeline. | • All tests pass on every PR.<br>• Coverage ≥ 80 %. |
| **Documentation & Onboarding** | Quick‑start guide, API reference (Swagger), and sample project repo. | • Docs build without errors.<br>• New user can create a plan in ≤ 15 min. |
| **Observability** | Basic logging (structured JSON) + health endpoint (`/healthz`). | • Logs shipped to Axentx’s central ELK stack.<br>• Health endpoint returns 200 when all services up. |

### MVP Success Metrics
- **Launch Readiness:** All ✅ items completed, security audit passed, and internal beta users (≥ 5) achieve ≥ 90 % task completion.
- **Performance:** Blueprint generation ≤ 5 seconds for typical workloads (≤ 50 services).
- **Reliability:** CI pipeline ≥ 99 % pass rate over 2 weeks.
- **User Satisfaction:** NPS ≥ 30 from beta cohort.

---

## 🌟 v1 – “Enterprise Orchestrator” (Target 2027‑03‑31)

| Theme | Key Features |
|-------|--------------|
| **Full‑Stack Execution** | • Real‑time orchestration engine (Kubernetes‑native operator).<br>• Support for AWS, Azure, GCP, and hybrid on‑prem.<br>• Rollback & drift‑detection mechanisms. |
| **Policy Engine** | • Central policy repository (OPA‑based).<br>• Automated compliance reporting (PCI, SOC2, ISO27001). |
| **Advanced Governance** | • Role‑based access with fine‑grained permissions (resource‑level).<br>• Audit trail stored immutable in append‑only log. |
| **Multi‑Cloud Connectors** | • Native providers for Terraform Cloud, Pulumi, and CloudFormation.<br>• Connector SDK for third‑party tools. |
| **Reporting & Dashboards** | • KPI dashboards (cost, performance, compliance).<br>• Export to PDF/CSV and Slack/webhook alerts. |
| **Extensibility** | • Plugin framework for custom objective‑to‑architecture rules.<br>• Marketplace API for internal/external pattern sharing. |
| **Scalability & HA** | • Horizontal scaling of planning service (stateless, Redis cache).<br>• Disaster‑recovery deployment scripts. |

### v1 Success Metrics
- **Adoption:** ≥ 3 enterprise pilots (≥ $250k ARR each) within 90 days of release.
- **Compliance:** 100 % of generated blueprints pass OPA policy suite.
- **Reliability:** 99.9 % uptime for orchestration engine over 30 days.

---

## 🚀 v2 – “Intelligent Optimizer & Marketplace” (Target 2027‑10‑31)

| Theme | Key Features |
|-------|--------------|
| **AI‑Driven Recommendations** | • Large‑language‑model (LLM) powered advisor that suggests architecture tweaks for cost, latency, and resiliency.<br>• Continuous learning loop feeding back execution outcomes into Axentx BRAIN. |
| **Closed‑Loop Cost Optimization** | • Real‑time spend monitoring → automated right‑sizing & reserved‑instance recommendations.<br>• Auto‑apply safe optimizations after user approval. |
| **Pattern Marketplace** | • Curated library of reusable migration patterns (e.g., “Lift‑and‑Shift”, “Data‑Lake Modernization”).<br>• Rating & review system; revenue‑share model for external contributors. |
| **Cross‑Org Collaboration** | • Shared workspaces, versioned plans, and comment threads.<br>• Integration with Axentx’s internal chat (SGLang) for async discussions. |
| **Advanced Analytics** | • Predictive ROI modeling using historic execution data.<br>• Exportable notebooks (Jupyter) for custom analysis. |
| **Security Automation** | • Auto‑remediation of misconfigurations detected by integrated CSPM tools.<br>• Continuous compliance drift detection. |

### v2 Success Metrics
- **Optimization Impact:** Average cost reduction ≥ 25 % vs. baseline after 30 days of auto‑optimizations.
- **Marketplace Revenue:** ≥ $100k ARR from third‑party pattern sales within 6 months.
- **AI Accuracy:** Recommendation acceptance rate ≥ 70 % in beta trials.

---

## 📦 Release Process & Governance

1. **Sprint Planning** – 2‑week sprints, backlog prioritized by ROI and MVP‑critical flags.  
2. **Feature Freeze** – 1 week before each milestone; only bug fixes & documentation allowed.  
3. **Release Candidate (RC) Validation** – Internal QA + security audit; sign‑off by PM & Lead Architect.  
4. **Beta Rollout** – Staged rollout to selected customers (5 % → 25 % → 100 %).  
5. **Post‑Launch Review** – Metrics collection, retrospective, and backlog adjustment.

---

## 📚 Supporting Documentation

- **Architecture Decision Records (ADRs)** – `docs/adr/` (linking to chosen frameworks: vLLM for LLM inference, SGLang for structured generation).  
- **API Spec** – OpenAPI 3.1 (`api/openapi.yaml`).  
- **CI/CD Pipelines** – `.github/workflows/` (Terraform validation, security scans, unit/integration tests).  
- **Data Sources** – Pricing datasets, compliance rule sets, and execution telemetry stored in Axentx BRAIN (pgvector).  

---

*Prepared by the Cloud‑Nexus Product & Engineering Lead, 2026‑06‑18.*
