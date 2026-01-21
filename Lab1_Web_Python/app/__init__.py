# app/__init__.py

from flask import Flask, request, g # Добавили g для хранения данных в контексте запроса
from flask_login import LoginManager # Импортируем LoginManager
from app.i18n import get_text
def create_app():
    app = Flask(__name__)
    app.secret_key = 'secret-key'

    # Инициализируем LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    # Укажем маршрут для перенаправления неавторизованных пользователей
    login_manager.login_view = 'main.login'  # Используем Blueprint 'main' и маршрут 'login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

    @login_manager.user_loader
    def load_user(user_id):
        """Функция для загрузки пользователя из сессии."""
        from app.user import User  # Импортируем здесь, чтобы избежать циклических импортов
        return User.get_user_by_id(user_id)

    # выполняется перед каждым запросом
    @app.before_request
    def set_language():
        # Проверяем, есть ли параметр 'lang' в URL (например, ?lang=en)
        lang_param = request.args.get('lang')
        if lang_param and lang_param in ['ru', 'en']:
            # Если есть, устанавливаем его как выбранный язык
            g.language = lang_param
            # И сохраняем в cookie (на 30 дней)
            from datetime import datetime, timedelta
            expire_date = datetime.now() + timedelta(days=30)
            from flask import make_response
            # Так как before_request не возвращает response, мы не можем напрямую установить cookie здесь.
            # Мы сохраним язык в g и установим cookie позже, если нужно.
            # Пока просто запоминаем.
            g.lang_from_url = True
        else:
            # Если параметра нет, пытаемся получить язык из cookie
            lang_cookie = request.cookies.get('language')
            if lang_cookie and lang_cookie in ['ru', 'en']:
                g.language = lang_cookie
            else:
                # Если и cookie нет, используем язык по умолчанию
                g.language = 'ru' # Или можно определить из заголовков запроса request.accept_languages
            g.lang_from_url = False

    # Импортируем и регистрируем Blueprint с маршрутами
    from app import routes
    app.register_blueprint(routes.bp)

    return app
