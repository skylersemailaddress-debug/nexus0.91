from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from nexus_os.autonomy_policy import evaluate
from nexus_os.benchmarking import run_benchmark
from nexus_os.customer_ops import process_event
from nexus_os.distribution import build_distribution
from nexus_os.economics import compute_economics
from nexus_os.factory import build_factory, blueprint_summary
from nexus_os.fleet_maintenance import check_status
from nexus_os.market_intelligence import analyze_signal
from nexus_os.portfolio import build_portfolio
from nexus_os.surface_fabric import build_surface

ROOT = Path(__file__).resolve().parents[2]
ALPHA_RUN_DIR = ROOT / "docs" / "release" / "evidence" / "alpha_runs"


@dataclass(frozen=True)
class EdgeSurface:
    name: str
    role: str
    default_state: str = "hover_reveal"
    pinnable: bool = True
    keyboard_shortcut: str = ""
    live_bindings: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AlphaRun:
    generated_at: str
    idea: str
    shell_doctrine: str
    resting_state: str
    edge_surfaces: list[EdgeSurface]
    pane_families: dict[str, object]
    pipeline: dict[str, object]
    saved_to: str = ""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(text: str) -> str:
    cleaned = "_".join(part for part in text.lower().replace("/", " ").split() if part)
    return cleaned[:80] or "alpha_run"


def _edge_surfaces() -> list[EdgeSurface]:
    return [
        EdgeSurface(
            name="left_edge",
            role="continuity_projects_threads_rituals_history_memory",
            keyboard_shortcut="Ctrl+L",
            live_bindings=["projects", "threads", "memory_anchors", "recent_runs"],
        ),
        EdgeSurface(
            name="right_edge",
            role="jobs_approvals_blockers_prepared_outputs_runtime_truth",
            keyboard_shortcut="Ctrl+R",
            live_bindings=["policy_decision", "factory_blueprint", "surface_plan", "run_status"],
        ),
        EdgeSurface(
            name="top_edge",
            role="global_control_mode_workspace_notifications_command_palette",
            keyboard_shortcut="Ctrl+K",
            live_bindings=["mode", "workspace_identity", "notifications"],
        ),
        EdgeSurface(
            name="bottom_command_bar",
            role="chat_input_quick_actions_attachments_voice_recent_commands",
            keyboard_shortcut="Ctrl+Space",
            live_bindings=["messy_input", "quick_actions", "command_memory"],
        ),
    ]


def build_alpha_workspace(idea: str) -> AlphaRun:
    signal = analyze_signal("alpha_operator", idea)
    portfolio = build_portfolio([idea])
    top = portfolio.ranked_items[0] if portfolio.ranked_items else None
    factory = build_factory(top.name if top else idea)
    surface = build_surface(factory.name, factory.workflows)
    economics = compute_economics(1000, 400)
    policy = evaluate("deploy to production")
    distribution = build_distribution(factory.name)
    customer = process_event(idea)
    fleet = check_status("alpha_runtime_ok")
    benchmark = run_benchmark(signal.opportunity_score)

    pipeline = {
        "market_signal": asdict(signal),
        "portfolio_decision": asdict(top) if top else None,
        "factory_blueprint": asdict(factory),
        "factory_summary": blueprint_summary(factory),
        "surface_plan": asdict(surface),
        "economics": asdict(economics),
        "autonomy_policy": asdict(policy),
        "distribution": asdict(distribution),
        "customer_ops": asdict(customer),
        "fleet_maintenance": asdict(fleet),
        "benchmarking": asdict(benchmark),
    }

    panes: dict[str, object] = {
        "now": {
            "objective": idea,
            "best_next_move": top.recommended_next_step if top else "clarify_input",
            "priority": top.priority if top else "unknown",
        },
        "what_changed": ["new_alpha_run_generated", "product_domain_pipeline_completed"],
        "in_motion": {
            "factory_workflows": factory.workflows,
            "surface_panels": [panel.name for panel in surface.panels],
        },
        "needs_you": {
            "policy_requires_approval": policy.requires_approval,
            "blocked": policy.blocked,
            "controls": policy.controls,
        },
        "prepared_for_you": {
            "distribution_channels": distribution.channels,
            "campaigns": distribution.campaigns,
            "acceptance_criteria": factory.acceptance_criteria,
        },
        "context": {
            "customer_pains": signal.customer_pains,
            "evidence": signal.evidence,
            "benchmark_label": benchmark.label,
        },
    }

    return AlphaRun(
        generated_at=_utc_now(),
        idea=idea,
        shell_doctrine="hover_native_ambient_command_os",
        resting_state="minimal_workspace_with_adaptive_operational_reveals",
        edge_surfaces=_edge_surfaces(),
        pane_families=panes,
        pipeline=pipeline,
    )


def save_alpha_run(run: AlphaRun) -> Path:
    ALPHA_RUN_DIR.mkdir(parents=True, exist_ok=True)
    path = ALPHA_RUN_DIR / f"{_slug(run.idea)}.json"
    payload = asdict(run)
    payload["saved_to"] = str(path.relative_to(ROOT))
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def render_alpha_workspace(run: AlphaRun) -> str:
    panes = run.pane_families
    pipeline = run.pipeline
    lines = [
        "NEXUS ALPHA WORKSPACE",
        "doctrine: hover-native ambient command OS",
        "resting_state: minimal workspace; surfaces reveal on intent; every surface is pinnable",
        "",
        "EDGES",
    ]
    for edge in run.edge_surfaces:
        lines.append(f"- {edge.name}: {edge.role} [{edge.default_state}, shortcut={edge.keyboard_shortcut}]")
    lines.extend([
        "",
        "NOW",
        json.dumps(panes["now"], indent=2),
        "",
        "IN MOTION",
        json.dumps(panes["in_motion"], indent=2),
        "",
        "NEEDS YOU",
        json.dumps(panes["needs_you"], indent=2),
        "",
        "PREPARED FOR YOU",
        json.dumps(panes["prepared_for_you"], indent=2),
        "",
        "CONTEXT",
        json.dumps(panes["context"], indent=2),
        "",
        "PIPELINE SUMMARY",
        json.dumps({
            "market_opportunity_score": pipeline["market_signal"]["opportunity_score"],
            "portfolio_priority": pipeline["portfolio_decision"]["priority"] if pipeline["portfolio_decision"] else None,
            "product_type": pipeline["factory_blueprint"]["product_type"],
            "surface_panels": [panel["name"] for panel in pipeline["surface_plan"]["panels"]],
            "economics_viability": pipeline["economics"]["viability"],
            "policy_requires_approval": pipeline["autonomy_policy"]["requires_approval"],
            "benchmark_label": pipeline["benchmarking"]["label"],
        }, indent=2),
    ])
    return "\n".join(lines)


def main() -> None:
    print("Nexus UI alpha shell")
    print("Paste messy product/company input. Press Enter to run. Blank input uses default alpha scenario.")
    idea = input("> ").strip() or "urgent customer churn problem in enterprise SaaS"
    run = build_alpha_workspace(idea)
    path = save_alpha_run(run)
    print(render_alpha_workspace(run))
    print(f"\nSAVED_ALPHA_RUN={path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
