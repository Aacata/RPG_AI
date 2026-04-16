from __future__ import annotations

from dataclasses import dataclass, field

from src.core.ids import EventId, LocationId, RegionId, WorldSpaceId


@dataclass
class WorldSpaceRecord:
    world_space_id: WorldSpaceId
    sea_level_z: float = 0.0


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
    x: float | None = None
    y: float | None = None
    z: float | None = None
    biome: str | None = None
    is_hidden_by_default: bool = False


@dataclass
class MapDiscoveryEntry:
    location_ref: LocationId
    is_revealed: bool = False
    is_name_revealed: bool = False
    is_marker_visible: bool = False
    is_visited: bool = False


def build_player_location_discovery_read_model(
    location_ref: LocationId,
    canonical_location: LocationRecord | None,
    discovery_entry: MapDiscoveryEntry | None,
) -> dict[str, object]:
    return {
        "location_ref": str(location_ref),
        "canonically_present": canonical_location is not None,
        "hidden_by_default": (
            canonical_location.is_hidden_by_default if canonical_location is not None else False
        ),
        "is_revealed": discovery_entry.is_revealed if discovery_entry is not None else False,
        "is_name_revealed": (
            discovery_entry.is_name_revealed if discovery_entry is not None else False
        ),
        "is_marker_visible": (
            discovery_entry.is_marker_visible if discovery_entry is not None else False
        ),
        "is_visited": discovery_entry.is_visited if discovery_entry is not None else False,
    }


@dataclass
class RegionRecord:
    region_id: RegionId
    world_space_ref: WorldSpaceId | None = None
    display_name: str | None = None
    region_parent_ref: RegionId | None = None
