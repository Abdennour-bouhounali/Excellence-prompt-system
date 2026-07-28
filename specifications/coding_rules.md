# Excellens Coding & Software Architecture Rules (`coding_rules.md`)

This specification defines the frontend architecture, JavaScript state management (`excellens_progress_v1`), DOM performance rules, and HTML/CSS coding standards for Excellens web applications.

---

## 1. Single-File Zero-Dependency Architecture

1. **Standalone Distribution**: Each lesson is compiled into a single `.html` file containing HTML structure, embedded `<style>` block, and modular `<script>` block.
2. **External CDN Resources**: The only allowed external CDNs are KaTeX stylesheets and scripts for mathematical rendering:
   ```html
   <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css" crossorigin="anonymous">
   <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js" crossorigin="anonymous"></script>
   <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" crossorigin="anonymous"></script>
   ```
3. **Zero Third-Party UI Frameworks**: Do not rely on React, Vue, Tailwind, or Bootstrap. All layout and interactions must use Vanilla JS and CSS Custom Properties.

---

## 2. JavaScript State Engine & Storage Architecture (`excellens_progress_v1`)

1. **Encapsulated Scope**: Wrap all application logic in an Immediately Invoked Function Expression (IIFE) to avoid global namespace pollution:
   ```javascript
   (() => {
     'use strict';
     // Application state & logic
   })();
   ```

2. **SaaS Platform State Management**:
   - Maintain state under key `excellens_progress_v1`:
     ```javascript
     const STORAGE_KEY = 'excellens_progress_v1';
     let state = {
       platform: 'v1',
       lessonId: 'simplifier-racines-carrees',
       completedStages: [],
       unlockedStages: [0],
       xp: 0,
       streak: 0,
       errorNotebook: []
     };
     ```
   - Wrap `localStorage` read/write calls in `try...catch` blocks to prevent crashes in restricted browsing contexts.

3. **Dynamic SVG Rendering**:
   - Interactive graphics must be rendered dynamically using `document.createElementNS('http://www.w3.org/2000/svg', tag)`.

4. **KaTeX Compilation Helper & Dynamic LaTeX Rendering**:
   - Provide a safe `renderAllMath(element = document.body)` helper function:
     ```javascript
     function renderAllMath(element = document.body) {
       if (window.renderMathInElement) {
         renderMathInElement(element, {
           delimiters: [
             { left: '$$', right: '$$', display: true },
             { left: '$', right: '$', display: false }
           ],
           throwOnError: false
         });
       }
     }
     ```
   - Trigger `renderAllMath(document.body)` on `DOMContentLoaded` and after any dynamic DOM modification.

5. **Dynamic Sidebar Active, 3-State Icon & Lock Progression**:
   - Use `IntersectionObserver` to dynamically toggle `.active` ONLY on the navigation item matching the section visible in the viewport.
   - Maintain 3 step states:
     - `.nav-item.locked .status-icon`: Displays `🔒` (`color: var(--amber-warning)`).
     - `.nav-item.active .status-icon`: Displays `▶` and highlight border.
     - `.nav-item.completed .status-icon`: Displays `✅` (`color: var(--emerald-positive)`).

6. **Non-Blocking Progression**:
   - **Case A (Correct Answer)**: Auto-mark completed (icon -> green ✅), unlock next stage, smooth scroll (`nextElement.scrollIntoView({ behavior: 'smooth' })`).
   - **Case B (Incorrect Answer)**: Display corrective feedback AND immediately reveal Continue button (`➡ Continuer vers : Étape X`). Clicking unlocks next stage, smooth scrolls, and updates sidebar active state.
   - **Case C (Informational Step)**: Render bottom navigation button (`➡ Continuer vers : Étape suivante`).

---

## 3. CSS & HTML Architecture Standards

1. **Box Model Reset**: Apply `* { box-sizing: border-box; }` universally.
2. **CSS Variables First**: Every color, font, border radius, spacing unit, and shadow MUST use defined `--var` custom properties.
3. **Semantic HTML (Zero Raw Markdown)**: Raw Markdown syntax (`**bold**`, `*italic*`) MUST NEVER exist in output HTML or JS template strings. Convert emphasis to `<strong>`, `<em>`.
4. **Locked Section Overlay**: Enforce `.lab-section.locked` with:
   ```css
   .lab-section.locked {
     position: relative;
     opacity: 0.55;
     pointer-events: none;
     filter: blur(1px);
   }
   .lab-section.locked::after {
     content: "🔒 Complète l'étape précédente pour débloquer cette section";
     position: absolute;
     inset: 0;
     display: grid;
     place-items: center;
     background: rgba(15, 23, 42, 0.45);
     backdrop-filter: blur(4px);
     border-radius: var(--radius-lg);
     color: white;
     font-weight: 800;
     font-size: 1.1rem;
     text-align: center;
     padding: 20px;
     z-index: 10;
   }
   ```
5. **Bounded Sidebar Container**:
   - Sidebar MUST enforce viewport-constrained max height and internal vertical scrolling (`position: sticky; top: 84px; max-height: calc(100vh - 104px); overflow-y: auto; overscroll-behavior: contain; scroll-behavior: smooth;`).

---

## 4. Performance & Reliability Budgets

- **Execution Budget**: Initial script parsing and DOM rendering must complete in `< 50ms`.
- **Memory Safety**: Clean up dynamic timers (`setInterval`) when tests or exam timers complete.
- **Offline Self-Containment**: Application core must function fully offline once KaTeX assets are cached.
