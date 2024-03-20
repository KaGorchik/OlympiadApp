import tkinter as tk
from data_base_connect import connection
from tkinter import messagebox as mb
import hashlib


class Login_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Вход", command=self.frame_pack)

        # Поля ввода
        self.description_frame = tk.Frame(self)
        self.description_frame.pack(anchor=tk.N)

        self.description_frame_label = tk.Label(
            self.description_frame, text="Для входа необходимо ввести имя пользователя и пароль.\n" 
                                         "Все пароли хэшируются поэтому вручную добавить их в базу не получится.\n"
                                         "Если вы зашли в приложение в первый раз, после нажатия на кнопку \"Вход\" и "
                                         "введения имени и пароля,\n создается пользователь. С тем именем и паролем что "
                                         "вы ввели.\n Постарайтесь его не забыть!")
        self.description_frame_label.pack()

        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.username_label = tk.Label(self.input_new_frame, text="Имя пользователя:")
        self.username_entry = tk.Entry(self.input_new_frame)

        self.password_label = tk.Label(self.input_new_frame, text="Пароль:")
        self.password_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Вход", command=self.check_data)

        # Позиционирование
        self.username_label.pack(side=tk.LEFT, pady=25)
        self.username_entry.pack(side=tk.LEFT, pady=25)

        self.password_label.pack(side=tk.LEFT, pady=25)
        self.password_entry.pack(side=tk.LEFT, pady=25)

        self.add_data_btn.pack(side=tk.LEFT, pady=25)

    def frame_pack(self):
        self.pack()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.btn.configure(text="Вход", command=self.frame_pack)

    def check_data(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not (username and password):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Создаём таблицы если их нет
        try:
            cursor = connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password_hash VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS Auditory (
                    id SERIAL PRIMARY KEY,
                    number VARCHAR(255) NOT NULL,
                    sector VARCHAR(255) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS Inventory (
                    id SERIAL PRIMARY KEY,
                    inventory_number VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NOT NULL,
                    commissioning_date DATE,
                    auditory_id INT,
                    FOREIGN KEY (auditory_id) REFERENCES Auditory(id)
                );
            """)
            connection.commit()
        except Exception as e:
            print(e)
            mb.showerror("Ошибка", f"Ошибка при создании таблицы User: {str(e)}")

        try:
            cursor = connection.cursor()

            # Проверяем есть ли пользователи
            cursor.execute("SELECT COUNT(*) FROM Users")
            result = cursor.fetchone()[0]

            if result == 0:
                # Создаем нового пользователя
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
                connection.commit()
                mb.showinfo("Информация", "Пользователь успешно добавлен")

            else:
                # Проверяем логин и пароль пользователя
                cursor.execute("SELECT password_hash FROM Users WHERE username = %s", (username,))
                result = cursor.fetchone()

                if result is None:
                    mb.showerror("Ошибка", "Пользователь с таким именем не существует")
                    return

                stored_password_hash = result[0]
                input_password_hash = hashlib.sha256(password.encode()).hexdigest()

                if stored_password_hash != input_password_hash:
                    mb.showerror("Ошибка", "Неправильный пароль")
                    return

            mb.showinfo("Успех", "Вход выполнен успешно")
            self.pack_forget()
            self.btn.pack_forget()
            self.parent.buttons_activation()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при проверке данных: {str(e)}")