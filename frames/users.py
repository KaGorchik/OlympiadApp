import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb
import hashlib
import random
import string


class User_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Пользователи", command=self.frame_pack)

        # Поля ввода
        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.username_label = tk.Label(self.input_new_frame, text="Имя пользователя:")
        self.username_entry = tk.Entry(self.input_new_frame)

        self.password_label = tk.Label(self.input_new_frame, text="Пароль:")
        self.password_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Добавить", command=self.add_data)

        # Позиционирование
        self.username_label.pack(side=tk.LEFT, pady=25)
        self.username_entry.pack(side=tk.LEFT, pady=25)

        self.password_label.pack(side=tk.LEFT, pady=25)
        self.password_entry.pack(side=tk.LEFT, pady=25)

        self.add_data_btn.pack(side=tk.LEFT, pady=25)

        # Таблица
        self.tree = ttk.Treeview(self, columns=("Username", "Password"), show="headings")
        self.tree.heading("Username", text="Имя пользователя")
        self.tree.heading("Password", text="Пароль")
        self.tree.pack(expand=True, fill="both")

        self.add_random_data_btn = tk.Button(self, text="Добавить случайные данные (Для проверки работы).",
                                             command=self.add_random_data)
        self.add_random_data_btn.pack()

    def frame_pack(self):
        self.pack()
        self.load_data()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Пользователи", command=self.frame_pack)

    def load_data(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем данные
        cursor = connection.cursor()
        cursor.execute("SELECT username, password_hash FROM Users")
        users = cursor.fetchall()

        # Заполняем таблицу
        for user in users:
            self.tree.insert("", "end", values=user)

    def add_data(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not (username and password):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Хеширование пароля
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Добавление в базу
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
            connection.commit()
            mb.showinfo("Успех", "Данные успешно добавлены в базу")
            self.load_data()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при добавлении данных в базу: {str(e)}")

    def add_random_data(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.add_data()
