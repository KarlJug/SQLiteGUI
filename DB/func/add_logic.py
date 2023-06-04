import tkinter as tk
from tkinter import ttk


class Add:
    """logic to add data to a database"""
    def __init__(self, master, QueryDAO, refresh_data, parent_item):
        self.master = master
        self.queryDAO = QueryDAO
        self.entries = []  # holds entry widgets from add_window()
        self.add_data_window = None
        self.refresh_data = refresh_data
        self.parent_item = parent_item

    def add_window(self):

        self.add_data_window = tk.Toplevel(self.master)
        self.add_data_window.title("Add a new entry")

        middle_frame = ttk.Frame(self.add_data_window)
        name_frame = ttk.Frame(middle_frame)
        input_frame = ttk.Frame(middle_frame)
        submit_frame = ttk.Frame(self.add_data_window)

        # label
        label_top = tk.Label(self.add_data_window, text="Lisage andmebaasi uued andmed")
        label_top.pack(pady=5)

        # input
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

        self.queryDAO.queryAddDataToDatabase(id_value, self.parent_item)
        self.add_data_window.destroy()

        self.refresh_data()  # refreshes the data tree
        del self
