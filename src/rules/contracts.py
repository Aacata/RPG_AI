from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.core.contracts import EventHandoff, ProposedChange
from src.core.ids import ActorId


@dataclass(frozen=True)
class RulesActionRequest:
    request_id: str
    action_kind: Literal["set_actor_current_activity"]
    actor_id: ActorId
    activity: str


@dataclass(frozen=True)
class RulesInspectionResult:
    status: Literal["accepted", "rejected"]
    diagnostics: tuple[str, ...]
    proposed_change: ProposedChange | None
    event_handoff: EventHandoff | None
