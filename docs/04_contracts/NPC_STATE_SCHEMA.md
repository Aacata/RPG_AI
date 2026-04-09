# NPC State Schema

## Purpose

Define the minimum conceptual contract for canonical NPC state within the shared actor-family baseline also used by the player model. This is a schema blueprint, not an implementation.

Cross-reference:

- `docs/03_systems/NPC_SYSTEM.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/04_contracts/RELATIONSHIP_MODEL.md`
- `docs/06_decisions/ADR_PLAYER_AS_ACTOR.md`

## Structural Framing

- Player and NPC share the same foundational actor baseline.
- Player is a specialized actor from the same structural family, but differs in agency source, perspective, and information handling.
- Backend owns canonical player state even though the human player supplies input.
- Some NPC-oriented internal fields do not need to be mirrored for direct player use, especially hidden-agenda or certain rumor and internal-disposition fields.

This file retains the `NPC_STATE_SCHEMA` name for repository continuity, but its baseline sections should be read as actor-family structure unless a later ADR replaces it with a dedicated actor contract.

## Minimum Schema Areas

### Identity

- Canonical NPC ID
- Shared actor-ID space preferred if it simplifies implementation and preserves specialization boundaries
- Display name placeholder
- Origin or archetype placeholder

### Actor Family / Specialization

- Shared actor-family identifier or schema version placeholder
- Actor branch marker such as player or NPC specialization
- Perspective or information-handling placeholder
- Agency-source placeholder such as human input or simulation-driven behavior
- Shared core-logic compatibility placeholder

### Category

- NPC category or role placeholder
- Optional campaign-specific classification hook
- Priority tier placeholder such as background, person-of-interest, plot-relevant, ally/rival/antagonist, or companion or major-character tier

### Stats

- Deterministic stat container placeholder
- TODO: define whether stats are numeric-only or support richer typed values

### Skills

- Skill container placeholder
- TODO: define campaign-specific extensibility model

### Traits / Personality

- Stable trait anchors
- Personality descriptors as canonical or semi-canonical fields
- Voice or personality consistency anchors where needed for interpretation
- TODO: define how much of personality is deterministic input versus descriptive metadata

### Emotions / State

- Current emotional or mental-state placeholder
- Temporary condition flags
- TODO: define how these fields are updated and validated

### Relationships

- References to relationship records defined in `RELATIONSHIP_MODEL.md`
- Family-tie references
- Companion-status linkage placeholder where applicable

### Faction Links

- Membership references
- Standing or rank placeholder

### Knowledge

- Knowledge references or knowledge state placeholder
- Rumor-exposure references or visibility placeholder
- TODO: clarify how much knowledge state is stored inline versus by reference

### Memories

- Memory references
- Memory salience or access placeholder
- TODO: backend memory used for simulation truth is not false; subjective false belief belongs to knowledge or rumor state instead

### Inventory Links

- Inventory or possession references

### Location

- Current location ID
- Region or travel context placeholder

### Current Activity

- Active task or behavior placeholder
- Travel-state reference placeholder where movement is in progress

### Goals

- Short-term and long-term goal placeholders
- Player-goal visibility placeholder if player and NPC specializations diverge in presentation or hiddenness

Player specialization may still support goal-compatible fields for time-skip, long-stay, or related backend-managed behavior.

### Schedule

- Optional schedule reference or schedule state placeholder

Player specialization may still support schedule-compatible fields where backend time progression or long-stay handling benefits from them.

### Internal / Hidden NPC Fields

- Optional hidden-agenda placeholder
- Optional internal rumor or suspicion placeholder
- Optional private disposition or conviction-pressure placeholder

These fields are NPC-facing placeholders and should not be assumed to mirror directly into player-facing structure. Player specialization should not own a hidden-agenda field.

### Status Flags

- Alive / active / incapacitated placeholders
- Other deterministic flags as needed

## TODO

- Define mandatory versus optional fields.
- Define which fields are common actor-family baseline versus NPC-only specialization fields.
- Define versioning strategy for campaign-specific schema extension.
- Define whether companion tier is stored inline, derived from relationship state, or both.
- Clarify whether shared actor-ID and shared core logic should remain a preference or be promoted into a stricter contract rule later.
