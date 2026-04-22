# Implementation Status

## Purpose

This file is an operational status snapshot for contributors and AI sessions.
It is not a second architecture document. Use canon files for ownership and invariants.
Use this file for blunt implementation boundaries.

## Core

- Canon status: Backend-owned mutation validation and authoritative event handoff are canon.
- Implemented now: Typed IDs, core mutation/event contracts, validated mutation surface, atomic apply path, authoritative event handoff objects, event object building via the event envelope, and `process_proposed_change(...)`.
- Tested now: `tests/test_phase1_core_slice.py`.
- Explicitly not implemented: Persistent event storage, event retrieval backend, persistence backend, save/load strategy, schema versioning beyond current in-memory event object building.
- Next allowed slice: Keep expanding only through narrow canon-backed contracts. Event construction is not event persistence. Do not imply storage, retrieval, or replay support from current in-memory event object building.

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
- Implemented now: `MapDiscoveryEntry`, `StateRoot.player_map_discovery`, `build_player_location_discovery_read_model(...)`, and helper-level updates for reveal/name/visited in `src/world/map_discovery_updates.py`.
- Tested now: `tests/test_phase1_core_slice.py`; demo in `tools/test_env_map_discovery_v0.py`.
- Explicitly not implemented: Full discovery mechanics, rumor-driven reveal, quest-driven reveal, multi-viewpoint discovery, proposed-change integration, authoritative-event integration for discovery helpers.
- Next allowed slice: Add one narrow backend-approved discovery contract or trigger path at a time. Do not treat helper functions as full discovery subsystem completion.

## AI Runtime

- Canon status: AI is advisory only and may not own deterministic outcomes.
- Implemented now: No AI runtime implementation in the current repo state.
- Tested now: No AI runtime tests in the current repo state.
- Explicitly not implemented: Gemini runtime, FLOW runtime modulation, advisory log, AI proposal intake pipeline, viewpoint-filtered narration runtime.
- Next allowed slice: Only canon-backed advisory adapters and validation paths. Do not imply runtime AI support from canon docs alone.

## Persistence

- Canon status: Persistence direction is not fully decided in canon.
- Implemented now: Save-slot metadata record only.
- Tested now: Save-slot metadata is exercised in `tests/test_phase1_core_slice.py` as record state, not as save/load implementation.
- Explicitly not implemented: SQLite backend, snapshot storage, delta storage, load/replay pipeline, persisted event history.
- Next allowed slice: Direction-setting and narrow persistence foundation work only after canon-backed decisions. Save-slot metadata is not persistence. Do not imply save/load implementation from save-slot fields.

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
