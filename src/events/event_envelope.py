from __future__ import annotations

from src.core.contracts import AuthoritativeEvent, EventHandoff
from src.core.ids import make_event_id


def build_authoritative_event(
    handoff: EventHandoff,
    event_suffix: str,
    occurred_at: str,
) -> AuthoritativeEvent:
    return AuthoritativeEvent(
        event_id=make_event_id(event_suffix),
        category=handoff.category,
        occurred_at=occurred_at,
        primary_subject_ref=handoff.primary_subject_ref,
        related_refs=handoff.related_refs,
        payload=handoff.payload,
        schema_version=1,
        related_advisory_ref=handoff.related_advisory_ref,
    )
