# World System

## Purpose

Represent canonical world-scale state such as places, regions, time context, weather, and other non-actor environmental conditions.

Cross-reference:

- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/03_systems/TRAVEL_SYSTEM.md`

## Responsibilities

- Maintain canonical location and region structures
- Represent world time and calendar state
- Represent weather and environmental state
- Represent world-side travel topology and travel-condition inputs
- Support the world-side preconditions for map-initiated long-distance travel
- Expose world-level inputs used by other backend systems
- Link active world events to the broader simulation context

## Non-Responsibilities

- Resolving deterministic gameplay outcomes on its own
- Owning NPC personality, goals, or memories
- Generating AI narration
- Owning frontend map presentation or dashboard editing state
- Owning authoritative travel-time, travel-risk, or interruption resolution on its own

## Inputs

- Canonical time progression
- Rule-approved world mutations
- Faction presence or influence updates
- Event history references
- Travel topology, route metadata, or map-derived condition inputs approved into canonical state

## Outputs

- Current world snapshot data
- Location and region references for NPCs, factions, quests, and events
- Environmental context consumed by rules or AI interpretation
- Travel-condition context consumed by the travel subsystem and rules layer

## Owned Data

- Locations
- Regions
- Weather state
- Time and calendar state
- World-level environmental flags
- Travel topology and travel-condition references

## Dependencies

- `core` for orchestration and identifiers
- `events` for immutable history linkage
- `factions` for active group presence
- `travel` for hybrid movement logic
- `rules` for deterministic validation of world mutations

## Likely Future Extensions

- Settlement state
- Environmental hazards
- Campaign-setting-specific world modules
- Travel topology variants such as roads, sea lanes, or setting-specific route networks

## Open Questions

- How granular should world snapshots be relative to event replay?
- Should economy indicators remain here or be split into a dedicated subsystem later?
- How are authored map assets linked without shifting ownership to presentation layers?
- Which parts of travel topology are canonical data versus tool-authored map inputs awaiting publication
