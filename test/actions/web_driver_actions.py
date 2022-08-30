import os
import tempfile
import uuid

from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# Ждём окончания процесса загрузки
def wait_loading_indicator(web_driver: WebDriver):
    WebDriverWait(web_driver, 30) \
        .until(expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, ".spinner-border")))


def wait_no_errors_in_toast_present(web_driver: WebDriver, wait_seconds: int, error_message: str):
    # Ждём, что не будет ошибки
    expected_error = None
    try:
        WebDriverWait(web_driver, wait_seconds) \
            .until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, ".toast-header")))
    except TimeoutException as e:
        expected_error = e

    # Должна быть ошибка ожидания
    assert expected_error is not None, error_message


class WebDriverActions:
    web_driver = None

    def __init__(self, web_driver: WebDriver):
        self.web_driver = web_driver

    def open_base_url(self):
        self.web_driver.get("http://localhost")

    def register_user(self, username: str, password: str):
        self.open_base_url()

        # Панель регистрации
        self.web_driver.find_element(By.LINK_TEXT, "Регистрация здесь").click()

        random_uuid = str(uuid.uuid4())
        # Имя
        self.web_driver.find_element(By.CSS_SELECTOR, ".forms-inputs:nth-child(2) > .form-control").send_keys(username)
        # Пароль
        self.web_driver.find_element(By.CSS_SELECTOR, ".forms-inputs:nth-child(3) > .form-control").send_keys(password)
        self.web_driver.find_element(By.CSS_SELECTOR, ".forms-inputs:nth-child(4) > .form-control").send_keys(password)

        # Регистрация
        self.web_driver.find_element(By.CSS_SELECTOR, ".btn").click()

        # Ждём выполнения запроса на регистрацию
        wait_loading_indicator(self.web_driver)

        # Ждём, что не будет ошибки авторизации
        wait_no_errors_in_toast_present(self.web_driver, 3, 'Не удалось зарегистрировать пользователя')

    def login(self, username: str, password: str):
        self.open_base_url()

        # имя
        self.web_driver.find_element(By.CSS_SELECTOR, ".forms-inputs:nth-child(2) > .form-control").send_keys(username)
        # пароль
        self.web_driver.find_element(By.CSS_SELECTOR, ".forms-inputs:nth-child(3) > .form-control").send_keys(password)

        # авторизация
        self.web_driver.find_element(By.CSS_SELECTOR, ".btn").click()
        # Ждём выполнения запроса на авторизацию
        wait_loading_indicator(self.web_driver)

        # Ждём загрузки главной страницы
        WebDriverWait(self.web_driver, 10) \
            .until(expected_conditions.element_to_be_clickable((By.LINK_TEXT, 'Меню')))

        # Ждём загрузки данных на странице
        wait_loading_indicator(self.web_driver)

        # Должна быть кнопка создания новой заметки
        WebDriverWait(self.web_driver, 10) \
            .until(expected_conditions
                   .element_to_be_clickable((By.XPATH, "//button[contains(text(),'Новая заметка')]")))

    def logout(self):
        self.open_base_url()

        # Открытие меню пользователя
        self.web_driver.find_element(By.CSS_SELECTOR, ".mx-1").click()
        # Выход
        self.web_driver.find_element(By.LINK_TEXT, "Выход").click()

        # Открывается страница логина
        WebDriverWait(self.web_driver, 30) \
            .until(expected_conditions
                   .element_to_be_clickable((By.XPATH, "//button[contains(text(),'Вход')]")))

        # Ждём, что не будет ошибки авторизации
        wait_no_errors_in_toast_present(self.web_driver, 3, 'При выходе возникла ошибка')

    def create_new_note(self, note_title):
        self.open_base_url()
        wait_loading_indicator(self.web_driver)

        # Создаём темповый файл
        temp_file_descriptor, temp_file_path = tempfile.mkstemp(suffix='.tmp')
        try:
            with os.fdopen(temp_file_descriptor, 'w') as open_file:
                open_file.write('hello')

            # Нажимаем на создание новой заметки
            self.web_driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
            # Титул заметки
            self.web_driver.find_element(By.ID, "inputTitle").send_keys(note_title)
            self.web_driver.find_element(By.ID, "inputText").send_keys(note_title)

            # Открываем модалку добавления файла
            self.web_driver.find_element(By.CSS_SELECTOR, ".bi").click()

            # Модалка добавления файла видима пользователю
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .visibility_of_element_located((By.XPATH, "//h5[contains(text(),'Добавление файла')]")))

            # Добавляем файл
            self.web_driver.find_element(By.CSS_SELECTOR, ".modal-body > .form-control").send_keys(temp_file_path)
            # Кнопка сохранения файла должна быть активна
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .element_to_be_clickable((By.CSS_SELECTOR, "#addFileModal .btn-primary")))
            # Сохраняем добавленный файл
            self.web_driver.find_element(By.CSS_SELECTOR, "#addFileModal .btn-primary").click()

            # Сохраняем документ
            self.web_driver.find_element(By.XPATH, "//button[contains(text(),'Сохранить и выйти')]").click()

            # Ждём окончания сохранения
            wait_loading_indicator(self.web_driver)
            # Не должно быть ошибок сохранения
            wait_no_errors_in_toast_present(self.web_driver, 3, 'При сохранении заметки возникли ошибки')
            # Должна быть кнопка создания новой заметки
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .element_to_be_clickable((By.XPATH, "//button[contains(text(),'Новая заметка')]")))

        finally:
            os.unlink(temp_file_path)

    def edit_note(self, note_title, new_note_title):
        self.open_base_url()
        wait_loading_indicator(self.web_driver)

        # Должна быть видна заметка с текстом
        WebDriverWait(self.web_driver, 10) \
            .until(expected_conditions
                   .visibility_of_element_located((By.XPATH, "//p[contains(text(),'" + note_title[:6] + "')]")))

        # Создаём темповый файл
        temp_file_descriptor, temp_file_path = tempfile.mkstemp(suffix='.tmp')
        try:
            with os.fdopen(temp_file_descriptor, 'w') as open_file:
                open_file.write('hello')

            # Нажимаем на открытие заметки
            self.web_driver.find_element(By.CSS_SELECTOR, ".btn-sm").click()
            wait_loading_indicator(self.web_driver)
            # Титул заметки
            self.web_driver.find_element(By.ID, "inputTitle").send_keys(new_note_title)
            self.web_driver.find_element(By.ID, "inputText").send_keys(new_note_title)

            # Открываем модалку добавления файла
            self.web_driver.find_element(By.CSS_SELECTOR, ".bi").click()

            # Модалка добавления файла видима пользователю
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .visibility_of_element_located((By.XPATH, "//h5[contains(text(),'Добавление файла')]")))

            # Добавляем файл
            self.web_driver.find_element(By.CSS_SELECTOR, ".modal-body > .form-control").send_keys(temp_file_path)
            # Кнопка сохранения файла должна быть активна
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .element_to_be_clickable((By.CSS_SELECTOR, "#addFileModal .btn-primary")))
            # Сохраняем добавленный файл
            self.web_driver.find_element(By.CSS_SELECTOR, "#addFileModal .btn-primary").click()

            # Сохраняем документ
            self.web_driver.find_element(By.XPATH, "//button[contains(text(),'Сохранить и выйти')]").click()

            # Ждём окончания сохранения
            wait_loading_indicator(self.web_driver)
            # Не должно быть ошибок сохранения
            wait_no_errors_in_toast_present(self.web_driver, 3, 'При сохранении заметки возникли ошибки')
            # Должна быть кнопка создания новой заметки
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .element_to_be_clickable((By.XPATH, "//button[contains(text(),'Новая заметка')]")))

            # Должна быть видна заметка с новым текстом
            WebDriverWait(self.web_driver, 10) \
                .until(expected_conditions
                       .visibility_of_element_located((By.XPATH, "//p[contains(text(),'" + new_note_title[:6] + "')]")))

        finally:
            os.unlink(temp_file_path)
