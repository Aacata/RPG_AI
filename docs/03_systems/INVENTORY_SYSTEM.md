# Inventory System

## Purpose

Represent canonical item possession and item-state relationships within the simulation.

Cross-reference:

- `docs/04_contracts/NPC_STATE_SCHEMA.md`
- `docs/02_canon/DATA_OWNERSHIP.md`

## Responsibilities

- Track possession links between entities and items
- Represent item-state placeholders needed for deterministic rules
- Support transfers, consumption, and equipment state once rules are defined
- Expose inventory references to NPCs, quests, and rules

## Non-Responsibilities

- Rendering item cards or UI lists
- Freeform loot narration
- Determining outcome validity without rules approval
- Replacing a future item definition content pipeline if one is later added

## Inputs

- Rule-approved item mutations
- Entity references
- Quest or world linkage when items are location-based

## Outputs

- Inventory references for actors and locations
- Item state consumed by rules and AI interpretation

## Owned Data

- Item possession links
- Equipment placeholders
- Quantity or stack placeholders where relevant
- Item status flags

## Dependencies

- `core` for entity IDs
- `npc` and `world` for ownership or location references
- `rules` for deterministic transitions
- `events` for historical traceability

## Likely Future Extensions

- Containers
- Durability
- Crafting inputs and outputs
- Trade or economy integration

## Open Questions

- Where canonical item definitions live versus instance state
- How location-held inventory is represented in world state
