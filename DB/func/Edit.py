import tkinter as tk
from tkinter import ttk


class Edit:
    def __init__(self, master, QueryDAO, load_data, parent_item):
        self.master = master
        self.queryDAO = QueryDAO
        self.entries = []
        self.load_data = load_data
        self.parent_item = parent_item

        self.id = []
        self.id_name = []
        self.entry_list = []


    def edit_window(self, valuse):
        no_id_values = valuse

        for i in self.queryDAO.selected_column_id_spot:
            self.id.append(valuse[i])
            self.id_name.append(self.queryDAO.selected_column_names[i])
            del no_id_values[i]

        self.edit_data_window = tk.Toplevel(self.master)
        self.edit_data_window.title("Muuda admeid")

        # layout
        middle_frame = ttk.Frame(self.edit_data_window)
        name_frame = ttk.Frame(middle_frame)
        input_frame = ttk.Frame(middle_frame)
        submit_frame = ttk.Frame(self.edit_data_window)

        # label
        label_top = tk.Label(self.edit_data_window, text="Muuda admeid")
        label_top.pack(pady=5)


        # input
        for i, row in enumerate(no_id_values):

            label = tk.Label(name_frame, text=self.queryDAO.selected_column_names_no_id[i])
            label.pack(pady=3)

            entry = tk.Entry(input_frame)
            entry.insert(0, row)
            entry.pack(pady=4)
            self.entry_list.append(entry)

            self.entries.append(entry)

        # submit button
        submit_button = tk.Button(submit_frame, text="Muuda", command=lambda: self.send_change_to_database())
        submit_button.pack()

        middle_frame.pack(padx=20)
        name_frame.pack(side='left', fill='both', expand=True)
        input_frame.pack(side='right', fill='both', expand=True)
        submit_frame.pack(side='bottom', fill='both', expand=True)

    def send_change_to_database(self):
        id_value = []
        for entry in self.entries:
            id_value.append(entry.get())

        self.queryDAO.updateData(self.get_entry(), self.id_name, self.id, self.parent_item)
        self.edit_data_window.destroy()

        self.load_data()  # refreshes the data tree

        del self

    def get_entry(self):
        values = []
        for entry in self.entry_list:
            value = entry.get()
            values.append(value)

        return values
