# Проект “Парсер вакансий с БД ”

## Краткое описание

Проект, который позволяет получать информацию о вакансиях с платформы hh, загружает в базу данных и осуществлять запросы к базе данных. Проект выполнен на Windows. Создан с использованием Python и postgreSQL. Подключение к API платформы hh.ru осуществляется с помощью библиотеки requests. 
Проект содержит:
1. Модуль requests_classes.py, позволяющий получить данные с сайта через request и API сайта.
2. functions.py с функциями для составления списка данных, необходимых для внесения в БД
3. Модуль db_manager_class.py для подключения к БД и взаимодействиям с ней
4. user_interaction.py с функцией для работы с БД.

## Инструкция по запуску

1. Установите зависимости проекта, указанные в файле requiments.txt
2. Создайте файл .env с данными для подключения к БД.
3. Запустите файл main.py и вводите запрашиваемые данные с соблюдением предложенного формата ответа (если есть).

## Технологии в проекте (стек)

* Python 3.11
* PostgreSQL
* Requests
* Pytest
