# World State Schema

## Purpose

Define the minimum conceptual contract for canonical world state.

Cross-reference:

- `docs/03_systems/WORLD_SYSTEM.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/03_systems/TRAVEL_SYSTEM.md`

## Minimum Schema Areas

### Locations

- Canonical location records
- Location identifiers
- Location type placeholder

### Regions

- Region records
- Region hierarchy or grouping placeholder

### Travel Topology

- Route-network placeholder
- Road versus wilderness traversal metadata placeholder
- Setting-specific route-layer placeholder such as sea lanes or space lanes
- Waypoint or route-node placeholder
- Long-distance map-travel initiation support placeholder

### Weather State

- Current weather or environment state placeholder
- TODO: define granularity by location or region

### Terrain / Biome / Traversal Conditions

- Terrain classification placeholder
- Biome placeholder
- Travel-condition modifiers placeholder

### Time / Calendar

- Current simulation time
- Calendar system placeholder
- TODO: define whether campaigns may swap calendar models

### Active Factions

- References to faction entities active in the world
- Presence or influence placeholders
- Travel-access or travel-risk modifiers tied to faction influence placeholder

### Active Events

- References to ongoing or currently relevant event IDs
- TODO: define distinction between immutable events and active state projections

### Active Travel State

- Active travel record or group-travel reference placeholder
- Long-distance fast-forward state placeholder
- Travel interruption or blocker placeholder
- Local travel interruption state placeholder
- TODO: define whether active travel state lives centrally in world state, per actor, or both

### Economy Indicators

- High-level economy placeholders
- TODO: determine whether economy remains in world state or becomes a dedicated subsystem later

### Social / Political State Placeholders

- Social tension placeholder
- Political control or stability placeholder
- Governance model placeholder

### Crime / Law / Response Placeholders

- Wanted-state propagation placeholder
- Witness-response placeholder
- Faction or regional law-response placeholder

## TODO

- Define snapshot granularity.
- Define how region-local and global state relate.
- Clarify persistence strategy for active-event projections.
- Clarify how map-tool-authored topology becomes canonical published world data.
- Clarify whether long-distance map initiation leaves a durable world-state marker or only a travel-state record.
