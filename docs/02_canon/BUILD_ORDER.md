# Build Order

## Purpose

This file defines the phased implementation order so future work proceeds from
canonical foundations outward. Phase boundaries are sequencing guidance, not a
guarantee that every detail inside a phase is fully solved before moving forward.

A phase is complete when its exit criteria are met, not when every open question
inside it is resolved. Unresolved questions that do not block the next phase are
carried forward as explicit TODOs.

Historical note:

- Some phase-gate language below is governance framing from initial planning.
- The current repo may contain implemented and tested slices from a phase that is not fully closed.
- Distinguish carefully between implemented slice, phase fully closed, and broader goals still deferred.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/SESSION_MANIFEST.md`
- `docs/05_build/CODEX_WORKFLOW.md`

---

## Phase 0: Documentation

**Status: Canon baseline established; open canon questions remain**

### Focus
- Establish canon documents
- Lock ownership boundaries
- Define minimum contracts
- Record unresolved questions explicitly

### Canon maturity achieved so far
- Shared actor-family decision for player and NPC specialization
- Travel subsystem definition at canon level
- Explicit separation between event truth, memory, knowledge, and rumor
- Explicit separation between advisory AI flow and authoritative event history
- Core resolution formula, attributes, skill system, and difficulty categories
- AI stack with concrete component assignments
- Voice system with routing logic, factory pipeline, and curation workflow
- AI boundary rules and proposal flow lifecycle

### Exit Criteria
All of the following must be true before Phase 1 begins:

- [ ] `PROJECT_BRAIN.md` — present and internally consistent
- [ ] `SYSTEM_MAP.md` — layer boundaries defined
- [ ] `DATA_OWNERSHIP.md` — ownership rules locked
- [ ] `AI_BOUNDARY_RULES.md` — AI constraints locked
- [ ] `BUILD_ORDER.md` — this file, with exit criteria per phase
- [ ] `RULES_SYSTEM.md` — resolution formula, attributes, and skill system locked
- [ ] `AI_STACK.md` — concrete components assigned
- [ ] `VOICE_SYSTEM.md` — voice pipeline and routing defined
- [ ] `SESSION_MANIFEST.md` — compact session entry point present
- [ ] `EVENT_MODEL.md` — immutable event principles defined
- [ ] `NPC_STATE_SCHEMA.md` — actor family baseline defined
- [ ] `WORLD_STATE_SCHEMA.md` — world state schema defined
- [ ] `KNOWLEDGE_MODEL.md` — knowledge and rumor separation defined
- [ ] `RELATIONSHIP_MODEL.md` — MVP relationship axes locked
- [ ] `AI_PROPOSAL_FLOW.md` — advisory proposal lifecycle defined
- [ ] `ADR_PLAYER_AS_ACTOR.md` — player specialization decision recorded
- [ ] NPC importance tier names locked as canon
- [ ] No unresolved ownership conflicts between existing documents

### Open questions carried forward from Phase 0
- NPC importance tier names still need canon lock before actor-tier semantics expand further
- Save/load persistence strategy still needs directional decision before persistence work begins

---

## Phase 1: Minimal Canonical Core

**Status: Implemented and tested in the current repo; persistence and save/load direction remain open**

### Focus
- Create the minimal backend simulation core in `src/core`
- Define canonical entity identifier scheme
- Implement event emission interface
- Implement basic state transition validation scaffold
- Establish persistence layer foundation (SQLite preferred)
- Define the save/load direction

### What this phase does not include
- World state population
- NPC state population
- Rules resolution logic
- AI integration
- Any frontend or tooling surface

### Dependencies
- Phase 0 exit criteria met
- `EVENT_MODEL.md` contract stable
- `DATA_OWNERSHIP.md` rules locked

### Current repo status
- `src/core` exists with typed canonical IDs, core mutation contracts, validation, and atomic apply support
- `src/events/event_envelope.py` exists and builds `AuthoritativeEvent` records from backend `EventHandoff` data
- `src/core/runtime.py` routes `ProposedChange -> validation -> atomic apply -> authoritative event build`
- `tests/test_phase1_core_slice.py` covers the current core slice
- NOTE: persistence backend and save/load direction are still not implemented

### Exit Criteria
All of the following must be true before Phase 2 begins:

- [x] `src/core` exists with canonical entity ID generation
- [x] Event emission interface implemented and tested
- [ ] At least one event type can be created, stored, and retrieved
- [x] Basic state transition validation scaffold in place
- [ ] Persistence layer (SQLite) initialized with schema versioning
- [ ] Save/load direction decided and recorded (snapshot, delta, or hybrid)
- [x] All core modules have corresponding contract tests for the currently implemented slice
- [x] No AI, frontend, or tooling code exists in `src/core`

### Key decisions to make during this phase
- Whether `events` is a standalone module or lives under `core` while remaining
  conceptually separate
- Exact save/load strategy (recommend recording as an ADR)
- Whether canonical entity IDs are UUIDs, sequential integers, or typed composites

---

## Phase 2: Basic World and NPC State

**Status: Implemented slice in the current repo and tested; some broader phase goals remain open**

### Focus
- Introduce canonical world state container
- Introduce canonical NPC and player actor state using shared actor-family baseline
- Add location, time, region, and faction link placeholders
- Add actor status, tier, and importance tier fields
- Establish snapshot strategy for world and actor state
- Link world and actor state to event history

### What this phase does not include
- Deterministic rules resolution
- Memory and knowledge representation
- AI integration
- Companion behavior depth beyond tier designation
- Any frontend or tooling surface

### Dependencies
- Phase 1 core slice available
- `NPC_STATE_SCHEMA.md` contract stable
- `WORLD_STATE_SCHEMA.md` contract stable
- Player-as-specialized-actor ADR accepted
- NOTE: NPC importance tier names are still not locked in canon; broader tier semantics remain deferred

### Current repo status
- `src/npc` and `src/world` exist with `ActorRecord`, `WorldRootRecord`, `RegionRecord`, and `LocationRecord`
- `StateRoot` stores `world_spaces`, `actors`, `locations`, `regions`, `save_slots`, and `player_map_discovery`
- Map MVP records now include `WorldSpaceRecord` plus `LocationRecord.x/y/z/biome/is_hidden_by_default`
- Actor spatial linkage remains `location_ref` only
- Narrow mutation and validation support exists for `RegionRecord.world_space_ref`
- Player-viewpoint map discovery storage, read-model helper, and backend update helpers exist and are tested
- `tools/test_env_map_discovery_v0.py` demonstrates the current discovery MVP
- NOTE: full mutation-surface support for `LocationRecord.x/y/z/biome/is_hidden_by_default` is not implemented

### Exit Criteria
All of the following must be true before Phase 3 begins:

- [x] `src/world` exists with canonical location and region records
- [x] `src/npc` exists with canonical actor records using shared family baseline
- [x] Player specialization implemented within shared actor family
- [ ] NPC importance tiers implemented and stored
- [x] World time and calendar state implemented
- [ ] Faction link placeholders in place for actors and locations
- [ ] World and actor state can be snapshotted and restored
- [ ] All state changes emit events via the Phase 1 event interface
- [x] Contract tests cover world and actor state mutations for the currently implemented slice
- [x] No rules resolution logic lives in world or NPC modules
- [x] No AI code lives in world or NPC modules

### Key decisions to make during this phase
- Exact snapshot granularity relative to event replay
- Whether faction entities require their own module in this phase or remain
  as link placeholders only

---

## Phase 3: Deterministic Rules Boundary MVP

**Status: First MVP slice implemented and tested**

### Focus

- Define the smallest useful rules-layer contract above the current canonical core
- Accept a minimal backend action request shape
- Inspect canonical state without mutating it directly
- Produce backend-owned approved mutations through existing mutation contracts
- Produce rejection diagnostics for invalid or blocked actions
- Produce authoritative event handoff payloads for downstream event creation
- Prove the call sequence from action request -> rules inspection -> core validation -> atomic apply -> event handoff

### What this phase does not include

- Full implementation of the complete resolution formula across the whole game
- Full attribute rollout on all actors
- Universal base skill list implementation
- Skill progression system
- Luck system implementation beyond explicit future TODO references
- Travel subsystem implementation
- Combat subsystem implementation
- AI runtime integration
- Memory, knowledge, rumor, relationship, faction, inventory, or quest semantics
- Persistence backend
- Any frontend or tooling surface

### Dependencies

- Phase 2 actor/world state slice complete
- `RULES_SYSTEM.md` available as canon reference, but not treated as full implementation scope for this slice
- `AI_BOUNDARY_RULES.md` and `AI_PROPOSAL_FLOW.md` stable enough to preserve ownership boundaries
- Existing `StateRoot`, `ProposedChange`, validation, runtime, and authoritative event handoff path intact

### Current repo status

- `src/rules/contracts.py` defines `RulesActionRequest` and `RulesInspectionResult`
- `src/rules/boundary.py` implements the first supported action kind: `set_actor_current_activity`
- Rules inspect canonical actor state without mutating it directly and emit `ProposedChange` plus `EventHandoff`
- `process_rules_action(...)` routes through existing core validation and atomic apply before building the authoritative event
- `tests/test_rules_boundary_mvp.py` covers accepted and rejected MVP action flows
- `tools/test_env_v0.py` demonstrates the current rules-boundary MVP
- NOTE: the broader rules engine, additional action kinds, and full formula rollout remain deferred
- NOTE: the current repo proves one event-integrated rules path, not a gameplay-wide rules engine

### Exit Criteria

All of the following must be true before Phase 4 begins:

- [x] A minimal rules entrypoint contract is defined
- [x] A minimal action request shape is defined in code and tested
- [x] Rules read canonical state without mutating it directly
- [x] Rules produce `ProposedChange` outputs instead of direct state writes
- [x] Rules rejection diagnostics are returned for disallowed or incomplete actions
- [x] Rules produce authoritative event handoff payload data
- [x] Existing core validation remains the final mutation legality gate
- [x] Existing runtime apply path remains atomic and all-or-nothing
- [x] At least one narrow end-to-end test passes from action request to approved mutation set and event handoff
- [x] No subsystem semantics are silently introduced into the rules boundary for the current MVP slice
- [ ] No AI or frontend layer can bypass backend rule authority across the broader engine

### Key decisions for later Phase 3 expansion

- The first supported MVP action kind is now `set_actor_current_activity`
- Whether rules result and event handoff types should remain in `src/rules` or move to a narrower shared contract location
- How much action-specific payload structure is required before a request is considered valid
- Which details remain explicit TODOs for the later full rules-system phase

## Phase 4: Memory and Knowledge

**Status: Not started**

### Focus
- Implement actor memory records linked to canonical event history
- Implement actor knowledge state separate from memory and event truth
- Implement rumor as a first-class persisted information type
- Implement knowledge gating so actors only react to what they know
- Implement faction-level collective knowledge placeholders
- Implement witness and observation linkage feeding knowledge and rumor

### What this phase does not include
- AI-assisted memory extraction (advisory only, Phase 5)
- Full rumor propagation simulation (may be phased)
- Any frontend or tooling surface

### Dependencies
- Phase 3 exit criteria met
- `KNOWLEDGE_MODEL.md` contract stable
- `RELATIONSHIP_MODEL.md` contract stable
- `MEMORY_SYSTEM.md` responsibilities locked

### Exit Criteria
All of the following must be true before Phase 5 begins:

- [ ] Actor memory records implemented and linked to event IDs
- [ ] Actor knowledge state implemented separately from memory and event truth
- [ ] Rumor records implemented as first-class persisted type
- [ ] Knowledge gating implemented — actors react only to known events
- [ ] Faction-level knowledge placeholders in place
- [ ] Witness observation produces memory and knowledge records
- [ ] False belief stored as knowledge state, never promoted to event truth
- [ ] All memory and knowledge mutations emit events
- [ ] Contract tests cover the memory-knowledge-rumor separation
- [ ] No AI code owns memory or knowledge records directly

### Key decisions to make during this phase
- Whether rumor propagation simulation is implemented now or deferred to a later pass
- Whether collective faction knowledge shares the actor knowledge schema or uses
  a dedicated model

---

## Phase 5: AI Interpretation

**Status: Not started**

### Focus
- Integrate Gemini as the strategic and narrative layer
- Integrate FLOW as the compact runtime modulation layer
- Integrate local text generation via Ollama
- Implement advisory proposal intake and validation workflow
- Implement separate advisory log distinct from authoritative event history
- Implement difficulty category proposal flow from AI to rules engine
- Implement viewpoint filtering so AI does not leak hidden canonical information
- Implement Gemini prompt logging and cost tracking

### What this phase does not include
- Voice and audio rendering (Phase 6)
- Campaign authoring tools (Phase 6)
- Any frontend or tooling surface beyond debug inspection

### Dependencies
- Phase 4 exit criteria met
- `AI_BOUNDARY_RULES.md` locked
- `AI_PROPOSAL_FLOW.md` contract stable
- `AI_STACK.md` components confirmed
- FLOW Ollama model selected and registered in canon

### Exit Criteria
All of the following must be true before Phase 6 begins:

- [ ] Gemini adapter implemented in `adapters/ai/gemini_adapter.py`
- [ ] FLOW adapter implemented in `adapters/ai/flow_adapter.py`
- [ ] Local text adapter implemented in `adapters/ai/local_text_adapter.py`
- [ ] Advisory proposal intake and validation workflow implemented
- [ ] Advisory log implemented and kept separate from event history
- [ ] Difficulty category proposals flow from AI through rules engine correctly
- [ ] Viewpoint filtering implemented — hidden canonical state does not leak
- [ ] Gemini prompts logged to `exports/current/gemini_calls/`
- [ ] Gemini token and cost history persisted in backend storage
- [ ] FLOW mode switching works across deterministic, local_ai, hybrid, disabled
- [ ] All AI outputs are advisory until backend-approved
- [ ] Contract tests verify that AI proposals cannot directly mutate canonical state
- [ ] At least one end-to-end test covers: player input → AI proposal → backend
      validation → event emission

### Key decisions to make during this phase
- FLOW Ollama model selection (must be locked before this phase begins)
- Whether narrator AI and specialist AI roles are separated in this phase or later

---

## Phase 6: Voice, Campaign Tools, and Presentation Foundation

**Status: Not started**

### Focus
- Implement voice routing and audio ledger
- Implement GPT-SoVITS and Kokoro TTS adapters for runtime speech
- Implement Fish Speech, Tortoise, and Stable Audio adapters for factory pipeline
- Implement seed curation workflow and sound registry
- Build campaign authoring tool foundation
- Build debug and inspection tool foundation
- Implement minimal presentation adapter layer

### What this phase does not include
- Full gameplay client
- Speech-to-text
- Combat system
- Economy or politics subsystems

### Dependencies
- Phase 5 exit criteria met
- `VOICE_SYSTEM.md` routing and factory rules locked
- Campaign tooling ownership rules defined

### Exit Criteria
All of the following must be true before Phase 7 begins:

- [ ] Voice routing engine implemented and backend-owned
- [ ] Backend audio ledger implemented
- [ ] NPC voice profiles implemented in backend storage
- [ ] GPT-SoVITS adapter implemented and tested
- [ ] Kokoro TTS adapter implemented and tested
- [ ] Fish Speech adapter implemented and tested
- [ ] Tortoise adapter implemented and tested
- [ ] Stable Audio adapter implemented and tested
- [ ] Seed curation workflow implemented with pending/approved/rejected states
- [ ] Sound registry implemented in backend storage
- [ ] End-to-end voice conversation flow works: approved text → routing →
      audio render → audio ledger → clip reference returned
- [ ] Campaign authoring tool can create and inspect world state without
      owning canonical simulation truth
- [ ] Debug inspection tool can view event history and actor state
- [ ] Minimal presentation adapter layer exists for future client connection

### Key decisions to make during this phase
- Whether emote bank ingestion workflow is implemented now or deferred
- Whether the campaign tool is NiceGUI-based from the start or CLI-first

---

## Phase 7: Client and Presentation

**Status: Not started**

### Focus
- Build player-facing presentation layer
- Keep all client logic replaceable and state-derived
- Connect client to backend through stable adapter contracts
- Support initial end-to-end playable session

### Dependencies
- Phase 6 exit criteria met
- Stable adapter contracts
- Stable canonical read models

### Exit Criteria
All of the following must be true to consider Phase 7 complete:

- [ ] At least one client surface renders canonical world and actor state correctly
- [ ] Player input flows through backend contracts without frontend owning state
- [ ] Client can be replaced without changing backend or adapter contracts
- [ ] End-to-end playable session possible: input → rules → state change →
      AI narration → voice render → presentation
- [ ] No canonical simulation logic lives in the client layer

---

## Deferred — Not In Current Phase Scope

The following capabilities are intentionally deferred. They should not influence
current phase work unless promoted through the candidate pipeline.

- Full combat system with action economy
- Speech-to-text pipeline
- C++ core migration for compute-heavy systems
- Godot gameplay client
- Economy and logistics subsystem
- Politics and diplomacy subsystem
- Unreal thin client experiment
- Multiplayer or networked session support

---

## Open Questions Carried Forward

- NPC importance tier names are still not locked in canon and should be resolved before actor-tier semantics expand further
- HP formula multipliers remain open before later full rules-system expansion
- FLOW Ollama model selection must be locked before Phase 5 (blocking)
- Save/load strategy direction remains undecided before persistence and snapshot work expands
- Whether `events` is a standalone module or lives under `core` (Phase 1 decision)
- Whether campaign rule variation hooks are added in a later Phase 3 expansion or deferred further
- Whether rumor propagation simulation is implemented in Phase 4 or deferred
- Whether narrator AI and specialist AI roles are separated in Phase 5 or later
- Whether emote bank ingestion workflow is implemented in Phase 6 or deferred
- Whether the campaign tool is NiceGUI-based from the start or CLI-first
