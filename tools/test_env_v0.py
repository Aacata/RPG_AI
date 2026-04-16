from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.ids import ActorId, make_actor_id
from src.core.state_root import StateRoot
from src.npc.actor_baseline import ActorRecord
from src.rules.boundary import process_rules_action
from src.rules.contracts import RulesActionRequest


def build_demo_state() -> tuple[StateRoot, ActorId]:
    actor_id = make_actor_id("demo_guard")
    state_root = StateRoot(
        actors={
            str(actor_id): ActorRecord(
                actor_id=actor_id,
                display_name="Demo Guard",
            )
        }
    )
    return state_root, actor_id


def run_demo() -> str:
    state_root, actor_id = build_demo_state()
    before_activity = state_root.actors[str(actor_id)].current_activity

    action_request = RulesActionRequest(
        request_id="demo_req_1",
        action_kind="set_actor_current_activity",
        actor_id=actor_id,
        activity="standing_guard",
    )

    updated_state, events, diagnostics = process_rules_action(state_root, action_request)
    after_activity = updated_state.actors[str(actor_id)].current_activity

    event_category = events[0].category.value if events else "NONE"
    event_payload = events[0].payload if events else {}

    output = "\n".join(
        (
            "Phase 3 Test Environment v0",
            f"actor_id: {actor_id}",
            f"before_activity: {before_activity!r}",
            f"requested_activity: {action_request.activity!r}",
            f"after_activity: {after_activity!r}",
            f"diagnostics: {diagnostics}",
            f"event_category: {event_category}",
            f"event_payload: {event_payload}",
        )
    )
    print(output)
    return output


if __name__ == "__main__":
    run_demo()
