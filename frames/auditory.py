import random
import string
import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb


class Auditory_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Аудитории", command=self.frame_pack)

        # Поля ввода
        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.number_label = tk.Label(self.input_new_frame, text="Номер:")
        self.number_entry = tk.Entry(self.input_new_frame)

        self.sector_label = tk.Label(self.input_new_frame, text="Сектор:")
        self.sector_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Добавить", command=self.add_data)

        # Позиционирование
        self.number_label.pack(side=tk.LEFT, pady=25)
        self.number_entry.pack(side=tk.LEFT, pady=25)

        self.sector_label.pack(side=tk.LEFT, pady=25)
        self.sector_entry.pack(side=tk.LEFT, pady=25)

        self.add_data_btn.pack(side=tk.LEFT, pady=25)

        # Таблица
        self.tree = ttk.Treeview(self, columns=("Number", "Sector"), show="headings")
        self.tree.heading("Number", text="Номер")
        self.tree.heading("Sector", text="Сектор")
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
        self.btn.configure(text="Аудитории", command=self.frame_pack)

    def load_data(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем данные
        cursor = connection.cursor()
        cursor.execute("SELECT Number, Sector FROM auditory")
        auditoriums = cursor.fetchall()

        # Заполняем таблицу
        for auditory in auditoriums:
            self.tree.insert("", "end", values=auditory)

    def add_data(self):
        number = self.number_entry.get()
        sector = self.sector_entry.get()

        if not (number and sector):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        # Уникальность аудитории
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM auditory WHERE Number = %s AND Sector = %s", (number, sector))
            count = cursor.fetchone()[0]
            if count > 0:
                mb.showerror("Ошибка", "Аудитория с таким номером и сектором уже существует")
                return
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при проверке уникальности: {str(e)}")
            return

        # Добавление в базу
        try:
            cursor.execute("INSERT INTO auditory (Number, Sector) VALUES (%s, %s)", (number, sector))
            connection.commit()
            mb.showinfo("Успех", "Данные успешно добавлены в базу")
            self.load_data()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при добавлении данных в базу: {str(e)}")

    def add_random_data(self):
        number = ''.join(random.choices(string.digits, k=3))
        sector = random.choice("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")

        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, number)
        self.sector_entry.delete(0, tk.END)
        self.sector_entry.insert(0, sector)
        self.add_data()
