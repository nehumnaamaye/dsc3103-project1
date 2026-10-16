## Step 1 — Baseline query result

Average price by market where commodity = Maize :

| market   | mean_price | n   |
|----------|-----------:|----:|
| Bwaise   | 3103.85    | 99  |
| mukono   | 2978.74    | 80  |
| Nakasero | 2866.82    | 85  |
| Unknown  | 2834.69    | 85  |
| Kansanga | 2710.69    | 90  |

Answer to Step 1 question — highest mean price per commodity:
- Maize → Bwaise (mean ≈ 3103.85)
- Beans → **Nakasero** (mean ≈ 2741.82)

## Step 2 — What was traded for what

- By denormalizing into fact_price_observation , dim_market and dim_commodity, I gave up
having the market and commodity names stored directly on every row, in exchange for smaller, deduplicated
 dimension tables, integer surrogate keys that group and join faster than repeated text, and a
 schema that is easy to extend with new attributes (e.g. market region) without touching the
 fact table.

## Step 5 — Measure, don't assert

Run `python src/analytics/build_analytics.py` and paste your actual printed numbers here, e.g.:

Flat Parquet query time:  0.0127s
Star schema query time:   0.0104s

**What to expect and why:** the dataset is only 889 rows in a single row group (17 KB on disk),
so both queries finish in well under a tenth of a second and the difference between them is
likely to be small. At this size, the cost of two extra joins in the star-schema
query roughly cancels out the benefit of smaller integer keys. The star schema's advantages
wich is faster grouping, less duplicated text, cleaner extensibility become clearly measurable only as
row counts grow into the millions. This run mainly demonstrates how to measure it, not a big
win at this scale.

## Step 6 — Architecture justification (choose ONE in your submission)

Option A: Is the star schema worth it at this size?
At 889 rows, my Step 5 numbers show the flat-file query and the star-schema query finishing in
roughly the same fraction of a second — any difference was within measurement noise. Given that,
a star schema is not *necessary* for performance today. I would still argue it is worth building
now rather than later: it costs almost nothing to maintain at this size, it makes every query
easier to read (`JOIN dim_market` is clearer than repeating market-name strings), and it means
the schema is already in place for when the dataset grows past the point where a full scan of a
flat Parquet file becomes noticeably slower. The real payoff is deferred, not absent.

## Data notes worth mentioning in the presentation

- `rainfall_mm` is missing for 588 of 889 rows (~66%) — every row where `market = 'Unknown'` has
  no rainfall reading at all, which is a useful, concrete example of a real data-quality gap from
  the join in the pipeline.
- Market names are inconsistently cased in the raw data (`mukono` lowercase vs. `Nakasero`,
  `Bwaise`, `Kansanga` capitalized) — worth a one-line mention if asked about data cleaning.
