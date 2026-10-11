# Svelte 5 runes and components

**Read when:** implementing or testing svelte 5 runes and components.

## Technical method
1. Svelte 5 state uses $state for mutable reactive variables, $derived for pure computed values, and $effect for external effects. $effect runs in browser, NOT SSR, and effects writing tracked dependencies can loop. Do not use effects for state duplication.

2. Component inputs use $props() in Svelte 5, not blindly old Svelte 4 export let syntax. Keep keys on each lists and explicit focus/labels in markup. Use context carefully when state is truly shared.

3. Example: let count = $state(0); let doubled = $derived(count * 2); is valid in a Svelte 5 component; an $effect that writes count whenever doubled changes is unnecessary and risky.

4. SSR global variables in server modules can persist between requests: currentUser must be per-request. HTML injection via {@html ...} needs sanitized trusted content and careful CSP.

5. Test derived dependencies, $effect cleanup on unmount, key reorder, disabled input handling, hydration with no effects on server, and TypeScript/svelte-check against installed version.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://svelte.dev/docs/svelte/%24state
- https://svelte.dev/docs/svelte/%24derived
- https://svelte.dev/docs/svelte/%24effect
