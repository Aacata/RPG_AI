# Quest System

## Purpose

Represent structured progression state for goals, tasks, or objective chains without replacing emergent simulation.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/04_contracts/SAVEGAME_SCHEMA.md`

## Responsibilities

- Track canonical quest or objective progression state
- Link quest state to entities, locations, events, or factions
- Expose quest progression to rules, AI interpretation, and presentation layers

## Non-Responsibilities

- Replacing systemic simulation with hardcoded narrative authority
- Determining success conditions outside deterministic rule validation
- Owning UI quest journals
- Acting as the sole source of player motivation or story

## Inputs

- Event history
- Rule-approved progression updates
- Entity and location references

## Outputs

- Canonical quest status views
- Objective linkage for clients and tools
- Historical references for summaries and replay inspection

## Owned Data

- Quest identifiers
- Objective state
- Participation links
- Status and progression flags

## Dependencies

- `events` for authoritative triggers
- `rules` for progression validation
- `npc`, `world`, `factions`, and `inventory` for linked conditions

## Likely Future Extensions

- Procedural objective generation
- Multiple quest archetypes
- Campaign-authored quest templates
- Faction-aware quest variants

## Open Questions

- How strongly quests should be first-class in an emergent simulation-first design
- Whether quest state is actor-specific, campaign-wide, or both
