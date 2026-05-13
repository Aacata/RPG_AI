from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


PERSISTENCE_SCHEMA_VERSION = 1


_INIT_SQL = """
CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS authoritative_events (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL UNIQUE,
    occurred_at TEXT NOT NULL,
    category TEXT NOT NULL,
    primary_subject_ref TEXT,
    related_refs_json TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    event_schema_version INTEGER NOT NULL,
    location_ref TEXT,
    faction_ref TEXT,
    causation_ref TEXT,
    correlation_ref TEXT,
    related_advisory_ref TEXT
);

CREATE TABLE IF NOT EXISTS state_snapshots (
    snapshot_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    snapshot_schema_version INTEGER NOT NULL,
    state_json TEXT NOT NULL
);
"""


@dataclass
class PersistenceBackend:
    """SQLite persistence handle. Owns connection lifecycle; callers close explicitly."""

    connection: sqlite3.Connection
    schema_version: int = PERSISTENCE_SCHEMA_VERSION

    def close(self) -> None:
        self.connection.close()


def open_persistence(path: str | Path | None = None) -> PersistenceBackend:
    """
    Open SQLite persistence. Pass None or ':memory:' for an in-memory database.

    Initializes schema and records persistence schema version in schema_meta.
    """
    uri = ":memory:" if path is None else str(path)
    conn = sqlite3.connect(uri)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(_INIT_SQL)
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?);",
        ("persistence_schema_version", str(PERSISTENCE_SCHEMA_VERSION)),
    )
    conn.commit()
    return PersistenceBackend(connection=conn, schema_version=PERSISTENCE_SCHEMA_VERSION)
