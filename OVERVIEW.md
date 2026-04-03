# CSA Roadmap Template Overview

## Purpose

This overview is intentionally generic so any user can map their own projects, cloud environment, and role goals to a practical architecture roadmap.

## Phase structure

| Phase | Weeks | Focus | Expected output |
|---|---|---|---|
| 0 | Pre-start | Skill gap analysis | Filled assessment + gap report + adjusted plan |
| 1 | 1-2 | Architecture foundations | Network, identity, and baseline IaC patterns |
| 2 | 3-4 | AI application architecture | RAG or AI app pattern + deployment readiness |
| 3 | 5-6 | Operations and platform tooling | Tooling, automation, and support workflows |
| 4 | 7-8 | Delivery and communication | Playbooks, demos, runbooks, stakeholder artifacts |
| 5 | 9-10 | Advanced engineering and design governance | Observability, event-driven patterns, ADRs |

## Generic milestone framework

Each week should contain:

- Objective
- Deliverable
- Validation criteria
- Evidence links
- Status

## Project slot model

Use these slots instead of fixed project names:

- Project A: Architecture and IaC
- Project B: AI application pattern
- Project C: Operations and support tooling
- Project D: Delivery-ready reference implementation

## Resource matrix usage

Track where each cloud resource appears across projects using `docs/RESOURCE_MATRIX_TEMPLATE.md`.

## Gap analysis

Before planning, identify which Azure CSA competency domains need the most work.

1. Fill `docs/SKILL_ASSESSMENT_TEMPLATE.md` with your current and target levels (1–5).
2. Run `python scripts/analyze_gaps.py` to generate a prioritized gap report.
3. Record your action plan in `docs/GAP_ANALYSIS_TEMPLATE.md`.
4. Use the top gaps to guide which weeks and project slots matter most for you.

## Audience paths

- Executives: `index.html` then `docs/EXECUTIVE_SUMMARY_TEMPLATE.md`
- Managers: `docs/PLAN_TEMPLATE.md` + week status files
- Engineers: `projects/INDEX.md` + week assignments
- New joiners: `docs/ONBOARDING_CHECKLIST.md`
- Engineers wanting diagnostic start: `docs/SKILL_ASSESSMENT_TEMPLATE.md` → `scripts/analyze_gaps.py`
