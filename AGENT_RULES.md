# Agent Rules

All future agent sessions must operate from canon documentation before making changes.

## Required Reading Order

1. `docs/05_build/SESSION_MANIFEST.md`
2. `docs/05_build/BUILD_DIRECTIVE.md` — **obligatorisk** för batched implementation: implementera batch, review, drift/buggpass, commit + push, sedan nästa batch tills mänsklig input krävs (se stoppvillkor i direktivet).
3. `docs/05_build/IMPLEMENTATION_STATUS.md`
4. `docs/02_canon/PROJECT_BRAIN.md`
5. `docs/02_canon/SYSTEM_MAP.md`
6. `docs/02_canon/DATA_OWNERSHIP.md`
7. `docs/02_canon/AI_BOUNDARY_RULES.md`
8. `docs/02_canon/BUILD_ORDER.md`
9. Relevant system files in `docs/03_systems`
10. Relevant contract files in `docs/04_contracts`
11. `docs/05_build/CODEX_WORKFLOW.md`
12. `docs/05_build/REVIEWER_GATEKEEPER.md` for review and gatekeeping sessions

If the task touches deterministic resolution, read `docs/03_systems/RULES_SYSTEM.md`.
If the task touches AI or voice, also read `docs/03_systems/AI_STACK.md` and `docs/03_systems/VOICE_SYSTEM.md`.

## Non-Negotiable Rules

- Never implement directly from `docs/00_inbox/VISIONARY_IDEAS.md`.
- Never invent missing architecture because a prompt sounds plausible.
- Never let AI logic decide deterministic authoritative outcomes.
- Never let frontend concerns redefine backend truth ownership.
- Report uncertainty explicitly instead of guessing.
- Escalate doc/code conflicts instead of silently reconciling them.

## Expected Behavior

- When doing multi-step or release-oriented implementation, follow `docs/05_build/BUILD_DIRECTIVE.md` (batch → review → drift/bugs → commit → push → next batch until human-input stop).
- Work analysis-first unless a canon-backed implementation task is explicit.
- Cite the canon and contract files that justify any proposed code change.
- Preserve unresolved areas as `TODO` or `NEEDS CLARIFICATION` when canon is not yet locked.
