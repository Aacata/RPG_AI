from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone

from src.core.state_root import StateRoot
from src.persistence.snapshot_codec import (
    SNAPSHOT_SCHEMA_VERSION,
    decode_state_root,
    encode_state_root,
)


class SnapshotRepository:
    """Persist and load whole StateRoot snapshots as versioned JSON blobs."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def save_snapshot(
        self,
        state_root: StateRoot,
        *,
        created_at: str | None = None,
        snapshot_id: str | None = None,
    ) -> str:
        sid = snapshot_id if snapshot_id is not None else f"snap_{uuid.uuid4().hex}"
        ts = created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        blob = encode_state_root(state_root)

        self._conn.execute(
            """
            INSERT INTO state_snapshots (snapshot_id, created_at, snapshot_schema_version, state_json)
            VALUES (?, ?, ?, ?);
            """,
            (sid, ts, SNAPSHOT_SCHEMA_VERSION, blob),
        )
        self._conn.commit()
        return sid

    def load_snapshot(self, snapshot_id: str) -> StateRoot:
        cur = self._conn.execute(
            "SELECT state_json FROM state_snapshots WHERE snapshot_id = ?;",
            (snapshot_id,),
        )
        row = cur.fetchone()
        if row is None:
            raise KeyError(f"Unknown snapshot_id: {snapshot_id}")
        return decode_state_root(row[0])
