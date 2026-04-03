# Skill Assessment Template

Fill in your **Current** and **Target** level for each domain using the 1–5 scale below. Add evidence links from past project work where available. Then run the gap analysis script to generate your prioritized learning report.

```bash
python scripts/analyze_gaps.py
```

## Proficiency scale

| Level | Label | Description |
|:---:|---|---|
| 1 | Aware | Read about it; no hands-on experience |
| 2 | Familiar | Completed labs or tutorials; limited real usage |
| 3 | Proficient | Used on real projects; can work independently |
| 4 | Advanced | Go-to person; can architect solutions and mentor others |
| 5 | Expert | Deep specialist; contributes to patterns, standards, or publications |

## Instructions

1. Set **Current** honestly based on hands-on evidence from real projects.
2. Set **Target** based on your role requirements or certification goals. Use 3 as a minimum viable proficiency for most CSA work; 4–5 for your primary specialization domains.
3. Fill **Evidence** with links to GitHub repos, architecture docs, or artifacts that demonstrate your current level.
4. Run `python scripts/analyze_gaps.py` to generate a gap report mapped to template weeks and project slots.
5. Record your action plan in `docs/GAP_ANALYSIS_TEMPLATE.md`.

---

## Assessment table

> Replace the placeholder values in **Current** and **Target** columns with your actual levels (1–5).

### Architecture foundations

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure Networking | 1 | 5 | |
| Identity & Access Management | 1 | 5 | |
| Infrastructure as Code | 1 | 5 | |
| Azure Landing Zones | 1 | 5 | |
| Azure Policy & Compliance | 1 | 5 | |

### Security

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Network Security | 1 | 5 | |
| Application Security | 1 | 5 | |
| Microsoft Defender for Cloud | 1 | 5 | |

### Compute and application platforms

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure Kubernetes Service | 1 | 5 | |
| Azure Container Apps | 1 | 5 | |
| Azure Functions & Serverless | 1 | 5 | |
| Azure App Service | 1 | 5 | |

### Data and storage

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure Storage Services | 1 | 5 | |
| Azure SQL & Relational Databases | 1 | 5 | |
| Azure Cosmos DB | 1 | 5 | |
| Azure Fabric & Analytics | 1 | 5 | |

### Messaging and integration

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure Messaging & Integration | 1 | 5 | |
| Azure API Management | 1 | 5 | |

### AI and intelligence

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure AI Services | 1 | 5 | |
| Azure OpenAI & Generative AI | 1 | 5 | |
| Azure Machine Learning | 1 | 5 | |

### Operations and delivery

| Competency Domain | Current (1-5) | Target (1-5) | Evidence from past projects |
|---|:---:|:---:|---|
| Azure Monitor & Observability | 1 | 5 | |
| CI/CD & DevOps | 1 | 5 | |
| Cost Management & FinOps | 1 | 5 | |
| Architecture Design & Advisory | 1 | 5 | |

---

## Domain descriptions

### Architecture foundations

**Azure Networking** — VNets, subnets, NSGs, route tables, VNet peering, DNS zones, private endpoints, ExpressRoute, VPN Gateway, Azure Bastion, and hub-spoke topology design.

**Identity & Access Management** — Microsoft Entra ID, RBAC role assignments, managed identities (system-assigned and user-assigned), conditional access policies, Privileged Identity Management (PIM), and workload identity federation.

**Infrastructure as Code** — Bicep authoring, Terraform on Azure, ARM templates, Azure Developer CLI (azd), module design, parameter files, and deployment pipelines for infrastructure.

**Azure Landing Zones** — Enterprise-scale landing zones, management group hierarchy, subscription vending, policy-driven governance, platform vs. application landing zones, and Cloud Adoption Framework alignment.

**Azure Policy & Compliance** — Policy definitions and initiatives, compliance reporting, remediation tasks, Defender for Cloud regulatory compliance, and audit vs. deny effect strategies.

### Security

**Network Security** — Azure Firewall, DDoS Protection, Web Application Firewall, NSG flow logs, private endpoints for PaaS services, and zero-trust network design.

**Application Security** — Azure Key Vault for secrets and certificates, secret rotation, encryption at rest and in transit, managed identity for secretless access, and OWASP-aligned application hardening.

**Microsoft Defender for Cloud** — Security posture management, Secure Score, security recommendations, workload protections, threat detection alerts, and integration with SIEM.

### Compute and application platforms

**Azure Kubernetes Service** — Cluster design, node pool configuration, networking (Azure CNI, Overlay), pod identity, KEDA scaling, GitOps (Flux/ArgoCD), upgrades, and production-hardened AKS patterns.

**Azure Container Apps** — Microservices hosting, Dapr integration, KEDA-based scaling, ingress configurations, environment design, and event-driven container applications.

**Azure Functions & Serverless** — HTTP, timer, queue, event, and Durable Function triggers; bindings; Flex Consumption plan; cold start mitigation; and serverless-first architecture patterns.

**Azure App Service** — Web app hosting, deployment slots, autoscaling, App Service Environment (ASE), custom domains, TLS, and hybrid connectivity.

### Data and storage

**Azure Storage Services** — Blob storage, Azure Data Lake Storage Gen2, queues, file shares, Table storage, access tiers (hot/cool/archive), lifecycle management, and private endpoint access.

**Azure SQL & Relational Databases** — Azure SQL Database, Managed Instance, elastic pools, failover groups, geo-replication, Hyperscale, and SQL security posture.

**Azure Cosmos DB** — Partition key design, consistency level trade-offs, multi-model APIs (NoSQL, MongoDB, Cassandra, Gremlin, Table), global distribution, and integrated vector search.

**Azure Fabric & Analytics** — Microsoft Fabric (OneLake, Lakehouse, Warehouse), Azure Synapse Analytics, Azure Data Factory, Delta Lake, and medallion architecture patterns.

### Messaging and integration

**Azure Messaging & Integration** — Azure Service Bus (queues and topics), Event Grid (system and custom events), Event Hubs (streaming), Logic Apps, and event-driven architecture patterns.

**Azure API Management** — Policy authoring (inbound/outbound/backend), backends, developer portal, subscription management, rate limiting, AI gateway mode, and OpenAPI import.

### AI and intelligence

**Azure AI Services** — Azure AI Search (vector and hybrid search), Document Intelligence, Speech services, Language services, Vision, and applied AI solution design.

**Azure OpenAI & Generative AI** — GPT model deployment and usage, prompt engineering, embeddings, Retrieval-Augmented Generation (RAG), AI Foundry, responsible AI, and multi-agent orchestration.

**Azure Machine Learning** — Model training, experiment tracking, MLOps pipelines, managed online endpoints, feature store, and production ML deployment patterns.

### Operations and delivery

**Azure Monitor & Observability** — Metrics, log analytics, alerts, workbooks, Application Insights (distributed tracing, dependency tracking), Log Analytics KQL queries, and dashboards.

**CI/CD & DevOps** — GitHub Actions workflows, Azure DevOps pipelines, deployment automation, infrastructure-as-code pipelines, shift-left security scanning, and environment promotion strategies.

**Cost Management & FinOps** — Azure Cost Management budgets and alerts, cost advisor recommendations, reserved instances, savings plans, tagging strategy, and FinOps framework adoption.

**Architecture Design & Advisory** — Well-Architected Framework (WAF) pillar reviews, architecture decision records (ADRs), design pattern selection, customer advisory communication, and reference architecture delivery.

---

## After filling this template

Run the gap analysis:

```bash
python scripts/analyze_gaps.py
```

Then record your prioritized action plan in `docs/GAP_ANALYSIS_TEMPLATE.md` and use it to fill in the weekly milestone table in `docs/PLAN_TEMPLATE.md`.
