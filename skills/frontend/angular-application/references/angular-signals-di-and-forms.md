# Angular Signals, DI and typed reactive forms

**Read when:** implementing or testing angular signals, di and typed reactive forms.

## Technical method
1. Angular signals: signal() for mutable state, computed() for pure derived values. Use effect() only for imperative non-reactive APIs, not copying signals; Angular documentation warns about update cycles and recommends computed/linkedSignal when supported.

2. Standalone component plus dependency injection at appropriate scope controls ownership. A root singleton service should not store one current SSR user's secret state. Typed ReactiveForms help developer correctness but backend still validates and authorizes.

3. Example (component snippet): readonly count = signal(0); readonly double = computed(() => this.count() * 2); increment() { this.count.update(v=>v+1); } No effect needed.

4. Confirm Angular major, signal input/output APIs, zoneless support and SSR config before applying snippets. Do not convert a large legacy NgModule project to standalone blindly.

5. Test template result, component inputs, DI mocks, validation errors, asynchronous resources and SSR request scope. Include keyboard/focus and network timeout behaviors.

## Production and security gate
Pin actual versions and hosting adapter. Test negative permission, malformed input, stale response after identity changes, mismatched SSR/hydration, slow/error behavior and browser keyboard interaction. Validate rendered payload for confidential fields and distinguish route visibility from API authorization. Record which assertions ran against the actual framework versus illustrative examples; don't claim a deployment is safe solely because static tests passed.

## Official references
- https://angular.dev/guide/signals
- https://angular.dev/guide/signals/effect
- https://angular.dev/guide/forms/typed-forms
