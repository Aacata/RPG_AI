# System Map

## Purpose

This file describes the current top-level architecture layers and their intended boundaries. It is a map, not a detailed specification. Detailed ownership and contracts live in the system and contract documents.

Cross-reference:

- Canon entry point: `docs/02_canon/PROJECT_BRAIN.md`
- Ownership rules: `docs/02_canon/DATA_OWNERSHIP.md`
- AI operating boundaries: `docs/02_canon/AI_BOUNDARY_RULES.md`
- Relationship contract: `docs/04_contracts/RELATIONSHIP_MODEL.md`
- Knowledge contract: `docs/04_contracts/KNOWLEDGE_MODEL.md`

## Layered Architecture

### 1. Core Simulation Layer

Purpose:

- Host deterministic orchestration, shared simulation primitives, and authoritative state transition coordination.

Examples of concerns:

- Simulation tick or step orchestration
- Canonical entity identifiers
- Event emission interfaces
- Validation of proposed state changes

Non-goals:

- Presentation formatting
- Narrative styling
- Dashboard-specific workflows

Primary repo areas:

- `src/core`
- `src/events`

### 2. NPC / Actor Simulation Layer

Purpose:

- Represent actor state and actor-facing inputs to simulation.

Examples of concerns:

- Identity, traits, goals, relationships, activity state
- Links to memory, inventory, factions, and location
- Shared actor-family baseline for player and NPC structures, with different agency and visibility handling
- Dynamic NPC priority tiers, including companion or major-character tier

Primary repo areas:

- `src/npc`
- `src/memory`
- `src/inventory`

### 3. Society / World Dynamics Layer

Purpose:

- Represent world-scale state beyond a single actor.

Examples of concerns:

- Locations and regions
- Time and calendar
- Weather and environment
- Travel topology and travel conditions
- Faction presence and group-level dynamics
- Social and political placeholders

Primary repo areas:

- `src/world`
- `src/factions`

### 4. Gameplay / Rules Layer

Purpose:

- Resolve deterministic gameplay outcomes according to campaign rules.

Examples of concerns:

- Combat resolution
- Skill checks
- Resource transfer rules
- Quest state transitions validated by rules
- Travel-time, travel-risk, interruption, and route validation logic

Primary repo areas:

- `src/rules`
- `src/quests`

### 5. AI Interpretation Layer

Purpose:

- Interpret canonical state and events for narration, summarization, classification, and proposed changes.

Examples of concerns:

- Dialogue framing
- Event summarization
- Candidate action proposals
- Classification of ambiguous player input

Non-goals:

- Authoritative deterministic resolution
- Direct mutation of canonical state without backend approval

Primary repo area:

- `src/ai`

### 6. Campaign Tooling Layer

Purpose:

- Support campaign creation, inspection, balancing, and scenario setup.

Examples of concerns:

- Dashboard workflows
- Configuration editing
- Scenario authoring
- Simulation inspection utilities

Non-goals:

- Becoming the canonical owner of runtime state

Primary repo areas:

- `src/tools`
- `/tools`

### 7. Presentation / Client Layer

Purpose:

- Render state for players or operators and collect user input.

Examples of concerns:

- UI screens
- View models
- Interaction affordances
- Transport adapters

Non-goals:

- Defining truth
- Replacing deterministic backend rule resolution

Primary repo area:

- `src/adapters`

### 8. Debug / Inspection Layer

Purpose:

- Make simulation history and state intelligible to humans without changing ownership rules.

Examples of concerns:

- Event viewers
- Replay tools
- Contract validation reports
- State diff inspection

Likely repo areas:

- `/tools`
- `src/tools`
- test and reporting utilities

## Cross-Cutting Subsystem Notes

### Travel Subsystem

Travel is a hybrid subsystem spanning world state, actor state, deterministic rules, event history, and AI narration boundaries.

- World and related contracts provide topology, terrain, weather, biome, and faction-context inputs.
- Rules and core logic own route validity, travel time, interruption logic, and authoritative travel outcomes.
- Actor systems provide schedules, goals, burden, skills, companion influence, and local intent inputs.
- AI may narrate travel or frame likely risk, but does not determine authoritative travel results.

Primary documentation:

- `docs/03_systems/TRAVEL_SYSTEM.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- Long-distance travel initiation is map-driven, while local travel may come from direct intent and remain interruptible.

### Actor Information Boundary

The actor-information boundary is intentionally split across several contracts:

- Event truth remains immutable history.
- Memory tracks actor-linked recollection grounded in authoritative history or approved observation.
- Knowledge tracks what an actor knows or believes.
- Rumor tracks socially propagated, potentially distorted information.
- Relationship state tracks social ties and dynamic relational metrics.

Primary documentation:

- `docs/03_systems/MEMORY_SYSTEM.md`
- `docs/03_systems/NPC_SYSTEM.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/04_contracts/RELATIONSHIP_MODEL.md`

### Advisory AI Flow Boundary

The advisory AI flow remains separate from authoritative history:

- Narrator AI and local specialist AI may participate in advisory proposal exchange.
- Backend validation remains the authority for deterministic outcomes and canonical state change.
- A separate advisory log may persist proposals and rejections without turning them into event truth.

Primary documentation:

- `docs/03_systems/AI_INTERPRETATION_SYSTEM.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`

## Current Dependency Direction

Preferred direction is inward toward canonical state:

`presentation/tooling -> adapters/ai -> core + systems + contracts -> events/history`

The exact runtime dependency graph remains a `TODO`, but the ownership direction is already fixed: outer layers consume or request changes to canonical systems; they do not own canonical truth.

## TODO

- Define the inspection boundary between `/tools` and `src/tools`.
- Add a concrete runtime diagram once implementation planning begins.

## Resolved

- `events` remains a standalone module at `src/events/` that the core runtime imports. Conceptual separation between event truth and core orchestration is preserved. See `docs/02_canon/BUILD_ORDER.md` Phase 1 for the canonical record of this decision.
