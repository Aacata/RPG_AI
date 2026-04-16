from __future__ import annotations

from src.core.ids import LocationId
from src.core.state_root import StateRoot
from src.world.world_state import MapDiscoveryEntry


def reveal_player_location(state_root: StateRoot, location_ref: LocationId) -> None:
    location_key = str(location_ref)
    if location_key not in state_root.locations:
        raise ValueError(f"Unknown location reference: {location_key}.")

    discovery_entry = state_root.player_map_discovery.get(location_key)
    if discovery_entry is None:
        state_root.player_map_discovery[location_key] = MapDiscoveryEntry(
            location_ref=location_ref,
            is_revealed=True,
        )
        return

    discovery_entry.is_revealed = True


def reveal_player_location_name(state_root: StateRoot, location_ref: LocationId) -> None:
    location_key = str(location_ref)
    if location_key not in state_root.locations:
        raise ValueError(f"Unknown location reference: {location_key}.")

    discovery_entry = state_root.player_map_discovery.get(location_key)
    if discovery_entry is None:
        state_root.player_map_discovery[location_key] = MapDiscoveryEntry(
            location_ref=location_ref,
            is_revealed=True,
            is_name_revealed=True,
        )
        return

    discovery_entry.is_revealed = True
    discovery_entry.is_name_revealed = True


def mark_player_location_visited(state_root: StateRoot, location_ref: LocationId) -> None:
    location_key = str(location_ref)
    if location_key not in state_root.locations:
        raise ValueError(f"Unknown location reference: {location_key}.")

    discovery_entry = state_root.player_map_discovery.get(location_key)
    if discovery_entry is None:
        state_root.player_map_discovery[location_key] = MapDiscoveryEntry(
            location_ref=location_ref,
            is_revealed=True,
            is_name_revealed=True,
            is_visited=True,
        )
        return

    discovery_entry.is_revealed = True
    discovery_entry.is_name_revealed = True
    discovery_entry.is_visited = True
