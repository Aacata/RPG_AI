from __future__ import annotations

from dataclasses import dataclass, field

from src.core.ids import ActorId, SaveSlotId
from src.npc.actor_baseline import ActorRecord
from src.world.world_state import (
    LocationRecord,
    MapDiscoveryEntry,
    RegionRecord,
    WorldRootRecord,
    WorldSpaceRecord,
)


@dataclass
class SaveSlotMetaRecord:
    save_slot_id: SaveSlotId
    save_label: str | None = None
    save_last_updated: str | None = None
    world_snapshot_ref: str | None = None
    event_checkpoint_ref: str | None = None
    player_actor_ref: ActorId | None = None


@dataclass
class StateRoot:
    world_root: WorldRootRecord = field(default_factory=WorldRootRecord)
    world_spaces: dict[str, WorldSpaceRecord] = field(default_factory=dict)
    actors: dict[str, ActorRecord] = field(default_factory=dict)
    locations: dict[str, LocationRecord] = field(default_factory=dict)
    player_map_discovery: dict[str, MapDiscoveryEntry] = field(default_factory=dict)
    regions: dict[str, RegionRecord] = field(default_factory=dict)
    save_slots: dict[str, SaveSlotMetaRecord] = field(default_factory=dict)
