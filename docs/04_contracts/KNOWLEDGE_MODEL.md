# Knowledge Model

## Purpose

Define the conceptual boundary between event truth, memory, knowledge, and rumor so actor information handling remains correct and auditable.

Cross-reference:

- `docs/04_contracts/EVENT_MODEL.md`
- `docs/03_systems/MEMORY_SYSTEM.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`

## Core Distinctions

### Event Truth

- Immutable authoritative record of what happened
- Canonical simulation truth
- Not replaced by summaries, beliefs, or rumor

### Memory

- Actor-linked remembered record or recollection reference grounded in canonical event truth or approved observation
- Backend memory used for simulation truth is not false
- May vary in salience or accessibility without becoming untrue

### Knowledge

- What an actor knows or believes they know
- May be incomplete, false, distorted, hidden, delayed, or perspective-limited
- Canonical as belief-state, not canonical as world truth
- May exist at actor level and faction or institution level

### Rumor

- Socially propagated information moving through actors, factions, or institutions
- May distort truth while retaining some underlying signal
- May vary by setting in speed, reach, and transmission channel
- Canonically treated as a first-class persisted information type

## Knowledge Record Concept

Minimum conceptual areas:

- Owning actor or audience reference
- Owning faction or institutional audience reference where collective knowledge applies
- Subject reference
- Source type placeholder such as direct observation, memory, report, institution, or rumor
- Confidence or certainty placeholder
- Visibility or secrecy placeholder
- Freshness or delay placeholder
- Truth-status unknown placeholder

This is a conceptual model only. Field shapes remain a `TODO`.

## Rumor Record Concept

Rumor is canonically first-class at the persistence-model level. Implementation may realize that as a dedicated rumor schema or as a first-class subtype within a broader information-record family, but canon no longer treats rumor as optional or merely incidental propagation metadata.

Minimum conceptual areas:

- Rumor identifier
- Origin or source placeholder
- Subject placeholder
- Propagation channel placeholder
- Distortion or signal-retention placeholder
- Reach or audience placeholder
- Freshness, decay, or spread-speed placeholder

Setting-dependent channels may include courier-like systems, magical channels, internet-like systems, or social-media-like systems.

## Rumor Boundary

- Rumor is not identical to memory.
- Rumor is not identical to authoritative event truth.
- Rumor may produce or update actor knowledge state.
- Rumor may also produce faction-level or institution-level knowledge state.
- Rumor speed and channel rules may vary by campaign setting.

## Crime, Witness, And Response Integration

- Witnessed events may produce memory and then knowledge effects for specific actors.
- Knowledge and rumor boundaries should govern how crime awareness spreads.
- Wanted-state propagation, faction-law response, and social suspicion should use knowledge and rumor handling rather than bypassing them with omniscient truth.

## AI Reveal Boundary

- AI may summarize or reveal only what the player can reasonably know from the current viewpoint unless an approved tooling or debug context says otherwise.
- AI may use broader canonical context for framing, but hidden knowledge must not leak into player-facing output improperly.

## TODO

- Define minimum required fields for knowledge records.
- Clarify whether institutions or factions maintain separate collective-knowledge models.
- Clarify whether rumor persistence should use a dedicated rumor schema or a specialized subtype within a broader information-record family.
