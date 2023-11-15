from pages.auth_page import *
from pages.settings import *
import pytest
import time


@pytest.mark.Authorization
@pytest.mark.Positive
def test_auth_page_email_valid(browser):
    """ Авторизация по валидным почте и паролю."""

    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(valid_pass_reg)
    time.sleep(15)    # Окно для ввода капчи.
    page.btn_click_enter()
    time.sleep(2)
    page.driver.save_screenshot('Success_Authorization.png')

    assert page.get_relative_link() == '/account_b2c/page'


@pytest.mark.Authorization
@pytest.mark.Negative
@pytest.mark.parametrize('username', [fake_phone, fake_login, fake_ls, fake_email],
                         ids=['fake phone', 'fake login', 'fake ls', 'fake_email'])
def test_auth_page_fake_phone_login_serv_account(browser, username):
    """ Авторизации по паролю и невалидным телефону, логину, лицевому счету, почте."""

    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_pass_reg)
    time.sleep(15)    # Окно для ввода капчи.
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    assert error_mess.text == 'Неверный логин или пароль'


@pytest.mark.Authorization
@pytest.mark.Negative
def test_auth_page_fake_password(browser):
    """ Авторизация по почте и невалидному паролю."""

    page = AuthPage(browser)
    page.enter_username(valid_email)
    page.enter_password(fake_password)
    time.sleep(15)    # Окно для ввода капчи.
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_FORM_ERROR)
    assert error_mess.text == 'Неверный логин или пароль'


@pytest.mark.Authorization
@pytest.mark.Negative
@pytest.mark.parametrize('username', ["12345", "123456789"],
                         ids=['5 digits', '9 digits'])
def test_auth_page_invalid_username(browser, username):
    """ Авторизация по паролю и телефону с неверным форматом."""

    page = AuthPage(browser)
    page.enter_username(username)
    page.enter_password(valid_pass_reg)
    time.sleep(15)    # Окно для ввода капчи.
    page.btn_click_enter()
    browser.implicitly_wait(10)

    error_mess = browser.find_element(*AuthLocators.AUTH_MESS_ERROR)
    assert error_mess.text == 'Неверный формат телефона'
