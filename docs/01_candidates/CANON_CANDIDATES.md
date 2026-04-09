# Canon Candidates

## Purpose

This file is the staging area between raw ideas and approved canon. A candidate should be specific enough to evaluate, but it is still not authoritative until accepted and moved into the relevant canon documents.

Cross-reference:

- Source ideas often originate in `docs/00_inbox/VISIONARY_IDEAS.md`.
- Accepted material must land in `docs/02_canon/` and, when needed, in `docs/03_systems/` or `docs/04_contracts/`.

## Candidate Status Model

- `DRAFT`: Candidate exists but is not ready for review.
- `UNDER_REVIEW`: Candidate is being evaluated for architecture fit, ownership, and scope.
- `BLOCKED`: Candidate cannot proceed until specified dependencies or clarifications are resolved.
- `APPROVED_FOR_CANON`: Candidate is accepted and must be translated into canon docs before implementation.
- `REJECTED`: Candidate conflicts with architecture, ownership rules, or current scope.
- `DEFERRED`: Candidate may be valuable later but is intentionally not entering canon now.

## Evaluation Checklist

A candidate should be checked against the following:

- Does it preserve backend-owned simulation truth?
- Does it avoid giving AI authority over deterministic outcomes?
- Does it preserve frontend replaceability?
- Does it fit within the existing system map without collapsing boundaries?
- Does it require new ownership definitions?
- Does it need new contract files or schema changes?
- Does it create auditability or replay concerns?
- Is it required for MVP, or is it clearly a later-phase capability?
- Are unresolved assumptions recorded explicitly?

## Candidate Template

```md
## Candidate: <title>

Status:
Origin:
Proposed owner:
Related docs:

Summary:

Problem being solved:

Why this may belong in canon:

Architecture impact:

Ownership impact:

Dependencies:

MVP or Later:

Acceptance criteria for canon:

Open questions:
```

## Ownership Placeholder

Every candidate must identify a proposed owner, even if the owner is only a placeholder such as `core`, `world`, `rules`, `ai`, `adapters`, or `tooling`. If ownership is unclear, record `NEEDS CLARIFICATION` rather than leaving it implicit.

## Dependency Placeholder

Candidates should declare dependencies on:

- Canon documents that must be updated
- Contracts that must be defined first
- Systems that must exist before the candidate can be implemented
- Decisions that may require an ADR

## MVP Vs Later Placeholder

Every candidate should state one of the following:

- `MVP`: Required for the smallest coherent canonical engine.
- `LATER`: Important, but intentionally delayed.
- `UNKNOWN`: Cannot yet be placed without further architecture clarification.

## TODO

- Define whether candidates should become individual files once volume increases.
- Decide whether candidate review requires ADR linkage for all accepted architectural changes.
