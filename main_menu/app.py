import json
import os
from flask import Flask, render_template, session
from auth.auth_blueprint import auth_blueprint
from query.model_blueprint import model_app
from decorators.access import login_required
from reports.reports_blueprint import reports_bp

from basket.basket_blueprint import basket_bp
from user_menu.user_menu_blueprint import user_menu_blueprint

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# === Загружаем конфиг БД ===
db_config_path = os.path.join(os.path.dirname(__file__), '../data/db_config.json')
with open(db_config_path, 'r', encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)

# === Загружаем права доступа ===
access_path = os.path.join(os.path.dirname(__file__), '../data/access.json')
with open(access_path, 'r', encoding='utf-8') as f:
    app.config['db_access'] = json.load(f)

# === Регистрируем блюпринты ===
app.register_blueprint(auth_blueprint)
app.register_blueprint(model_app, url_prefix='/query')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(basket_bp)
app.register_blueprint(user_menu_blueprint, url_prefix='/user_menu')

# === Главное меню ===
@app.route('/')
@login_required
def main_menu():
    username = session.get('username')
    group = session.get('user_group')
    if group == 'user':
        # Для внешнего пользователя показываем меню действий
        # Получаем имя пользователя для приветствия
        from database.select import select_list
        sql = "SELECT full_name FROM users WHERE username = %s"
        result = select_list(sql, [username])
        full_name = result[0][0] if result else username
        return render_template('user_menu.html', username=username, group=group, full_name=full_name)
    else:
        return render_template('menu.html', username=username, group=group)

@app.route('/exit')
@login_required
def exit_page():
    session.clear()
    return render_template('goodbye.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)