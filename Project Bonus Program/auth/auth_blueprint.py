# query/auth_blueprint.py
import os
from flask import Blueprint, render_template, request, session, redirect, url_for
from database.sql_provider import SQLProvider
from .auth_model import check_user  # подключаем модель

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

# === 1. Отображение страницы входа (GET) ===
@auth_blueprint.route('/auth', methods=['GET'])
def auth_form():
    """
    Показывает форму для входа в систему.
    """
    return render_template('login.html')


# === 2. Обработка данных формы (POST) ===
@auth_blueprint.route('/auth', methods=['POST'])
def auth_process():
    """
    Обрабатывает данные из формы авторизации.
    """
    login = request.form.get('login')
    password = request.form.get('password')

    user = check_user(provider, login, password)

    if user:
        # создаём сессию
        session['user_id'] = user[0]  # id пользователя
        session['username'] = user[1]
        session['user_group'] = user[3]
        return redirect(url_for('main_menu'))
    else:
        # ошибка авторизации
        return render_template('login.html', message='❌ Неверный логин или пароль')


# === 3. Завершение сессии (выход из системы) ===
@auth_blueprint.route('/logout')
def logout():
    """
    Завершает сессию и возвращает на страницу авторизации.
    """
    session.clear()
    return redirect(url_for('auth_blueprint.auth_form'))