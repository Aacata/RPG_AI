# Relationship Model

## Purpose

Define the boundary for baseline social ties and dynamic relationship state between actors.

Cross-reference:

- `docs/03_systems/NPC_SYSTEM.md`
- `docs/03_systems/COMPANION_SYSTEM.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

## Baseline Principles

- Family ties are immutable baseline relationship facts.
- Other relationship states are dynamic.
- Emotional state and relationship state are related but not identical.
- Companion status is strongly connected to relationship state, but is not identical to it.

## Relationship Record Concept

Minimum conceptual areas:

- Relationship record identifier
- Primary actor reference
- Secondary actor reference
- Baseline relationship facts
- Dynamic relationship metrics
- Context modifiers placeholder
- Versioning or audit placeholder

## Immutable Baseline Facts

Examples:

- Family ties
- Kinship structure
- Baseline guardianship or lineage facts if approved later

Immutable baseline facts may be supplemented by later discoveries, but they should not be treated as ordinary mutable disposition values.

## Dynamic Relationship Metrics

The MVP relationship model includes the following default axes:

- Disposition as a central signed scale such as `-100` to `100`
- Trust axis
- Fear axis
- Loyalty axis
- Affection axis
- Resentment axis

These axes are canonically locked as MVP-level default relationship axes. Additional axes may be added later if canon requires them, but these defaults should not be treated as optional for MVP-level relationship modeling.

## Influences On Relationship Change

Relationship change may be influenced by:

- Alignment or morality derived in part from traits, actions, faction context, and related factors rather than assumed to be a rigid standalone field
- Faction context
- Internal convictions
- Emotional state
- Memory and knowledge
- Rule-approved actions and outcomes

## Conviction And Manipulation Boundary

- Manipulated behavior against internal convictions may create shame, regret, corruption, apathy, fear, or rupture.
- These effects may influence relationship state, but they are not synonymous with relationship state.
- Companion status may be affected by relationship rupture, but it remains a separate designation.

## TODO

- Clarify whether relationship records are directional, bidirectional, or both.
- Clarify how faction-mediated relationships interact with person-to-person records.
