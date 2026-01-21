# app/i18n.py

# Словарь ресурсов для русского языка
RESOURCES_RU = {
    'welcome_title': 'Автосервис (СТО)',
    'welcome_message': 'Это приложение демонстрирует работу с Web-запросами в Python/Flask.',
    'nav_cars_list': 'Список автомобилей',
    'nav_add_car': 'Добавить новый автомобиль',
    'nav_user_profile': 'Пример профиля мастера',
    'home_title': 'Добро пожаловать в Автосервис!',
    'home_link': 'На главную',
    'nav_cookies': 'Куки',
    'nav_session': 'Сессия',

    # Страница списка автомобилей
    'cars_title': 'Автомобили в автосервисе',
    'cars_filter_title': 'Фильтр по статусу:',
    'cars_filter_all': 'Все',
    'cars_table_id': 'ID',
    'cars_table_car': 'Автомобиль',
    'cars_table_plate': 'Гос. номер',
    'cars_table_owner': 'Информация о владельце',
    'cars_table_defect': 'Неисправность',
    'cars_table_status': 'Статус',
    'cars_table_actions': 'Действия',
    'cars_table_view': 'Просмотр',
    'cars_table_edit': 'Редактировать',
    'cars_table_delete': 'Удалить',
    'cars_table_delete_confirm': 'Вы уверены, что хотите удалить автомобиль {make_model_year} ({plate_number})?',
    'cars_no_cars': 'Автомобили не найдены.',
    'cars_add_link': 'Добавить новый автомобиль',

    # Страница деталей автомобиля
    'car_details_title': 'Детали автомобиля',
    'car_details_id': 'ID:',
    'car_details_car': 'Автомобиль:',
    'car_details_vin': 'VIN:',
    'car_details_plate': 'Гос. номер:',
    'car_details_owner': 'Информация о владельце:',
    'car_details_defect': 'Неисправность:',
    'car_details_master': 'ID Мастера:',
    'car_details_status': 'Статус:',
    'car_details_edit': 'Редактировать',
    'car_details_back_to_list': 'Назад к списку',

    # Форма добавления/редактирования автомобиля
    'form_add_title': 'Добавить новый автомобиль в автосервис',
    'form_edit_title': 'Редактировать данные автомобиля',
    'form_make_model_year': 'Марка, модель, год выпуска:',
    'form_vin': 'VIN-номер:',
    'form_plate': 'Гос. номер:',
    'form_owner': 'Имя владельца и контакт (через запятую):',
    'form_defect': 'Описание неисправности:',
    'form_master': 'ID Мастера:',
    'form_status': 'Статус:',
    'form_status_pending': 'В очереди',
    'form_status_in_progress': 'В ремонте',
    'form_status_ready': 'Готов',
    'form_submit_add': 'Добавить автомобиль',
    'form_submit_edit': 'Сохранить изменения',
    'form_cancel': 'Отмена',
    'form_errors_title': 'Ошибки при заполнении формы:',
    'form_success_add': 'Автомобиль успешно добавлен!',
    'form_success_edit': 'Данные автомобиля успешно обновлены!',

    # Страница 404
    'error_404_title': 'Ошибка 404',
    'error_404_message': 'Автомобиль с ID {car_id} не найден.',
    'error_404_back_to_list': 'К списку автомобилей',

    # Статусы (дублируем для удобства)
    'status_pending': 'В очереди',
    'status_in_progress': 'В ремонте',
    'status_ready': 'Готов',

    # Аутентификация
    'login_title': 'Вход в систему',
    'login_header': 'Вход в систему',
    'login_username': 'Имя пользователя:',
    'login_password': 'Пароль:',
    'login_button': 'Войти',
    'login_invalid_credentials': 'Неверное имя пользователя или пароль.',
    'login_success': 'Вы успешно вошли в систему.',
    'logout_link': 'Выйти',

    'login_remember_me': 'Запомнить меня',

    # Страница Cookies
    'cookies_title': 'Куки',
    'cookies_current_value': 'Текущее значение куки:',
    'cookies_set_new': 'Установить новое значение куки:',
    'cookies_button': 'Установить куки',

    # Страница Session
    'session_title': 'Сессия',
    'session_previous_value': 'Предыдущее значение сессии:',
    'session_new_saved': 'Новое значение сессии сохранено!',
    'session_visit_count': 'Количество посещений (этой сессии):',
    'session_refresh': 'Обновить',
    'session_home': 'На главную',
    'cookies_current_value_not_set': 'Куки не установлено',
    'session_current_value_not_set': 'Данные сессии не установлены',
    'session_current_value': 'Текущее значение сессии:',
    'session_set_new': 'Установить новое значение сессии:',
    'session_save': 'Сохранить в сессию',
    'total_visits_this_session': 'Всего посещений (этой сессии):',
}

# Словарь ресурсов для английского языка
RESOURCES_EN = {
    'welcome_title': 'Auto Service (STO)',
    'welcome_message': 'This application demonstrates working with Web requests in Python/Flask.',
    'nav_cars_list': 'Cars List',
    'nav_add_car': 'Add New Car',
    'nav_user_profile': 'Master Profile Example',
    'home_title': 'Welcome to Auto Service!',
    'home_link': 'Home',
    'nav_cookies': 'Cookies',
    'nav_session': 'Session',

    # Страница списка автомобилей
    'cars_title': 'Cars in Auto Service',
    'cars_filter_title': 'Filter by Status:',
    'cars_filter_all': 'All',
    'cars_table_id': 'ID',
    'cars_table_car': 'Car',
    'cars_table_plate': 'Plate Number',
    'cars_table_owner': 'Owner Info',
    'cars_table_defect': 'Defect',
    'cars_table_status': 'Status',
    'cars_table_actions': 'Actions',
    'cars_table_view': 'View',
    'cars_table_edit': 'Edit',
    'cars_table_delete': 'Delete',
    'cars_table_delete_confirm': 'Are you sure you want to delete car {make_model_year} ({plate_number})?',
    'cars_no_cars': 'No cars found.',
    'cars_add_link': 'Add New Car',

    # Страница деталей автомобиля
    'car_details_title': 'Car Details',
    'car_details_id': 'ID:',
    'car_details_car': 'Car:',
    'car_details_vin': 'VIN:',
    'car_details_plate': 'Plate Number:',
    'car_details_owner': 'Owner Info:',
    'car_details_defect': 'Defect:',
    'car_details_master': 'Master ID:',
    'car_details_status': 'Status:',
    'car_details_edit': 'Edit',
    'car_details_back_to_list': 'Back to List',

    # Форма добавления/редактирования автомобиля
    'form_add_title': 'Add New Car to Auto Service',
    'form_edit_title': 'Edit Car Details',
    'form_make_model_year': 'Make, Model, Year:',
    'form_vin': 'VIN Number:',
    'form_plate': 'Plate Number:',
    'form_owner': 'Owner Name and Contact (comma separated):',
    'form_defect': 'Defect Description:',
    'form_master': 'Master ID:',
    'form_status': 'Status:',
    'form_status_pending': 'Pending',
    'form_status_in_progress': 'In Progress',
    'form_status_ready': 'Ready',
    'form_submit_add': 'Add Car',
    'form_submit_edit': 'Save Changes',
    'form_cancel': 'Cancel',
    'form_errors_title': 'Form Validation Errors:',
    'form_success_add': 'Car added successfully!',
    'form_success_edit': 'Car details updated successfully!',

    # Страница 404
    'error_404_title': 'Error 404',
    'error_404_message': 'Car with ID {car_id} not found.',
    'error_404_back_to_list': 'Back to Cars List',

    # Статусы
    'status_pending': 'Pending',
    'status_in_progress': 'In Progress',
    'status_ready': 'Ready',
    # Аутентификация
    'login_title': 'Login',
    'login_header': 'Login',
    'login_username': 'Username:',
    'login_password': 'Password:',
    'login_button': 'Login',
    'login_invalid_credentials': 'Invalid username or password.',
    'login_success': 'You have successfully logged in.',
    'logout_link': 'Logout',

    'login_remember_me': 'Remember me',

    # Cookies page
    'cookies_title': 'Cookies',
    'cookies_current_value': 'Current value of cookie:',
    'cookies_set_new': 'Set new cookie value:',
    'cookies_button': 'Set Cookie',

    # Session page
    'session_title': 'Session',
    'session_previous_value': 'Previous session value was:',
    'session_new_saved': 'New session value has been saved!',
    'session_visit_count': 'Visit count (for this session):',
    'session_refresh': 'Refresh',
    'session_home': 'Home',
    'cookies_current_value_not_set': 'Cookie not set yet',
    'session_current_value_not_set': 'Session data not set yet',
    'session_current_value': 'Current session value:',
    'session_set_new': 'Set new session value:',
    'session_save': 'Save to Session',
    'total_visits_this_session': 'Total visits (this session):',
}

# Словарь, содержащий все словари ресурсов
LANGUAGES = {
    'ru': RESOURCES_RU,
    'en': RESOURCES_EN
}

# Функция для получения перевода по ключу и языку
def get_text(key, language='ru'):
    """Получает текст по ключу для указанного языка."""
    resources = LANGUAGES.get(language, RESOURCES_RU) # По умолчанию русский
    return resources.get(key, f'[{key}]') # Если ключ не найден, возвращаем его в скобках
