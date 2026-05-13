from __future__ import annotations

import unittest

from src.core.contracts import (
    ActorSpecialization,
    AgencySource,
    EventCategory,
    MutationKind,
    ProposedChange,
    ProposedChangeOrigin,
    RequestedMutation,
    SlotKey,
    StatusFlag,
    TargetKind,
    TargetSelector,
)
from src.core.ids import make_actor_id, make_location_id, make_region_id, make_save_slot_id
from src.core.runtime import process_proposed_change
from src.core.state_root import SaveSlotMetaRecord, StateRoot
from src.npc.actor_baseline import ActorRecord
from src.persistence import (
    EventRepository,
    SnapshotRepository,
    load_state_from_save_snapshot_ref,
    open_persistence,
    process_proposed_change_persisted,
    process_rules_action_persisted,
    save_slot_checkpoint_snapshot,
)
from src.rules.contracts import RulesActionRequest
from src.world.world_state import LocationRecord, WorldRootRecord


class PersistencePhase1Tests(unittest.TestCase):
    def test_append_and_fetch_authoritative_event(self) -> None:
        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            from src.core.contracts import AuthoritativeEvent
            from src.core.ids import make_event_id

            event = AuthoritativeEvent(
                event_id=make_event_id("demo_1"),
                category=EventCategory.SYSTEM,
                occurred_at="2026-05-12T12:00:00Z",
                primary_subject_ref=None,
                related_refs=("actor_player",),
                payload={"approved_change_count": 1},
                schema_version=1,
            )
            repo.append_events((event,))
            loaded = repo.fetch_event_by_id(str(event.event_id))
            self.assertIsNotNone(loaded)
            assert loaded is not None
            self.assertEqual(loaded.event_id, event.event_id)
            self.assertEqual(loaded.category, event.category)
            self.assertEqual(loaded.payload, event.payload)
            listed = repo.list_events_ordered(limit=10)
            self.assertEqual(len(listed), 1)
        finally:
            backend.close()

    def test_event_repository_max_seq_empty(self) -> None:
        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            self.assertEqual(repo.max_seq(), 0)
        finally:
            backend.close()

    def test_process_proposed_change_persisted_appends(self) -> None:
        player_id = make_actor_id("player")
        location_id = make_location_id("town")
        region_id = make_region_id("heartlands")
        state_root = StateRoot(
            world_root=WorldRootRecord(),
            actors={
                str(player_id): ActorRecord(
                    actor_id=player_id,
                    display_name="Player",
                    actor_specialization=ActorSpecialization.PLAYER,
                    agency_source=AgencySource.HUMAN_PLAYER,
                    location_ref=location_id,
                    status_flags={StatusFlag.ACTIVE},
                )
            },
            locations={
                str(location_id): LocationRecord(
                    location_id=location_id,
                    display_name="Town",
                    region_ref=region_id,
                    location_type="settlement",
                )
            },
        )
        proposed_change = ProposedChange(
            proposal_id="p1",
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="rename_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(player_id)),),
            requested_changes=(
                RequestedMutation(
                    change_id="c1",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, str(player_id)),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "Renamed",
                    },
                ),
            ),
            submitted_at="2026-05-12T12:00:00Z",
            origin_actor_id=player_id,
        )
        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            updated, events, _ = process_proposed_change_persisted(backend, state_root, proposed_change)
            self.assertTrue(events)
            self.assertEqual(repo.max_seq(), len(events))
            for ev in events:
                self.assertIsNotNone(repo.fetch_event_by_id(str(ev.event_id)))
            self.assertEqual(updated.actors[str(player_id)].display_name, "Renamed")
        finally:
            backend.close()

    def test_process_proposed_change_persisted_rejection_does_not_append(self) -> None:
        bad_proposal = ProposedChange(
            proposal_id="bad",
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="rename_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, "actor_nobody"),),
            requested_changes=(
                RequestedMutation(
                    change_id="c1",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, "actor_nobody"),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "X",
                    },
                ),
            ),
            submitted_at="2026-05-12T12:00:00Z",
            origin_actor_id=make_actor_id("player"),
        )
        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            empty = StateRoot()
            updated, events, _ = process_proposed_change_persisted(backend, empty, bad_proposal)
            self.assertEqual(events, ())
            self.assertEqual(repo.max_seq(), 0)
            self.assertIs(updated, empty)
        finally:
            backend.close()

    def test_process_rules_action_persisted_appends(self) -> None:
        player_id = make_actor_id("hero")
        state_root = StateRoot(
            actors={
                str(player_id): ActorRecord(
                    actor_id=player_id,
                    display_name="Hero",
                )
            },
        )
        req = RulesActionRequest(
            request_id="r1",
            action_kind="set_actor_current_activity",
            actor_id=player_id,
            activity="resting",
        )
        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            updated, events, _ = process_rules_action_persisted(backend, state_root, req)
            self.assertTrue(events)
            self.assertEqual(repo.max_seq(), 1)
            self.assertEqual(updated.actors[str(player_id)].current_activity, "resting")
        finally:
            backend.close()

    def test_save_slot_checkpoint_snapshot_and_load(self) -> None:
        player_id = make_actor_id("p")
        save_id = make_save_slot_id("s1")
        save_key = str(save_id)
        location_id = make_location_id("loc")
        region_id = make_region_id("reg")
        state_root = StateRoot(
            save_slots={
                save_key: SaveSlotMetaRecord(
                    save_slot_id=save_id,
                    save_label="Slot A",
                    player_actor_ref=player_id,
                )
            },
            world_root=WorldRootRecord(),
            actors={
                str(player_id): ActorRecord(
                    actor_id=player_id,
                    display_name="Player",
                    actor_specialization=ActorSpecialization.PLAYER,
                    agency_source=AgencySource.HUMAN_PLAYER,
                    location_ref=location_id,
                    status_flags={StatusFlag.ACTIVE},
                )
            },
            locations={
                str(location_id): LocationRecord(
                    location_id=location_id,
                    display_name="Loc",
                    region_ref=region_id,
                    location_type="wilderness",
                )
            },
        )
        proposed_change = ProposedChange(
            proposal_id="p1",
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="rename_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(player_id)),),
            requested_changes=(
                RequestedMutation(
                    change_id="c1",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, str(player_id)),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "SavedName",
                    },
                ),
            ),
            submitted_at="2026-05-12T12:00:00Z",
            origin_actor_id=player_id,
        )
        backend = open_persistence()
        try:
            updated, events, _ = process_proposed_change_persisted(backend, state_root, proposed_change)
            self.assertTrue(events)
            new_state, snap_id = save_slot_checkpoint_snapshot(backend, updated, save_key)
            self.assertEqual(new_state.save_slots[save_key].world_snapshot_ref, snap_id)
            ev_repo = EventRepository(backend.connection)
            self.assertEqual(
                new_state.save_slots[save_key].event_checkpoint_ref,
                str(ev_repo.max_seq()),
            )
            loaded = load_state_from_save_snapshot_ref(backend, new_state, save_key)
            self.assertEqual(loaded.actors[str(player_id)].display_name, "SavedName")
            self.assertEqual(loaded.save_slots[save_key].world_snapshot_ref, snap_id)
        finally:
            backend.close()

    def test_process_proposed_change_events_round_trip_through_sqlite(self) -> None:
        player_id = make_actor_id("player")
        location_id = make_location_id("town")
        region_id = make_region_id("heartlands")
        state_root = StateRoot(
            world_root=WorldRootRecord(),
            actors={
                str(player_id): ActorRecord(
                    actor_id=player_id,
                    display_name="Player",
                    actor_specialization=ActorSpecialization.PLAYER,
                    agency_source=AgencySource.HUMAN_PLAYER,
                    location_ref=location_id,
                    status_flags={StatusFlag.ACTIVE},
                )
            },
            locations={
                str(location_id): LocationRecord(
                    location_id=location_id,
                    display_name="Town",
                    region_ref=region_id,
                    location_type="settlement",
                )
            },
        )
        proposed_change = ProposedChange(
            proposal_id="p1",
            origin_type=ProposedChangeOrigin.PLAYER_INPUT,
            intent_type="rename_actor",
            target_refs=(TargetSelector(TargetKind.ACTOR, str(player_id)),),
            requested_changes=(
                RequestedMutation(
                    change_id="c1",
                    mutation_kind=MutationKind.SET_VALUE,
                    target=TargetSelector(TargetKind.ACTOR, str(player_id)),
                    arguments={
                        "slot_key": SlotKey.DISPLAY_NAME.value,
                        "value": "Renamed",
                    },
                ),
            ),
            submitted_at="2026-05-12T12:00:00Z",
            origin_actor_id=player_id,
        )
        updated, events, _ = process_proposed_change(state_root, proposed_change)

        backend = open_persistence()
        try:
            repo = EventRepository(backend.connection)
            repo.append_events(events)
            for ev in events:
                loaded = repo.fetch_event_by_id(str(ev.event_id))
                self.assertIsNotNone(loaded)
                assert loaded is not None
                self.assertEqual(loaded.category, ev.category)
                self.assertEqual(loaded.payload, ev.payload)
        finally:
            backend.close()

        self.assertEqual(updated.actors[str(player_id)].display_name, "Renamed")

    def test_state_snapshot_round_trip(self) -> None:
        player_id = make_actor_id("p")
        save_id = make_save_slot_id("s1")
        state = StateRoot(
            save_slots={
                str(save_id): SaveSlotMetaRecord(
                    save_slot_id=save_id,
                    save_label="Slot A",
                    player_actor_ref=player_id,
                )
            }
        )
        backend = open_persistence()
        try:
            snaps = SnapshotRepository(backend.connection)
            sid = snaps.save_snapshot(state)
            restored = snaps.load_snapshot(sid)
            self.assertEqual(restored.save_slots[str(save_id)].save_label, "Slot A")
            self.assertEqual(
                str(restored.save_slots[str(save_id)].player_actor_ref),
                str(player_id),
            )
        finally:
            backend.close()


if __name__ == "__main__":
    unittest.main()
