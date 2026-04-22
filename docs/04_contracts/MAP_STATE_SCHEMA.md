# Map State Schema

## 1. Purpose

This document defines the minimum canonical spatial state contract for the project.

It is not a full map engine specification. It exists to lock the smallest backend-owned spatial model that can support:

- canonical spatial truth
- actor placement against canonical map references
- hidden-but-existing places
- later discovery separation
- later derived 2D map rendering

Cross-reference:

- `docs/03_systems/MAP_SYSTEM.md`
- `docs/04_contracts/WORLD_STATE_SCHEMA.md`
- `docs/04_contracts/KNOWLEDGE_MODEL.md`
- `docs/02_canon/DATA_OWNERSHIP.md`

Status note:

- `WorldSpaceRecord`, `RegionRecord`, and `LocationRecord` exist in code.
- `LocationRecord` currently carries `x`, `y`, `z`, `biome`, and `is_hidden_by_default`.
- Narrow validated mutation support currently exists for `RegionRecord.world_space_ref`.
- Full mutation-surface rollout for all `LocationRecord` spatial fields is not implemented.
- Actor spatial linkage remains `location_ref` only.

## 2. Scope of this contract

This contract covers only the minimum canonical spatial data needed now for:

- a world / region / location style hierarchy
- canonical placement references
- `x`, `y`, `z` coordinate capability
- biome attachment at MVP level
- hidden-but-existing place support
- actor -> map reference linkage boundaries

This contract does not cover now:

- full campaign-builder workflows
- beauty map export format
- full discovery runtime schema
- hydrology generation
- roads generation
- trade route simulation
- faction propagation logic
- travel runtime resolution
- polygon tooling or final border geometry
- runtime rendering implementation details

## 3. Minimum canonical spatial record model

Recommended MVP-level canonical record set:

- `WorldSpaceRecord`
- `RegionRecord`
- `LocationRecord`

POIs are typed locations for now.

This is the recommended MVP choice because:

- the current backend already orients actors around `location_ref`
- the current code already has `RegionRecord` and `LocationRecord`
- a separate POI record would create another canonical place surface before the project has a real need for one
- settlements, ruins, landmarks, shrines, caves, gates, and similar places can all be represented as location types without broadening the schema

### WorldSpaceRecord

Purpose:

- the top-level canonical spatial container for one world or one equivalent playable spatial domain

Exact MVP fields:

- `world_space_id`
- `sea_level_z`

Why each field belongs now:

- `world_space_id`
  - gives a stable canonical anchor for regions
  - prevents region hierarchies from floating without a top-level spatial owner
- `sea_level_z`
  - pays for itself immediately because the project already wants `z = 0` as the normal-world convention
  - is narrower and more useful now than a broader `world_profile` field

Deferred:

- `world_profile`
- world bounds
- climate model
- planetary or orbital model
- multiple simultaneous world spaces in one campaign

### RegionRecord

Purpose:

- a large-area canonical spatial grouping within a world space

Exact MVP fields:

- `region_id`
- `world_space_ref`
- `display_name`
- `region_parent_ref`

Why each field belongs now:

- `region_id`
  - required stable canonical identifier
- `world_space_ref`
  - required to keep regions attached to a top-level spatial container
- `display_name`
  - belongs now because regions are likely to be named canonical places rather than purely invisible partition keys
  - supports future derived map labeling without inventing a second naming source
- `region_parent_ref`
  - should remain present in MVP because the current code already carries it
  - allows thin hierarchical grouping without requiring geometry

Deferred:

- region centroid
- region bounds
- polygon borders
- climate zones
- procedural metadata

### LocationRecord

Purpose:

- a concrete canonical place that actors, systems, and events can reference directly
- settlements, landmarks, ruins, entrances, outposts, shrines, caves, gates, and similar POIs as typed locations

Exact MVP fields:

- `location_id`
- `region_ref`
- `display_name`
- `location_type`
- `x`
- `y`
- `z`
- `biome`
- `is_hidden_by_default`

Why each field belongs now:

- `location_id`
  - required stable canonical identifier
- `region_ref`
  - required to attach a place to world hierarchy
- `display_name`
  - belongs now because both settlements and hidden POIs may have canonical names before discovery
  - frontend reveal rules may hide the name later, but canonical state should still carry it
- `location_type`
  - required because POIs are typed locations in MVP
  - prevents a second record family for settlements versus landmarks versus ruins
- `x`
  - required for canonical spatial anchoring
- `y`
  - required for canonical spatial anchoring
- `z`
  - required for elevation-aware placement and sea-level-relative placement
- `biome`
  - required for minimal place context and later derived map coloring
- `is_hidden_by_default`
  - required to support one hidden-but-existing place model without inventing discovery runtime schema

Deferred:

- sub-location graph structure
- interior or exterior split model
- route graph membership
- local terrain mesh
- tactical terrain detail
- icon metadata
- render metadata
- discovery visibility state

## 4. Coordinate and spatial anchoring rules

Canonical spatial state must support `x`, `y`, `z`.

Exact MVP recommendations:

- `LocationRecord` requires explicit `x`, `y`, `z`
- `RegionRecord` may stay hierarchy-anchored only and does not require explicit coordinates in MVP
- `WorldSpaceRecord` does not require full coordinates, but does require `sea_level_z`

Normal-world convention:

- `z = 0` represents sea level for ordinary ocean-based worlds

Nonstandard settings:

- a later world-profile override may define a different baseline for subterranean, floating, space, or otherwise non-ocean contexts

Concrete choices for MVP:

- `sea_level_z` belongs on `WorldSpaceRecord` now
- region centroid does not belong now
- region bounds do not belong now

TODO:

- define whether future nonstandard world profiles override `sea_level_z` only or also coordinate interpretation

## 5. Biome attachment at MVP level

Recommended MVP option:

- biome is stored directly on `LocationRecord`

Why this is the narrowest useful choice:

- it supports immediate backend truth for place context
- it does not require a separate biome grid, zone graph, or raster layer yet
- it is sufficient for one hidden POI, one settlement, and basic derived map rendering later

Recommended contract-level field shape:

- `biome: str`

For MVP this should be treated as a canonical controlled string, not an open descriptive paragraph and not yet a hard-coded global enum registry.

Example biome terminology:

- forest
- plains
- hills
- mountains
- swamp
- desert
- tundra
- coast

Deferred:

- separate biome cell layers
- blended biome boundaries
- region-scale biome overlays

## 6. Hidden-but-existing place rule at schema level

This rule is locked at canonical-state level:

- a `LocationRecord` may exist before the player knows about it
- undiscovered does not mean absent from canonical state
- discovery state must not be represented by deleting, omitting, or lazily inventing canonical place records

Exact MVP field recommendation:

- `is_hidden_by_default: bool`

Why this field belongs now:

- it is the smallest useful canonical placeholder for hidden-but-existing support
- it supports one hidden POI without inventing player discovery state
- it does not claim to model who knows the place, only that public visibility should not be assumed by default

This document does not define player discovery storage. It only locks the canonical-side rule that existence and discovery are separate concerns.

## 7. Actor linkage boundary

At this phase:

- actors should point to `location_ref`

This is the canonical actor -> map link for MVP because:

- current actor state already has `location_ref`
- current core state already stores actors and locations directly
- location is the smallest useful spatial anchor for actor placement

Region or world references on actors:

- actor region refs stay derivable from `location_ref`
- actor world refs stay derivable from `location_ref -> region_ref -> world_space_ref`

No new actor spatial fields should be added in the next slice unless a concrete blocker appears.

Deferred:

- actor sub-location anchors
- actor coordinate offsets within a location
- direct actor -> region references as canonical fields
- direct actor -> world-space references as canonical fields

## 8. Deferred explicitly

Deferred from this schema contract:

- full builder draft model
- final beauty-map export contract
- full discovery-state schema
- hydrology schema
- road or route-generation schema
- trade route simulation schema
- faction propagation schema
- travel runtime state schema
- biome cell or tile grid schema
- exact region border geometry
- exact map asset pipeline
- region centroid or bounds fields

## 9. Minimal recommended next slice

Next narrow slice:

- a narrow implementation-planning pass for adding the locked MVP fields to the actual world and location records while keeping actor linkage on `location_ref` only
