from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from src.core.contracts import (
    AuthoritativeEvent,
    MutationKind,
    ProposedChange,
    ProposedChangeOrigin,
    RequestedMutation,
    SlotKey,
    TargetKind,
    TargetSelector,
)
from src.core.ids import LocationId, RegionId, WorldSpaceId
from src.core.runtime import process_proposed_change
from src.core.state_root import StateRoot


@dataclass(frozen=True)
class SpatialBootstrapPublicationRequest:
    request_id: str
    submitted_at: str
    world_space_id: WorldSpaceId
    sea_level_z: float
    region_id: RegionId
    region_display_name: str
    location_id: LocationId
    location_display_name: str
    location_type: str


@dataclass(frozen=True)
class SpatialBootstrapPublicationInspectionResult:
    status: Literal["accepted", "rejected"]
    diagnostics: tuple[str, ...]
    proposed_change: ProposedChange | None


def inspect_spatial_bootstrap_publication(
    request: SpatialBootstrapPublicationRequest,
) -> SpatialBootstrapPublicationInspectionResult:
    diagnostics = _validate_request(request)
    if diagnostics:
        return SpatialBootstrapPublicationInspectionResult(
            status="rejected",
            diagnostics=diagnostics,
            proposed_change=None,
        )

    world_space_target = TargetSelector(kind=TargetKind.WORLD_SPACE)
    region_target = TargetSelector(kind=TargetKind.REGION)
    location_target = TargetSelector(kind=TargetKind.LOCATION)

    proposed_change = ProposedChange(
        proposal_id=request.request_id,
        origin_type=ProposedChangeOrigin.TOOL,
        intent_type="world.publish_spatial_bootstrap",
        target_refs=(world_space_target, region_target, location_target),
        requested_changes=(
            RequestedMutation(
                change_id=f"{request.request_id}_world_space",
                mutation_kind=MutationKind.CREATE_RECORD,
                target=world_space_target,
                arguments={
                    "record_kind": TargetKind.WORLD_SPACE.value,
                    "new_id": str(request.world_space_id),
                    "initial_slots": {
                        SlotKey.SEA_LEVEL_Z.value: request.sea_level_z,
                    },
                },
            ),
            RequestedMutation(
                change_id=f"{request.request_id}_region",
                mutation_kind=MutationKind.CREATE_RECORD,
                target=region_target,
                arguments={
                    "record_kind": TargetKind.REGION.value,
                    "new_id": str(request.region_id),
                    "initial_slots": {
                        SlotKey.DISPLAY_NAME.value: request.region_display_name,
                        SlotKey.WORLD_SPACE_REF.value: str(request.world_space_id),
                    },
                },
            ),
            RequestedMutation(
                change_id=f"{request.request_id}_location",
                mutation_kind=MutationKind.CREATE_RECORD,
                target=location_target,
                arguments={
                    "record_kind": TargetKind.LOCATION.value,
                    "new_id": str(request.location_id),
                    "initial_slots": {
                        SlotKey.DISPLAY_NAME.value: request.location_display_name,
                        SlotKey.REGION_REF.value: str(request.region_id),
                        SlotKey.LOCATION_TYPE.value: request.location_type,
                    },
                },
            ),
        ),
        submitted_at=request.submitted_at,
        context={},
    )
    return SpatialBootstrapPublicationInspectionResult(
        status="accepted",
        diagnostics=(),
        proposed_change=proposed_change,
    )


def publish_spatial_bootstrap(
    state_root: StateRoot,
    request: SpatialBootstrapPublicationRequest,
    event_suffix_prefix: str = "world_publish",
) -> tuple[StateRoot, tuple[AuthoritativeEvent, ...], tuple[str, ...]]:
    inspection_result = inspect_spatial_bootstrap_publication(request)
    if inspection_result.status == "rejected":
        return state_root, (), inspection_result.diagnostics

    proposed_change = inspection_result.proposed_change
    if proposed_change is None:
        raise ValueError("Accepted publication inspection result must include ProposedChange.")

    return process_proposed_change(
        state_root,
        proposed_change,
        event_suffix_prefix=event_suffix_prefix,
    )


def _validate_request(
    request: SpatialBootstrapPublicationRequest,
) -> tuple[str, ...]:
    diagnostics: list[str] = []

    if not request.request_id.strip():
        diagnostics.append("request_id must be a non-empty string.")
    if not request.submitted_at.strip():
        diagnostics.append("submitted_at must be a non-empty string.")
    if not isinstance(request.sea_level_z, (int, float)):
        diagnostics.append("sea_level_z must be numeric.")
    if not request.region_display_name.strip():
        diagnostics.append("region_display_name must be a non-empty string.")
    if not request.location_display_name.strip():
        diagnostics.append("location_display_name must be a non-empty string.")
    if not request.location_type.strip():
        diagnostics.append("location_type must be a non-empty string.")

    return tuple(diagnostics)
