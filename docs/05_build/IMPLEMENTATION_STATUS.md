# Implementation Status

## Purpose

This file is an operational status snapshot for contributors and AI sessions.
It is not a second architecture document. Use canon files for ownership and invariants.
Use this file for blunt implementation boundaries.

## Core

- Canon status: Backend-owned mutation validation and authoritative event handoff are canon.
- Implemented now: Typed IDs, core mutation/event contracts, validated mutation surface, atomic apply path, authoritative event handoff objects, event object building via the event envelope, and `process_proposed_change(...)`.
- Tested now: `tests/test_phase1_core_slice.py`.
- Explicitly not implemented in core: automatic SQLite or disk writes from `process_proposed_change` (persistence is opt-in via `src.persistence` orchestration helpers). Save/load strategy beyond contracts, schema versioning beyond current in-memory event object building.
- Next allowed slice: Keep expanding only through narrow canon-backed contracts. Event construction is not event persistence unless callers use the persistence orchestration layer.

## World / Map

- Canon status: Canonical spatial truth is backend-owned and separate from discovery/presentation.
- Implemented now: `WorldSpaceRecord`, `RegionRecord`, `LocationRecord`, `StateRoot.world_spaces`, and record-level `LocationRecord` fields (`x`, `y`, `z`, `biome`, `is_hidden_by_default`).
- Tested now: `tests/test_phase1_core_slice.py` covers record presence and world-space linking.
- Explicitly not implemented: Travel semantics, route logic, beauty-map pipeline, and full validated mutation support for `LocationRecord.x/y/z/biome/is_hidden_by_default`.
- Next allowed slice: Add only narrow canon-backed map/state slices. Field presence is not mutation support. Do not treat record-level fields as permission to mutate them or as a full travel/map subsystem.

## NPC / Actor Baseline

- Canon status: Player and NPC share the actor family baseline; backend owns actor truth.
- Implemented now: `ActorRecord`, shared baseline fields, player specialization, `location_ref` actor placement, and narrow actor mutation support in core validation.
- Tested now: `tests/test_phase1_core_slice.py`.
- Explicitly not implemented: Tier semantics beyond stored fields, companion behavior, memory-aware behavior, inventory/faction subsystem behavior.
- Next allowed slice: Keep actor expansion narrow and canon-backed. Do not infer subsystem semantics from stored actor fields alone.

## Rules Boundary

- Canon status: Rules are backend-owned; AI remains advisory only.
- Implemented now: Narrow MVP boundary with `RulesActionRequest`, `RulesInspectionResult`, `inspect_rules_action(...)`, and `process_rules_action(...)` for one action kind: `set_actor_current_activity`.
- Tested now: `tests/test_rules_boundary_mvp.py`; demo in `tools/test_env_v0.py`.
- Explicitly not implemented: General gameplay-wide resolution engine, full formula rollout, multiple action kinds, travel/combat/quest rule semantics.
- Next allowed slice: Add one small rules action at a time through `ProposedChange` plus authoritative event handoff. Do not claim full rules-engine implementation from the current MVP path.

## Map Discovery

- Canon status: Discovery is separate from canonical map truth and is backend-owned, not frontend-owned.
- Implemented now: `MapDiscoveryEntry`, `StateRoot.player_map_discovery`, `build_player_location_discovery_read_model(...)`, and **canonical mutation path** via `TargetKind.PLAYER_MAP_DISCOVERY` + discovery `SlotKey`s in `src/core/transition_validation.py`. High-level builders and WORLD events in [`src/world/map_discovery_pipeline.py`](d:/BJARKI/RPG_2026_AI/RPG_AI/src/world/map_discovery_pipeline.py): reveal, reveal name, visited, marker visible (`set_player_location_marker_visible_through_runtime`). Backward-compatible in-place helpers in [`src/world/map_discovery_updates.py`](d:/BJARKI/RPG_2026_AI/RPG_AI/src/world/map_discovery_updates.py) delegate to the pipeline and sync `player_map_discovery` on the caller's `StateRoot`.
- Tested now: `tests/test_phase1_core_slice.py` (discovery behavior); `tests/test_map_discovery_pipeline.py` (event category, slot matrix, visit flags).
- Explicitly not implemented: Full discovery mechanics, rumor-driven reveal, quest-driven reveal, multi-viewpoint discovery, clearing map-discovery flags via `ProposedChange` (Phase 1 only accepts `True` for discovery booleans; hiding a marker without new rules remains deferred).
- Next allowed slice: narrow `map_discovery` intents that set `is_marker_visible`, or discovery-from-rumor contracts. Do not treat read-model helpers alone as full discovery completion.

## Spatial Publication

- Canon status: Backend-owned publication path that creates a minimal `WorldSpace` + `Region` + `Location` bundle atomically through the canonical runtime entry point. Tool-origin authoring may request publication; canonical truth ownership remains backend-side.
- Implemented now: `SpatialBootstrapPublicationRequest`, `inspect_spatial_bootstrap_publication(...)`, and `publish_spatial_bootstrap(...)` in `src/world/spatial_publication.py`. The publisher inspects/validates request fields, builds a `ProposedChange` with three `CREATE_RECORD` mutations (world_space, region, location), and delegates to `process_proposed_change(...)`. Pending-create cross-references are resolved inside the same batch via `_collect_pending_create_ids` in `src/core/transition_validation.py`.
- Tested now: `tests/test_spatial_publication_v0.py` covers happy path, atomic rejection when the region references an unknown world space, atomic rejection when the location references an unknown region, all-or-nothing rollback on any single invalid mutation, and rejection of duplicate `new_id` within the same bundle. Demo in `tools/test_env_spatial_publication_v0.py`.
- Explicitly not implemented: Publication of `LocationRecord.x/y/z/biome/is_hidden_by_default` through the mutation surface (those fields remain record-level only), multi-location bundles, hierarchical region trees in one publish, builder-side draft workflow, persistence of published bundles, and any AI-assisted publication proposals.
- Next allowed slice: Add one narrow canon-backed publication field at a time. Field presence on the record is not mutation support; mutation-surface support is the next gating step before extra spatial fields become publishable.

## AI Runtime

- Canon status: AI is advisory only and may not own deterministic outcomes.
- Implemented now: No AI runtime implementation in the current repo state.
- Tested now: No AI runtime tests in the current repo state.
- Explicitly not implemented: Gemini runtime, FLOW runtime modulation, advisory log, AI proposal intake pipeline, viewpoint-filtered narration runtime.
- Next allowed slice: Only canon-backed advisory adapters and validation paths. Do not imply runtime AI support from canon docs alone.

## Persistence

- Canon status: Hybrid MVP direction is locked in `docs/06_decisions/ADR_SAVE_LOAD_AND_PERSISTENCE.md` — snapshots as primary restore vehicle, append-only authoritative event log as secondary audit and future replay input, deltas deferred.
- Implemented now: `src/persistence/` with `open_persistence`, `schema_meta` key `persistence_schema_version`, append-only `authoritative_events` table, `EventRepository.append_events` / `fetch_event_by_id` / `list_events_ordered` / `max_seq`, and `state_snapshots` with `SnapshotRepository.save_snapshot` / `load_snapshot` (optional preassigned `snapshot_id`) plus JSON `StateRoot` codec (`snapshot_schema_version` inside blob). Orchestration in `src/persistence/orchestration.py`: `process_proposed_change_persisted`, `process_rules_action_persisted` (append events after successful applies; core stays SQLite-free), `save_slot_checkpoint_snapshot`, `load_state_from_save_snapshot_ref` for `world_snapshot_ref` / `event_checkpoint_ref` wiring on `SaveSlotMetaRecord`.
- Tested now: `tests/test_persistence_phase1.py` covers event append and fetch, events emitted from `process_proposed_change` persisted to SQLite, snapshot round-trip, orchestration append/skip-on-reject, rules persisted path, and save-slot checkpoint plus load round-trip.
- Explicitly not implemented: implicit hook inside `process_proposed_change` itself (callers use orchestration helpers instead), event-sourced full replay from an empty base, delta materialization between snapshots, event-tail replay after snapshot restore, multi-process concurrency.
- Next allowed slice: optional event tail after `load_snapshot` when replay rules exist; map discovery through `ProposedChange` if closing Phase 2 “all mutations emit events” literally.

## Travel

- Canon status: Travel is a defined future subsystem with backend-owned authority.
- Implemented now: No travel subsystem implementation in the current repo state.
- Tested now: No travel tests in the current repo state.
- Explicitly not implemented: Routes, travel-time resolution, interruption logic, travel events, map-driven travel mechanics.
- Next allowed slice: Only explicit canon-backed travel slices. Do not infer travel behavior from map records or rules canon.

## Memory / Knowledge / Rumor

- Canon status: Event truth, memory, knowledge, and rumor are distinct and must remain distinct.
- Implemented now: No memory/knowledge/rumor runtime implementation in the current repo state.
- Tested now: No memory/knowledge/rumor tests in the current repo state.
- Explicitly not implemented: Memory records, knowledge state, rumor objects, witness logic, knowledge gating.
- Next allowed slice: One narrow contract-backed boundary at a time. Do not infer these systems from documentation-only canon.

## Inventory / Factions / Quests

- Canon status: These remain backend-owned future subsystems.
- Implemented now: Placeholder references only, such as actor inventory refs, faction link refs, world active faction refs, and save-slot refs. Core validation allows some narrow reference/value storage.
- Tested now: `tests/test_phase1_core_slice.py` covers only placeholder reference storage and mutation legality.
- Explicitly not implemented: Inventory semantics, faction entities/logic, quest state/progression, subsystem-specific rules or event flows.
- Next allowed slice: Add explicit subsystem contracts before claiming subsystem behavior. Do not equate placeholder refs with subsystem implementation.
