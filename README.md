# Excellens Prompt System

The **Excellens AI Generation Framework Prompt System** is a multi-agent AI pipeline designed to generate standalone, production-ready, interactive educational web application lessons.

## Framework Architecture

The framework orchestrates an end-to-end multi-stage pipeline:

```
00_system.md (Orchestration & Validation)
      │
      ├──> 01_lesson_designer.md (Pedagogical Spec -> lesson_spec.json)
      │
      ├──> 02_html_generator.md (HTML/CSS/JS Application -> lesson.html)
      │
      └──> 03_reviewer.md (Quality Audit & Precision Remediation -> final_lesson.html)
```

## Directory Structure

```
.
├── prompts/
│   ├── 00_system.md             # System Orchestrator & Gatekeeper
│   ├── 01_lesson_designer.md    # Pedagogical & Cognitive Architect
│   ├── 02_html_generator.md     # Frontend Application & Experience Architect
│   └── 03_reviewer.md           # Quality Assurance & Production Auditor
│
└── specifications/
    ├── accessibility_rules.md   # WCAG 2.1 AA accessibility guidelines
    ├── animation_rules.md       # Motion, transitions & performance budget
    ├── coding_rules.md          # Architecture, state persistence & HTML standards
    ├── curriculum_rules.md      # Pedagogical progression & standards
    ├── decision_principles.md   # UX & cognitive friction rules
    ├── design_system.md         # Visual tokens, typography & CSS rules
    ├── excellens_style_guide.md # Educational tone & content standards
    └── output_schema.md         # JSON schemas for inter-stage data exchange
```

## Core Behavioral Features

- **Strict LaTeX Math Rendering**: Mandatory KaTeX compilation formatting ensuring zero raw LaTeX text renders in browser output.
- **HTML Formatting**: Automatic conversion of markdown text emphasis markers (`**text**` ➔ `<strong>text</strong>`) into clean HTML elements.
- **Visual Progress Sidebar**: Explicit visual state styling for locked (`🔒` amber/yellow) vs unlocked (`🔓` green) stage icons.
- **Dynamic Scroll Observer**: Navigation `.active` class dynamically tracks viewport section scrolling (`IntersectionObserver`).
- **Non-Blocking Learning Progression**: Exercise attempts provide immediate diagnostic feedback and unlock downstream stages regardless of answer correctness (`student_attempted ➔ unlock_next_stage()`).
