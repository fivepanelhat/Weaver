# Kotahitanga Investment Strategy — Sovereign AI Capital Allocation Framework

**Authority:** CAT Architectural Standards (Diamond/Platinum/Gold), Te Mana Raraunga (OCAP® Principles), NZ Privacy Act 2020  
**Effective Date:** 2026-07-12  
**Classification:** Diamond (primary) | Platinum (secondary) | Gold (tertiary)  
**HITL Gate:** ✓ Mandatory for all capital allocation decisions  
**Scope:** Weaver, Coastal-Alpine-Core, coastal-alpine-stack, Aether

---

## Executive Summary

Kotahitanga Investment Strategy operationalizes sovereign AI capital allocation for indigenous data infrastructure across Aotearoa New Zealand. This framework ensures:

1. **Capital allocation decisions** are made through OCAP®-verified processes (Ownership, Control, Access, Possession)
2. **All funded projects** meet 225-point compliance verification baseline (Privacy Act 2020 + SOC 2 + Te Mana Raraunga)
3. **Tier classification** (Diamond/Platinum/Gold) is assigned at allocation time, not post-hoc
4. **Remediation guardrails** enforce Green/Yellow/Red status with automatic capital freeze at Red threshold
5. **Cultural Advisory Board** has veto authority over all projects affecting Māori data or indigenous sovereignty
6. **Local benefit-sharing** is tracked + reported quarterly with investment impact on data sovereignty compliance

---

## Three-Tier Capital Model

### DIAMOND TIER — Onshore Bare-Metal Sovereignty Infrastructure

**Investment Profile:**
- Capital allocation: $500K–$2M per project
- Timeline: 12–18 months (long-term sovereignty build)
- Risk profile: Strategic (core infrastructure)
- Compliance requirement: ≥95% on 225-point audit checklist

**Core Characteristics:**
- Bare-metal infrastructure (no cloud dependency)
- Onshore compute (Aotearoa-based data centers only)
- Dual-key encryption (iwi holds master key)
- Enterprise-grade security (SOC 2 Type II audit-ready)
- Full audit trail (18-month immutable logs)
- Zero-trust architecture (VPC, WAF, KMS, MFA, RBAC)
- Production-ready from day one (IaC, Kubernetes, blue-green deployments)

**Funding Decision Gate:**
```yaml
HITL Requirement:
  1. Technology review: Board approval required
  2. Cultural review: Cultural Advisory Board sign-off
  3. Compliance review: Minimum 90% on 225-point baseline
  4. Sovereignty review: Te Mana Raraunga officer confirmation
  5. Financial approval: CFO + CISO joint sign-off

Approval Timeline: 14 calendar days (expedited) to 30 days (standard)
```

**Example Projects:**
- Regional health data sovereign cloud (hosted in Aotearoa, iwi-controlled encryption keys)
- Māori cultural database with dual-key access model
- Community agriculture monitoring infrastructure (field sensors + intelligence hub)

---

### PLATINUM TIER — Edge-Autonomous Intelligent Systems

**Investment Profile:**
- Capital allocation: $200K–$800K per project
- Timeline: 6–12 months (rapid deployment)
- Risk profile: Moderate (field-tested systems)
- Compliance requirement: ≥85% on 225-point audit checklist

**Core Characteristics:**
- Hybrid cloud-edge architecture (Raspberry Pi 5 16GB + Hailo-10H at field layer)
- NVIDIA DGX Spark GB10 intelligence hub (128GB UMA, local fine-tuning)
- Continuous improvement loop (capture → curate → LoRA/PEFT → evaluate → hot-swap)
- Predictive value creation (models improve from every transaction)
- Local data flywheel (Platinum as self-improving system)
- On-device processing (minimize data transmission, maximize privacy)
- Bias detection + fairness monitoring (continuous)

**Funding Decision Gate:**
```yaml
HITL Requirement:
  1. Data flywheel design: Platinum working group review
  2. Cultural review: Cultural Advisory Board notification (14-day comment period)
  3. Compliance review: Minimum 85% on 225-point baseline
  4. Autonomous systems review: Explainability + HITL safeguards documented
  5. Budget approval: CTO + Data Officer sign-off

Approval Timeline: 10 calendar days (expedited) to 20 days (standard)
```

**Example Projects:**
- Autonomous farm management system (field sensors → local ML models → farmer recommendations)
- Community health prediction engine (biometric sensors → risk scoring → kaitiaki intervention)
- Whānau financial wellness assistant (local data processing, no transmission to cloud)

---

### GOLD TIER — Commercial Workflow Optimization

**Investment Profile:**
- Capital allocation: $50K–$300K per project
- Timeline: 3–6 months (quick value delivery)
- Risk profile: Low (proven patterns)
- Compliance requirement: ≥80% on 225-point audit checklist

**Core Characteristics:**
- Linear workflow alignment (Gold standard: Discovery → Design → Development → Testing → Deployment)
- Commercial-off-the-shelf (COTS) + open-source stack (Next.js, Python, PostgreSQL, Redis)
- Process-first design (digital reflection of real-world workflow)
- Supply chain optimization (procurement, inventory, logistics workflows)
- Community marketplace or service delivery
- Clear data flows and lifecycle phases
- Audit-friendly (deterministic, repeatable processes)

**Funding Decision Gate:**
```yaml
HITL Requirement:
  1. Workflow mapping: Process owner approval
  2. Compliance review: Minimum 80% on 225-point baseline
  3. Community review: Stakeholder consultation (if affecting community operations)
  4. Budget approval: Director + Finance Officer sign-off

Approval Timeline: 7 calendar days (expedited) to 14 days (standard)
```

**Example Projects:**
- Indigenous supply chain transparency platform (farm-to-market tracking)
- Whakapapa (genealogy) management system with cultural stewardship
- Community event booking and resource allocation system

---

## OCAP® Verification System

Every capital allocation must verify OCAP® principles before funds are released:

### OWNERSHIP Verification
```yaml
Question: Who legally owns the data/system/outcomes?

Diamond Tier:
  - Iwi/hapū holds legal ownership of sensitive data
  - Organization holds operational ownership
  - Dual-ownership documented in Data Use Agreement
  - Ownership registry maintained + reviewed quarterly

Platinum Tier:
  - Community owns data generated by edge sensors
  - Organization manages infrastructure (federated model)
  - Benefit-sharing agreement signed before deployment

Gold Tier:
  - Clear ownership assignment (organization or community)
  - Third-party COTS vendors have no data ownership claims
  - Contractual clarity required in procurement

Verification Gate:
  - [ ] Ownership structure documented + legal review completed
  - [ ] Data Use Agreement signed (Diamond/Platinum only)
  - [ ] Ownership registry entry created
  - [ ] Cultural Advisory Board confirms alignment with Te Tiriti o Waitangi
```

### CONTROL Verification
```yaml
Question: Who controls data access, use, and deletion?

Diamond Tier:
  - Iwi holds master encryption key (Control P2)
  - Organization holds operational key (Control P1)
  - Threshold cryptography: requires both keys to decrypt
  - Quarterly access review (iwi + organization joint)
  - Veto authority: Cultural Advisory Board can restrict any access

Platinum Tier:
  - Community + organization joint control (with community override)
  - Edge nodes under community physical control
  - Cloud intelligence hub under organizational control
  - Weekly data use audit (community + org)

Gold Tier:
  - Organization controls day-to-day access via RBAC
  - Community has quarterly data governance review
  - Deletion authority: community can request deletion within 30 days
  - Sunset clause: data auto-deleted after 7 years (or community-specified period)

Verification Gate:
  - [ ] Access control matrix documented (who can access what data)
  - [ ] Encryption key distribution verified (hardware security module or equivalent)
  - [ ] Deletion procedures tested + working
  - [ ] Cultural Advisory Board confirms control structure
```

### ACCESS Verification
```yaml
Question: Who can access data, under what conditions, with what logging?

Diamond Tier:
  - All access logged (immutable, 18-month retention minimum)
  - Quarterly access audit: human review of all logs
  - MFA required for sensitive data access
  - Geofencing: access only from Aotearoa-based locations
  - Purpose limitation: can only access for stated purpose in DUA
  - Audit trail shows: who, what, when, why, outcome

Platinum Tier:
  - Field sensors: limited local access (edge processing only)
  - Cloud intelligence: API-based access with rate limiting
  - Weekly automated alerts if access patterns deviate from baseline
  - Community review: monthly access report

Gold Tier:
  - Standard RBAC: viewer/editor/admin roles
  - API key rotation: 90-day cycle
  - Audit logging: all API calls recorded
  - Community notification: annual access summary

Verification Gate:
  - [ ] Access control policy documented + enforced
  - [ ] Logging infrastructure deployed + tested
  - [ ] Quarterly audit completed with zero unauthorized access findings
  - [ ] Cultural Advisory Board reviews access patterns (diamond tier)
```

### POSSESSION Verification
```yaml
Question: Who physically possesses the data and infrastructure?

Diamond Tier:
  - All data in Aotearoa-based data centers (no international cloud)
  - Physical access controls: badge/CCTV/environmental monitoring
  - Backup media: encrypted + stored separately
  - Disaster recovery: tested quarterly, RTO ≤4 hours
  - Possession register: document all data copies + locations

Platinum Tier:
  - Edge nodes: physically located with community (Raspberry Pi on-site)
  - Intelligence hub: hosted in Aotearoa
  - Data replication: synchronized between edge + hub with encryption
  - Possession audit: monthly physical verification

Gold Tier:
  - Cloud infrastructure: Aotearoa-based (AWS/Azure regional)
  - Backup: encrypted, geographically diverse
  - Physical security: provider compliance verified (annual)
  - Possession tracking: documented in procurement contract

Verification Gate:
  - [ ] Infrastructure location confirmed (all in Aotearoa)
  - [ ] Data possession audit completed
  - [ ] Encryption key location documented (separate from data)
  - [ ] Cultural Advisory Board confirms no international dependencies
```

---

## Compliance Baseline Verification (225-Point Framework)

Every funded project must achieve minimum compliance threshold before capital release:

| Tier | Requirement | Verification |
|------|-------------|--------------|
| **DIAMOND** | ≥95% (214/225 items) | External SOC 2 auditor sign-off required |
| **PLATINUM** | ≥85% (191/225 items) | Internal audit + CISO review |
| **GOLD** | ≥80% (180/225 items) | Compliance Officer checklist + spot checks |

**225-Point Framework Coverage:**
- CC1 (Governance & Oversight): 15 items
- CC6 (Logical & Physical Access): 49 items
- CC7 (Change Management & Secrets): 38 items
- CC9 (Security & Backup): 42 items
- A (Availability): 22 items
- P (Privacy + NZ Privacy Act IPPs 1-11): 34 items
- Te Mana Raraunga (OCAP®): 11 items
- Architecture & Infrastructure: 9 items
- **TOTAL: 225 items**

**Verification Gate:**
```yaml
Pre-Funding Checklist:
  - [ ] Baseline audit completed (225-point checklist scored)
  - [ ] Compliance percentage calculated (Green/Yellow/Red status)
  - [ ] Remediation plan submitted (if <95% for Diamond)
  - [ ] Auditor (or Compliance Officer) sign-off obtained
  - [ ] Risk register reviewed (identify gaps)
  - [ ] Timeline for remediation documented (if Yellow/Red)
  - [ ] Capital freeze conditions documented (if Red)
```

---

## Remediation Guardrails System

### GREEN Status (≥90% Compliance)
```yaml
Criteria: 203+ items passing on 225-point checklist

Capital Release:
  - Full funding authorized
  - Immediate project commencement
  - Standard quarterly compliance reviews

Obligations:
  - Monthly internal compliance reviews
  - Quarterly audit checklist re-scoring
  - Annual external audit (Diamond tier)
  - Annual training + awareness program
```

### YELLOW Status (70–89% Compliance)
```yaml
Criteria: 158–202 items passing on 225-point checklist
Trigger: Significant compliance gaps in specific control areas

Capital Release:
  - 50% of initial funding released
  - Remaining 50% held in escrow (released on remediation)
  - Project commencement conditional on remediation timeline

Remediation Timeline:
  - 14 calendar days: submit detailed remediation plan
  - 30 calendar days: implement high-priority gaps
  - 60 calendar days: target full Green status

Obligations:
  - Weekly compliance status updates
  - Bi-weekly remediation progress meetings
  - Monthly re-scoring against 225-point checklist
  - Cultural Advisory Board bi-weekly review (if Māori data involved)
```

### RED Status (<70% Compliance)
```yaml
Criteria: <158 items passing on 225-point checklist
Trigger: Critical compliance failures, security exposure, or cultural sovereignty violations

Capital Release:
  - ZERO funding released (capital freeze)
  - Project commencement blocked until remediation complete
  - Infrastructure lockout: systems not operational until compliance gates pass

Remediation Timeline:
  - Immediate: escalation to board + Cultural Advisory Board
  - 7 calendar days: comprehensive remediation plan due
  - 30 calendar days: target Yellow status
  - 60 calendar days: target Green status
  - If not met by day 60: project termination + capital reclamation

Escalation:
  - Notify Privacy Commissioner (if data privacy exposure)
  - Engage external auditor (immediate compliance assessment)
  - Cultural Advisory Board veto authority (if Te Mana Raraunga violation)
  - Executive decision: remediate vs. terminate

Obligations:
  - Daily compliance status updates
  - Weekly executive steering committee meetings
  - Real-time remediation tracking dashboard
  - Cultural Advisory Board daily review (if cultural sovereignty at risk)
```

**Remediation Guardrails Automation:**
```yaml
Continuous Monitoring:
  - Daily automated 225-point scoring (subset: critical controls only)
  - Real-time alerts: if critical control fails
  - Weekly full re-scoring: compliance dashboard updated
  - Monthly historical tracking: Green/Yellow/Red trend analysis

Dashboard Metrics:
  - Current compliance % (overall + by control category)
  - Trend (improving/stable/declining)
  - Risk areas (lowest-scoring control categories)
  - Time to remediation (estimated based on effort)
  - Capital at risk (escrow amount in Yellow/Red)

Escalation Automation:
  - Yellow: Auto-notify Compliance Officer + CTO
  - Red: Auto-notify CEO + CFO + CISO + Cultural Advisory Board Chair
```

---

## Capital Allocation Decision Matrix

### Pre-Funding Phase

```yaml
Step 1: Project Definition (Week 1)
  Input: Project proposal + business case
  HITL Gates:
    - [ ] Technology steering committee review
    - [ ] Cultural review: Cultural Advisory Board consult
    - [ ] Compliance scoping: Which tier? (Diamond/Platinum/Gold)
    - [ ] Sovereignty scoping: Does it affect Māori data? (Yes → Diamond minimum)
  Output: Approved tier classification + compliance target

Step 2: OCAP® Verification (Week 2)
  Verification:
    - [ ] Ownership structure finalized (legal review)
    - [ ] Control mechanisms documented (encryption keys, access model)
    - [ ] Access logging designed (audit trail format)
    - [ ] Possession confirmed (data location, backup strategy)
  HITL Gate:
    - [ ] Cultural Advisory Board confirms OCAP® alignment
  Output: OCAP® verification checklist signed

Step 3: Compliance Baseline (Week 3)
  Assessment:
    - [ ] 225-point pre-audit completed (estimate baseline score)
    - [ ] Remediation plan developed (for gaps)
    - [ ] Timeline set (when Green status achievable)
    - [ ] Risk register reviewed (identify critical gaps)
  HITL Gate:
    - [ ] Compliance Officer + auditor sign-off
    - [ ] Cultural Advisory Board reviews cultural controls (if applicable)
  Output: Compliance baseline assessment + Green/Yellow/Red status

Step 4: Capital Approval (Week 4)
  Decision:
    - If GREEN (≥90%): Approve full funding
    - If YELLOW (70–89%): Approve 50% + 50% escrow (on remediation)
    - If RED (<70%): Capital freeze (remediate first)
  HITL Gates:
    - [ ] CFO approval (budget availability)
    - [ ] CISO approval (security posture)
    - [ ] Cultural Advisory Board final sign-off
  Output: Capital allocation approval + release schedule

Step 5: Project Charter (Week 4)
  Documentation:
    - [ ] Tier classification + compliance target
    - [ ] OCAP® verification attached
    - [ ] Remediation plan (if Yellow/Red)
    - [ ] Quarterly review schedule set
  Output: Project charter signed by all HITL stakeholders
```

### During Project Phase

```yaml
Quarterly Compliance Reviews:
  - [ ] 225-point checklist re-scored
  - [ ] Green/Yellow/Red status updated
  - [ ] Remediation progress assessed
  - [ ] Escalations identified + acted on
  - [ ] Cultural Advisory Board briefing (if Māori data)
  - [ ] Board-level compliance dashboard updated

Monthly Steering Committee:
  - Review compliance dashboard
  - Approve remediation plan adjustments
  - Address escalations
  - Forecast timeline to Green status

Real-Time Guardrails:
  - If drift to Yellow: Auto-notify Compliance Officer + CTO
  - If drop to Red: Auto-freeze remaining capital
  - If critical control fails: Auto-incident response (see Incident Playbook)
```

### Post-Project Phase (Ongoing)

```yaml
Sustainability Phase:
  - Annual compliance audit (external for Diamond tier)
  - Quarterly compliance reviews (all tiers)
  - Annual Cultural Advisory Board review (if Māori data)
  - Sunset review: Is project still delivering value? (recommend extension vs. decommission)
  - Data retention: Follow original DUA (7-year health data limit, etc.)

Decommissioning:
  - Data deletion verified (audited)
  - Infrastructure decomposed
  - Compliance archive maintained (7+ years for health data)
  - Final report: Impact on data sovereignty + community benefit-sharing
```

---

## Local Benefit-Sharing Tracking

Every project must demonstrate concrete local benefit and report quarterly:

### Diamond Tier (Sovereignty Infrastructure)
```yaml
Expected Outcomes:
  - Local employment: FTE created
  - Skills transfer: Technical training for community members
  - Data ownership: Māori/Hapū legal control
  - Revenue sharing: Percentage of outcomes reinvested locally
  - Capability building: Infrastructure asset owned locally (no vendor lock-in)

Quarterly Report:
  | Metric | Q1 | Q2 | Q3 | Q4 |
  |--------|----|----|----|----|
  | Local FTEs | — | 3 | 4 | 4 |
  | Community training (people) | — | 12 | 24 | 36 |
  | Data under community control | 100% | 100% | 100% | 100% |
  | Revenue reinvested locally | $50K | $75K | $100K | $125K |
  | Capability transfer (%) | 20% | 40% | 60% | 80% |

Annual Impact Summary:
  - Sovereignty capability: Demonstrated independence from external vendors
  - Community leadership: Iwi in decision-making roles (board, committees)
  - Data asset value: Estimated market value of locally-controlled data
  - Regional resilience: Infrastructure resilience (reduced dependency)
```

### Platinum Tier (Edge-Autonomous)
```yaml
Expected Outcomes:
  - Field autonomy: Community operates edge systems independently
  - Knowledge capture: Community decision-making logic codified + improvable
  - Continuous improvement: Monthly model improvements from local data
  - Predictive capability: System becomes smarter over time

Quarterly Report:
  | Metric | Q1 | Q2 | Q3 | Q4 |
  |--------|----|----|----|----|
  | Model accuracy improvement (%) | Baseline | 3% | 7% | 12% |
  | Edge system uptime (%) | 98% | 99.2% | 99.5% | 99.5% |
  | Community-generated insights | 10 | 25 | 45 | 68 |
  | Autonomous decisions (count) | 200 | 500 | 1200 | 2100 |
  | Manual overrides (%) | 15% | 12% | 8% | 5% |

Annual Impact Summary:
  - Autonomy level: Percentage of decisions made without human intervention
  - Learning velocity: Accuracy improvement per quarter
  - Value creation: Estimated cost savings + outcome improvements
  - Knowledge asset: Proprietary models owned + controlled locally
```

### Gold Tier (Commercial Workflows)
```yaml
Expected Outcomes:
  - Process efficiency: Reduced time/cost per transaction
  - Accessibility: More community members can participate
  - Market participation: Improved market access (supply chains, services)
  - Economic participation: Revenue growth for community

Quarterly Report:
  | Metric | Q1 | Q2 | Q3 | Q4 |
  |--------|----|----|----|----|
  | Process cycle time reduction (%) | Baseline | 20% | 35% | 45% |
  | User adoption (%) | 20% | 45% | 70% | 85% |
  | Revenue growth (%) | Baseline | 15% | 30% | 50% |
  | Cost per transaction reduction (%) | Baseline | 25% | 40% | 55% |

Annual Impact Summary:
  - Market competitiveness: Demonstrated efficiency gains vs. alternatives
  - Community wealth creation: Revenue generated + distributed
  - Process modernization: Digital transformation level
  - Ecosystem participation: Number of community participants + partners
```

---

## Tier-Specific Deployment Templates

### DIAMOND TIER Deployment Checklist

```yaml
Pre-Deployment (Week 1-4):
  Infrastructure:
    - [ ] Onshore data center identified + contract signed
    - [ ] Bare-metal server procurement (CPU/memory/storage specs)
    - [ ] Network design: VPC, subnets, routing tables
    - [ ] Encryption infrastructure: HSM or equivalent for key management
    - [ ] Backup infrastructure: Separate secure facility + replication
  
  Security & Compliance:
    - [ ] Zero-trust architecture documented
    - [ ] IAM: MFA, RBAC matrix, service account strategy
    - [ ] Network segmentation: DMZ, app tier, database tier, backup tier
    - [ ] TLS 1.3+ configuration on all endpoints
    - [ ] WAF rules: OWASP Top 10 coverage
    - [ ] DLP (Data Loss Prevention) configured
  
  Governance:
    - [ ] Incident response plan documented + tested
    - [ ] On-call rotation established (24/7 coverage)
    - [ ] Audit logging infrastructure deployed
    - [ ] Monitoring/alerting: SIEM deployed + baseline configured
    - [ ] Compliance monitoring dashboard built
  
  Cultural Controls:
    - [ ] Dual-key encryption: iwi key management strategy
    - [ ] Cultural Advisory Board veto authority documented
    - [ ] Data Use Agreement finalized + signed
    - [ ] Community benefit-sharing model approved
    - [ ] Iwi staff/representatives on governance committee

Deployment (Week 5-8):
  - [ ] Bare-metal servers provisioned (IaC/Terraform)
  - [ ] Kubernetes cluster established + hardened
  - [ ] PostgreSQL + Redis deployed (encrypted, replicated)
  - [ ] Monitoring stack (Prometheus/Grafana/ELK) operational
  - [ ] Backup system tested (restore from backup successful)
  - [ ] API endpoints deployed behind WAF
  - [ ] SSL/TLS certificates installed + valid
  - [ ] DLP policies active + tested
  - [ ] Incident response drills (2x minimum)

Post-Deployment (Week 9-12):
  - [ ] External SOC 2 audit scheduled (start month 6)
  - [ ] Penetration test completed (external)
  - [ ] Backup restoration test (monthly schedule set)
  - [ ] Team training: incident response, compliance, cultural protocols
  - [ ] Monthly compliance reviews started
  - [ ] Quarterly community hui (gathering) scheduled

Continuous Operation:
  - Monthly: Full backup restoration test
  - Monthly: Compliance checklist review
  - Quarterly: Access review + recertification
  - Quarterly: Penetration test (recommended)
  - Quarterly: Cultural Advisory Board meeting
  - 18-month: SOC 2 Type II audit completion

Success Criteria:
  - ✓ External SOC 2 Type II audit passed (auditor opinion: unqualified)
  - ✓ Zero critical compliance findings
  - ✓ Zero unauthorized access incidents
  - ✓ ≥95% uptime SLA achieved (99.5% monthly)
  - ✓ All backups restorable within 4-hour RTO
  - ✓ Cultural Advisory Board approval + ongoing partnership
  - ✓ Community benefit-sharing targets met
```

### PLATINUM TIER Deployment Checklist

```yaml
Pre-Deployment (Week 1-2):
  Edge Hardware:
    - [ ] Raspberry Pi 5 16GB units procured + imaging template prepared
    - [ ] Hailo-10H accelerators installed + drivers configured
    - [ ] Field deployment locations identified
    - [ ] Network connectivity: cellular/satellite backup available
    - [ ] Physical security: weatherproof enclosures, tamper detection
  
  Cloud Intelligence Hub:
    - [ ] NVIDIA DGX Spark GB10 environment (128GB UMA)
    - [ ] Kubernetes cluster for model serving
    - [ ] Data pipeline: edge sync → hub ingestion → model training
    - [ ] LoRA/PEFT infrastructure for fine-tuning
  
  Data Flywheel:
    - [ ] Data capture strategy (what metrics? frequency?)
    - [ ] Curation process (validate + label data)
    - [ ] Model training pipeline (auto-retraining schedule)
    - [ ] Evaluation framework (accuracy, fairness, drift detection)
    - [ ] Hot-swap mechanism (update edge models without downtime)
  
  Governance:
    - [ ] Explainability requirements (how to show why system recommended X?)
    - [ ] Fairness monitoring (bias detection + reporting)
    - [ ] Audit logging (all model decisions logged)
    - [ ] HITL override process (humans can override autonomous decisions)
    - [ ] Community review: explain how ML models benefit community

Deployment (Week 3-5):
  - [ ] Raspberry Pi edge nodes deployed at field locations
  - [ ] Connectivity validated (upload/download tests)
  - [ ] DGX Spark configured + operational
  - [ ] Initial models trained on curated data
  - [ ] Bi-directional sync: cloud ↔ edge (encrypted)
  - [ ] Monitoring: model accuracy, data quality, sync lag
  - [ ] HITL approval workflow (community reviews recommendations)

Post-Deployment (Week 6-8):
  - [ ] Continuous improvement cycle started (capture → curate → train → evaluate)
  - [ ] Monthly model improvement reports
  - [ ] Fairness audit: bias detection running
  - [ ] Community feedback incorporated
  - [ ] Autonomous decision approval rates tracked
  - [ ] Team training: model explainability, fairness concepts

Continuous Operation:
  - Weekly: Accuracy + fairness metrics reviewed
  - Monthly: Model improvement cycles completed
  - Monthly: Community insight extraction + documentation
  - Quarterly: Drift detection analysis
  - Quarterly: Cultural Advisory Board review (if cultural data)
  - 6-monthly: Local fine-tuning assessment (when to retrain?)

Success Criteria:
  - ✓ Model accuracy improving month-over-month (learning loop working)
  - ✓ Fairness metrics stable (no bias drift detected)
  - ✓ Edge uptime ≥99% monthly
  - ✓ Autonomous decisions reaching 90%+ community approval
  - ✓ Community generating valuable insights (monthly reports)
  - ✓ Community operates edge systems independently (with support)
  - ✓ Investment ROI: quantified value creation (cost savings, outcomes)
```

### GOLD TIER Deployment Checklist

```yaml
Pre-Deployment (Week 1):
  Stack:
    - [ ] Next.js frontend configured (WCAG 2.2 AA compliant)
    - [ ] Python backend with FastAPI (async, validated)
    - [ ] PostgreSQL database schema designed (normalized)
    - [ ] Redis caching layer (session, rate limiting)
    - [ ] Docker images built + security scanned
  
  Workflow:
    - [ ] Linear phase gates documented (Discovery → Design → Dev → Test → Deploy)
    - [ ] User acceptance testing plan
    - [ ] Rollback procedures documented
    - [ ] Monitoring/alerting configured
  
  Compliance:
    - [ ] Privacy policy published
    - [ ] Data retention policy configured (auto-deletion after period)
    - [ ] Access logging enabled
    - [ ] DPA with any third-party integrations signed

Deployment (Week 2-3):
  - [ ] AWS region selected (Aotearoa-based)
  - [ ] ECS/EKS deployed (container orchestration)
  - [ ] Database migrations applied
  - [ ] API endpoints tested (functional + load)
  - [ ] Frontend deployed (CDN + caching)
  - [ ] Domain + SSL certificates configured
  - [ ] Smoke tests passed (core workflows functional)

Post-Deployment (Week 4):
  - [ ] User training + onboarding started
  - [ ] Community feedback collection process
  - [ ] Monthly compliance checklist reviews
  - [ ] Support process documented + staffed

Continuous Operation:
  - Weekly: Uptime + performance metrics reviewed
  - Monthly: Compliance checklist + community feedback
  - Quarterly: Feature improvements (based on feedback)
  - 6-monthly: Security assessment (code review, dependency updates)

Success Criteria:
  - ✓ Workflow maps 1:1 to real-world process
  - ✓ User adoption ≥80%
  - ✓ Data retention auto-deletion working (verified monthly)
  - ✓ Zero compliance violations
  - ✓ Community report positive impact (survey/interview)
  - ✓ Sustainable operational cost (<$50K annual)
```

---

## HITL Gate Decision Authority Matrix

| Decision | Authority | Timeline | Veto |
|----------|-----------|----------|------|
| **Tier classification** | Board + CISO | 7 days | Cultural Advisory Board (if Māori data) |
| **Capital allocation (>$500K)** | CFO + CEO | 10 days | Cultural Advisory Board |
| **Capital allocation ($200K–$500K)** | CISO + CTO | 5 days | Cultural Advisory Board |
| **Remediation plan acceptance** | Compliance Officer + CISO | 3 days | N/A |
| **OCAP® verification** | Privacy Officer + Data Officer | 5 days | Cultural Advisory Board |
| **Māori data new use** | Cultural Advisory Board | 30 days | Mandatory veto authority |
| **Cultural data deletion** | Cultural Advisory Board | 7 days | Iwi leadership required |
| **Encryption key rotation** | CISO only | 1 day | N/A (ops decision) |
| **Emergency incident response** | Incident Commander | Real-time | N/A (post-action review) |

---

## Critical Success Metrics

Track these quarterly + report to board:

| Metric | Target | Green | Yellow | Red |
|--------|--------|-------|--------|-----|
| **Compliance Baseline** | 90%+ | ≥95% | 70–89% | <70% |
| **Uptime SLA** | 99.5% | ≥99.5% | 99.0–99.4% | <99% |
| **Audit Log Integrity** | 100% | 0 gaps | 1–2 gaps | >2 gaps |
| **DSAR Response Time** | ≤20 days | ≤10 days | 11–20 days | >20 days |
| **Unauthorized Access Events** | 0 | 0 | 1–2 | >2 |
| **Data Sovereignty Compliance** | 100% | All controls | 90–99% | <90% |
| **Community Benefit Realization** | Target+ | On-target | 80–99% target | <80% target |
| **Cultural Advisory Board Meetings** | Quarterly | 4+/yr | 2–3/yr | <2/yr |

---

## References & Integration

**CAT Architectural Standards Integration:**
- Primary: Diamond (sovereign governance + enterprise security)
- Secondary: Platinum (autonomous loops + continuous improvement)
- Tertiary: Gold (commercial workflows + supply chain)

**Compliance Framework Integration:**
- 225-Point Audit Checklist (nz-ai-compliance-soc2)
- Te Mana Raraunga Principles (OCAP® Framework)
- NZ Privacy Act 2020 (Information Privacy Principles 1-11)
- SOC 2 Type II Controls (Trust Services Criteria)
- MBIE Responsible AI Framework (explainability, fairness, HITL gates)

**Related Skills & Tools:**
- nz-ai-compliance-soc2 skill (master compliance framework)
- cat-architectural-standards skill (tier definitions + HITL gates)
- aether-core (autonomous intelligence layer)
- te-mana-raraunga-sovereignty (OCAP® implementation)

---

**Version:** 1.0.0  
**Date:** 2026-07-12  
**Authority:** Coastal Alpine Tech Board + Cultural Advisory Board  
**Next Review:** 2026-10-12 (quarterly compliance + outcomes assessment)
