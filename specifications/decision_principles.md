# Excellens Meta-Decision Principles (`decision_principles.md`)

This document is the foundational reasoning engine of the **Excellens Lesson Generation Intelligence Framework**. It defines the meta-level cognitive, pedagogical, design, and engineering rules that guide expert AI agents in synthesizing world-class educational web applications.

---

## 1. The Anti-Hardcoding Meta-Rule

Every decision made by the framework must derive from first-principles educational reasoning, never from static template matching.

> **RULE**: Never encode a visual or technical pattern from the reference implementation as a universal directive.
>
> For every pattern encountered, the AI must evaluate:
> 1. **Context & Constraint**: What learning obstacle or cognitive friction is the student facing?
> 2. **Options Considered**: What candidate representations or UI mechanisms can resolve this friction?
> 3. **Evaluation**: Which option minimizes extraneous cognitive load while maximizing intuitive clarity?
> 4. **Conditional Decision**: Implement the selected pattern *only* for the duration and scope required to satisfy the learning objective.

---

## 2. Meta-Reasoning Engine: `Constraints → Options → Evaluation → Decision`

All framework prompts and agents must process decisions through the following four-step reasoning algorithm:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ 1. IDENTIFY CONSTRAINTS                                                 │
│    • Subject domain & target age/grade level                            │
│    • Common misconceptions and abstract friction points                 │
│    • Accessibility & device/screen constraints                          │
├─────────────────────────────────────────────────────────────────────────┤
│ 2. ENUMERATE OPTIONS                                                    │
│    • Candidate mental models (spatial, visual, symbolic, analogy)       │
│    • Candidate UI layout patterns (linear, tabbed, interactive canvas)  │
│    • Candidate interaction types (predict-slider, quiz, open input)     │
├─────────────────────────────────────────────────────────────────────────┤
│ 3. EVALUATE COGNITIVE IMPACT                                            │
│    • Extraneous Load: Does this option add visual or cognitive noise?   │
│    • Germane Load: Does this option help build correct schema?          │
│    • Accessibility: Can every student navigate and perceive this?       │
├─────────────────────────────────────────────────────────────────────────┤
│ 4. EMIT CONDITIONAL DECISION                                            │
│    • Select optimal pattern + document rationale                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Cognitive Load Minimization Principles

1. **One Cognitive Objective per Visual Container**:
   - Each visual card or module must focus on a single conceptual step.
   - Do not mix conceptual discovery with complex formal calculation in the same visual space.

2. **Predict-First Active Discovery**:
   - Students must be prompted to form a mental prediction *before* revealing calculated outcomes or formal formulas.
   - Prediction triggers active schema activation and highlights cognitive misalignment.

3. **Dual-Coding Representation Matching**:
   - Match the abstract concept to the spatial or physical model that best preserves its relational properties:
     - **Signed values / Relative magnitudes**: 1D/2D Spatial Continua (Number Lines, Gauges, Thermometers, Elevators).
     - **Structures / Networks**: Hierarchical Trees, Graphs, Molecular diagrams.
     - **Processes / Algorithms**: Dynamic State Machines, Step Sequences, Timelines.
     - **Transformations / Functions**: Interactive Input/Output Machines, Sliders, Function Graphs.

4. **Split-Attention Reduction**:
   - Explanations, graphics, and interactive controls must be co-located.
   - Never require a student to scroll up and down or switch context to correlate a control with its graphical feedback.

---

## 4. Subject Generalization Matrix

The framework reasoning applies universally across disciplines:

| Subject | Core Friction Point | Mental Model Selection | Interactive Engine Pattern |
|---|---|---|---|
| **Mathematics** | Abstract operations & negative/fractional quantities | Spatial continua, vector arrows, area models | Dynamic SVG coordinate canvas, slider predictors |
| **Physics** | Forces, vectors, field interactions, kinematics | Free-body diagrams, trajectory arcs, velocity vectors | Interactive vector simulator, parameter sliders |
| **Chemistry** | Microscopic reactions & stoichiometry | Molecular structures, balancing balances, electron shells | Atom/molecule builder, balance slider engine |
| **Biology** | Complex multi-stage processes & cellular structures | Layered diagrams, sequence flowcharts, zoomable cells | Interactive step-through timeline, toggle layers |
| **Computer Science**| Memory representation, algorithms, recursion | Call stack visualizers, array index pointers, state trees | Step-by-step code execution trace engine |
| **Languages** | Grammar syntax, verb conjugation, vocabulary retention | Sentence diagramming trees, contextual flashcards | Drag-and-drop syntax builders, cloze tests |
| **History** | Chronology, causal networks, multi-perspective events | Parallel timelines, geographical map overlays | Interactive timeline scrubber, cause-effect cards |

---

## 5. Gamification & Self-Determination Theory (SDT)

Gamification must serve psychological learning needs (Competence, Autonomy, Relatedness) and never act as manipulative distraction:

1. **Competence Reinforcement**:
   - Award XP and progress indicators immediately upon verified cognitive milestone completion.
   - Display real-time streaks for consecutive accurate responses.

2. **Autonomy & Agency**:
   - Progression locking must feel logical (unlocking subsequent stages upon completing prerequisite steps).
   - Students must always be able to revisit unlocked stages to review or rebuild confidence.

3. **Metacognition & Diagnostic Mastery**:
   - Mistakes are never penalized with negative XP; they are captured into a personalized **Error Notebook** with targeted conceptual hints.
   - High-level mastery is verified via student-led explanation (**Feynman Technique**) and timed self-evaluation.
