# Frosted surfaces: progressive CSS fallback and QA

Read when: introducing actual glassmorphism, protecting contrast above imagery or testing translucency fallbacks and performance.

## Start opaque, enhance locally
```css
.glass-panel {
  color: var(--panel-foreground);
  background-color: var(--panel-solid, #ffffff);
  border: 1px solid var(--panel-border, #56616c);
}
@supports (backdrop-filter: blur(12px)) {
  .glass-panel {
    background-color: var(--panel-translucent, rgb(255 255 255 / .88));
    backdrop-filter: blur(12px);
  }
}
@media (prefers-reduced-transparency: reduce) {
  .glass-panel {
    background-color: var(--panel-solid, #ffffff);
    backdrop-filter: none;
  }
}
@media (forced-colors: active) {
  .glass-panel {
    color: CanvasText;
    background-color: Canvas;
    border-color: CanvasText;
    backdrop-filter: none;
  }
}
```
`--panel-foreground`, colors and opacities must be audited against *real* imagery in each theme; this snippet is not brand-ready nor proof of WCAG compliance. The reduced-transparency feature is **not universally supported**, so the opaque fallback and user-friendly component design remain mandatory.

## Safety and performance
Avoid nested full-screen blurs, giant fixed compositing layers and text that depends on fluctuating video/background brightness. Keep `outline` visible above scrims. If blur performance is disputed, measure animation FPS and compositing rather than assuming a universal limit. Never blur essential informational imagery or introduce translucent overlays that intercept clicks without purpose.

## Verify
Capture over dark, light, saturated photo and changing video frames when applicable; with blur unavailable, forced-colors, reduced transparency, 200% zoom, modal opened, focus visible and disabled/error states. Treat `prefers-reduced-motion` separately if transitions are used; glass opacity should not imply animation.

Official: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/prefers-reduced-transparency and https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/%40media/forced-colors
