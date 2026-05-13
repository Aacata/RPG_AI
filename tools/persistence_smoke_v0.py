from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.contracts import AuthoritativeEvent, EventCategory
from src.core.ids import make_event_id
from src.persistence import EventRepository, SnapshotRepository, open_persistence
from src.core.state_root import StateRoot


def run_demo() -> str:
    backend = open_persistence()
    try:
        events = EventRepository(backend.connection)
        snaps = SnapshotRepository(backend.connection)

        event = AuthoritativeEvent(
            event_id=make_event_id("smoke_1"),
            category=EventCategory.SYSTEM,
            occurred_at="2026-05-12T12:00:00Z",
            primary_subject_ref=None,
            related_refs=(),
            payload={"note": "persistence smoke"},
            schema_version=1,
        )
        events.append_events((event,))
        loaded = events.fetch_event_by_id(str(event.event_id))

        sid = snaps.save_snapshot(StateRoot())
        restored = snaps.load_snapshot(sid)

        output = "\n".join(
            (
                "Persistence Smoke v0",
                f"event_round_trip_ok: {loaded is not None}",
                f"event_payload: {loaded.payload if loaded else {}}",
                f"snapshot_id: {sid}",
                f"snapshot_restore_empty_state_ok: {restored.world_spaces == {}}",
            )
        )
        print(output)
        return output
    finally:
        backend.close()


if __name__ == "__main__":
    run_demo()
