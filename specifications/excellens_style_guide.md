# Excellens Style Guide (`excellens_style_guide.md`)

This specification defines the voice, tone, linguistic rules, mathematical formatting, and naming conventions for all content produced within the Excellens platform.

---

## 1. Educational Voice & Tone

1. **Student-Centric & Empowering**:
   - Address the student directly using encouraging, respectful French (*tutoiement*: "tu", "ton", "tes").
   - Frame mistakes as essential discovery opportunities, not failures ("Attention : réessaie en visualisant le sens").
   - Use action-oriented verbs ("Expérimente", "Prédis", "Observe", "Valide").

2. **Rigorous yet Intuitive**:
   - Never sacrifice scientific or mathematical accuracy for simplicity.
   - Explain the *why* behind every rule before introducing formal definitions or algorithms.
   - Maintain high academic standards aligned with French national curriculum benchmarks (*Programme officiel du Collège et du Lycée*).

---

## 2. French Pedagogical Terminology Standards

- **Lesson Level Tags**: *5e, 4e, 3e, Seconde, Préparation Brevet*.
- **Section Kicker**: *🔬 Laboratoire de Mathématiques / Physique / Science*.
- **Action Buttons**: *Relever le défi ➔*, *Vérifier*, *J'ai compris, étape suivante ➔*, *Valider mon explication (+30 XP) ➔*, *Lancer l'Examen Chronométré ⏱️*.
- **Gamification Badges**: *Série de bonnes réponses (🔥)*, *Points d'expérience (✨ XP)*, *Défi Initial*, *Carnet d'Erreurs*.

---

## 3. Mathematical & Scientific Expression Conventions

1. **LaTeX Notation**:
   - Inline math expressions must be enclosed in single dollar signs: `$x = -5$`.
   - Display equations must be enclosed in double dollar signs: `$$A = \frac{-b \pm \sqrt{\Delta}}{2a}$$`.
   - Always use proper LaTeX symbols for operators ($\times$ via `\times`, $\div$ via `\div`, $\circ\text{C}$ via `^\circ\text{C}`).

2. **Number Formatting**:
   - Use standard French decimal notation (comma or space for thousands: `$3\text{ }500$`).
   - Clearly delineate positive and negative signs when building signed intuition ($+5$, $-7$).

---

## 4. Code & Variable Naming Conventions

- **HTML Element IDs**: camelCase or kebab-case adhering to component roles (`#themeToggle`, `#progressFill`, `#xpDisplay`, `#stage1`, `#errorNotebookContainer`).
- **CSS Custom Properties**: kebab-case prefixed with semantic domain (`--bg-base`, `--violet-soft`, `--emerald-positive`).
- **JS LocalStorage Keys**: Prefix all keys with `excellens_` to prevent domain collisions (`excellens_lesson_state`, `excellens_theme`).
