# Voice System

## Purpose

Define the canonical voice and audio pipeline for the simulation engine. The voice
system is a presentation and asset layer above the backend. It reads finalized
backend-approved text and actor state, then produces audio output. It does not
generate story content, decide NPC behavior, or mutate canonical world state.

Cross-reference:

- `docs/03_systems/AI_STACK.md`
- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/02_canon/DATA_OWNERSHIP.md`
- `docs/04_contracts/NPC_STATE_SCHEMA.md`

---

## Core Principles

- Voice is downstream of backend-approved text. Audio is never generated before
  the text it renders has been validated by backend systems.
- Voice routing is backend-owned. No frontend or AI layer decides which voice
  path an actor uses.
- Voice identity is persisted in backend-owned NPC voice profiles, not in
  transient session state or frontend configuration.
- Heavy offline generation (Fish Speech, Tortoise, Stable Audio) is factory work,
  not runtime work. These paths produce assets that are registered in the backend
  audio ledger before use.
- The emote bank is a curated recorded asset library, not a generated output.

---

## Responsibilities

- Route NPC and narrator speech to the correct voice provider based on actor
  importance tier and available reference assets
- Render finalized backend-approved text to audio
- Persist generated audio clips in the backend audio ledger
- Manage NPC voice profiles and voice identity references
- Support offline batch generation of high-quality dialogue, ambient, and SFX assets
- Register all voice seed, SFX, and ambient asset slots in the backend sound registry
- Enforce curation gates before generated seeds become trusted references

## Non-Responsibilities

- Generating story content or NPC dialogue text
- Deciding NPC behavior or canonical actor state
- Owning microphone input or transcription logic
- Rendering UI audio controls or playback interfaces
- Replacing the backend audio ledger with frontend-managed audio state
- Treating unapproved seeds as production-ready references

---

## Voice Components

See `docs/03_systems/AI_STACK.md` for full component descriptions.

| Component           | Role                          | Runtime Use |
|---------------------|-------------------------------|-------------|
| GPT-SoVITS          | Fast runtime NPC speech       | Yes         |
| Kokoro TTS          | Generic fallback speech       | Yes         |
| Fish Speech S2 Pro  | HQ offline dialogue factory   | Offline     |
| Tortoise TTS        | Voice seed generator          | Offline     |
| Stable Audio Open   | Ambient and SFX factory       | Offline     |
| Emote Bank          | Curated human vocal reactions | Yes         |

---

## NPC Voice Routing

Voice routing is a backend-owned decision made per actor per speech event.
The routing engine evaluates actor state and available assets before selecting a path.

### Routing Decision Tree

```
Does the actor have a personal voice reference WAV?
├── Yes → Is the actor companion or essential tier?
│         ├── Yes → GPT-SoVITS (primary)
│         │         └── Fallback: Fish Speech HQ clip (if pre-rendered exists)
│         └── No  → GPT-SoVITS (primary)
│                   └── Fallback: Kokoro TTS
└── No  → Is the actor plot-relevant or named?
          ├── Yes → Kokoro TTS with archetype voice hint
          └── No  → Kokoro TTS generic
                    └── Fallback: Text only (no audio)
```

### Routing Rules

- GPT-SoVITS is only activated when a personal reference WAV is registered for
  the actor in the backend NPC voice profile table.
- Kokoro TTS requires no reference WAV and is always available as fallback.
- Fish Speech pre-rendered clips may supplement GPT-SoVITS for pre-authored
  campaign content but are not a live runtime alternative.
- Text-only fallback is always valid. Audio is enhancement, not a requirement.
- Routing decisions are logged for observability.

---

## NPC Voice Profiles

Each named or important NPC may have a backend-owned voice profile.

### Voice Profile Data (placeholder schema)

- Actor ID reference
- Voice archetype ID
- Reference WAV path or registry key
- Preferred runtime provider
- Fallback provider
- Voice theme metadata
- Curation status of associated seeds

Voice profiles are created and managed through backend service contracts.
Frontend and campaign tooling may display profiles but do not own them.

---

## Archetype System

Voice archetypes provide a reusable identity foundation for NPC voice generation.
Archetypes are settings-agnostic at the core level. Settings-specific archetypes
are defined in the campaign builder.

### Archetype Design Rules

- Core archetype IDs must be gender-neutral where possible.
- Gender is handled via `male.wav` and `female.wav` seed slots per archetype.
- Title variants such as king, queen, captain, or elder are metadata labels
  above a shared archetype, not separate core archetype IDs.
- Archetype IDs use lowercase snake_case.

### Example Core Archetypes

| Archetype ID       | Domain                              |
|--------------------|-------------------------------------|
| `elder_wise`       | Ancient, calm, authoritative        |
| `warrior_gruff`    | Direct, physical, blunt             |
| `merchant_shrewd`  | Calculating, persuasive, measured   |
| `priest`           | Formal, reverent, composed          |
| `magic_wielder`    | Unusual cadence, intense, precise   |
| `charmer`          | Warm, fluid, socially aware         |
| `monarch_regal`    | Commanding, formal, measured        |
| `outcast_rough`    | Guarded, irregular, weathered       |
| `scholar`          | Precise, absorbed, methodical       |
| `hermit`           | Sparse, distant, deliberate         |
| `blacksmith`       | Straightforward, physical, reliable |
| `corrupt_noble`    | Polished surface, cold interior     |
| `young_hero`       | Eager, unsteady, earnest            |
| `narrator`         | Clear, paced, authoritative         |

Settings-specific archetypes such as `ai_operator`, `space_pilot`, or
`street_hacker` are defined in campaign builder configuration, not in core canon.

---

## Vox Factory — Offline Asset Pipeline

The Vox Factory is the offline batch generation system for high-quality voice seeds,
pre-rendered dialogue, ambient soundscapes, and SFX assets.

Factory work runs separately from the live runtime. Assets produced by the factory
are reviewed, curated, and registered in the backend sound registry before use.

### Factory Paths

#### Voice Seed Generation (Tortoise TTS)
- Generates `male.wav` and `female.wav` reference seeds per archetype
- Seeds stored in `assets/voice_seeds/`
- All seeds start with curation status `pending`
- Seeds must be reviewed and marked `approved` before becoming trusted references
- Approved seeds may be rerendered at higher quality in a later pass
- Batch runner: `tools/run_tortoise_seed_batch.py`

#### HQ Dialogue Generation (Fish Speech S2 Pro)
- Generates high-quality pre-rendered dialogue clips for campaign content
- Suitable for cutscene-style content, archetype library building, and
  important lines that benefit from voice-identity fidelity
- Not suitable for live runtime due to latency
- Outputs registered in the backend audio ledger before use
- Generated clips reviewed before becoming trusted long-term assets

#### Ambient and SFX Generation (Stable Audio Open)
- Generates ambient soundscapes, music beds, and SFX clips
- Outputs registered in the backend sound registry
- Generated clips reviewed before becoming trusted long-term assets

#### Emote Bank (Curated Recorded Assets)
- Human nonverbal vocal reactions: laughs, sighs, gasps, pain, grunts, surprise
- Source: curator-recorded real audio, not AI-generated
- Fish Speech and Stable Audio are not the primary source for human emotes
- Location: `assets/emote_bank/`
- Status: placeholder until recorded assets are ingested

### Curation Workflow

```
Generate seed or clip
        ↓
Status: pending
        ↓
Human review (listen, evaluate)
        ↓
Mark approved or rejected via curation tool
        ↓
Approved → available for runtime use or higher-quality rerender
Rejected → logged, excluded from production paths
```

Curation tools:
- `tools/build_seed_curation_board.py` — generates review report
- `tools/set_seed_curation_status.py` — updates curation status per seed

---

## Backend Audio Ledger

All generated audio clips are registered in the backend audio ledger.

Minimum ledger record (placeholder):
- Clip ID
- Actor or context reference
- Text content that was rendered
- Provider used
- File path or storage reference
- Generation timestamp
- Curation status where applicable

The audio ledger is backend-owned. Frontend and tooling may read from it
but do not write to it directly.

---

## Runtime Voice Conversation Flow

The canonical end-to-end NPC voice conversation path:

```
Player input
      ↓
Backend resolves NPC dialogue text
(via rules, AI interpretation, and approval)
      ↓
Backend selects voice provider
(routing engine evaluates actor tier and reference assets)
      ↓
Voice adapter renders audio from approved text
      ↓
Audio clip registered in backend audio ledger
      ↓
Audio clip reference returned to presentation layer
      ↓
Presentation layer plays audio
```

At no point does the presentation layer own text generation, routing decisions,
or audio ledger state.

---

## Future Speech-to-Text

Microphone audio capture may reside in the presentation layer.
Transcription, intent routing, and dispatch into gameplay or NPC dialogue
must be backend-owned service contracts.

Voice commands and spoken NPC dialogue must feed the same canonical
chat and action path as typed input.

No paid or cloud-dependent STT service is planned. Local STT options
will be evaluated when this path is implemented.

Status: deferred, not yet in implementation scope.

---

## Owned Data

- NPC voice profiles
- Voice archetype registry
- Backend sound registry (seeds, SFX, ambient slots)
- Backend audio ledger (generated clips)
- Seed curation status records
- Voice routing configuration

## Dependencies

- `npc` for actor tier and identity
- `adapters/voice/` for all provider interfaces
- `ai` for text generation upstream of voice rendering
- `rules` and `core` for approved text before rendering
- `events` for audio clip history linkage where needed

## Likely Future Extensions

- Party or group voice management
- Dynamic voice aging or condition effects
- Setting-specific archetype packs in campaign builder
- Local speech-to-text integration
- Voice-driven player input routing

## Open Questions

- How reference WAVs are versioned and replaced over time
- Whether companion voice identity should lock a WAV permanently or allow updates
- How the emote bank ingestion workflow is formally defined
- Whether Fish Speech pre-rendered clips need their own curation tier
- How setting-specific archetypes are validated and versioned in the campaign builder
