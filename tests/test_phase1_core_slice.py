from __future__ import annotations

import unittest

from src.core.contracts import (
    ActorSpecialization,
    AgencySource,
    MutationKind,
    ProposedChange,
    ProposedChangeOrigin,
    RequestedMutation,
    SlotKey,
    StatusFlag,
    TargetKind,
    TargetSelector,
    ValidationStatus,
)
from src.core.ids import (
    make_actor_id,
    make_location_id,
    make_region_id,
    make_save_slot_id,
    make_world_space_id,
)
from src.core.runtime import process_proposed_change
from src.core.state_root import SaveSlotMetaRecord, StateRoot
from src.core.transition_validation import (
    is_legal_mutation_kind,
    is_legal_slot_for_target,
    is_legal_slot_key,
    is_legal_status_flag,
    is_legal_target_kind,
    validate_proposed_change,
)
from src.npc.actor_baseline import ActorRecord
from src.world.map_discovery_updates import (
    mark_player_location_visited,
    reveal_player_location,
    reveal_player_location_name,
)
from src.world.world_state import (
    LocationRecord,
    MapDiscoveryEntry,
    RegionRecord,
    WorldRootRecord,
    WorldSpaceRecord,
    build_player_location_discovery_read_model,
)


class Phase1CoreSliceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.player_id = make_actor_id("player")
        self.npc_id = make_actor_id("npc")
        self.location_id = make_location_id("town")
        self.region_id = make_region_id("heartlands")
        self.region_parent_id = make_region_id("continent")
        self.save_id = make_save_slot_id("slot1")

        self.state_root = StateRoot(
            world_root=WorldRootRecord(),
            actors={
                str(self.player_id): ActorRecord(
                    actor_id=self.player_id,
                    display_name="Player",
                    actor_specialization=ActorSpecialization.PLAYER,
                    agency_source=AgencySource.HUMAN_PLAYER,
                    location_ref=self.location_id,
                    status_flags={StatusFlag.ACTIVE},
                ),
                str(self.npc_id): ActorRecord(
                    actor_id=self.npc_id,
                    display_name="Npc",
                    actor_specialization=ActorSpecialization.NPC,
                    agency_source=AgencySource.SIMULATION_SYSTEM,
                    location_ref=self.location_id,
                    status_flags={StatusFlag.ACTIVE},
                ),
            },
            locations={
                str(self.location_id): LocationRecord(
                    location_id=self.location_id,
                    display_name="Town",
                    region_ref=self.region_id,
                    location_type="settlement",
                )
            },
            regions={
                str(self.region_parent_id): RegionRecord(
                    region_id=self.region_parent_id,
                    display_name="Continent",
                ),
                str(self.region_id): RegionRecord(
                    region_id=self.region_id,
                    display_name="Heartlands",
                )
            },
            save_slots={
                str(self.save_id): SaveSlotMetaRecord(
                    save_slot_id=self.save_id,
                    save_label="Slot 1",
                    player_actor_ref=self.player_id,
                )
            },
        )

    def make_proposed_change(
        self,
        proposal_id: str,
        requested_mutations: tuple[RequestedMutation, ...],
        *,
        origin_type: ProposedChangeOrigin = ProposedChangeOrigin.SIMULATION_SYSTEM,
        intent_type: str = "test_intent",
        target_refs: tuple[TargetSelector, ...] = (),
        origin_actor_id=None,
    ) -> ProposedChange:
        return ProposedChange(
            proposal_id=proposal_id,
            origin_type=origin_type,
            intent_type=intent_type,
            target_refs=target_refs,
            requested_changes=requested_mutations,
            submitted_at="2026-04-10T10:00:00Z",
            origin_actor_id=origin_actor_id,
        )

    def test_legal_surface_helpers(self) -> None:
        self.assertTrue(is_legal_target_kind(TargetKind.ACTOR))
        self.assertTrue(is_legal_mutation_kind(MutationKind.SET_VALUE))
        self.assertTrue(is_legal_status_flag(StatusFlag.ACTIVE))
        self.assertTrue(is_legal_slot_key(SlotKey.DISPLAY_NAME))
        self.assertTrue(
            is_legal_slot_for_target(TargetKind.ACTOR, SlotKey.DISPLAY_NAME)
        )
        self.assertFalse(
            is_legal_slot_for_target(TargetKind.REGION, SlotKey.LOCATION_REF)
        )

    def test_rejects_illegal_status_flag(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_1",
            (
                RequestedMutation(
                    change_id="change_1",
                    mutation_kind=MutationKind.SET_STATUS_FLAG,
                    target=TargetSelector(TargetKind.ACTOR, str(self.player_id)),
                    arguments={
                        "slot_key": SlotKey.STATUS_FLAG.value,
                        "flag_name": "illegal_flag",
                        "flag_value": True,
                    },
                ),
            ),
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="status_update",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.player_id)),),
            origin_actor_id=self.player_id,
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal status flag" in message for message in result.diagnostics))

    def test_rejects_illegal_slot_for_target(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_2",
            (
                RequestedMutation(
                    change_id="change_2",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.REGION, str(self.region_id)),
                    arguments={
                        "slot_key": SlotKey.LOCATION_REF.value,
                        "value": str(self.location_id),
                    },
                ),
            ),
            intent_type="bad_slot",
            target_refs=(TargetSelector(TargetKind.REGION, str(self.region_id)),),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal slot" in message for message in result.diagnostics))

    def test_processes_valid_set_value_change(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_3",
            (
                RequestedMutation(
                    change_id="change_3",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, str(self.player_id)),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "Renamed Player",
                    },
                ),
            ),
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="rename_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.player_id)),),
            origin_actor_id=self.player_id,
        )

        updated_state, events, diagnostics = process_proposed_change(
            self.state_root,
            proposed_change,
        )

        self.assertEqual(updated_state.actors[str(self.player_id)].display_name, "Renamed Player")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].payload["approved_change_count"], 1)
        self.assertIn("accepted", diagnostics[0].lower())

    def test_processes_valid_set_status_flag_change(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_4",
            (
                RequestedMutation(
                    change_id="change_4",
                    mutation_kind=MutationKind.SET_STATUS_FLAG,
                    target=TargetSelector(TargetKind.ACTOR, str(self.npc_id)),
                    arguments={
                        "slot_key": SlotKey.STATUS_FLAG.value,
                        "flag_name": StatusFlag.DISABLED.value,
                        "flag_value": True,
                    },
                ),
            ),
            intent_type="disable_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.npc_id)),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)

        self.assertIn(
            StatusFlag.DISABLED,
            updated_state.actors[str(self.npc_id)].status_flags,
        )
        self.assertEqual(len(events), 1)

    def test_processes_valid_create_record_change(self) -> None:
        new_actor_id = make_actor_id("new_npc")
        proposed_change = self.make_proposed_change(
            "proposal_5",
            (
                RequestedMutation(
                    change_id="change_5",
                    mutation_kind=MutationKind.CREATE_RECORD,
                    target=TargetSelector(TargetKind.ACTOR),
                    arguments={
                        "record_kind": TargetKind.ACTOR.value,
                        "new_id": str(new_actor_id),
                        "initial_slots": {
                            SlotKey.DISPLAY_NAME.value: "New Npc",
                            SlotKey.ACTOR_SPECIALIZATION.value: ActorSpecialization.NPC.value,
                            SlotKey.AGENCY_SOURCE.value: AgencySource.SIMULATION_SYSTEM.value,
                        },
                    },
                ),
            ),
            intent_type="create_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)

        self.assertIn(str(new_actor_id), updated_state.actors)
        self.assertEqual(updated_state.actors[str(new_actor_id)].display_name, "New Npc")
        self.assertEqual(len(events), 1)

    def test_rejects_illegal_create_record_kind(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_6",
            (
                RequestedMutation(
                    change_id="change_6",
                    mutation_kind=MutationKind.CREATE_RECORD,
                    target=TargetSelector(TargetKind.ACTOR),
                    arguments={
                        "record_kind": "world_root",
                        "new_id": str(make_actor_id("bad_actor")),
                        "initial_slots": {},
                    },
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal create_record record_kind" in message for message in result.diagnostics))

    def test_rejects_non_create_mutation_without_record_id(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_7",
            (
                RequestedMutation(
                    change_id="change_7",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "No Target",
                    },
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertIn("Non-create mutations require a target record_id.", result.diagnostics)

    def test_rejects_set_status_flag_for_non_actor_target(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_8",
            (
                RequestedMutation(
                    change_id="change_8",
                    mutation_kind=MutationKind.SET_STATUS_FLAG,
                    target=TargetSelector(TargetKind.LOCATION, str(self.location_id)),
                    arguments={
                        "slot_key": SlotKey.STATUS_FLAG.value,
                        "flag_name": StatusFlag.ACTIVE.value,
                        "flag_value": True,
                    },
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("only legal for actor targets" in message for message in result.diagnostics))

    def test_rejects_illegal_initial_slot_in_create_record(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_9",
            (
                RequestedMutation(
                    change_id="change_9",
                    mutation_kind=MutationKind.CREATE_RECORD,
                    target=TargetSelector(TargetKind.ACTOR),
                    arguments={
                        "record_kind": TargetKind.ACTOR.value,
                        "new_id": str(make_actor_id("bad_slot_actor")),
                        "initial_slots": {
                            SlotKey.WORLD_TIME.value: "2026-04-10T11:00:00Z",
                        },
                    },
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal slot world_time" in message for message in result.diagnostics))

    def test_rejects_illegal_mutation_kind(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_10",
            (
                RequestedMutation(
                    change_id="change_10",
                    mutation_kind="destroy_record",  # type: ignore[arg-type]
                    target=TargetSelector(TargetKind.ACTOR, str(self.player_id)),
                    arguments={},
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal mutation kind" in message for message in result.diagnostics))

    def test_rejects_illegal_target_kind(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_11",
            (
                RequestedMutation(
                    change_id="change_11",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector("inventory", str(self.player_id)),  # type: ignore[arg-type]
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "Still Player",
                    },
                ),
            ),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Illegal target kind" in message for message in result.diagnostics))

    def test_rejects_batch_all_or_nothing_when_one_mutation_is_invalid(self) -> None:
        original_name = self.state_root.actors[str(self.player_id)].display_name
        proposed_change = self.make_proposed_change(
            "proposal_12",
            (
                RequestedMutation(
                    change_id="change_12a",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, str(self.player_id)),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "Would Have Changed",
                    },
                ),
                RequestedMutation(
                    change_id="change_12b",
                    mutation_kind=MutationKind.SET_STATUS_FLAG,
                    target=TargetSelector(TargetKind.ACTOR, str(self.player_id)),
                    arguments={
                        "slot_key": SlotKey.STATUS_FLAG.value,
                        "flag_name": "not_real",
                        "flag_value": True,
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.player_id)),),
        )

        validation = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(validation.status, ValidationStatus.REJECTED)
        self.assertEqual(validation.approved_mutations, ())
        self.assertTrue(any("all-or-nothing" in message for message in validation.diagnostics))

        updated_state, events, diagnostics = process_proposed_change(
            self.state_root,
            proposed_change,
        )
        self.assertEqual(updated_state.actors[str(self.player_id)].display_name, original_name)
        self.assertEqual(events, ())
        self.assertTrue(any("all-or-nothing" in message for message in diagnostics))

    def test_processes_valid_actor_phase2_value_field_mutations(self) -> None:
        cases = (
            (SlotKey.ORIGIN_ARCHETYPE, "village_guard", "origin_archetype"),
            (SlotKey.CATEGORY_OR_ROLE, "guard", "category_or_role"),
            (SlotKey.PRIORITY_TIER, "major_character", "priority_tier"),
        )

        for index, (slot_key, value, attribute_name) in enumerate(cases, start=1):
            with self.subTest(slot_key=slot_key.value):
                proposed_change = self.make_proposed_change(
                    f"proposal_phase2_value_{index}",
                    (
                        RequestedMutation(
                            change_id=f"change_phase2_value_{index}",
                            mutation_kind=MutationKind.SET_VALUE,
                            target=TargetSelector(TargetKind.ACTOR, str(self.npc_id)),
                            arguments={
                                "slot_key": slot_key.value,
                                "value": value,
                            },
                        ),
                    ),
                    target_refs=(TargetSelector(TargetKind.ACTOR, str(self.npc_id)),),
                )

                updated_state, events, _ = process_proposed_change(
                    self.state_root,
                    proposed_change,
                )

                self.assertEqual(
                    getattr(updated_state.actors[str(self.npc_id)], attribute_name),
                    value,
                )
                self.assertEqual(len(events), 1)

    def test_processes_valid_actor_inventory_ref_mutation(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_phase2_inventory_ref",
            (
                RequestedMutation(
                    change_id="change_phase2_inventory_ref",
                    mutation_kind=MutationKind.SET_REFERENCE,
                    target=TargetSelector(TargetKind.ACTOR, str(self.npc_id)),
                    arguments={
                        "slot_key": SlotKey.INVENTORY_REF.value,
                        "ref_id": "inventory_npc_main",
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.npc_id)),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)
        self.assertEqual(
            updated_state.actors[str(self.npc_id)].inventory_ref,
            "inventory_npc_main",
        )
        self.assertEqual(len(events), 1)

    def test_processes_valid_actor_faction_link_ref_mutation(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_phase2_faction_link",
            (
                RequestedMutation(
                    change_id="change_phase2_faction_link",
                    mutation_kind=MutationKind.ADD_REFERENCE,
                    target=TargetSelector(TargetKind.ACTOR, str(self.npc_id)),
                    arguments={
                        "slot_key": SlotKey.FACTION_LINK_REF.value,
                        "ref_id": "faction_city_watch",
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.ACTOR, str(self.npc_id)),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)
        self.assertIn(
            "faction_city_watch",
            updated_state.actors[str(self.npc_id)].faction_link_refs,
        )
        self.assertEqual(len(events), 1)

    def test_processes_valid_world_root_active_faction_ref_mutation(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_phase2_active_faction",
            (
                RequestedMutation(
                    change_id="change_phase2_active_faction",
                    mutation_kind=MutationKind.ADD_REFERENCE,
                    target=TargetSelector(TargetKind.WORLD_ROOT, "world_root"),
                    arguments={
                        "slot_key": SlotKey.ACTIVE_FACTION_REF.value,
                        "ref_id": "faction_city_watch",
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.WORLD_ROOT, "world_root"),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)
        self.assertIn("faction_city_watch", updated_state.world_root.active_faction_refs)
        self.assertEqual(len(events), 1)

    def test_processes_valid_region_parent_ref_mutation(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_phase2_region_parent",
            (
                RequestedMutation(
                    change_id="change_phase2_region_parent",
                    mutation_kind=MutationKind.SET_REFERENCE,
                    target=TargetSelector(TargetKind.REGION, str(self.region_id)),
                    arguments={
                        "slot_key": SlotKey.REGION_PARENT_REF.value,
                        "ref_id": str(self.region_parent_id),
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.REGION, str(self.region_id)),),
        )

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)
        self.assertEqual(
            updated_state.regions[str(self.region_id)].region_parent_ref,
            str(self.region_parent_id),
        )
        self.assertEqual(len(events), 1)

    def test_rejects_unknown_region_parent_ref_mutation(self) -> None:
        proposed_change = self.make_proposed_change(
            "proposal_phase2_bad_region_parent",
            (
                RequestedMutation(
                    change_id="change_phase2_bad_region_parent",
                    mutation_kind=MutationKind.SET_REFERENCE,
                    target=TargetSelector(TargetKind.REGION, str(self.region_id)),
                    arguments={
                        "slot_key": SlotKey.REGION_PARENT_REF.value,
                        "ref_id": str(make_region_id("missing_parent")),
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.REGION, str(self.region_id)),),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(
            any("Unknown region parent reference" in message for message in result.diagnostics)
        )

    def test_processes_valid_region_world_space_ref_mutation(self) -> None:
        world_space_id = make_world_space_id("primary")
        self.state_root.world_spaces[str(world_space_id)] = WorldSpaceRecord(
            world_space_id=world_space_id,
            sea_level_z=0.0,
        )

        proposed_change = self.make_proposed_change(
            "proposal_map_region_world_space",
            (
                RequestedMutation(
                    change_id="change_map_region_world_space",
                    mutation_kind=MutationKind.SET_REFERENCE,
                    target=TargetSelector(TargetKind.REGION, str(self.region_id)),
                    arguments={
                        "slot_key": SlotKey.WORLD_SPACE_REF.value,
                        "ref_id": str(world_space_id),
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.REGION, str(self.region_id)),),
        )

        validation = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(validation.status, ValidationStatus.ACCEPTED)

        updated_state, events, _ = process_proposed_change(self.state_root, proposed_change)
        self.assertEqual(
            updated_state.regions[str(self.region_id)].world_space_ref,
            str(world_space_id),
        )
        self.assertEqual(len(events), 1)

    def test_rejects_unknown_region_world_space_ref_mutation(self) -> None:
        unknown_world_space_id = make_world_space_id("missing_world_space")
        proposed_change = self.make_proposed_change(
            "proposal_map_bad_region_world_space",
            (
                RequestedMutation(
                    change_id="change_map_bad_region_world_space",
                    mutation_kind=MutationKind.SET_REFERENCE,
                    target=TargetSelector(TargetKind.REGION, str(self.region_id)),
                    arguments={
                        "slot_key": SlotKey.WORLD_SPACE_REF.value,
                        "ref_id": str(unknown_world_space_id),
                    },
                ),
            ),
            target_refs=(TargetSelector(TargetKind.REGION, str(self.region_id)),),
        )

        result = validate_proposed_change(proposed_change, self.state_root)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertEqual(result.approved_mutations, ())
        self.assertTrue(
            any("Unknown world space reference" in message for message in result.diagnostics)
        )

        original_world_space_ref = self.state_root.regions[str(self.region_id)].world_space_ref
        updated_state, events, diagnostics = process_proposed_change(
            self.state_root,
            proposed_change,
        )
        self.assertEqual(
            updated_state.regions[str(self.region_id)].world_space_ref,
            original_world_space_ref,
        )
        self.assertEqual(events, ())
        self.assertTrue(
            any("Unknown world space reference" in message for message in diagnostics)
        )

    def test_rejects_illegal_phase2_target_slot_combinations(self) -> None:
        cases = (
            (
                TargetKind.WORLD_ROOT,
                "world_root",
                MutationKind.SET_VALUE,
                SlotKey.PRIORITY_TIER,
                "major_character",
            ),
            (
                TargetKind.REGION,
                str(self.region_id),
                MutationKind.ADD_REFERENCE,
                SlotKey.ACTIVE_FACTION_REF,
                "faction_city_watch",
            ),
        )

        for index, (target_kind, record_id, mutation_kind, slot_key, payload_value) in enumerate(cases, start=1):
            with self.subTest(slot_key=slot_key.value, target_kind=target_kind.value):
                arguments = {
                    "slot_key": slot_key.value,
                    "value": payload_value,
                }
                if mutation_kind is MutationKind.ADD_REFERENCE:
                    arguments = {
                        "slot_key": slot_key.value,
                        "ref_id": payload_value,
                    }

                proposed_change = self.make_proposed_change(
                    f"proposal_phase2_illegal_slot_{index}",
                    (
                        RequestedMutation(
                            change_id=f"change_phase2_illegal_slot_{index}",
                            mutation_kind=mutation_kind,
                            target=TargetSelector(target_kind, record_id),
                            arguments=arguments,
                        ),
                    ),
                )

                result = validate_proposed_change(proposed_change, self.state_root)
                self.assertEqual(result.status, ValidationStatus.REJECTED)
                self.assertTrue(any("Illegal slot" in message for message in result.diagnostics))

    def test_supports_map_mvp_record_fields_with_world_space_and_hidden_location(self) -> None:
        world_space_id = make_world_space_id("primary")
        hidden_location_id = make_location_id("hidden_shrine")
        region = RegionRecord(
            region_id=self.region_id,
            world_space_ref=world_space_id,
            display_name="Heartlands",
        )
        hidden_location = LocationRecord(
            location_id=hidden_location_id,
            display_name="Sunken Shrine",
            region_ref=self.region_id,
            location_type="ruin",
            x=125.5,
            y=340.25,
            z=-2.0,
            biome="swamp",
            is_hidden_by_default=True,
        )

        self.state_root.world_spaces[str(world_space_id)] = WorldSpaceRecord(
            world_space_id=world_space_id,
            sea_level_z=0.0,
        )
        self.state_root.regions[str(self.region_id)] = region
        self.state_root.locations[str(hidden_location_id)] = hidden_location

        self.assertIn(str(world_space_id), self.state_root.world_spaces)
        self.assertEqual(
            self.state_root.world_spaces[str(world_space_id)].sea_level_z,
            0.0,
        )
        self.assertEqual(
            self.state_root.regions[str(self.region_id)].world_space_ref,
            world_space_id,
        )
        self.assertEqual(hidden_location.x, 125.5)
        self.assertEqual(hidden_location.y, 340.25)
        self.assertEqual(hidden_location.z, -2.0)
        self.assertEqual(hidden_location.biome, "swamp")
        self.assertTrue(hidden_location.is_hidden_by_default)
        self.assertEqual(
            self.state_root.actors[str(self.player_id)].location_ref,
            self.location_id,
        )

    def test_stores_player_map_discovery_entry_for_canonical_location(self) -> None:
        discovery_entry = MapDiscoveryEntry(
            location_ref=self.location_id,
            is_revealed=True,
            is_name_revealed=False,
            is_marker_visible=False,
            is_visited=False,
        )
        self.state_root.player_map_discovery[str(self.location_id)] = discovery_entry

        stored_entry = self.state_root.player_map_discovery[str(self.location_id)]
        canonical_location = self.state_root.locations[str(self.location_id)]

        self.assertEqual(stored_entry.location_ref, self.location_id)
        self.assertTrue(stored_entry.is_revealed)
        self.assertFalse(stored_entry.is_name_revealed)
        self.assertFalse(stored_entry.is_marker_visible)
        self.assertFalse(stored_entry.is_visited)
        self.assertEqual(canonical_location.display_name, "Town")
        self.assertEqual(canonical_location.location_type, "settlement")
        self.assertFalse(hasattr(stored_entry, "display_name"))
        self.assertFalse(hasattr(stored_entry, "location_type"))

    def test_builds_player_location_discovery_read_model_with_and_without_entry(self) -> None:
        hidden_location_id = make_location_id("hidden_archive")
        self.state_root.locations[str(hidden_location_id)] = LocationRecord(
            location_id=hidden_location_id,
            display_name="Hidden Archive",
            location_type="ruin",
            is_hidden_by_default=True,
        )

        no_discovery_entry_view = build_player_location_discovery_read_model(
            location_ref=hidden_location_id,
            canonical_location=self.state_root.locations[str(hidden_location_id)],
            discovery_entry=self.state_root.player_map_discovery.get(str(hidden_location_id)),
        )
        self.assertTrue(no_discovery_entry_view["canonically_present"])
        self.assertTrue(no_discovery_entry_view["hidden_by_default"])
        self.assertFalse(no_discovery_entry_view["is_revealed"])
        self.assertFalse(no_discovery_entry_view["is_name_revealed"])
        self.assertFalse(no_discovery_entry_view["is_marker_visible"])
        self.assertFalse(no_discovery_entry_view["is_visited"])
        self.assertNotIn("display_name", no_discovery_entry_view)

        self.state_root.player_map_discovery[str(hidden_location_id)] = MapDiscoveryEntry(
            location_ref=hidden_location_id,
            is_revealed=True,
            is_name_revealed=True,
            is_marker_visible=True,
            is_visited=False,
        )

        with_discovery_entry_view = build_player_location_discovery_read_model(
            location_ref=hidden_location_id,
            canonical_location=self.state_root.locations[str(hidden_location_id)],
            discovery_entry=self.state_root.player_map_discovery[str(hidden_location_id)],
        )
        self.assertTrue(with_discovery_entry_view["canonically_present"])
        self.assertTrue(with_discovery_entry_view["hidden_by_default"])
        self.assertTrue(with_discovery_entry_view["is_revealed"])
        self.assertTrue(with_discovery_entry_view["is_name_revealed"])
        self.assertTrue(with_discovery_entry_view["is_marker_visible"])
        self.assertFalse(with_discovery_entry_view["is_visited"])
        self.assertNotIn("display_name", with_discovery_entry_view)

    def test_reveal_player_location_creates_discovery_entry_and_preserves_canonical_location(self) -> None:
        hidden_location_id = make_location_id("hidden_vault")
        self.state_root.locations[str(hidden_location_id)] = LocationRecord(
            location_id=hidden_location_id,
            display_name="Hidden Vault",
            location_type="ruin",
            is_hidden_by_default=True,
        )

        reveal_player_location(self.state_root, hidden_location_id)

        discovery_entry = self.state_root.player_map_discovery[str(hidden_location_id)]
        canonical_location = self.state_root.locations[str(hidden_location_id)]
        self.assertEqual(discovery_entry.location_ref, hidden_location_id)
        self.assertTrue(discovery_entry.is_revealed)
        self.assertFalse(discovery_entry.is_name_revealed)
        self.assertFalse(discovery_entry.is_marker_visible)
        self.assertFalse(discovery_entry.is_visited)
        self.assertEqual(canonical_location.display_name, "Hidden Vault")
        self.assertEqual(canonical_location.location_type, "ruin")
        self.assertTrue(canonical_location.is_hidden_by_default)

    def test_reveal_player_location_rejects_unknown_location_ref(self) -> None:
        unknown_location_id = make_location_id("missing_location")

        with self.assertRaises(ValueError):
            reveal_player_location(self.state_root, unknown_location_id)

        self.assertEqual(self.state_root.player_map_discovery, {})

    def test_reveal_player_location_name_creates_or_updates_name_reveal_and_preserves_other_fields(self) -> None:
        hidden_location_id = make_location_id("named_hidden_vault")
        self.state_root.locations[str(hidden_location_id)] = LocationRecord(
            location_id=hidden_location_id,
            display_name="Named Hidden Vault",
            location_type="ruin",
            is_hidden_by_default=True,
        )

        reveal_player_location_name(self.state_root, hidden_location_id)

        created_entry = self.state_root.player_map_discovery[str(hidden_location_id)]
        canonical_location = self.state_root.locations[str(hidden_location_id)]
        self.assertEqual(created_entry.location_ref, hidden_location_id)
        self.assertTrue(created_entry.is_revealed)
        self.assertTrue(created_entry.is_name_revealed)
        self.assertFalse(created_entry.is_marker_visible)
        self.assertFalse(created_entry.is_visited)
        self.assertEqual(canonical_location.display_name, "Named Hidden Vault")
        self.assertEqual(canonical_location.location_type, "ruin")
        self.assertTrue(canonical_location.is_hidden_by_default)

        self.state_root.player_map_discovery[str(hidden_location_id)] = MapDiscoveryEntry(
            location_ref=hidden_location_id,
            is_revealed=False,
            is_name_revealed=False,
            is_marker_visible=True,
            is_visited=True,
        )

        reveal_player_location_name(self.state_root, hidden_location_id)

        updated_entry = self.state_root.player_map_discovery[str(hidden_location_id)]
        self.assertTrue(updated_entry.is_revealed)
        self.assertTrue(updated_entry.is_name_revealed)
        self.assertTrue(updated_entry.is_marker_visible)
        self.assertTrue(updated_entry.is_visited)

    def test_reveal_player_location_name_rejects_unknown_location_ref(self) -> None:
        unknown_location_id = make_location_id("missing_named_location")

        with self.assertRaises(ValueError):
            reveal_player_location_name(self.state_root, unknown_location_id)

        self.assertEqual(self.state_root.player_map_discovery, {})

    def test_mark_player_location_visited_sets_visit_reveal_and_preserves_marker_visibility(self) -> None:
        hidden_location_id = make_location_id("visited_hidden_vault")
        self.state_root.locations[str(hidden_location_id)] = LocationRecord(
            location_id=hidden_location_id,
            display_name="Visited Hidden Vault",
            location_type="ruin",
            is_hidden_by_default=True,
        )
        self.state_root.player_map_discovery[str(hidden_location_id)] = MapDiscoveryEntry(
            location_ref=hidden_location_id,
            is_revealed=False,
            is_name_revealed=False,
            is_marker_visible=True,
            is_visited=False,
        )

        mark_player_location_visited(self.state_root, hidden_location_id)

        discovery_entry = self.state_root.player_map_discovery[str(hidden_location_id)]
        canonical_location = self.state_root.locations[str(hidden_location_id)]
        self.assertTrue(discovery_entry.is_revealed)
        self.assertTrue(discovery_entry.is_name_revealed)
        self.assertTrue(discovery_entry.is_visited)
        self.assertTrue(discovery_entry.is_marker_visible)
        self.assertEqual(canonical_location.display_name, "Visited Hidden Vault")
        self.assertEqual(canonical_location.location_type, "ruin")
        self.assertTrue(canonical_location.is_hidden_by_default)

    def test_mark_player_location_visited_rejects_unknown_location_ref(self) -> None:
        unknown_location_id = make_location_id("missing_visited_location")

        with self.assertRaises(ValueError):
            mark_player_location_visited(self.state_root, unknown_location_id)

        self.assertEqual(self.state_root.player_map_discovery, {})


if __name__ == "__main__":
    unittest.main()
