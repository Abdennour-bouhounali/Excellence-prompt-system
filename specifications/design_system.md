# Excellens Design System (`design_system.md`)

This specification defines the visual primitives, CSS custom property tokens, responsive layout rules, theme systems, and component patterns of the **Excellens Design System**.

---

## 1. Design Tokens & Color Architecture

All styling must be driven by CSS Custom Properties attached to `:root` and overridden under `[data-theme="dark"]`.

```css
:root {
  /* Brand & Base Palette */
  --bg-base: #f8fafc;
  --bg-surface: #ffffff;
  --bg-surface-elevated: #ffffff;
  --bg-alt: #f1f5f9;
  --border-color: #cbd5e1;
  --text-main: #0f172a;
  --text-muted: #475569;
  
  --navy-primary: #0f172a;
  --navy-accent: #1e293b;
  
  /* Semantic State Colors */
  --emerald-positive: #10b981;
  --emerald-dark: #047857;
  --emerald-bg: #ecfdf5;
  --emerald-border: #a7f3d0;
  
  --coral-negative: #f43f5e;
  --coral-dark: #be123c;
  --coral-bg: #fff1f2;
  --coral-border: #fecdd3;
  
  --violet-accent: #6d28d9;
  --violet-soft: #7c3aed;
  --violet-bg: #f5f3ff;
  --violet-border: #ddd6fe;
  
  --amber-warning: #d97706;
  --amber-bg: #fffbeb;
  --amber-border: #fef3c7;
  
  /* Surface Geometry & Shadows */
  --radius-sm: 10px;
  --radius-md: 16px;
  --radius-lg: 24px;
  
  --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 10px 30px rgba(15, 23, 42, 0.08);
  --shadow-lg: 0 20px 40px rgba(15, 23, 42, 0.12);
  
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
  --max-width: 1160px;
}

[data-theme="dark"] {
  --bg-base: #090d16;
  --bg-surface: #111827;
  --bg-surface-elevated: #1f2937;
  --bg-alt: #1a2332;
  --border-color: #334155;
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  
  --navy-primary: #f8fafc;
  --navy-accent: #e2e8f0;
  
  --emerald-bg: rgba(16, 185, 129, 0.15);
  --emerald-border: rgba(16, 185, 129, 0.4);
  
  --coral-bg: rgba(244, 63, 94, 0.15);
  --coral-border: rgba(244, 63, 94, 0.4);
  
  --violet-bg: rgba(124, 58, 237, 0.2);
  --violet-border: rgba(139, 92, 246, 0.4);
  
  --amber-bg: rgba(245, 158, 11, 0.18);
  --amber-border: rgba(245, 158, 11, 0.4);
  
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 10px 30px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 20px 40px rgba(0, 0, 0, 0.5);
}
```

---

## 2. Typography & Responsive Hierarchy

- **Title 1 (`h1`)**: `clamp(2rem, 3.8vw, 3.2rem)`, `font-weight: 900`, `letter-spacing: -0.04em`.
- **Section Heading (`h2`)**: `clamp(1.5rem, 2.8vw, 2.2rem)`, `font-weight: 900`, `letter-spacing: -0.03em`.
- **Sub-heading (`h3`/`h4`)**: `1.1rem`–`1.3rem`, `font-weight: 800`.
- **Body Text**: `1rem`–`1.15rem`, `line-height: 1.65`.
- **Math Delimiters**: LaTeX formulas are rendered using KaTeX (`$x$` inline, `$$x$$` display block).

---

## 3. Layout Architecture

- **Sticky Topbar Header**: `position: sticky; top: 0; z-index: 100`, glassmorphic backdrop filter (`backdrop-filter: blur(16px)`). Holds brand logo, streak badge, XP display, lesson progress bar, theme toggle.
- **Hero Header**: High-impact header section containing breadcrumbs, kicker tag, main title, overview metadata, and initial challenge card.
- **Two-Column Main Layout**:
  - `sidebar`: `position: sticky; top: 84px`, 260px fixed width, bounded height (`max-height: calc(100vh - 104px)`), internal vertical scroll area (`overflow-y: auto; overscroll-behavior: contain; scroll-behavior: smooth;`), rendering section navigation links with status icons (`🔓`/`🔒`). The sidebar must never expand infinitely or push page layout.
  - `sidebar active tracking`: Uses `IntersectionObserver` (or scroll position tracking) to dynamically attach `.active` ONLY to the navigation item corresponding to the section currently visible in the viewport. When the student scrolls away from Stage 0 (`#stage-0`), `.active` MUST be removed from Stage 0 and assigned to the active section. Permanent highlighting of Stage 0 is strictly forbidden.
  - `main`: Fluid flexible column (`minmax(0, 1fr)`) containing sequential `.lab-section` modules.

---

## 4. UI Component Primitives

1. **`.sidebar` & `.sidebar-nav`**: Navigation container with sticky positioning (`top: 84px`), fixed width (`260px`), viewport-constrained max height (`max-height: calc(100vh - 104px)`), and internal vertical scrolling (`overflow-y: auto; scroll-behavior: smooth`).
   - **3-State Sidebar Icons & Progression**:
     - `.nav-item.locked .status-icon`: Displays `🔒` with yellow/amber styling (`color: var(--amber-warning)`), indicating the stage is unavailable and non-interactive.
     - `.nav-item.active .status-icon`: Displays `▶` with primary accent highlight border (`border-left: 3px solid var(--violet-accent)`), indicating the student is currently working on this step.
     - `.nav-item.completed .status-icon`: Displays `✅` with vibrant green styling (`color: var(--emerald-positive)`), indicating the step has been completed. This icon remains green permanently.
2. **`.lab-section` & Locked Section Overlay**: Main content section container. When locked (`.lab-section.locked`), it enforces:
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
3. **`.discovery-panel`**: Interactive experimentation container housing dynamic equation displays, range sliders, and prediction action controls.
4. **`.quiz-card` & `.exercise-card`**: Input/QCM option card containers featuring feedback boxes (`.feedback-box.good`, `.feedback-box.bad`, `.feedback-box.info`) and instant non-blocking Continue action buttons for wrong answers/informational steps.
5. **`.worked-example`**: Multi-step solution card featuring numbered counter steps (`.steps li::before`).
6. **`.callout`**: Emphasized alert container with colored left-border accent (`.callout.success`, `.callout.warning`, `.callout.danger`).
7. **`.mastery-report-card`**: Synthesis completion card featuring badge icon, score metrics grid, and recommendation highlights.
8. **`.revision-card`**: Flash-revision card container.
9. **`.exam-header-bar`**: Dark header bar displaying live exam countdown timer, question progression, and action controls.
10. **`.math-input-group` (Student-Friendly Mathematical Input Components)**: Atomic input component layout where mathematical notation ($\sqrt{\phantom{x}}$, fraction bars, superscripts) is rendered visually by the UI.
    - **Accessibility Attributes**: Every input field MUST feature explicit, descriptive accessibility tags (`aria-label="..."`, e.g. `aria-label="Coefficient extérieur"`, `aria-label="Nombre sous la racine"`, `aria-label="Numérateur"`).
    - **Mobile Keypad Optimization**: All numeric fields MUST include `inputmode="numeric"` and `pattern="[0-9]*"` to automatically trigger mobile numeric keypads on iOS and Android devices.
    - **Touch Targets & Focus**: Minimum touch target height ≥ 44px, inline width matched to expected value length (`min-width: 44px`, `text-align: center`), with high-contrast `:focus-visible` ring.

---

## 5. Responsive Breakpoints

- **Desktop (default)**: 2-column grid (`260px` sidebar + `1fr` main content).
- **Tablet (`@media (max-width: 900px)`)**: Sidebar hides; main content expands to 100% full width.
- **Mobile (`@media (max-width: 640px)`)**: Options grid stacks vertically (`grid-template-columns: 1fr`), inputs stack, topbar hides text-heavy progress elements to prevent overflow.
- **Print (`@media print`)**: Navigation, buttons, confetti, theme toggles hide; layout converts to standard black/white printable document.
