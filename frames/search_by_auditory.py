import tkinter as tk
from tkinter import ttk
from data_base_connect import connection
from tkinter import messagebox as mb


class Search_by_auditory_Frame(tk.Frame):
    def __init__(self, parent, btn):
        super().__init__(parent)
        self.parent = parent
        self.btn = btn
        self.btn.configure(text="Поиск по аудитории", command=self.frame_pack)

        self.input_new_frame = tk.Frame(self)
        self.input_new_frame.pack(anchor=tk.N)

        self.number_label = tk.Label(self.input_new_frame, text="Номер:")
        self.number_entry = tk.Entry(self.input_new_frame)

        self.sector_label = tk.Label(self.input_new_frame, text="Сектор:")
        self.sector_entry = tk.Entry(self.input_new_frame)

        self.add_data_btn = tk.Button(self.input_new_frame, text="Искать", command=self.search_by_auditory)

        self.number_label.pack(side=tk.LEFT, pady=25)
        self.number_entry.pack(side=tk.LEFT, pady=25)

        self.sector_label.pack(side=tk.LEFT, pady=25)
        self.sector_entry.pack(side=tk.LEFT, pady=25)

        self.add_data_btn.pack(side=tk.LEFT, pady=25)

        # Таблица для отображения результатов
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
        self.btn.configure(text="Поиск по аудитории", command=self.frame_pack)

    def search_by_auditory(self):
        number = self.number_entry.get()
        sector = self.sector_entry.get()

        if not (number and sector):
            mb.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            # поиск по аудитории
            cursor = connection.cursor()
            cursor.execute("SELECT inventory_number, description, commissioning_date FROM inventory "
                           "INNER JOIN Auditory ON inventory.auditory_id = Auditory.id "
                           "WHERE Auditory.number = %s AND Auditory.sector = %s",
                           (number, sector))
            result = cursor.fetchall()

            self.clear_table()

            for row in result:
                self.tree.insert("", "end", values=row)

        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка при выполнении запроса: {str(e)}")

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
