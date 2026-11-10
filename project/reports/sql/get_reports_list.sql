SELECT
    report_id,
    year,
    month,
    total_sales,
    created_at
FROM reports
ORDER BY year DESC, month DESC;