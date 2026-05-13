from __future__ import annotations

from src.core.ids import LocationId
from src.core.state_root import StateRoot
from src.world.map_discovery_pipeline import (
    mark_player_location_visited_through_runtime,
    reveal_player_location_name_through_runtime,
    reveal_player_location_through_runtime,
    set_player_location_marker_visible_through_runtime,
)


def _sync_discovery_overlay(state_root: StateRoot, updated: StateRoot) -> None:
    state_root.player_map_discovery.clear()
    state_root.player_map_discovery.update(updated.player_map_discovery)


def reveal_player_location(state_root: StateRoot, location_ref: LocationId) -> None:
    updated, events, diagnostics = reveal_player_location_through_runtime(
        state_root,
        location_ref,
    )
    if not events:
        raise ValueError(diagnostics[0] if diagnostics else "Map discovery reveal was rejected.")
    _sync_discovery_overlay(state_root, updated)


def reveal_player_location_name(state_root: StateRoot, location_ref: LocationId) -> None:
    updated, events, diagnostics = reveal_player_location_name_through_runtime(
        state_root,
        location_ref,
    )
    if not events:
        raise ValueError(
            diagnostics[0] if diagnostics else "Map discovery reveal_name was rejected."
        )
    _sync_discovery_overlay(state_root, updated)


def mark_player_location_visited(state_root: StateRoot, location_ref: LocationId) -> None:
    updated, events, diagnostics = mark_player_location_visited_through_runtime(
        state_root,
        location_ref,
    )
    if not events:
        raise ValueError(diagnostics[0] if diagnostics else "Map discovery visit was rejected.")
    _sync_discovery_overlay(state_root, updated)


def set_player_location_marker_visible(state_root: StateRoot, location_ref: LocationId) -> None:
    updated, events, diagnostics = set_player_location_marker_visible_through_runtime(
        state_root,
        location_ref,
    )
    if not events:
        raise ValueError(
            diagnostics[0] if diagnostics else "Map discovery marker_visible was rejected."
        )
    _sync_discovery_overlay(state_root, updated)
