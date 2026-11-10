# reports.py (обновленная версия)
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import os
from database.sql_provider import SQLProvider
from reports.report_model import m_create_report, get_report, get_report_types
from decorators.access import login_required, group_required

reports_bp = Blueprint('reports_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@reports_bp.route('/', methods=['GET'])
@group_required
def reports_menu():
    report_types = get_report_types()
    return render_template('reports_menu.html', report_types=report_types)


@reports_bp.route('/create', methods=['GET', 'POST'])
@group_required
def create_report():
    report_type = request.args.get('type')
    report_types = get_report_types()

    if report_type not in report_types:
        return render_template('report_error.html',
                               message='Неизвестный тип отчета',
                               return_url=url_for('reports_bp.reports_menu'))

    report_config = report_types[report_type]

    if request.method == 'GET':
        return render_template('create_report_form.html',
                               report_type=report_type,
                               report_config=report_config)

    # POST запрос
    try:
        params = {}
        for field in report_config['form_fields']:
            field_name = field['name']
            if field['type'] == 'number':
                value = request.form.get(field_name)
                if value is None or value == '':
                    params[field_name] = None
                else:
                    try:
                        params[field_name] = int(value)
                    except ValueError:
                        return render_template('report_error.html',
                                               message=f'Поле "{field["label"]}" должно быть числом',
                                               return_url=url_for('reports_bp.create_report', type=report_type))
            else:
                value = request.form.get(field_name)
                params[field_name] = value if value is not None else None


        # Обязательность года и месяца для new_passenger_registrations
        if report_type in ('new_passenger_registrations', 'popular_routes'):
            missing = []
            year_val = params.get('year')
            month_val = params.get('month')
            if year_val is None or str(year_val).strip() == '':
                missing.append('год')
            if month_val is None or str(month_val).strip() == '':
                missing.append('месяц')
            if missing:
                msg = 'Необходимо заполнить следующие поля: ' + ', '.join(missing)
                return render_template('report_error.html',
                                       message=msg,
                                       return_url=url_for('reports_bp.create_report', type=report_type))
        # Стандартная валидация диапазонов
        if 'year' in params and params['year']:
            if params['year'] < 2000 or params['year'] > 2025:
                return render_template('report_error.html',
                                       message='Год должен быть в диапазоне 2000-2025',
                                       return_url=url_for('reports_bp.create_report', type=report_type))
        if 'month' in params and params['month']:
            if params['month'] < 1 or params['month'] > 12:
                return render_template('report_error.html',
                                       message='Месяц должен быть в диапазоне 1-12',
                                       return_url=url_for('reports_bp.create_report', type=report_type))
        if 'day' in params and params['day']:
            if params['day'] < 1 or params['day'] > 31:
                return render_template('report_error.html',
                                       message='День должен быть в диапазоне 1-31',
                                       return_url=url_for('reports_bp.create_report', type=report_type))

        # Создание отчета
        result = m_create_report(provider, report_type, params)

        if result.status:
            flash(result.message, 'success')
            return redirect(url_for('reports_bp.reports_menu'))
        else:
            return render_template('report_error.html',
                                   message=result.message,
                                   return_url=url_for('reports_bp.create_report', type=report_type))

    except Exception as e:
        return render_template('report_error.html',
                               message=f'Ошибка при создании отчета: {str(e)}',
                               return_url=url_for('reports_bp.create_report', type=report_type))


@reports_bp.route('/view', methods=['GET', 'POST'])
@group_required
def view_report():
    report_type = request.args.get('type')
    report_types = get_report_types()

    if report_type not in report_types:
        return render_template('report_error.html',
                               message='Неизвестный тип отчета',
                               return_url=url_for('reports_bp.reports_menu'))

    report_config = report_types[report_type]

    if request.method == 'GET':
        return render_template('view_report_form.html',
                               report_type=report_type,
                               report_config=report_config)

    # POST запрос
    try:
        params = {}
        for field in report_config['form_fields']:
            field_name = field['name']
            if field['type'] == 'number':
                value = request.form.get(field_name)
                if value is None or value == '':
                    params[field_name] = None
                else:
                    try:
                        params[field_name] = int(value)
                    except ValueError:
                        return render_template('report_error.html',
                                               message=f'Поле "{field["label"]}" должно быть числом',
                                               return_url=url_for('reports_bp.view_report', type=report_type))
            else:
                value = request.form.get(field_name)
                params[field_name] = value if value is not None else None


        # Обязательность года и месяца для new_passenger_registrations
        if report_type in ('new_passenger_registrations', 'popular_routes'):
            missing = []
            year_val = params.get('year')
            month_val = params.get('month')
            if year_val is None or str(year_val).strip() == '':
                missing.append('год')
            if month_val is None or str(month_val).strip() == '':
                missing.append('месяц')
            if missing:
                msg = 'Необходимо заполнить следующие поля: ' + ', '.join(missing)
                return render_template('report_error.html',
                                       message=msg,
                                       return_url=url_for('reports_bp.view_report', type=report_type))
        # Стандартная валидация диапазонов
        if 'year' in params and params['year']:
            if params['year'] < 2000 or params['year'] > 2025:
                return render_template('report_error.html',
                                       message='Год должен быть в диапазоне 2000-2025',
                                       return_url=url_for('reports_bp.view_report', type=report_type))
        if 'month' in params and params['month']:
            if params['month'] < 1 or params['month'] > 12:
                return render_template('report_error.html',
                                       message='Месяц должен быть в диапазоне 1-12',
                                       return_url=url_for('reports_bp.view_report', type=report_type))
        if 'day' in params and params['day']:
            if params['day'] < 1 or params['day'] > 31:
                return render_template('report_error.html',
                                       message='День должен быть в диапазоне 1-31',
                                       return_url=url_for('reports_bp.view_report', type=report_type))

        # Получение отчета
        result = get_report(provider, report_type, params)

        if result.status:
            if report_type == 'new_passenger_registrations':
                return render_template('view_new_passenger_registrations.html',
                                       report_data=result.data,
                                       report_type=report_type,
                                       report_config=report_config,
                                       params=params,
                                       message=result.message)
            elif report_type == 'popular_routes':
                return render_template('view_popular_routes.html',
                                       report_data=result.data,
                                       report_type=report_type,
                                       report_config=report_config,
                                       params=params,
                                       message=result.message)
        else:
            return render_template('report_error.html',
                                   message=result.message,
                                   return_url=url_for('reports_bp.view_report', type=report_type))
#1
    except Exception as e:
        return render_template('report_error.html',
                               message=f'Ошибка при загрузке отчета: {str(e)}',
                               return_url=url_for('reports_bp.view_report', type=report_type))
