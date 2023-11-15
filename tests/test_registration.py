from pages.temporary_email import EmailRegistration
from pages.auth_page import *
from pages.settings import *
import pytest
import time


class TestRegistration:
    """ Проверка регистрации на сайте с кодом подтверждения."""

    result_email, status_email = EmailRegistration().get_api_email()  # Получение нового Email
    email_reg = result_email[0]

    @pytest.mark.Registration
    @pytest.mark.Positive
    def test_get_registration_valid(self, browser):
        """ Регистрация на сайте."""

        # Разделение email на имя и домен
        sign_at = self.email_reg.find('@')
        mail_name = self.email_reg[0:sign_at]
        mail_domain = self.email_reg[sign_at + 1:len(self.email_reg)]
        assert self.status_email == 200, 'status_email error'
        assert len(self.result_email) > 0, 'len(result_email) > 0 -> error'

        # Открытие формы регистрации
        page = AuthPage(browser)
        page.enter_reg_page()
        browser.implicitly_wait(5)
        assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
        page = RegistrationPage(browser)

        # Ввод данных для регистрации.
        page.enter_firstname(fake_firstname)  # Имя
        browser.implicitly_wait(5)
        page.enter_lastname(fake_lastname)   # Фамилия
        browser.implicitly_wait(5)
        page.enter_email(self.email_reg)  # Email
        browser.implicitly_wait(5)
        page.enter_password(fake_password)  # Пароль
        browser.implicitly_wait(5)
        page.enter_pass_conf(fake_password)  # Подтверждение пароля
        browser.implicitly_wait(5)

        page.btn_click()
        time.sleep(25)  # Ожидание писльма с подтверждением

        # Получение id письма с кодом из почтового ящика
        result_id, status_id = EmailRegistration().get_id_letter(mail_name, mail_domain)
        id_letter = result_id[0].get('id')
        assert status_id == 200, "status_id error"
        assert id_letter > 0, "id_letter > 0 error"

        # Получение кода регистрации
        result_code, status_code = EmailRegistration().get_reg_code(mail_name, mail_domain, str(id_letter))
        text_body = result_code.get('body')
        reg_code = text_body[text_body.find('Ваш код : ') + len('Ваш код : '):
                             text_body.find('Ваш код : ') + len('Ваш код : ') + 6]
        assert status_code == 200, "status_code error"
        assert reg_code != '', "reg_code != [] error"
        browser.implicitly_wait(5)
        for i in range(0, 6):
            browser.find_elements(By.XPATH, '//input[@inputmode="numeric"]')[i].send_keys(reg_code[i])
            browser.implicitly_wait(5)

        # Прохождение регистрации, открытие личного кабинета
        assert page.get_relative_link() == '/account_b2c/page', 'Регистрация НЕ пройдена'
        page.driver.save_screenshot('Success_Registration.png')

        # Сохранение Email и пароля
        page.driver.save_screenshot('Success_Registration.png')
        print(self.email_reg, fake_password)
        with open(r"../pages/Settings.py", 'r', encoding='utf8') as file:
            lines = []
            print(lines)
            for line in file.readlines():
                if 'valid_email' in line:
                    lines.append(f"valid_email = '{str(self.email_reg)}'\n")
                elif 'valid_pass_reg' in line:
                    lines.append(f"valid_pass_reg = '{fake_password}'\n")
                else:
                    lines.append(line)
        with open(r"../pages/Settings.py", 'w', encoding='utf8') as file:
            file.writelines(lines)


@pytest.mark.Registration
@pytest.mark.Negative
@pytest.mark.parametrize('symbols', ['', generate_string_rus(1), generate_string_rus(31),
                                       generate_string_rus(256), english_chars(), chinese_chars(),
                                       special_chars(), 12345],
                         ids=['empty', '1 char', '31 chars', '256 chars', 'english_chars', 'chinese_chars',
                              'special_symbols', 'number'])

def test_get_registration_invalid_format_firstname(browser, symbols):
    """ Регистрация с невалидным именем."""

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(5)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
    page = RegistrationPage(browser)

    # Ввод данных для регистрации.
    page.enter_firstname(symbols)  # Имя
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)   # Фамилия
    browser.implicitly_wait(5)
    page.enter_email(fake_email)  # Email
    browser.implicitly_wait(5)
    page.enter_password(fake_password)  # Пароль
    browser.implicitly_wait(5)
    page.enter_pass_conf(fake_password)  # Подтверждение пароля
    browser.implicitly_wait(5)

    page.btn_click()
    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.Registration
@pytest.mark.Negative
@pytest.mark.parametrize('symbols', ['', generate_string_rus(1), generate_string_rus(31),
                                      generate_string_rus(256), english_chars(), chinese_chars(),
                                      special_chars(), 12345],
                         ids=['empty', '1 char', '31 chars', '256 chars', 'english_chars', 'chinese_chars',
                              'special_symbols', 'number'])

def test_get_registration_invalid_format_lastname(browser, symbols):
    """ Регистрация с невалидной фамилией."""

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(5)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
    page = RegistrationPage(browser)

    # Ввод данных для регистрации.
    page.enter_firstname(fake_firstname)  # Имя
    browser.implicitly_wait(5)
    page.enter_lastname(symbols)   # Фамилия
    browser.implicitly_wait(5)
    page.enter_email(fake_email)  # Email
    browser.implicitly_wait(5)
    page.enter_password(fake_password)  # Пароль
    browser.implicitly_wait(5)
    page.enter_pass_conf(fake_password)  # Подтверждение пароля
    browser.implicitly_wait(5)

    page.btn_click()
    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Необходимо заполнить поле кириллицей. От 2 до 30 символов.'


@pytest.mark.Registration
@pytest.mark.Negative
@pytest.mark.parametrize('symbols', ['', '+7', '+375', '+7987654321X', '1234567890', 'exampleemail.ru',
                                   'example@', 'example@@email.ru', '@example.com'])

def test_get_registration_invalid_format_email_or_number(browser, symbols):
    """ Регистрация с невалидным форматои почты или телефона."""

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(5)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
    page = RegistrationPage(browser)

    # Ввод данных для регистрации.
    page.enter_firstname(fake_firstname)  # Имя
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)   # Фамилия
    browser.implicitly_wait(5)
    page.enter_email(symbols)  # Email
    browser.implicitly_wait(5)
    page.enter_password(fake_password)  # Пароль
    browser.implicitly_wait(5)
    page.enter_pass_conf(fake_password)  # Подтверждение пароля
    browser.implicitly_wait(5)

    page.btn_click()
    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, ' \
                              'или email в формате example@email.ru'


@pytest.mark.Registration
@pytest.mark.Negative

def test_get_registration_living_account(browser):
    """ Регистрация с указанием данных уже существующего аккаунта."""

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(5)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
    page = RegistrationPage(browser)

    # Ввод данных для регистрации.
    page.enter_firstname(fake_firstname)  # Имя
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)   # Фамилия
    browser.implicitly_wait(5)
    page.enter_email(valid_email)  # Email
    browser.implicitly_wait(5)
    page.enter_password(fake_password)  # Пароль
    browser.implicitly_wait(5)
    page.enter_pass_conf(fake_password)  # Подтверждение пароля
    browser.implicitly_wait(5)

    page.btn_click()
    card_modal_title = browser.find_element(*RegLocators.REG_CARD_MODAL)
    assert card_modal_title.text == 'Учётная запись уже существует'


@pytest.mark.Registration
@pytest.mark.Negative

def test_get_registration_diff_pass_and_pass_conf(browser):
    """ Регистрация с невалидным подтверждением пароля."""

    page = AuthPage(browser)
    page.enter_reg_page()
    browser.implicitly_wait(5)
    assert page.get_relative_link() == '/auth/realms/b2c/login-actions/registration'
    page = RegistrationPage(browser)

    # Ввод данных для регистрации.
    page.enter_firstname(fake_firstname)  # Имя
    browser.implicitly_wait(5)
    page.enter_lastname(fake_lastname)   # Фамилия
    browser.implicitly_wait(5)
    page.enter_email(fake_email)  # Email
    browser.implicitly_wait(5)
    page.enter_password(valid_pass_reg)  # Пароль
    browser.implicitly_wait(5)
    page.enter_pass_conf(fake_password)  # Подтверждение пароля
    browser.implicitly_wait(5)

    page.btn_click()
    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Пароли не совпадают'
