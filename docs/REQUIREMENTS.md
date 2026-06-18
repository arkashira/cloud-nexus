# REQUIREMENTS.md

## Document Overview
This document defines the functional and non‑functional requirements, constraints, and assumptions for **cloud‑nexus**, Axentx’s cloud transformation planning and execution platform. It serves as the definitive source of truth for the development team, QA, and stakeholders throughout the product lifecycle.

---

## 1. Functional Requirements (FR)

| ID | Description | Acceptance Criteria |
|----|-------------|----------------------|
| **FR‑1** | **User Authentication & Authorization** – Secure login using SSO (SAML/OIDC) and role‑based access control (RBAC). | • Users can sign‑in via corporate IdP.<br>• Roles: `Executive`, `Planner`, `Engineer`, `Auditor` with distinct permission sets.<br>• Unauthorized actions return HTTP 403. |
| **FR‑2** | **Business Objective Capture** – UI wizard to define high‑level business goals (e.g., cost reduction, latency, compliance). | • Wizard stores objectives in the `objectives` table.<br>• Each objective has a unique ID, description, KPI target, and priority. |
| **FR‑3** | **Technical Landscape Inventory** – Auto‑discovery of existing cloud resources (AWS, Azure, GCP) via APIs and import of CSV/JSON inventories. | • Supports AWS, Azure, GCP APIs (IAM, EC2/VM, S3/Blob, RDS/SQL, etc.).<br>• Imported inventory appears in the “Resources” view with status `Discovered`. |
| **FR‑4** | **Gap Analysis Engine** – Compare business objectives against current technical landscape and generate a list of gaps. | • Engine runs on demand or on schedule.<br>• Output includes gap ID, description, severity, and suggested remediation. |
| **FR‑5** | **Transformation Blueprint Builder** – Drag‑and‑drop canvas to design migration/modernisation plans (phases, tasks, dependencies). | • Blueprint saved as JSON.<br>• Tasks can be assigned to users and linked to cloud‑provider services. |
| **FR‑6** | **Execution Orchestrator** – Trigger and monitor automated execution of blueprint tasks using IaC (Terraform, Pulumi) and CI/CD pipelines. | • Orchestrator launches jobs, streams logs, and updates task status (`Pending`, `Running`, `Success`, `Failed`). |
| **FR‑7** | **Cost & Impact Simulation** – Run “what‑if” simulations to estimate cost, performance, and risk before execution. | • Simulation returns projected monthly cost, SLA impact, and risk score.<br>• Results can be exported as PDF/CSV. |
| **FR‑8** | **Audit Trail & Reporting** – Immutable log of all actions, changes, and execution outcomes; generate compliance reports. | • Logs stored in append‑only datastore (e.g., AWS QLDB or PostgreSQL with WAL).<br>• Reports exportable in PDF, HTML, and JSON. |
| **FR‑9** | **Collaboration & Commenting** – Inline comments on objectives, gaps, and tasks; notifications via email/Slack. | • Users can mention others (`@username`).<br>• Notification preferences configurable per user. |
| **FR‑10** | **API‑First Access** – Fully documented REST/GraphQL API for all platform features. | • OpenAPI spec versioned and published.<br>• API keys scoped to RBAC roles. |

---

## 2. Non‑Functional Requirements (NFR)

| ID | Category | Requirement |
|----|----------|-------------|
| **NFR‑1** | **Performance** | UI page load ≤ 2 s (3G) for dashboards; API latency ≤ 200 ms for read operations, ≤ 500 ms for write operations under 100 concurrent users. |
| **NFR‑2** | **Scalability** | Horizontal scaling to support up to 10 k concurrent users and 1 M managed resources; auto‑scale compute pods (K8s) based on CPU > 70 %. |
| **NFR‑3** | **Reliability** | 99.9 % uptime SLA; data replication across at least 2 AZs; graceful degradation of discovery services when provider APIs throttle. |
| **NFR‑4** | **Security** | • Data at rest encrypted with AES‑256.<br>• TLS 1.3 for all network traffic.<br>• OWASP Top 10 compliance.<br>• Role‑based API access enforced via JWTs signed with RSA‑4096. |
| **NFR‑5** | **Observability** | Centralized logging (ELK), metrics (Prometheus + Grafana), and tracing (OpenTelemetry) with alerts for error rate > 1 % or latency breaches. |
| **NFR‑6** | **Maintainability** | Codebase follows Axentx C‑Framework conventions; unit test coverage ≥ 80 %; CI pipeline runs lint, tests, and security scans on every PR. |
| **NFR‑7** | **Portability** | Deployable on Kubernetes (EKS, AKS, GKE) using Helm charts; support for on‑prem OpenShift clusters. |
| **NFR‑8** | **Data Governance** | Retention policy: audit logs retained 2 years, user data 5 years; GDPR‑compliant data export/delete endpoints. |
| **NFR‑9** | **Usability** | UI conforms to WCAG 2.1 AA; onboarding wizard completes in ≤ 10 minutes for a new tenant. |
| **NFR‑10** | **Compliance** | Must satisfy SOC 2 Type II and ISO 27001 controls for all production environments. |

---

## 3. Constraints

1. **Technology Stack** – Must use the verified Axentx C‑Frameworks: `vLLM` for any LLM‑driven recommendation features, `SGLang` for structured generation of transformation scripts.  
2. **Data Sources** – Only the licensed datasets listed in the company knowledge base may be used for training any internal ML models (e.g., cost‑prediction).  
3. **Deployment** – All services must be containerized (Docker) and orchestrated via Helm 3 on a Kubernetes 1.27+ cluster.  
4. **Budget** – Cloud‑nexus must operate within a maximum monthly infrastructure cost of **$12,000** for the MVP environment (including compute, storage, and third‑party SaaS).  
5. **Regulatory** – Must not store any raw cloud provider credentials; use temporary STS tokens with least‑privilege scopes.  

---

## 4. Assumptions

| ID | Assumption |
|----|------------|
| **A‑1** | Target customers already have at least one public cloud subscription (AWS, Azure, or GCP). |
| **A‑2** | Corporate IdPs support SAML 2.0 or OIDC for SSO integration. |
| **A‑3** | Users possess basic cloud knowledge; advanced training is out of scope for the MVP. |
| **A‑4** | The underlying Axentx BRAIN (pgvector) is available for similarity search and recommendation services. |
| **A‑5** | Third‑party IaC providers (Terraform, Pulumi) are pre‑installed in the execution environment. |
| **A‑6** | Network egress to cloud provider APIs is unrestricted for discovery and execution phases. |
| **A‑7** | The MVP will support English language only; multi‑language support is planned for v2. |

--- 

*Prepared by the Cloud‑Nexus Product & Engineering Lead, Axentx – 2026‑06‑18*
