from __future__ import annotations

from copy import deepcopy
from typing import Mapping

from src.core.contracts import (
    ActorSpecialization,
    AgencySource,
    ApprovedMutation,
    EventCategory,
    EventHandoff,
    MutationKind,
    ProposedChange,
    RequestedMutation,
    SlotKey,
    StatusFlag,
    TargetKind,
    ValidationResult,
    ValidationStatus,
)
from src.core.ids import ActorId, LocationId, RegionId, SaveSlotId
from src.core.state_root import SaveSlotMetaRecord, StateRoot
from src.npc.actor_baseline import ActorRecord
from src.world.world_state import LocationRecord, RegionRecord, WorldRootRecord


MutableRecord = (
    ActorRecord
    | LocationRecord
    | RegionRecord
    | SaveSlotMetaRecord
    | WorldRootRecord
)

ALLOWED_TARGET_KINDS = frozenset(TargetKind)
ALLOWED_MUTATION_KINDS = frozenset(MutationKind)
ALLOWED_STATUS_FLAGS = frozenset(StatusFlag)
CREATEABLE_RECORD_KINDS = frozenset(
    {
        TargetKind.ACTOR,
        TargetKind.LOCATION,
        TargetKind.REGION,
        TargetKind.SAVE_SLOT_META,
    }
)

ALLOWED_SLOT_MATRIX: dict[TargetKind, frozenset[SlotKey]] = {
    TargetKind.ACTOR: frozenset(
        {
            SlotKey.DISPLAY_NAME,
            SlotKey.ORIGIN_ARCHETYPE,
            SlotKey.ACTOR_SPECIALIZATION,
            SlotKey.AGENCY_SOURCE,
            SlotKey.CATEGORY_OR_ROLE,
            SlotKey.PRIORITY_TIER,
            SlotKey.LOCATION_REF,
            SlotKey.CURRENT_ACTIVITY,
            SlotKey.STATUS_FLAG,
            SlotKey.GOAL_REF,
            SlotKey.SCHEDULE_REF,
            SlotKey.FACTION_LINK_REF,
            SlotKey.INVENTORY_REF,
        }
    ),
    TargetKind.WORLD_ROOT: frozenset(
        {
            SlotKey.WORLD_TIME,
            SlotKey.CALENDAR_REF,
            SlotKey.ACTIVE_EVENT_REF,
            SlotKey.ACTIVE_FACTION_REF,
        }
    ),
    TargetKind.LOCATION: frozenset(
        {
            SlotKey.DISPLAY_NAME,
            SlotKey.REGION_REF,
            SlotKey.LOCATION_TYPE,
        }
    ),
    TargetKind.REGION: frozenset(
        {
            SlotKey.DISPLAY_NAME,
            SlotKey.WORLD_SPACE_REF,
            SlotKey.REGION_PARENT_REF,
        }
    ),
    TargetKind.SAVE_SLOT_META: frozenset(
        {
            SlotKey.SAVE_LABEL,
            SlotKey.SAVE_LAST_UPDATED,
            SlotKey.WORLD_SNAPSHOT_REF,
            SlotKey.EVENT_CHECKPOINT_REF,
            SlotKey.PLAYER_ACTOR_REF,
        }
    ),
}

VALUE_SLOTS = frozenset(
    {
        SlotKey.DISPLAY_NAME,
        SlotKey.ORIGIN_ARCHETYPE,
        SlotKey.ACTOR_SPECIALIZATION,
        SlotKey.AGENCY_SOURCE,
        SlotKey.CATEGORY_OR_ROLE,
        SlotKey.PRIORITY_TIER,
        SlotKey.CURRENT_ACTIVITY,
        SlotKey.WORLD_TIME,
        SlotKey.CALENDAR_REF,
        SlotKey.LOCATION_TYPE,
        SlotKey.SAVE_LABEL,
        SlotKey.SAVE_LAST_UPDATED,
        SlotKey.WORLD_SNAPSHOT_REF,
        SlotKey.EVENT_CHECKPOINT_REF,
    }
)

SINGLE_REFERENCE_SLOTS = frozenset(
    {
        SlotKey.LOCATION_REF,
        SlotKey.GOAL_REF,
        SlotKey.SCHEDULE_REF,
        SlotKey.INVENTORY_REF,
        SlotKey.REGION_REF,
        SlotKey.WORLD_SPACE_REF,
        SlotKey.REGION_PARENT_REF,
        SlotKey.PLAYER_ACTOR_REF,
    }
)

REFERENCE_COLLECTION_SLOTS = frozenset(
    {
        SlotKey.ACTIVE_EVENT_REF,
        SlotKey.FACTION_LINK_REF,
        SlotKey.ACTIVE_FACTION_REF,
    }
)


def is_legal_target_kind(value: TargetKind | str) -> bool:
    try:
        return TargetKind(value) in ALLOWED_TARGET_KINDS
    except ValueError:
        return False


def is_legal_mutation_kind(value: MutationKind | str) -> bool:
    try:
        return MutationKind(value) in ALLOWED_MUTATION_KINDS
    except ValueError:
        return False


def is_legal_status_flag(value: StatusFlag | str) -> bool:
    try:
        return StatusFlag(value) in ALLOWED_STATUS_FLAGS
    except ValueError:
        return False


def is_legal_slot_key(value: SlotKey | str) -> bool:
    try:
        SlotKey(value)
    except ValueError:
        return False
    return True


def is_legal_slot_for_target(
    target_kind: TargetKind | str,
    slot_key: SlotKey | str,
) -> bool:
    try:
        resolved_target = TargetKind(target_kind)
        resolved_slot = SlotKey(slot_key)
    except ValueError:
        return False
    return resolved_slot in ALLOWED_SLOT_MATRIX.get(resolved_target, frozenset())


def validate_proposed_change(
    proposed_change: ProposedChange,
    state_root: StateRoot,
) -> ValidationResult:
    if not proposed_change.requested_changes:
        return ValidationResult(
            status=ValidationStatus.REJECTED,
            diagnostics=("ProposedChange must include at least one requested mutation.",),
        )

    request_errors: list[str] = []
    approved: list[ApprovedMutation] = []

    for requested_change in proposed_change.requested_changes:
        mutation_errors = _validate_requested_mutation(requested_change, state_root)
        if mutation_errors:
            request_errors.extend(mutation_errors)
            continue

        approved.append(
            ApprovedMutation(
                mutation_id=f"approved_{requested_change.change_id}",
                mutation_kind=requested_change.mutation_kind,
                target=requested_change.target,
                applied_arguments=dict(requested_change.arguments),
                source_change_id=requested_change.change_id,
            )
        )

    if request_errors:
        return ValidationResult(
            status=ValidationStatus.REJECTED,
            diagnostics=(
                "Phase 1 uses all-or-nothing request validation; no mutations were approved.",
                *request_errors,
            ),
            approved_mutations=(),
            event_handoffs=(),
        )

    handoff = EventHandoff(
        category=EventCategory.SYSTEM,
        payload={"approved_change_count": len(approved)},
        primary_subject_ref=proposed_change.origin_actor_id,
        related_refs=tuple(
            ref.record_id for ref in proposed_change.target_refs if ref.record_id
        ),
        related_advisory_ref=proposed_change.advisory_ref,
    )
    return ValidationResult(
        status=ValidationStatus.ACCEPTED,
        diagnostics=("ProposedChange accepted.",),
        approved_mutations=tuple(approved),
        event_handoffs=(handoff,),
    )


def apply_approved_mutations(
    state_root: StateRoot,
    approved_mutations: tuple[ApprovedMutation, ...],
) -> StateRoot:
    updated_state = deepcopy(state_root)
    for mutation in approved_mutations:
        _apply_single_mutation(updated_state, mutation)
    return updated_state


def _validate_requested_mutation(
    requested_change: RequestedMutation,
    state_root: StateRoot,
) -> list[str]:
    errors: list[str] = []

    if not is_legal_mutation_kind(requested_change.mutation_kind):
        return [f"Illegal mutation kind: {requested_change.mutation_kind!s}."]

    if not is_legal_target_kind(requested_change.target.kind):
        return [f"Illegal target kind: {requested_change.target.kind!s}."]

    if requested_change.mutation_kind is MutationKind.CREATE_RECORD:
        return _validate_create_record(requested_change, state_root)

    if requested_change.target.record_id is None:
        return ["Non-create mutations require a target record_id."]

    if not _target_exists(
        state_root,
        requested_change.target.kind,
        requested_change.target.record_id,
    ):
        return [
            f"Target does not exist: "
            f"{requested_change.target.kind.value}:{requested_change.target.record_id}."
        ]

    if requested_change.mutation_kind is MutationKind.SET_VALUE:
        errors.extend(_validate_set_value(requested_change))
    elif requested_change.mutation_kind is MutationKind.SET_REFERENCE:
        errors.extend(_validate_set_reference(requested_change, state_root))
    elif requested_change.mutation_kind is MutationKind.ADD_REFERENCE:
        errors.extend(_validate_add_reference(requested_change, state_root))
    elif requested_change.mutation_kind is MutationKind.REMOVE_REFERENCE:
        errors.extend(_validate_remove_reference(requested_change, state_root))
    elif requested_change.mutation_kind is MutationKind.SET_STATUS_FLAG:
        errors.extend(_validate_set_status_flag(requested_change))

    return errors


def _validate_create_record(
    requested_change: RequestedMutation,
    state_root: StateRoot,
) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"record_kind", "new_id", "initial_slots"}),
    )
    if argument_errors:
        return argument_errors

    if requested_change.target.kind not in CREATEABLE_RECORD_KINDS:
        return [
            f"create_record is not allowed for target kind "
            f"{requested_change.target.kind.value}."
        ]
    if requested_change.target.record_id is not None:
        return ["create_record target selector must not include record_id."]

    record_kind_obj = requested_change.arguments.get("record_kind")
    new_id_obj = requested_change.arguments.get("new_id")
    initial_slots_obj = requested_change.arguments.get("initial_slots")

    if not isinstance(record_kind_obj, str):
        return ["create_record record_kind must be a string."]
    if record_kind_obj not in {kind.value for kind in CREATEABLE_RECORD_KINDS}:
        return [f"Illegal create_record record_kind: {record_kind_obj!r}."]
    if record_kind_obj != requested_change.target.kind.value:
        return ["create_record record_kind must match target kind."]
    if not isinstance(new_id_obj, str) or not new_id_obj:
        return ["create_record new_id must be a non-empty string."]
    if not isinstance(initial_slots_obj, Mapping):
        return ["create_record initial_slots must be a mapping."]
    if _target_exists(state_root, requested_change.target.kind, new_id_obj):
        return [f"Record already exists for {record_kind_obj}:{new_id_obj}."]

    errors: list[str] = []
    for slot_name, value in initial_slots_obj.items():
        slot_error = _validate_slot_for_target_name(
            requested_change.target.kind,
            slot_name,
        )
        if slot_error:
            errors.append(slot_error)
            continue

        errors.extend(
            _validate_initial_slot_value(
                requested_change.target.kind,
                SlotKey(slot_name),
                value,
                state_root,
            )
        )
    return errors


def _validate_set_value(requested_change: RequestedMutation) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"slot_key", "value"}),
    )
    if argument_errors:
        return argument_errors

    slot = _coerce_slot_key(requested_change.arguments.get("slot_key"))
    value = requested_change.arguments.get("value")

    if slot is None:
        return ["set_value requires a legal slot_key."]
    if not is_legal_slot_for_target(requested_change.target.kind, slot):
        return [f"Illegal slot {slot.value} for target kind {requested_change.target.kind.value}."]
    if slot not in VALUE_SLOTS:
        return [f"set_value is not legal for slot {slot.value}."]

    if slot is SlotKey.ACTOR_SPECIALIZATION:
        try:
            ActorSpecialization(value)
        except ValueError:
            return [f"Illegal actor_specialization value: {value!r}."]
    if slot is SlotKey.AGENCY_SOURCE:
        try:
            AgencySource(value)
        except ValueError:
            return [f"Illegal agency_source value: {value!r}."]

    return []


def _validate_set_reference(
    requested_change: RequestedMutation,
    state_root: StateRoot,
) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"slot_key", "ref_id"}),
    )
    if argument_errors:
        return argument_errors

    slot = _coerce_slot_key(requested_change.arguments.get("slot_key"))
    ref_id = requested_change.arguments.get("ref_id")

    if slot is None:
        return ["set_reference requires a legal slot_key."]
    if not is_legal_slot_for_target(requested_change.target.kind, slot):
        return [f"Illegal slot {slot.value} for target kind {requested_change.target.kind.value}."]
    if slot not in SINGLE_REFERENCE_SLOTS:
        return [f"set_reference is not legal for slot {slot.value}."]
    if not isinstance(ref_id, str) or not ref_id:
        return ["set_reference requires ref_id as a non-empty string."]

    return _validate_reference_target_exists(slot, ref_id, state_root)


def _validate_add_reference(
    requested_change: RequestedMutation,
    state_root: StateRoot,
) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"slot_key", "ref_id"}),
    )
    if argument_errors:
        return argument_errors

    slot = _coerce_slot_key(requested_change.arguments.get("slot_key"))
    ref_id = requested_change.arguments.get("ref_id")

    if slot is None:
        return ["add_reference requires a legal slot_key."]
    if not is_legal_slot_for_target(requested_change.target.kind, slot):
        return [f"Illegal slot {slot.value} for target kind {requested_change.target.kind.value}."]
    if slot not in REFERENCE_COLLECTION_SLOTS:
        return [f"add_reference is not legal for slot {slot.value}."]
    if not isinstance(ref_id, str) or not ref_id:
        return ["add_reference requires ref_id as a non-empty string."]

    return []


def _validate_remove_reference(
    requested_change: RequestedMutation,
    state_root: StateRoot,
) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"slot_key", "ref_id"}),
    )
    if argument_errors:
        return argument_errors

    slot = _coerce_slot_key(requested_change.arguments.get("slot_key"))
    ref_id = requested_change.arguments.get("ref_id")

    if slot is None:
        return ["remove_reference requires a legal slot_key."]
    if not is_legal_slot_for_target(requested_change.target.kind, slot):
        return [f"Illegal slot {slot.value} for target kind {requested_change.target.kind.value}."]
    if slot not in REFERENCE_COLLECTION_SLOTS:
        return [f"remove_reference is not legal for slot {slot.value}."]
    if not isinstance(ref_id, str) or not ref_id:
        return ["remove_reference requires ref_id as a non-empty string."]

    collection = _resolve_collection(
        state_root,
        requested_change.target.kind,
        requested_change.target.record_id,
        slot,
    )
    if ref_id not in [str(item) for item in collection]:
        return [f"Reference {ref_id} is not present in {slot.value}."]

    return []


def _validate_set_status_flag(requested_change: RequestedMutation) -> list[str]:
    argument_errors = _validate_argument_keys(
        requested_change.arguments,
        required_keys=frozenset({"slot_key", "flag_name", "flag_value"}),
    )
    if argument_errors:
        return argument_errors

    if requested_change.target.kind is not TargetKind.ACTOR:
        return ["set_status_flag is only legal for actor targets in Phase 1."]

    slot = _coerce_slot_key(requested_change.arguments.get("slot_key"))
    flag_name = requested_change.arguments.get("flag_name")
    flag_value = requested_change.arguments.get("flag_value")

    if slot is not SlotKey.STATUS_FLAG:
        return ["set_status_flag requires slot_key=status_flag."]
    if not is_legal_status_flag(flag_name):
        return [f"Illegal status flag: {flag_name!r}."]
    if not isinstance(flag_value, bool):
        return ["set_status_flag requires boolean flag_value."]

    return []


def _apply_single_mutation(state_root: StateRoot, mutation: ApprovedMutation) -> None:
    if mutation.mutation_kind is MutationKind.CREATE_RECORD:
        _apply_create_record(state_root, mutation)
        return

    record = _get_record(state_root, mutation.target.kind, mutation.target.record_id)

    if mutation.mutation_kind is MutationKind.SET_VALUE:
        slot = SlotKey(mutation.applied_arguments["slot_key"])
        setattr(record, slot.value, mutation.applied_arguments["value"])
    elif mutation.mutation_kind is MutationKind.SET_REFERENCE:
        slot = SlotKey(mutation.applied_arguments["slot_key"])
        setattr(record, slot.value, mutation.applied_arguments["ref_id"])
    elif mutation.mutation_kind is MutationKind.ADD_REFERENCE:
        slot = SlotKey(mutation.applied_arguments["slot_key"])
        collection = _resolve_collection(
            state_root,
            mutation.target.kind,
            mutation.target.record_id,
            slot,
        )
        ref_id_obj = mutation.applied_arguments["ref_id"]
        if not isinstance(ref_id_obj, str):
            raise ValueError("add_reference ref_id must be a string.")
        if ref_id_obj not in collection:
            collection.append(ref_id_obj)
    elif mutation.mutation_kind is MutationKind.REMOVE_REFERENCE:
        slot = SlotKey(mutation.applied_arguments["slot_key"])
        collection = _resolve_collection(
            state_root,
            mutation.target.kind,
            mutation.target.record_id,
            slot,
        )
        ref_id_obj = mutation.applied_arguments["ref_id"]
        if not isinstance(ref_id_obj, str):
            raise ValueError("remove_reference ref_id must be a string.")
        collection[:] = [item for item in collection if str(item) != ref_id_obj]
    elif mutation.mutation_kind is MutationKind.SET_STATUS_FLAG:
        _apply_status_flag(record, mutation.applied_arguments)


def _apply_create_record(state_root: StateRoot, mutation: ApprovedMutation) -> None:
    target_kind = mutation.target.kind
    raw_new_id = mutation.applied_arguments["new_id"]
    if not isinstance(raw_new_id, str):
        raise ValueError("new_id must be a string.")

    typed_new_id = _coerce_new_id(target_kind, raw_new_id)

    initial_slots_obj = mutation.applied_arguments.get("initial_slots", {})
    if not isinstance(initial_slots_obj, Mapping):
        raise ValueError("initial_slots must be a mapping.")

    if target_kind is TargetKind.ACTOR:
        record = ActorRecord(actor_id=typed_new_id)
        state_root.actors[str(typed_new_id)] = record
    elif target_kind is TargetKind.LOCATION:
        record = LocationRecord(location_id=typed_new_id)
        state_root.locations[str(typed_new_id)] = record
    elif target_kind is TargetKind.REGION:
        record = RegionRecord(region_id=typed_new_id)
        state_root.regions[str(typed_new_id)] = record
    elif target_kind is TargetKind.SAVE_SLOT_META:
        record = SaveSlotMetaRecord(save_slot_id=typed_new_id)
        state_root.save_slots[str(typed_new_id)] = record
    else:
        raise ValueError(f"Unsupported create_record target kind: {target_kind.value}.")

    _apply_initial_slots(record, initial_slots_obj)


def _apply_initial_slots(
    record: MutableRecord,
    initial_slots: Mapping[str, object],
) -> None:
    for slot_name, value in initial_slots.items():
        slot = SlotKey(slot_name)
        if slot is SlotKey.STATUS_FLAG:
            if not isinstance(value, Mapping):
                raise ValueError("Initial status_flag value must be a mapping.")
            _apply_status_flag(record, value)
            continue
        setattr(record, slot.value, value)


def _apply_status_flag(
    record: MutableRecord,
    arguments: Mapping[str, object],
) -> None:
    flag_name = arguments["flag_name"]
    flag_value = arguments["flag_value"]

    if not isinstance(flag_name, str):
        raise ValueError("flag_name must be a string.")
    if not isinstance(flag_value, bool):
        raise ValueError("flag_value must be a boolean.")

    flag = StatusFlag(flag_name)
    if flag_value:
        record.status_flags.add(flag)
    else:
        record.status_flags.discard(flag)


def _coerce_new_id(
    target_kind: TargetKind,
    raw_id: str,
) -> ActorId | LocationId | RegionId | SaveSlotId:
    if target_kind is TargetKind.ACTOR:
        return ActorId(raw_id)
    if target_kind is TargetKind.LOCATION:
        return LocationId(raw_id)
    if target_kind is TargetKind.REGION:
        return RegionId(raw_id)
    if target_kind is TargetKind.SAVE_SLOT_META:
        return SaveSlotId(raw_id)
    raise ValueError(f"Unsupported target kind for new_id coercion: {target_kind.value}.")


def _validate_argument_keys(
    arguments: Mapping[str, object],
    required_keys: frozenset[str],
) -> list[str]:
    provided_keys = frozenset(arguments.keys())
    missing = required_keys - provided_keys
    unexpected = provided_keys - required_keys

    errors: list[str] = []
    if missing:
        errors.append(
            f"Malformed mutation arguments; missing keys: {', '.join(sorted(missing))}."
        )
    if unexpected:
        errors.append(
            f"Malformed mutation arguments; unexpected keys: {', '.join(sorted(unexpected))}."
        )
    return errors


def _coerce_slot_key(value: object) -> SlotKey | None:
    try:
        return SlotKey(value)
    except ValueError:
        return None


def _validate_slot_for_target_name(target_kind: TargetKind, slot_name: object) -> str | None:
    try:
        slot = SlotKey(slot_name)
    except ValueError:
        return f"Illegal slot key: {slot_name!r}."
    if not is_legal_slot_for_target(target_kind, slot):
        return f"Illegal slot {slot.value} for target kind {target_kind.value}."
    return None


def _validate_initial_slot_value(
    target_kind: TargetKind,
    slot: SlotKey,
    value: object,
    state_root: StateRoot,
) -> list[str]:
    if not is_legal_slot_for_target(target_kind, slot):
        return [f"Illegal slot {slot.value} for target kind {target_kind.value}."]

    if slot in REFERENCE_COLLECTION_SLOTS:
        return [f"Initial slot {slot.value} is not supported for create_record in Phase 1."]

    if slot is SlotKey.STATUS_FLAG:
        if not isinstance(value, Mapping):
            return ["Initial status_flag value must be a mapping."]
        status_errors = _validate_argument_keys(
            value,
            required_keys=frozenset({"flag_name", "flag_value"}),
        )
        if status_errors:
            return [f"Initial status_flag is malformed. {error}" for error in status_errors]

        flag_name = value.get("flag_name")
        flag_value = value.get("flag_value")
        if not is_legal_status_flag(flag_name if isinstance(flag_name, str) else ""):
            return [f"Illegal initial status flag: {flag_name!r}."]
        if not isinstance(flag_value, bool):
            return ["Initial status_flag requires boolean flag_value."]
        return []

    if slot in VALUE_SLOTS:
        if slot is SlotKey.ACTOR_SPECIALIZATION:
            try:
                ActorSpecialization(value)
            except ValueError:
                return [f"Illegal actor_specialization value: {value!r}."]
        if slot is SlotKey.AGENCY_SOURCE:
            try:
                AgencySource(value)
            except ValueError:
                return [f"Illegal agency_source value: {value!r}."]
        return []

    if slot in SINGLE_REFERENCE_SLOTS:
        if not isinstance(value, str) or not value:
            return [f"Initial reference slot {slot.value} requires a non-empty string value."]
        return _validate_reference_target_exists(slot, value, state_root)

    return [f"Initial slot {slot.value} is not supported for create_record in Phase 1."]


def _target_exists(
    state_root: StateRoot,
    target_kind: TargetKind,
    record_id: str | None,
) -> bool:
    if target_kind is TargetKind.WORLD_ROOT:
        return record_id in (None, "world_root")
    if record_id is None:
        return False
    store = _store_for_target_kind(state_root, target_kind)
    return str(record_id) in store


def _store_for_target_kind(
    state_root: StateRoot,
    target_kind: TargetKind,
) -> dict[str, object]:
    if target_kind is TargetKind.ACTOR:
        return state_root.actors
    if target_kind is TargetKind.LOCATION:
        return state_root.locations
    if target_kind is TargetKind.REGION:
        return state_root.regions
    if target_kind is TargetKind.SAVE_SLOT_META:
        return state_root.save_slots
    raise ValueError(f"Target kind {target_kind.value} does not map to a dictionary store.")


def _get_record(
    state_root: StateRoot,
    target_kind: TargetKind,
    record_id: str | None,
) -> MutableRecord:
    if target_kind is TargetKind.WORLD_ROOT:
        return state_root.world_root
    if record_id is None:
        raise ValueError("record_id is required for non-world_root targets.")
    store = _store_for_target_kind(state_root, target_kind)
    record = store[str(record_id)]
    if not isinstance(
        record,
        (ActorRecord, LocationRecord, RegionRecord, SaveSlotMetaRecord, WorldRootRecord),
    ):
        raise TypeError("Resolved record has unsupported type.")
    return record


def _resolve_collection(
    state_root: StateRoot,
    target_kind: TargetKind,
    record_id: str | None,
    slot: SlotKey,
) -> list[object]:
    record = _get_record(state_root, target_kind, record_id)
    if slot is SlotKey.ACTIVE_EVENT_REF:
        return record.active_event_refs
    if slot is SlotKey.FACTION_LINK_REF:
        return record.faction_link_refs
    if slot is SlotKey.ACTIVE_FACTION_REF:
        return record.active_faction_refs
    raise ValueError(f"Unsupported collection slot: {slot.value}.")


def _validate_reference_target_exists(
    slot: SlotKey,
    ref_id: str,
    state_root: StateRoot,
) -> list[str]:
    if slot is SlotKey.LOCATION_REF and ref_id not in state_root.locations:
        return [f"Unknown location reference: {ref_id}."]
    if slot is SlotKey.REGION_REF and ref_id not in state_root.regions:
        return [f"Unknown region reference: {ref_id}."]
    if slot is SlotKey.WORLD_SPACE_REF and ref_id not in state_root.world_spaces:
        return [f"Unknown world space reference: {ref_id}."]
    if slot is SlotKey.REGION_PARENT_REF and ref_id not in state_root.regions:
        return [f"Unknown region parent reference: {ref_id}."]
    if slot is SlotKey.PLAYER_ACTOR_REF and ref_id not in state_root.actors:
        return [f"Unknown actor reference: {ref_id}."]
    return []
