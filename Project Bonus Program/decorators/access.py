# main_menu/access.py
from functools import wraps
from flask import session, redirect, url_for, current_app, request

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth_blueprint.auth_form'))
    return wrapper

'''	•	*args — это “позиционные” аргументы (обычные, без имени);
	•	**kwargs — это “именованные” аргументы (типа id=5, name='Nick').'''

def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' not in session:
            return redirect(url_for('auth_blueprint.auth_form'))

        # Достаём словарь прав доступа (загружен в app.config в app.py)
        access = current_app.config.get('db_access', {})

        # Определяем, из какого blueprint пришёл запрос
        # Например: "query_blueprint.query_form" → "query_blueprint"
        user_request = request.endpoint.split('.')[0]  # имя blueprint-а
        user_role = session.get('user_group')

        # Проверяем: есть ли у этой роли право на данный blueprint
        if user_role in access and user_request in access[user_role]:
            return func(*args, **kwargs)
        else:
            return "⛔ У вас нет прав на доступ к этой странице."
    return wrapper