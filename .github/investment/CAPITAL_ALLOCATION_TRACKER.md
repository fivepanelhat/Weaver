# Capital Allocation Tracking System

**Purpose:** Real-time visibility into all active project allocations, compliance status, remediation progress, and benefit-sharing outcomes  
**Frequency:** Daily dashboard updates, weekly reporting, quarterly strategic review  
**Authority:** CFO, CISO, Compliance Officer, Cultural Advisory Board

---

## Active Project Registry

**Template for tracking all funded projects:**

```yaml
Project ID: KAS-2026-001-DIAMOND-WEAVER-SOVEREIGN-CLOUD
  Tier: Diamond
  Status: ACTIVE
  Allocation Amount: $1,200,000
  Release Schedule:
    - Tranche 1 (approval): $300,000 (2026-07-15)
    - Tranche 2 (Day 30): $300,000 (conditional on ≥85% compliance)
    - Tranche 3 (Day 60): $300,000 (conditional on ≥90% compliance)
    - Tranche 4 (Day 90): $300,000 (conditional on Green status + CAB approval)
  
  Timeline:
    Approval Date: 2026-07-12
    Projected Completion: 2026-12-31 (24 weeks)
    Post-Deployment Support: 12 months minimum
  
  Compliance Status:
    Baseline Audit Score: 94/225 (83%) → YELLOW
    Target Score: 214/225 (95%) → GREEN
    Current Score: 102/225 (85%) → YELLOW (trending to Green)
    Green Projection: 2026-09-15 (8 weeks)
  
  Remediation Plan:
    Gap Areas:
      - Access control logging: 8 items (implement SIEM)
      - Backup/DR testing: 5 items (schedule monthly tests)
      - Encryption key rotation: 3 items (automate 90-day cycle)
    Owner: [CISO Name], [Email], [Phone]
    Deadline: 2026-09-15
    Status: In Progress (45% complete)
  
  OCAP® Verification:
    Ownership: ✓ Signed (iwi + organization co-ownership)
    Control: ✓ Threshold encryption (iwi master key + org operational key)
    Access: ✓ Audit logging designed (18-month immutable logs)
    Possession: ✓ Aotearoa-based infrastructure confirmed
    Verification Date: 2026-07-12
    Next Review: 2026-10-12 (quarterly)
  
  Cultural Controls:
    Cultural Advisory Board Status: ✓ Approved (2026-07-10)
    Data Use Agreement: ✓ Signed (2026-07-08)
    Community Benefit-Sharing: ✓ Documented (local FTE target: 5, training: 50)
    Iwi Leadership Representation: ✓ 2 seats on governance committee
  
  Financial Tracking:
    Budget: $1,200,000
    Spent YTD: $120,000 (Tranche 1 + vendor deposits)
    Committed: $180,000 (orders + contracts)
    Remaining: $900,000 (in escrow, released on milestones)
    Contingency: 10% ($120,000 reserve)
  
  Key Milestones:
    - [ ] Week 1-2: Governance charter signed
    - [ ] Week 3-4: Vendor procurement completed
    - [ ] Week 5-8: Infrastructure deployment (Tranche 2 release trigger)
    - [ ] Week 9-12: Security hardening + compliance work (Tranche 3 release trigger)
    - [ ] Week 13-16: Testing + audit preparation (Tranche 4 release trigger)
    - [ ] Week 17-20: External SOC 2 audit
    - [ ] Week 21-24: Post-audit remediation + go-live
  
  Risk Register:
    Risk 1: Skilled labor shortage (onshore engineers)
      Impact: HIGH (schedule slip 8 weeks)
      Mitigation: Pre-contracted vendors + staff training program
      Status: MANAGED
    
    Risk 2: Encryption key management complexity
      Impact: MEDIUM (compliance gap if not solved)
      Mitigation: HSM deployment + redundancy
      Status: ACTIVE (mitigating)
    
    Risk 3: Cultural Advisory Board veto (low probability)
      Impact: CRITICAL (project termination)
      Mitigation: Transparent governance + monthly CAB briefings
      Status: MANAGED (0 veto threats to date)
  
  Stakeholders:
    Project Sponsor: [CEO Name], [Email]
    Technical Lead: [CTO Name], [Email]
    Compliance Officer: [Officer Name], [Email]
    Cultural Advisor: [Advisor Name], [Email]
    Finance Manager: [Manager Name], [Email]
```

---

## Compliance Status Dashboard (Real-Time)

**Updated daily, accessible to HITL gate committee:**

```yaml
KOTAHITANGA PORTFOLIO SUMMARY (2026-07-12):

Total Active Projects: 8
  - Diamond Tier: 2 projects ($2.5M allocated)
  - Platinum Tier: 3 projects ($1.2M allocated)
  - Gold Tier: 3 projects ($0.6M allocated)
  Total Portfolio: $4.3M

Compliance Distribution:
  🟢 GREEN (≥90%): 3 projects
    - KAS-2026-001-DIAMOND-WEAVER (85% → trending Green)
    - KAS-2026-005-GOLD-MARKETPLACE (92%)
    - KAS-2026-007-PLATINUM-FARM-AI (88%)
  
  🟡 YELLOW (70–89%): 4 projects
    - KAS-2026-002-DIAMOND-CORE (76% → needs remediation)
    - KAS-2026-003-PLATINUM-STACK (81%)
    - KAS-2026-004-PLATINUM-HEALTH (78%)
    - KAS-2026-006-GOLD-SUPPLY-CHAIN (82%)
  
  🔴 RED (<70%): 1 project
    - KAS-2026-008-DIAMOND-AETHER (64%) → CAPITAL FREEZE

Capital Status:
  Total Allocated: $4.3M
  Released to Date: $1.2M (28%)
  Held in Escrow (Yellow/Red): $1.8M (42%)
  Frozen (Red tier): $0.4M (9%)
  Available for New Allocation: $0.9M (budget remaining)

Remediation Pipeline:
  Critical Gaps (next 7 days):
    - KAS-2026-008 AETHER: Immediate SIEM deployment required (security)
    - KAS-2026-002 CORE: Backup/DR testing plan due (compliance)
  
  Active Remediation (next 30 days):
    - 4 projects with active remediation plans
    - Cumulative effort: ~240 person-days
    - Current pace: On track for 80% Green by 2026-09-30

Cultural Advisory Board Status:
  Approvals Pending: 0
  Reviews in Progress: 2 (KAS-2026-004, KAS-2026-008)
  Approvals Issued: 6
  Vetoes Issued: 0

Investment Impact (Quarterly Reporting):
  Local Employment: 12 FTEs created YTD
  Training Programs: 45 community members (target: 200)
  Data Sovereignty Milestones: 60% achieved (target: 100% by Q4)
  Community Benefit-Sharing: $220K reinvested locally (target: $500K by year-end)
```

---

## Weekly Remediation Status Report

**Distributed Monday mornings to HITL committee:**

```yaml
Week of: 2026-07-08 to 2026-07-14

RED TIER PROJECTS (Require Daily Attention):

KAS-2026-008-DIAMOND-AETHER: 64% → CAPITAL FREEZE

  Compliance Gaps:
    - [ ] SIEM (Security Information Event Management) not deployed
      Impact: Cannot audit access logs (CC6 violation, auditor blocker)
      Remediation: Deploy Splunk (Week 1 of next sprint)
      Owner: [CISO], ETA: 2026-07-21
      Status: Procurement approved, vendor contacted (delivery 2 weeks)
    
    - [ ] API key rotation not automated
      Impact: Manual process error-prone (CC7 violation)
      Remediation: Implement HashiCorp Vault integration
      Owner: [CTO], ETA: 2026-07-28
      Status: Engineering spike underway
    
    - [ ] Backup restoration testing: 0/4 tests passed
      Impact: Cannot verify RTO/RPO (CC9 violation)
      Remediation: Conduct monthly restore drill
      Owner: [Ops Manager], ETA: 2026-07-19
      Status: Test environment prepared, drill scheduled
  
  Immediate Actions (This Week):
    - [ ] Board notification (escalation approved)
    - [ ] SIEM procurement order placed
    - [ ] Vault implementation sprint planning
    - [ ] Backup test drill scheduled
  
  Projection:
    Current: 64% (RED)
    After SIEM (Week 2): 72% (YELLOW)
    After Vault (Week 3): 78% (YELLOW)
    Target: 92% (GREEN) by 2026-08-30
  
  Risk Mitigation: If not at YELLOW by 2026-07-26, recommend project termination + capital reclamation ($400K).

YELLOW TIER PROJECTS (Monitor Closely):

KAS-2026-002-DIAMOND-CORE: 76% → Remediation on track

  Compliance Gaps Addressed This Week:
    ✓ Encryption key audit completed (2 of 3 gaps closed)
    ⏳ Physical access logging: waiting on data center installation (ETA: 2026-07-18)
  
  Remediation Progress:
    Week 1: 71% → Week 2: 74% → Week 3: 76%
    Pace: +2.5% per week
    On track for Green by 2026-08-20 (5 weeks remaining)
  
  Owner: [Compliance Officer], [Phone], Status: GREEN (trending up)

KAS-2026-003-PLATINUM-STACK: 81% → Remediation on track

  Compliance Gaps:
    3 of 5 gaps closed (access logging, monitoring, incident response)
    Remaining: Fairness monitoring (ML bias detection) + annual security audit scheduling
  
  Next Steps:
    - Deploy fairness monitoring tool (2 weeks)
    - Schedule external penetration test (1 week)
  
  Owner: [Data Officer], Status: YELLOW (improving)

KAS-2026-004-PLATINUM-HEALTH: 78% → Cultural review underway

  Status: Awaiting Cultural Advisory Board feedback on health data classification
  Cultural Review: Due 2026-07-21
  Compliance gaps: Contingent on CAB decision (may require additional controls)
  Owner: [Cultural Advisor], Status: PENDING (CAB decision)

GREEN TIER PROJECTS (Quarterly Review Only):

KAS-2026-001-DIAMOND-WEAVER: 85% → Trending to Green

  Excellent progress this week: 81% → 85% (+4%)
  3 of 4 major remediation items completed
  Final gap: Quarterly access review audit trail (administrative task, due 2026-07-20)
  Projection: GREEN by 2026-07-28 (next Tranche 2 release eligible)
  Owner: [Compliance Officer], Status: ON TRACK

KAS-2026-005-GOLD-MARKETPLACE: 92% → Stable

  Maintaining Green status
  Minor gap: Annual penetration test scheduling (non-critical)
  Next review: 2026-10-12 (quarterly audit)
  Status: STABLE

KAS-2026-007-PLATINUM-FARM-AI: 88% → Approaching Green

  Model fairness monitoring operational
  Autonomous decision approval rate: 91% (excellent)
  Community benefit-sharing: 15 FTEs created, 35 community members trained
  Projection: GREEN by 2026-08-20
  Status: ON TRACK

---

## Weekly Action Items

| Item | Owner | Due | Status | Notes |
|------|-------|-----|--------|-------|
| KAS-2026-008 SIEM deployment | CISO | 2026-07-21 | IN PROGRESS | Splunk procurement approved |
| KAS-2026-008 Board escalation | CEO | 2026-07-14 | PENDING | RED tier capital freeze notification |
| KAS-2026-002 Physical access logging | Ops | 2026-07-18 | SCHEDULED | Data center work order in progress |
| KAS-2026-004 CAB decision | Cultural Advisor | 2026-07-21 | IN REVIEW | Health data classification determination |
| KAS-2026-001 Access review audit | Compliance Officer | 2026-07-20 | IN PROGRESS | Final Green status trigger |
| KAS-2026-003 Fairness monitoring | Data Officer | 2026-07-28 | BACKLOG | Low priority, on track for deadline |

---

## Remediation Escrow Tracking

**Capital held pending remediation completion:**

| Project | Tier | Total Allocation | Released | Escrowed | Condition | Release Trigger |
|---------|------|-----------------|----------|----------|-----------|-----------------|
| KAS-2026-001 WEAVER | Diamond | $1,200K | $300K | $900K | Reach GREEN | 2026-07-28 (est.) |
| KAS-2026-002 CORE | Diamond | $900K | $180K | $720K | Reach GREEN | 2026-08-20 (est.) |
| KAS-2026-003 STACK | Platinum | $400K | $120K | $280K | Reach GREEN | 2026-08-30 (est.) |
| KAS-2026-004 HEALTH | Platinum | $300K | $0K | $300K | CAB decision + GREEN | 2026-08-15 (pending) |
| KAS-2026-008 AETHER | Diamond | $400K | $0K | $400K | Reach YELLOW+ | 2026-07-26 (CRITICAL) |
| **TOTAL ESCROWED** | — | **$4.3M** | **$1.2M** | **$2.8M** | — | — |

**Escrow Release Logic:**
- **GREEN projects:** Remaining tranches released on schedule (monthly)
- **YELLOW projects:** 50% of next tranche released on achievement of next milestone (50% held until GREEN)
- **RED projects:** ALL tranches frozen until YELLOW status achieved (minimum $50K emergency allocation for remediation only)

---

## Quarterly Board Report Template

**Presented to board + Cultural Advisory Board, 2026-10-12:**

```
KOTAHITANGA INVESTMENT STRATEGY — Q3 PERFORMANCE REPORT

Executive Summary:
  - Portfolio Status: 3 GREEN, 4 YELLOW, 1 RED
  - Compliance Trend: 82% average (up from 78% baseline)
  - Capital Deployed: $1.2M (28% of $4.3M total)
  - Remediation Progress: 60% of RED/YELLOW gaps closed
  - On Track: 5 of 8 projects trending to GREEN by 2026-09-30

Investment Impact:
  - Local employment created: 12 FTEs
  - Community training: 45 people (22.5% of 200-person target)
  - Data sovereignty milestones: 60% achieved
  - Community benefit-sharing: $220K (44% of $500K annual target)

Risk Summary:
  - 1 RED project (AETHER) under capital freeze
  - Mitigation: SIEM deployment in progress, on-time for 2026-07-26 deadline
  - Board decision required: If not at YELLOW by 2026-07-26, recommend termination + reclamation

Recommendations:
  1. Approve tranches 2–4 release for KAS-2026-001 (WEAVER) on 2026-07-28
  2. Monitor KAS-2026-008 (AETHER) weekly; escalate if not at YELLOW by 2026-07-26
  3. Authorize additional $500K for new Gold tier projects (budget available)
  4. Cultural Advisory Board: provide guidance on KAS-2026-004 (HEALTH) health data classification

Next Steps:
  - Monthly remediation reviews (starting 2026-08-12)
  - Quarterly board report (next: 2026-10-12)
  - Annual external audit (SOC 2 Type II, starting month 6)
```

---

## Automated Dashboard Integration

**Real-time metrics fed to organizational dashboard (updated daily):**

```yaml
Metrics to Track:
  - Compliance Score (by project + portfolio)
  - Remediation Progress (% gaps closed per week)
  - Capital Deployment Rate (% of allocated funds released)
  - Escrow Balance (amount held pending remediation)
  - Risk Incidents (unauthorized access, data breaches, compliance violations)
  - Community Benefit-Sharing (FTEs, training, ROI)
  - Audit Readiness (% of 225-point baseline met)

Alert Thresholds:
  - Compliance drops <70%: RED (immediate escalation to board)
  - Remediation stalls >2 weeks: YELLOW alert
  - Escrow exceeds $3M: Budget review flag
  - Community benefit-sharing <75% target: Replan required

Data Sources:
  - Jira: Remediation task tracking
  - GitHub: Code review + deployment logs
  - Splunk: Security/audit logs (for Diamond tier)
  - Custom Portal: Manual compliance reporting + benefit-sharing tracking
  - Cultural Advisory Board: Quarterly attestations
```

---

## Success Criteria (6-Month Review, 2026-12-31)

- ✓ 6+ projects at GREEN status (≥90% compliance)
- ✓ 0 RED projects (all remediated or terminated)
- ✓ $3.5M+ capital deployed (82%+ of allocated funds)
- ✓ 30+ FTEs employed (local benefit-sharing)
- ✓ 150+ community members trained
- ✓ Zero unauthorized access incidents
- ✓ 100% OCAP® verification compliance
- ✓ Cultural Advisory Board satisfaction (survey: ≥4/5 rating)
- ✓ External SOC 2 Type II audit on track (audit started, completion expected Q1 2027)
- ✓ Data sovereignty metrics: 80%+ of infrastructure under community control

---

**Version:** 1.0.0  
**Updated:** 2026-07-12  
**Next Update:** 2026-07-19 (weekly)  
**Owner:** CFO + Compliance Officer + Cultural Advisory Board Chair
