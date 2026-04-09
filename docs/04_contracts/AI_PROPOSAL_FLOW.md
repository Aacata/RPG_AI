# AI Proposal Flow

## Purpose

Define how advisory AI outputs move through validation without becoming authoritative state by default.

Cross-reference:

- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/EVENT_MODEL.md`
- `docs/03_systems/AI_INTERPRETATION_SYSTEM.md`

## Proposal Categories

AI may propose:

- Narration
- Interpretation
- Likely intent
- Difficulty framing
- Candidate state shifts
- Pacing suggestions
- Campaign-authoring suggestions

A future director-AI layer may receive its own proposal types later, but that remains partially unresolved and is not yet locked into canon beyond this note.

These categories are advisory, not authoritative.

## Approval Principles

- Backend validates all deterministic outcomes.
- Backend validates all canonical state changes.
- AI warnings about plausibility or difficulty are advisory only.
- Backend decides whether an action is impossible, difficult, allowed, blocked, or conditionally allowed.
- Proposal exchange may involve narrator AI, local specialist AI, and backend code, but backend validation remains the authoritative gate.

## Conceptual Flow

1. AI produces an advisory proposal.
2. Proposal is tagged by type, origin role, and associated context.
3. Proposal may be enriched, challenged, or reframed by another AI role within the advisory flow if the architecture uses narrator and local specialist stages.
4. Backend validation or approval logic inspects the proposal.
5. Proposal is marked approved, partially approved, rejected, or superseded.
6. Only approved outcomes may result in canonical state change or authoritative event emission.
7. Rejected proposals may remain loggable as advisory records.

## Logging And Audit

- A separate advisory log should exist in addition to the immutable authoritative event archive.
- Advisory AI outputs should remain distinct from authoritative event history until approved.
- Rejected proposals should be loggable.
- Approved authoritative events may optionally reference the proposal that preceded them.
- Logging a rejected proposal does not make the proposal true.

## Minimum Conceptual Metadata

- Proposal identifier
- Proposal type
- Proposal origin role placeholder such as narrator AI, specialist AI, or later director AI
- Source context placeholder
- Target entities or state areas placeholder
- Validation status
- Rejection or approval reason placeholder
- Advisory-log reference placeholder
- Link to resulting authoritative event if one exists

## TODO

- Define whether proposal validation is synchronous, asynchronous, or both.
- Define which proposal types are eligible for partial approval.
- Clarify retention policy for rejected proposals.
- Clarify whether director-AI proposals will share the same advisory-log contract or require a dedicated extension later.
