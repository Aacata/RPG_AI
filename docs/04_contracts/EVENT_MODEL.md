# Event Model

## Purpose

Define the canonical concept of an event so simulation history remains auditable, replayable, and distinguishable from summaries or interpreted text.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/03_systems/MEMORY_SYSTEM.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`

## What An Event Is

An event is an immutable record of an authoritative occurrence or state transition relevant to the simulation. It should be durable enough to support auditability and replay while remaining distinct from presentation-layer narrative.

At minimum, an event will likely require:

- A unique event identifier
- A timestamp or simulation-time reference
- A category
- References to affected entities
- A payload describing the authoritative occurrence
- Versioning or schema metadata

The exact field-level schema remains a `TODO`.

## Immutable Event Principles

- Events are append-only.
- Events are not rewritten to improve narration.
- Corrections, reversals, or compensations should be represented as new events unless a later canon document defines a tightly controlled exception.
- Summaries may reference events, but may not replace them as canonical history.
- Actor belief, rumor, or memory state may derive from events, but they do not redefine event truth.

## Event Categories

Seed categories, subject to refinement:

- `WORLD`
- `NPC`
- `RULES_OUTCOME`
- `COMBAT`
- `INVENTORY`
- `QUEST`
- `FACTION`
- `TRAVEL`
- `RELATIONSHIP`
- `SYSTEM`

These categories are directional placeholders and are not yet a locked enum.

## Event Linkage To Entity IDs

Events should link to canonical entity IDs rather than presentation-layer identifiers. Linkage should support:

- Primary subject entity
- Secondary or related entities
- Location references
- Faction references where relevant
- Travel, route, or region references where relevant

## Event Truth Versus Memory, Knowledge, And Rumor

- Event truth records what authoritatively happened.
- Memory records may reference events as remembered source material.
- Knowledge records what an actor knows or believes.
- Rumor records socially propagated, possibly distorted information.

Events may feed these downstream layers, but those downstream layers do not retroactively redefine events.

## Relation To AI Proposals

- Advisory AI outputs are not authoritative events by default.
- AI proposals should remain distinct from the authoritative event history until backend approval occurs.
- A separate advisory log should exist in addition to the immutable authoritative event archive.
- Approved proposals may lead to authoritative events that optionally reference the proposal record that preceded them.
- Rejected proposals may remain logged in a separate advisory record flow, but rejection does not create new historical truth about the world unless the backend explicitly emits an authoritative event about the rejection itself.

## Relation To Snapshots, Replay, And Summaries

- Snapshots are state captures derived from canonical state at a point in time; they are not replacements for event history.
- Replay should consume immutable events and any required deterministic reconstruction rules.
- Summaries are derived artifacts that help humans or AI systems understand history faster, but summaries are not canonical truth.
- Knowledge, rumor, and memory reconstruction may consult events during replay or inspection, but they remain distinct layers.

## TODO

- Define the minimum required event fields.
- Decide whether event payloads are strongly typed per category or share a base envelope plus typed detail blocks.
- Clarify how savegames reference event history and snapshots together.
- Clarify whether the advisory log shares storage infrastructure with events while remaining logically distinct from the authoritative stream.
