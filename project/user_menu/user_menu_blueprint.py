
from flask import Blueprint, render_template, session
from user_menu.user_menu_module import get_bonus_history

user_menu_blueprint = Blueprint('user_menu', __name__, template_folder='templates')

@user_menu_blueprint.route('/bonus_history')
def bonus_history():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('bonus_history.html', history=None, error='Пользователь не найден')
    history = get_bonus_history(user_id)
    total_bonus = None
    if history and len(history) > 0:
        try:
            total_bonus = sum(row['Всего бонусов'] for row in history if row.get('Всего бонусов') is not None)
        except Exception:
            total_bonus = None
    return render_template('bonus_history.html', history=history, total_bonus=total_bonus)
