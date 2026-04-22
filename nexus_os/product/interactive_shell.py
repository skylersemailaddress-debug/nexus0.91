from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ShellState:
    mode: str = "product"
    history: List[str] = field(default_factory=list)


WELCOME = """Nexus Standalone Shell\n\nCommands:\n  help      Show commands\n  status    Show shell status\n  mission   Set current mission\n  history   Show entered commands\n  quit      Exit shell\n"""


def run_shell(mode: str = "product") -> None:
    state = ShellState(mode=mode)
    mission = "No mission set"

    print(WELCOME)
    while True:
        try:
            raw = input("nexus> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Nexus] Exiting shell")
            return

        if not raw:
            continue

        state.history.append(raw)

        if raw == "help":
            print(WELCOME)
        elif raw == "status":
            print(f"mode={state.mode}")
            print(f"mission={mission}")
            print(f"history_count={len(state.history)}")
        elif raw == "history":
            for idx, item in enumerate(state.history, start=1):
                print(f"{idx}. {item}")
        elif raw.startswith("mission"):
            parts = raw.split(maxsplit=1)
            if len(parts) == 1:
                print(f"mission={mission}")
            else:
                mission = parts[1]
                print(f"[Nexus] Mission set: {mission}")
        elif raw in {"quit", "exit"}:
            print("[Nexus] Goodbye")
            return
        else:
            print(f"[Nexus] Received: {raw}")
