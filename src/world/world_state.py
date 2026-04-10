from __future__ import annotations

from dataclasses import dataclass, field

from src.core.ids import EventId, LocationId, RegionId


@dataclass
class WorldRootRecord:
    world_time: str | None = None
    calendar_ref: str | None = None
    active_event_refs: list[EventId] = field(default_factory=list)
    active_faction_refs: list[str] = field(default_factory=list)


@dataclass
class LocationRecord:
    location_id: LocationId
    display_name: str | None = None
    region_ref: RegionId | None = None
    location_type: str | None = None


@dataclass
class RegionRecord:
    region_id: RegionId
    display_name: str | None = None
    region_parent_ref: RegionId | None = None
