import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get('https://petfriends.skillfactory.ru/login')

    # Явное ожидание для полей формы
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'email'))
    )

    driver.find_element(By.ID, 'email').send_keys('test666@gmail.com')
    driver.find_element(By.ID, 'pass').send_keys('12345678qwe')
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Явное ожидание заголовка
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'PetFriends')
    )

    # Переход на страницу питомцев
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@href="/my_pets"]'))
    ).click()

    # Явное ожидание загрузки страницы с питомцами
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'all_my_pets'))
    )

    yield driver
    driver.quit()

# 1.Присутствуют все питомцы.
def test_check_pets_users(driver):
    # Явное ожидание для статистики
    stats_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='task3 fill']//div[contains(@class, 'col-sm-4 left')]"))
    )

    stats_text = stats_element.text
    pets_number = int(stats_text.split('Питомцев: ')[1].split('\n')[0])

    # Явное ожидание для строк таблицы
    rows_pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#all_my_pets table tbody tr"))
    )

    assert pets_number == len(rows_pets), f"Ожидалось {pets_number} питомцев, найдено {len(rows_pets)}"


# 2.Хотя бы у половины питомцев есть фото.
def test_photos_of_users_pets(driver):
    # Явное ожидание для изображений
    images = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#all_my_pets table tbody tr th img"))
    )

    photo = 0
    for image in images:
        if image.get_attribute('src') and image.get_attribute('src') != '':
            photo += 1

    # Проверка: хотя бы у половины питомцев есть фото
    assert photo >= len(images) / 2, f"Фото есть только у {photo} из {len(images)} питомцев"

# 3.У всех питомцев есть имя, возраст и порода.
def test_name_age_breed(driver):
    # Явное ожидание для строк таблицы
    rows_pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#all_my_pets table tbody tr"))
    )

    names, breeds, ages = [], [], []

    for row in rows_pets:
        cells = row.find_elements(By.TAG_NAME, "td")

        # Проверяем что есть достаточно ячеек
        if len(cells) >= 3:
            if cells[0].text.strip():
                names.append(cells[0].text.strip())
            if cells[1].text.strip():
                breeds.append(cells[1].text.strip())
            if cells[2].text.strip():
                ages.append(cells[2].text.strip())

    print(f'Количество имен: {len(names)}, пород: {len(breeds)}, возрастов: {len(ages)}')
    assert len(names) == len(rows_pets) and len(breeds) == len(rows_pets) and len(ages) == len(rows_pets)


# 4.У всех питомцев разные имена.
def test_names_pets(driver):
    # Явное ожидание для имен
    names_pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]'))
    )

    names = [name.text.strip() for name in names_pets if name.text.strip()]
    print(f"Имена питомцев: {names}")
    assert len(names) == len(set(names)), f"Есть повторяющиеся имена: {[n for n in names if names.count(n) > 1]}"


# 5.В списке нет повторяющихся питомцев.
def test_duplicates_pets(driver):
    # Явное ожидание для строк таблицы
    pets = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr'))
    )

    pets_data = []
    for pet in pets:
        if pet.text.strip():
            # Берем только текст из ячеек (имя, порода, возраст)
            cells = pet.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                pet_info = (cells[0].text.strip(), cells[1].text.strip(), cells[2].text.strip())
                pets_data.append(pet_info)

    assert len(pets_data) == len(set(pets_data)), "Есть повторяющиеся карточки питомцев!"


# python -m pytest test_petfriends_30_3_1.py -v
