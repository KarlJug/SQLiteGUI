import tkinter as tk
from tkinter import ttk
from DB.QueryDAO import QueryDAO


class Add:
    queryDAO = QueryDAO()

    def __init__(self, master, QueryDAO):
        self.master = master
        self.queryDAO = QueryDAO
        self.entries = []  # holds entry widgets from add_window()


    def add_window(self):
        add_window = tk.Toplevel(self.master)
        add_window.title("Add a new entry")

        middle_frame = ttk.Frame(add_window)
        name_frame = ttk.Frame(middle_frame)
        input_frame = ttk.Frame(middle_frame)
        submit_frame = ttk.Frame(add_window)

        # label
        label_top = tk.Label(add_window, text="Lisage andmebaasi uued andmed")
        label_top.pack(pady=5)

        # input
        print(self.queryDAO.selected_column_names_no_id)
        for i in range(len(self.queryDAO.selected_column_names_no_id)):
            label = tk.Label(name_frame, text=self.queryDAO.selected_column_names_no_id[i])
            label.pack(pady=3)

            entry = tk.Entry(input_frame)
            entry.pack(pady=4)

            self.entries.append(entry)

        # submit button
        submit_button = tk.Button(submit_frame, text="Lisa", command=self.send_to_database)
        submit_button.pack()

        middle_frame.pack(padx=20)
        name_frame.pack(side='left', fill='both', expand=True)
        input_frame.pack(side='right', fill='both', expand=True)
        submit_frame.pack(side='bottom', fill='both', expand=True)

    def send_to_database(self):
        id_value = []
        for entry in self.entries:
            id_value.append(entry.get())

        self.queryDAO.queryAddDataToDatabase(id_value)