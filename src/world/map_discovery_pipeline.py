from __future__ import annotations

import uuid
from datetime import datetime, timezone

from src.core.contracts import (
    AuthoritativeEvent,
    EventCategory,
    EventHandoff,
    MutationKind,
    ProposedChange,
    ProposedChangeOrigin,
    RequestedMutation,
    SlotKey,
    TargetKind,
    TargetSelector,
)
from src.core.ids import ActorId, LocationId
from src.core.runtime import process_proposed_change
from src.core.state_root import StateRoot


def _utc_timestamp() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _discovery_handoff(intent_type: str, location_key: str) -> EventHandoff:
    return EventHandoff(
        category=EventCategory.WORLD,
        payload={"intent_type": intent_type, "location_ref": location_key},
        primary_subject_ref=location_key,
        related_refs=(),
        related_advisory_ref=None,
    )


def reveal_player_location_through_runtime(
    state_root: StateRoot,
    location_ref: LocationId,
    *,
    proposal_id: str | None = None,
    submitted_at: str | None = None,
    origin_type: ProposedChangeOrigin = ProposedChangeOrigin.SIMULATION_SYSTEM,
    origin_actor_id: ActorId | None = None,
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    loc_key = str(location_ref)
    pid = proposal_id or f"map_discovery_reveal_{uuid.uuid4().hex[:12]}"
    ts = submitted_at or _utc_timestamp()
    proposed = ProposedChange(
        proposal_id=pid,
        origin_type=origin_type,
        intent_type="map_discovery.reveal_location",
        target_refs=(TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),),
        requested_changes=(
            RequestedMutation(
                change_id=f"{pid}_c1",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_REVEALED.value,
                    "value": True,
                },
            ),
        ),
        submitted_at=ts,
        origin_actor_id=origin_actor_id,
    )
    return process_proposed_change(
        state_root,
        proposed,
        event_suffix_prefix="map_discovery",
        event_handoff_override=(_discovery_handoff("map_discovery.reveal_location", loc_key),),
    )


def reveal_player_location_name_through_runtime(
    state_root: StateRoot,
    location_ref: LocationId,
    *,
    proposal_id: str | None = None,
    submitted_at: str | None = None,
    origin_type: ProposedChangeOrigin = ProposedChangeOrigin.SIMULATION_SYSTEM,
    origin_actor_id: ActorId | None = None,
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    loc_key = str(location_ref)
    pid = proposal_id or f"map_discovery_reveal_name_{uuid.uuid4().hex[:12]}"
    ts = submitted_at or _utc_timestamp()
    proposed = ProposedChange(
        proposal_id=pid,
        origin_type=origin_type,
        intent_type="map_discovery.reveal_location_name",
        target_refs=(TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),),
        requested_changes=(
            RequestedMutation(
                change_id=f"{pid}_c1",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_REVEALED.value,
                    "value": True,
                },
            ),
            RequestedMutation(
                change_id=f"{pid}_c2",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_NAME_REVEALED.value,
                    "value": True,
                },
            ),
        ),
        submitted_at=ts,
        origin_actor_id=origin_actor_id,
    )
    return process_proposed_change(
        state_root,
        proposed,
        event_suffix_prefix="map_discovery",
        event_handoff_override=(_discovery_handoff("map_discovery.reveal_location_name", loc_key),),
    )


def mark_player_location_visited_through_runtime(
    state_root: StateRoot,
    location_ref: LocationId,
    *,
    proposal_id: str | None = None,
    submitted_at: str | None = None,
    origin_type: ProposedChangeOrigin = ProposedChangeOrigin.SIMULATION_SYSTEM,
    origin_actor_id: ActorId | None = None,
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    loc_key = str(location_ref)
    pid = proposal_id or f"map_discovery_visit_{uuid.uuid4().hex[:12]}"
    ts = submitted_at or _utc_timestamp()
    proposed = ProposedChange(
        proposal_id=pid,
        origin_type=origin_type,
        intent_type="map_discovery.mark_location_visited",
        target_refs=(TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),),
        requested_changes=(
            RequestedMutation(
                change_id=f"{pid}_c1",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_REVEALED.value,
                    "value": True,
                },
            ),
            RequestedMutation(
                change_id=f"{pid}_c2",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_NAME_REVEALED.value,
                    "value": True,
                },
            ),
            RequestedMutation(
                change_id=f"{pid}_c3",
                mutation_kind=MutationKind.SET_VALUE,
                target=TargetSelector(TargetKind.PLAYER_MAP_DISCOVERY, loc_key),
                arguments={
                    "slot_key": SlotKey.DISCOVERY_IS_VISITED.value,
                    "value": True,
                },
            ),
        ),
        submitted_at=ts,
        origin_actor_id=origin_actor_id,
    )
    return process_proposed_change(
        state_root,
        proposed,
        event_suffix_prefix="map_discovery",
        event_handoff_override=(_discovery_handoff("map_discovery.mark_location_visited", loc_key),),
    )
