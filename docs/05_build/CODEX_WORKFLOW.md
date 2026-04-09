# Codex Workflow

## Purpose

This file tells future Codex sessions how to operate in this repository. It is intentionally strict to prevent architecture drift and premature implementation.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/SYSTEM_MAP.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`

## Default Analysis-Only Mode

Unless a prompt explicitly requests implementation that is supported by canon, default to analysis-first and documentation-first behavior.

That means:

- Read canon before proposing changes.
- Do not invent unresolved system behavior.
- Prefer documenting gaps over filling them with assumptions.
- Avoid implementing gameplay features from visionary material.

## Required Reading Order Before Making Changes

1. `docs/02_canon/PROJECT_BRAIN.md`
2. `docs/02_canon/SYSTEM_MAP.md`
3. `docs/02_canon/DATA_OWNERSHIP.md`
4. `docs/02_canon/AI_BOUNDARY_RULES.md`
5. Relevant files in `docs/03_systems/`
6. Relevant files in `docs/04_contracts/`
7. `docs/02_canon/BUILD_ORDER.md`

## How Visionary Ideas Move To Canon

1. Raw idea enters `docs/00_inbox/VISIONARY_IDEAS.md`.
2. If it appears structurally relevant, it is rewritten as a candidate in `docs/01_candidates/CANON_CANDIDATES.md`.
3. Candidate is evaluated against ownership, deterministic authority, auditability, and architecture fit.
4. If accepted, canon documents are updated first.
5. Only after canon is updated should implementation planning or coding begin.

## How Code Changes Must Be Proposed

Before coding:

- Cite the canon and contract documents that justify the change.
- State which ownership boundary the change belongs to.
- State any assumptions explicitly.
- Stop if required canon or contract support is missing.

## When To Stop And Ask

Stop and escalate when:

- A change would assign deterministic authority to AI.
- A change would let frontend or tooling own canonical state.
- Canon and code conflict in a way that affects behavior.
- A requested implementation depends on undefined schema or ownership rules.
- The prompt asks for behavior that only exists in `docs/00_inbox`.

## How To Avoid Architecture Drift

- Do not merge layers for convenience.
- Do not treat summaries, dashboards, or view models as truth.
- Do not smuggle architecture changes into refactors.
- Prefer TODO notes over unsupported certainty.

## How To Handle Uncertainty

- Use `TODO`, `UNKNOWN`, or `NEEDS CLARIFICATION`.
- Keep unresolved questions near the affected document or contract.
- If assumptions are unavoidable, label them clearly in the change summary.

## How To Report Assumptions

Every substantial change should record:

- Which canon file it follows
- Which area remains unresolved
- Which assumption was made temporarily, if any
- What would invalidate that assumption

## How To Validate Changes Against Docs

- Check the relevant system document for responsibility overlap.
- Check the relevant contract document for schema fit.
- Check `DATA_OWNERSHIP.md` for ownership violations.
- Check `AI_BOUNDARY_RULES.md` for AI overreach.
- If architecture changed, add or update a decision record.

## TODO

- Define a standard implementation proposal template once the project begins coding.
- Decide whether every architecture-affecting code change must include an ADR reference.
