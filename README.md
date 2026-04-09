# RPG_AI

RPG_AI is an offline AI-driven RPG simulation engine scaffolded around a documentation-first architecture. The repository is intentionally organized so that simulation truth remains backend-owned, AI stays advisory and interpretive, and any future frontend or dashboard remains replaceable.

This phase establishes repository structure, architectural rules, and canonical documentation only. It does not implement gameplay systems or simulation behavior.

## Core Principles

- Documentation drives implementation.
- Canonical simulation truth lives in the backend simulation core.
- AI may interpret, classify, summarize, narrate, and propose changes, but may not authoritatively decide deterministic outcomes.
- Frontend and campaign tooling are separate layers and do not own simulation truth.
- Unclear areas stay marked as `TODO` or `NEEDS CLARIFICATION` until resolved.

## Repository Structure

- `docs/00_inbox`: Freeform ideas and non-canon concepts.
- `docs/01_candidates`: Review queue for possible canon material.
- `docs/02_canon`: Current canonical architecture and operating rules.
- `docs/03_systems`: System-by-system responsibility boundaries.
- `docs/04_contracts`: State and event contracts.
- `docs/05_build`: Workflow rules for implementation agents and contributors.
- `docs/06_decisions`: Architecture decision records.
- `docs/07_reference`: Supporting reference material that is not implementation authority.
- `src/`: Future code organized by ownership boundary, currently placeholders only.
- `tests/`: Future verification and contract tests.
- `tools/`: Future repository tooling and automation.
- `legacy_reference/`: Imported historical material that should not automatically become canon.

## Where To Start Reading

Read the following in order before making any architectural or code change:

1. [PROJECT_BRAIN](./docs/02_canon/PROJECT_BRAIN.md)
2. [SYSTEM_MAP](./docs/02_canon/SYSTEM_MAP.md)
3. [DATA_OWNERSHIP](./docs/02_canon/DATA_OWNERSHIP.md)
4. [AI_BOUNDARY_RULES](./docs/02_canon/AI_BOUNDARY_RULES.md)
5. Relevant files in `docs/03_systems` and `docs/04_contracts`
6. [CODEX_WORKFLOW](./docs/05_build/CODEX_WORKFLOW.md)

## Working Model

No implementation should begin from ideas in `docs/00_inbox` alone. Visionary material must first move through `docs/01_candidates` and then into `docs/02_canon` before feature work is considered.

When documentation and code diverge, treat the divergence as a governance issue to be surfaced explicitly rather than resolved silently in implementation.
