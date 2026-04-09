# Faction System

## Purpose

Represent canonical group affiliations and group-level state that influence the broader simulation.

Cross-reference:

- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

## Responsibilities

- Maintain faction identity and membership links
- Represent faction-level standing or influence placeholders
- Link factions to world locations, actors, and active world conditions
- Expose faction context to rules, quests, and AI interpretation

## Non-Responsibilities

- Owning individual NPC personality or inventory
- Acting as a frontend guild or menu model
- Narrating faction conflict outcomes authoritatively
- Replacing a future politics or economy subsystem if one is later approved

## Inputs

- Membership and relationship changes approved by rules
- World references
- Quest or event references

## Outputs

- Faction linkage data for NPC, world, and quest systems
- Group context for AI summaries or campaign tooling

## Owned Data

- Faction identifiers
- Membership links
- Standing and influence placeholders
- Faction-world linkage placeholders

## Dependencies

- `core` for identifiers
- `world` for location and region context
- `npc` for member links
- `rules` for authoritative updates
- `events` for historical linkage

## Likely Future Extensions

- Reputation matrices
- Territory control
- Politics and diplomacy
- Resource ownership

## Open Questions

- Whether faction relations belong inside this system or a future society subsystem
- How campaign-specific faction rules plug in without destabilizing the architecture
