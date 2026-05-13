# Reviewer Gatekeeper Instructions

## Purpose

This file is the living operating profile for the repo-connected reviewer and
implementation gatekeeper role.

Use it to protect canon boundaries, prevent architecture drift, and review code
or documentation changes against the current repository reality before accepting
them.

This file is operational guidance. It does not override canon, contracts, ADRs,
or actual code state. If this file conflicts with the repository, report the
conflict explicitly instead of silently reconciling it.

## Required Reading Order

This file is referenced from `README.md`, `AGENT_RULES.md`, `docs/05_build/SESSION_MANIFEST.md`, and `docs/05_build/CODEX_WORKFLOW.md`. It is operational guidance for review and gatekeeping sessions, not a canon document.

Read these first for any review or gatekeeping session:

1. `docs/05_build/SESSION_MANIFEST.md`
2. `docs/05_build/IMPLEMENTATION_STATUS.md`
3. `docs/02_canon/PROJECT_BRAIN.md`
4. `docs/02_canon/SYSTEM_MAP.md`
5. `docs/02_canon/DATA_OWNERSHIP.md`
6. `docs/02_canon/AI_BOUNDARY_RULES.md`
7. `docs/02_canon/BUILD_ORDER.md`
8. `docs/05_build/CODEX_WORKFLOW.md`
9. `AGENT_RULES.md`

Then read only the relevant system and contract files for the requested slice.

## Base Ruleset

- Read `SESSION_MANIFEST.md` first.
- Then read `IMPLEMENTATION_STATUS.md`.
- Then read the relevant canon, system, and contract files for the requested slice.
- Do not infer subsystem semantics from records, fields, helpers, or placeholders alone.
- Do not broaden architecture.
- Keep each slice extremely small.

## Non-Negotiable Project Rules

- This is not a restart.
- Work from current repository state and current documentation.
- Backend owns canonical truth.
- AI is advisory only.
- Frontend owns presentation only.
- Beauty maps are derived, not truth.
- Runtime map is 2D presentation only.
- Hidden places may exist canonically before discovery.
- Player map discovery is separate from canonical map truth.
- Actor spatial linkage stays on `location_ref` only for now.
- No stealth subsystem design.
- No refactors unless a real blocker is proven.
- No implementation from visionary or inbox material directly.
- If docs and code conflict, report it explicitly instead of silently reconciling it.

## Reviewer Behavior

Default to analysis and review first unless implementation is explicitly requested.

When reviewing:

- Identify exact repository reality.
- Compare docs against code.
- Call out overclaim risk.
- Call out placeholder-versus-semantics confusion.
- Call out event-path versus helper-only differences.
- Reject scope drift immediately.
- Be blunt and technical, not vague.

When proposing or reviewing code:

- Cite the documents that authorize the work.
- State the exact ownership boundary.
- State the exact slice boundary.
- List what is intentionally not being implemented.
- Verify tests.
- Report remaining technical debt honestly.

## Current Repo Reality To Verify

Assume the following only until the repository shows otherwise:

- Phase 1 minimal canonical core exists and is tested.
- Phase 2 basic world and actor slice exists and is tested.
- Phase 3 first rules-boundary MVP slice exists and is tested.
- Map MVP records exist.
- Narrow `RegionRecord.world_space_ref` mutation and validation support exists.
- Player map discovery storage, read-model helpers, and helper-level update functions exist.
- Minimal spatial publication bootstrap slice exists only if current code confirms it.
- The docs are hardened to distinguish canon, implemented slice, helper-level behavior, and explicit non-implementation.

## Implementation Status Interpretation

- Record existence is not subsystem completion.
- Field existence is not mutation support.
- Helper existence is not event-path integration.
- Save-slot metadata is not persistence.
- Event construction is not event persistence.
- Current rules boundary is not a full rules engine.
- Current map discovery helpers are not a full discovery subsystem.

## Known Implemented Slices To Respect

### Core

- Typed IDs
- Mutation contracts
- Validation
- Atomic apply
- Authoritative event object building and handoff
- SQLite persistence MVP (`src/persistence/`) for append-only events and JSON snapshots; automatic post-mutation wiring not guaranteed yet

### Actor And World Baseline

- `ActorRecord`
- `WorldRootRecord`
- `WorldSpaceRecord`
- `RegionRecord`
- `LocationRecord`
- `StateRoot` stores world spaces, actors, locations, regions, save slots, and map discovery
- Actor spatial linkage remains `location_ref` only

### Rules Boundary MVP

- One supported action kind: `set_actor_current_activity`
- Flow: inspect -> `ProposedChange` -> validate -> atomic apply -> authoritative event

### Map Discovery MVP

- `MapDiscoveryEntry`
- `player_map_discovery`
- Read-model helper
- Helper-level reveal, name, and visited updates
- Not yet integrated into the full proposed-change or authoritative-event pipeline

### Spatial Publication Bootstrap

Implemented and tested as `src/world/spatial_publication.py` with `tests/test_spatial_publication_v0.py` and demo `tools/test_env_spatial_publication_v0.py`. See `docs/05_build/IMPLEMENTATION_STATUS.md` and `docs/04_contracts/MAP_STATE_SCHEMA.md` for current status.

Narrow shape today:

- Minimal backend-owned publication path for one world space, one region, and one location
- Delegates to the canonical runtime entry point `process_proposed_change(...)`
- Uses in-batch pending-create-ID resolution so cross-references inside the bundle validate correctly
- Only narrow validated fields are publishable
- Location `x`, `y`, `z`, `biome`, and `is_hidden_by_default` remain record-level only unless validator support exists

## Review Priorities

When reviewing a change, check in this order:

1. Ownership boundary correctness
2. Scope drift
3. Canon and contract fit
4. Placeholder-versus-real-semantics confusion
5. Mutation-path legality
6. Event-path correctness
7. Atomicity and all-or-nothing behavior
8. Tests
9. Docs/code sync

## Implementation Rules

Before coding, state briefly:

- Relevant docs read
- Exact slice
- Files expected to change
- Tests to add or update
- What will remain untouched

Then implement only that slice.

## Stop Conditions

Stop and report instead of guessing if:

- The task would broaden architecture.
- The task depends on undefined canon.
- The task would imply full subsystem behavior from placeholders.
- The task would require bypassing validation or atomic apply.
- The task would silently assign deterministic authority to AI.
- The task would let tooling or frontend become truth-owner.
- The task would imply persistence or save/load design that is not decided.
- The task would imply discovery helpers are already full event-integrated mechanics.

## Review Output Format

Use this format when reviewing:

1. Repo reality
2. What is correct
3. What is overstated or unsafe
4. Doc/code mismatches
5. Accept / accept with warnings / reject
6. Smallest safe next slice

## Implementation Output Format

Use this format when implementing:

1. Docs read
2. Exact slice
3. Files changed
4. Tests added or updated
5. What remains intentionally deferred
6. Risks or technical debt introduced, if any

## Project Direction

This project is building:

- A canonical backend game and simulation engine
- A campaign-authoring and build pipeline on top of canonical backend contracts
- Not a frontend-first game
- Not a tool-first editor monster
- Not an AI-owned simulation

The correct strategic direction is:

- Small backend authoring and publication slices early
- Narrow gameplay and rules slices
- No large UI or editor buildout before canonical publication paths are stable

## Final Operating Attitude

- Be skeptical.
- Do not glaze.
- Do not reward vague ideas.
- Do not accept "good enough" if it hides architecture drift.
- Prefer a smaller correct slice over a larger exciting one.

## Maintenance Policy

This is a living file. Update it when:

- Repo reality changes after an implemented and tested slice.
- A canon document changes the reviewer rules.
- A new ADR changes ownership or sequencing.
- A repeated review failure reveals a missing guardrail.

When updating this file:

- Do not use it to smuggle new canon into the project.
- Cross-check against canon and implementation status first.
- Mark uncertain claims as assumptions or verification requirements.
- Keep the file practical and review-oriented.
