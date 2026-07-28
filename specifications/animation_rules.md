# Excellens Animation & Motion Rules (`animation_rules.md`)

This specification defines the motion design philosophy, animation keyframes, timing budgets, and reduced motion fallbacks for all Excellens interactive applications.

---

## 1. Educational Motion Philosophy

1. **Cognitive Focus Only**: Animation must serve an educational purpose (visualizing vector direction, drawing path trajectories, reinforcing milestone completion).
2. **Zero Distraction**: Non-functional decorative loops or bouncing animations that draw focus away from learning material are strictly forbidden.
3. **Short Duration Budget**: Micro-interactions must complete in **200ms – 400ms**. Complex path drawings must complete in **< 600ms**.

---

## 2. Easing & Timing Specifications

- **Standard Micro-interaction**: `transition: all 0.2s ease;` (Hover effects, tab switches, focus rings).
- **Smooth Layout Transition**: `transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);` (Progress bar fills).
- **SVG Arc / Path Draw**: `animation: drawPath 600ms ease forwards;`.
- **Result Node Pop**: `animation: popDot 400ms ease 500ms both;`.

---

## 3. Standard Keyframe Definitions

```css
/* SVG Vector Path Draw */
.svg-path-draw {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: drawPath 600ms ease forwards;
}

@keyframes drawPath {
  to { stroke-dashoffset: 0; }
}

/* Result Node Pop */
.svg-result-dot {
  transform-box: fill-box;
  transform-origin: center;
  animation: popDot 400ms ease 500ms both;
}

@keyframes popDot {
  0% { opacity: 0; transform: scale(0.5); }
  70% { opacity: 1; transform: scale(1.2); }
  100% { opacity: 1; transform: scale(1); }
}

/* Dynamic Fade In */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}
```

---

## 4. Particle Confetti Engine Specifications

- Triggered upon completing major milestones (Mastery test submission, Exam completion).
- Implemented via a fixed overlay `<canvas id="confettiCanvas">` with `pointer-events: none; z-index: 999`.
- Renders ~90 particles using brand colors (`--emerald-positive`, `--violet-soft`, `--coral-negative`, `--amber-warning`).
- Cancels animation loop gracefully when particles fall beyond viewport.
