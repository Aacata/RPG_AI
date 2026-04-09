# Savegame Schema

## Purpose

Define the conceptual structure of savegame data without locking implementation details prematurely.

Cross-reference:

- `docs/02_canon/BUILD_ORDER.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`
- `docs/06_decisions/ADR_PLAYER_AS_ACTOR.md`

## Save Slot Model

Minimum conceptual areas:

- Save slot identifier
- Human-readable label placeholder
- Creation timestamp
- Last updated timestamp
- Active campaign reference placeholder

## World Snapshot References

- Reference to canonical world snapshot data
- Optional event history checkpoint reference
- TODO: define whether savegames store full snapshots, deltas, or both

## Player State

- Player state snapshot or reference within the shared actor-family baseline
- Player-specialization data placeholder within that shared actor-family structure

The accepted architecture decision is that player and NPC share a foundational actor baseline. Save handling should therefore treat player state as canonical actor-family state with player specialization, not as a reopened player-versus-NPC architecture question.

## NPC State References

- References to canonical NPC state snapshot data
- TODO: define whether all NPCs are serialized or only active/known subsets

## Quest Progress

- Quest progression references
- Objective state placeholder

## Metadata And Versioning Strategy

- Save format version
- Campaign ruleset version placeholder
- Compatibility metadata placeholder
- Validation status placeholder

## TODO

- Define savegame granularity relative to event replay.
- Define how shared actor-family snapshots are partitioned between player specialization and NPC specialization during serialization.
- Define persistence boundary between runtime state, authored campaign data, and tool-owned drafts.
- Define whether save slots store actor snapshots directly, references to actor snapshots, or a mixed model.
- Decide whether save migrations require dedicated ADR coverage.
