# tests/test_models.py

import sys
import os

# Добавляем путь к директории app, чтобы можно было импортировать модули
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models import add_car, cars_data
from unittest.mock import patch

# Тест для функции add_car
class TestAddCar:
    def setup_method(self):
        """Очищаем временные данные перед каждым тестом."""
        # Сохраняем оригинальные данные
        self.original_data = cars_data.copy()
        # Очищаем список
        cars_data.clear()

    def teardown_method(self):
        """Восстанавливаем оригинальные данные после каждого теста."""
        cars_data.clear()
        cars_data.extend(self.original_data)

    def test_add_car_success(self):
        """Тест: успешное добавление автомобиля."""
        make_model_year = "Test Make Model 2023"
        vin = "TESTVIN123456789"
        plate_number = "T999TT99"
        owner_info = "Test Owner, +7(111)222-33-44"
        defect = "Test defect"
        master_id = "104"
        status_code = "pending"

        success, errors, new_car = add_car(
            make_model_year, vin, plate_number, owner_info,
            defect, master_id, status_code
        )

        assert success is True
        assert errors == []
        assert new_car is not None
        assert new_car["make_model_year"] == make_model_year
        assert new_car["vin"] == vin
        assert new_car["plate_number"] == plate_number
        assert new_car["owner_info"] == owner_info
        assert new_car["defect"] == defect
        assert new_car["master_id"] == 104
        assert new_car["status"] == status_code
        assert len(cars_data) == 1 # Проверяем, что машина добавлена в список

    def test_add_car_missing_fields(self):
        """Тест: ошибка при отсутствии обязательных полей."""
        # Проверим, что ошибка возникает, если make_model_year пустой
        success, errors, new_car = add_car(
            "", "TESTVIN123", "T111TT11", "Owner", "Defect", "104", "pending"
        )
        assert success is False
        assert "Марка, модель и год выпуска обязательны." in errors
        assert new_car is None

        # Проверим, что ошибка возникает, если vin пустой
        success, errors, new_car = add_car(
            "Make Model 2023", "", "T222TT22", "Owner", "Defect", "104", "pending"
        )
        assert success is False
        assert "VIN-номер обязателен." in errors
        assert new_car is None

        # Проверим, что ошибка возникает, если plate_number пустой
        success, errors, new_car = add_car(
            "Make Model 2023", "TESTVIN456", "", "Owner", "Defect", "104", "pending"
        )
        assert success is False
        assert "Гос. номер обязателен." in errors
        assert new_car is None

        # Проверим, что ошибка возникает, если owner_info пустой
        success, errors, new_car = add_car(
            "Make Model 2023", "TESTVIN789", "T333TT33", "", "Defect", "104", "pending"
        )
        assert success is False
        assert "Информация о владельце обязательна." in errors
        assert new_car is None

        # Проверим, что ошибка возникает, если status_code некорректный
        success, errors, new_car = add_car(
            "Make Model 2023", "TESTVIN999", "T444TT44", "Owner", "Defect", "104", "invalid_status"
        )
        assert success is False
        assert "Некорректный статус." in errors
        assert new_car is None

    def test_add_car_duplicate_plate(self):
        """Тест: ошибка при попытке добавить автомобиль с существующим гос. номером."""
        # Сначала добавим один автомобиль
        add_car("Make1", "VIN1", "PLATE1", "Owner1", "Defect1", "104", "pending")
        assert len(cars_data) == 1

        # Попробуем добавить другой автомобиль с тем же гос. номером
        success, errors, new_car = add_car(
            "Make2", "VIN2", "PLATE1", "Owner2", "Defect2", "105", "ready"
        )

        assert success is False
        assert "Автомобиль с таким гос. номером уже существует." in errors
        assert new_car is None
        assert len(cars_data) == 1 # Проверяем, что вторая машина не добавлена
