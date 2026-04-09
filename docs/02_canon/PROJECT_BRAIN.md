# Project Brain

## Mission

Build an offline AI-driven RPG simulation engine in which the simulation core remains the canonical source of truth, AI serves as a constrained interpretive layer, and presentation surfaces remain replaceable across multiple campaign genres.

## Design Philosophy

- Simulation first: story should emerge from world state, rules, events, and actor behavior.
- Deterministic logic stays backend-owned.
- AI augments interpretation and presentation but does not own authoritative outcomes.
- Documentation defines scope, ownership, and sequencing before implementation.
- Visionary concepts require review before becoming canon.
- The architecture must support varied campaign settings without reassigning truth ownership.

## Architecture Overview

The repository is divided into layers rather than feature bundles:

- Canon and governance documents define the rules of the system.
- Core simulation systems own deterministic state transitions and event generation.
- AI systems interpret existing state and may propose changes for backend validation.
- Tooling systems support campaign authoring, debugging, and inspection without becoming simulation authority.
- Client and adapter layers present state to users without owning truth.

See `docs/02_canon/SYSTEM_MAP.md` for the current layer map and `docs/02_canon/BUILD_ORDER.md` for sequencing.

## Simulation Truth Principles

- Canonical game truth resides in backend-managed state and event history.
- Deterministic outcomes such as combat resolution, inventory mutation, quest state transitions, and rules enforcement must be reproducible without requiring AI agreement.
- Event history must be auditable and suitable for replay or inspection.
- Summaries are convenience artifacts, not canonical history.

Related documents:

- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/04_contracts/EVENT_MODEL.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

## AI Boundary Principles

- AI may interpret, classify, summarize, narrate, and propose state changes.
- AI may not directly decide deterministic outcomes or overwrite backend authority.
- AI output must be treated as advisory until validated by deterministic systems or explicit approval rules defined in canon.

See `docs/02_canon/AI_BOUNDARY_RULES.md` for operating constraints.

## Frontend Boundary Principles

- Frontend code is a presentation layer, not the owner of canonical world or actor state.
- UI-specific view models may exist, but they derive from backend truth.
- Replacing one client should not require redefining simulation contracts.
- Campaign tooling dashboards are also non-canonical surfaces, even when they expose powerful controls.

## System Map Summary

Current top-level system areas:

- `core`: Canonical simulation orchestration and shared primitives.
- `world`: Locations, regions, time, weather, and world-level state.
- `npc`: Shared actor-family baseline for NPCs and player specialization, plus NPC-specific behavior inputs.
- `memory`: Memory and knowledge representation.
- `events`: Immutable event history and event queries.
- `factions`: Group-level affiliations and dynamics.
- `rules`: Deterministic resolution logic.
- `inventory`: Item state and possession links.
- `quests`: Structured objective and progression state.
- `ai`: Interpretation, summarization, and proposal generation.
- `adapters`: Boundary layer for clients and external surfaces.
- `tools`: Campaign tooling, debug, and inspection support.
- `travel`: Hybrid subsystem spanning world state, actor state, rules, and event history.
- `companion`: Dynamic high-priority NPC tier, not a separate actor family.

## Reading Order For Future Contributors And Agents

1. This file
2. `docs/02_canon/SYSTEM_MAP.md`
3. `docs/02_canon/DATA_OWNERSHIP.md`
4. `docs/02_canon/AI_BOUNDARY_RULES.md`
5. `docs/02_canon/BUILD_ORDER.md`
6. Relevant system documents in `docs/03_systems/`
7. Relevant contracts in `docs/04_contracts/`
8. `docs/05_build/CODEX_WORKFLOW.md`

## TODO

- Define the minimal canonical runtime boundary inside `src/core` once implementation planning begins.
- Import any historical architecture notes into `legacy_reference/` before treating them as inputs to canon.
- Clarify whether the shared actor-family baseline should eventually be renamed into a dedicated actor contract or remain anchored under current NPC naming.
