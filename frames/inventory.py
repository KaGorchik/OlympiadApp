import random
import string
import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb
from datetime import datetime


class Inventory_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Инвентарь", command=self.frame_pack)

        # Поля ввода
        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.number_label = tk.Label(self.input_new_frame, text="Инвентарный номер:")
        self.number_entry = tk.Entry(self.input_new_frame)

        self.description_label = tk.Label(self.input_new_frame, text="Описание:")
        self.description_entry = tk.Entry(self.input_new_frame)

        self.commissioning_date_label = tk.Label(self.input_new_frame,
                                                 text="Дата введения в эксплуатацию в формате (ГГГГ-ММ-ДД):")
        self.commissioning_date_entry = tk.Entry(self.input_new_frame)

        self.auditory_number_label = tk.Label(self.input_new_frame, text="Номер аудитории:")
        self.auditory_number_entry = tk.Entry(self.input_new_frame)

        self.auditory_sector_label = tk.Label(self.input_new_frame, text="Сектор аудитории:")
        self.auditory_sector_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Добавить", command=self.add_data)

        # Позиционирование
        self.number_label.grid(row=0, column=0, padx=5, pady=5)
        self.number_entry.grid(row=0, column=1, padx=5, pady=5)

        self.description_label.grid(row=1, column=0, padx=5, pady=5)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        self.commissioning_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.commissioning_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.auditory_number_label.grid(row=3, column=0, padx=5, pady=5)
        self.auditory_number_entry.grid(row=3, column=1, padx=5, pady=5)

        self.auditory_sector_label.grid(row=4, column=0, padx=5, pady=5)
        self.auditory_sector_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_data_btn.grid(row=5, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self, columns=("Inventory_number", "Description", "Commissioning_date",
                                                "Auditory_number", "Auditory_sector"), show="headings")

        self.tree.heading("Inventory_number", text="Инвентарный номер")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Commissioning_date", text="Дата введения в эксплуатацию")
        self.tree.heading("Auditory_number", text="Аудитория")
        self.tree.heading("Auditory_sector", text="Сектор")

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
        self.btn.configure(text="Инвентарь", command=self.frame_pack)

    def load_data(self):
        # Очистка таблицы
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Получаем данные
        cursor = connection.cursor()
        # cursor.execute("SELECT inventory_number, description, commissioning_date, auditory_id FROM inventory")
        cursor.execute("SELECT inventory_number, description, commissioning_date, Auditory.number, "
                       "Auditory.sector FROM inventory INNER JOIN Auditory ON inventory.auditory_id = Auditory.id")
        inventories = cursor.fetchall()

        # Заполняем таблицу
        for inventory in inventories:
            self.tree.insert("", "end", values=inventory)

    def add_data(self):
        inventory_number = self.number_entry.get()
        description = self.description_entry.get()
        commissioning_date = self.commissioning_date_entry.get()
        auditory_number = self.auditory_number_entry.get()
        auditory_sector = self.auditory_sector_entry.get()

        if not (inventory_number and description and commissioning_date and auditory_number and auditory_sector):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            datetime.strptime(commissioning_date, '%Y-%m-%d')
        except ValueError:
            mb.showerror("Ошибка", "Неправильный формат даты. Используйте формат yyyy-mm-dd")
            return

        # Уникальность номера
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM inventory WHERE inventory_number = %s", (inventory_number,))
        if cursor.fetchone():
            mb.showerror("Ошибка", "Инвентарный номер уже существует. Пожалуйста, используйте другой номер")
            return

        # Проверка на аудиторию
        cursor.execute("SELECT id FROM auditory WHERE number = %s AND sector = %s", (auditory_number, auditory_sector))
        auditory = cursor.fetchone()
        if not auditory:
            # Если аудитории нет
            try:
                cursor.execute("INSERT INTO auditory (number, sector) VALUES (%s, %s)",
                               (auditory_number, auditory_sector))
                connection.commit()
            except Exception as e:
                mb.showerror("Ошибка", f"Ошибка при добавлении аудитории в базу данных: {str(e)}")
                return

        # Получаем или обновляем идентификатор аудитории
        cursor.execute("SELECT id FROM auditory WHERE number = %s AND sector = %s", (auditory_number, auditory_sector))
        auditory_id = cursor.fetchone()[0]

        # Добавление в базу
        try:
            cursor.execute("INSERT INTO inventory (inventory_number, description, commissioning_date, auditory_id) "
                           "VALUES (%s, %s, %s, %s)",
                           (inventory_number, description, commissioning_date, auditory_id))
            connection.commit()
            mb.showinfo("Успешно", "Данные успешно добавлены в базу")
            self.load_data()
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при добавлении данных в базу: {str(e)}")

    def add_random_data(self):
        inventory_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        description = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        commissioning_date = f"{random.randint(2020, 2023)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
        auditory_number = ''.join(random.choices(string.digits, k=3))
        auditory_sector = random.choice("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ")

        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, inventory_number)
        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, description)
        self.commissioning_date_entry.delete(0, tk.END)
        self.commissioning_date_entry.insert(0, commissioning_date)
        self.auditory_number_entry.delete(0, tk.END)
        self.auditory_number_entry.insert(0, auditory_number)
        self.auditory_sector_entry.delete(0, tk.END)
        self.auditory_sector_entry.insert(0, auditory_sector)
        self.add_data()


