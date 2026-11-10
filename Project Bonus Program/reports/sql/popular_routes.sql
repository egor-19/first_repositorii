SELECT
    year,
    month,
    departure_airport,
    arrival_airport,
    tickets_sold,
    created_at
FROM
    report_popular_routes
WHERE
    year = %s
    AND (month = %s OR month IS NULL)
ORDER BY
    tickets_sold DESC, created_at DESC; 