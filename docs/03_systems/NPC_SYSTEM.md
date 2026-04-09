# NPC System

## Purpose

Represent canonical NPC actor state within a shared actor-family baseline that is also used by the player model. The player is a specialized actor from the same structural family, but NPCs remain the simulation-driven branch with their own behavior, visibility, and internal-state needs.

Cross-reference:

- `docs/04_contracts/NPC_STATE_SCHEMA.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/04_contracts/RELATIONSHIP_MODEL.md`
- `docs/03_systems/COMPANION_SYSTEM.md`
- `docs/06_decisions/ADR_PLAYER_AS_ACTOR.md`

## Responsibilities

- Maintain canonical NPC identity and status
- Apply the shared actor-family baseline to NPCs while preserving NPC-specific internal state where needed
- Preserve compatibility with a shared base actor ID space and shared core actor logic if that simplifies implementation without blurring specialization boundaries
- Track stats, skills, traits, and current state fields
- Link NPCs to factions, inventory, memories, knowledge, and locations
- Track NPC priority tier or importance tier, including companion or major-character status
- Expose NPC-specific agency inputs such as schedule, goals, role pressure, and simulation-driven autonomy
- Expose actor state needed by rules, quests, and AI interpretation

## Non-Responsibilities

- Owning the human player's input loop or UI perspective rules
- Assigning player-only exclusions such as hidden-agenda absence to frontend presentation instead of to actor-model boundaries
- Determining authoritative outcomes without rules involvement
- Owning immutable event history
- Owning UI dialogue presentation
- Replacing memory, inventory, or faction systems
- Replacing the relationship contract with ad hoc per-NPC fields
- Treating companion status as a separate actor species outside the NPC model

## Inputs

- Rule-approved state changes
- World location references
- Memory and knowledge references
- Relationship state references
- Faction link updates
- Inventory links
- Travel state, route, and interruption context where relevant
- Human player actions only as external interaction inputs, not as NPC agency drivers

## Outputs

- Canonical actor state views
- NPC agency and autonomy inputs for rules, scheduling, travel, and AI interpretation
- NPC tier and companion-status signals for systems that need deeper modeling depth
- Relationship inputs for memory, quest, faction, and AI systems
- Status flags consumed by deterministic rules

## Owned Data

- Shared actor-family baseline fields used by NPC instances
- Identity fields
- Category and role placeholders
- Stats and skills
- Traits and personality anchors
- Emotions or current actor state fields
- Goals and current activity
- Relationship links
- Priority tier or modeling-depth tier
- NPC-only internal fields where approved, such as hidden agenda or internal rumor/disposition tracking that should not be mirrored directly for player-facing use

Player specialization may still use shared goal or schedule-compatible fields for time-skip, long-stay, or similar backend-managed behavior, but player specialization should not own a hidden-agenda field.

## Dependencies

- `core` for orchestration and entity IDs
- `world` for location references
- `memory` for memory linkage
- `inventory` for possession linkage
- `factions` for affiliation linkage
- `travel` for active route and travel-state interaction
- `relationship` contract for baseline and dynamic social state
- `rules` for authoritative state transitions

## Likely Future Extensions

- Schedule modeling
- Social role templates
- Per-campaign stat or trait overlays
- Dynamic tier promotion and demotion between background, person-of-interest, plot-relevant, ally/rival/antagonist, and companion or major-character tiers
- Shared actor-core utilities reused by both player and NPC specializations

## Open Questions

- Whether the shared actor-family baseline should eventually be renamed into a dedicated actor contract without disrupting current doc structure
- How emotions are represented without letting narrative interpretation become authoritative
- How deep schedule support should go in the MVP
- Which NPC-only internal fields need explicit contract treatment instead of remaining implementation-detail placeholders
- Whether shared base ID and shared core actor logic should be documented as a hard requirement or remain an implementation preference
