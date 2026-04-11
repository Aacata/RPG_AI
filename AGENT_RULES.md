# Agent Rules

All future agent sessions must operate from canon documentation before making changes.

## Required Reading Order

1. `docs/05_build/SESSION_MANIFEST.md`
2. `docs/02_canon/PROJECT_BRAIN.md`
3. `docs/02_canon/SYSTEM_MAP.md`
4. `docs/02_canon/DATA_OWNERSHIP.md`
5. `docs/02_canon/AI_BOUNDARY_RULES.md`
6. `docs/02_canon/BUILD_ORDER.md`
7. Relevant system files in `docs/03_systems`
8. Relevant contract files in `docs/04_contracts`
9. `docs/05_build/CODEX_WORKFLOW.md`

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

- Work analysis-first unless a canon-backed implementation task is explicit.
- Cite the canon and contract files that justify any proposed code change.
- Preserve unresolved areas as `TODO` or `NEEDS CLARIFICATION` when canon is not yet locked.
