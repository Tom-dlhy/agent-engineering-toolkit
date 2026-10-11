---
name: glassmorphism
domain: design
version: "0.1.0"
description: >-
  Use when a product explicitly calls for glassmorphism, frosted surfaces or layered translucent UI. Do not use by default on forms, dense data tables or low-contrast accessibility-sensitive screens.
---

# glassmorphism

## Composition
Use glass as a targeted foreground surface over a carefully chosen background, not as a blanket treatment. Define consistent translucency, blur, border luminance and elevation tokens. Keep text in sufficiently opaque contrast-bearing regions. Avoid nesting many blurs and stacking expensive backdrop filters.

~~~css
.glass {
  background: rgb(255 255 255 / 0.72);
  border: 1px solid rgb(255 255 255 / 0.45);
  box-shadow: 0 12px 32px rgb(0 0 0 / 0.12);
}
@supports (backdrop-filter: blur(12px)) {
  .glass { backdrop-filter: blur(12px); }
}
~~~

## Production checks
Test against every background variant, including photographs and dynamic imagery. Provide graceful no-blur fallback and consider reduced-transparency preferences where supported. Check WCAG contrast for text and controls, mobile GPU/frame impact, focus outlines and nested modal readability.

## Done when
The style serves a product goal, works without blur, and is legible on real devices.
