# Build Order

## Purpose

This file defines the phased implementation order so future work proceeds from canonical foundations outward. Phase boundaries are sequencing guidance, not a guarantee that every detail inside a phase is fully solved.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/05_build/CODEX_WORKFLOW.md`

## Phase 0: Documentation

Focus:

- Establish canon documents
- Lock ownership boundaries
- Define minimum contracts
- Record unresolved questions explicitly

Current canon maturity now includes:

- Shared actor-family decision for player and NPC specialization
- Travel subsystem definition at the canon level
- Explicit separation between event truth, memory, knowledge, and rumor
- Explicit separation between advisory AI flow and authoritative event history

Exit signal:

- Core canon and contract docs are present and internally consistent enough to guide implementation planning.

## Phase 1: Minimal Canonical Core

Focus:

- Create the minimal backend simulation core
- Define canonical identifiers and event emission interfaces
- Support deterministic state transition validation

Dependencies:

- Event model
- Core ownership rules

## Phase 2: Basic World And NPC State

Focus:

- Introduce canonical world and NPC state containers
- Apply the accepted shared actor-family baseline for player and NPC specialization
- Add location, time, faction links, and actor status placeholders
- Establish snapshot and persistence direction

Dependencies:

- World and NPC contracts
- Player-as-specialized-actor ADR
- Event linkage conventions

## Phase 3: Rules Engine

Focus:

- Implement deterministic resolution logic
- Lock basic outcome handling for gameplay actions
- Prevent AI or frontend bypass of rule authority
- Ground travel resolution on backend-owned route, time, interruption, and risk logic

Dependencies:

- Core state and event foundations

## Phase 4: Memory And Knowledge

Focus:

- Introduce memory and knowledge representation
- Define relationship between events, knowledge, recollection, and actor-specific views
- Treat rumor as first-class persisted information distinct from both memory and event truth

Dependencies:

- NPC state
- Event model
- Knowledge and relationship contracts
- Clarified persistence strategy

## Phase 5: AI Interpretation

Focus:

- Add AI-assisted classification, summarization, narration, and proposal workflows
- Keep all outputs advisory until backend-approved
- Preserve the separate advisory-log boundary from authoritative event history

Dependencies:

- Canonical state models
- Stable rule boundaries
- AI approval pathway definition

## Phase 6: Campaign Tools

Focus:

- Build campaign authoring and inspection tools
- Support dashboard workflows without changing truth ownership

Dependencies:

- Stable contracts and publish rules for tool-created data

## Phase 7: Client / Presentation

Focus:

- Build player-facing presentation layers
- Keep client logic replaceable and state-derived

Dependencies:

- Stable adapters
- Stable canonical read models

## TODO

- Define concrete phase exit criteria once implementation planning begins.
- Clarify whether save/load belongs in Phase 1 or Phase 2.
- Identify which current canon areas are stable enough to support narrow implementation planning first without opening fresh architecture questions.
