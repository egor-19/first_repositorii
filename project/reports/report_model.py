# model_reports.py
from dataclasses import dataclass
from database.select import select_dict, call_procedure
import json
import os


@dataclass
class ReportResult:
    data: list
    status: bool
    message: str


# Загружаем конфигурацию отчетов из JSON файла
def load_report_config():
    # Определяем абсолютный путь к файлу конфигурации
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'data', 'reports.json')

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Глобальная конфигурация отчетов
REPORT_CONFIG = load_report_config()


def get_report_types():
    return REPORT_CONFIG



def m_create_report(provider, report_type: str, params: dict):
    try:
        result = None  # Инициализация переменной result
        if report_type not in REPORT_CONFIG:
            return ReportResult(data=None, status=False, message='Неизвестный тип отчета')

        report_config = REPORT_CONFIG[report_type]

        # Подготовка параметров для процедуры
        procedure_params = []
        for param_name in report_config['create_params']:
            if param_name not in params:
                return ReportResult(data=None, status=False, message=f'Отсутствует параметр: {param_name}')
            procedure_params.append(params[param_name])

        # Логируем параметры процедуры
        print(f"🔍 [DEBUG] Параметры процедуры: {procedure_params}")

        # Вызываем хранимую процедуру
        result = call_procedure(report_config['create_procedure'], procedure_params)

        # Логируем результат вызова процедуры
        print(f"🔍 [DEBUG] Результат вызова процедуры: {result}"   )

        if result:
            status_from_db = result[0][0]  # 'success' или 'error'
            message_from_db = result[0][1]  # сообщение из процедуры

            if status_from_db == 'success':
                return ReportResult(data=None, status=True, message=message_from_db)
            else:
                return ReportResult(data=None, status=False, message=message_from_db)
        else:
            return ReportResult(data=None, status=False, message='Неизвестная ошибка при создании отчета')

    except Exception as e:
        return ReportResult(data=None, status=False, message=f'Ошибка при создании отчета: {str(e)}, result={result}')


def get_report(provider, report_type: str, params: dict):
    try:
        print(f"🔍 [DEBUG] Получение отчета: {report_type}")
        print(f"🔍 [DEBUG] Параметры: {params}")

        if report_type not in REPORT_CONFIG:
            return ReportResult(data=None, status=False, message='Неизвестный тип отчета')

        report_config = REPORT_CONFIG[report_type]
        print(f"🔍 [DEBUG] Конфиг отчета: {report_config}")

        # Получаем SQL запрос
        _sql = provider.get(report_config['view_sql'])
        print(f"🔍 [DEBUG] SQL запрос: {_sql}")

        # Подготовка параметров для SQL запроса
        sql_params = {}
        for param_name in report_config['view_params']:
            if param_name not in params:
                return ReportResult(data=None, status=False, message=f'Отсутствует параметр: {param_name}')
            sql_params[param_name] = params[param_name]

        print(f"🔍 [DEBUG] SQL параметры: {sql_params}")

        # Выполняем запрос
        result = select_dict(_sql, sql_params)
        print(f"🔍 [DEBUG] Результат запроса: {result}")

        if result:
            return ReportResult(data=result, status=True, message='Отчет успешно загружен')
        else:
            return ReportResult(data=None, status=False, message='Отчет не найден')

    except Exception as e:
        print(f"❌ [DEBUG] Ошибка в get_report: {str(e)}")
        return ReportResult(data=None, status=False, message=f'Ошибка при загрузке отчета: {str(e)}')
