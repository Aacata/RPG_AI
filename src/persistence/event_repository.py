from __future__ import annotations

import sqlite3
from typing import Iterable

from src.core.contracts import AuthoritativeEvent
from src.persistence.event_codec import authoritative_event_to_row, row_to_authoritative_event


class EventRepository:
    """Append-only store and retrieval for AuthoritativeEvent rows."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def append_events(self, events: Iterable[AuthoritativeEvent]) -> None:
        row_tuples = []
        for event in events:
            r = authoritative_event_to_row(event)
            row_tuples.append(
                (
                    r["event_id"],
                    r["occurred_at"],
                    r["category"],
                    r["primary_subject_ref"],
                    r["related_refs_json"],
                    r["payload_json"],
                    r["event_schema_version"],
                    r["location_ref"],
                    r["faction_ref"],
                    r["causation_ref"],
                    r["correlation_ref"],
                    r["related_advisory_ref"],
                )
            )
        self._conn.executemany(
            """
            INSERT INTO authoritative_events (
                event_id,
                occurred_at,
                category,
                primary_subject_ref,
                related_refs_json,
                payload_json,
                event_schema_version,
                location_ref,
                faction_ref,
                causation_ref,
                correlation_ref,
                related_advisory_ref
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            row_tuples,
        )
        self._conn.commit()

    def fetch_event_by_id(self, event_id: str) -> AuthoritativeEvent | None:
        cur = self._conn.execute(
            """
            SELECT seq, event_id, occurred_at, category, primary_subject_ref,
                   related_refs_json, payload_json, event_schema_version,
                   location_ref, faction_ref, causation_ref, correlation_ref,
                   related_advisory_ref
            FROM authoritative_events
            WHERE event_id = ?;
            """,
            (event_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return row_to_authoritative_event(row)

    def list_events_ordered(self, limit: int = 100) -> tuple[AuthoritativeEvent, ...]:
        cur = self._conn.execute(
            """
            SELECT seq, event_id, occurred_at, category, primary_subject_ref,
                   related_refs_json, payload_json, event_schema_version,
                   location_ref, faction_ref, causation_ref, correlation_ref,
                   related_advisory_ref
            FROM authoritative_events
            ORDER BY seq ASC
            LIMIT ?;
            """,
            (limit,),
        )
        return tuple(row_to_authoritative_event(row) for row in cur.fetchall())

    def max_seq(self) -> int:
        """Highest authoritative_events.seq, or 0 when the log is empty."""
        cur = self._conn.execute("SELECT COALESCE(MAX(seq), 0) FROM authoritative_events;")
        row = cur.fetchone()
        return int(row[0]) if row is not None else 0
