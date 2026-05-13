# Phase 2 Close Plan (Operational)

## Purpose

Compact plan for closing remaining Phase 2 exit criteria from [docs/02_canon/BUILD_ORDER.md](docs/02_canon/BUILD_ORDER.md) now that persistence primitives exist ([ADR_SAVE_LOAD_AND_PERSISTENCE.md](../06_decisions/ADR_SAVE_LOAD_AND_PERSISTENCE.md), `src/persistence/`).

## Already Unblocked By Current Code

- **Snapshot and restore (MVP):** `SnapshotRepository` + `snapshot_codec` provide full `StateRoot` round-trip. Save-slot metadata fields can store `snapshot_id` strings as `world_snapshot_ref` once orchestration writes them.
- **Event storage:** `EventRepository` can persist `AuthoritativeEvent` tuples emitted from `process_proposed_change` and rules paths.
- **Orchestration hook (done):** `src/persistence/orchestration.py` — `process_proposed_change_persisted`, `process_rules_action_persisted` append non-empty event tuples after successful applies; core remains SQLite-free.
- **Map discovery (MVP pipeline):** `TargetKind.PLAYER_MAP_DISCOVERY` with boolean slots (reveal, name, visited, marker visible), `map_discovery_pipeline` runtime entry points, WORLD-category event handoffs; legacy helpers delegate to the pipeline.
- **Save slot wiring (MVP done):** `save_slot_checkpoint_snapshot` writes `world_snapshot_ref` + `event_checkpoint_ref` (string of `max_seq`) and persists one self-consistent snapshot; `load_state_from_save_snapshot_ref` restores by slot ref.

## Remaining Work (Prioritized)

1. **Map discovery extensions:** rumor/quest-driven reveals and multi-viewpoint discovery remain deferred; optional future slice: allow `False` for discovery boolean slots if canon requires undo/hide.

2. **NPC importance tier names:** lock enum vocabulary in canon (`docs/02_canon/BUILD_ORDER.md` open question) before expanding tier semantics or voice routing that depends on tiers.

3. **Faction link on locations:** optional narrow contract + mutation matrix row if canon requires parity with actors.

4. **Post-snapshot event tail (future):** optional replay of events after `load_snapshot` when replay rules exist; not implemented in MVP wiring.

## Non-Goals For This Pass

- Full event-sourced replay reconstructing arbitrary `StateRoot` from an empty base.
- Multiplayer or networked saves.
