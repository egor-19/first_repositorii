SELECT
    year,
    month,
    month_str,
    registrations_count,
    created_at
FROM
    report_new_passenger_registrations
WHERE
    year = %s
    AND (month = %s OR month IS NULL)
ORDER BY
    created_at DESC;