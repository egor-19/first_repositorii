from flask import Blueprint, render_template, request, current_app
from database.sql_provider import SQLProvider
from query.model_route import model_route
import os
import json
from decorators.access import group_required

model_app = Blueprint('model_app', __name__, template_folder='templates')

# Загружаем SQL-провайдер
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

# Загружаем конфиг запросов из JSON
with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'query_config.json'), encoding='utf-8') as f:
    QUERY_CONFIG = json.load(f)

@model_app.route('/', methods=['GET'])
@group_required
def query_form():
    """
    Контроллер: показывает форму для выбора типа запроса и параметров
    """
    return render_template('query_form.html')

@model_app.route('/result', methods=['POST'])
@group_required
def query_result():
    """
    Контроллер: получает данные из формы, вызывает модель, возвращает результат
    """
    query_type = request.form.get('query_type')
    config = QUERY_CONFIG.get(query_type)
    if not config:
        return render_template('query_form.html', error="Выберите тип запроса!")

    # Собираем параметры из формы согласно конфигу выбранного запроса
    user_input = {}
    for param in config['params']:
        value = request.form.get(param)
        print(f'param: {param}, value: {value}')  # Диагностика: выводим имя и значение параметра
        if not value:
            # Если параметр не заполнен — возвращаем форму с ошибкой
            return render_template('query_form.html', error=f"Введите параметр: {param}!")
        user_input[param] = value.strip()  # Удаляем лишние пробелы

    # Вызываем модель для выполнения SQL-запроса с собранными параметрами
    result_info = model_route(provider, user_input, config['sql'])

    # Обрабатываем результат выполнения запроса
    if result_info.status:
        items = list(result_info.result)  # Преобразуем результат к списку
        print('items from DB:', items)    # Диагностика: выводим полученные строки
        dict_items = [dict(zip(config['columns'], row)) for row in items] if items else []
        print('dict_items for template:', dict_items)
        # Проверка: все ли значения во всех строках пустые/None
        all_empty = True
        for row in dict_items:
            for value in row.values():
                if value not in (None, '', [], {}):
                    all_empty = False
                    break
            if not all_empty:
                break
        return render_template('query_result.html', items=dict_items, columns=config['columns'], all_empty=all_empty)
    else:
        # Если запрос завершился с ошибкой — возвращаем форму с сообщением
        return render_template('query_form.html', error=result_info.err_message)


