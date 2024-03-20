import tkinter as tk
from frames.users import User_Frame
from frames.auditory import Auditory_Frame
from frames.inventory import Inventory_Frame
from frames.login import Login_Frame
from frames.search_by_auditory import Search_by_auditory_Frame
from frames.search_universal import Search_universal_Frame
from frames.search_date import Search_by_date


class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Учёт")
        self.geometry("1000x600")
        self.resizable(True, True)
        self.button_activation = True

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(anchor=tk.N)

        self.login_btn = tk.Button(self.button_frame)
        self.login_btn.pack(side=tk.LEFT, pady=10)

        self.user_btn = tk.Button(self.button_frame)
        self.user_btn.pack(side=tk.LEFT, pady=10)

        self.auditory_btn = tk.Button(self.button_frame)
        self.auditory_btn.pack(side=tk.LEFT, pady=10)

        self.inventory_btn = tk.Button(self.button_frame)
        self.inventory_btn.pack(side=tk.LEFT, pady=10)

        self.search_by_auditory_btn = tk.Button(self.button_frame)
        self.search_by_auditory_btn.pack(side=tk.LEFT, pady=10)

        self.search_universal_btn = tk.Button(self.button_frame)
        self.search_universal_btn.pack(side=tk.LEFT, pady=10)

        self.search_by_date_btn = tk.Button(self.button_frame)
        self.search_by_date_btn.pack(side=tk.LEFT, pady=10)

        self.user = User_Frame(self, self.user_btn)
        self.auditory = Auditory_Frame(self, self.auditory_btn)
        self.inventory = Inventory_Frame(self, self.inventory_btn)
        self.search_by_auditory = Search_by_auditory_Frame(self, self.search_by_auditory_btn)
        self.search_universal = Search_universal_Frame(self, self.search_universal_btn)
        self.search_by_date = Search_by_date(self, self.search_by_date_btn)

        self.buttons_activation()

        self.login = Login_Frame(self, self.login_btn)

    def buttons_activation(self):
        if self.button_activation:
            self.user_btn.configure(state="disabled")
            self.auditory_btn.configure(state="disabled")
            self.inventory_btn.configure(state="disabled")
            self.search_by_auditory_btn.configure(state="disabled")
            self.search_universal_btn.configure(state="disabled")
            self.search_by_date_btn.configure(state="disabled")
        else:
            self.user_btn.configure(state="normal")
            self.auditory_btn.configure(state="normal")
            self.inventory_btn.configure(state="normal")
            self.search_by_auditory_btn.configure(state="normal")
            self.search_universal_btn.configure(state="normal")
            self.search_by_date_btn.configure(state="normal")

        self.button_activation = not self.button_activation
