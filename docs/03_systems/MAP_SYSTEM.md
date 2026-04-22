# Map System

## 1. Purpose

The map system defines how spatial truth is represented, authored, derived, and revealed in the project.

It exists to prevent four different concerns from collapsing into one:

- backend-owned canonical spatial truth
- campaign-builder authoring surfaces
- derived player-facing 2D map presentation
- viewpoint-specific discovery and knowledge state

The project needs all four, but they do not own the same thing. The map system locks that separation so future implementation does not let a builder view, a beauty render, or an AI narration layer become canonical geography by accident.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/SYSTEM_MAP.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`

Status note:

- Map MVP records exist in code.
- Narrow mutation and validation support exists for `RegionRecord.world_space_ref`.
- Player map discovery storage, a read-model helper, and helper-level update functions exist in code.
- Discovery helpers are not the same thing as full discovery mechanics and are not yet integrated into the full proposed-change or authoritative-event pipeline.
- `LocationRecord` spatial fields exist in records, but full mutation-surface rollout for all of them is not implemented.

## 2. Core architectural separation

### Canonical spatial map

This layer is backend-owned truth.

It owns:

- the existence of regions, locations, and map-relevant places
- canonical spatial relationships
- canonical coordinates and topology inputs
- biome ownership
- canonical routes, water bodies, settlements, and faction influence layers
- hidden-but-existing places whether or not any actor currently knows them

It does not own:

- beauty rendering
- UI zoom widgets
- player-facing reveal decisions by presentation convenience
- builder-only draft controls

### Campaign-builder authoring model

This layer is tooling.

It owns:

- authoring workflows
- terrain sculpting and import operations
- generation controls
- manual editing affordances
- review surfaces for generated spatial content

It does not own:

- runtime truth by itself
- player discovery truth
- frontend presentation truth

Builder tooling edits or publishes backend-owned spatial data. The builder is a powerful editor, not a second source of truth.

### Derived beauty map / 2D presentation

This layer is presentation.

It owns:

- rendered 2D map images or tiles
- overlay styling
- labels, icons, colors, and aesthetic composition
- zoom-level-specific derived views

It does not own:

- whether a place exists
- whether a route exists
- whether a name is known
- whether a POI should be visible to a given viewpoint

Beauty maps are derived assets, not truth.

### Discovery / knowledge overlay

This layer is backend-owned or contract-owned reveal state, not frontend invention.

It owns:

- what a player viewpoint is allowed to know about spatial truth
- whether a place is undiscovered, partially known, named, mapped, rumored, or confirmed
- reveal progression through travel, rumor, dialogue, intel, or acquired map information

It does not own:

- canonical spatial existence
- geometry authoring
- presentation styling

Canonical existence and viewpoint knowledge must remain separate.

## 3. Canonical spatial truth

Backend-owned map truth should include the canonical spatial model of the world, but this document does not lock a final storage schema yet.

Minimum canonical concepts:

- spatial hierarchy such as world -> region -> location -> POI or equivalent place layering
- stable spatial identifiers for canonical places
- `x`, `y`, `z` coordinate capability for canonical placement
- region and location grouping relationships
- biome ownership as canonical world data
- settlements as canonical placed entities or canonical place records
- routes as canonical travel-relevant spatial links
- water bodies as canonical spatial features
- faction influence as canonical world-state input where spatially relevant

Coordinate rule for normal worlds:

- `z = 0` should represent sea level for ordinary ocean-based worlds

This is a convention, not a universal cosmology rule. Non-ocean, subterranean, floating-island, space, or other nonstandard settings may require a different world profile or equivalent spatial baseline.

TODO:

- define where world-profile overrides live for nonstandard settings
- define whether POIs are separate records, typed location variants, or a mixed layered model
- define how much topology is stored explicitly versus derived from coordinates and route data

### Hidden-but-existing places principle

A place may exist canonically before:

- the player knows it exists
- the player knows its name
- the player can see it on a map
- any current actor has reliable knowledge of it

Canonical spatial truth is not gated by discovery.

## 4. Campaign builder authoring model

The campaign builder may use a 3D or 2.5D authoring representation where that is useful for creation and editing.

Allowed builder capabilities include:

- sculpt terrain
- import heightmaps
- define world size or map bounds
- paint biome layers
- place major settlements
- place POIs
- place water sources or water bodies
- run procedural generation passes
- manually adjust generated roads, curves, and placements
- define, inspect, or review faction influence layers

The builder may also stage draft content before publication into canonical runtime data.

Hard boundary:

- a builder viewport is not runtime truth by itself
- generated output becomes canonical only when written into backend-owned map data through approved publication or editing flow

TODO:

- define publication workflow from draft builder state into canonical runtime state
- define whether builder drafts are tool-owned only or may reference canonical records before publication

## 5. Derived 2D runtime map

The runtime player-facing world map is a derived 2D presentation layer.

This rule is locked:

- the actual game runtime must not require rendering the full 3D world map

Allowed derived presentation forms include:

- biome-color-based beauty render
- roads overlay
- rivers overlay
- labels overlay
- icons or POI markers
- different zoom levels or granularity bands

These are all derived views of the same canonical map truth, not separate truths.

The project may support multiple derived runtime views, such as:

- high-level world view
- regional map view
- local overview map

Those views remain presentation derivatives unless a later contract explicitly promotes some map abstraction into canonical simulation input.

Beauty-rendered maps are presentation assets, not canonical truth.

## 6. Discovery and knowledge model for maps

This boundary is non-negotiable.

- a place may exist canonically before the player knows about it
- visibility is viewpoint-specific
- naming is viewpoint-specific
- POI reveal is viewpoint-specific
- discovery progression is not frontend-owned

Map reveal may happen through:

- travel
- rumor
- NPC dialogue
- quest intel
- acquired maps
- other approved information acquisition paths

The frontend may render reveal state, but it must not invent it.

Examples of reveal progression that fit this boundary:

- an unnamed settlement marker becomes visible before the settlement name is known
- a route is rumored to exist before it is confirmed
- a hidden ruin exists canonically but appears only after discovery or intel
- a region name is known while specific POIs within it remain unknown

This document does not define the full discovery data model. It only locks the separation:

- canonical spatial truth is one thing
- player/viewpoint knowledge about that truth is another

AI boundary within map reveal:

- AI may narrate or summarize only what the current viewpoint can reasonably know under backend-approved reveal rules
- AI must not directly reveal hidden canonical places, names, routes, or POIs outside approved viewpoint rules

TODO:

- define minimum discovery-state contract for place visibility, naming visibility, and POI visibility
- define whether discovery is tracked only for the player viewpoint or for all relevant actors and institutions
- define how acquired paper maps, charts, or equivalent intel interact with discovery state

## 7. Procedural generation responsibilities

Procedural generation and analysis passes are separate from canonical storage.

Likely generation or processing passes include:

- river or hydrology generation
- settlement suitability or settlement fill
- road generation
- faction influence propagation
- trade route generation

These passes are backend services, builder tools, or controlled publication workflows operating on map data. They are not spontaneous AI truth generation.

Hard boundary:

- procedural output is not canon merely because a generation pass produced it
- generated results become canonical when accepted and written into backend-owned spatial state
- AI may assist authoring analysis, but AI does not directly declare map truth

TODO:

- define which generation passes are builder-time only versus runtime-safe preprocessing
- define how accepted generated output is reviewed or published

## 8. Deferred explicitly

The following are intentionally deferred:

- full hydrology realism
- erosion or climate simulation
- real-time world regeneration
- tactical combat terrain generation
- orbital mechanics
- full economy or trade simulation
- full discovery runtime implementation details
- exact reveal-storage schema
- exact beauty-map export format
- exact builder publication workflow

## 9. Minimal build order recommendation

Recommended narrow order:

1. lock canon and ownership boundaries for the map system
2. implement a minimal spatial slice with `x`, `y`, `z`, biome, one settlement, and one hidden POI
3. define a derived beauty-map export contract
4. define a minimal discovery contract for visibility and naming reveal
5. implement builder tooling v0 against canonical spatial data
6. add procedural generation passes later as explicit backend or tooling layers

This sequence is intentionally modest. The project does not need a full map engine before it can lock the boundaries correctly.

## 10. Non-negotiable rules

- Runtime game map is a 2D presentation layer, not canonical 3D world rendering.
- Beauty map output is derived presentation, not truth.
- Hidden places may exist canonically before discovery.
- Frontend does not own reveal truth.
- AI does not directly reveal hidden map truth outside approved backend or viewpoint rules.
- Campaign builder edits canonical data but is not truth by itself.
