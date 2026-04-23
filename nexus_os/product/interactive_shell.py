from __future__ import annotations

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from .readiness_engine import score_readiness_field


def _render_workspace(runtime: dict) -> None:
    panes = score_readiness_field(runtime)

    print("=" * 72)
    print("WORKSPACE (curated readiness field)")
    print("=" * 72)

    for pane in panes[:4]:
        print(f"[{pane.title}] ({pane.kind})")
        print(f"  {pane.summary}")
        print(f"  actions: {', '.join(pane.actions)}")
        print(f"  why: {pane.reason}")
        print("-" * 72)


def _render_chat(runtime: dict) -> None:
    ui = runtime.get("ui_state", {})
    active = ui.get("chat_active", False)
    if active:
        print("[chat: active]")
    else:
        print("[chat: collapsed — press enter to open]")


def run_shell() -> None:
    while True:
        runtime = load_state()

        _render_workspace(runtime)
        _render_chat(runtime)

        cmd = input("nexus> ").strip()
        ui = runtime.setdefault("ui_state", {})

        if cmd in {"exit", "quit"}:
            return

        ui["chat_active"] = True

        if cmd.startswith("pin "):
            ui.setdefault("pinned_sections", []).append(cmd.split(" ", 1)[1])

        elif cmd.startswith("mode "):
            ui["mode"] = cmd.split(" ", 1)[1]

        elif cmd == "collapse":
            ui["chat_active"] = False

        else:
            msg = {
                "id": f"msg:{len(runtime.get('messages', [])) + 1}",
                "role": "user",
                "text": cmd,
                "meta": {},
            }
            runtime.setdefault("messages", []).append(msg)
            append_audit_event("message_append", msg)

        save_state(runtime)
