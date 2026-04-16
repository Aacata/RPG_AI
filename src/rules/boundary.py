from __future__ import annotations

from datetime import datetime, timezone

from src.core.contracts import (
    EventCategory,
    EventHandoff,
    MutationKind,
    ProposedChange,
    ProposedChangeOrigin,
    RequestedMutation,
    SlotKey,
    TargetKind,
    TargetSelector,
    ValidationStatus,
)
from src.core.runtime import AuthoritativeEvent
from src.core.state_root import StateRoot
from src.core.transition_validation import (
    apply_approved_mutations,
    validate_proposed_change,
)
from src.events.event_envelope import build_authoritative_event
from src.rules.contracts import RulesActionRequest, RulesInspectionResult


def inspect_rules_action(
    state_root: StateRoot,
    action_request: RulesActionRequest,
) -> RulesInspectionResult:
    if action_request.action_kind != "set_actor_current_activity":
        raise ValueError("Unsupported action_kind for Phase 3 MVP.")

    actor_id = str(action_request.actor_id)
    if actor_id not in state_root.actors:
        return RulesInspectionResult(
            status="rejected",
            diagnostics=("Unknown actor reference.",),
            proposed_change=None,
            event_handoff=None,
        )

    if not isinstance(action_request.activity, str) or not action_request.activity.strip():
        return RulesInspectionResult(
            status="rejected",
            diagnostics=("Activity must be a non-empty string.",),
            proposed_change=None,
            event_handoff=None,
        )

    target = TargetSelector(kind=TargetKind.ACTOR, record_id=actor_id)
    proposed_change = ProposedChange(
        proposal_id=action_request.request_id,
        origin_type=ProposedChangeOrigin.SIMULATION_SYSTEM,
        intent_type="rules.set_actor_current_activity",
        target_refs=(target,),
        requested_changes=(
            RequestedMutation(
                change_id=action_request.request_id,
                mutation_kind=MutationKind.SET_VALUE,
                target=target,
                arguments={
                    "slot_key": SlotKey.CURRENT_ACTIVITY.value,
                    "value": action_request.activity,
                },
                preconditions={},
            ),
        ),
        submitted_at=_make_submitted_at(),
        origin_actor_id=action_request.actor_id,
        advisory_ref=None,
        context={},
    )
    event_handoff = EventHandoff(
        category=EventCategory.RULES_OUTCOME,
        payload={
            "action_kind": "set_actor_current_activity",
            "activity": action_request.activity,
        },
        primary_subject_ref=actor_id,
        related_refs=(),
        related_advisory_ref=None,
    )
    return RulesInspectionResult(
        status="accepted",
        diagnostics=(),
        proposed_change=proposed_change,
        event_handoff=event_handoff,
    )


def process_rules_action(
    state_root: StateRoot,
    action_request: RulesActionRequest,
    event_suffix_prefix: str = "rules",
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    inspection_result = inspect_rules_action(state_root, action_request)
    if inspection_result.status == "rejected":
        return state_root, (), inspection_result.diagnostics

    proposed_change = inspection_result.proposed_change
    event_handoff = inspection_result.event_handoff
    if proposed_change is None or event_handoff is None:
        raise ValueError("Accepted rules inspection result must include ProposedChange and EventHandoff.")

    validation_result = validate_proposed_change(proposed_change, state_root)
    if validation_result.status is ValidationStatus.REJECTED:
        return state_root, (), validation_result.diagnostics

    updated_state = apply_approved_mutations(
        state_root,
        validation_result.approved_mutations,
    )
    event = build_authoritative_event(
        handoff=event_handoff,
        event_suffix=f"{event_suffix_prefix}_1",
        occurred_at=proposed_change.submitted_at,
    )
    return updated_state, (event,), validation_result.diagnostics


def _make_submitted_at() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
