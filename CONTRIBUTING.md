# Contributing

Contributions to this repository must follow the documentation-first operating model.

## Required Rules

- Do not implement features without checking the relevant canon documents first.
- Do not introduce silent architecture changes in code, documentation, or folder layout.
- Do not allow frontend code or UI assumptions to become owners of canonical simulation truth.
- Do not promote material from `docs/00_inbox` directly into implementation.
- Do not guess through unresolved architectural areas; record `TODO` or `NEEDS CLARIFICATION` instead.

## Before Changing Anything

Read, at minimum:

1. `docs/02_canon/PROJECT_BRAIN.md`
2. `docs/02_canon/SYSTEM_MAP.md`
3. `docs/02_canon/DATA_OWNERSHIP.md`
4. `docs/02_canon/AI_BOUNDARY_RULES.md`
5. Relevant files in `docs/03_systems` and `docs/04_contracts`

## Change Expectations

- Proposed code changes should cite the canon documents they implement.
- Proposed architecture changes should be reviewed through candidate and decision records rather than hidden inside code patches.
- When code and canon disagree, stop and document the conflict before proceeding.
