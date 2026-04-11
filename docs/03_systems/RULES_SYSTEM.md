# Rules System

## Purpose

Provide deterministic resolution logic for authoritative gameplay and simulation outcomes.
The rules system is settings-agnostic at its core. Campaign-specific skill sets, stat
variations, and rule extensions are layered on top through the campaign builder without
replacing or overriding core resolution authority.

Cross-reference:

- `docs/02_canon/PROJECT_BRAIN.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/EVENT_MODEL.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

---

## Core Resolution Formula

```
1d20 + attribute_value + skill_bonus + situational_bonus >= DC
```

### Components

- `attribute_value`: The raw canonical base stat of the acting actor (1–10).
- `skill_bonus`: The actor's trained skill level for the relevant skill. If untrained,
  defaults to `floor(attribute_value / 2)`.
- `situational_bonus`: A signed integer derived from the AI-assessed context category.
  Backend translates the category into the authoritative numeric value.
- `DC`: The difficulty class set or derived by backend rules for the action type.

### Natural Roll Results

- `Natural 20`: Always a critical success regardless of total or DC.
- `Natural 1`: Always a critical failure regardless of total or DC.

---

## Attributes

Eight canonical base attributes. Range is 1–9 at actor creation, maximum 10 during play.
Attributes are settings-agnostic and apply to all campaign types.

| Attribute     | Abbreviation | Primary Domain                                  |
|---------------|--------------|-------------------------------------------------|
| Strength      | STR          | Physical force, melee, carry capacity           |
| Agility       | AGI          | Speed, stealth, precision, evasion              |
| Physique      | PHY          | Endurance, health, resistance, stamina          |
| Psyche        | PSY          | Willpower, mental resistance, emotional control |
| Intelligence  | INT          | Reasoning, memory, analysis, learning           |
| Charisma      | CHA          | Social influence, persuasion, performance       |
| Perception    | PER          | Awareness, tracking, reading people             |
| Luck          | LCK          | Passive saves and active reroll resource        |

---

## Luck Mechanics

Luck is a mechanical resource, not a trainable skill.

### Passive Luck Save
When a Natural 1 is rolled, a hidden automatic save is triggered:
`1d20 + luck_value >= 15`
A successful passive save reduces or negates the critical failure effect.
Backend determines the mitigation scope.

### Active Luck Burn
The player may choose to spend 1 permanent luck point before a result is finalized.
Effect: roll 2d20 and keep the better result.
Luck points spent this way are permanently reduced.
NPC luck burn is backend-governed and not player-controlled.

---

## Skill System

### Skill Levels

Skills use an open numeric scale. There is no hard upper ceiling.

| Range  | Label        | Description                                      |
|--------|--------------|--------------------------------------------------|
| 0      | Untrained    | No training. Uses attribute / 2 as bonus floor.  |
| 1–5    | Novice       | Basic familiarity.                               |
| 6–10   | Trained      | Reliable competence.                             |
| 11–15  | Expert       | Advanced mastery.                                |
| 16–20  | Master       | Peak standard human capability.                  |
| 21+    | Exceptional  | Beyond normal human limits. Rare.                |

### Untrained Skill Bonus
If an actor does not have a skill, the bonus for that check defaults to:
`floor(linked_attribute_value / 2)`

This means attribute quality still matters even without training.

### Skill Progression
Skills increase through experience, practice, and explicit learning events.
New skills may be acquired during play if canon and campaign rules permit.
Progression is backend-owned. AI may suggest readiness but does not grant level increases.

### Skill Categories

Skills are divided into two layers:

**1. Universal Base Skills**
Present on all actors across all settings. Tied to a canonical attribute.
These are locked in core canon and cannot be removed by campaign configuration.

**2. Setting Skills**
Defined in the campaign builder. Tied to canonical attributes but vary by genre.
Examples: fantasy spellcasting, space piloting, hacking, divine calling.

---

## Universal Base Skills

### Strength (STR)
| Skill          | Description                                     |
|----------------|-------------------------------------------------|
| Climb          | Scale surfaces, walls, or terrain               |
| Lift           | Move, hold, or throw heavy objects              |
| Break          | Force open, destroy, or overpower structures    |
| Grapple        | Seize, restrain, or wrestle another actor       |
| Melee Strike   | Unarmed or basic melee attack                   |

### Agility (AGI)
| Skill              | Description                                     |
|--------------------|-------------------------------------------------|
| Sneak              | Move without being detected                     |
| Dodge              | Evade incoming physical attacks or hazards      |
| Acrobatics         | Balance, tumble, vault, or perform agile feats  |
| Pickpocket         | Remove items from a person without detection    |
| Sleight of Hand    | Conceal small items or perform manual tricks    |
| Ranged Attack      | Attack with thrown or projectile weapons        |

### Physique (PHY)
| Skill            | Description                                     |
|------------------|-------------------------------------------------|
| Swim             | Move through or survive in water                |
| Sprint           | Burst of short-duration maximum speed           |
| Endure           | Sustain physical effort over time               |
| Resist Disease   | Fight off illness or infection                  |
| Resist Pain      | Maintain function under physical suffering      |
| Brace            | Withstand impact, knockback, or physical force  |

### Psyche (PSY)
| Skill                | Description                                   |
|----------------------|-----------------------------------------------|
| Resist Fear          | Maintain composure under terror or dread      |
| Willpower            | Hold resolve against coercion or temptation   |
| Concentration        | Sustain focus during distraction or pressure  |
| Resist Manipulation  | Recognize and resist social or mental coercion|

### Intelligence (INT)
| Skill        | Description                                         |
|--------------|-----------------------------------------------------|
| Investigate  | Find clues, examine scenes, connect information     |
| First Aid    | Stabilize wounds or treat basic injuries            |
| Remember     | Recall facts, lore, or past experiences             |
| Analyze      | Interpret patterns, weaknesses, or hidden structure |
| Craft        | Construct, repair, or modify physical objects       |

### Charisma (CHA)
| Skill      | Description                                           |
|------------|-------------------------------------------------------|
| Persuade   | Convince through argument, appeal, or negotiation     |
| Deceive    | Mislead, lie, or maintain a false identity            |
| Intimidate | Coerce through fear, force of personality, or threat  |
| Perform    | Entertain, orate, or express through art or spectacle |
| Seduce     | Attract, charm, or create romantic or social tension  |

### Perception (PER)
| Skill         | Description                                        |
|---------------|----------------------------------------------------|
| Spot          | Notice visual details, movement, or hidden things  |
| Listen        | Detect sounds, voices, or activity by ear          |
| Track         | Follow movement traces across terrain or time      |
| Read Person   | Interpret mood, intent, or deception in an actor   |
| Search        | Systematically examine an area for hidden content  |

### Luck (LCK)
Luck has no trainable skills. It functions only through passive saves and active burns
as described in the Luck Mechanics section.

---

## Situational Bonus System

AI assesses the context of a proposed action and returns a named difficulty category
with a narrative justification. Backend translates the category into the authoritative
numeric modifier applied to the roll.

AI never returns a raw number. AI returns a category and a reason.
Backend owns the numeric mapping and may override category translation if canon rules
require it.

### Difficulty Categories

| Category       | Situational Bonus | Example Context                                          |
|----------------|-------------------|----------------------------------------------------------|
| Routine        | +15               | Practiced actor doing a familiar task in ideal conditions|
| Trivial        | +10               | Simple task with no real obstacle                        |
| Easy           | +5                | Minor challenge, favorable conditions                    |
| Standard       | 0                 | No significant advantage or disadvantage                 |
| Challenging    | -5                | Meaningful obstacle, unfavorable conditions              |
| Hard           | -10               | Significant opposition, adverse context                  |
| Extreme        | -15               | Near the edge of what is realistically possible          |
| Absurd         | -25               | Wildly implausible given actor state and world context   |
| Impossible     | BLOCKED           | Cannot proceed regardless of roll result                 |

### BLOCKED Actions

An action may be blocked before a roll is attempted.

**AI may block** when the action is narratively impossible given world state, actor
condition, or physical reality as AI understands it from context.

**Backend may block** when the action violates a hard rule, a canonical constraint,
a faction access rule, a travel blocker, or a state precondition.

Both block types are logged. A blocked action does not produce a roll result.
The blocking reason is recorded as part of the action resolution event.

### Advisory Proposal Linkage

AI situational assessments are advisory proposals as defined in `AI_PROPOSAL_FLOW.md`.
Each assessment carries:
- The proposed difficulty category
- A narrative justification string
- The source context used to reach the assessment
- Validation status once backend confirms or overrides

Backend may override the AI category if rule conditions mandate a different result.
The override and original proposal are both logged for auditability.

---

## Character Level and Progression

### Actor Level
Actors have a derived total level representing accumulated capability.
Level is computed from total earned experience points or total skill investment
depending on campaign configuration. The exact formula is a TODO pending
campaign builder canon.

### Hit Points
HP represents physical resilience and survivability.

Base formula placeholder:
```
max_hp = base_hp + (physique * physique_multiplier) + (level * hp_per_level)
```

Exact multipliers are campaign-configurable but must be registered in backend
canon before campaign launch. AI does not set HP values.

### Level Effects
Level influences:
- Maximum HP
- Carry capacity thresholds
- Number of available actions per turn (placeholder, combat system TODO)
- Resistance thresholds for certain rule checks
- NPC threat assessment inputs for AI context

Level does not grant immunity to rules or bypass DC resolution.
A high-level actor still fails a Natural 1. A blocked action remains blocked.

---

## Responsibilities

- Resolve deterministic outcomes via the core formula
- Validate and translate AI difficulty category proposals into numeric modifiers
- Block actions that violate hard rules or canonical constraints
- Apply campaign rule variations without shifting truth ownership
- Emit or trigger event creation for all authoritative outcomes
- Own skill level validation and progression gating

## Non-Responsibilities

- Freeform narrative generation
- Frontend interaction design
- Dashboard authoring workflows
- Replacing the event history model with summaries or interpretations
- Deciding situational context narratively — that belongs to AI interpretation
- Granting skill increases without backend validation

## Inputs

- Canonical world state
- Canonical actor state including attributes, skills, and level
- Inventory, faction, and quest state
- AI-proposed difficulty category and justification
- User or AI proposed actions
- Campaign rule configuration

## Outputs

- Approved state transitions
- Deterministic outcome records including roll result, components, and final verdict
- Event payload inputs
- Block reasons when actions cannot proceed
- Skill progression approvals

## Owned Data

- Core resolution formula and DC definitions
- Attribute definitions and ranges
- Universal base skill list and attribute mappings
- Difficulty category to numeric bonus mapping
- Validation and block logic
- Campaign rule variation hooks

## Dependencies

- `core` for orchestration
- `world`, `npc`, `inventory`, `quests`, `factions` for state inputs
- `events` for authoritative history linkage
- `ai` for advisory difficulty proposals via `AI_PROPOSAL_FLOW.md`

## Likely Future Extensions

- Combat resolution module with action economy
- Social resolution module with relationship pressure inputs
- Extended skill trees per campaign setting
- Per-campaign rule packages loaded at campaign init
- Compound skill checks combining multiple attributes

## Open Questions

- Exact XP formula and level thresholds pending campaign builder canon
- Whether HP multipliers are global defaults or always campaign-configured
- How setting skills are validated and versioned in the campaign builder
- Whether compound checks use average, highest, or lowest attribute combination
- How BLOCKED reasons surface to the player versus staying internal to backend logs