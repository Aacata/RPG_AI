# Session Manifest

## Purpose

This file is the compact entry point for a new agent or contributor session.
Read this file first. It tells you what the project is, what is canon, what is
already implemented, what remains undecided, and where to go next.

Do not implement anything from this file alone. Use it to orient yourself,
then follow the reading order below before making any changes.

---

## What This Project Is

An offline AI-driven RPG simulation engine. The simulation core is the canonical
source of truth. AI is a constrained interpretive and narrative layer. Presentation
surfaces are replaceable. The architecture supports multiple campaign genres without
reassigning truth ownership.

---

## One-Sentence Rules

- Backend owns all canonical state. AI advises. Frontend presents.
- Never implement from `docs/00_inbox/` alone.
- When in doubt, write a TODO instead of guessing.
- When docs and code conflict, stop and surface the conflict.

## Operational Reading Rules

- **Batched implementation and release:** follow [`docs/05_build/BUILD_DIRECTIVE.md`](BUILD_DIRECTIVE.md) (implement batch → self-review → drift/bugs → patch → commit → push → next batch until a human-input stop).
- A record, schema, or field existing does not mean the subsystem semantics are implemented.
- A helper existing does not mean it is integrated into the full proposed-change or authoritative-event pipeline.
- Current repo progress includes narrow slices. Do not misread a narrow slice as full subsystem completion.
- Future sessions must distinguish record existence, validated mutation support, helper-level behavior, and event-integrated behavior.

---

## Canonical Architecture At A Glance

| Layer | Owner | Examples |
|---|---|---|
| Simulation truth | Backend | World state, NPC state, event history |
| Deterministic rules | Backend | Roll resolution, skill checks, travel outcomes |
| AI interpretation | Advisory only | Narration, proposals, difficulty framing |
| Voice and audio | Adapter layer | GPT-SoVITS, Fish Speech, Kokoro, Stable Audio |
| Presentation | Frontend | UI, view models, player input collection |
| Campaign tooling | Tool layer | Authoring dashboards, debug, inspection |

---

## AI Stack Summary

| Role | Component | Cloud / Local |
|---|---|---|
| Strategic and narrative AI | Gemini | Cloud |
| Runtime modulation (FLOW) | Ollama (model TBD) | Local |
| Local text generation | Ollama (model TBD) | Local |
| Fast runtime voice | GPT-SoVITS | Local |
| Generic voice fallback | Kokoro TTS | Local |
| HQ offline dialogue | Fish Speech S2 Pro | Local |
| Voice seed generation | Tortoise TTS | Local |
| Ambient and SFX | Stable Audio Open | Local |

Only Gemini is a cloud dependency. All other components run locally.
ElevenLabs and other paid voice services are explicitly excluded.

---

## Core Rules System Summary

Resolution formula: `1d20 + attribute + skill_bonus + situational_bonus >= DC`

Attributes: `strength, agility, physique, psyche, intelligence, charisma, perception, luck`

- Attribute range: 1-9 at creation, max 10
- Untrained skill bonus: `floor(attribute / 2)`
- Skill scale: 0-20 normal, 21+ exceptional, no hard ceiling
- Natural 20: always critical success
- Natural 1: always critical failure, triggers passive luck save

Difficulty categories (AI proposes, backend translates to number):

| Category | Bonus |
|---|---|
| Routine | +15 |
| Trivial | +10 |
| Easy | +5 |
| Standard | 0 |
| Challenging | -5 |
| Hard | -10 |
| Extreme | -15 |
| Absurd | -25 |
| Impossible | BLOCKED |

---

## Current Canon Maturity

### Locked in canon

- Project mission and design philosophy (`PROJECT_BRAIN.md`)
- System map and layer boundaries (`SYSTEM_MAP.md`)
- Data ownership rules (`DATA_OWNERSHIP.md`)
- AI boundary rules (`AI_BOUNDARY_RULES.md`)
- Core resolution formula, attributes, and skill system (`RULES_SYSTEM.md`)
- AI stack and voice stack (`AI_STACK.md`, `VOICE_SYSTEM.md`)
- Player as specialized actor in shared actor family (`ADR_PLAYER_AS_ACTOR.md`)
- Event model principles (`EVENT_MODEL.md`)
- Knowledge, memory, and rumor separation (`KNOWLEDGE_MODEL.md`)
- Relationship model with locked MVP axes (`RELATIONSHIP_MODEL.md`)
- Build order phases (`BUILD_ORDER.md`)
- Agent and contributor operating rules (`AGENT_RULES.md`, `CODEX_WORKFLOW.md`)
- Autonomous build cycle directive (`BUILD_DIRECTIVE.md`)

### Partially defined - needs clarification before later implementation

- NPC importance tier names
- Exact XP formula and level thresholds
- HP multipliers and level scaling values
- FLOW model selection (Ollama model TBD)
- Save game granularity, snapshot cadence relative to event replay, and save-slot orchestration defaults (hybrid direction is recorded in `ADR_SAVE_LOAD_AND_PERSISTENCE.md`; operational defaults still TBD)
- Campaign configuration publication rules

### Not yet in canon - do not implement

- Anything in `docs/00_inbox/VISIONARY_IDEAS.md`
- Combat system details beyond the resolution formula and rules boundary
- Speech-to-text pipeline
- C++ core migration
- Godot or other frontend client integration
- Economy or politics subsystems

---

## Current Build Phase

Current implemented foundation:

- Phase 1 minimal canonical core implemented and tested
- Phase 1 validator hardening implemented and tested (pending-create-ID resolution for in-batch references, deepcopy-based atomic apply, broadened slot matrix, and all-or-nothing batch rejection)
- Phase 1 persistence MVP implemented and tested (SQLite schema versioning, append-only authoritative event storage with retrieval, versioned JSON snapshots of `StateRoot`, hybrid save/load direction recorded in ADR)
- Phase 2 basic world and actor state slice implemented and tested
- Phase 2 spatial publication v0 slice implemented and tested (atomic world_space + region + location publish via `process_proposed_change`)
- Phase 3 deterministic rules boundary MVP slice implemented and tested

Current status notes:

- Later rules-system expansion beyond the current MVP slice remains deferred
- Optional event tail after snapshot restore is not implemented; see `PHASE2_CLOSE_PLAN.md`
- Phase 4 memory and knowledge is not started

See `docs/02_canon/BUILD_ORDER.md` for full phase definitions.

---

## What Is Already Implemented

Implemented now:

- Typed canonical IDs
- Core mutation and event contracts
- Legal mutation surface and bounded validation
- All-or-nothing backend mutation approval path
- In-batch pending-create-ID resolution for cross-record references inside one `ProposedChange`
- Authoritative event handoff, event envelope builder, and runtime integration
- Canonical runtime entry point `process_proposed_change(...)` used by every event-integrated slice
- Minimal `StateRoot`
- Shared actor-family baseline for player and NPC specialization
- Basic world and actor state expansion fields
- Map MVP records: `WorldSpaceRecord`, `RegionRecord`, `LocationRecord`
- Narrow mutation and validation support for `RegionRecord.world_space_ref`
- Spatial publication v0: atomic `WorldSpace` + `Region` + `Location` publication via `process_proposed_change`
- Player map discovery storage in `StateRoot.player_map_discovery`
- Player map discovery read-model helper and backend update helpers
- Rules boundary MVP for `set_actor_current_activity`
- Demo and test harness files for rules boundary MVP, map discovery MVP, and spatial publication v0
- Focused contract and validation tests
- SQLite persistence MVP: `src/persistence/` (`EventRepository`, `SnapshotRepository`, `open_persistence`) with tests in `tests/test_persistence_phase1.py`

Still intentionally not implemented:

- Full deterministic gameplay rules engine
- Full map mutation-surface support for `LocationRecord.x/y/z/biome/is_hidden_by_default`
- Proposed-change/event-pipeline integration for map discovery helpers
- Travel subsystem
- Knowledge, rumor, and quest systems
- AI runtime execution
- Automatic persistence after every backend mutation (events must be appended explicitly or via a future orchestration hook)
- Full event-sourced replay from an empty base
- Frontend/gameplay client

---

## Required Reading Order Before Making Changes

1. This file
2. `docs/05_build/IMPLEMENTATION_STATUS.md`
3. `docs/02_canon/PROJECT_BRAIN.md`
4. `docs/02_canon/SYSTEM_MAP.md`
5. `docs/02_canon/DATA_OWNERSHIP.md`
6. `docs/02_canon/AI_BOUNDARY_RULES.md`
7. `docs/02_canon/BUILD_ORDER.md`
8. `docs/03_systems/RULES_SYSTEM.md`
9. Relevant system files in `docs/03_systems/`
10. Relevant contract files in `docs/04_contracts/`
11. `docs/05_build/CODEX_WORKFLOW.md`

If the task touches AI or voice, also read:

- `docs/03_systems/AI_STACK.md`
- `docs/03_systems/VOICE_SYSTEM.md`

If the task is a review or gatekeeping pass, also read:

- `docs/05_build/REVIEWER_GATEKEEPER.md`

---

## Key File Locations

### Canon

- `docs/02_canon/PROJECT_BRAIN.md` - mission, philosophy, architecture overview
- `docs/02_canon/SYSTEM_MAP.md` - layer map and system boundaries
- `docs/02_canon/DATA_OWNERSHIP.md` - who owns what data
- `docs/02_canon/AI_BOUNDARY_RULES.md` - what AI may and may not do
- `docs/02_canon/BUILD_ORDER.md` - phased implementation order

### Systems

- `docs/03_systems/RULES_SYSTEM.md` - resolution formula, attributes, skills
- `docs/03_systems/AI_STACK.md` - concrete AI and voice components
- `docs/03_systems/VOICE_SYSTEM.md` - voice pipeline, routing, factory
- `docs/03_systems/NPC_SYSTEM.md` - actor model and NPC state
- `docs/03_systems/WORLD_SYSTEM.md` - world state, locations, time
- `docs/03_systems/MEMORY_SYSTEM.md` - memory, knowledge, rumor separation
- `docs/03_systems/COMPANION_SYSTEM.md` - companion tier definition
- `docs/03_systems/TRAVEL_SYSTEM.md` - travel subsystem
- `docs/03_systems/FACTION_SYSTEM.md` - faction and group state
- `docs/03_systems/QUEST_SYSTEM.md` - structured objective state
- `docs/03_systems/INVENTORY_SYSTEM.md` - item possession and state
- `docs/03_systems/AI_INTERPRETATION_SYSTEM.md` - AI interpretation boundaries

### Contracts

- `docs/04_contracts/EVENT_MODEL.md` - immutable event history
- `docs/04_contracts/NPC_STATE_SCHEMA.md` - actor family baseline
- `docs/04_contracts/WORLD_STATE_SCHEMA.md` - world state schema
- `docs/04_contracts/KNOWLEDGE_MODEL.md` - knowledge and rumor model
- `docs/04_contracts/RELATIONSHIP_MODEL.md` - relationship axes
- `docs/04_contracts/AI_PROPOSAL_FLOW.md` - advisory proposal lifecycle
- `docs/04_contracts/SAVEGAME_SCHEMA.md` - save slot structure

### Build

- `docs/05_build/SESSION_MANIFEST.md` - compact session entry point
- `docs/05_build/IMPLEMENTATION_STATUS.md` - blunt implementation boundary snapshot
- `docs/05_build/CODEX_WORKFLOW.md` - agent operating rules
- `docs/05_build/REVIEWER_GATEKEEPER.md` - reviewer and gatekeeping operating profile
- `docs/05_build/PHASE2_CLOSE_PLAN.md` - remaining Phase 2 close items after persistence MVP
- `docs/05_build/DEBUG_INSPECTION_UI.md` - Phase 6 inspection UI scope (CLI-first v0)
- `AGENT_RULES.md` - non-negotiable agent constraints
- `docs/05_build/PROMPT_PATTERNS.md` - reusable prompt templates

### Decisions

- `docs/06_decisions/ADR_PLAYER_AS_ACTOR.md` - player in shared actor family
- `docs/06_decisions/ADR_SAVE_LOAD_AND_PERSISTENCE.md` - SQLite persistence, event append log, snapshot strategy

### Inbox and Candidates

- `docs/00_inbox/VISIONARY_IDEAS.md` - non-canon ideas, do not implement directly
- `docs/01_candidates/CANON_CANDIDATES.md` - review queue for possible canon

### Reference

- `docs/07_reference/MASTER_SYSTEM_LIST_REFERENCE.md` - orientation reference only

---

## Legacy Reference

The `legacy_reference/` folder contains imported material from a prior project.
This material is reference-only. It informs candidate analysis but does not
become canon automatically. Do not copy legacy code or architecture directly.

Valuable legacy concepts already absorbed into current canon:

- Core resolution formula and attribute list
- Luck mechanics
- NPC importance tier concept
- Knowledge gating principle
- AI boundary and adapter separation
- Voice routing per actor tier
- Vox Factory offline pipeline concept

---

## Hard Stops

Stop and escalate if any of the following occur:

- A change would give AI authority over deterministic outcomes
- A change would let frontend or tooling own canonical state
- Canon and code conflict in a way that affects behavior
- A prompt asks for implementation that depends on undefined schema or ownership
- A prompt asks you to implement from `docs/00_inbox/` directly
- A proposal would leak hidden canonical information to the wrong viewpoint

---

## Fresh Session Handoff Prompt

Use this in a new session to orient an agent quickly:

```text
Read docs/05_build/SESSION_MANIFEST.md first.
The project has implemented and tested the minimal canonical core (including SQLite persistence MVP for events and snapshots), the basic world/actor state slice, spatial publication v0, and the first Phase 3 rules-boundary MVP slice.
Default to analysis-first mode unless a canon-backed implementation task is explicit.
Cite canon files before proposing any change.
Mark unresolved areas as TODO rather than guessing.
```
