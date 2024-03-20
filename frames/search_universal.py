import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb


class Search_universal_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Поиск по инвентарю", command=self.frame_pack)

        # Поля ввода
        self.description_frame = tk.Frame(self)
        self.description_frame.pack(anchor=tk.N)

        self.description_frame_label = tk.Label(
            self.description_frame, text="Универсальный поиск инвентаря, для поиска необходимо заполнить хотя бы одно "
                                         "поле. \n Поиск возможен даже если вы ввели данные не полностью, к примеру "
                                         "только начало инвентарного номера или описания. С датой это не "
                                         "работает.\n Поиск зависим от регистра!")
        self.description_frame_label.pack()

        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.inventory_number_label = tk.Label(self.input_new_frame, text="Инвентарный номер:")
        self.inventory_number_entry = tk.Entry(self.input_new_frame)

        self.description_label = tk.Label(self.input_new_frame, text="Описание:")
        self.description_entry = tk.Entry(self.input_new_frame)

        self.commissioning_date_label = tk.Label(self.input_new_frame, text="Дата эксплуатации (ГГГГ-ММ-ДД):")
        self.commissioning_date_entry = tk.Entry(self.input_new_frame)

        self.search_btn = tk.Button(self.input_new_frame, text="Искать", command=self.search_universal)

        self.inventory_number_label.pack(side=tk.LEFT, pady=25)
        self.inventory_number_entry.pack(side=tk.LEFT, pady=25)

        self.description_label.pack(side=tk.LEFT, pady=25)
        self.description_entry.pack(side=tk.LEFT, pady=25)

        self.commissioning_date_label.pack(side=tk.LEFT, pady=25)
        self.commissioning_date_entry.pack(side=tk.LEFT, pady=25)

        self.search_btn.pack(side=tk.LEFT, pady=25)

        self.tree = ttk.Treeview(self, columns=("Inventory Number", "Description", "Commissioning Date"),
                                 show="headings")
        self.tree.heading("Inventory Number", text="Инвентарный номер")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Commissioning Date", text="Дата ввода в эксплуатацию")
        self.tree.pack(expand=True, fill="both")

    def frame_pack(self):
        self.pack()
        self.parent.buttons_activation()
        self.btn.configure(text="Закрыть", command=self.frame_close, state="normal")

    def frame_close(self):
        self.pack_forget()
        self.parent.buttons_activation()
        self.btn.configure(text="Поиск по инвентарю", command=self.frame_pack)

    def search_universal(self):
        query = "SELECT inventory_number, description, commissioning_date, auditory_id FROM inventory WHERE "
        conditions = []

        # Проверка на заполненность, а также добавление запросов
        if self.inventory_number_entry.get():
            conditions.append(f"inventory_number LIKE '{self.inventory_number_entry.get()}%'")
        if self.description_entry.get():
            conditions.append(f"description LIKE '%{self.description_entry.get()}%'")
        if self.commissioning_date_entry.get():
            conditions.append(f"commissioning_date = '{self.commissioning_date_entry.get()}'")

        # Условие запроса
        if conditions:
            query += " AND ".join(conditions)
        else:
            mb.showerror("Ошибка", "Пожалуйста, заполните хотя бы одно поле для поиска.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute(query)
            inventories = cursor.fetchall()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for inventory in inventories:
                self.tree.insert("", "end", values=inventory)

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при выполнении запроса: {str(e)}")