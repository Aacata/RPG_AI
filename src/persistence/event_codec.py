from __future__ import annotations

import json
from typing import Any

from src.core.contracts import AuthoritativeEvent, EventCategory
from src.core.ids import EventId


def authoritative_event_to_row(event: AuthoritativeEvent) -> dict[str, Any]:
    return {
        "event_id": str(event.event_id),
        "occurred_at": event.occurred_at,
        "category": event.category.value,
        "primary_subject_ref": event.primary_subject_ref,
        "related_refs_json": json.dumps(list(event.related_refs)),
        "payload_json": json.dumps(event.payload),
        "event_schema_version": event.schema_version,
        "location_ref": event.location_ref,
        "faction_ref": event.faction_ref,
        "causation_ref": event.causation_ref,
        "correlation_ref": event.correlation_ref,
        "related_advisory_ref": event.related_advisory_ref,
    }


def row_to_authoritative_event(row: tuple[Any, ...]) -> AuthoritativeEvent:
    (
        _seq,
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
        related_advisory_ref,
    ) = row
    related_refs = tuple(json.loads(related_refs_json))
    payload = json.loads(payload_json)
    return AuthoritativeEvent(
        event_id=EventId(event_id),
        category=EventCategory(category),
        occurred_at=occurred_at,
        primary_subject_ref=primary_subject_ref,
        related_refs=related_refs,
        payload=payload,
        schema_version=int(event_schema_version),
        location_ref=location_ref,
        faction_ref=faction_ref,
        causation_ref=causation_ref,
        correlation_ref=correlation_ref,
        related_advisory_ref=related_advisory_ref,
    )
