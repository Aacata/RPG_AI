# AI Boundary Rules

## Purpose

This file defines what AI systems may and may not do in this repository and in the future engine runtime. These rules exist to prevent architecture drift, preserve deterministic authority, and keep AI useful without making it canonical truth.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/03_systems/AI_INTERPRETATION_SYSTEM.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`

## Allowed Actions

AI may:

- Interpret player or operator input into structured candidate intents
- Summarize events, state changes, or recent history
- Generate narrative descriptions that are grounded in canonical state
- Classify ambiguous text into predefined backend-consumable categories
- Propose state changes for deterministic validation
- Propose likely difficulty framing, pacing suggestions, or candidate social consequences
- Generate candidate dialogue text or flavor text
- Assist campaign tooling with drafting, labeling, or analysis
- Filter presentation output so it only reveals what the requesting viewpoint can reasonably know
- Use broader canonical context for framing or coherence as long as hidden canonical information is not improperly leaked
- Participate in a staged advisory flow involving narrator AI, local specialist AI, and backend validation

## Disallowed Actions

AI may not:

- Decide authoritative deterministic outcomes
- Mutate canonical state without backend approval
- Replace event history with summaries
- Override explicit rules because a narrative output seems preferable
- Invent missing canon and treat it as approved architecture
- Merge tooling drafts, frontend views, and runtime truth into one data source
- Leak hidden canonical information to the player or another actor viewpoint without an approved reveal basis
- Mark an action as impossible purely from AI judgment when backend rules have not decided that result
- Treat the advisory log as if it were authoritative history

## Escalation Rules When Uncertain

If an AI-facing workflow encounters ambiguity:

- Prefer returning multiple labeled candidates rather than one invented answer.
- Mark unresolved items as `TODO`, `UNKNOWN`, or `NEEDS CLARIFICATION`.
- Escalate when a request would make AI the owner of deterministic resolution.
- Escalate when documentation does not define approval rules for a proposed change.
- Escalate when a prompt conflicts with canon ownership boundaries.
- Escalate when reveal boundaries are unclear between event truth, actor knowledge, and player-facing narration.
- Escalate when a prompt would require AI to expose hidden agenda, rumor state, or private knowledge not available to the current viewpoint.

## Policy For Reporting Conflicts Between Docs And Code

When documentation and code disagree:

- Do not silently update code to match assumption.
- Do not silently update docs to rationalize existing code.
- Record the conflict in the change summary or review notes.
- Identify which canon or contract file appears to be authoritative.
- Stop implementation if proceeding would lock in an architectural assumption.
- If the conflict concerns AI proposal approval, knowledge visibility, or reveal scope, reference the applicable contract file directly.

## Operational Guidance

- AI outputs should be structured so deterministic systems can inspect or reject them.
- AI-facing prompts should cite the current canon instead of embedding fresh architecture.
- Narrative polish is downstream of validated state, not a substitute for it.
- Rejected AI proposals should remain loggable, but they must stay distinct from authoritative event history.
- AI narration should distinguish between canonical truth, actor belief, rumor, and player-visible knowledge whenever that distinction matters to correctness.
- Multi-stage AI collaboration is allowed only within the advisory layer; backend approval remains the sole authority for canonical outcomes.

## TODO

- Define which AI outputs, if any, should be persisted and under what lifecycle rules.
- Define whether any AI-assisted reveal override is ever permitted for debugging or tooling and how it is separated from player-facing flows.
- Clarify whether future director-AI behavior requires separate boundary rules or can extend the existing advisory-flow model.
