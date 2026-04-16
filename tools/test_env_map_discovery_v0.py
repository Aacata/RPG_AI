from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.ids import LocationId, make_location_id
from src.core.state_root import StateRoot
from src.world.world_state import (
    LocationRecord,
    MapDiscoveryEntry,
    build_player_location_discovery_read_model,
)


def build_demo_state() -> tuple[StateRoot, LocationId]:
    location_id = make_location_id("hidden_shrine")
    state_root = StateRoot(
        locations={
            str(location_id): LocationRecord(
                location_id=location_id,
                display_name="Sunken Shrine",
                location_type="ruin",
                is_hidden_by_default=True,
            )
        }
    )
    return state_root, location_id


def run_demo() -> str:
    state_root, location_id = build_demo_state()
    canonical_location = state_root.locations[str(location_id)]

    no_discovery_entry_view = build_player_location_discovery_read_model(
        location_ref=location_id,
        canonical_location=canonical_location,
        discovery_entry=state_root.player_map_discovery.get(str(location_id)),
    )

    state_root.player_map_discovery[str(location_id)] = MapDiscoveryEntry(
        location_ref=location_id,
        is_revealed=True,
        is_name_revealed=True,
        is_marker_visible=True,
        is_visited=False,
    )

    with_discovery_entry_view = build_player_location_discovery_read_model(
        location_ref=location_id,
        canonical_location=canonical_location,
        discovery_entry=state_root.player_map_discovery.get(str(location_id)),
    )

    output = "\n".join(
        (
            "Map Discovery Demo v0",
            f"location_ref: {location_id}",
            "case: no_discovery_entry",
            f"  canonically_present: {no_discovery_entry_view['canonically_present']}",
            f"  hidden_by_default: {no_discovery_entry_view['hidden_by_default']}",
            f"  is_revealed: {no_discovery_entry_view['is_revealed']}",
            f"  is_name_revealed: {no_discovery_entry_view['is_name_revealed']}",
            f"  is_marker_visible: {no_discovery_entry_view['is_marker_visible']}",
            f"  is_visited: {no_discovery_entry_view['is_visited']}",
            "case: discovery_entry_present",
            f"  canonically_present: {with_discovery_entry_view['canonically_present']}",
            f"  hidden_by_default: {with_discovery_entry_view['hidden_by_default']}",
            f"  is_revealed: {with_discovery_entry_view['is_revealed']}",
            f"  is_name_revealed: {with_discovery_entry_view['is_name_revealed']}",
            f"  is_marker_visible: {with_discovery_entry_view['is_marker_visible']}",
            f"  is_visited: {with_discovery_entry_view['is_visited']}",
        )
    )
    print(output)
    return output


if __name__ == "__main__":
    run_demo()
