# Excellens Curriculum & Pedagogical Rules (`curriculum_rules.md`)

This specification defines the pedagogical architecture, learning journey phases, exercise design methodology, error diagnostics, and assessment philosophy for all Excellens lessons.

---

## 1. The Core Learning Progression Phases

Every Excellens lesson constructs a flexible learning journey spanning mandatory pedagogical phases. The exact number of modules/sections adapts to topic complexity, but must incorporate the following phase types:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. CURIOSITY & PREREQUISITE CHECK                                       │
│    • Low-stakes diagnostic questions to verify baseline readiness       │
│    • Intriguing real-world challenge or intuition hook                  │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. ACTIVE DISCOVERY & INTERACTION                                       │
│    • Predict-first interactive engine (sliders, inputs, toggles)        │
│    • Immediate visual feedback on prediction vs. outcome                │
├─────────────────────────────────────────────────────────────────────────┤
│ 3. INTUITION & MICRO-RULE ABSTRACTION                                   │
│    • Concise 1-sentence takeaways derived directly from discovery       │
│    • Visual icon + rule pairing for schema building                     │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. DUAL-CODING & MULTI-REPRESENTATION                                   │
│    • Switching context (e.g. spatial axis to physical/real-world gauge) │
│    • Demonstrates universal validity across real-world domains          │
├─────────────────────────────────────────────────────────────────────────┤
│ 5. GUIDED ANIMATION & FORMALIZATION                                     │
│    • Step-by-step walkthrough of tricky edge cases                      │
│    • Formal mathematical/scientific notation & sign/rule tables         │
│    • Worked examples with numbered step counters                        │
├─────────────────────────────────────────────────────────────────────────┤
│ 6. GUIDED COACHING PRACTICE                                             │
│    • Scaffolded exercise with optional step-by-step hints               │
│    • Expandable detailed correction walkthrough                         │
├─────────────────────────────────────────────────────────────────────────┤
│ 7. AUTONOMOUS PRACTICE & DIAGNOSTIC REPLAY                              │
│    • Graded exercise series with instant verification                   │
│    • Captures incorrect responses directly into Error Notebook          │
├─────────────────────────────────────────────────────────────────────────┤
│ 8. MASTERY ASSESSMENT & RETENTION REPORT                                │
│    • Synthesis quiz to evaluate overall concept retention               │
│    • Personalized mastery card with strength/weakness summary          │
├─────────────────────────────────────────────────────────────────────────┤
│ 9. REVISION EXPRESS SHEET                                               │
│    • Ultra-condensed cheat sheet (5-second visual digest cards)         │
│    • Common exam traps checklist & pre-submission checklist            │
├─────────────────────────────────────────────────────────────────────────┤
│ 10. METACOGNITION & FEYNMAN TECHNIQUE                                   │
│    • Open-ended student prompt: "Explain this concept in your own words"│
│    • Model answer & self-evaluation rubric checklist                    │
├─────────────────────────────────────────────────────────────────────────┤
│ 11. TIMED EXAM SIMULATION & ANALYTICS                                   │
│    • Official exam-style questions under a countdown timer              │
│    • Skill-by-skill percentage breakdown analytics and feedback         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Exercise Design & Scaffolding Principles

1. **Scaffolded Hints**:
   - Every guided exercise must provide progressive assistance.
   - Hint 1: Conceptual reminder or visual strategy.
   - Hint 2 / Solution: Detailed step-by-step breakdown.

2. **Error Notebook & Diagnostic Hints**:
   - When a student submits an incorrect answer in autonomous practice or exams, the framework records:
     - Question text
     - Student's response
     - Correct target response
     - Skill category
     - Specific diagnostic feedback explaining *why* the error occurred.

3. **Feynman Self-Teaching Technique**:
   - Asks the student to explain a core rule in plain language as if teaching a beginner.
   - Upon submission, reveals a structured Model Explanation and a self-evaluation checklist.

4. **Non-Blocking Exercise Progression Protocol**:
   - Wrong answers MUST NEVER block stage progression or lock the student in a stuck state.
   - The exercise **attempt** itself satisfies the stage advancement criteria:
     - **Correct Answer**: Displays positive feedback, awards XP, triggers milestone confetti, and unlocks the next stage.
     - **Incorrect Answer**: Displays clear explanation and diagnostic correction (`❌ Pas tout à fait...`), logs entry into Error Notebook, permits additional retries, AND STILL unlocks the next stage (`if (student_attempted) unlock_next_stage()`).
   - Learning occurs through active attempts, immediate feedback, and risk-free iteration.

---

## 3. Assessment Philosophy

1. **Low-Stakes Non-Blocking Diagnostics**: Initial tests and practice questions never block progress; they identify baseline readiness and encourage continuous forward momentum.
2. **Mastery Verification**: End-of-lesson assessment measures multi-faceted understanding.
3. **Exam Simulation**: Timed evaluations simulate real exam conditions, offering detailed skill analytics across cognitive levels (Easy, Medium, Hard, Official Exam standard).
