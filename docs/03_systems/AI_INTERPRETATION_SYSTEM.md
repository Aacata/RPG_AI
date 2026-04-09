# AI Interpretation System

## Purpose

Provide AI-assisted interpretation, summarization, classification, and narrative generation grounded in canonical state while preserving backend authority.

Cross-reference:

- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/04_contracts/EVENT_MODEL.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`

## Responsibilities

- Transform canonical state and events into narrative or analytical outputs
- Classify ambiguous text into backend-consumable proposals
- Produce advisory state-change suggestions for backend validation
- Support proposal exchange patterns between narrator AI, local specialist AI, and backend validation flow
- Support tool-facing summaries and client-facing narration
- Respect viewpoint and reveal boundaries so hidden canonical information is not exposed improperly
- Distinguish between event truth, memory, knowledge, rumor, and player-visible information when generating outputs

## Non-Responsibilities

- Final deterministic resolution
- Direct canonical mutation
- Canon replacement through summaries
- Architecture decision-making without candidate and canon review
- Treating omniscient canonical context as automatically revealable to the player viewpoint
- Treating proposal plausibility warnings as authoritative impossibility judgments
- Assuming a future director-AI layer is already canonically defined beyond currently approved advisory-flow placeholders

## Inputs

- Canonical world, NPC, inventory, quest, faction, and event data
- Knowledge, rumor, and relationship boundaries
- Player or operator text input
- Approved rule and schema definitions

## Outputs

- Summaries
- Narrative descriptions
- Candidate structured intents
- Advisory change proposals
- Difficulty and plausibility framing
- Classification labels

## Owned Data

- Prompting and interpretation configuration placeholders
- AI output artifacts that are explicitly marked non-canonical until approved
- Viewpoint-filtering or reveal-policy placeholders
- Advisory-log linkage placeholders for persisted proposal records

## Dependencies

- All relevant canonical contracts as read inputs
- `knowledge` contract for what can be revealed or believed
- `ai proposal flow` contract for advisory-output lifecycle
- `rules` or approval mechanisms for any proposed changes
- `adapters` and `tools` as downstream consumers of non-canonical outputs

## Likely Future Extensions

- Dialogue style layers
- Memory extraction assistance
- Campaign-specific narrative voices
- Tool-assisted balancing or classification workflows
- Travel narration and pacing support

## Open Questions

- Which AI outputs should be persisted, if any
- Whether offline local models impose additional formatting or capability constraints
- How much broader hidden context AI may use internally for framing before reveal-boundary checks become too opaque
- Which proposal types, if any, belong to a future director-AI role rather than narrator or specialist flows
