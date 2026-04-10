from __future__ import annotations

from dataclasses import dataclass, field

from src.core.contracts import ActorSpecialization, AgencySource, StatusFlag
from src.core.ids import ActorId, LocationId


@dataclass
class ActorRecord:
    actor_id: ActorId
    display_name: str | None = None
    origin_archetype: str | None = None
    actor_specialization: ActorSpecialization | None = None
    agency_source: AgencySource | None = None
    category_or_role: str | None = None
    priority_tier: str | None = None
    location_ref: LocationId | None = None
    current_activity: str | None = None
    goal_ref: str | None = None
    schedule_ref: str | None = None
    inventory_ref: str | None = None
    faction_link_refs: list[str] = field(default_factory=list)
    status_flags: set[StatusFlag] = field(default_factory=set)
