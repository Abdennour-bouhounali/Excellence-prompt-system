# Excellens Educational Invariants (`educational_invariants.md`)

This document defines the non-negotiable **Pedagogical DNA** of the Excellens framework. Regardless of subject domain, target grade, or topic complexity, EVERY lesson produced by the Excellens Educational AI Content Compiler MUST strictly embody these 8 educational invariants.

---

## 1. Prior Knowledge Activation
- **Directive**: Every lesson MUST begin by connecting new concepts to familiar baseline schema (*Activate Prior Knowledge*).
- **Enforcement**: Stage 0 (`activate_prior`) must present low-stakes diagnostic questions or real-world intuition hooks to ground student confidence before introducing abstract concepts.

---

## 2. Predict-First Active Discovery
- **Directive**: Students MUST be prompted to form a mental prediction *before* revealing calculated outcomes or formal formulas.
- **Enforcement**: Interactive discovery engines (sliders, inputs, toggles) must require the student to submit a prediction. Observing outcome vs. prediction creates cognitive misalignment, triggering active schema restructuring.

---

## 3. Micro-Rule Intuition Abstraction
- **Directive**: Abstract rules MUST be derived directly from active discovery as concise, 1-sentence takeaways before formalization.
- **Enforcement**: Immediately following discovery, the lesson must state the core intuition in simple, memorable student language (e.g. *"Extraire un carré, c'est trouver la racine d'un facteur parfait"*).

---

## 4. Co-located Visual Feedback (Split-Attention Reduction)
- **Directive**: Explanations, visual graphics, and interactive controls MUST be physically co-located in the same visual container.
- **Enforcement**: Students must never be required to scroll across sections or switch tabs to correlate an input control with its visual feedback canvas. One Visual Container = One Cognitive Step.

---

## 5. Diagnostic Misconception Repair
- **Directive**: Mistakes MUST be treated as essential learning opportunities, accompanied by specific diagnostic explanations explaining *why* the error occurred.
- **Enforcement**: Stage 4 (`misconception_repair`) MUST explicitly showcase common student traps (e.g. $\sqrt{a+b} \neq \sqrt{a} + \sqrt{b}$) and provide student error analysis to dismantle deep-seated misconceptions.

---

## 6. Non-Blocking Exercise Progression
- **Directive**: Student errors MUST NEVER block stage advancement or lock the student in a stuck state.
- **Enforcement**: The attempt itself satisfies the unlock condition. Correct answers unlock the next stage with positive feedback and XP rewards; incorrect answers provide diagnostic feedback, log the question into the Error Notebook, permit retries, AND present an immediate Continue action button (`➡ Continuer vers : Étape X`) so learning momentum is never stopped.

---

## 7. Mastery Verification & Metacognitive Reflection
- **Directive**: Every lesson MUST verify autonomous mastery and prompt metacognitive self-teaching.
- **Enforcement**:
  - **Mastery**: Stage 5 (`mastery`) must test autonomous application across scaffolded exercises.
  - **Feynman Reflection**: Stage 6 (`reflection`) must include an open prompt (*"Explain this rule in your own words as if teaching a classmate"*), followed by a structured Model Explanation and self-evaluation checklist.

---

## 8. Chrono Exam Simulation & Speed Readiness
- **Directive**: Every lesson MUST conclude with a timed exam simulation (`exam_test`) powered by `exam_engine` to build exam readiness, time management, and precision under real Brevet conditions.
- **Enforcement**: Stage 7 (`exam_test`) MUST include an interactive countdown timer, question progress bar, Brevet-standard exam questions, and a final performance & speed score report.
