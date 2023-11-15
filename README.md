Кейс компании «Ростелеком Информационные Технологии»

Тест-кесы и баг-репорты к заданию: https://docs.google.com/spreadsheets/d/1zxj9pQPaSTyrDWmLcpR8LjtxQQKKdSYtku4C-hR2n5I

Инструменты применяемые для тестирования:

    pytest: Библиотека, используемая для написания и запуска тестов.

    requests: Используется для отправки HTTP-запросов. Этот инструмент использовался для создания запросов к API на 
    сайте 1secmail.com и получения данных.

    selenium: Инструмент для автоматизации браузерного тестирования. Он предоставляет API для взаимодействия с веб-страницами, 
    выполнения действий пользователя и проверки результатов. В данном случае, он использовался для автоматизации тестирования 
    веб-страницы "Ростелеком" и взаимодействия с элементами на странице, такими как ввод имени пользователя и пароля.
    
    faker: Библиотека для генерации фейковых данных. Использовалась для создания случайных данных, таких как имя, фамилия, 
    номер телефона, логин и пароль, которые были использованы в автоматических тестах для имитации различных сценариев.

    Для получения временной электронной почты использовался сайт www.1secmail.com

Перед началом тестов необходимо указать путь к драйверу браузера в файле conftest.py

Все тесты можно запустить кнопкой Run Test слева от названия теста.