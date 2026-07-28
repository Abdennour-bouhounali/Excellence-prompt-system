# Excellens Coding & Software Architecture Rules (`coding_rules.md`)

This specification defines the frontend architecture, JavaScript state management, DOM performance rules, and HTML/CSS coding standards for Excellens web applications.

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

## 2. JavaScript State Engine & Storage Architecture

1. **Encapsulated Scope**: Wrap all application logic in an Immediately Invoked Function Expression (IIFE) to avoid global namespace pollution:
   ```javascript
   (() => {
     'use strict';
     // Application state & logic
   })();
   ```

2. **State Management Protocol**:
   - Maintain a single reactive `state` object holding `unlockedStages` (initially `[0]`), `completedStages`, XP, streak counters, error log entries, and exam state.
   - Persist state to `localStorage` under a unique key (`excellens_[topic_slug]_state`).
   - Wrap `localStorage` calls in `try...catch` blocks to prevent crashes in restricted browsing contexts.

3. **Dynamic SVG Rendering**:
   - Interactive graphics must be rendered dynamically using `document.createElementNS('http://www.w3.org/2000/svg', tag)`.
   - Update graphics responsively based on viewport bounds and scale coordinates mathematically.

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
   - **Timing & Execution Lifecycle**: Never use `onload` on `<script defer src=".../auto-render.min.js">` tag. Always invoke `renderAllMath(document.body)` inside `DOMContentLoaded`.

5. **Dynamic Sidebar Active, 3-State Icon & Lock Progression Management**:
   - **IntersectionObserver Active Tracking**: Use an `IntersectionObserver` to monitor `.lab-section` visibility. Dynamically assign `.active` ONLY to the navigation item matching the currently visible section in the viewport.
   - **3-State Sidebar Progression**: Maintain explicit CSS and JS rendering for 3 step states:
     - `.nav-item.locked .status-icon`: Displays `🔒` with amber styling (`color: var(--amber-warning)`).
     - `.nav-item.active .status-icon`: Displays `▶` with primary accent highlight border (`border-left: 3px solid var(--violet-accent)`).
     - `.nav-item.completed .status-icon`: Displays `✅` with green styling (`color: var(--emerald-positive)`). Once a step is completed, its sidebar icon stays green permanently.

6. **Automatic Unlocking & Non-Blocking Progression Protocol**:
   - **Case A (Evaluated - Correct Answer)**: Automatically mark current step completed (`completedStages.push(curr)`), icon -> green `✅`, unlock next stage (`unlockedStages.push(next)`), update UI, perform smooth scroll (`nextElement.scrollIntoView({ behavior: 'smooth' })`), and activate next step. No extra click required.
   - **Case B (Evaluated - Incorrect Answer)**: Display corrective feedback AND immediately reveal a Continue button (`➡ Continuer vers : Étape X — [Title]`). Clicking unlocks next stage, smooth scrolls, and updates sidebar active state. Student is never blocked.
   - **Case C (Informational Step)**: Render a navigation button at bottom (`➡ Continuer vers : Étape suivante — [Title]`). Clicking marks current step completed (icon -> ✅), unlocks next stage, smooth scrolls, and updates sidebar active state.

---

## 3. CSS & HTML Architecture Standards

1. **Box Model Reset**: Apply `* { box-sizing: border-box; }` universally.
2. **CSS Variables First**: Every color, font, border radius, spacing unit, and shadow MUST use defined `--var` custom properties.
3. **Semantic HTML (No Raw Markdown)**: Raw Markdown syntax (`**bold**`, `*italic*`, `_text_`) MUST NEVER exist in the generated HTML source or JS innerHTML templates. Convert all emphasis into semantic HTML tags (`<strong>`, `<em>`).
4. **Smooth Theme Transitions**: Include `transition: background-color 0.3s ease, color 0.3s ease;` on core layout elements.
5. **Locked Section Overlay**: Implement `.lab-section.locked` with:
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
6. **Bounded Sidebar Container**:
   - The navigation sidebar MUST enforce viewport-constrained max height and internal vertical scrolling (`position: sticky; top: 84px; max-height: calc(100vh - 104px); overflow-y: auto; overscroll-behavior: contain; scroll-behavior: smooth;`).

---

## 4. Performance & Reliability Budgets

- **Execution Budget**: Initial script parsing and DOM rendering must complete in `< 50ms`.
- **Memory Safety**: Clean up dynamic timers (`setInterval`) when tests or exam timers complete.
- **Offline Self-Containment**: Application core must function fully offline once KaTeX assets are cached.
