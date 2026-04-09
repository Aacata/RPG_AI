# Companion System

## Purpose

Define companion behavior as a dynamic high-priority NPC tier rather than as a separate actor model. Companion status increases modeling depth and narrative relevance, but companions remain NPCs within the shared actor-family structure.

Cross-reference:

- `docs/03_systems/NPC_SYSTEM.md`
- `docs/04_contracts/RELATIONSHIP_MODEL.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

## Responsibilities

- Define companion as a dynamic NPC tier or status
- Support promotion and demotion between NPC importance tiers
- Support a general highest-importance tier while leaving exact tier names partially unresolved
- Support dynamic role labels such as friend, lover, rival, ally, spouse, archenemy, boss, or major character layered onto or within the prioritization model
- Expose deeper behavioral, emotional, relational, and autonomy signals for high-priority NPCs
- Support independent companion action, including self-chosen or assigned tasks away from the player
- Provide companion influence inputs to travel, group decisions, and social conflict

## Non-Responsibilities

- Creating a separate companion actor schema outside the NPC model
- Forcing companions to follow the player at all times
- Owning voice generation or presentation-layer speech styling
- Replacing deterministic rules for loyalty, refusal, conflict, or departure outcomes
- Locking tier vocabulary more rigidly than current canon supports

## Inputs

- NPC baseline state
- Relationship state
- Current emotional or situational state
- Goals, schedules, and role pressures
- World and travel context
- Player interactions
- Rule-approved state changes

## Outputs

- Companion-status or tier signals
- Group-behavior inputs
- Autonomy and task-allocation inputs
- AI interpretation inputs for companion-aware narration
- Travel and social-interruption influence inputs

## Owned Data

- Companion or major-character tier designation
- Modeling-depth markers for companion-level simulation
- Companion participation status placeholders
- Task-assignment and independence-status placeholders
- Dynamic role-layer placeholders associated with high-priority NPC status

Relationship metrics such as trust, loyalty, affection, fear, or resentment remain owned by the relationship contract rather than duplicated here.

Bosses and companions may share the same priority framework if that keeps the architecture simpler, but this remains a tiering-model decision rather than a claim that boss and companion behavior are identical.

## Dependencies

- `npc` for actor baseline and tier placement
- `relationship` contract for relational state
- `memory` and `knowledge` contracts for context
- `travel` for group-movement and objection influence
- `rules` for authoritative outcomes
- `ai` for non-canonical narration and interpretation

## Likely Future Extensions

- Companion group roles
- Loyalty crisis handling
- Manipulation and moral-conflict responses
- Major-character persistence policies

## Open Questions

- Which tier names should become canonical enums versus reference vocabulary
- Whether bosses and companions should share one explicit top-tier framework or only partially overlap within it
- Whether companion-level autonomy needs explicit state-machine contracts in MVP or later
- How much companion-group coordination is needed before party systems become their own subsystem
