# Memory System

## Purpose

Represent how actors retain, access, and reference remembered information without replacing immutable event history.

Cross-reference:

- `docs/04_contracts/EVENT_MODEL.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`

## Responsibilities

- Store actor-linked memory references or memory records
- Distinguish between canonical event truth, actor memory, actor knowledge, and rumor propagation
- Support recollection queries without collapsing them into authoritative event history
- Provide memory-grounded inputs to knowledge handling and AI interpretation
- Preserve auditability of what is source history versus derived memory state
- Preserve the rule that backend memory used for simulation truth is not false

## Non-Responsibilities

- Acting as the sole source of truth for what happened
- Owning actor belief-state in general
- Owning rumor propagation as a whole social system
- Overwriting immutable events with summaries
- Owning deterministic rules resolution
- Owning frontend conversation history formatting
- Treating witness belief, suspicion, or rumor as the same thing as memory

## Inputs

- Immutable event references
- Rule-approved memory updates
- NPC identity and relationship context
- Knowledge and rumor references where recollection affects propagation
- Potential AI-generated memory proposals subject to approval rules

## Outputs

- Actor memory references
- Knowledge availability inputs grounded in approved memory state
- Recollection context for AI interpretation or rule checks if canon later permits it
- Witness and observation linkage inputs that downstream knowledge or rumor systems may consume
- Inputs that faction-level knowledge or rumor propagation systems may consume when collective awareness matters

## Owned Data

- Memory records or references
- Memory-source linkage to canonical events or approved observation
- Memory salience and access metadata placeholders

Canonical false belief does not belong to memory ownership. If an actor believes something false, that belongs to knowledge or rumor state rather than to backend memory truth.

## Dependencies

- `events` for source history
- `npc` for actor linkage
- `knowledge` contract for belief-state boundaries
- `rules` for approved changes
- `ai` only for advisory proposals, never direct authority

## Likely Future Extensions

- Memory decay
- Subjective recollection overlays that remain distinct from simulation-truth memory
- Shared knowledge propagation
- Faction-level information diffusion
- Crime witness and law-response hooks through knowledge boundaries

## Open Questions

- Which memory fields are canonical in MVP versus later
- Whether memory stores event references only or allows richer derived records
- Whether subjective recollection should ever be modeled separately from canonical backend memory
