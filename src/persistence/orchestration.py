from __future__ import annotations

import uuid
from dataclasses import replace

from src.core.contracts import (
    AuthoritativeEvent,
    EventHandoff,
    ProposedChange,
)
from src.core.runtime import process_proposed_change
from src.core.state_root import StateRoot
from src.persistence.event_repository import EventRepository
from src.persistence.snapshot_repository import SnapshotRepository
from src.persistence.sqlite_backend import PersistenceBackend
from src.rules.boundary import process_rules_action
from src.rules.contracts import RulesActionRequest


def process_proposed_change_persisted(
    backend: PersistenceBackend,
    state_root: StateRoot,
    proposed_change: ProposedChange,
    *,
    event_suffix_prefix: str = "core",
    event_handoff_override: tuple[EventHandoff, ...] | None = None,
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    """
    Run ``process_proposed_change`` and append emitted events to SQLite when non-empty.

    Rejected proposals emit no events; nothing is written to the log.
    """
    updated, events, diagnostics = process_proposed_change(
        state_root,
        proposed_change,
        event_suffix_prefix=event_suffix_prefix,
        event_handoff_override=event_handoff_override,
    )
    if events:
        EventRepository(backend.connection).append_events(events)
    return updated, events, diagnostics


def process_rules_action_persisted(
    backend: PersistenceBackend,
    state_root: StateRoot,
    action_request: RulesActionRequest,
    *,
    event_suffix_prefix: str = "rules",
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    """Run ``process_rules_action`` and append emitted events when non-empty."""
    updated, events, diagnostics = process_rules_action(
        state_root,
        action_request,
        event_suffix_prefix=event_suffix_prefix,
    )
    if events:
        EventRepository(backend.connection).append_events(events)
    return updated, events, diagnostics


def save_slot_checkpoint_snapshot(
    backend: PersistenceBackend,
    state_root: StateRoot,
    save_slot_key: str,
    *,
    created_at: str | None = None,
) -> tuple[StateRoot, str]:
    """
    Persist ``state_root`` with save-slot linkage fields set in one snapshot row.

    ``event_checkpoint_ref`` is the current tail ``authoritative_events.seq`` (string).
    ``world_snapshot_ref`` matches the new snapshot row id so restored state is self-consistent.
    """
    if save_slot_key not in state_root.save_slots:
        raise KeyError(f"Unknown save slot key: {save_slot_key!r}")
    events_repo = EventRepository(backend.connection)
    checkpoint = str(events_repo.max_seq())
    snapshot_id = f"snap_{uuid.uuid4().hex}"
    slot = state_root.save_slots[save_slot_key]
    new_slot = replace(
        slot,
        world_snapshot_ref=snapshot_id,
        event_checkpoint_ref=checkpoint,
    )
    new_state = replace(state_root, save_slots={**state_root.save_slots, save_slot_key: new_slot})
    SnapshotRepository(backend.connection).save_snapshot(
        new_state,
        created_at=created_at,
        snapshot_id=snapshot_id,
    )
    return new_state, snapshot_id


def load_state_from_save_snapshot_ref(
    backend: PersistenceBackend,
    state_root: StateRoot,
    save_slot_key: str,
) -> StateRoot:
    """Load ``StateRoot`` from ``world_snapshot_ref`` on the given save slot."""
    if save_slot_key not in state_root.save_slots:
        raise KeyError(f"Unknown save slot key: {save_slot_key!r}")
    ref = state_root.save_slots[save_slot_key].world_snapshot_ref
    if not ref:
        raise ValueError(f"Save slot {save_slot_key!r} has no world_snapshot_ref.")
    return SnapshotRepository(backend.connection).load_snapshot(ref)
