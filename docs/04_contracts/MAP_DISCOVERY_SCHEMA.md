# Map Discovery Schema

## 1. Purpose

This document defines the minimum contract for viewpoint-specific map reveal state.

It exists to keep canonical map truth separate from what a player-facing viewpoint is currently allowed to know. It is not the full knowledge system, not the full rumor system, and not a map UI specification.

This contract sits between:
- canonical spatial state in `MAP_STATE_SCHEMA.md`
- broader knowledge boundaries in `KNOWLEDGE_MODEL.md`
- future derived 2D map presentation described by `MAP_SYSTEM.md`

## 2. Scope of this contract

This contract covers only the minimum needed for:
- separation between canonical place existence and discovery state
- viewpoint-specific reveal state for locations
- viewpoint-specific reveal state for location names
- a very small marker/POI reveal boundary at MVP level
- backend-owned discovery truth

This contract does not cover:
- full rumor propagation
- full NPC knowledge state
- full faction or institutional knowledge
- travel runtime mechanics
- map rendering or UI behavior
- quest-intel mechanics beyond naming them as possible reveal sources
- per-viewer style, icon, or presentation preferences

## 3. Core separation rule

- Canonical location existence is not the same as discovery.
- A `LocationRecord` may exist in canonical state before the active viewpoint knows it exists.
- Discovery state is viewpoint-specific.
- Frontend may render discovery state, but frontend does not own discovery truth.
- AI may describe only what the active viewpoint is allowed to know under backend-approved discovery state.

This means undiscovered locations remain in canonical state. They are not created on reveal and they are not removed to simulate ignorance.

## 4. Minimum recommended discovery unit

Discovery should be tracked per `LocationRecord` for MVP.

Rationale:
- `MAP_STATE_SCHEMA.md` already locks POIs as typed locations for MVP.
- Per-location tracking is the smallest practical unit that supports hidden settlements, hidden POIs, and later naming reveal without introducing a second spatial abstraction.
- Starting at a broader region layer would be too coarse for hidden-but-existing places.

This contract therefore assumes a tiny location-scoped discovery record, conceptually named `MapDiscoveryEntry`.

## 5. Minimum reveal fields

The MVP discovery unit should contain only the following conceptual fields:

### `location_ref`
- Purpose: points to the canonical `LocationRecord` this discovery entry refers to.
- Required because discovery must stay anchored to canonical map truth.

### `is_revealed`
- Type: `bool`
- Purpose: indicates whether the active viewpoint knows that the location exists at all.
- This is the minimum existence-reveal flag.

### `is_name_revealed`
- Type: `bool`
- Purpose: indicates whether the active viewpoint may know the location's display name.
- This allows a place to be known before its formal name is known.

### `is_marker_visible`
- Type: `bool`
- Purpose: indicates whether a player-facing map may show a marker or equivalent POI indicator for this location.
- This is intentionally separate from `is_revealed` so a place may be known in some sense without forcing marker visibility.

### `is_visited`
- Type: `bool`
- Purpose: indicates whether the active viewpoint has physically reached or directly entered the location.
- This should remain separate from generic reveal because hearing of a place is not the same as visiting it.

These are the minimum useful fields for MVP.

Do not add in this contract:
- reveal timestamps
- confidence levels
- per-source weighting
- discovery radius data
- per-faction overlays
- free-form notes

TODO:
- The exact persistence container for these entries is not yet locked here. It may live under save/viewpoint state rather than canonical world-map records. This document locks the field contract and separation rules, not the final storage site.

## 6. Reveal sources at contract level

The following reveal-source categories are valid at contract level:
- travel
- direct observation
- rumor or intel
- NPC dialogue
- acquired map or document

These are origin categories only. This contract does not define how they work mechanically, how reliable they are, or how they are prioritized.

## 7. What must remain separate from this schema

This schema does not replace:
- full actor knowledge models in `KNOWLEDGE_MODEL.md`
- rumor truth, distortion, or propagation logic
- canonical map state in `MAP_STATE_SCHEMA.md`
- frontend presentation styling, icons, fog-of-war rendering, or zoom behavior

Map discovery is a viewpoint-level reveal contract layered over canonical place records. It is not the source of map truth and it is not the complete knowledge system.

## 8. Deferred explicitly

The following are intentionally deferred:
- exact storage location for discovery entries
- support for multiple simultaneous viewpoints
- faction-level or institution-level map knowledge
- false map entries or deceptive cartography
- reveal timestamps and reveal history
- partial geometry reveal or route-segment reveal
- discovery mechanics driven by travel, rumor, quests, or tools
- UI rules for icons, labels, and fog presentation

## 9. Minimal recommended next slice

Proceed with a narrow implementation-planning pass for minimal player-viewpoint map discovery state.

That next slice should answer only:
- where the MVP `MapDiscoveryEntry` lives conceptually
- what the single active player-viewpoint boundary is for MVP
- how discovery entries relate to canonical `LocationRecord` ids

It should not broaden into rumor, NPC knowledge, travel, or UI behavior.
