from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class MissionHeader:
    mission_title: str
    continuity_label: str
    work_state: str
    active_intelligence_line: str


@dataclass
class PrimarySurface:
    log_lines: List[str] = field(default_factory=list)
    next_best_move: str = ""
    composer_prompt: str = "nexus> "


@dataclass
class ContextReveal:
    kind: str
    title: str
    summary: str
    priority: int = 0


@dataclass
class CapabilityCard:
    kind: str
    title: str
    summary: str


@dataclass
class TrustPanel:
    title: str
    lines: List[str] = field(default_factory=list)


@dataclass
class ApprovalPrompt:
    title: str
    summary: str
    action_label: str = "approve"


@dataclass
class UIControls:
    mode: str = "focus"
    pinned_sections: List[str] = field(default_factory=list)
    hover_target: str = "mission"
    palette_commands: List[str] = field(default_factory=list)


@dataclass
class ShellFrame:
    header: MissionHeader
    primary: PrimarySurface
    reveals: List[ContextReveal] = field(default_factory=list)
    cards: List[CapabilityCard] = field(default_factory=list)
    trust_panel: TrustPanel | None = None
    approval_prompt: ApprovalPrompt | None = None
    controls: UIControls = field(default_factory=UIControls)
