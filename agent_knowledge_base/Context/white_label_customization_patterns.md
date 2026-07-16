# White-Label Customization Patterns

## Coastal Alpine Tech: Industry-Agnostic Agentic Architecture

**Date:** 23 May 2026

This document provides actionable patterns for adapting the Platinum Standard agentic architecture to any business vertical. The Mana Kai agricultural implementation demonstrates the core patterns; this guide shows how to replicate them for other industries without architectural changes.

---

## 1. Customization Framework

Every industry deployment follows this customization matrix:

| Layer | Mana Kai Example | Customization Point | Example: Plumbing |
|-------|------------------|---------------------|-------------------|
| **Data Ingestion** | Sensor readings (temp, humidity, light) | Define input schema and connectors | Service request forms, customer data, job history |
| **Domain Knowledge** | Microgreen growth stages, optimal conditions | `knowledge_sources`: PDFs, FAQs, standard procedures | Plumbing codes, service manuals, price lists, contractor profiles |
| **Agent Workflow** | Monitor → Analyze → Optimize → Alert | Agent sequencing and decision rules | Intake → Quote → Dispatch → Track → Invoice |
| **Escalation Rules** | Critical temp → automatic alert; mild → dashboard | `escalation_rules` JSONB config | Angry customer → human escalation; emergency plumbing → fast dispatch |
| **Brand Voice** | Professional, data-focused, action-oriented | `brand_voice` in `tenant_configs` | Friendly, local, reliability-focused |
| **User Interface** | Flutter dashboard for microgreen metrics | UI widgets and visualizations | Flutter dashboard for job tracking, technician updates, invoices |

The **architecture and agent core remain identical** across all industries. Only these five layers change.

---

## 2. Industry Adaptations (Detailed Examples)

### 2.1 Plumbing / Trades Services

**Business Problem:** Plumbing company needs to handle service requests, generate quotes, dispatch technicians, and manage callbacks.

**Customization:**

| Component | Configuration |
|-----------|----------------|
| **Tenant** | "Taranaki Plumbing Co" (industry: "Trades") |
| **Data Ingestion** | Web form submissions, phone transcripts, CRM data, technician location data |
| **Knowledge Sources** | Service manuals, plumbing codes, pricing guides, contractor profiles, common issues FAQ |
| **Agent Workflow** | IntakeAgent → classify (emergency, routine, quote) → FulfillmentAgent → dispatch to technician queue → ResolutionAgent for escalations |
| **Escalation Rules** | `{"emergency_response_time": 30min, "require_human_for": "customer_anger > 7", "auto_dispatch_threshold": "$200"}` |
| **Brand Voice** | "Local, reliable, no-nonsense. We show up on time or you get $50 off." |

**Agent Prompts (Examples):**
- **IntakeAgent:** "You are a helpful dispatcher for a local plumbing company. Assess the urgency of the request (emergency, routine, quote) and extract the address, contact info, and problem description."
- **FulfillmentAgent:** "You are a dispatcher. Based on the technician availability, current jobs, and travel time, assign this request to the best available technician. If no one is available within 2 hours, escalate."

**Data in `knowledge_embeddings`:**
- Plumbing code sections (searchable by problem type)
- Service pricing matrix (searchable by task)
- Common customer questions and responses
- Technician specialization profiles

---

### 2.2 Retail / E-Commerce

**Business Problem:** Clothing boutique needs customer support, inventory checking, order fulfillment, and feedback tracking.

**Customization:**

| Component | Configuration |
|-----------|----------------|
| **Tenant** | "The Button Box" (industry: "Retail") |
| **Data Ingestion** | Web chat, email, social media DMs, POS system data, inventory feed |
| **Knowledge Sources** | Product catalogs, return policies, shipping info, staff FAQ, sizing guides, brand story |
| **Agent Workflow** | IntakeAgent → classify (product question, order status, return, complaint) → FulfillmentAgent → check inventory, process returns, upsell → ResolutionAgent for customer issues |
| **Escalation Rules** | `{"max_refund_auto": 75, "require_human_for": "complaint_satisfaction < 3", "offer_discount_threshold": 50}` |
| **Brand Voice** | "Warm, quirky, fashion-forward. We love helping you find your perfect fit." |

**Agent Prompts (Examples):**
- **IntakeAgent:** "You are a friendly retail assistant. Determine if the customer is asking about product sizing, order status, returns, or something else. Be warm and conversational."
- **FulfillmentAgent:** "Check our inventory system and recommend alternatives if the requested item is out of stock. For returns, confirm eligibility and offer store credit or refund."

**Data in `knowledge_embeddings`:**
- Product descriptions and sizing info (searchable by style, size, color)
- Return policy sections (searchable by reason)
- FAQ on shipping and delivery
- Customer testimonials and styling tips

---

### 2.3 Manufacturing / Quality Control

**Business Problem:** Factory needs real-time monitoring, anomaly detection, quality assurance, and compliance logging.

**Customization:**

| Component | Configuration |
|-----------|----------------|
| **Tenant** | "Precision Widget Corp" (industry: "Manufacturing") |
| **Data Ingestion** | IoT sensors (temperature, pressure, vibration), inspection cameras, quality logs, worker time-tracking |
| **Knowledge Sources** | Manufacturing specs, quality standards, maintenance schedules, safety procedures, historical trend analysis |
| **Agent Workflow** | Data Ingestion Agent → real-time anomaly detection → Optimization Agent → adjust parameters → Alerting Agent → operator notification |
| **Escalation Rules** | `{"critical_deviation_threshold": 0.05, "maintenance_alert_interval": 30days, "require_human_for": "quality_fail_rate > 2%"}` |
| **Brand Voice** | "Data-driven, precise, safety-first. Every widget meets spec." |

**Agent Prompts (Examples):**
- **Data Ingestion Agent:** "Normalize sensor data from the production floor. Flag any reading that exceeds ±10% of target spec."
- **Optimization Agent:** "Based on current conditions and historical patterns, recommend adjustments to temperature, pressure, or line speed to maintain quality."

**Data in `knowledge_embeddings`:**
- Product specifications and tolerance ranges
- Maintenance procedures and schedules
- Safety protocols and incident reports
- Historical defect analyses and root causes

---

### 2.4 Healthcare / Patient Intake

**Business Problem:** Medical clinic needs patient screening, appointment management, compliance tracking, and follow-up coordination.

**Customization:**

| Component | Configuration |
|-----------|----------------|
| **Tenant** | "Taranaki Health Clinic" (industry: "Healthcare") |
| **Data Ingestion** | Patient intake forms, appointment requests, insurance info, medical history (HIPAA-compliant, on-premise only) |
| **Knowledge Sources** | Clinic policies, appointment availability, treatment protocols, insurance requirements, patient education materials |
| **Agent Workflow** | IntakeAgent → collect patient info and reason for visit → FulfillmentAgent → schedule appointment, verify insurance → ResolutionAgent for follow-ups and referrals |
| **Escalation Rules** | `{"urgent_symptom_escalation": true, "require_human_for": "treatment_decision", "hipaa_audit_level": "strict"}` |
| **Brand Voice** | "Caring, professional, reassuring. Your health is our priority." |

**Agent Prompts (Examples):**
- **IntakeAgent:** "You are a clinic receptionist. Gather the patient's name, contact, reason for visit, and any urgent symptoms. Be empathetic and clear."
- **FulfillmentAgent:** "Check the appointment schedule and insurance requirements. Offer the next available slot that fits the urgency level."

**Data in `knowledge_embeddings`:**
- Clinic policies and procedures
- Appointment availability and scheduling rules
- Insurance plan details and requirements
- Patient education resources by condition
- Common questions and answers

---

## 3. Configuration Template for New Industries

To onboard a new industry, follow this template:

```json
{
  "tenant_id": "uuid",
  "company_name": "[Business Name]",
  "industry": "[Industry]",
  "subscription_tier": "Professional",
  "brand_voice": "[2-3 sentences describing tone and values]",
  "escalation_rules": {
    "max_auto_action": "[threshold]",
    "require_human_for": "[criteria]",
    "response_time_sla": "[duration]",
    "custom_rule_1": "[industry-specific]",
    "custom_rule_2": "[industry-specific]"
  },
  "active_channels": {
    "web_widget": true,
    "email": true,
    "sms": false,
    "api": true,
    "custom_channel": false
  },
  "custom_instructions": "[Any special handling, compliance notes, or business logic]",
  "agent_workflow": "[Agent sequence for this industry, e.g., 'IntakeAgent → QuoteAgent → DispatchAgent']",
  "knowledge_source_types": "[List of document types to ingest, e.g., 'PDF, Product Catalog, FAQ, Training Manuals']"
}
```

---

## 4. Common Customization Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| Treating the architecture as industry-specific | Remember: agents and infrastructure are generic. Customization lives in `tenant_configs` and prompts only. |
| Over-engineering the escalation rules | Start simple: define 1–2 clear thresholds. Add complexity only as use cases emerge. |
| Uploading unstructured knowledge sources | Chunk and label all ingested documents with metadata (topic, date, confidence). The vector DB only works if data is clean. |
| Hardcoding agent behavior for one industry | Use parameterized prompts and decision trees. Every agent should accept `tenant_id` and adapt dynamically. |
| Ignoring data residency requirements | Always verify: for regulated industries (healthcare, finance), all data stays on-premise. No cloud storage without explicit consent. |

---

## 5. Deployment Checklist for New Industry

- [ ] Define tenant record in PostgreSQL (`tenants` table)
- [ ] Create `tenant_configs` with industry-specific brand voice, escalation rules, channels
- [ ] Ingest knowledge sources into `knowledge_sources` table
- [ ] Chunk and embed all documents into `knowledge_embeddings` (vector DB)
- [ ] Write or adapt agent prompts for the industry workflow
- [ ] Set up industry-specific integrations (CRM, POS, ERP, webhooks)
- [ ] Build/customize Flutter dashboard for the industry's key metrics
- [ ] Test full agent workflow end-to-end
- [ ] Deploy to production (on-premise or private cloud per tenant requirements)
- [ ] Monitor interaction logs for drift or escalation trends

---

## 6. Next Steps

Each new industry deployment is a 1–2 week cycle:
1. **Week 1:** Gather requirements, build `tenant_configs`, ingest knowledge sources
2. **Week 2:** Test agent workflow, refine prompts, deploy to staging
3. **Go-Live:** Deploy to production with monitoring and escalation support

The architecture supports unlimited industry verticals without code changes.
