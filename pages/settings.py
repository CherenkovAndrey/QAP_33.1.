from faker import Faker


fake_ru = Faker('ru_RU')
fake_firstname = fake_ru.first_name_male()
fake_lastname = fake_ru.last_name_male()
fake_phone = fake_ru.phone_number()
fake = Faker()
fake_password = fake.password()
fake_login = fake.user_name()
fake_email = fake.email()
valid_pass_reg = '$1EFAJfxfZ'
valid_email = '0elmbw1vm@icznn.com'
fake_ls = '123123123123'


def generate_string_rus(n):
    return 'Д' * n

def russian_chars():
    return 'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'

def english_chars():
    return 'abcdefghijklmnopqrstuvwxyz'

def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'

def special_chars():
   return '|\\\/!@#$%^&*()-_=+`~?"№;:[]{}'