
from flask import Blueprint, render_template, request, url_for, session, redirect, current_app
import os
from database.sql_provider import SQLProvider
from database.DBcm import DBContextManager
from basket.basket_module import basket_model, create_full_order
from database.select import select_list
from decorators.access import group_required

basket_bp = Blueprint('basket_bp', __name__, template_folder='templates')

@basket_bp.route('/buy_ticket', methods=['GET', 'POST'])
@group_required
def buy_ticket():
    from datetime import date
    message = None
    flights = []
    # Получаем список рейсов
    sql_flights = "SELECT flight_id, flight_number, departure_airport, arrival_airport, departure_date FROM Flights ORDER BY departure_date"
    with DBContextManager(current_app.config['db_config']) as cursor:
        cursor.execute(sql_flights)
        flights = [
            {
                'flight_id': row[0],
                'flight_number': row[1],
                'departure_airport': row[2],
                'arrival_airport': row[3],
                'departure_date': row[4],
            } for row in cursor.fetchall()
        ]
    if request.method == 'POST':
        user_id = session.get('user_id')
        flight_id = request.form.get('flight_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        ticket_class = request.form.get('ticket_class')
        purchase_date = date.today()
        # 1. Найти или создать пассажира
        with DBContextManager(current_app.config['db_config']) as cursor:
            cursor.execute("SELECT passenger_id FROM Passengers WHERE first_name=%s AND last_name=%s", [first_name, last_name])
            row = cursor.fetchone()
            if row:
                passenger_id = row[0]
            else:
                cursor.execute("INSERT INTO Passengers (first_name, last_name, registration_date) VALUES (%s, %s, %s)", [first_name, last_name, purchase_date])
                passenger_id = cursor.lastrowid
            # 2. Получить цену билета (можно доработать под разные классы)
            cursor.execute("SELECT 8000.00", [])  # Здесь можно реализовать свою логику ценообразования
            ticket_price = float(cursor.fetchone()[0])
            # 3. Создать билет
            cursor.execute("INSERT INTO Tickets (passenger_id, flight_id, purchase_date, ticket_price, ticket_class) VALUES (%s, %s, %s, %s, %s)", [passenger_id, flight_id, purchase_date, ticket_price, ticket_class])
            ticket_id = cursor.lastrowid
            # 4. Добавить в TicketBuyers
            cursor.execute("INSERT INTO TicketBuyers (ticket_id, buyer_id) VALUES (%s, %s)", [ticket_id, user_id])
            # 5. Начислить бонусы
            # Получить инфо о рейсе
            cursor.execute("SELECT departure_date, departure_airport, arrival_airport FROM Flights WHERE flight_id=%s", [flight_id])
            f = cursor.fetchone()
            flight_date, departure_airport, arrival_airport = f[0], f[1], f[2]
            fixed_bonus = 80
            if ticket_class == 'эконом':
                total_bonus = fixed_bonus + int(ticket_price * 0.05)
            elif ticket_class == 'бизнес':
                total_bonus = fixed_bonus + int(ticket_price * 0.10)
            else:
                total_bonus = fixed_bonus
            cursor.execute("INSERT INTO BonusHistory (buyer_id, ticket_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [user_id, ticket_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, purchase_date])
        message = 'Билет успешно куплен и бонусы начислены!'
    return render_template('buy_ticket.html', flights=flights, message=message)

@basket_bp.route('/create_ticket_form', methods=['GET', 'POST'])
@group_required
def create_ticket_form():
    from datetime import date
    message = None
    if request.method == 'POST':
        user_id = session.get('user_id')
        flight_number = request.form.get('flight_number')
        passenger_name = request.form.get('passenger_name')
        passport = request.form.get('passport')
        seat = request.form.get('seat')
        ticket_class = request.form.get('ticket_class')
        price = request.form.get('price')
        accrual_date = date.today()
        fixed_bonus = 80
        total_bonus = fixed_bonus
        # Сохраняем билет в Tickets
        sql_ticket = '''INSERT INTO Tickets (flight_number, passenger_name, passport, seat, ticket_class, price, buyer_id) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
        with DBContextManager(current_app.config['db_config']) as cursor:
            cursor.execute(sql_ticket, [flight_number, passenger_name, passport, seat, ticket_class, price, user_id])
            ticket_id = cursor.lastrowid
            # Сохраняем бонусы
            sql_bonus = '''INSERT INTO BonusHistory (buyer_id, ticket_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            cursor.execute(sql_bonus, [user_id, ticket_id, accrual_date, 'N/A', 'N/A', price, ticket_class, fixed_bonus, total_bonus, accrual_date])
        message = 'Билет успешно оформлен и бонусы начислены!'
    return render_template('create_ticket_form.html', message=message)
from flask import Blueprint, render_template, request, url_for, session, redirect
import os
from database.sql_provider import SQLProvider
from database.DBcm import DBContextManager
from basket.basket_module import basket_model, create_full_order
from database.select import select_list
from decorators.access import group_required
from flask import current_app

basket_bp = Blueprint('basket_bp', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# ==============================
# 1. Показываем корзину
# ==============================
@basket_bp.route('/order')
@group_required
def order_index():
    user_id = session.get('user_id')
    # Показываем все билеты, купленные этим пользователем
    sql = '''
        SELECT t.ticket_id, t.purchase_date, t.ticket_price, t.ticket_class,
               f.flight_number, f.departure_airport, f.arrival_airport, f.departure_date, f.arrival_date,
               p.first_name, p.last_name
        FROM Tickets t
        JOIN TicketBuyers tb ON t.ticket_id = tb.ticket_id
        JOIN Flights f ON t.flight_id = f.flight_id
        JOIN Passengers p ON t.passenger_id = p.passenger_id
        WHERE tb.buyer_id = %s
        ORDER BY t.purchase_date DESC
    '''
    tickets = []
    with DBContextManager(current_app.config['db_config']) as cursor:
        cursor.execute(sql, [user_id])
        for row in cursor.fetchall():
            tickets.append({
                'ticket_id': row[0],
                'purchase_date': row[1],
                'ticket_price': row[2],
                'ticket_class': row[3],
                'flight_number': row[4],
                'departure_airport': row[5],
                'arrival_airport': row[6],
                'departure_date': row[7],
                'arrival_date': row[8],
                'first_name': row[9],
                'last_name': row[10],
            })
    return render_template('basket_order_list.html', tickets=tickets)


# ==============================
# 2. Добавление товара в корзину
# ==============================
@basket_bp.route('/add_to_basket', methods=['POST'])
@group_required
def add_to_basket():
    if 'basket' not in session:
        session['basket'] = {}

    prod_id = request.form.get('prod_id')
    amount = int(request.form.get('amount', 1))

    # Если вдруг корзина сломана — чиним сразу
    if prod_id in session['basket'] and isinstance(session['basket'][prod_id], int):
        session['basket'][prod_id] = {"amount": session['basket'][prod_id]}

    if prod_id in session['basket']:
        session['basket'][prod_id]['amount'] += amount
    else:
        session['basket'][prod_id] = {'amount': amount}

    session.modified = True
    return redirect(url_for('basket_bp.order_index'))


# ==============================
# 3. Очистка корзины
# ==============================
@basket_bp.route('/clear_basket')
@group_required
def clear_basket():
    session.pop('basket', None)
    return redirect(url_for('basket_bp.order_index'))


# ==============================
# 4. Сохранение заказа
# ==============================
@basket_bp.route('/save_order')
@group_required
def save_order():
    basket = session.get('basket', {})
    user_id = session.get('user_id', 1)

    if not basket:
        return redirect(url_for('basket_bp.order_index'))

    # Нормализуем корзину
    for pid, it in list(basket.items()):
        if isinstance(it, int):
            basket[pid] = {'amount': it}

    # ВЫЗЫВАЕМ ЕДИНУЮ ТРАНЗАКЦИЮ
    result = create_full_order(provider, user_id, basket)

    if result.status:
        session.pop('basket', None)
        # Бонусы начисляются автоматически внутри create_full_order
        return render_template(
            'order_success.html',
            order_id=result.result,
            return_url=url_for('basket_bp.order_index')
        )
    else:
        return render_template(
            'order_error.html',
            message=result.err_message,
            return_url=url_for('basket_bp.order_index')
        )