
from database.select2 import select_list2, select_dict2
import os
from flask import current_app

def get_bonus_history(user_id):
    sql_path = os.path.join(os.path.dirname(__file__), 'sql', 'get_bonus_history.sql')
    with open(sql_path, encoding='utf-8') as f:
        sql = f.read()
    history = select_dict2(sql, {"user_id": user_id})
    return history
