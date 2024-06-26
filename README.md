# Инструкция по установке и использованию программы

## Требования к программному обеспечению

Для работы программы необходимо установить следующее программное обеспечение:

1. **Python 3**: Программа написана на Python 3. Установщик Python можно загрузить с [официального сайта Python](https://www.python.org/downloads/).
   
2. **PostgreSQL**: Для хранения данных используется СУБД PostgreSQL. Вы можете загрузить и установить PostgreSQL с [официального сайта PostgreSQL](https://www.postgresql.org/download/).

3. **tkinter**: Встроенная библиотека Python. По умолчанию должна всегда быть установленна но иногда отсутствует. Без неё запуск будет невозможен.

Код программы и инструкцию можно посмотреть (*крайне желательно*)на [аккаунте GitHub](https://github.com/KaGorchik/OlympiadApp).

## Подключение к базе данных
В файле **data_base_connect.py** укажите данные для подключения:
```bash
connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='Имя_Базы',
    user='Пользователь',
    password='Пароль',
```
Создать базу данных и именем, пользователем, и паролем который вы указали.
Сделать это можно при помощи программ "**DBeaver**" или "**pgAdmin 4**"

## Установка зависимостей
Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv # Или
python3 -m venv venv
```

Для установки зависимостей программы выполните следующие команды:
```bash
pip install psycopg2==2.9.9
```

## Запуск программы
После активации виртуального окружения запустите файл **main.py**:
```bash
python main.py # Или
python3 main.py
```

## Использованное ПО
1. **Python 3.9.12**
2. Библиотека Python **tkinter==8.6.12**
3. Библиотека Python **psycopg2==2.9.9**
4. **PostgreSQL 15.3**, compiled by Visual C++ build 1914, 64-bit
5. **DBeaver 23.1.0**
6. **Microsoft Windows 10 Pro** версии 22H2 64-bit
7. **PyCharm 2022.2 Professional**
