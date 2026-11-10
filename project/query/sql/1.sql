-- Получить пользователей с бонусными милями больше N (BonusMiles2)
SELECT u.*, b.miles_amount, b.last_update
FROM users u
JOIN BonusMiles2 b ON u.id = b.buyer_id
WHERE b.miles_amount > %s
ORDER BY b.miles_amount DESC;