SELECT
    prod_id,
    prod_name,
    prod_price,
    total_quantity,
    total_amount,
    year,
    month
FROM reports
WHERE year = %s AND month = %s
ORDER BY total_amount DESC;