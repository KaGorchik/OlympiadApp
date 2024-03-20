import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb


class Search_by_date(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Поиск по дате", command=self.frame_pack)

        # Поля ввода
        self.description_frame = tk.Frame(self)
        self.description_frame.pack(anchor=tk.N)

        self.description_frame_label = tk.Label(self.description_frame,
                                                text="Поиск по дате. Дату необходимо вводить в формате ГГГГ-ММ-ДД. \n"
                                                "Заполнять все поля не обязательно.")
        self.description_frame_label.pack()

        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.from_date_label = tk.Label(self.input_new_frame, text="С:")
        self.from_date_entry = tk.Entry(self.input_new_frame)

        self.to_date_label = tk.Label(self.input_new_frame, text="По:")
        self.to_date_entry = tk.Entry(self.input_new_frame)

        self.search_btn = tk.Button(self.input_new_frame, text="Искать", command=self.search_by_date)

        self.from_date_label.pack(side=tk.LEFT, pady=25)
        self.from_date_entry.pack(side=tk.LEFT, pady=25)

        self.to_date_label.pack(side=tk.LEFT, pady=25)
        self.to_date_entry.pack(side=tk.LEFT, pady=25)

        self.search_btn.pack(side=tk.LEFT, pady=25)

        # Таблица
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
        self.btn.configure(text="Поиск по дате", command=self.frame_pack)

    def search_by_date(self):
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()

        # Если нет даты нач
        if not from_date:
            from_date = "1000-01-01"

        try:
            # Выполнение запроса
            cursor = connection.cursor()

            # Если есть дата окончания
            if to_date:
                cursor.execute("SELECT inventory_number, description, commissioning_date "
                               "FROM inventory "
                               "WHERE commissioning_date BETWEEN %s AND %s",
                               (from_date, to_date))
            # Если нет даты окончания
            else:
                cursor.execute("SELECT inventory_number, description, commissioning_date "
                               "FROM inventory "
                               "WHERE commissioning_date >= %s",
                               (from_date,))

            inventories = cursor.fetchall()

            for row in self.tree.get_children():
                self.tree.delete(row)

            for inventory in inventories:
                self.tree.insert("", "end", values=inventory)

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при выполнении запроса: {str(e)}")