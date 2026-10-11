# Data tables, lists, grids and async display

Consult only for Table/DataGrid/TreeTable, lists, cards, charts, virtualization or similar.

1. Classify requirements: static table, sort/filter/paginate, selectable rows, grouping, tree, inline editing, infinite scrolling, virtualized large datasets and server-side controls.
2. Confirm whether the provider ships this functionality or delegates to an extension/third-party engine. Example: MUI DataGrid has separate X licensing; Mantine's core Table is not a built-in advanced DataTable.
3. Define stable keys, typed columns, row actions, loading/empty/error, accessibility, focus navigation, sort indicators and screen reader table semantics.
4. For remote data, keep pagination/sorting/filtering as explicit app state and align server contracts with UI state; avoid mixing client and server sorting.
5. Virtualization requires measured row heights, accessible fallback and careful sticky headers/focus retention. Check layout overflow on mobile before choosing horizontal scrolling.
6. For charts, provide accessible labels, units and non-color encodings; inspect provider integration and licensing.

**Examples to research:** MUI X DataGrid, PrimeReact/PrimeVue/PrimeNG DataTable, Ant Design Table, Quasar QTable, Angular MatTable, Mantine Table and Flutter DataTable.
