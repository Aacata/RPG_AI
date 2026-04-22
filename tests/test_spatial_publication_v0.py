from __future__ import annotations

import unittest

from src.core.contracts import MutationKind, ProposedChange, RequestedMutation
from src.core.ids import make_location_id, make_region_id, make_world_space_id
from src.core.runtime import process_proposed_change
from src.core.state_root import StateRoot
from src.world.spatial_publication import (
    SpatialBootstrapPublicationRequest,
    inspect_spatial_bootstrap_publication,
    publish_spatial_bootstrap,
)


class SpatialPublicationV0Tests(unittest.TestCase):
    def make_request(self) -> SpatialBootstrapPublicationRequest:
        return SpatialBootstrapPublicationRequest(
            request_id="publish_map_bootstrap_v0",
            submitted_at="2026-04-16T10:00:00Z",
            world_space_id=make_world_space_id("primary"),
            sea_level_z=0.0,
            region_id=make_region_id("heartlands"),
            region_display_name="Heartlands",
            location_id=make_location_id("rivergate"),
            location_display_name="Rivergate",
            location_type="settlement",
        )

    def test_accepts_minimal_spatial_bootstrap_publication(self) -> None:
        state_root = StateRoot()
        request = self.make_request()

        inspection = inspect_spatial_bootstrap_publication(request)
        self.assertEqual(inspection.status, "accepted")
        self.assertEqual(inspection.diagnostics, ())
        self.assertIsNotNone(inspection.proposed_change)

        updated_state, events, diagnostics = publish_spatial_bootstrap(state_root, request)

        self.assertEqual(diagnostics, ("ProposedChange accepted.",))
        self.assertIn(str(request.world_space_id), updated_state.world_spaces)
        self.assertIn(str(request.region_id), updated_state.regions)
        self.assertIn(str(request.location_id), updated_state.locations)
        self.assertEqual(
            updated_state.world_spaces[str(request.world_space_id)].sea_level_z,
            0.0,
        )
        self.assertEqual(
            updated_state.regions[str(request.region_id)].world_space_ref,
            str(request.world_space_id),
        )
        self.assertEqual(
            updated_state.locations[str(request.location_id)].region_ref,
            str(request.region_id),
        )
        self.assertEqual(
            updated_state.locations[str(request.location_id)].location_type,
            "settlement",
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].payload["approved_change_count"], 3)

    def test_rejects_bundle_when_region_references_unknown_world_space(self) -> None:
        state_root = StateRoot()
        request = self.make_request()
        proposed_change = self._inspect_proposed_change(request)

        bad_region_mutation = RequestedMutation(
            change_id="publish_map_bootstrap_v0_region",
            mutation_kind=MutationKind.CREATE_RECORD,
            target=proposed_change.requested_changes[1].target,
            arguments={
                "record_kind": proposed_change.requested_changes[1].arguments["record_kind"],
                "new_id": proposed_change.requested_changes[1].arguments["new_id"],
                "initial_slots": {
                    "display_name": request.region_display_name,
                    "world_space_ref": str(make_world_space_id("missing_world_space")),
                },
            },
        )
        bad_change = ProposedChange(
            proposal_id=proposed_change.proposal_id,
            origin_type=proposed_change.origin_type,
            intent_type=proposed_change.intent_type,
            target_refs=proposed_change.target_refs,
            requested_changes=(
                proposed_change.requested_changes[0],
                bad_region_mutation,
                proposed_change.requested_changes[2],
            ),
            submitted_at=proposed_change.submitted_at,
            context=proposed_change.context,
        )

        returned_state, events, diagnostics = process_proposed_change(
            state_root,
            bad_change,
            event_suffix_prefix="world_publish",
        )

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertTrue(
            any("Unknown world space reference" in message for message in diagnostics)
        )

    def test_rejects_bundle_when_location_references_unknown_region(self) -> None:
        state_root = StateRoot()
        request = self.make_request()
        proposed_change = self._inspect_proposed_change(request)

        bad_location_mutation = RequestedMutation(
            change_id="publish_map_bootstrap_v0_location",
            mutation_kind=MutationKind.CREATE_RECORD,
            target=proposed_change.requested_changes[2].target,
            arguments={
                "record_kind": proposed_change.requested_changes[2].arguments["record_kind"],
                "new_id": proposed_change.requested_changes[2].arguments["new_id"],
                "initial_slots": {
                    "display_name": request.location_display_name,
                    "region_ref": str(make_region_id("missing_region")),
                    "location_type": request.location_type,
                },
            },
        )
        bad_change = ProposedChange(
            proposal_id=proposed_change.proposal_id,
            origin_type=proposed_change.origin_type,
            intent_type=proposed_change.intent_type,
            target_refs=proposed_change.target_refs,
            requested_changes=(
                proposed_change.requested_changes[0],
                proposed_change.requested_changes[1],
                bad_location_mutation,
            ),
            submitted_at=proposed_change.submitted_at,
            context=proposed_change.context,
        )

        returned_state, events, diagnostics = process_proposed_change(
            state_root,
            bad_change,
            event_suffix_prefix="world_publish",
        )

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertTrue(any("Unknown region reference" in message for message in diagnostics))

    def test_rejects_bundle_atomically_when_one_part_is_invalid(self) -> None:
        state_root = StateRoot()
        request = self.make_request()
        proposed_change = self._inspect_proposed_change(request)

        bad_location_mutation = RequestedMutation(
            change_id="publish_map_bootstrap_v0_location",
            mutation_kind=MutationKind.CREATE_RECORD,
            target=proposed_change.requested_changes[2].target,
            arguments={
                "record_kind": proposed_change.requested_changes[2].arguments["record_kind"],
                "new_id": proposed_change.requested_changes[2].arguments["new_id"],
                "initial_slots": {
                    "display_name": request.location_display_name,
                    "region_ref": str(make_region_id("missing_region")),
                    "location_type": request.location_type,
                },
            },
        )
        bad_change = ProposedChange(
            proposal_id=proposed_change.proposal_id,
            origin_type=proposed_change.origin_type,
            intent_type=proposed_change.intent_type,
            target_refs=proposed_change.target_refs,
            requested_changes=(
                proposed_change.requested_changes[0],
                proposed_change.requested_changes[1],
                bad_location_mutation,
            ),
            submitted_at=proposed_change.submitted_at,
            context=proposed_change.context,
        )

        returned_state, events, diagnostics = process_proposed_change(
            state_root,
            bad_change,
            event_suffix_prefix="world_publish",
        )

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertEqual(returned_state.world_spaces, {})
        self.assertEqual(returned_state.regions, {})
        self.assertEqual(returned_state.locations, {})
        self.assertTrue(any("all-or-nothing" in message for message in diagnostics))

    def test_rejects_duplicate_create_record_target_in_same_bundle(self) -> None:
        state_root = StateRoot()
        request = self.make_request()
        proposed_change = self._inspect_proposed_change(request)

        duplicate_location_mutation = RequestedMutation(
            change_id="publish_map_bootstrap_v0_location_duplicate",
            mutation_kind=MutationKind.CREATE_RECORD,
            target=proposed_change.requested_changes[2].target,
            arguments=dict(proposed_change.requested_changes[2].arguments),
        )
        bad_change = ProposedChange(
            proposal_id=proposed_change.proposal_id,
            origin_type=proposed_change.origin_type,
            intent_type=proposed_change.intent_type,
            target_refs=proposed_change.target_refs,
            requested_changes=(
                proposed_change.requested_changes[0],
                proposed_change.requested_changes[1],
                proposed_change.requested_changes[2],
                duplicate_location_mutation,
            ),
            submitted_at=proposed_change.submitted_at,
            context=proposed_change.context,
        )

        returned_state, events, diagnostics = process_proposed_change(
            state_root,
            bad_change,
            event_suffix_prefix="world_publish",
        )

        self.assertIs(returned_state, state_root)
        self.assertEqual(events, ())
        self.assertEqual(returned_state.world_spaces, {})
        self.assertEqual(returned_state.regions, {})
        self.assertEqual(returned_state.locations, {})
        self.assertTrue(
            any(
                "Duplicate create_record new_id for target kind location"
                in message
                for message in diagnostics
            )
        )

    def _inspect_proposed_change(self, request: SpatialBootstrapPublicationRequest) -> ProposedChange:
        inspection = inspect_spatial_bootstrap_publication(request)
        proposed_change = inspection.proposed_change
        assert proposed_change is not None
        return proposed_change


if __name__ == "__main__":
    unittest.main()
