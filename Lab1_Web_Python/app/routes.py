# app/routes.py

from flask import Blueprint, request, render_template_string, render_template, redirect, url_for, make_response, g, flash, get_flashed_messages, jsonify
from flask_login import login_user, logout_user, login_required, current_user
# Импортируем новую функцию
from app.models import get_all_cars, get_car_by_id, get_cars_by_status, get_all_status, translate_status, update_car, delete_car
from app.i18n import get_text, LANGUAGES # Импортируем функции локализации
from app.user import User
from functools import wraps
from werkzeug.exceptions import abort
from flask import session
def _(key):
    # Получаем язык из g, установленный в before_request
    current_lang = getattr(g, 'language', 'ru')
    return get_text(key, current_lang)

def role_required(role_name):
    """Декоратор для проверки роли пользователя."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                # Если пользователь не аутентифицирован, перенаправляем на страницу входа
                return redirect(url_for('main.login'))
            if not current_user.has_role(role_name):
                # Если пользователь аутентифицирован, но не имеет нужной роли, возвращаем ошибку 403 (Forbidden)
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Создаем Blueprint для организации маршрутов
bp = Blueprint('main', __name__)

# --- Маршруты для отображения HTML через render_template_string (без сложных шаблонов) ---
TRANSLATE_STATUS_DICT = {
    'pending': 'В очереди',
    'in_progress': 'В ремонте',
    'ready': 'Готов'
}


@bp.route('/')
def hello_world():
    lang = g.language # Получаем текущий язык

    # Получаем счётчик посещений из сессии, если он есть, и увеличиваем его
    visit_count = session.get('visit_count', 0) + 1
    # Сохраняем обновлённое значение в сессию
    session['visit_count'] = visit_count

    response = make_response(render_template(
        'index.html',
        language=lang,
        _=_,
        username=current_user.username if current_user.is_authenticated else None,
        visit_count=visit_count
    ))
    # Если язык был передан в URL, устанавливаем cookie
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', lang, max_age=30*24*60*60) # 30 дней
    return response

@bp.route('/user/<username>')
def show_user_profile(username):
    # Отображаем профиль пользователя через render_template_string
    html_content = f'<h1 style="color: green;">Master Profile: <em>{username}</em></h1><br><a href="/">На главную</a>'
    return render_template_string(html_content)

# --- Маршруты для работы с автомобилями, использующие render_template_string с простыми шаблонами ---

# app/routes.py
@bp.route('/car/<int:car_id>')
@role_required('admin')
def car_detail(car_id):
    lang = g.language
    car = get_car_by_id(car_id)

    if car is None:
        # Локализуем сообщение об ошибке 404
        error_msg = _('error_404_message').format(car_id=car_id)
        html_content = f"""
        <html lang="{lang}">
        <head><title>{_('error_404_title')}</title></head>
        <body>
            <h2 style='color:red;'>{_('error_404_title')}</h2>
            <p>{error_msg}</p>
            <a href="/cars">{_('error_404_back_to_list')}</a> | <a href="/">{_('home_link')}</a>
        </body>
        </html>
        """
        return render_template_string(html_content, language=lang, _=_), 404

    status_russian = translate_status(car['status'])

    edit_link_html = f' <a href="/edit_car/{car["id"]}">{_("car_details_edit")}</a> |'

    # --- HTML и JavaScript для AJAX-обновления статуса ---
    ajax_status_html = f"""
        <div id="status-update-section">
            <h3>{_('car_details_status')}: <span id="current-status-display">{status_russian}</span></h3>
            <label for="status-select">{_('form_status')}</label>
            <select id="status-select" name="status-select">
                <option value="pending" {'selected' if car['status'] == 'pending' else ''}>{_('form_status_pending')}</option>
                <option value="in_progress" {'selected' if car['status'] == 'in_progress' else ''}>{_('form_status_in_progress')}</option>
                <option value="ready" {'selected' if car['status'] == 'ready' else ''}>{_('form_status_ready')}</option>
            </select>
            <button id="update-status-btn" onclick="updateStatus({car['id']})">{_('form_submit_edit')} {_('form_status')}</button>
            <div id="status-update-message" style="margin-top: 10px;"></div>
        </div>

        <script>
        function updateStatus(carId) {{
            const newStatus = document.getElementById('status-select').value;
            const messageDiv = document.getElementById('status-update-message');
            const displaySpan = document.getElementById('current-status-display');

            messageDiv.innerHTML = '<em>{_('form_success_edit')}... </em>';
            messageDiv.style.color = 'blue';

            fetch(`/api/update_status/${{carId}}`, {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    status: newStatus
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    displaySpan.textContent = data.new_status_display;
                    messageDiv.innerHTML = '<span style="color: green;">{_('form_success_edit')}</span>';
                }} else {{
                    messageDiv.innerHTML = '<span style="color: red;">Error: ' + (data.message || 'Unknown error') + '</span>';
                }}
            }})
            .catch((error) => {{
                console.error('Error:', error);
                messageDiv.innerHTML = '<span style="color: red;">Network error or invalid response.</span>';
            }});
        }}
    </script>
    """
    # --- Конец HTML и JavaScript ---

    html_content = f"""
        <!doctype html>
        <html lang="{lang}">
            <head><title>{_('car_details_title')} ID {car['id']}</title></head>
            <body>
                <h1>{_('car_details_title')}</h1>
                <ul>
                    <li><strong>{_('car_details_id')}</strong> {car['id']}</li>
                    <li><strong>{_('car_details_car')}</strong> {car['make_model_year']}</li>
                    <li><strong>{_('car_details_vin')}</strong> {car['vin']}</li>
                    <li><strong>{_('car_details_plate')}</strong> {car['plate_number']}</li>
                    <li><strong>{_('car_details_owner')}</strong> {car['owner_info']}</li>
                    <li><strong>{_('car_details_defect')}</strong> {car['defect']}</li>
                    <li><strong>{_('car_details_master')}</strong> {car['master_id']}</li>
                    <li><strong>{_('car_details_status')}</strong> {status_russian}</li>
                </ul>

                {ajax_status_html} <!-- Вставляем блок AJAX-редактирования -->

                {edit_link_html} <!-- Ссылка редактирования формы -->
                <a href="/cars">{_('car_details_back_to_list')}</a> |
                <a href="/">{_('home_link')}</a>
                 <p>
                    <a href="/car/{car['id']}?lang=ru">RU</a> |
                    <a href="/car/{car['id']}?lang=en">EN</a>
                </p>
            </body>
        </html>
        """
    response = make_response(render_template_string(html_content))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', lang, max_age=30 * 24 * 60 * 60)
    return response



@bp.route('/cars')
@login_required
def list_cars():
    filter_status_code = request.args.get('status')
    cars = get_cars_by_status(filter_status_code)
    all_status_codes = get_all_status()
    lang = g.language  # Получаем текущий язык

    # Создаем строки таблицы с локализацией
    table_rows = ""
    for car in cars:
        status_russian = translate_status(car['status'])  # Статусы мы переводим отдельно
        # Локализуем тексты действий
        confirm_msg = _('cars_table_delete_confirm').format(make_model_year=car['make_model_year'],
                                                            plate_number=car['plate_number'])
        # --- Проверка роли для кнопок действий ---
        edit_button_html = ""
        delete_button_html = ""
        if current_user.has_role('admin'):  # Только админ может редактировать/удалять
            edit_button_html = f' <a href="/edit_car/{car["id"]}">{_("cars_table_edit")}</a> |'
            delete_button_html = f"""
                    <form class="action-form" action="/delete_car/{car['id']}" method="post"
                          onsubmit="return confirm('{confirm_msg}');">
                        <button type="submit" class="action-button delete-button">{_('cars_table_delete')}</button>
                    </form>
                    """
        table_rows += f"""
        <tr>
            <td>{car['id']}</td>
            <td>{car['make_model_year']}</td>
            <td>{car['plate_number']}</td>
            <td>{car['owner_info']}</td>
            <td>{car['defect']}</td>
            <td>{status_russian}</td>
            <td>
                <a href="/car/{car['id']}">{_('cars_table_view')}</a> |
                {edit_button_html} <!-- Добавляем пробел перед кнопкой -->
                {delete_button_html}
            </td>
        </tr>
        """

    # Создаем список фильтров по статусам с локализацией
    filter_links = f'<li><a href="/cars"><strong>{_('cars_filter_all')}</strong></a></li>'
    for code in all_status_codes:
        status_name = translate_status(code)  # Переводим статус
        filter_links += f'<li><a href="/cars?status={code}">{status_name}</a></li>'

    html_content = f"""
    <!doctype html>
    <html lang="{lang}">
        <head>
            <title>{_('cars_title')}</title>
            <style>
                table, th, td {{ border: 1px solid black; border-collapse: collapse; padding: 5px; }}
                th {{ background-color: #f2f2f2; }}
                .action-form {{ display: inline; margin: 0 5px; }}
                .action-button {{ 
                    background: none;
                    border: none;
                    color: blue;
                    text-decoration: underline;
                    cursor: pointer;
                    padding: 0;
                    font: inherit;
                }}
                .action-button:hover {{ color: red; }}
                .delete-button {{ color: red; }}
                .delete-button:hover {{ color: darkred; }}
            </style>
        </head>
        <body>
            <h1>{_('cars_title')}</h1>

            <h2>{_('cars_filter_title')}</h2>
            <ul>
                {filter_links}
            </ul>

            <p><a href="/add_car">{_('cars_add_link')}</a> | <a href="/">{_('home_link')}</a></p>
            <p>
                <a href="/cars?lang=ru">RU</a> |
                <a href="/cars?lang=en">EN</a>
            </p>

            {{% if cars %}}
            <table>
                <tr>
                    <th>{_('cars_table_id')}</th>
                    <th>{_('cars_table_car')}</th>
                    <th>{_('cars_table_plate')}</th>
                    <th>{_('cars_table_owner')}</th>
                    <th>{_('cars_table_defect')}</th>
                    <th>{_('cars_table_status')}</th>
                    <th>{_('cars_table_actions')}</th>
                </tr>
                {table_rows}
            </table>
            {{% else %}}
            <p>{_('cars_no_cars')}</p>
            {{% endif %}}
            <br>
            <a href="/">{_('home_link')}</a>
        </body>
    </html>
    """

    response = make_response(render_template_string(html_content, cars=cars))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', lang, max_age=30 * 24 * 60 * 60)
    return response

# --- Маршруты для добавления автомобиля, использующие render_template для работы с файлом шаблона ---

@bp.route('/add_car', methods=['GET'])
@role_required('admin') # Только для аутентифицированных
def show_add_car_form():
    lang = g.language
    # Передаем пустые значения и локализованные тексты
    response = make_response(render_template(
        'add_car.html',
        errors=None,
        success_message=None,
        new_car=None,
        language=g.language,  # Явно передаем язык
        username=current_user.username,  # Передаем имя пользователя
        _=_
    ))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', g.language, max_age=30 * 24 * 60 * 60)
    return response

@bp.route('/add_car', methods=['POST'])
@role_required('admin')
def process_add_car_form():
    # Импортируем функцию добавления из models.py
    from app.models import add_car

    # Получаем данные из формы
    make_model_year = request.form.get('make_model_year', '').strip()
    vin = request.form.get('vin', '').strip()
    plate_number = request.form.get('plate_number', '').strip()
    owner_info = request.form.get('owner_info', '').strip() # Одно поле вместо двух
    defect = request.form.get('defect', '').strip()
    master_id_str = request.form.get('master_id', '').strip()
    status_code = request.form.get('status', '').strip() # status_code - английский

    # Вызываем функцию добавления из models.py
    # Передаем английский код статуса
    success, errors, new_car = add_car(
        make_model_year, vin, plate_number, owner_info,
        defect, master_id_str, status_code # Передаем английский код
    )

    if success:
        success_msg = _('form_success_add')
        response = make_response(
            render_template('add_car.html', errors=None, success_message=success_msg, new_car=new_car,
                            language=g.language, username=current_user.username,  _=_))
        if getattr(g, 'lang_from_url', False):
            response.set_cookie('language', g.language, max_age=30 * 24 * 60 * 60)
        return response
    else:
        response = make_response(
            render_template('add_car.html', errors=errors, success_message=None, new_car=None, language=g.language,
                            username=current_user.username,  _=_))
        return response

# Маршрут для отображения формы редактирования (GET)
@bp.route('/edit_car/<int:car_id>', methods=['GET'])
@role_required('admin')
def show_edit_car_form(car_id):
    # Получаем автомобиль по ID
    car = get_car_by_id(car_id)
    if car is None:
        # Если автомобиль не найден, возвращаем страницу ошибки 404
        return f"<h2 style='color:red;'>Ошибка 404</h2><p>Автомобиль с ID {car_id} не найден.</p><a href='/cars'>К списку автомобилей</a>", 404

    # Отображаем шаблон формы редактирования
    # Передаем данные редактируемого автомобиля и пустые ошибки/сообщения
    response = make_response(render_template(
        'edit_car.html',
        car=car,
        errors=None,
        success_message=None,
        language=g.language,
        username=current_user.username,
        _=_  # <-- Не забываем передать _
    ))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', g.language, max_age=30 * 24 * 60 * 60)
    return response

# Маршрут для обработки данных редактирования (POST)
@bp.route('/edit_car', methods=['POST'])
@role_required('admin')
def process_edit_car_form():
    # Получаем ID автомобиля из скрытого поля формы
    car_id_str = request.form.get('car_id')
    try:
        car_id = int(car_id_str)
    except (ValueError, TypeError):
        return f"<h2 style='color:red;'>Ошибка</h2><p>Некорректный ID автомобиля.</p><a href='/cars'>К списку автомобилей</a>", 400

    # Получаем данные из формы
    make_model_year = request.form.get('make_model_year', '').strip()
    vin = request.form.get('vin', '').strip()
    plate_number = request.form.get('plate_number', '').strip()
    owner_info = request.form.get('owner_info', '').strip()
    defect = request.form.get('defect', '').strip()
    master_id_str = request.form.get('master_id', '').strip()
    status_code = request.form.get('status', '').strip()

    # Вызываем функцию обновления из models.py
    success, errors = update_car(
        car_id, make_model_year, vin, plate_number, owner_info,
        defect, master_id_str, status_code
    )

    if success:
        # Если успешно, перенаправляем на страницу деталей автомобиля или списка
        return redirect(url_for('main.car_detail', car_id=car_id)) # Перенаправление на детали

    else:
        # Если ошибки, снова отображаем форму редактирования с ошибками
        # Нужно получить данные автомобиля снова для отображения в форме
        car = get_car_by_id(car_id)
        if not car:
             return f"<h2 style='color:red;'>Ошибка</h2><p>Автомобиль с ID {car_id} не найден.</p><a href='/cars'>К списку автомобилей</a>", 404
        response = make_response(render_template(
            'edit_car.html',
            car=car,
            errors=errors,
            success_message=None,
            language=g.language,
            username=current_user.username,
            _=_
        ))
        return response


# Маршрут для обработки запроса на удаление (POST)
@bp.route('/delete_car/<int:car_id>', methods=['POST'])
@role_required('admin')
def delete_car_route(car_id):
    # from app.models import delete_car # Уже импортировано или импортируйте
    deletion_success = delete_car(car_id)
    if deletion_success:
        # Перенаправляем на список автомобилей
        return redirect(url_for('main.list_cars'))
    else:
        # Можно отобразить ошибку, если автомобиль не найден
        # Но обычно просто игнорируем или показываем общее сообщение
        return redirect(url_for('main.list_cars'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    lang = g.language
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        remember_me = bool(request.form.get('remember'))

        # Найдем пользователя по имени
        user = User.get_user_by_username(username)

        # Проверим, существует ли пользователь и совпадает ли пароль
        if user and user.check_password(password):
            # Если да, аутентифицируем его
            login_user(user, remember=remember_me)

            next_page = request.args.get('next')
            # Используем url_for с указанием Blueprint
            return redirect(next_page) if next_page else redirect(url_for('main.hello_world'))
        else:
            # Если нет, покажем ошибку
            error = _('login_invalid_credentials')

    # Отобразим форму логина
    return render_template('login.html', error=error, message=None, language=lang, _=_)

@bp.route('/logout')
@login_required # Только для аутентифицированных пользователей
def logout():
    logout_user()
    # flash('Вы успешно вышли из системы.', 'message') # Опционально
    return redirect(url_for('main.hello_world'))



@bp.route('/cookies', methods=['GET', 'POST'])
def cookies_page():
    lang = g.language
    cookie_value = request.cookies.get('my_cookie', _('cookies_current_value_not_set'))

    if request.method == 'POST':
        new_cookie_value = request.form.get('cookie_value_input', '')
        # Подставляем результат _() напрямую в f-строку
        html_content = f"""
        <!doctype html>
        <html lang="{lang}">
        <head><title>{_('cookies_title')}</title></head> <!-- Подставляем локализованный заголовок -->
        <body>
            <h1>{_('cookies_title')}</h1> <!-- Подставляем локализованный заголовок -->
            <p>{_('cookies_current_value')} {cookie_value}</p> <!-- Подставляем локализованный текст и значение cookie -->
            <p>{_('cookies_new_value_set')} '{new_cookie_value}'!</p> <!-- Подставляем локализованный текст и новое значение -->
            <a href="/cookies">{_('session_refresh')}</a> | <a href="/"> {_('session_home')}</a> <!-- Подставляем локализованный текст -->
        </body>
        </html>
        """
        response = make_response(render_template_string(html_content, language=lang, _=_))
        response.set_cookie('my_cookie', new_cookie_value, max_age=300, httponly=True, samesite='Lax')
        if getattr(g, 'lang_from_url', False):
            response.set_cookie('language', lang, max_age=30*24*60*60)
        return response

    # GET запрос
    html_content = f"""
    <!doctype html>
    <html lang="{lang}">
    <head><title>{_('cookies_title')}</title></head> <!-- Подставляем локализованный заголовок -->
    <body>
        <h1>{_('cookies_title')}</h1> <!-- Подставляем локализованный заголовок -->
        <p>{_('cookies_current_value')} {cookie_value}</p> <!-- Подставляем локализованный текст и значение cookie -->
        <form method="post">
            <label for="cookie_value_input">{_('cookies_set_new')}</label> <!-- Подставляем локализованный текст -->
            <input type="text" id="cookie_value_input" name="cookie_value_input" required>
            <input type="submit" value="{_('cookies_button')}"> <!-- Подставляем локализованное значение кнопки -->
        </form>
        <br>
        <a href="/"> {_('session_home')}</a> <!-- Подставляем локализованный текст -->
    </body>
    </html>
    """
    response = make_response(render_template_string(html_content, language=lang, _=_))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', lang, max_age=30*24*60*60)
    return response

@bp.route('/session', methods=['GET', 'POST'])
def demo_session():
    lang = g.language
    session_value = session.get('my_session_data', _('session_current_value_not_set'))
    visit_count = session.get('visit_count', 0)

    if request.method == 'POST':
        new_session_value = request.form.get('session_value_input', '')
        session['my_session_data'] = new_session_value
        session['visit_count'] = visit_count + 1

        html_content = f"""
        <!doctype html>
        <html lang="{lang}">
        <head><title>{_('session_title')}</title></head> <!-- Подставляем локализованный заголовок -->
        <body>
            <h1>{_('session_title')}</h1> <!-- Подставляем локализованный заголовок -->
            <p>{_('session_previous_value')} {session_value}</p> <!-- Подставляем локализованный текст и значение -->
            <p>{_('session_new_saved')} '{new_session_value}'!</p> <!-- Подставляем локализованный текст и новое значение -->
            <p>{_('session_visit_count')} {session.get('visit_count')}</p> <!-- Подставляем локализованный текст и счётчик -->
            <a href="/session">{_('session_refresh')}</a> | <a href="/"> {_('session_home')}</a> <!-- Подставляем локализованный текст -->
        </body>
        </html>
        """
        response = make_response(render_template_string(html_content, language=lang, _=_))
        if getattr(g, 'lang_from_url', False):
            response.set_cookie('language', lang, max_age=30*24*60*60)
        return response

    # GET запрос
    session['visit_count'] = visit_count + 1

    html_content = f"""
    <!doctype html>
    <html lang="{lang}">
    <head><title>{_('session_title')}</title></head> <!-- Подставляем локализованный заголовок -->
    <body>
        <h1>{_('session_title')}</h1> <!-- Подставляем локализованный заголовок -->
        <p>{_('session_current_value')} {session_value}</p> <!-- Подставляем локализованный текст и значение -->
        <p>{_('session_visit_count')} {session.get('visit_count')}</p> <!-- Подставляем локализованный текст и счётчик -->
        <form method="post">
            <label for="session_value_input">{_('session_set_new')}</label> <!-- Подставляем локализованный текст -->
            <input type="text" id="session_value_input" name="session_value_input" required>
            <input type="submit" value="{_('session_save')}"> <!-- Подставляем локализованное значение кнопки -->
        </form>
        <br>
        <a href="/"> {_('session_home')}</a> <!-- Подставляем локализованный текст -->
    </body>
    </html>
    """
    response = make_response(render_template_string(html_content, language=lang, _=_))
    if getattr(g, 'lang_from_url', False):
        response.set_cookie('language', lang, max_age=30*24*60*60)
    return response



@bp.route('/api/update_status/<int:car_id>', methods=['POST'])
@role_required('admin') # Только администратор может изменить статус
def api_update_status(car_id):
    # Получаем новый статус из JSON-тела запроса
    # Предполагаем, что клиент отправляет JSON: {"status": "new_status_code"}
    import json
    try:
        data = request.get_json()
        if not data:
            # Если тело запроса не JSON или пустое
            return jsonify({'success': False, 'message': 'Invalid JSON data'}), 400

        new_status = data.get('status')

        # Проверяем, допустим ли новый статус
        if new_status not in ['pending', 'in_progress', 'ready']:
            return jsonify({'success': False, 'message': 'Invalid status value'}), 400

        # Найдём автомобиль по ID
        car = get_car_by_id(car_id)
        if not car:
            # Автомобиль не найден
            return jsonify({'success': False, 'message': 'Car not found'}), 404

        # Обновим статус
        car['status'] = new_status


        # Возвращаем успешный JSON-ответ
        # Также включим обновлённый русский статус для удобства обновления на клиенте
        return jsonify({
            'success': True,
            'message': 'Status updated successfully',
            'new_status_code': new_status,
            'new_status_display': translate_status(new_status) # Переведённый статус
        })

    except json.JSONDecodeError:
        # Если не удалось распарсить JSON
        return jsonify({'success': False, 'message': 'Invalid JSON format'}), 400
    except Exception as e:
        # Обработка других потенциальных ошибок
        print(f"Error updating status for car {car_id}: {e}") # Логирование ошибки
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


