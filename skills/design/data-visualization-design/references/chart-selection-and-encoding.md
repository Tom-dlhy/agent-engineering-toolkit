# Chart selection, graphical encoding and comparison

Read when: deciding how to depict a verified measure or when reviewing a chart whose shape may distort meaning.

## Start from the question, not an attractive template
| User question | Default candidate | Avoid / investigate |
|---|---|---|
| Compare categories | aligned bars or ranked table | 3D bars, unsorted long category labels |
| Show time trend | line for continuous trend; bars for discrete intervals | joining gaps as known data, unlabeled irregular spacing |
| Compare distribution | histogram, box plot or table of quantiles | pie chart with many categories |
| Examine two quantities | scatter with labeled scales, unit definitions | using radius/area inconsistently |
| Show part-to-whole | 100% stacked bar if few comparable parts | pie slices when differences are close or categories numerous |
| Monitor a handful of KPIs | metric values with change and period, sometimes sparklines | invented "growth" when denominator not verified |

The mapping is a starting rule, not a vendor API or universal statistical theorem. Determine categorical/ordered/numeric/time units and whether baseline or domain transformation changes interpretation. For bars, use a zero baseline unless a clearly justified and disclosed exception (some diverging/delta visualizations differ). For lines, specify units and readable axes; choose linear/log only deliberately and label log transforms. Never combine distinct units on dual axes without addressing misinterpretation.

## One specification, arbitrary compatible renderer
```yaml
question: Compare resolved tickets per week
metric_owner: analytics-modeling (or explicit source)
x: iso_week
y: resolved_count
unit: tickets
aggregation: weekly, specify timezone/window
candidate: bar
missing_period: missing (do not coerce to 0)
axis: zero baseline, integer counts
fallback: labeled table + concise trend summary
provider: inspect installed chart components first
```
This sample does not claim the product has such a metric. Use actual data/contracts for implementations, and do not prescribe a React code snippet here: the UI provider owns exact chart APIs.

## Acceptance and counterexamples
- Are axes and units explicit and values reproducible from documented metrics?
- Are negative values, zero, sparse dates and missing intervals handled without silent misleading interpolation?
- Do number formatting, sorting and chart type match decision intent?
- Can a user identify the important comparison using a table alternative?
- Is text readable at representative widths; are legends and series labels useful, not boilerplate?

Primary references: https://www.w3.org/WAI/tutorials/images/complex/ and https://www.w3.org/WAI/tutorials/tables/
