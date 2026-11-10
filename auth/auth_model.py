
from database.select import select_dict

def check_user(provider, login, password):
    """
    Проверяет пользователя в БД по логину и паролю.
    Возвращает запись пользователя или None.
    """

    # Загружаем SQL-запрос
    sql = provider.get('get_user.sql')

    # Параметры для подстановки
    user_input = {'login': login, 'password': password}

    # Вызываем универсальный метод select_dict()
    result = select_dict(sql, user_input)



    # Если нашли пользователя — возвращаем первую строку
    if result and len(result) > 0:
        return result[0]   # (u_id, login, password, user_group)
    else:
        return None