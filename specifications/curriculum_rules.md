# Excellens Curriculum & Pedagogical Rules (`curriculum_rules.md`)

This specification defines the pedagogical architecture, learning journey stages, 5-tier exercise design methodology, error diagnostics, and assessment philosophy for all Excellens lessons.

---

## 1. The Core 8-Stage Learning Progression

Every Excellens lesson constructs a structured cognitive learning journey spanning the **Mandatory 8-Stage Core Backbone**. Optional modular engines (`visualization_engine`, `algebra_manipulation_engine`, `proof_simulation_engine`, `exam_engine`) are dynamically invoked within these stages based on topic requirements:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. ACTIVATE PRIOR KNOWLEDGE (activate_prior)                            │
│    • Low-stakes diagnostic questions to verify baseline readiness       │
│    • Intriguing real-world challenge or intuition hook                  │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. PREDICT-FIRST DISCOVERY (discovery)                                  │
│    • Interactive discovery engine (sliders, inputs, vector arrows)      │
│    • Immediate visual feedback comparing prediction vs. outcome         │
├─────────────────────────────────────────────────────────────────────────┤
│ 3. INTUITION & FORMALIZATION (formalization)                            │
│    • Concise 1-sentence micro-rule takeaway derived from discovery      │
│    • Formal mathematical/scientific notation & sign/rule tables         │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. GUIDED COACHING PRACTICE (guided_practice)                           │
│    • Scaffolded worked examples with numbered step counters             │
│    • Progressive step-by-step hints and detailed correction             │
├─────────────────────────────────────────────────────────────────────────┤
│ 5. MISCONCEPTION REPAIR & ERROR DIAGNOSIS (misconception_repair)       │
│    • CRITICAL: Dismantles deep-seated student error traps               │
│    • Student error analysis of typical Brevet copy mistakes             │
├─────────────────────────────────────────────────────────────────────────┤
│ 6. AUTONOMOUS PRACTICE & DIAGNOSTIC REPLAY (mastery)                    │
│    • Graded autonomous exercise series                                  │
│    • Captures incorrect responses directly into Error Notebook          │
├─────────────────────────────────────────────────────────────────────────┤
│ 7. METACOGNITION & REVISION EXPRESS (reflection)                         │
│    • Open Feynman prompt: "Explain this rule in your own words"         │
│    • Model explanation, self-evaluation rubric, & 5-second cheat sheet  │
├─────────────────────────────────────────────────────────────────────────┤
│ 8. CHRONO EXAM SIMULATION (exam_test)                                   │
│    • Timed exam simulation with interactive countdown timer (exam_engine)│
│    • Final Brevet-standard assessment, speed & precision score report   │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. 5-Tier Exercise Taxonomy & Scaffolding Principles

Every lesson MUST generate **exactly 5 scaffolded exercises** spanning all cognitive levels:

1. **Level 1 (Recognition)**: Identify concept or pattern without calculation.
2. **Level 2 (Transformation)**: Direct 1-step application of core property.
3. **Level 3 (Multi-Step Application)**: Combine 2+ sub-skills (e.g. simplify radical with initial coefficient).
4. **Level 4 (Brevet Standard)**: Contextualized exam-style problem.
5. **Level 5 (Transfer)**: Novel challenge or conceptual extension.

### Exercise Metadata Schema Requirements
Each exercise MUST include rich metadata (`id`, `taxonomyLevel`, `levelName`, `skillTarget`, `cognitiveOperation`, `commonErrorTarget`, `expectedAnswerSchema`, `hintStrategy`, `masteryRequirement`).

---

## 3. Non-Blocking Exercise Progression Protocol

1. Wrong answers MUST NEVER block stage progression or lock the student in a stuck state.
2. The exercise **attempt** itself satisfies the stage advancement criteria:
   - **Correct Answer**: Displays positive feedback, awards XP, triggers milestone confetti, auto-marks completed (sidebar icon -> green ✅), unlocks next stage, and smooth-scrolls.
   - **Incorrect Answer**: Displays clear diagnostic correction (`❌ Pas tout à fait...`), logs entry into Error Notebook, permits additional retries, AND STILL presents an immediate Continue navigation button (`➡ Continuer vers : Étape X`) so learning momentum is never stopped.
