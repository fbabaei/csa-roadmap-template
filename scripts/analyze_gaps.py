#!/usr/bin/env python3
"""
analyze_gaps.py — CSA Roadmap skill gap analyzer.

Reads:
  docs/SKILL_ASSESSMENT_TEMPLATE.md  — fill in Current / Target values first
  week-XX/STATUS.md                  — execution status per week

Outputs:
  Console report with prioritized gaps mapped to template phases, weeks, and
  project slots. Shows execution progress for weeks that address each gap.

Usage:
    python scripts/analyze_gaps.py
    python scripts/analyze_gaps.py --assessment path/to/custom_assessment.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Domain-to-week mapping
# Each domain maps to the template phase and weeks that primarily address it,
# and the project slot where evidence should be built.
# ---------------------------------------------------------------------------
DOMAIN_MAP: dict[str, dict] = {
    "Azure Networking": {
        "phase": 1,
        "weeks": [1, 2],
        "slot": "A",
        "focus": "VNets, subnets, NSGs, peering, DNS, private endpoints, routing",
    },
    "Identity & Access Management": {
        "phase": 1,
        "weeks": [1, 2],
        "slot": "A",
        "focus": "Entra ID, RBAC, managed identity, conditional access, PIM",
    },
    "Infrastructure as Code": {
        "phase": 1,
        "weeks": [1, 2],
        "slot": "A",
        "focus": "Bicep, Terraform, ARM, azd, module design",
    },
    "Azure Landing Zones": {
        "phase": 1,
        "weeks": [2],
        "slot": "A",
        "focus": "Enterprise-scale, management groups, governance hierarchy",
    },
    "Azure Policy & Compliance": {
        "phase": 1,
        "weeks": [2],
        "slot": "A",
        "focus": "Policy definitions, initiatives, compliance reporting, remediation",
    },
    "Network Security": {
        "phase": 5,
        "weeks": [9, 10],
        "slot": "A",
        "focus": "Azure Firewall, DDoS, WAF, NSGs, private endpoints, zero-trust network",
    },
    "Application Security": {
        "phase": 5,
        "weeks": [9, 10],
        "slot": "A",
        "focus": "Key Vault, secret rotation, encryption, certificate management",
    },
    "Microsoft Defender for Cloud": {
        "phase": 5,
        "weeks": [9],
        "slot": "C",
        "focus": "Security posture, Secure Score, recommendations, threat protection",
    },
    "Azure Kubernetes Service": {
        "phase": 5,
        "weeks": [9, 10],
        "slot": "A",
        "focus": "Cluster design, networking (CNI), scaling, GitOps, KEDA",
    },
    "Azure Container Apps": {
        "phase": 5,
        "weeks": [10],
        "slot": "B",
        "focus": "Microservices, Dapr, KEDA, ingress, environments",
    },
    "Azure Functions & Serverless": {
        "phase": 3,
        "weeks": [5, 6],
        "slot": "C",
        "focus": "Trigger types, bindings, Durable Functions, Flex Consumption",
    },
    "Azure App Service": {
        "phase": 3,
        "weeks": [5],
        "slot": "C",
        "focus": "Web apps, deployment slots, autoscale, App Service Environments",
    },
    "Azure Storage Services": {
        "phase": 5,
        "weeks": [9],
        "slot": "A",
        "focus": "Blob, ADLS Gen2, queues, file shares, access tiers, lifecycle",
    },
    "Azure SQL & Relational Databases": {
        "phase": 5,
        "weeks": [10],
        "slot": "D",
        "focus": "Azure SQL DB, managed instance, elastic pools, failover groups",
    },
    "Azure Cosmos DB": {
        "phase": 5,
        "weeks": [10],
        "slot": "D",
        "focus": "Partition design, consistency levels, APIs, global distribution",
    },
    "Azure Fabric & Analytics": {
        "phase": 5,
        "weeks": [10],
        "slot": "D",
        "focus": "Microsoft Fabric, Synapse, Data Factory, Lakehouse, Delta Lake",
    },
    "Azure Messaging & Integration": {
        "phase": 5,
        "weeks": [9, 10],
        "slot": "D",
        "focus": "Service Bus, Event Grid, Event Hubs, Logic Apps, event-driven patterns",
    },
    "Azure API Management": {
        "phase": 4,
        "weeks": [8],
        "slot": "D",
        "focus": "Policies, backends, developer portal, rate limiting, AI gateway",
    },
    "Azure AI Services": {
        "phase": 2,
        "weeks": [3, 4],
        "slot": "B",
        "focus": "AI Search, Document Intelligence, Speech, Vision, Language",
    },
    "Azure OpenAI & Generative AI": {
        "phase": 2,
        "weeks": [3, 4],
        "slot": "B",
        "focus": "GPT models, embeddings, RAG, AI Foundry, prompt engineering",
    },
    "Azure Machine Learning": {
        "phase": 2,
        "weeks": [4],
        "slot": "B",
        "focus": "Model training, MLOps, managed endpoints, feature store",
    },
    "Azure Monitor & Observability": {
        "phase": 3,
        "weeks": [5, 6],
        "slot": "C",
        "focus": "Metrics, logs, alerts, workbooks, App Insights, Log Analytics, KQL",
    },
    "CI/CD & DevOps": {
        "phase": 3,
        "weeks": [5, 6],
        "slot": "C",
        "focus": "GitHub Actions, Azure DevOps, deployment automation, shift-left security",
    },
    "Cost Management & FinOps": {
        "phase": 3,
        "weeks": [6],
        "slot": "C",
        "focus": "Budgets, Cost Advisor, reservations, tagging strategy, FinOps framework",
    },
    "Architecture Design & Advisory": {
        "phase": 4,
        "weeks": [7, 8],
        "slot": "D",
        "focus": "WAF pillars, design patterns, ADRs, customer communication, design reviews",
    },
}

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

_SKIP_PREFIXES = frozenset({"domain", "competency", "---", ":---", "level", "|-"})


def parse_assessment(filepath: Path) -> list[dict]:
    """Parse the filled assessment table. Returns a list of domain rating dicts."""
    if not filepath.exists():
        print(f"ERROR: Assessment file not found:\n  {filepath}")
        print("\nFill in docs/SKILL_ASSESSMENT_TEMPLATE.md with your Current and Target")
        print("values (1-5), then run this script again.")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")

    # Match markdown table rows: | domain name | N | N | optional evidence |
    row_pattern = re.compile(
        r"^\|\s*([^|]{3,}?)\s*\|\s*([1-5])\s*\|\s*([1-5])\s*\|\s*([^|]*?)\s*\|",
        re.MULTILINE,
    )

    results = []
    for match in row_pattern.finditer(text):
        domain = match.group(1).strip()
        if any(domain.lower().startswith(p) for p in _SKIP_PREFIXES):
            continue
        current = int(match.group(2))
        target = int(match.group(3))
        evidence = match.group(4).strip()
        results.append(
            {
                "domain": domain,
                "current": current,
                "target": target,
                "gap": max(0, target - current),
                "evidence": evidence,
            }
        )
    return results


def parse_week_statuses() -> dict[int, str]:
    """Read STATUS.md from each week folder. Returns {week_num: status_string}."""
    statuses: dict[int, str] = {}
    for n in range(1, 11):
        folder = ROOT / f"week-{n:02d}"
        status_file = folder / "STATUS.md"
        status = "Not Started"
        if status_file.exists():
            text = status_file.read_text(encoding="utf-8").lower()
            if "completed" in text:
                status = "Completed"
            elif "in progress" in text:
                status = "In Progress"
            elif "blocked" in text:
                status = "Blocked"
        statuses[n] = status
    return statuses


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

_SEP = "=" * 72
_DIV = "-" * 72


def _bar(gap: int, max_val: int = 5) -> str:
    filled = min(gap, max_val)
    return "█" * filled + "░" * (max_val - filled)


def generate_report(assessments: list[dict], week_statuses: dict[int, str]) -> None:
    print(f"\n{_SEP}")
    print("  CSA ROADMAP — SKILL GAP ANALYSIS REPORT")
    print(_SEP)

    # Detect unfilled template: warn if every domain is still at default 1 → 5
    if assessments and all(d["current"] == 1 and d["target"] == 5 for d in assessments):
        print()
        print("  WARNING: All domains show the default placeholder values (1 → 5).")
        print("  Open docs/SKILL_ASSESSMENT_TEMPLATE.md, fill in your actual Current")
        print("  and Target levels, then run this script again.")
        print(f"\n{_SEP}\n")
        return

    gaps = sorted(
        [d for d in assessments if d["gap"] > 0],
        key=lambda d: (-d["gap"], -d["current"]),
    )
    covered = [d for d in assessments if d["gap"] == 0]
    unmapped = [d for d in assessments if d["domain"] not in DOMAIN_MAP]

    print(f"\n  Domains assessed :  {len(assessments)}")
    print(f"  Gaps identified  :  {len(gaps)}")
    print(f"  At target level  :  {len(covered)}")
    if unmapped:
        print(f"  Unmapped domains :  {len(unmapped)}  (custom entries — no week assignment)")

    if not gaps:
        print("\n  No gaps found. All domains are at or above target level.")
        print(f"\n{_SEP}\n")
        return

    # --- Prioritized gap list ---
    print(f"\n{_DIV}")
    print("  PRIORITIZED GAPS  (largest gap first)")
    print(_DIV)

    for i, d in enumerate(gaps, 1):
        mapping = DOMAIN_MAP.get(d["domain"], {})
        weeks: list[int] = mapping.get("weeks", [])
        phase = mapping.get("phase", "?")
        slot = mapping.get("slot", "?")
        focus: str = mapping.get("focus", "")

        week_labels = ", ".join(f"Week {w}" for w in weeks) if weeks else "no week mapping"

        progress_parts = []
        for w in weeks:
            st = week_statuses.get(w, "Unknown")
            marker = "✓" if st == "Completed" else ("→" if st == "In Progress" else "○")
            progress_parts.append(f"{marker} Week {w}: {st}")

        print(f"\n  #{i:02d}  {d['domain']}")
        print(f"       Gap :  {_bar(d['gap'])}  "
              f"({d['current']}/5 → {d['target']}/5, Δ = {d['gap']})")
        if focus:
            print(f"       Covers : {focus}")
        if weeks:
            print(f"       Roadmap: Phase {phase}  |  {week_labels}  |  Project Slot {slot}")
        if progress_parts:
            print(f"       Status : {' · '.join(progress_parts)}")
        if d["evidence"]:
            print(f"       Evidence already: {d['evidence']}")
        elif not d["evidence"]:
            print(f"       Evidence: none recorded — add links in SKILL_ASSESSMENT_TEMPLATE.md")

    # --- Domains at target ---
    if covered:
        print(f"\n{_DIV}")
        print("  AT OR ABOVE TARGET LEVEL")
        print(_DIV)
        for d in covered:
            marker = "✓" if d["current"] >= d["target"] else "~"
            print(f"  {marker}  {d['domain']:<45} {d['current']}/5 (target {d['target']}/5)")

    # --- Week execution snapshot ---
    print(f"\n{_DIV}")
    print("  WEEK EXECUTION SNAPSHOT")
    print(_DIV)
    for n in range(1, 11):
        st = week_statuses.get(n, "Not Started")
        marker = "✓" if st == "Completed" else ("→" if st == "In Progress" else ("!" if st == "Blocked" else "○"))
        print(f"  {marker}  Week {n:02d}: {st}")

    # --- Next step ---
    print(f"\n{_SEP}")
    print("  Next steps:")
    print("    1. Record your action plan in docs/GAP_ANALYSIS_TEMPLATE.md")
    print("    2. Use your top gaps to fill the weekly objectives in docs/PLAN_TEMPLATE.md")
    print("    3. Re-run this script after each phase to track progress")
    print(_SEP + "\n")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _parse_args() -> Path:
    assessment_path = ROOT / "docs" / "SKILL_ASSESSMENT_TEMPLATE.md"
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--assessment" and i + 1 < len(args):
            assessment_path = Path(args[i + 1])
            break
    return assessment_path


def main() -> None:
    assessment_path = _parse_args()
    assessments = parse_assessment(assessment_path)

    if not assessments:
        print("ERROR: No assessment rows found.")
        print(f"  Checked: {assessment_path}")
        print("  Ensure the table contains rows with numeric Current and Target values (1-5).")
        sys.exit(1)

    week_statuses = parse_week_statuses()
    generate_report(assessments, week_statuses)


if __name__ == "__main__":
    main()
