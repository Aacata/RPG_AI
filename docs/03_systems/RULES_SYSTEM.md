# Rules System

## Purpose

Provide deterministic resolution logic for authoritative gameplay and simulation outcomes.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/EVENT_MODEL.md`

## Responsibilities

- Resolve deterministic outcomes
- Validate proposed state changes before canonical mutation
- Apply campaign rule variations without moving truth ownership away from the backend
- Emit or trigger event creation for authoritative outcomes

## Non-Responsibilities

- Freeform narrative generation
- Frontend interaction design
- Dashboard authoring workflows
- Replacing the event history model with summaries or interpretations

## Inputs

- Canonical world state
- Canonical NPC state
- Inventory, faction, and quest state
- User or AI proposed actions
- Campaign rule configuration once canon defines it

## Outputs

- Approved state transitions
- Deterministic outcome records
- Event payload inputs
- Rejection reasons when actions are invalid

## Owned Data

- Rule definitions and resolution policies
- Validation logic
- Campaign-specific rule variation hooks or configuration references

## Dependencies

- `core` for orchestration
- `world`, `npc`, `inventory`, `quests`, `factions` for state inputs
- `events` for authoritative history linkage

## Likely Future Extensions

- Combat resolution modules
- Skill checks
- Social resolution rules
- Per-campaign rule packages

## Open Questions

- How campaign rule variation is loaded and versioned
- Which parts of rules configuration become canonical data contracts
- Whether rules execution is synchronous only in MVP
