import psycopg2

try:
    connection = psycopg2.connect(
        host='localhost',
        port='5432',
        database='Имя_Базы',
        user='Пользователь',
        password='Пароль',
    )
except psycopg2.Error as ex:
    print(f"Error: {ex}. While connecting to Database or Database not exist.")

except Exception as e:
    print(f"Error: {e}. Unexpected error in Database connect.")