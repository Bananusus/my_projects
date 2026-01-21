# app/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash # Для хеширования паролей

# Временное хранилище пользователей
users_data = []

class User(UserMixin):
    def __init__(self, id, username, password_hash, role='user'):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role # 'user', 'admin', 'master' и т.д.

    def set_password(self, password):
        """Хеширует и сохраняет пароль."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяет, совпадает ли введенный пароль с хешем."""
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        """Проверяет, имеет ли пользователь указанную роль."""
        return self.role == role_name

    @staticmethod
    def get_user_by_username(username):
        """Находит пользователя по имени."""
        for user in users_data:
            if user.username == username:
                return user
        return None

    @staticmethod
    def get_user_by_id(user_id):
        """Находит пользователя по ID."""
        for user in users_data:
            if str(user.id) == str(user_id): # Сравниваем как строки на всякий случай
                return user
        return None

# Пример: Создадим администратора при запуске

admin_username = 'admin'
admin_password = 'admin123'
admin_user = User.get_user_by_username(admin_username)
if not admin_user:
    admin_user = User(id=1, username=admin_username, password_hash='', role='admin')
    admin_user.set_password(admin_password) # Хешируем пароль
    users_data.append(admin_user)
    print(f"Admin user '{admin_username}' created.")
else:
    print(f"Admin user '{admin_username}' already exists.")

# Пример обычного пользователя
user_username = 'user1'
user_password = 'user123'
user_user = User.get_user_by_username(user_username)
if not user_user:
    user_user = User(id=2, username=user_username, password_hash='', role='user')
    user_user.set_password(user_password)
    users_data.append(user_user)
    print(f"Regular user '{user_username}' created.")
else:
    print(f"Regular user '{user_username}' already exists.")
