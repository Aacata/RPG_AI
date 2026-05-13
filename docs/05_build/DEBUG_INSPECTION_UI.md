# Debug Inspection UI (Phase 6 Scope Note)

## Purpose

Lock where a **simple dashboard-style inspection UI** belongs in the build order and remove ambiguity between Phase 5 (AI) and Phase 6 (tooling and presentation foundation).

Canon reference: [docs/02_canon/BUILD_ORDER.md](../02_canon/BUILD_ORDER.md) Phase 6 exit criteria include **debug and inspection tool foundation** and **minimal presentation adapter layer**.

## Decision

- **Phase 6** is the first phase that officially hosts player-facing or operator-facing **inspection dashboards** that render canonical backend state.
- **Phase 5** remains **AI runtime and advisory flows** only; BUILD_ORDER explicitly excludes general frontend or tooling surfaces beyond debug inspection in Phase 5 — any broad UI still waits for Phase 6 alignment.

## Stack Choice For Inspection v0 (Locked)

- **CLI-first for inspection v0:** textual commands or a minimal local HTTP server that prints JSON are acceptable first surfaces because they minimize ownership risk and ship fastest.
- **NiceGUI (or similar) deferred** until inspection contracts stabilize: richer dashboards belong immediately after the CLI/read-model contract is frozen, still under Phase 6 as **tool-owned inspection**, not simulation truth.

This choice resolves the open Phase 6 question "NiceGUI-based from the start or CLI-first" in favor of **CLI-first now, GUI later**, without forbidding a small NiceGUI slice once read paths are stable.

## Hard Rules

- Inspection UI must **read** canonical state and persisted events through backend or adapter contracts; it must not invent or persist canonical simulation truth.
- Any "write" path from inspection tools must go through existing `ProposedChange` / rules entrypoints, never direct mutation of `StateRoot` for gameplay-relevant fields.

## Related Implementation

- Persistence MVP: `src/persistence/` (SQLite append log + JSON snapshots).
- Future adapter: `src/adapters/` should host HTTP or UI glue when Phase 6 implementation begins.
