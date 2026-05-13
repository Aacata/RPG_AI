from __future__ import annotations

import json
from typing import Any

from src.core.contracts import ActorSpecialization, AgencySource, StatusFlag
from src.core.ids import (
    ActorId,
    EventId,
    LocationId,
    RegionId,
    SaveSlotId,
    WorldSpaceId,
)
from src.core.state_root import SaveSlotMetaRecord, StateRoot
from src.npc.actor_baseline import ActorRecord
from src.world.world_state import (
    LocationRecord,
    MapDiscoveryEntry,
    RegionRecord,
    WorldRootRecord,
    WorldSpaceRecord,
)

SNAPSHOT_SCHEMA_VERSION = 1


def _encode_world_root(record: WorldRootRecord) -> dict[str, Any]:
    return {
        "world_time": record.world_time,
        "calendar_ref": record.calendar_ref,
        "active_event_refs": [str(ref) for ref in record.active_event_refs],
        "active_faction_refs": list(record.active_faction_refs),
    }


def _decode_world_root(data: dict[str, Any]) -> WorldRootRecord:
    return WorldRootRecord(
        world_time=data.get("world_time"),
        calendar_ref=data.get("calendar_ref"),
        active_event_refs=[EventId(ref) for ref in data.get("active_event_refs", [])],
        active_faction_refs=list(data.get("active_faction_refs", [])),
    )


def _encode_world_space(record: WorldSpaceRecord) -> dict[str, Any]:
    return {
        "world_space_id": str(record.world_space_id),
        "sea_level_z": record.sea_level_z,
    }


def _decode_world_space(data: dict[str, Any]) -> WorldSpaceRecord:
    return WorldSpaceRecord(
        world_space_id=WorldSpaceId(data["world_space_id"]),
        sea_level_z=float(data.get("sea_level_z", 0.0)),
    )


def _encode_location(record: LocationRecord) -> dict[str, Any]:
    return {
        "location_id": str(record.location_id),
        "display_name": record.display_name,
        "region_ref": str(record.region_ref) if record.region_ref is not None else None,
        "location_type": record.location_type,
        "x": record.x,
        "y": record.y,
        "z": record.z,
        "biome": record.biome,
        "is_hidden_by_default": record.is_hidden_by_default,
    }


def _decode_location(data: dict[str, Any]) -> LocationRecord:
    region_ref = data.get("region_ref")
    return LocationRecord(
        location_id=LocationId(data["location_id"]),
        display_name=data.get("display_name"),
        region_ref=RegionId(region_ref) if region_ref is not None else None,
        location_type=data.get("location_type"),
        x=data.get("x"),
        y=data.get("y"),
        z=data.get("z"),
        biome=data.get("biome"),
        is_hidden_by_default=bool(data.get("is_hidden_by_default", False)),
    )


def _encode_region(record: RegionRecord) -> dict[str, Any]:
    return {
        "region_id": str(record.region_id),
        "world_space_ref": str(record.world_space_ref) if record.world_space_ref is not None else None,
        "display_name": record.display_name,
        "region_parent_ref": str(record.region_parent_ref) if record.region_parent_ref is not None else None,
    }


def _decode_region(data: dict[str, Any]) -> RegionRecord:
    wsr = data.get("world_space_ref")
    rpr = data.get("region_parent_ref")
    return RegionRecord(
        region_id=RegionId(data["region_id"]),
        world_space_ref=WorldSpaceId(wsr) if wsr is not None else None,
        display_name=data.get("display_name"),
        region_parent_ref=RegionId(rpr) if rpr is not None else None,
    )


def _encode_map_discovery(entry: MapDiscoveryEntry) -> dict[str, Any]:
    return {
        "location_ref": str(entry.location_ref),
        "is_revealed": entry.is_revealed,
        "is_name_revealed": entry.is_name_revealed,
        "is_marker_visible": entry.is_marker_visible,
        "is_visited": entry.is_visited,
    }


def _decode_map_discovery(data: dict[str, Any]) -> MapDiscoveryEntry:
    return MapDiscoveryEntry(
        location_ref=LocationId(data["location_ref"]),
        is_revealed=bool(data.get("is_revealed", False)),
        is_name_revealed=bool(data.get("is_name_revealed", False)),
        is_marker_visible=bool(data.get("is_marker_visible", False)),
        is_visited=bool(data.get("is_visited", False)),
    )


def _encode_save_slot(record: SaveSlotMetaRecord) -> dict[str, Any]:
    return {
        "save_slot_id": str(record.save_slot_id),
        "save_label": record.save_label,
        "save_last_updated": record.save_last_updated,
        "world_snapshot_ref": record.world_snapshot_ref,
        "event_checkpoint_ref": record.event_checkpoint_ref,
        "player_actor_ref": str(record.player_actor_ref) if record.player_actor_ref is not None else None,
    }


def _decode_save_slot(data: dict[str, Any]) -> SaveSlotMetaRecord:
    par = data.get("player_actor_ref")
    return SaveSlotMetaRecord(
        save_slot_id=SaveSlotId(data["save_slot_id"]),
        save_label=data.get("save_label"),
        save_last_updated=data.get("save_last_updated"),
        world_snapshot_ref=data.get("world_snapshot_ref"),
        event_checkpoint_ref=data.get("event_checkpoint_ref"),
        player_actor_ref=ActorId(par) if par is not None else None,
    )


def _encode_actor(record: ActorRecord) -> dict[str, Any]:
    return {
        "actor_id": str(record.actor_id),
        "display_name": record.display_name,
        "origin_archetype": record.origin_archetype,
        "actor_specialization": record.actor_specialization.value if record.actor_specialization else None,
        "agency_source": record.agency_source.value if record.agency_source else None,
        "category_or_role": record.category_or_role,
        "priority_tier": record.priority_tier,
        "location_ref": str(record.location_ref) if record.location_ref is not None else None,
        "current_activity": record.current_activity,
        "goal_ref": record.goal_ref,
        "schedule_ref": record.schedule_ref,
        "inventory_ref": record.inventory_ref,
        "faction_link_refs": list(record.faction_link_refs),
        "status_flags": sorted(flag.value for flag in record.status_flags),
    }


def _decode_actor(data: dict[str, Any]) -> ActorRecord:
    spec = data.get("actor_specialization")
    agency = data.get("agency_source")
    loc = data.get("location_ref")
    flags_raw = data.get("status_flags", [])
    return ActorRecord(
        actor_id=ActorId(data["actor_id"]),
        display_name=data.get("display_name"),
        origin_archetype=data.get("origin_archetype"),
        actor_specialization=ActorSpecialization(spec) if spec is not None else None,
        agency_source=AgencySource(agency) if agency is not None else None,
        category_or_role=data.get("category_or_role"),
        priority_tier=data.get("priority_tier"),
        location_ref=LocationId(loc) if loc is not None else None,
        current_activity=data.get("current_activity"),
        goal_ref=data.get("goal_ref"),
        schedule_ref=data.get("schedule_ref"),
        inventory_ref=data.get("inventory_ref"),
        faction_link_refs=list(data.get("faction_link_refs", [])),
        status_flags={StatusFlag(f) for f in flags_raw},
    )


def encode_state_root(state_root: StateRoot) -> str:
    payload: dict[str, Any] = {
        "snapshot_schema_version": SNAPSHOT_SCHEMA_VERSION,
        "world_root": _encode_world_root(state_root.world_root),
        "world_spaces": {k: _encode_world_space(v) for k, v in state_root.world_spaces.items()},
        "actors": {k: _encode_actor(v) for k, v in state_root.actors.items()},
        "locations": {k: _encode_location(v) for k, v in state_root.locations.items()},
        "player_map_discovery": {k: _encode_map_discovery(v) for k, v in state_root.player_map_discovery.items()},
        "regions": {k: _encode_region(v) for k, v in state_root.regions.items()},
        "save_slots": {k: _encode_save_slot(v) for k, v in state_root.save_slots.items()},
    }
    return json.dumps(payload, sort_keys=True)


def decode_state_root(blob: str) -> StateRoot:
    data = json.loads(blob)
    if int(data.get("snapshot_schema_version", 0)) != SNAPSHOT_SCHEMA_VERSION:
        raise ValueError("Unsupported snapshot_schema_version.")

    return StateRoot(
        world_root=_decode_world_root(data["world_root"]),
        world_spaces={k: _decode_world_space(v) for k, v in data.get("world_spaces", {}).items()},
        actors={k: _decode_actor(v) for k, v in data.get("actors", {}).items()},
        locations={k: _decode_location(v) for k, v in data.get("locations", {}).items()},
        player_map_discovery={k: _decode_map_discovery(v) for k, v in data.get("player_map_discovery", {}).items()},
        regions={k: _decode_region(v) for k, v in data.get("regions", {}).items()},
        save_slots={k: _decode_save_slot(v) for k, v in data.get("save_slots", {}).items()},
    )
