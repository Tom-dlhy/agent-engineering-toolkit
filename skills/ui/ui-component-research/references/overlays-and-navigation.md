# Overlays and navigation

Consult only for Dialog, Sheet, Drawer, Menu, Popover, Tooltip, Tabs, Sidebar or mobile navigation.

1. Read the provider's primitive anatomy: trigger, portal/container, content, title/description, backdrop, close button and event hooks.
2. For true modals, verify accessible name, initial focus, focus trap, Escape, outside click policy, focus restoration and body scroll lock. Do not reimplement built-in focus logic.
3. Check provider-specific custom trigger composition: Radix `asChild`, Base UI `render`, React Aria slots/render props, Svelte snippets and Flutter widget builders have different contracts.
4. Tabs and menus need correct semantics for focus/selection vs activation, roving focus, nesting, keyboard mapping and route state persistence.
5. Consider responsive orientation, portals/z-index, scrolling, SSR hydration, browser back navigation and device safe areas; Ionic and React Native navigation stacks need platform-specific treatment.

**Examples to research:** Dialog, Sheet, DropdownMenu, NavigationMenu, Sidebars and mobile action sheets in the installed provider's official docs.
