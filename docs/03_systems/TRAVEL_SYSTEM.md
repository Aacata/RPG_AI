# Travel System

## Purpose

Define travel as a hybrid subsystem spanning world state, actor state, deterministic rules, event history, and AI narration. Long-distance travel is initiated from the map, while more local travel may be initiated through direct textual intent; in both cases, backend systems remain authoritative over outcomes.

Cross-reference:

- `docs/03_systems/WORLD_SYSTEM.md`
- `docs/03_systems/NPC_SYSTEM.md`
- `docs/03_systems/COMPANION_SYSTEM.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/EVENT_MODEL.md`

## Responsibilities

- Represent canonical travel state and travel intent once accepted by backend systems
- Support long-distance route planning and time-based travel simulation initiated from the map
- Support travel-time fast-forward without removing interruption handling
- Support more granular local travel where canon or setting rules require it
- Expose deterministic travel inputs such as terrain, roads, wilderness, weather, biome, burden, vehicles, mounts, faction influence, and setting-specific routing logic
- Support player waypoints and interruption by encounters, blockers, or social constraints
- Keep local travel interruptible mid-action
- Support NPC travel driven by schedules, routes, roles, faction activity, and world simulation
- Expose companion influence on travel through skills, persuasion, objections, manipulation, or social dynamics

## Non-Responsibilities

- Owning world-map UI or local navigation presentation
- Letting AI decide authoritative travel outcomes
- Replacing combat, encounter, or social-resolution rules once travel triggers those interactions
- Treating every movement action as requiring the same granularity

## Inputs

- World topology and travel conditions
- Actor locations, burden, skills, goals, schedules, and available transport
- Companion and relationship influence inputs
- Faction influence and access constraints
- Weather and biome context
- Player-submitted travel intent or waypoints
- Map-originated long-distance travel initiation
- Direct-text local travel intent
- Rule-approved interruptions and event triggers

## Outputs

- Canonical active travel state
- Route references or route selections
- Travel-time and resource-impact outputs
- Fast-forward progression context subject to interruption
- Interruption and encounter trigger inputs for rules and events
- Travel context for AI narration and presentation layers

## Owned Data

- Active travel intent once accepted into canonical state
- Route or waypoint references
- Travel mode and progress placeholders
- Travel scope placeholder such as long-distance or local traversal
- Fast-forward state placeholder
- Interruption-state placeholders

## Dependencies

- `world` for topology, weather, region, and travel-condition data
- `npc` and related actor state for travelers
- `inventory` for burden and transport-related equipment state
- `relationship` and `companion` context for group travel influence
- `rules` for authoritative timing, risk, and interruption outcomes
- `events` for authoritative travel history
- `ai` for non-canonical travel narration

## Likely Future Extensions

- Setting-specific travel logic such as sea routes or space lanes
- Dynamic route discovery
- Escort or convoy travel
- Fast-travel policies constrained by canon
- Mixed travel initiation rules across settings while preserving the map-only rule for long-distance travel

## Open Questions

- Where local traversal stops being a travel-system concern and becomes a lower-level interaction concern
- Whether travel state should be modeled per actor, per group, or both in MVP
- How setting-specific travel variants are configured without fragmenting the core architecture
- How much of long-travel fast-forward state should be persisted versus derived during replay
