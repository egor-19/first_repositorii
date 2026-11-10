-- Получить список всех рейсов по аэропорту отправления
SELECT * FROM Flights WHERE departure_airport = %s ORDER BY departure_date;
