import mintotp
import os
import requests
import time
import json
from dotenv import load_dotenv, set_key
from methods.totp_check import time_to_live
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_vk_token():
    driver_path = "./chromedriver-win64/chromedriver.exe"

    # Загрузка переменных окружения
    load_dotenv()

    # Генерация временного кода
    try:
        tmp_auth = mintotp.totp(os.getenv('hash_vk'))
    except Exception as e:
        print(f"Ошибка генерации временного кода: {e}")
        return None

    # Проверка времени жизни кода
    ttl = time_to_live(tmp_auth)
    if ttl <= 5:
        print("Ожидание для обновления кода TOTP...")
        time.sleep(8)
        tmp_auth = mintotp.totp(os.getenv('hash_vk'))

    # Настройки для Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--no-first-run')

    try:
        # Запуск Chrome
        driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=chrome_options)
        driver.get("https://web.vk.me/")

        # Выполнение шагов авторизации
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiSimpleCell"))
        )
        element[1].click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "login"))
        )
        element[0].send_keys(os.getenv('number'))

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiButton__content"))
        )
        element[0].click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "password"))
        )
        element[0].send_keys(os.getenv('pass'))

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiButton__content"))
        )
        element[0].click()

        # Ввод временного кода TOTP
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.NAME, "otp"))
        )
        element[0].send_keys(tmp_auth)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiButton__content"))
        )
        element[0].click()

        # Завершаем авторизацию
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='vkc__AuthSimpleScreen__bottom']//button//span[contains(text(), 'Продолжить')]"))
        )
        button.click()

        # Небольшая задержка перед получением cookies
        time.sleep(2)

        # Получение всех cookies после авторизации
        cookies = driver.get_cookies()

    except Exception as e:
        print(f"Ошибка при работе с WebDriver: {e}")
        return None
    finally:
        # Завершение сессии и закрытие браузера
        driver.quit()  # Закрытие браузера

    # Преобразование cookies в формат, подходящий для requests
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    # Выполнение POST-запроса
    try:
        url = "https://web.vk.me/?act=web_token&app_id=8202606&v=5.241"
        response = session.post(url)

        if response.status_code == 200:
            data_tokens = response.text
            tokens_list = json.loads(data_tokens)
            print("Полученные данные токенов:", tokens_list)

            # Проверка наличия второго токена
            if len(tokens_list) > 1:
                second_access_token = tokens_list[1]['access_token']
                set_key(dotenv_path=".env", key_to_set="token", value_to_set=f"{second_access_token}")
                return second_access_token
            else:
                print("Не удалось найти второй access_token, возможно структура ответа изменилась")
                return None
        else:
            print(f"Ошибка выполнения POST-запроса, код ошибки: {response.status_code}")
            return None

    except Exception as e:
        print(f"Ошибка при выполнении запроса к API: {e}")
        return None
    finally:
        # Очистка сессии requests
        session.cookies.clear()  # Очищаем cookies в сессии
        session.close()  # Закрываем сессию
