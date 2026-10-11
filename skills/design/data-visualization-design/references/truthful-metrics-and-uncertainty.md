# Honest KPI storytelling, uncertainty and scale

Read when: charts or dashboard KPIs have changing populations, denominators, missing data, uncertainty, comparison windows or risk of visual manipulation.

## Verify business truth at the source
Obtain denominator, numerator, granularity, filters, dimensions, aggregation, currency and unit, timezone, source freshness and correction/backfill semantics from `data/analytics-modeling` or the available contract. A chart skill cannot repair double-counting by restyling. A change from 5% to 6% can be **+1 percentage point** and **+20% relative**, and these are not interchangeable; keep the metric contract explicit. If a denominator is unavailable, do not infer one.

## Design invariants
1. Show actual period and comparison baseline, including known population changes.
2. Avoid bars with a clipped baseline; if an axis is deliberately truncated for a justified analytical line plot, label it visibly and assess the interpretation risk.
3. Keep missing data different from measured zero; label interpolation and imputation.
4. Use consistent units, scaling and color semantics between comparable panels; disclose log scales and smoothing windows.
5. Display variation/uncertainty (confidence bounds, ranges, sampling error) only when supplied/derivable from authorized calculations, **never** fabricate error bands.
6. Don't conceal important categories in a visual "Other" without a clear grouping rule and access to the underlying breakdown.
7. Report filters, time window, source and update time when needed for interpretation; loading/stale data must not appear as final truth.

## Useful negative fixtures
```text
Data: {week: W1, successes: 4, attempts: 20}, {week: W2, successes: 6, attempts: 50}
Incorrect: raw success counts imply conversion improved.
Check: W1 20%, W2 12%; counts rose while rate fell.
Required: metric owner confirms definition and population.
```
The fixture is synthetic, not real observed data. Test outliers, tiny sample sizes, changed timezones, percentage sums not exactly 100% due to rounding, and reversed sorted order.

## Boundaries
The data skill owns metric implementation and QA. The design skill can reject misleading presentations and request verified source changes; it cannot rewrite SQL or assert a statistical result without data. Document measurement limits, not fabricated "insights".

References: https://www.w3.org/WAI/tutorials/images/complex/ and https://www.w3.org/TR/WCAG22/
