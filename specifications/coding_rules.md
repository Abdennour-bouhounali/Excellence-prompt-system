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
   - Maintain a single reactive `state` object holding XP, streak counters, unlocked stages, completed exercise IDs, error log entries, and exam state.
   - Persist state to `localStorage` under a unique key (`excellens_[topic_slug]_state`).
   - Wrap `localStorage` calls in `try...catch` blocks to prevent crashes in restricted browsing contexts.

3. **Dynamic SVG Rendering**:
   - Interactive graphics must be rendered dynamically using `document.createElementNS('http://www.w3.org/2000/svg', tag)`.
   - Update graphics responsively based on viewport bounds and scale coordinates mathematically.

4. **KaTeX Compilation Helper**:
   - Provide a safe `renderMath(container)` helper function that checks for `renderMathInElement` readiness before triggering math parsing.

---

## 3. CSS Architecture Standards

1. **Box Model Reset**: Apply `* { box-sizing: border-box; }` universally.
2. **CSS Variables First**: Every color, font, border radius, spacing unit, and shadow MUST use defined `--var` custom properties.
3. **Smooth Theme Transitions**: Include `transition: background-color 0.3s ease, color 0.3s ease;` on core layout elements.
4. **Scaffolded Locking**: Implement `.lab-section.locked` with `opacity: 0.55; pointer-events: none; filter: blur(1px);` and a pseudo-element `::after` lock message overlay.
5. **Bounded Sidebar Container**: The navigation sidebar MUST enforce viewport-constrained max height and internal vertical scrolling (`position: sticky; top: 84px; max-height: calc(100vh - 104px); overflow-y: auto; overscroll-behavior: contain; scroll-behavior: smooth;`). The sidebar MUST NEVER expand infinitely or displace page layout when lessons feature 20+ sections.

---

## 4. Performance & Reliability Budgets

- **Execution Budget**: Initial script parsing and DOM rendering must complete in `< 50ms`.
- **Memory Safety**: Clean up dynamic timers (`setInterval`) when tests or exam timers complete.
- **Offline Self-Containment**: Application core must function fully offline once KaTeX assets are cached.
