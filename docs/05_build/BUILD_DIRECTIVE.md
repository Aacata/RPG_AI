# Byggdirektiv: batch, review, drift, commit, nästa batch

## Syfte

Detta dokument är **det operativa byggdirektivet** för autonoma implementationssessioner: en repeterbar cykel som minskar drift, halvfärdiga lägen och glömda pushar. **Alla agenter som implementerar kod ska följa denna cykel** om inte användaren uttryckligen begränsar omfattningen till en enstaka ändring.

Canon och läsordning förblir i [`AGENT_RULES.md`](../../AGENT_RULES.md) och [`SESSION_MANIFEST.md`](SESSION_MANIFEST.md). Detta direktiv styr **hur** batch-arbete utförs och när cykeln pausas för mänsklig input.

---

## Cykel (upprepa tills blockerare)

### 1. Välj batch

- Ta **en** tydlig batch från [`PHASE2_CLOSE_PLAN.md`](PHASE2_CLOSE_PLAN.md), [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md), eller användarens explicita mål.
- Begränsa batch till det som går att **reviewa** och **testa** i samma pass (hellre två små batcher än en stor).

### 2. Implementera batch

- Följ canon/kontrakt; ändra bara det som batch kräver.
- Kör relevanta tester (minst `python -m unittest discover -s tests -p "test_*.py"` när Pythonkod berörs).

### 3. Review batch (självreview innan commit)

- Läs diffen: finns det oavsiktliga ändringar, debug-kod eller uppenbar risk?
- Kontrollera mot [`REVIEWER_GATEKEEPER.md`](REVIEWER_GATEKEEPER.md) (gate: backend truth, events, inga AI-authoritative shortcuts).
- Uppdatera **status-/plan-docs** om batch ändrar vad som är sant i repo (så [`IMPLEMENTATION_STATUS.md`](IMPLEMENTATION_STATUS.md) inte driver).

### 4. Drift och buggar

- **Drift:** stäm av korta statusrader i build-docs mot faktisk kod (t.ex. "not implemented" som redan finns).
- **Buggar:** åtgärda uppenbara regressions; om något är osäkert och kräver canon-beslut → notera i commit eller stoppa vid steg 6 (mänsklig input).

### 5. Patch vid behov

- Minimal patch; kör tester igen efter patch.

### 6. Commit och push (GitHub)

- **Ingen** `__pycache__` eller `*.pyc` i commit (se repo-`.gitignore`).
- Ett commit per färdig batch (eller en tydligt beskriven grupp om batcherna är atomärt sammankopplade).
- Meddelande: kort **vad** och **varför** (engelska eller svenska enligt team, konsekvent).
- `git push` till `origin` för aktuell branch (efter commit).

### 7. Nästa batch (automatiskt)

- Utan ny användarprompt: välj **nästa** prioriterade item från samma plan-källor.
- **Starta om cykeln** från steg 1 för den batchen.

---

## När cykeln MÅSTE pausas (vänta på mänsklig input)

- Canon eller kontrakt **motsäger** varandra eller kräver produktval (t.ex. låsta enum-namn som påverkar röst/routing).
- **Autentisering eller secrets** (tokens, lösenord, org-specifik remote).
- **Destruktiva** git-operationer utanför normal commit/push på nuvarande branch.
- **CI/regression** som kräver beslut utanför kod (t.ex. policyändring).
- Uppgift är **omenbar** trots läsning av canon (rapportera vad som saknas, gör inte gissningar).

När du pausar: lämna kort handoff (vad som gjorts, vad som blockerar, nästa förslag) i svar eller i relevant build-fil om sessionen uttryckligen kräver det.

---

## Översättning till engelska (samma process)

Implement batch → self-review batch → check doc/code drift and bugs → patch if needed → commit and push to GitHub → automatically pick and start the next batch until a human-input stop condition above applies.

---

## Nästa steg (operativt)

Efter varje lyckad push: öppna [`PHASE2_CLOSE_PLAN.md`](PHASE2_CLOSE_PLAN.md) och ta nästa **Remaining Work**-punkt som batch 1, eller den punkt användaren pekat ut.
