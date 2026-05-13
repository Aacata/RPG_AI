from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.ids import make_location_id, make_region_id, make_world_space_id
from src.core.state_root import StateRoot
from src.world.spatial_publication import (
    SpatialBootstrapPublicationRequest,
    inspect_spatial_bootstrap_publication,
    publish_spatial_bootstrap,
)


def build_demo_request() -> SpatialBootstrapPublicationRequest:
    return SpatialBootstrapPublicationRequest(
        request_id="demo_publish_map_bootstrap_v0",
        submitted_at="2026-04-16T10:00:00Z",
        world_space_id=make_world_space_id("primary"),
        sea_level_z=0.0,
        region_id=make_region_id("heartlands"),
        region_display_name="Heartlands",
        location_id=make_location_id("rivergate"),
        location_display_name="Rivergate",
        location_type="settlement",
    )


def run_demo() -> str:
    state_root = StateRoot()
    request = build_demo_request()

    inspection = inspect_spatial_bootstrap_publication(request)
    updated_state, events, diagnostics = publish_spatial_bootstrap(state_root, request)

    published_world_space = updated_state.world_spaces.get(str(request.world_space_id))
    published_region = updated_state.regions.get(str(request.region_id))
    published_location = updated_state.locations.get(str(request.location_id))

    event_category = events[0].category.value if events else "NONE"
    event_payload = events[0].payload if events else {}

    output = "\n".join(
        (
            "Spatial Publication v0 Demo",
            f"request_id: {request.request_id}",
            f"inspection_status: {inspection.status}",
            f"inspection_diagnostics: {inspection.diagnostics}",
            f"world_space_present: {published_world_space is not None}",
            f"region_present: {published_region is not None}",
            f"location_present: {published_location is not None}",
            f"region.world_space_ref: {published_region.world_space_ref if published_region else None}",
            f"location.region_ref: {published_location.region_ref if published_location else None}",
            f"location.location_type: {published_location.location_type if published_location else None}",
            f"diagnostics: {diagnostics}",
            f"event_category: {event_category}",
            f"event_payload: {event_payload}",
        )
    )
    print(output)
    return output


if __name__ == "__main__":
    run_demo()
