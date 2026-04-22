from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

from src.core.ids import ActorId, EventId


class TargetKind(str, Enum):
    ACTOR = "actor"
    WORLD_ROOT = "world_root"
    WORLD_SPACE = "world_space"
    LOCATION = "location"
    REGION = "region"
    SAVE_SLOT_META = "save_slot_meta"


class SlotKey(str, Enum):
    DISPLAY_NAME = "display_name"
    ORIGIN_ARCHETYPE = "origin_archetype"
    ACTOR_SPECIALIZATION = "actor_specialization"
    AGENCY_SOURCE = "agency_source"
    CATEGORY_OR_ROLE = "category_or_role"
    PRIORITY_TIER = "priority_tier"
    LOCATION_REF = "location_ref"
    CURRENT_ACTIVITY = "current_activity"
    STATUS_FLAG = "status_flag"
    GOAL_REF = "goal_ref"
    SCHEDULE_REF = "schedule_ref"
    FACTION_LINK_REF = "faction_link_ref"
    INVENTORY_REF = "inventory_ref"
    WORLD_TIME = "world_time"
    CALENDAR_REF = "calendar_ref"
    ACTIVE_EVENT_REF = "active_event_ref"
    ACTIVE_FACTION_REF = "active_faction_ref"
    SEA_LEVEL_Z = "sea_level_z"
    REGION_REF = "region_ref"
    WORLD_SPACE_REF = "world_space_ref"
    REGION_PARENT_REF = "region_parent_ref"
    LOCATION_TYPE = "location_type"
    SAVE_LABEL = "save_label"
    SAVE_LAST_UPDATED = "save_last_updated"
    WORLD_SNAPSHOT_REF = "world_snapshot_ref"
    EVENT_CHECKPOINT_REF = "event_checkpoint_ref"
    PLAYER_ACTOR_REF = "player_actor_ref"


class StatusFlag(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    ARCHIVED = "archived"


class MutationKind(str, Enum):
    CREATE_RECORD = "create_record"
    SET_VALUE = "set_value"
    SET_REFERENCE = "set_reference"
    ADD_REFERENCE = "add_reference"
    REMOVE_REFERENCE = "remove_reference"
    SET_STATUS_FLAG = "set_status_flag"


class ProposedChangeOrigin(str, Enum):
    PLAYER_INPUT = "player_input"
    SIMULATION_SYSTEM = "simulation_system"
    TOOL = "tool"
    ADVISORY_AI_REF = "advisory_ai_ref"


class ValidationStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class EventCategory(str, Enum):
    WORLD = "WORLD"
    NPC = "NPC"
    RULES_OUTCOME = "RULES_OUTCOME"
    SYSTEM = "SYSTEM"


class ActorSpecialization(str, Enum):
    PLAYER = "player"
    NPC = "npc"


class AgencySource(str, Enum):
    HUMAN_PLAYER = "human_player"
    SIMULATION_SYSTEM = "simulation_system"


@dataclass(frozen=True)
class TargetSelector:
    kind: TargetKind
    record_id: str | None = None


@dataclass(frozen=True)
class RequestedMutation:
    change_id: str
    mutation_kind: MutationKind
    target: TargetSelector
    arguments: Mapping[str, Any]
    preconditions: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProposedChange:
    proposal_id: str
    origin_type: ProposedChangeOrigin
    intent_type: str
    target_refs: tuple[TargetSelector, ...]
    requested_changes: tuple[RequestedMutation, ...]
    submitted_at: str
    origin_actor_id: ActorId | None = None
    advisory_ref: str | None = None
    context: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ApprovedMutation:
    mutation_id: str
    mutation_kind: MutationKind
    target: TargetSelector
    applied_arguments: Mapping[str, Any]
    source_change_id: str


@dataclass(frozen=True)
class EventHandoff:
    category: EventCategory
    payload: dict[str, Any]
    primary_subject_ref: str | None = None
    related_refs: tuple[str, ...] = ()
    related_advisory_ref: str | None = None


@dataclass(frozen=True)
class ValidationResult:
    status: ValidationStatus
    diagnostics: tuple[str, ...]
    approved_mutations: tuple[ApprovedMutation, ...] = ()
    event_handoffs: tuple[EventHandoff, ...] = ()


@dataclass(frozen=True)
class AuthoritativeEvent:
    event_id: EventId
    category: EventCategory
    occurred_at: str
    primary_subject_ref: str | None
    related_refs: tuple[str, ...]
    payload: dict[str, Any]
    schema_version: int
    location_ref: str | None = None
    faction_ref: str | None = None
    causation_ref: str | None = None
    correlation_ref: str | None = None
    related_advisory_ref: str | None = None
