# TECH_SPEC.md
**Project:** cloud‑nexus  
**Owner:** AxentX – Cloud Transformation Platform  
**Status:** MVP (ready for internal beta)  
**Last Updated:** 2026‑06‑18  

---  

## 1. Overview  

cloud‑nexus is a SaaS platform that enables enterprises to **plan**, **model**, and **execute** cloud‑migration and transformation initiatives. It translates high‑level business objectives (e.g., cost reduction, latency improvement, compliance) into concrete technical road‑maps, resource‑level deployment plans, and automated execution pipelines.  

Key capabilities:  

| Capability | Description |
|------------|-------------|
| **Objective Capture** | UI/REST API for business stakeholders to define goals, KPIs, constraints, and timelines. |
| **Architecture Modeling** | Drag‑and‑drop topology editor backed by a graph model (services, data stores, networks). |
| **Gap Analysis** | Engine that compares target architecture against current on‑prem / cloud footprint, surfacing gaps, risks, and cost estimates. |
| **Road‑Map Generation** | Optimizer (mixed‑integer programming) produces phased migration plans respecting dependencies and budgets. |
| **Execution Orchestrator** | Declarative pipelines (Terraform, Pulumi, Ansible) triggered via CI/CD runners; status tracking & rollback. |
| **Observability Dashboard** | Real‑time KPI tracking, cost monitoring, and compliance reporting. |

---  

## 2. Architecture Overview  

```
+-------------------+        +-------------------+        +-------------------+
|   Front‑End (SPA) | <----> |   API Gateway     | <----> |   Auth Service    |
+-------------------+        +-------------------+        +-------------------+
                                 |
                                 v
                        +-------------------+
                        |   Core Services   |
                        |-------------------|
                        | • Objective Svc  |
                        | • Modeling Svc   |
                        | • Analysis Svc   |
                        | • Planner Svc    |
                        | • Orchestrator Svc|
                        +-------------------+
                                 |
                                 v
                        +-------------------+
                        |   Data Store(s)   |
                        |-------------------|
                        | • PostgreSQL      |
                        | • Neo4j (graph)   |
                        | • Redis (cache)   |
                        +-------------------+
                                 |
                                 v
                        +-------------------+
                        |   External Tools  |
                        |-------------------|
                        | • Terraform CLI   |
                        | • Pulumi SDK      |
                        | • Ansible Runner  |
                        +-------------------+
```

* **Front‑End** – React + TypeScript SPA, served via CDN.  
* **API Gateway** – FastAPI (Python) acting as edge router, request validation, rate limiting.  
* **Auth Service** – OAuth2 / OpenID Connect (Keycloak) with JWT issuance.  
* **Core Services** – Individual FastAPI micro‑services, containerised, communicating over HTTP/2 + gRPC for internal calls.  
* **Data Stores** –  
  * **PostgreSQL** – relational data (users, projects, audit logs).  
  * **Neo4j** – graph representation of current & target architectures, dependency graphs.  
  * **Redis** – short‑lived cache for analysis results and token revocation.  
* **External Tools** – Executed in isolated worker containers via Docker‑in‑Docker (DinD) or Kubernetes Jobs.  

All services are deployed in a **Kubernetes** cluster (v1.28) with Helm charts for reproducibility.

---  

## 3. Component Details  

### 3.1 Front‑End (ui)  

| Item | Tech | Reason |
|------|------|--------|
| Framework | React 18 + Vite | Fast dev, HMR, small bundle |
| State Mgmt | Redux Toolkit + RTK Query | Centralised cache, auto‑refetch |
| UI Library | MUI v6 | Enterprise‑grade components |
| Auth | OIDC client (oidc‑client) | Seamless SSO with Keycloak |
| Diagramming | React‑Flow + Dagre | Interactive topology editor |

### 3.2 API Gateway  

* **Framework:** FastAPI (Python 3.11)  
* **Features:**  
  * OpenAPI schema generation (auto‑docs).  
  * Request validation via Pydantic models.  
  * Rate limiting (Redis‑backed token bucket).  
  * Centralised exception handling & logging (structlog).  

### 3.3 Core Services  

| Service | Responsibility | Main Endpoints | Key Libraries |
|---------|----------------|----------------|---------------|
| **ObjectiveSvc** | CRUD of business objectives, KPI mapping | `POST /objectives`, `GET /objectives/{id}` | Pydantic, SQLModel |
| **ModelingSvc** | Store & query architecture graphs | `POST /graphs`, `GET /graphs/{id}` | Neo4j driver, py2neo |
| **AnalysisSvc** | Gap analysis, cost estimation | `POST /analysis/run` | pandas, numpy, scikit‑learn (cost models) |
| **PlannerSvc** | Phase‑wise migration optimizer | `POST /plan/generate` | PuLP (MILP), networkx |
| **OrchestratorSvc** | Trigger IaC pipelines, monitor status | `POST /exec/run`, `GET /exec/{id}` | python‑terraform, pulumi‑sdk, ansible‑runner, Celery (task queue) |

All services expose **OpenAPI v3** specs and share a common **Auth middleware** that validates JWTs and injects `user_id` into request context.

### 3.4 Data Model  

#### 3.4.1 Relational (PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY,
    owner_id UUID REFERENCES users(id),
    name TEXT NOT NULL,
    status TEXT CHECK (status IN ('draft','analysis','planned','executing','completed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE objectives (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    title TEXT NOT NULL,
    description TEXT,
    kpi JSONB,               -- { "type": "cost", "target": 0.8 }
    deadline DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

#### 3.4.2 Graph (Neo4j)

* **Node Labels:** `Component`, `Service`, `Database`, `Network`, `CloudProvider`
* **Relationship Types:** `DEPENDS_ON`, `HOSTED_ON`, `CONNECTS_TO`, `MIGRATES_TO`
* Example Cypher to retrieve migration path:

```cypher
MATCH p=shortestPath(
    (c:Component {id: $source})-[:DEPENDS_ON*]->(t:Component {id: $target})
)
RETURN p
```

### 3.5 Execution Workers  

* **Container Runtime:** Docker (v26) inside Kubernetes pods.  
* **Isolation:** Each execution runs in a **dedicated namespace** with limited IAM role (least‑privilege).  
* **Artifacts:** Terraform state stored in encrypted S3 bucket; Pulumi stacks in GCS; Ansible logs in Elasticsearch.  

---  

## 4. Key APIs / Interfaces  

### 4.1 Public REST (JSON)  

All endpoints are versioned under `/api/v1/`. Example snippets:

```http
POST /api/v1/projects
Authorization: Bearer <jwt>
Content-Type: application/json

{
  "name": "Acme Cloud Migration",
  "owner_id": "c1a2b3..."
}
```

Response:

```json
{
  "id": "d4e5f6...",
  "name": "Acme Cloud Migration",
  "status": "draft",
  "created_at": "2026-06-18T12:34:56Z"
}
```

### 4.2 gRPC (internal)  

* **Service:** `Planner`
* **Method:** `GeneratePlan(PlanRequest) returns (PlanResponse)`
* **Proto (excerpt):**

```proto
syntax = "proto3";

package cloudnexus.planner;

message PlanRequest {
  string project_id = 1;
  repeated string objective_ids = 2;
  double budget_usd = 3;
  google.protobuf.Timestamp deadline = 4;
}

message Phase {
  int32 order = 1;
  repeated string actions = 2; // e.g., "terraform apply -target=module.vpc"
}

message PlanResponse {
  string plan_id = 1;
  repeated Phase phases = 2;
  double estimated_cost_usd = 3;
}
```

### 4.3 Event Bus  

* **Broker:** NATS JetStream (v2.10)  
* Topics:  
  * `project.created` → triggers initial analysis.  
  * `plan.generated` → notifies Orchestrator.  
  * `execution.status` → UI real‑time updates.  

---  

## 5. Technology Stack  

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Front‑End | React, Vite, MUI | 18, 5.2, 6.0 | Modern SPA, fast builds |
| API Gateway / Services | FastAPI + Uvicorn | 0.115, 0.24 | High performance, async, auto‑docs |
| Auth | Keycloak | 24.0.5 | Enterprise OIDC, LDAP integration |
| DB (relational) | PostgreSQL | 15 | ACID, JSONB, mature |
| DB (graph) | Neo4j | 5.15 | Native graph queries |
| Cache | Redis | 7.2 | Rate‑limit, short‑term cache |
| Task Queue | Celery + RabbitMQ | 5.3, 3.12 | Reliable background jobs |
| IaC Execution | Terraform CLI, Pulumi SDK, Ansible Runner | 1.9, 3.112, 2.12 | Multi‑cloud support |
| Orchestration | Kubernetes | 1.28 | Scalability, isolation |
| CI/CD | GitHub Actions + Argo CD | – | Automated builds & GitOps |
| Monitoring | Prometheus + Grafana | 2.53, 10.4 | Metrics, alerts |
| Logging | Loki + Fluent Bit | 3.2, 2.1 | Centralised log aggregation |
| Messaging | NATS JetStream | 2.10 | Low‑latency events |
| Packaging | Docker, Helm | 27, 3.14 | Reproducible deployments |

---  

## 6. Dependencies  

| Dependency | License | Source |
|------------|---------|--------|
| FastAPI | MIT | PyPI |
| Uvicorn | BSD-3 | PyPI |
| Pydantic | MIT | PyPI |
| SQLModel | Apache‑2.0 | PyPI |
| Neo4j Python Driver | Apache‑2.0 | PyPI |
| PuLP (MILP) | MIT | PyPI |
| python‑terraform | MIT | PyPI |
| pulumi‑sdk | Apache‑2.0 | PyPI |
| ansible‑runner | Apache‑2.0 | PyPI |
| Redis‑py | MIT | PyPI |
| Celery | BSD-3 | PyPI |
| NATS‑Python | Apache‑2.0 | PyPI |
| React, MUI, React‑Flow | MIT | npm |
| Keycloak | Apache‑2.0 | GitHub |
| PostgreSQL, Neo4j, Redis, RabbitMQ, NATS | Various (open) | Official images |

All third‑party components are vetted for CVE compliance (weekly `dependabot` scans).

---  

## 7. Deployment Architecture  

### 7.1 Kubernetes Cluster  

| Namespace | Purpose |
|-----------|---------|
| `cloud-nexus-api` | API Gateway, Auth Service |
| `cloud-nexus-core` | All core micro‑services |
| `cloud-nexus-db` | PostgreSQL, Neo4j, Redis |
| `cloud-nexus-exec` | Execution workers (dynamic pods) |
| `cloud-nexus-monitor` | Prometheus, Grafana, Loki |

### 7.2 Helm Chart Structure  

```
cloud-nexus/
├─ charts/
│  ├─ api/
│  ├─ core/
│  ├─ db/
│  └─ exec/
├─ values.yaml
└─ Chart.yaml
```

* `values.yaml` contains environment‑specific overrides (cloud provider, domain, TLS certs).  

### 7.3 CI/CD Flow  

1. **Push** → GitHub Actions run unit, integration, and security tests.  
2. **Docker Build** → Multi‑arch images pushed to `registry.axentx.io/cloud-nexus`.  
3. **Argo CD** watches `helm/` directory; on new chart version it performs a **GitOps** rollout.  
4. Post‑deployment **smoke tests** (Postman collection) executed via GitHub Actions; failures block promotion.  

---  

## 8. Security & Compliance  

| Aspect | Implementation |
|--------|----------------|
| Authentication | OIDC (Keycloak) + MFA; JWT signed with RSA‑2048. |
| Authorization | RBAC per‑project; policies stored in PostgreSQL. |
| Data‑at‑Rest | PostgreSQL & Neo4j encrypted with AWS KMS‑managed keys; S3 bucket versioned & SSE‑KMS. |
| Data‑in‑Transit | TLS 1.3 everywhere (Ingress, internal service mesh via Istio). |
| Auditing | All mutating API calls logged to Elasticsearch with immutable index policy. |
| Pen‑Test | Quarterly external audit; automated OWASP ZAP scans in CI. |
| Compliance | GDPR‑ready (data‑subject export endpoint), SOC‑2 Type II controls built into runbooks. |

---  

## 9. Observability  

* **Metrics** – Prometheus scrapes `/metrics` from each FastAPI service (via `prometheus_fastapi_instrumentator`).  
* **Dashboards** – Grafana dashboards for:  
  * Project health (phase completion, cost burn‑rate).  
  * Execution latency & failure rates.  
  * Resource utilization of the Kubernetes cluster.  
* **Tracing** – OpenTelemetry (Jaeger) traces across HTTP/gRPC calls.  

---  

## 10. Scalability & Performance  

| Dimension | Target | Strategy |
|-----------|--------|----------|
| API Throughput | 5 k RPS (peak) | Horizontal pod autoscaling (CPU > 70 %) |
| Graph Queries | ≤ 200 ms for 10k‑node topology | Neo4j Enterprise clustering + query caching |
| Planner Optimizer | ≤ 30 s for ≤ 200 components | MILP warm‑start, parallel scenario evaluation |
| Execution Workers | 100 concurrent runs | Kubernetes Job queue with resource quotas |
| Storage | 10 TB of Terraform state | S3 tiered storage + lifecycle policies |

---  

## 11. Testing Strategy  

| Layer | Tool | Coverage Goal |
|-------|------|---------------|
| Unit | pytest, hypothesis | 85 % |
| Integration | testcontainers (Postgres, Neo4j), FastAPI TestClient | 80 % |
| End‑to‑End | Cypress (frontend), Postman/Newman (API) | 75 % |
| Load | k6 scripts (API, graph queries) | 5 k RPS sustained |
| Security | Bandit, OWASP ZAP, Trivy (container) | No critical findings |

All tests run in CI; failures block merge.

---  

## 12. Roadmap (Post‑MVP)

| Milestone | ETA | Description |
|-----------|-----|-------------|
| **Beta Release** | 2026‑07‑15 | Internal pilot with 2 enterprise customers; feedback loop for UI/UX. |
| **Multi‑Cloud Provider Plugins** | 2026‑09‑01 | Add native modules for Azure Resource Manager & GCP Deployment Manager. |
| **AI‑Assist Planner** | 2026‑11‑30 | Integrate `vLLM` inference to suggest migration patterns based on historical data. |
| **Self‑Service Marketplace** | 2027‑02‑15 | Allow users to publish reusable “blueprints” (IaC modules) within the platform. |
| **Compliance Automation** | 2027‑04‑01 | Auto‑generate SOC‑2 / ISO‑27001 evidence from execution logs. |

---  

## 13. Glossary  

| Term | Meaning |
|------|---------|
| **Objective** | Business‑level goal (cost, latency, compliance). |
| **Component** | Logical unit in architecture graph (service, DB, network). |
| **Phase** | Ordered set of IaC actions executed together. |
| **Plan** | Output of PlannerSvc – a sequenced migration roadmap. |
| **Execution** | Run of a Plan via OrchestratorSvc, materialising IaC changes. |

---  

*Prepared by:* Senior Product/Engineering Lead – AxentX Cloud‑Nexus Team*
