from __future__ import annotations

from src.core.contracts import (
    AuthoritativeEvent,
    EventHandoff,
    ProposedChange,
    ValidationStatus,
)
from src.core.state_root import StateRoot
from src.core.transition_validation import (
    apply_approved_mutations,
    validate_proposed_change,
)
from src.events.event_envelope import build_authoritative_event


def process_proposed_change(
    state_root: StateRoot,
    proposed_change: ProposedChange,
    event_suffix_prefix: str = "core",
    event_handoff_override: tuple[EventHandoff, ...] | None = None,
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    validation_result = validate_proposed_change(proposed_change, state_root)
    if validation_result.status is ValidationStatus.REJECTED:
        return state_root, (), validation_result.diagnostics

    updated_state = apply_approved_mutations(
        state_root,
        validation_result.approved_mutations,
    )
    handoffs = (
        event_handoff_override
        if event_handoff_override is not None
        else validation_result.event_handoffs
    )
    events = tuple(
        build_authoritative_event(
            handoff=handoff,
            event_suffix=f"{event_suffix_prefix}_{index}",
            occurred_at=proposed_change.submitted_at,
        )
        for index, handoff in enumerate(handoffs, start=1)
    )
    return updated_state, events, validation_result.diagnostics
