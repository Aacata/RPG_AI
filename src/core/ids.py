from __future__ import annotations

from typing import NewType


ActorId = NewType("ActorId", str)
EventId = NewType("EventId", str)
LocationId = NewType("LocationId", str)
RegionId = NewType("RegionId", str)
WorldSpaceId = NewType("WorldSpaceId", str)
FactionId = NewType("FactionId", str)
SaveSlotId = NewType("SaveSlotId", str)


def _build_id(prefix: str, raw_value: str) -> str:
    if not raw_value:
        raise ValueError("ID raw value must be non-empty.")
    return f"{prefix}_{raw_value}"


def make_actor_id(raw_value: str) -> ActorId:
    return ActorId(_build_id("actor", raw_value))


def make_event_id(raw_value: str) -> EventId:
    return EventId(_build_id("event", raw_value))


def make_location_id(raw_value: str) -> LocationId:
    return LocationId(_build_id("loc", raw_value))


def make_region_id(raw_value: str) -> RegionId:
    return RegionId(_build_id("region", raw_value))


def make_world_space_id(raw_value: str) -> WorldSpaceId:
    return WorldSpaceId(_build_id("worldspace", raw_value))


def make_faction_id(raw_value: str) -> FactionId:
    return FactionId(_build_id("faction", raw_value))


def make_save_slot_id(raw_value: str) -> SaveSlotId:
    return SaveSlotId(_build_id("save", raw_value))
