SELECT 
	
	flight_date AS 'Дата вылета',
	departure_airport AS 'Откуда',
	arrival_airport AS 'Куда',
	ticket_price AS 'Цена билета',
	ticket_class AS 'Класс',
	fixed_bonus AS 'Фиксированный бонус',
	total_bonus AS 'Всего бонусов',
	accrual_date AS 'Дата начисления'
FROM BonusHistory
WHERE buyer_id = %s
ORDER BY accrual_date DESC;