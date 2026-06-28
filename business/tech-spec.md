`tech-spec.md` written to `/tmp/cloud-nexus/tech-spec.md`.

# cloud-nexus — Technical Specification (v1)

> Bridges business objectives → technical cloud execution. v1 is a **planning-and-tracking SaaS**, not an agent that mutates your cloud. Read-only cloud introspection + opinionated migration-wave planning. Write-actions deferred to v2 to keep blast radius (and liability) near zero.

## Stack

| Layer | Choice | Why (opinionated) |
|---|---|---|
| Language | **TypeScript 5.x** (strict) | One language across API + web; shared Zod schemas as single source of truth. |
| Backend | **Fastify 4** (Node 20 LTS) | ~2x Express throughput, JSON-schema validation, low cold-start. |
| Frontend | **Next.js 14 (App Router) + Tailwind + shadcn/ui** | SSR landing + dashboard in one deploy. |
| DB access | **Drizzle ORM** | Typed SQL, light runtime — beats Prisma on serverless cold start. |
| Async/jobs | **BullMQ** (Redis) | Cloud scans are 30s–5min; off the request path. |
| Auth | **Clerk** | Org/team + SSO; don't build auth. |

**Monorepo:** pnpm workspaces — `apps/web`, `apps/api`, `packages/contracts`, `packages/db`, `packages/worker`.

## Hosting (free-tier-first, $0/mo at launch)

| Concern | Platform | Free tier | Upgrade trigger |
|---|---|---|---|
| Web | **Vercel** Hobby | 100GB BW | >100GB → Pro $20 |
| API/worker | **Fly.io** | 3×256MB VMs | sustained CPU |
| Postgres | **Neon** | 0.5GB, scale-to-zero, branching | >0.5GB → $19 |
| Redis | **Upstash** | 10k cmd/day | job volume |
| Storage (exports) | **Cloudflare R2** | 10GB, zero egress | >10GB |
| Email | **Resend** | 3k/mo | onboarding volume |

First paid line item is almost always Neon storage.

## Data model (Postgres, multi-tenant via `org_id`)

`organizations` · `users` (role: owner/editor/viewer) · `cloud_connections` (mode: readonly_role/plan_upload, `external_id`, `assume_role_arn` — **no long-lived keys stored**) · `initiatives` (business_objective, target_kpi, target_date — the goal anchor) · `workloads` (current-state inventory + monthly_cost) · `migration_waves` (6 R's strategy, sequence) · `wave_items` (effort_points, risk, blocked_by) · `assessments` (well_architected/cis/cost, score, findings) · `audit_log`.

## API surface (`/v1`, Clerk JWT, org-scoped)

| Method | Path | Purpose |
|---|---|---|
| POST | `/connections` | Register connection; return IAM trust policy / upload URL. |
| POST | `/connections/:id/scan` | Enqueue read-only inventory + cost scan. |
| GET | `/connections/:id/scan/:jobId` | Poll scan status/result. |
| GET | `/workloads` | List discovered inventory. |
| POST | `/initiatives` | Create initiative (objective → KPI → date). |
| POST | `/initiatives/:id/plan` | Generate draft wave plan (LLM + 6R rules). |
| GET | `/initiatives/:id/waves` | Waves + items + dependency graph. |
| PATCH | `/wave-items/:id` | Update effort/risk/status/deps. |
| POST | `/assessments` | Run Well-Architected / cost / CIS assessment. |
| GET | `/initiatives/:id/export` | Board-ready PDF/CSV (signed R2 URL). |

## Security model

- **Zero stored cloud credentials.** AWS cross-account **read-only IAM role** + per-connection `ExternalId` (confused-deputy defense); `sts:AssumeRole` per scan, creds in-memory TTL ≤15min. GCP via Workload Identity Federation. Offline mode: upload `terraform plan -json`, no live access.
- **Auth:** Clerk JWT verified via JWKS; RBAC in a Fastify `preHandler`.
- **Secrets:** Doppler/host env; per-org secrets encrypted at rest (KMS envelope).
- **Isolation:** mandatory `org_id` predicate in one data layer; cross-org leak tests. RLS staged for v2.
- **Abuse:** Redis rate-limit 100 req/min/org; 1 concurrent scan/connection; full audit log on every mutation + assume-role.

## Observability

- **Logs:** `pino` JSON with `request_id`+`org_id` → Axiom.
- **Metrics:** `fastify-metrics` → Prometheus; SLIs: API p95, scan duration, scan failure rate, queue depth, assume-role errors → Grafana Cloud.
- **Traces:** OpenTelemetry (HTTP/pg/BullMQ) → Tempo/Honeycomb; full `scan` span API→worker→cloud SDK.
- **Errors:** Sentry, tagged to git SHA. **Activation event** tracked in PostHog: connect → scan → first plan generated.

## Build / CI

GitHub Actions: install (frozen lockfile) → typecheck → eslint → vitest (unit + Zod contract) → drizzle migrate on ephemeral **Neon branch per PR** → build. Gates: green CI + 1 review, 70% coverage floor on contracts/data layer. CD: Vercel auto-deploy web, Fly deploy api/worker; forward-only migrations gated by manual prod approval. Supply chain: Dependabot + `pnpm audit` + Gitleaks.

---
**v1 guardrail:** read-only introspection + planning only — no write/apply to customer clouds, no long-lived keys. Caps liability while shipping the validated value (objectives → sequenced, costed technical plan) before taking execution risk in v2.