# Vue 3 reactivity and component contracts

**Read when:** implementing or testing vue 3 reactivity and component contracts.

## Technical method
1. Use ref() for owned reactive primitives/objects; reactive() for proxy objects; computed() for pure derivation, watch()/watchEffect() for actual side effects and cleanup. Avoid destructuring reactive proxies without toRefs.

2. Typed defineProps/defineEmits and keyed v-for preserve component ownership. Use Pinia only for truly shared long-lived app state, not every form toggle.

3. Example decision: filteredProducts = computed(() => products.value.filter(p => p.name.includes(query.value))) is derived state; do not mirror it in another ref through a watcher.

4. Check reactive async watchers for stale requests and stop/cleanup. A direct mutable module-global currentUser is unsafe in SSR. Vue escapes interpolated template content but v-html bypasses escaping; never compile untrusted templates.

5. Test prop changes, keyed reordering, disabled/empty form states, async request cancellation, input focus, keyboard and no unsafe markup.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://vuejs.org/guide/essentials/reactivity-fundamentals.html
- https://vuejs.org/guide/essentials/watchers.html
- https://vuejs.org/guide/best-practices/security.html
