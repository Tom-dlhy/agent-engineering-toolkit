# Data tables, grids, lists and async display

**Read when:** the UI contains tables/grids, filterable lists, pagination, virtualization, tree views or async data cards.

## Match feature requirement to component

| Need | Candidate | What must be implemented |
|---|---|---|
| Small static table | Native `table`, provider Table | `caption`, `th scope`, responsive overflow |
| Sort/filter/page on small in-memory dataset | Provider table + local state | Stable row keys, explicit sort state, no hidden filter surprises |
| Remote searchable/paginated data | Provider advanced DataGrid/Table | Backend query contract, total count, loading, error, stale-response cancellation |
| Massive scrolling lists | Virtualized list/row component | Stable IDs, measured heights, keyboard continuity and accessible fallback |
| Editable grid | Purpose-built component | Validation, row save/cancel, conflict resolution and optimistic rollback |

Material UI's advanced DataGrid is a separate MUI X product with tier-specific features. Mantine core Table is not a full enterprise grid. PrimeReact, PrimeVue, PrimeNG and Quasar each expose their own lazy/server contracts—do not reuse event payload names from another provider.

## Server pagination example: state is not data

```ts
type Query = {
  page: number
  pageSize: number
  sortField?: string
  sortDirection?: 'asc' | 'desc'
  filter?: string
}
type Page<Row> = { rows: Row[]; totalRows: number }
```

The UI must keep `query` stable and request a new `Page<Row>` whenever query changes. On quick sorting/filter changes, cancel or discard superseded responses, preserve the correct loading state, and reset the page to a valid index. If total rows are unknown, use an API-supported cursor/hasMore model rather than inventing an exact count.

### Row identity

Use a stable server ID or compound key, not the array index, particularly when sorting, paging, editing or selecting. Selection state may refer to rows not present in the current page; decide whether cross-page selection is allowed.

## Accessibility and virtualization

For tables ensure meaningful column headings/sort state. An interactive row must expose keyboard functionality rather than click-only. Virtualized grids can reuse DOM nodes; ensure focus remains on logical cell/row and screen-reader announcements are still intelligible. Large row height variability, sticky columns and portals can break scroll geometry.

## Test matrix

Empty response, loading skeleton vs actual table header, HTTP failure, unauthorized action, stale response on filter change, sort by nulls/locale, selection across pages, 10k rows, offline recovery, small screens and column overflow. Record exact backend and provider contracts rather than guessing.
