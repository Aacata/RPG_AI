# ADR: Player As Specialized Actor

## ADR Metadata

- ADR ID: ADR_PLAYER_AS_ACTOR
- Title: Player As Specialized Actor In A Shared Structural Family
- Date: 2026-04-08
- Status: Accepted
- Related Docs: `docs/03_systems/NPC_SYSTEM.md`, `docs/04_contracts/NPC_STATE_SCHEMA.md`, `docs/02_canon/DATA_OWNERSHIP.md`
- Related Candidates: None recorded at bootstrap time

## Context

The repository initially left open whether player state should be treated as fully separate from NPC state or whether both should share a deeper common structure. The approved design input clarifies that player and NPC belong to the same foundational actor family while still differing in agency source, perspective, and information handling.

## Decision

Player and NPC share a foundational actor baseline.

- Player is a specialized actor within the same structural family as NPCs.
- Backend owns canonical player state.
- NPCs remain the simulation-driven branch with support for schedules, goals, internal fields, and tiering such as companion status.
- Player specialization may still support goal and schedule-compatible fields where backend time progression or long-stay handling benefits from them.
- Player specialization should not include a hidden-agenda field.
- Player-facing structure does not need to mirror every NPC-only internal field.
- Shared base actor IDs and shared core actor logic are preferred if they simplify implementation without weakening specialization boundaries.

For repository continuity, the existing `NPC_STATE_SCHEMA.md` file remains in place for now, but it should be interpreted as defining the current actor-family baseline plus NPC specialization boundaries.

## Ownership Impact

- Backend owns canonical player and NPC state.
- Frontend owns player input collection and presentation only.
- AI may interpret player intent or narrate outcomes, but does not own player truth or deterministic results.

## Consequences

- Positive:
  - Reduces duplication between player and NPC structures.
  - Preserves a unified actor-model foundation.
  - Makes companion and relationship integration cleaner.
- Negative:
  - The current file naming may appear NPC-specific even though the baseline is broader.
  - Some fields require careful visibility handling so NPC-only internals are not mirrored into player-facing use.
- Tradeoffs:
  - The repository keeps current naming stability now, at the cost of a possible future rename to a dedicated actor contract.

## Alternatives Considered

- Alternative 1: Fully separate player and NPC schemas from the start.
- Alternative 2: Treat player as an NPC subtype with no visibility or agency distinctions.
- Alternative 3: Delay the decision and leave both models ambiguous.

## Follow-Up Required

- Canon files to update: completed in the related system and contract docs for this phase
- Contract files to update: completed for current scope
- Implementation impact: future code and persistence design should treat player and NPC as the same actor family with specialization boundaries
- Open questions: whether the actor-family baseline should eventually receive a renamed dedicated contract file
