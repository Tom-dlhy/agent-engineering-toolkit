# Feedback, tokens and visual consistency

Consult only for badges, alerts, skeletons, loaders, notifications, theming or responsive states.

1. Reuse semantic tokens (surface, foreground, muted, accent, danger, success) from the existing provider. Respect light/dark/high-contrast themes without raw per-control palette overrides.
2. Loading skeletons should resemble content geometry, announce long waits as appropriate and avoid layout shift; keep cancel/retry actions for recoverable errors.
3. Distinguish status feedback (inline alert), transient success (toast/snackbar), destructive confirmation (dialog), progress and validation error. Use provider conventions and avoid duplicate notification providers.
4. Audit icon library and sizing conventions; do not assume shadcn Lucide, Material Icons and Fluent Icons are interchangeable.
5. Verify contrast, reduced motion, touch targets, density, color-blind cues and screen reader messaging; test the exact theme/SSR environment.
6. In source-owned libraries, prefer updating documented variants/tokens rather than accumulating arbitrary one-off component overrides.

**Examples to research:** shadcn Alert/Skeleton/Badge, Chakra recipes, Mantine Notifications, MUI ThemeProvider, FluentProvider, Web Awesome themes, Flutter ThemeData, Tamagui Theme.
