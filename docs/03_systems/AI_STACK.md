# AI Stack

## Purpose

Define the concrete AI components used in this project, their roles, boundaries, and
integration rules. This document binds the abstract boundary rules in
`docs/02_canon/AI_BOUNDARY_RULES.md` to specific tools and models.

All AI components in this stack are advisory unless explicitly stated otherwise.
Backend systems remain the sole authority over canonical state and deterministic outcomes.

Cross-reference:

- `docs/02_canon/AI_BOUNDARY_RULES.md`
- `docs/04_contracts/AI_PROPOSAL_FLOW.md`
- `docs/03_systems/AI_INTERPRETATION_SYSTEM.md`
- `docs/03_systems/RULES_SYSTEM.md`
- `docs/03_systems/VOICE_SYSTEM.md`

---

## Stack Overview

| Role                        | Component              | Type        | Replaceability         |
|-----------------------------|------------------------|-------------|------------------------|
| Strategic / Narrative AI    | Gemini                 | Cloud API   | High — adapter-owned   |
| Runtime Modulation (FLOW)   | Ollama (model TBD)     | Local       | High — model-agnostic  |
| Fast Runtime Voice          | GPT-SoVITS             | Local       | Medium                 |
| Generic Voice Fallback      | Kokoro TTS             | Local       | High                   |
| HQ Offline Dialogue Factory | Fish Speech S2 Pro     | Local       | Medium                 |
| Voice Seed Generator        | Tortoise TTS           | Local       | Low — seed factory     |
| Ambient and SFX Factory     | Stable Audio Open      | Local       | Medium                 |
| Local Text Generation       | Ollama (model TBD)     | Local       | High — model-agnostic  |

**Design rule**: The only cloud dependency is Gemini. All other components run locally.
ElevenLabs and other paid voice APIs are explicitly excluded.

---

## Layer 1 — Strategic and Narrative AI

### Component: Gemini
**Interface**: `adapters/ai/gemini_adapter.py`
**Type**: Cloud API via `google.genai`

### Role
Gemini is the primary strategic reasoning and long-form narrative layer.

Responsibilities:
- Campaign-scale synthesis and planning
- Long-form travel narration
- Major world event contextualization
- High-importance scene interpretation
- Lore generation and political synthesis
- Difficulty framing proposals for complex social or world-scale actions

### Boundaries
Gemini may:
- Generate narrative text grounded in canonical state
- Propose difficulty categories using the named scale defined in `RULES_SYSTEM.md`
- Suggest candidate state changes for backend validation
- Summarize events, factions, or world conditions

Gemini may not:
- Decide authoritative deterministic outcomes
- Mutate canonical state directly
- Replace event history with narrative summaries
- Leak hidden canonical information to the wrong viewpoint

### Prompt Discipline
- Prompts must be grounded in canonical state packets, not full design documents
- Prompt depth should come from runtime context, not injected architecture docs
- Full outbound prompts are logged for inspection and cost tracking
- Gemini token usage and cost history are persisted in backend storage

### Fallback
If Gemini is unavailable, strategic narration degrades gracefully to a reduced local
text generation path. Backend deterministic systems are unaffected.

---

## Layer 2 — Runtime Modulation (FLOW)

### Component: Ollama with configurable local model
**Interface**: `adapters/ai/flow_adapter.py`
**Type**: Local HTTP via Ollama

### Role
FLOW is the compact runtime modulation layer. It handles short-horizon emotional and
contextual shaping without becoming a second story engine.

Responsibilities:
- Emotional and affective state shaping for NPC responses
- Relationship pressure signals
- Pre-dialogue context conditioning
- Short-horizon tension and pacing modulation
- Compact structured patch output (JSON preferred over prose)

### Model Selection
The specific Ollama model is intentionally deferred. Candidate models will be evaluated
against response quality, latency, and VRAM budget before a model is locked into canon.
Model selection is registered via environment configuration, not hardcoded.

Recommended evaluation candidates:
- `Qwen2.5-1.5B-Instruct` — proven in prior project, very fast
- `Mistral-7B-Instruct` — stronger reasoning, higher VRAM cost
- `Phi-3-mini` — compact, fast, good instruction following

### Boundaries
FLOW may:
- Emit compact structured patches for affect, tension, or relationship pressure
- Shape pre-dialogue context for other AI layers
- Return named modulation signals for backend interpretation

FLOW may not:
- Own canonical state
- Override backend rule outcomes
- Act as an autonomous gameplay agent
- Replace Gemini for long-form narrative or strategic reasoning

### FLOW is not DeerFlow
FLOW is a compact local modulation layer. DeerFlow is an external orchestration
framework. These must not be conflated. FLOW stays narrow and runtime-safe by design.

### Modes
FLOW supports multiple runtime modes configured via environment variables:

| Mode          | Description                                        |
|---------------|----------------------------------------------------|
| `deterministic` | Rule-based fallback with no local model          |
| `local_ai`    | Active Ollama model                                |
| `hybrid`      | Deterministic baseline with local AI enrichment   |
| `disabled`    | FLOW layer inactive, no modulation output          |

---

## Layer 3 — Local Text Generation

### Component: Ollama with configurable local model
**Interface**: `adapters/ai/local_text_adapter.py`
**Type**: Local HTTP via Ollama

### Role
Fast local text generation for low-priority dialogue, background NPC chatter,
ambient scene descriptions, and short-form text tasks that do not require
Gemini's strategic depth.

### Boundaries
- Advisory only
- Does not own narrative truth
- Does not replace Gemini for campaign-scale or high-importance content
- Model is configurable and separate from the FLOW model instance

---

## Voice Stack

The voice stack is a set of adapters above the backend audio ledger. Voice components
read finalized backend-approved text and return audio. They do not generate story
content or mutate world state.

See `docs/03_systems/VOICE_SYSTEM.md` for full voice system documentation.

### GPT-SoVITS — Fast Runtime Voice
**Interface**: `adapters/voice/gpt_sovits_adapter.py`
**Type**: Local HTTP API

Role:
- Primary runtime speech renderer for named NPCs and companions
- Requires a personal voice reference WAV per actor
- Preferred for companions, essential NPCs, and voice-identity-important roles
- Target latency: under 2 seconds for short clips

### Kokoro TTS — Generic Voice Fallback
**Interface**: `adapters/voice/kokoro_adapter.py`
**Type**: Local, embedded

Role:
- Generic fallback for background NPCs, shell-tier actors, and low-priority speech
- No reference WAV required
- Replaces Coqui TTS from prior project
- Significantly better quality than Coqui at equivalent cost (zero)

### Fish Speech S2 Pro — HQ Offline Dialogue Factory
**Interface**: `adapters/voice/fish_speech_adapter.py`
**Type**: Local HTTP API

Role:
- High-quality offline dialogue generation for pre-rendered campaign content
- Not suitable as a fast runtime path due to latency
- Used for HQ dialogue passes, cutscene-style content, and archetype library building
- Canonical target for voice-identity asset generation

### Tortoise TTS — Voice Seed Generator
**Interface**: `adapters/voice/tortoise_adapter.py`
**Type**: Local, isolated Python runtime

Role:
- Offline generation of high-quality archetype voice seeds
- Seeds stored in `assets/voice_seeds/` under backend-managed registry
- Seeds require curation review before becoming trusted references
- Not used for runtime speech

Seed curation rules:
- No seed is assumed approved without explicit curation status
- Seeds are reviewed before higher-quality rerenders
- Gender is handled via `male.wav` / `female.wav` slots, not core archetype IDs
- Core archetype IDs should be gender-neutral where possible

### Stable Audio Open — Ambient and SFX Factory
**Interface**: `adapters/voice/stable_audio_adapter.py`
**Type**: Local

Role:
- High-quality offline ambient soundscape and SFX generation
- Music bed generation for campaign atmosphere
- Not used for NPC speech or dialogue
- Outputs reviewed before becoming trusted long-term assets

### Emote Bank
**Location**: `assets/emote_bank/`

Role:
- Curated recorded human nonverbal vocal reactions
- Laughs, sighs, gasps, pain sounds, grunts, and similar emotes
- Fish Speech and Stable Audio are not the primary source for human emotes
- Status: placeholder until recorded assets are ingested

---

## NPC Voice Routing

Voice path selection is backend-owned and based on actor importance tier.

| Actor Tier              | Primary Voice Path  | Fallback          |
|-------------------------|---------------------|-------------------|
| Companion / Essential   | GPT-SoVITS          | Fish Speech (HQ)  |
| Plot-relevant / Named   | GPT-SoVITS          | Kokoro TTS        |
| Background / Shell      | Kokoro TTS          | None (text only)  |

Rules:
- GPT-SoVITS is only used when a personal voice reference WAV exists for the actor
- Voice identity is persisted in backend-owned NPC voice profiles
- Routing decisions are not made by the frontend or AI layers
- Future speech-to-text input must route through backend transcription contracts,
  not frontend-owned microphone logic

---

## Observability and Cost Control

- Full outbound Gemini prompts are logged to `exports/current/gemini_calls/`
- Gemini token usage and cost history are persisted in backend storage
- FLOW patch outputs are logged with applied / no-op / rejected status
- AI advisory proposals are logged separately from authoritative event history
- Voice clip generation is logged in the backend audio ledger
- Heavy batch jobs (Tortoise, Fish Speech, Stable Audio) should not run concurrently
  with active development or gameplay sessions on the same GPU

---

## Adapter Boundary Rules

All AI and voice components are accessed exclusively through adapter modules.
No system outside the adapter layer may call AI or voice APIs directly.

Adapter responsibilities:
- Translate between internal contracts and external API formats
- Handle authentication, timeouts, and fallback gracefully
- Never own canonical state
- Never make deterministic gameplay decisions
- Return structured outputs that backend systems can inspect and validate

---

## Excluded Components

The following are explicitly excluded from this project:

| Component     | Reason                                          |
|---------------|-------------------------------------------------|
| ElevenLabs    | Paid cloud service, cost prohibitive            |
| Coqui TTS     | Replaced by Kokoro TTS (better quality, maintained) |
| Bark          | Legacy experimental path, not a quality target  |
| Any paid STT  | Future speech-to-text must use local options    |

---

## Environment Configuration

AI and voice components are activated via environment variables, not hardcoded paths.
This allows different runtime profiles without changing source code.

Key variables (exact names are implementation TODO):
- `GEMINI_API_KEY`
- `FLOW_MODE` — `deterministic`, `local_ai`, `hybrid`, `disabled`
- `FLOW_MODEL_NAME` — Ollama model identifier for FLOW
- `LOCAL_TEXT_MODEL_NAME` — Ollama model identifier for local text generation
- `GPT_SOVITS_URL` — local API endpoint
- `FISH_SPEECH_URL` — local API endpoint
- `VOICE_ROUTING_MODE` — override for testing

---

## Open Questions

- Which Ollama model is selected for FLOW after evaluation
- Whether FLOW and local text generation share one Ollama instance or run separately
- How voice reference WAVs are managed and versioned for GPT-SoVITS
- Whether a speech-to-text component is needed and which local option is preferred
- How the emote bank ingestion workflow is defined once recording assets exist
- Whether Gemini fallback narration quality is acceptable or requires a local alternative
