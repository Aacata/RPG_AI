# Data Ownership

## Purpose

This file defines which layer owns which kind of data and which layers may only derive, interpret, or present that data. Ownership here is authoritative unless superseded by a later accepted ADR.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/EVENT_MODEL.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/04_contracts/RELATIONSHIP_MODEL.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`

## Backend-Owned

Backend-owned data is canonical and authoritative.

Includes:

- World state
- Player state
- NPC state
- Combat outcomes
- Quest progression state
- Inventory possession and transfer state
- Faction membership links
- Relationship state
- Travel state, route logic inputs, and interruption state
- Actor memory records used by simulation truth
- Actor knowledge and belief state
- Faction or institution knowledge state
- Rumor propagation state
- Time progression
- Immutable event history

Examples:

- World state: canonical locations, weather state, active factions, economy indicators.
- Player state: canonical actor state owned by the backend even though the human player supplies input.
- NPC state: identity, stats, traits, current activity, goals, relationships, status flags.
- Combat outcomes: validated hit results, damage, defeat, escape, or other deterministic resolution results.
- Inventory: item possession, equipped state, transfers, consumptions.
- Travel: canonical route selection results, travel time, risk application, interruption triggers, and resource impact once validated by backend rules.
- Relationship state: canonical baseline ties and dynamic relational metrics tracked for simulation use.
- Knowledge and rumor: backend-owned records of what actors know or believe, even when those beliefs are incomplete, delayed, hidden, or false.
- Collective knowledge: backend-owned faction or institution belief-state where group awareness matters.

## Truth, Memory, Knowledge, And Rumor Distinction

These concepts must remain separate:

- Event truth: immutable authoritative history of what happened.
- Memory: backend-tracked remembered records or recollection references grounded in canonical history or approved observation. Backend memory used for simulation truth is not false.
- Knowledge: what an actor knows or believes they know. Knowledge may be incomplete, delayed, hidden, perspective-limited, distorted, or false.
- Rumor: socially propagated knowledge-like information that may distort truth while retaining some underlying signal.
- Rumor should persist as a first-class rumor object or equivalent first-class persisted information type.

False knowledge and distorted rumor may be backend-owned as actor or social belief-state, but they do not replace authoritative event truth.

## AI-Interpreted But Backend-Approved

This category covers artifacts generated or influenced by AI that may affect workflows but are not authoritative until backend validation or approval.

Some of these artifacts may be retained in a backend-managed advisory log for auditability while remaining non-canonical.

Includes:

- Dialogue interpretation
- Player intent classification
- Narrative summaries
- Proposed state changes
- Difficulty framing
- Pacing suggestions
- Candidate memory extraction
- Suggested quest framing
- Campaign-authoring suggestions

Examples:

- Dialogue: AI may generate or reframe dialogue text, but resulting state changes must be validated by backend rules.
- Summaries: AI may summarize recent events, but summaries are not canonical history.
- Proposed actions: AI may suggest likely intents or consequences, but backend systems decide authoritative outcomes.
- Difficulty framing: AI may warn that an action appears implausible or extremely difficult, but backend systems decide whether it is impossible, hard, or allowed.
- Advisory logs: backend-managed records of AI proposals may persist for audit or review, but they remain distinct from event truth.

## Frontend-Owned

Frontend-owned data exists only to support presentation or local interaction flow.

Includes:

- UI component state
- Layout preferences
- Client-side interaction affordances
- Cached view models derived from backend truth
- Accessibility and display settings
- Unsubmitted travel waypoint edits or local interaction drafts

Examples:

- UI: selected panels, camera state, modal visibility, list sorting, presentation-only formatting.
- Client text layout: narrative pane formatting, tooltip composition, local navigation state.

## Tool-Owned

Tool-owned data exists for authoring, debugging, inspection, or operational workflow and must not silently become runtime canon.

Includes:

- Dashboard filters
- Scenario authoring drafts
- Validation reports
- Balancing worksheets
- Debug annotations
- Legacy analysis notes and imported reference digests

Examples:

- Dashboards: editor tabs, draft encounter setup, candidate campaign metadata before publication.
- Inspection artifacts: event diffs, schema validation results, replay bookmarks.
- Legacy notes: migration observations, concept extraction, and redesign inspiration recorded from older systems without becoming canon automatically.

## Undecided

The following ownership areas are not fully locked and require clarification before code depends on them:

- Whether authored narrative assets live under tool-owned configuration, adapter-owned presentation assets, or a dedicated content layer
- How much campaign configuration becomes canonical input versus tool-managed draft material
- Whether rumor propagation is primarily owned by the knowledge contract, a future society subsystem, or a dedicated propagation subsystem

## Ownership Rules By Example

- World state: backend-owned.
- Player state: backend-owned.
- NPC state: backend-owned.
- Combat outcomes: backend-owned.
- Travel routes and interruption logic: backend-owned.
- Event truth: backend-owned.
- Memory records used by simulation truth: backend-owned.
- Actor knowledge and rumor state: backend-owned belief-state, not backend-owned truth.
- Advisory AI log: backend-managed non-canonical operational record, not authoritative event truth.
- Dialogue text: AI-interpreted and frontend-presented, with any state impact backend-approved.
- Summaries: AI-interpreted artifacts only, never canonical truth.
- UI state: frontend-owned.
- Dashboard state: tool-owned.
- Legacy reference material: reference-owned until formally analyzed and written into canon.

## Hard Constraints

- No frontend layer may override backend-owned world or actor truth.
- No AI artifact may be treated as historical truth without contract-backed persistence rules.
- No summary may replace immutable events.
- False beliefs may exist in backend-owned knowledge state, but they may not be promoted into event truth.
- Legacy material may inform candidate analysis, but may not be copied or treated as canon by default.

## TODO

- Define publication rules for campaign drafts becoming canonical runtime inputs.
- Clarify storage boundary for authored lore text versus generated narrative text.
- Clarify whether some knowledge or rumor propagation data should be snapshot-only versus fully replayable.
