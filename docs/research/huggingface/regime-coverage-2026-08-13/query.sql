COPY (
  WITH totals AS (
    SELECT
      regime,
      COUNT(*)::INTEGER AS total_items
    FROM data
    GROUP BY regime
  ),
  coded AS (
    SELECT
      regime_iconocratico AS regime,
      COUNT(*)::INTEGER AS coded_items
    FROM read_parquet(
      'https://huggingface.co/datasets/warholana/iconocracy-corpus/resolve/refs%2Fconvert%2Fparquet/purification/train/0000.parquet'
    )
    GROUP BY regime_iconocratico
  )
  SELECT
    totals.regime,
    totals.total_items,
    coded.coded_items,
    totals.total_items - coded.coded_items AS pending_items,
    ROUND(100.0 * coded.coded_items / totals.total_items, 1) AS coverage_pct
  FROM totals
  JOIN coded USING (regime)
  ORDER BY totals.total_items DESC
) TO 'tmp_coverage.csv' (FORMAT CSV, HEADER, DELIMITER ',');
