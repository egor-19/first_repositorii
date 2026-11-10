-- Получить все билеты пассажира по имени и фамилии
SELECT t.*, f.flight_number, f.departure_airport, f.arrival_airport, f.departure_date, f.arrival_date
FROM Tickets t
JOIN Passengers p ON t.passenger_id = p.passenger_id
JOIN Flights f ON t.flight_id = f.flight_id
WHERE p.first_name LIKE %s AND p.last_name LIKE %s
ORDER BY f.departure_date;