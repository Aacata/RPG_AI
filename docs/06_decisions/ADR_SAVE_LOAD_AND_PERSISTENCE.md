# ADR: Save, Load, Event Append Log, And Snapshot Strategy

## ADR Metadata

- ADR ID: ADR_SAVE_LOAD_AND_PERSISTENCE
- Title: Save, Load, Event Append Log, And Snapshot Strategy For Phase 1–2
- Date: 2026-05-12
- Status: Accepted
- Related Docs: `docs/02_canon/BUILD_ORDER.md`, `docs/04_contracts/SAVEGAME_SCHEMA.md`, `docs/04_contracts/EVENT_MODEL.md`, `docs/05_build/IMPLEMENTATION_STATUS.md`

## Context

Phase 1 exit criteria require: (1) authoritative events that can be created, stored, and retrieved, (2) a persistence layer with schema versioning, and (3) a recorded save/load direction. Phase 2 requires snapshot and restore of world and actor state. The simulation core already produces in-memory `AuthoritativeEvent` objects and mutates `StateRoot` through validated `ProposedChange` paths, but nothing survived process restarts.

## Decision

1. **Persistence engine:** SQLite via the Python standard library (`sqlite3`), with an explicit `persistence_schema_version` row in `schema_meta` and versioned tables for events and snapshots.

2. **Authoritative event history:** Append-only rows in `authoritative_events`. Events are stored as JSON-serialized payloads and string-normalized identifiers. Retrieval is by `event_id` and ordered listing by monotonic `seq`. This satisfies "created, stored, and retrieved" for Phase 1. It is not yet a full replay engine.

3. **State snapshots:** Full `StateRoot` is serialized to a versioned JSON blob (`snapshot_schema_version` inside the JSON) and stored in `state_snapshots`. `SnapshotRepository.save_snapshot` / `load_snapshot` provide round-trip restore for MVP inspection and save-slot wiring later.

4. **Save/load direction (hybrid intent, MVP implementation):**
   - **Primary:** periodic or explicit **snapshots** of `StateRoot` (full blob).
   - **Secondary:** **append-only authoritative event log** for audit and future replay or delta derivation.
   - **Deferred:** automatic **delta** materialization between snapshots, multi-writer concurrency, and cross-campaign migration beyond schema version bumps.

Save slot metadata fields (`world_snapshot_ref`, `event_checkpoint_ref`) remain the linkage surface to these stores; wiring save slots to concrete snapshot and event checkpoint IDs is Phase 2+ integration work on top of this ADR.

## Consequences

- Positive: Phase 1 persistence exit criteria can be met with a small, testable module (`src/persistence/`) without pulling ORMs or cloud dependencies.
- Positive: Snapshots and events are logically separable, matching canon separation between state at a point in time and immutable history.
- Negative: Snapshot JSON must evolve carefully when `StateRoot` fields change; migrations will require explicit codec version bumps.
- Tradeoff: Full world replay from events alone is not implemented; snapshots are the reliable restore path for MVP.

## Alternatives Considered

- **Snapshot only:** simpler, weaker audit trail — rejected because Phase 1 explicitly asks for stored and retrieved events.
- **Events only (derive state by replay):** highest fidelity long term — deferred due to complexity before deterministic replay rules are fully defined.
- **Delta-only between snapshots:** deferred until event coverage guarantees completeness.

## Follow-Up Required

- Callers use `src/persistence/orchestration.py` helpers (`process_proposed_change_persisted`, `save_slot_checkpoint_snapshot`, …) instead of implicit hooks inside `process_proposed_change`.
- Optional: event tail after `load_snapshot` when deterministic replay from checkpoint is defined.
- Define migration policy when `snapshot_schema_version` increments.
