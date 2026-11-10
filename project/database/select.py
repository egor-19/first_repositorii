from database.DBcm import DBContextManager
from flask import current_app # Глобальная переменная с глобальным конфигурационным словарю


def select_list(_sql: str, param_list: list) -> tuple:
    with DBContextManager(current_app.config['db_config']) as cursor:
        result = None
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            print('SQL:', _sql)
            print('Params:', param_list)
            print('Param repr:', [repr(p) for p in param_list])
            cursor.execute(_sql, param_list)
            result = cursor.fetchall()
            print('DB result:', result)
            if 'money' in _sql or 'SUM' in _sql:
                print('Money query result:', result)
    return result

def select_dict(_sql: str, user_input: dict) -> tuple:
    user_list = []
    for key in user_input:
        user_list.append(user_input[key])
    print('SQL:', _sql)
    print('user_list in dict:', user_list)
    print('user_list in dict:', user_list)
    result = select_list(_sql, user_list)
    return result


def call_procedure(proc_name: str, param_list: list):
    # Создаётся соединение с БД на основе конфигурации приложения.
    with DBContextManager(current_app.config['db_config']) as cursor:
        #Проверка успешности подключения
        if cursor is None:
            raise ValueError('Курсор не создан')

        # Правильный вызов хранимой процедуры
        cursor.callproc(proc_name, param_list)
        result = cursor.fetchall()

    return result
def execute_sql(_sql: str, param_list: list = None) -> int:
    """
    Универсальный метод выполнения SQL-команд (INSERT, UPDATE, DELETE).
    Возвращает количество затронутых строк.
    """
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")

        if param_list:
            cursor.execute(_sql, param_list)
        else:
            cursor.execute(_sql)

        # rowcount — сколько строк изменено
        return cursor.rowcount