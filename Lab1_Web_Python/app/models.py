# app/models.py

# Временное хранилище данных в памяти (список словарей)
# В реальном приложении здесь будет код для работы с БД
cars_data = [
    {
        "id": 1,
        "make_model_year": "Toyota Camry 2015",
        "vin": "ABC123XYZ789DEF456",
        "plate_number": "A123BC78",
        "owner_info": "Иванов Иван Иванович, +7(999)123-45-67",
        "defect": "Не заводится двигатель",
        "master_id": 101,
        "status": "in_progress" # Английский
    },
    {
        "id": 2,
        "make_model_year": "Lada Vesta 2020",
        "vin": "XYZ987CBA321FED654",
        "plate_number": "B456CС90",
        "owner_info": "Петрова Анна Сергеевна, +7(921)023-11-89",
        "defect": "Скрежет в коробке передач",
        "master_id": 102,
        "status": "pending" # Английский
    },
     {
        "id": 3,
        "make_model_year": "BMW X5 2018",
        "vin": "BMW555BMW555BMW55555",
        "plate_number": "C789АE12",
        "owner_info": "Сидоров Дмитрий Владимирович, +7(911)987-65-43",
        "defect": "Замена масла и фильтров",
        "master_id": 103,
        "status": "ready" # Английский
    }
]

# --- Добавьте эту новую функцию ---
def translate_status(status_code):
    """Преобразует английский код статуса в русское название."""
    translations = {
        'pending': 'В очереди',
        'in_progress': 'В ремонте',
        'ready': 'Готов'
    }
    # Если код не найден, возвращаем его же или какое-то значение по умолчанию
    return translations.get(status_code, status_code)
# ---


# Функция для получения всех автомобилей
def get_all_cars():
    return cars_data

# Функция для получения автомобиля по ID
def get_car_by_id(car_id):
    for car in cars_data:
        if car['id'] == car_id:
            return car
    return None # Если не найден

# Функция для фильтрации автомобилей по статусу
# (Убедитесь, что она фильтрует по английским значениям)
def get_cars_by_status(status_code):
     if status_code: # status_code - английский
         # Фильтруем по английскому коду
         return [car for car in cars_data if car['status'] == status_code]
     else:
         return cars_data # Если статус не указан, возвращаем все

# Функция для получения уникальных статусов (для фильтрации)
# (Убедитесь, что она возвращает английские значения)
def get_all_status():
    # Используем set для получения уникальных значений
    # Возвращаем английские коды
    return list(set(car['status'] for car in cars_data))

# Функция для добавления нового автомобиля
# Возвращает кортеж: (успешно_ли, список_ошибок, добавленный_автомобиль_или_None)
def add_car(make_model_year, vin, plate_number, owner_info, defect, master_id, status_code):
    errors = []

    # --- Базовая валидация ---
    if not make_model_year:
        errors.append("Марка, модель и год выпуска обязательны.")
    if not vin:
        errors.append("VIN-номер обязателен.")
    if not plate_number:
        errors.append("Гос. номер обязателен.")
    if not owner_info: # Теперь проверяем owner_info
        errors.append("Информация о владельце обязательна.")
    # Проверка статуса - теперь только английские варианты
    if status_code not in ['pending', 'in_progress', 'ready']:
        errors.append("Некорректный статус.")
    # Проверка уникальности гос. номера (простая, для демонстрации)
    if any(car['plate_number'] == plate_number for car in cars_data):
         errors.append("Автомобиль с таким гос. номером уже существует.")

    # Если есть ошибки, не добавляем
    if errors:
        return False, errors, None

    # --- Добавление ---
    # Определяем новый ID (простой способ, в реальной БД это делает СУБД)
    new_id = max((car['id'] for car in cars_data), default=0) + 1

    # Создаем новый словарь для автомобиля
    # status_code уже английский
    new_car = {
        "id": new_id,
        "make_model_year": make_model_year.strip(),
        "vin": vin.strip(),
        "plate_number": plate_number.strip(),
        "owner_info": owner_info.strip(), # Одно поле вместо двух
        "defect": defect.strip() if defect else "",
        "master_id": int(master_id) if master_id and master_id.isdigit() else None,
        "status": status_code # Сохраняем английский код
    }

    # Добавляем в список
    cars_data.append(new_car)

    return True, [], new_car




def update_car(car_id, make_model_year, vin, plate_number, owner_info, defect, master_id, status_code):

    errors = []

    # --- Базовая валидация (та же, что и в add_car) ---
    if not make_model_year:
        errors.append("Марка, модель и год выпуска обязательны.")
    if not vin:
        errors.append("VIN-номер обязателен.")
    if not plate_number:
        errors.append("Гос. номер обязателен.")
    if not owner_info:
        errors.append("Информация о владельце обязательна.")
    if status_code not in ['pending', 'in_progress', 'ready']:
        errors.append("Некорректный статус.")

    # --- Проверка уникальности гос. номера ---
    # Исключаем текущий редактируемый автомобиль из проверки
    if any(car['plate_number'] == plate_number and car['id'] != car_id for car in cars_data):
        errors.append("Автомобиль с таким гос. номером уже существует.")

    # Если есть ошибки валидации, не обновляем
    if errors:
        return False, errors

    # --- Обновление ---
    # Найти автомобиль по ID
    car_to_update = None
    for car in cars_data:
        if car['id'] == car_id:
            car_to_update = car
            break

    if not car_to_update:
        errors.append("Автомобиль не найден.")
        return False, errors

    # Обновляем поля найденного автомобиля
    car_to_update["make_model_year"] = make_model_year.strip()
    car_to_update["vin"] = vin.strip()
    car_to_update["plate_number"] = plate_number.strip()
    car_to_update["owner_info"] = owner_info.strip()
    car_to_update["defect"] = defect.strip() if defect else ""

    # Преобразуем master_id в число, если возможно
    if master_id and master_id.isdigit():
        car_to_update["master_id"] = int(master_id)
    elif master_id == "":  # Если передана пустая строка, можно установить None
        car_to_update["master_id"] = None
    else:  # Если передано что-то еще (например, буквы), оставляем старое значение или None
        pass  # Или можно добавить ошибку валидации, если это критично

    car_to_update["status"] = status_code

    return True, []

def delete_car(car_id):
    global cars_data # Необходимо, если cars_data - глобальная переменная
    # Найти индекс автомобиля по ID
    for i, car in enumerate(cars_data):
        if car['id'] == car_id:
            # Удалить автомобиль из списка
            del cars_data[i]
            return True
    return False # Автомобиль не найден
