# Excellens Accessibility Rules (`accessibility_rules.md`)

This specification defines the universal accessibility requirements, WCAG 2.1 AA compliance benchmarks, ARIA usage patterns, keyboard navigation rules, and reduced motion fallbacks for all Excellens lessons.

---

## 1. WCAG 2.1 AA Benchmarks

1. **Color Contrast Ratios**:
   - Primary text against background: Minimum **4.5:1**.
   - Large text (≥ 18pt or 14pt bold) & interactive UI borders: Minimum **3.0:1**.
   - Dark mode variants must preserve high contrast (e.g. text `#f8fafc` on surface `#111827`).

2. **Touch & Click Target Sizes**:
   - All buttons, range sliders, links, QCM options, and exam navigation pills must measure at least **44 × 44 pixels** in touch target area.

3. **Semantic HTML Structure**:
   - Use native semantic tags: `<header>`, `<nav>`, `<main>`, `<aside>`, `<section>`, `<article>`, `<footer>`.
   - Heading hierarchy must be strict and non-skipping (`h1` ➔ `h2` ➔ `h3`/`h4`).

---

## 2. ARIA & Dynamic Screen Reader Announcements

1. **Live Regions**:
   - Interactive feedback containers, slider calculation results, and dynamic error messages must feature `aria-live="polite"` or `role="status"`.
2. **Interactive Graphic Descriptions**:
   - Dynamic SVG canvases must include `role="img"` and a descriptive `aria-label` (e.g. `aria-label="Flèche graduée interactive de repérage"`).
3. **Form & Input Accessibility**:
   - Every input field must have an associated `<label>` or explicit `aria-label`.
   - QCM options and buttons must indicate state using `aria-pressed` or explicit CSS/text feedback.

---

## 3. Keyboard Navigation & Focus Management

1. **Visible Focus Indicator**:
   - Provide an unmistakable focus outline for all interactive elements using `:focus-visible`:
     ```css
     :focus-visible {
       outline: 3px solid var(--violet-soft);
       outline-offset: 3px;
     }
     ```
2. **Logical Tab Order**:
   - Interactive controls follow natural DOM order (topbar ➔ hero ➔ sidebar nav ➔ stage content).
3. **Keyboard Controls for Sliders**:
   - Native `<input type="range">` elements must respond to Arrow keys (`Left`, `Right`, `Up`, `Down`).

---

## 4. Reduced Motion & Sensory Adaptation

Include a mandatory `@media (prefers-reduced-motion: reduce)` block disabling non-essential animations:

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
