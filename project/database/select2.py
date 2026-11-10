from database.DBcm import DBContextManager
from flask import current_app  # глобальная переменная с глобальными конфигурационными данными
from database.select import select_list

def select_list2(_sql, user_list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError("Курсор не создан")
        else:
            cursor.execute(_sql, user_list)
            result = cursor.fetchall()
            schema = []
            for item in cursor.description:
                schema.append(item[0])
            print(schema)
    return result, schema


def select_dict2(_sql, user_dict: dict):
    user_list = []
    for key in user_dict:
        user_list.append(user_dict[key])
    print('User_list in select_dict:', user_list)

    result, schema = select_list2(_sql, user_list)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    print(result_dict)
    return result_dict