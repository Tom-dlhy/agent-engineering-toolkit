# Component library candidates — curated selection index

**Read when:** Comparing potential providers for a new project or an explicit UI-library migration. Do not open when the existing library is already chosen.

This catalog is **not** a version compatibility oracle. Verify current package versions, official docs, licenses and package status at selection time. The selector should use this index *without loading 35 vendor SKILL.md bodies*.

| Library (skill name) | Ecosystem | Best-fit signal | Official docs |
|---|---|---|---|
| shadcn/ui (`shadcn-ui`) | React / TypeScript | source-owned components, Tailwind-first product UI and customizable design systems | https://ui.shadcn.com/docs |
| Base UI (`base-ui`) | React / TypeScript | headless accessible React primitives for a bespoke design system | https://base-ui.com/react/overview/quick-start |
| Radix Primitives (`radix-primitives`) | React / TypeScript | unstyled React interaction primitives for accessible custom interfaces | https://www.radix-ui.com/primitives/docs/overview/introduction |
| Radix Themes (`radix-themes`) | React / TypeScript | ready-styled Radix design language with consistent theme scales | https://www.radix-ui.com/themes/docs/overview/getting-started |
| React Aria Components (`react-aria-components`) | React / TypeScript | complex accessible interactions, keyboard use, internationalization and custom styling | https://react-spectrum.adobe.com/react-aria/components.html |
| HeroUI (`heroui`) | React / TypeScript | polished, styled React components for fast app delivery | https://www.heroui.com/docs |
| Mantine (`mantine`) | React / TypeScript | feature-rich SaaS, admin consoles and internal tools with integrated utilities | https://mantine.dev/ |
| Chakra UI (`chakra-ui`) | React / TypeScript | token-based React design systems and composable recipes | https://chakra-ui.com/docs |
| Material UI (MUI) (`mui`) | React / TypeScript | mature Material Design and enterprise dashboards | https://mui.com/material-ui/getting-started/ |
| Ant Design (`ant-design`) | React / TypeScript | data-dense, internationalized B2B applications | https://ant.design/components/overview/ |
| PrimeReact (`primereact`) | React / TypeScript | rich data tables, enterprise widgets and styled/unstyled options | https://primereact.org/ |
| Fluent UI React (`fluent-ui`) | React / TypeScript | Microsoft-inspired enterprise UI and accessibility conventions | https://react.fluentui.dev/ |
| Flowbite React (`flowbite-react`) | React / TypeScript | pre-styled Tailwind-oriented UI for conventional React apps | https://flowbite-react.com/docs/getting-started/introduction |
| Headless UI (`headless-ui`) | React and Vue | accessible unstyled patterns in React or Vue with Tailwind | https://headlessui.com/ |
| Vuetify (`vuetify`) | Vue / Nuxt | complete Material-style Vue applications | https://vuetifyjs.com/en/ |
| PrimeVue (`primevue`) | Vue / Nuxt | data-heavy Vue applications with theme and unstyled support | https://primevue.org/ |
| Quasar (`quasar`) | Vue / Nuxt | Vue apps requiring integrated routing, UI, platform and deployment tooling | https://quasar.dev/ |
| Element Plus (`element-plus`) | Vue / Nuxt | admin and enterprise Vue interfaces | https://element-plus.org/en-US/ |
| Ant Design Vue (`ant-design-vue`) | Vue / Nuxt | Ant Design conventions in enterprise Vue apps | https://www.antdv.com/components/overview |
| Angular Material (`angular-material`) | Angular | official Angular Material patterns with CDK integrations | https://material.angular.dev/ |
| PrimeNG (`primeng`) | Angular | rich enterprise data components in Angular | https://primeng.org/ |
| NG-ZORRO (`ng-zorro`) | Angular | Ant Design patterns for Angular enterprise teams | https://ng.ant.design/docs/introduce/en |
| Bits UI (`bits-ui`) | Svelte / SvelteKit | headless accessible primitives in Svelte 5 design systems | https://bits-ui.com/docs/introduction |
| Skeleton (`skeleton`) | Svelte and React | Tailwind-based UI system and themes for Svelte and supported React setups | https://www.skeleton.dev/ |
| Flowbite Svelte (`flowbite-svelte`) | Svelte / SvelteKit | ready-styled Tailwind components for rapid Svelte development | https://flowbite-svelte.com/ |
| daisyUI (`daisyui`) | CSS / Web Components | fast framework-agnostic Tailwind class-based interfaces | https://daisyui.com/docs/install/ |
| Bootstrap (`bootstrap`) | CSS / Web Components | conventional, mature and framework-agnostic web interfaces | https://getbootstrap.com/docs/ |
| Web Awesome (`web-awesome`) | CSS / Web Components | reusable standards-based Web Components across frameworks | https://webawesome.com/docs/ |
| Ionic (`ionic`) | Hybrid mobile | mobile-first hybrid application UI and navigation conventions | https://ionicframework.com/docs |
| React Native Paper (`react-native-paper`) | React Native / Expo | Material-aligned React Native and Expo applications | https://callstack.github.io/react-native-paper/ |
| Tamagui (`tamagui`) | React Native and Web | shared web and React Native design systems with tokens and optimizations | https://tamagui.dev/docs/intro/introduction |
| gluestack-ui (`gluestack-ui`) | React Native / Expo | open-code React Native/Expo components with NativeWind-style customization | https://gluestack.io/ui/docs/home/overview/introduction |
| React Native Elements (RNEUI) (`rneui`) | React Native / Expo | straightforward native UI components and theming | https://reactnativeelements.com/docs |
| Flutter Material (`flutter-material`) | Flutter | Flutter Material Design across mobile, web and desktop | https://docs.flutter.dev/ui/widgets/material |
| Flutter Cupertino (`flutter-cupertino`) | Flutter | Apple-style Flutter interfaces with iOS/macOS conventions | https://docs.flutter.dev/ui/widgets/cupertino |

## Shortlisting heuristics

- **React with design ownership:** first consider shadcn/ui, Base UI, Radix Primitives or React Aria; each has different styling and interaction tradeoffs.
- **React enterprise/data-heavy:** compare MUI (including MUI X licenses), Mantine, Ant Design, PrimeReact and Fluent UI; do not treat advanced tables as interchangeable.
- **Vue:** compare Vuetify/PrimeVue/Quasar/Element Plus/Ant Design Vue; retain existing Vue and Nuxt integrations.
- **Angular:** start with Angular Material; compare PrimeNG and NG-ZORRO when richer enterprise needs justify them.
- **Svelte:** Bits UI for headless design ownership, Skeleton/Flowbite Svelte for styled speed.
- **Agnostic/mobile:** daisyUI or Bootstrap for class-driven web, Web Awesome for custom elements, Ionic for hybrid navigation.
- **Native:** Paper for Material conventions, gluestack for source-owned components, Tamagui for web/native shared tokens, RNEUI for conventional UI.
- **Flutter:** Material is generally the standard platform baseline; Cupertino supports Apple idioms or explicitly adaptive screens.

A library may be considered only when its actual framework/version support and license fit are verified. Do not add all candidates to an installation profile.
