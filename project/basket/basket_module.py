def add_bonus_history_for_order(user_id, order_id, provider):
    """
    Добавляет запись о начислении бонусов в BonusHistory для каждого товара заказа (только для покупателя).
    """
    from datetime import date
    from database.DBcm import DBContextManager
    accrual_date = date.today()
    fixed_bonus = 80
    # Получаем все товары из order_list по order_id
    sql_items = "SELECT prod_id, p_amount FROM order_list WHERE o_id = %s"
    with DBContextManager(current_app.config['db_config']) as cursor:
        cursor.execute(sql_items, [order_id])
        items = cursor.fetchall()
        for prod_id, amount in items:
            # Получаем инфо о товаре
            sql_prod = provider.get('get_product_info.sql')
            cursor.execute(sql_prod, [prod_id])
            prod = cursor.fetchone()
            if not prod:
                continue
            ticket_price = float(prod['prod_price'])
            ticket_class = prod.get('prod_category', 'эконом')
            # Для примера аэропорты и даты фиктивные, замените на реальные если есть
            departure_airport = 'N/A'
            arrival_airport = 'N/A'
            flight_date = accrual_date
            total_bonus = fixed_bonus * amount
            # Вставка в BonusHistory
            cursor.execute(
                """
                INSERT INTO BonusHistory (buyer_id, ticket_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [user_id, order_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date]
            )
from dataclasses import dataclass
from database.select import execute_sql
from database.select2 import select_dict2
from database.DBcm import DBContextManager
from flask import current_app

def add_bonus_history(user_id, order_id, basket, provider):
    """
    Добавляет записи о начислении бонусов в BonusHistory для каждого товара заказа.
    """
    from datetime import date
    from database.DBcm import DBContextManager
    accrual_date = date.today()
    fixed_bonus = 80
    with DBContextManager(current_app.config['db_config']) as cursor:
        # Получаем детали товаров
        for prod_id, item in basket.items():
            # Получаем информацию о товаре (цена, название, класс)
            sql = provider.get('get_product_info.sql')
            cursor.execute(sql, [prod_id])
            prod = cursor.fetchone()
            if not prod:
                continue
            ticket_price = float(prod['prod_price'])
            ticket_class = prod.get('prod_class', 'эконом')
            amount = item['amount']
            total_bonus = fixed_bonus * amount
            # Для примера аэропорты и даты фиктивные, замените на реальные если есть
            departure_airport = prod.get('departure_airport', 'N/A')
            arrival_airport = prod.get('arrival_airport', 'N/A')
            flight_date = accrual_date
            # Вставка в BonusHistory
            cursor.execute(
                """
                INSERT INTO BonusHistory (buyer_id, ticket_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [user_id, order_id, flight_date, departure_airport, arrival_airport, ticket_price, ticket_class, fixed_bonus, total_bonus, accrual_date]
            )



@dataclass
class BasketResultInfo:
    result: any
    status: bool
    err_message: str = ""


def basket_model(provider, user_input: dict, sql_file: str, is_insert=False):
    _sql = provider.get(sql_file)
    params = list(user_input.values())

    # INSERT
    if is_insert:
        rows = execute_sql(_sql, params)

        if rows > 0:

            id_sql = provider.get("get_last_order_id.sql")
            last_id_result = select_dict2(id_sql, {"u_id": params[0]})

            if last_id_result:
                order_id = last_id_result[0]['order_id']
                return BasketResultInfo(order_id, True)

            return BasketResultInfo(None, False, "ID заказа не найден")

        return BasketResultInfo(None, False, "Ошибка INSERT")

    # SELECT
    result = select_dict2(_sql, user_input)
    if result:
        return BasketResultInfo(result, True)

    return BasketResultInfo(None, False, "Нет данных")

def create_full_order(provider, user_id: int, basket: dict):
    """
    Создаёт заказ + товары в одной транзакции.
    Возвращает BasketResultInfo(order_id, True/False)
    """

    try:
        with DBContextManager(current_app.config['db_config']) as cursor:
            # 1. Создать заказ
            sql_order = provider.get("create_order.sql")
            cursor.execute(sql_order, [user_id])
            order_id = cursor.lastrowid

            # 2. Добавлять товары
            sql_item = provider.get("add_order_item.sql")
            for prod_id, item in basket.items():
                cursor.execute(sql_item, [
                    order_id,
                    prod_id,
                    item["amount"]
                ])

        # commit произошёл автоматически
        # 3. Начислить бонусы (только для покупателя)
        add_bonus_history_for_order(user_id, order_id, provider)
        return BasketResultInfo(order_id, True)

    except Exception as e:
        return BasketResultInfo(None, False, f"Ошибка транзакции: {e}")