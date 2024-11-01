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
    driver_path = "/app/chromedriver-linux64/chromedriver"
    load_dotenv("/app/data/.env")

    print("Загрузка переменных окружения...")

    # Настройки для Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--user-data-dir=/app/data/User_Data')
    chrome_options.add_argument('--profile-directory=Profile_2')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,  # Отключение уведомлений
        "profile.default_content_setting_values.popups": 2         # Отключение всплывающих окон
    })

    driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=chrome_options)
    
    # Авторизация через вк
    driver.get("https://vk.com")

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.ID, "index_email"))
        )
        element[0].send_keys(os.getenv('number'))

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(@class, 'FlatButton') and contains(@class, 'VkIdForm__signInButton')]"))
        )
        element[0].click()

        try:

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.NAME, "password"))
            )
            element[0].send_keys(os.getenv('pass'))

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiButton__content"))
            )
            element[0].click()
            
            print("Авторизация прошла успешно")
        except Exception as e:
            print("Вход по сохранённым данным")
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.ID, "otp"))
            )
            try:
                tmp_auth = mintotp.totp(os.getenv('hash_vk'))
                ttl = time_to_live(tmp_auth)
                if ttl <= 3:
                    time.sleep(6)
                    print("Ожидание для обновления кода TOTP...")
                    tmp_auth = mintotp.totp(os.getenv('hash_vk'))
            except Exception as e:
                print(f"Ошибка генерации временного кода: {e}")
                return None
            element[0].send_keys(tmp_auth)            
        except Exception as e:
            print("OTP поля нет") 

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
    except Exception as e:
        print(f"Сессия доступна или произошла ошибка при работе с WebDriver: {e}")
    
    time.sleep(5)

    driver.get("https://web.vk.me/")    
    
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiSimpleCell"))
        )
        element[1].click()

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vkuiButton__content"))
        )
        element[0].click()

        cookies = driver.get_cookies()
    except Exception as e:
        cookies = driver.get_cookies()
        print("Прошлая авторизация не прошла")

    finally:
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
        session.close()  # Закрываем сессию
