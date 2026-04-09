# Prompt Patterns

## Purpose

Reusable prompt templates for future analysis, canon work, and tightly controlled implementation sessions.

## Analyze-Only

```md
Act in analysis-only mode.
Read the required canon documents before proposing anything.
Do not write code.
Identify:
- relevant canon files
- current ownership boundaries
- unresolved questions
- risks of architecture drift
Return recommendations only.
```

## Candidate Classification

```md
Review the following idea as a canon candidate.
Do not treat it as approved.
Classify it using the candidate status model in docs/01_candidates/CANON_CANDIDATES.md.
Evaluate:
- backend truth ownership
- AI boundary compliance
- frontend boundary compliance
- required contract changes
- MVP vs Later
Record open questions and recommended next document updates.
```

## Canon Drafting

```md
Update canon documentation only.
Do not implement code.
Use precise technical language.
Mark unresolved areas as TODO or NEEDS CLARIFICATION.
Cross-reference relevant system and contract files.
Do not invent architecture beyond the provided source material.
```

## Implementation Planning

```md
Produce an implementation plan only.
Read the relevant canon and contract files first.
List:
- scope
- ownership boundary
- required files
- tests to add
- assumptions
- blockers
Do not write production code.
```

## Implementation With Strict Limits

```md
Implement only the canon-backed change described below.
Before editing, cite the canon and contract files that authorize the work.
Do not expand scope.
Do not invent missing architecture.
If required details are undefined, stop and report the gap instead of guessing.
```

## Refactor Review

```md
Review this refactor for architecture drift.
Focus on:
- ownership boundary violations
- AI authority leakage
- frontend truth leakage
- contract mismatch
- hidden behavior changes
List findings first with file references.
```

## Ownership Review

```md
Analyze the following design or code change for data ownership correctness.
Use docs/02_canon/DATA_OWNERSHIP.md as the source of truth.
Call out:
- backend-owned data handled outside backend boundaries
- frontend-owned data promoted to canon
- tool-owned drafts treated as runtime truth
- AI outputs treated as authoritative
```

## Conflict Detection Between Docs And Code

```md
Compare the current implementation against the referenced canon documents.
Do not silently reconcile differences.
Return:
- explicit conflicts
- likely source of truth
- risk level
- whether implementation should stop
- recommended doc or code follow-up
```

## Advisory Flow Review

```md
Review the proposed AI workflow against docs/02_canon/AI_BOUNDARY_RULES.md and docs/04_contracts/AI_PROPOSAL_FLOW.md.
Check:
- whether outputs stay advisory until backend approval
- whether the advisory log is kept distinct from event history
- whether narrator AI, specialist AI, and backend roles are separated correctly
- whether hidden canonical information could leak during the flow
Return documentation findings only.
```

## Legacy Analysis

```md
Analyze the provided legacy material as reference only.
Do not treat it as canon.
Extract:
- reusable concepts
- migration insights
- risks if copied directly
- canon files that would need explicit updates before any redesign use
Call out any places where the legacy material conflicts with current ownership, AI, or frontend boundaries.
```
