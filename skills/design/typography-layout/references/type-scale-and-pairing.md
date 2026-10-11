# Typography engineering — scalable hierarchy and intentional pairings

**Read when:** choosing fonts and text scale for a page, design system or cross-device editorial hierarchy.

## Choose roles first

Display: expressive, rare; headings: navigational hierarchy; body: long reading; UI labels: compact clarity; data: dense, possibly tabular numerals. A brand can work well with one family if weights/optical sizes suffice. Don't force a trendy pairing onto a small utility app.

### Pairing dimensions

- **Contrast**: editorial serif display and neutral sans body can communicate culture and practicality; too much contrast fights coherence.
- **Character**: x-height, width, contrast of strokes and numeral appearance matter more than font marketing labels.
- **Fallback behavior**: include script coverage, accent marks, numbers, currency, punctuation and CJK/RTL when required.
- **License**: verify web embedding and distribution; a free preview font is not automatically allowed in production.
- **Performance**: variable font can reduce files but may have large range and unicode; subset responsibly, never remove required glyphs.

## A fluid heading scale

~~~css
:root {
  --text-body: 1rem;
  --text-display: clamp(2.4rem, 5vw + 0.5rem, 4.5rem);
  --text-heading: clamp(1.5rem, 2vw + 0.75rem, 2.25rem);
}
.article {
  max-width: 68ch;
  line-height: 1.6;
  text-wrap: pretty;
}
h1 {
  font-size: var(--text-display);
  line-height: 1.05;
  text-wrap: balance;
}
~~~

Treat values as testable starting points; adjust for actual font metrics, viewport and content. Browser support for text-wrap properties should be reviewed for target clients. A heading's tight line height may be wrong for languages with taller glyphs.

## Quality checks

Read paragraph on 320px mobile and wide desktop, zoom to 200%, compare fallbacks during load, test long German-style words and French accents, ensure button text doesn't truncate and table numerals align. Make heading structure semantic even when sizes are visually customized.

Method inspired by typography guidance in: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/67803eac81607188194aea9842a723b89326d90d/.claude/skills/ui-ux-pro-max/SKILL.md .
