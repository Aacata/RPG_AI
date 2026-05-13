from __future__ import annotations

import unittest

from src.core.contracts import EventCategory, SlotKey, TargetKind
from src.core.ids import make_location_id
from src.core.state_root import StateRoot
from src.world.map_discovery_pipeline import (
    mark_player_location_visited_through_runtime,
    reveal_player_location_name_through_runtime,
    reveal_player_location_through_runtime,
    set_player_location_marker_visible_through_runtime,
)
from src.world.world_state import LocationRecord


class MapDiscoveryPipelineTests(unittest.TestCase):
    def test_reveal_emits_world_event_with_intent_payload(self) -> None:
        loc = make_location_id("shrine")
        state = StateRoot(
            locations={
                str(loc): LocationRecord(
                    location_id=loc,
                    display_name="Shrine",
                    location_type="ruin",
                )
            }
        )
        updated, events, diag = reveal_player_location_through_runtime(
            state,
            loc,
            proposal_id="p_reveal",
            submitted_at="2026-05-12T14:00:00Z",
        )
        self.assertEqual(diag, ("ProposedChange accepted.",))
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].category, EventCategory.WORLD)
        self.assertEqual(events[0].payload.get("intent_type"), "map_discovery.reveal_location")
        self.assertEqual(events[0].payload.get("location_ref"), str(loc))
        self.assertTrue(updated.player_map_discovery[str(loc)].is_revealed)

    def test_discovery_slots_legal_for_player_map_discovery_target(self) -> None:
        from src.core.transition_validation import is_legal_slot_for_target

        self.assertTrue(
            is_legal_slot_for_target(TargetKind.PLAYER_MAP_DISCOVERY, SlotKey.DISCOVERY_IS_REVEALED)
        )
        self.assertTrue(
            is_legal_slot_for_target(
                TargetKind.PLAYER_MAP_DISCOVERY, SlotKey.DISCOVERY_IS_MARKER_VISIBLE
            )
        )

    def test_set_marker_visible_through_runtime(self) -> None:
        loc = make_location_id("peak")
        state = StateRoot(
            locations={
                str(loc): LocationRecord(
                    location_id=loc,
                    display_name="Peak",
                    location_type="wilderness",
                )
            }
        )
        updated, events, _ = set_player_location_marker_visible_through_runtime(
            state,
            loc,
            proposal_id="p_marker",
            submitted_at="2026-05-12T15:00:00Z",
        )
        self.assertTrue(events)
        self.assertTrue(updated.player_map_discovery[str(loc)].is_marker_visible)
        self.assertEqual(
            events[0].payload.get("intent_type"),
            "map_discovery.set_marker_visible",
        )

    def test_visit_sets_all_three_flags(self) -> None:
        loc = make_location_id("vault")
        state = StateRoot(
            locations={
                str(loc): LocationRecord(
                    location_id=loc,
                    display_name="Vault",
                    location_type="ruin",
                )
            }
        )
        state, _, _ = reveal_player_location_name_through_runtime(
            state,
            loc,
            proposal_id="p_name",
            submitted_at="2026-05-12T14:00:00Z",
        )
        updated, events, _ = mark_player_location_visited_through_runtime(
            state,
            loc,
            proposal_id="p_visit",
            submitted_at="2026-05-12T14:02:00Z",
        )
        self.assertTrue(events)
        entry = updated.player_map_discovery[str(loc)]
        self.assertTrue(entry.is_revealed)
        self.assertTrue(entry.is_name_revealed)
        self.assertTrue(entry.is_visited)


if __name__ == "__main__":
    unittest.main()
