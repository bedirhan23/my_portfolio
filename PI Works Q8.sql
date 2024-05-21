
WITH MedianVaccination AS (
    SELECT
        country,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY daily_vaccinations) AS median_vaccination
    FROM
        your_table_name
    WHERE
        daily_vaccinations IS NOT NULL
    GROUP BY
        country
)
  
UPDATE
    your_table_name AS t
SET
    daily_vaccinations = COALESCE(t.daily_vaccinations, mv.median_vaccination)
FROM
    MedianVaccination AS mv
WHERE
    t.country = mv.country;
