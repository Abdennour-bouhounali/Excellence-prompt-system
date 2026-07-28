# Excellens Agent Contracts Specification (`agent_contracts.md`)

This document is the **System Constitution** of the Excellens AI Educational Content Compiler. It defines the formal interfaces, input requirements, output artifacts, exclusive decision ownership, and strict negative boundaries (`MUST NOT`) for every specialist agent in the compilation pipeline.

---

## 1. Global Contract Protocol

All pipeline agents MUST adhere to the following universal rules:

1. **Artifact Versioning Header**: Every JSON artifact emitted MUST include top-level metadata:
   ```json
   {
     "meta": {
       "artifactVersion": "1.0",
       "pipelineVersion": "2026.07",
       "agentName": "agent_identifier",
       "agentVersion": "1.0",
       "generatedAt": "ISO-8601 Timestamp"
     }
   }
   ```
2. **Strict Non-Interference**: An agent MUST NOT make decisions outside its explicit contract domain. If required information is missing, the agent MUST flag a missing requirement attribute rather than inventing ad-hoc choices belonging to downstream or upstream agents.
3. **Schema Compliance**: Every emitted intermediate artifact MUST validate 100% against its corresponding schema in `specifications/output_schema.md`.

---

## 2. Agent 00: Compiler Orchestrator (`00_system.md`)

- **Role**: Pipeline Controller & Repair Loop Manager
- **Inputs**: User Request Payload (`subject`, `targetGrade`, `topicTitle`, `coreConceptDescription`, `targetLearningGoals`), Specifications Corpus.
- **Outputs**: Compilation Logs, Pipeline Execution Context.
- **Allowed Decisions**:
  - Sequential agent delegation order (`01` ➔ `02` ➔ `03` ➔ `04` ➔ `05`).
  - Pipeline termination and delivery of `final_lesson.html`.
  - Targeted local repair routing when `05_quality_engineer` flags defects.
  - Repair attempt counter tracking (`repairAttempt: 1..3`) and halting execution with `HUMAN_REVIEW_REQUIRED` after 3 failed retries.
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** generate HTML, CSS, or JavaScript code.
  - **MUST NOT** write or modify lesson text, explanations, or questions directly.
  - **MUST NOT** contain CSS visual style tokens, color hex codes, or backdrop-blur rules inside its prompt instructions.
  - **MUST NOT** bypass intermediate schema validation gates.

---

## 3. Agent 01: Lead Learning Architect (`01_learning_architect.md`)

- **Role**: Educational Intent & Cognitive Barrier Analysis
- **Inputs**: User Request Payload, `decision_principles.md`, `educational_invariants.md`.
- **Outputs**: `knowledge_graph.json`.
- **Allowed Decisions**:
  - Identifying core student schema, prerequisite skills, and baseline readiness checks.
  - Mapping abstract cognitive friction points, intuitive obstacles, and common student misconceptions.
  - Defining target learning objectives and mastery criteria.
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** specify UI layout, cards, color palettes, CSS variables, or visual themes.
  - **MUST NOT** design specific exercise option arrays, QCM choices, or input field HTML templates.
  - **MUST NOT** dictate CSS animations, transition timings, or confetti canvas engines.

---

## 4. Agent 02: Lead Content Architect (`02_content_architect.md`)

- **Role**: Pedagogical Narrative & Exercise Taxonomy Design
- **Inputs**: `knowledge_graph.json`, `curriculum_rules.md`, `excellens_style_guide.md`.
- **Outputs**: `content_spec.json`.
- **Allowed Decisions**:
  - Structuring the 8-stage Core Backbone (`activate_prior`, `discovery`, `formalization`, `guided_practice`, `misconception_repair`, `mastery`, `reflection`, `exam_test`).
  - Formulating narrative explanations, worked example steps, and French pedagogical voice.
  - Designing the 5-tier exercise taxonomy (L1: Recognition, L2: Transformation, L3: Application, L4: Brevet, L5: Transfer).
  - Writing scaffolded hints, detailed corrections, and diagnostic error notebook entries.
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** specify DOM IDs, CSS custom properties, responsive breakpoints, or layout grids.
  - **MUST NOT** define sidebar lock icons, navigation sticky positioning, or viewport max-heights.
  - **MUST NOT** write Vanilla JS event handlers or DOM manipulation code.

---

## 5. Agent 03: Lead Experience Architect (`03_experience_architect.md`)

- **Role**: Mental Model Engine Selection & UX Layout Architecture
- **Inputs**: `content_spec.json`, `design_system.md`, `animation_rules.md`.
- **Outputs**: `experience_spec.json`, `design_decisions.json`.
- **Allowed Decisions**:
  - Selecting spatial, visual, or structural mental models (Spatial Axis, Coordinate Canvas, Atomic Grid, Free-Body Diagram).
  - Choosing modular interaction engines (`visualization_engine`, `algebra_manipulation_engine`, `proof_simulation_engine`, `exam_engine`).
  - Layout component strategy (two-column grid, sticky bounded sidebar, hero header, worked example steps).
  - Documenting explainable design choices in `design_decisions.json`.
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** alter mathematical formulas, lesson explanations, or target question answers defined in `content_spec.json`.
  - **MUST NOT** omit required cognitive accessibility attributes (`aria-label`, `inputmode`).

---

## 6. Agent 04: Senior HTML Generator (`04_html_generator.md`)

- **Role**: Single-File Web Application Compiler & Code Generator
- **Inputs**: `experience_spec.json`, `design_decisions.json`, `coding_rules.md`, `accessibility_rules.md`.
- **Outputs**: `lesson.html`.
- **Allowed Decisions**:
  - Writing single-file semantic HTML5, CSS custom property tokens (`:root` / `[data-theme="dark"]`), and IIFE JavaScript.
  - Implementing `excellens_progress_v1` SaaS state persistence in `localStorage`.
  - Building responsive sticky glass topbar, bounded scrollable sidebar (`max-height: calc(100vh - 104px)`), dynamic `IntersectionObserver` active section tracking, 3-state icons (🔒/▶/✅), and locked overlays.
  - Embedding KaTeX CDN script inclusions and centralized `renderAllMath` compilation helper.
  - Constructing student-friendly componentized atomic math inputs (`.math-input-group`).
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** alter pedagogical sequence, change exercise questions, or modify worked example steps.
  - **MUST NOT** emit raw Markdown formatting markers (`**text**`, `*text*`) inside HTML text nodes.
  - **MUST NOT** require students to type complex mathematical symbols (`√`, `²`, `^`, `\sqrt`, `\frac`).
  - **MUST NOT** introduce external UI frameworks (React, Vue, Tailwind, Bootstrap).

---

## 7. Agent 05: Lead Quality Engineer (`05_quality_engineer.md`)

- **Role**: AI Quality Auditor & Targeted Repair Router
- **Inputs**: `lesson.html`, `design_decisions.json`, Deterministic Validation Logs (`validate_lesson.py`), Specifications Corpus.
- **Outputs**: `quality_report.json`, `final_lesson.html` (if PASS).
- **Allowed Decisions**:
  - Calculating Layer 2 Quality Score across Pedagogy (40%), UX (25%), Technical (20%), and Accessibility (15%).
  - Enforcing Layer 1 Hard Blocker 100% PASS gate (Zero uncompiled LaTeX, zero raw Markdown, zero missing `aria-label` tags).
  - Issuing `PASS` approval status when Layer 1 = 100% and Layer 2 Score ≥ 90 / 100.
  - Issuing `REJECT` status with targeted defect classification and routing repair to the specific responsible agent (HTML Generator, Content Architect, or Learning Architect).
- **Forbidden Decisions (`MUST NOT`)**:
  - **MUST NOT** redesign lesson structure or modify pedagogical scope when performing targeted fixes.
  - **MUST NOT** approve or emit `final_lesson.html` if any Layer 1 Hard Blocker fails or Layer 2 score < 90.
