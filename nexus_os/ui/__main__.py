from __future__ import annotations

import argparse
import html
import json
import threading
import urllib.parse
import webbrowser
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

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
DEFAULT_IDEA = "urgent customer churn problem in enterprise SaaS"


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
    idea = idea.strip() or DEFAULT_IDEA
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
        json.dumps(_pipeline_summary(run), indent=2),
    ])
    return "\n".join(lines)


def _pipeline_summary(run: AlphaRun) -> dict[str, Any]:
    pipeline = run.pipeline
    portfolio = pipeline.get("portfolio_decision") or {}
    surface = pipeline.get("surface_plan") or {}
    return {
        "market_opportunity_score": pipeline["market_signal"]["opportunity_score"],
        "portfolio_priority": portfolio.get("priority"),
        "product_type": pipeline["factory_blueprint"]["product_type"],
        "surface_panels": [panel["name"] for panel in surface.get("panels", [])],
        "economics_viability": pipeline["economics"]["viability"],
        "policy_requires_approval": pipeline["autonomy_policy"]["requires_approval"],
        "benchmark_label": pipeline["benchmarking"]["label"],
    }


def _html_escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _json_block(value: object) -> str:
    return html.escape(json.dumps(value, indent=2), quote=False)


def _render_card(title: str, body: object) -> str:
    return f"""
      <section class="card">
        <h2>{_html_escape(title)}</h2>
        <pre>{_json_block(body)}</pre>
      </section>
    """


def render_html(run: AlphaRun, saved_path: str = "") -> str:
    panes = run.pane_families
    pipeline = run.pipeline
    summary = _pipeline_summary(run)
    cards = "\n".join([
        _render_card("Now", panes["now"]),
        _render_card("In Motion", panes["in_motion"]),
        _render_card("Needs You", panes["needs_you"]),
        _render_card("Prepared For You", panes["prepared_for_you"]),
        _render_card("Context", panes["context"]),
        _render_card("Factory Blueprint", pipeline["factory_summary"]),
        _render_card("Economics", pipeline["economics"]),
        _render_card("Autonomy Policy", pipeline["autonomy_policy"]),
        _render_card("Distribution", pipeline["distribution"]),
    ])
    edges = "\n".join(
        f"<button class='edge-pill' title='{_html_escape(edge.role)}'>{_html_escape(edge.name)} <span>{_html_escape(edge.keyboard_shortcut)}</span></button>"
        for edge in run.edge_surfaces
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Nexus Alpha UI</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #08090b;
      --panel: rgba(255,255,255,0.065);
      --panel-strong: rgba(255,255,255,0.11);
      --text: #f4f6f8;
      --muted: #9aa4b2;
      --line: rgba(255,255,255,0.12);
      --accent: #a9c7ff;
      --good: #9df2bf;
      --warn: #ffd58a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at top left, rgba(104,132,255,0.18), transparent 32rem),
        radial-gradient(circle at bottom right, rgba(157,242,191,0.09), transparent 30rem),
        var(--bg);
      color: var(--text);
      overflow-x: hidden;
    }}
    .workspace {{
      min-height: 100vh;
      padding: 6.5rem 5.5rem 8rem;
    }}
    .hero {{ max-width: 980px; margin: 0 auto 2rem; }}
    .eyebrow {{ color: var(--accent); letter-spacing: .16em; text-transform: uppercase; font-size: .72rem; }}
    h1 {{ font-size: clamp(2.3rem, 7vw, 5.5rem); line-height: .92; margin: .6rem 0 1rem; font-weight: 720; }}
    .sub {{ color: var(--muted); max-width: 720px; font-size: 1rem; line-height: 1.6; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: .8rem;
      max-width: 980px;
      margin: 0 auto 1.4rem;
    }}
    .metric {{ padding: 1rem; border: 1px solid var(--line); background: var(--panel); border-radius: 1.25rem; }}
    .metric b {{ display:block; font-size: 1.3rem; margin-bottom: .2rem; }}
    .metric span {{ color: var(--muted); font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 1rem;
      max-width: 1180px;
      margin: 0 auto;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 1.4rem;
      background: var(--panel);
      box-shadow: 0 24px 80px rgba(0,0,0,.26);
      padding: 1rem;
      min-height: 160px;
    }}
    .card h2 {{ margin: 0 0 .7rem; font-size: .92rem; letter-spacing: .04em; }}
    pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; color: #dbe5f5; font-size: .82rem; line-height: 1.45; }}
    .edge {{ position: fixed; z-index: 20; transition: transform .22s ease, opacity .22s ease; opacity: .42; }}
    .edge:hover, .edge.pinned {{ transform: translate(0,0); opacity: 1; }}
    .edge-left {{ left: 0; top: 25vh; transform: translateX(-72%); }}
    .edge-right {{ right: 0; top: 25vh; transform: translateX(72%); }}
    .edge-top {{ top: 0; left: 50%; transform: translate(-50%, -62%); }}
    .edge-bottom {{ bottom: 0; left: 50%; transform: translate(-50%, 62%); width: min(860px, calc(100vw - 2rem)); }}
    .edge-box {{
      border: 1px solid var(--line);
      background: rgba(17,19,24,.9);
      backdrop-filter: blur(24px);
      border-radius: 1.2rem;
      padding: .65rem;
      display: flex;
      gap: .5rem;
      flex-wrap: wrap;
      box-shadow: 0 18px 80px rgba(0,0,0,.4);
    }}
    .edge-pill, .pin, button {{
      border: 1px solid var(--line);
      background: var(--panel-strong);
      color: var(--text);
      border-radius: 999px;
      padding: .55rem .75rem;
      cursor: pointer;
    }}
    .edge-pill span {{ color: var(--muted); margin-left: .4rem; }}
    .command {{ display:flex; gap:.5rem; width:100%; }}
    .command input {{
      flex: 1;
      border: 1px solid var(--line);
      background: rgba(255,255,255,.08);
      color: var(--text);
      border-radius: 999px;
      padding: .8rem 1rem;
      outline: none;
    }}
    .saved {{ color: var(--muted); font-size: .82rem; margin-top: .5rem; }}
    .hint {{ position: fixed; left: 1rem; bottom: 1rem; color: var(--muted); font-size:.78rem; }}
  </style>
</head>
<body>
  <div class="edge edge-left" id="leftEdge"><div class="edge-box"><button class="pin" data-pin="leftEdge">pin</button><span>Continuity</span><span>Projects</span><span>Memory</span></div></div>
  <div class="edge edge-right" id="rightEdge"><div class="edge-box"><button class="pin" data-pin="rightEdge">pin</button><span>Jobs</span><span>Approvals</span><span>Runtime Truth</span></div></div>
  <div class="edge edge-top" id="topEdge"><div class="edge-box"><button class="pin" data-pin="topEdge">pin</button>{edges}</div></div>
  <div class="edge edge-bottom" id="bottomEdge"><div class="edge-box"><button class="pin" data-pin="bottomEdge">pin</button><form class="command" method="get" action="/"><input name="idea" value="{_html_escape(run.idea)}" aria-label="Messy product input" /><button type="submit">Run Nexus</button></form><div class="saved">{_html_escape(saved_path)}</div></div></div>
  <main class="workspace">
    <section class="hero">
      <div class="eyebrow">Nexus Alpha Workspace</div>
      <h1>{_html_escape(run.idea)}</h1>
      <p class="sub">Master-truth aligned local UI: workspace first, hover-native edges, pinnable surfaces, adaptive pane families, and live product-domain pipeline output.</p>
    </section>
    <section class="summary">
      <div class="metric"><b>{_html_escape(summary['portfolio_priority'])}</b><span>Priority</span></div>
      <div class="metric"><b>{_html_escape(summary['product_type'])}</b><span>Product Type</span></div>
      <div class="metric"><b>{_html_escape(summary['market_opportunity_score'])}</b><span>Opportunity</span></div>
      <div class="metric"><b>{_html_escape(summary['economics_viability'])}</b><span>Economics</span></div>
      <div class="metric"><b>{_html_escape(summary['benchmark_label'])}</b><span>Benchmark</span></div>
    </section>
    <section class="cards">{cards}</section>
  </main>
  <div class="hint">Hover edges. Ctrl+K top. Ctrl+Space command. Pins persist for this page.</div>
  <script>
    document.querySelectorAll('.pin').forEach(btn => btn.addEventListener('click', () => {{
      const id = btn.getAttribute('data-pin');
      document.getElementById(id).classList.toggle('pinned');
    }}));
    window.addEventListener('keydown', event => {{
      if (event.ctrlKey && event.key.toLowerCase() === 'k') document.getElementById('topEdge').classList.toggle('pinned');
      if (event.ctrlKey && event.key === ' ') {{ event.preventDefault(); document.getElementById('bottomEdge').classList.toggle('pinned'); }}
      if (event.ctrlKey && event.key.toLowerCase() === 'l') document.getElementById('leftEdge').classList.toggle('pinned');
      if (event.ctrlKey && event.key.toLowerCase() === 'r') document.getElementById('rightEdge').classList.toggle('pinned');
    }});
  </script>
</body>
</html>"""


class NexusAlphaHandler(BaseHTTPRequestHandler):
    server_version = "NexusAlphaUI/1.0"

    def do_GET(self) -> None:  # noqa: N802 - stdlib API name
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path not in {"/", "/index.html"}:
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
            return
        params = urllib.parse.parse_qs(parsed.query)
        idea = params.get("idea", [DEFAULT_IDEA])[0]
        run = build_alpha_workspace(idea)
        saved_path = save_alpha_run(run)
        body = render_html(run, str(saved_path.relative_to(ROOT))).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[nexus-ui] {self.address_string()} - {format % args}")


def launch_web_ui(port: int = 8765, open_browser: bool = True) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), NexusAlphaHandler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Nexus local alpha UI: {url}")
    print("Press Ctrl+C to stop.")
    if open_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Nexus local alpha UI.")
    finally:
        server.server_close()


def run_cli() -> None:
    print("Nexus UI alpha shell")
    print("Paste messy product/company input. Press Enter to run. Blank input uses default alpha scenario.")
    idea = input("> ").strip() or DEFAULT_IDEA
    run = build_alpha_workspace(idea)
    path = save_alpha_run(run)
    print(render_alpha_workspace(run))
    print(f"\nSAVED_ALPHA_RUN={path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Launch Nexus alpha UI")
    parser.add_argument("--cli", action="store_true", help="Use terminal alpha UI instead of browser UI")
    parser.add_argument("--port", type=int, default=8765, help="Local browser UI port")
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open the browser")
    args = parser.parse_args()

    if args.cli:
        run_cli()
    else:
        launch_web_ui(port=args.port, open_browser=not args.no_open)


if __name__ == "__main__":
    main()
