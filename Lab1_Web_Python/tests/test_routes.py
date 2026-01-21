# tests/test_routes.py

import sys
import os
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import cars_data
from app.user import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

class TestProcessAddCarForm:

    def setup_method(self):
        self.original_data = cars_data.copy()
        cars_data.clear()

    def teardown_method(self):
        cars_data.clear()
        cars_data.extend(self.original_data)

    # Тест: успешное добавление через маршрут (имитация входа администратора)
    def test_process_add_car_form_success(self, client):
        form_data = {
            'make_model_year': 'Test Make Model 2024',
            'vin': 'TESTVIN987654321',
            'plate_number': 'T888TT88',
            'owner_info': 'Test Owner, +7(000)111-22-33',
            'defect': 'Test defect for route',
            'master_id': '106',
            'status': 'in_progress'
        }

        # --- ИМИТАЦИЯ ВХОДА КАК АДМИНИСТРАТОР ---
        admin_user_id = 1


        # Создадим тестовый пользовательский объект
        mock_admin_user = User(id=admin_user_id, username='admin', password_hash='...', role='admin')
        # Заглушим функцию `load_user`, чтобы она возвращала нашего администратора
        with patch('app.user.User.get_user_by_id', return_value=mock_admin_user):


            # Данные для логина
            login_data = {
                'username': 'admin',
                'password': 'admin123'
            }

            # Отправляем POST-запрос на /login
            login_response = client.post('/login', data=login_data, follow_redirects=True)

            assert login_response.status_code == 200


            # Теперь отправляем POST-запрос на /add_car
            # Создаем mock-объект для функции add_car
            mock_add_result = (True, [], {'id': 999, 'make_model_year': form_data['make_model_year'], 'plate_number': form_data['plate_number']})

            with patch('app.models.add_car', return_value=mock_add_result) as mock_add_func:
                response = client.post('/add_car', data=form_data, follow_redirects=True)

                # Проверяем, что запрос к add_car был сделан с правильными аргументами
                mock_add_func.assert_called_once_with(
                    form_data['make_model_year'], form_data['vin'], form_data['plate_number'],
                    form_data['owner_info'], form_data['defect'], form_data['master_id'], form_data['status']
                )

                assert response.status_code == 200 # Проверяем, что маршрут отработал без ошибки 500


    # Тест: ошибка валидации через маршрут (имитация входа администратора)
    def test_process_add_car_form_validation_error(self, client):
        form_data = {
            'make_model_year': '', # Ошибка
            'vin': 'TESTVIN987654322',
            'plate_number': 'T777TT77',
            'owner_info': 'Test Owner2, +7(000)111-22-34',
            'defect': 'Another test defect',
            'master_id': '107',
            'status': 'ready'
        }


        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        client.post('/login', data=login_data, follow_redirects=True)

        mock_add_result = (False, ["Марка, модель и год выпуска обязательны."], None)

        with patch('app.models.add_car', return_value=mock_add_result) as mock_add_func:
            response = client.post('/add_car', data=form_data, follow_redirects=True)

            # Проверяем, что запрос к add_car был сделан
            mock_add_func.assert_called_once()

            # Проверяем, что ответ 200
            assert response.status_code == 200
