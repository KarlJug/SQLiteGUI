import tkinter as tk
from tkinter import ttk
from DB.QueryDAO import QueryDAO
from DB.func.add_logic import Add
from DB.func.delete_logic import Delete


class TreeGUI:
    queryDAO = QueryDAO()
    queryDAO.getTables()

    def __init__(self, master):

        self.data_loaded = False

        self.master = master
        self.tables = tk.ttk.Treeview(master)
        self.tables.pack(side='left', fill=tk.BOTH)

        # temp widgets to be loaded later
        self.right_frame = ttk.Frame(self.master)

        # Set up the columns for the tree
        self.tables.heading("#0", text="Databases")

        self.tables.insert("", "end", text="epood_kjugapuu", iid='0')

        self.load_table()
        self.tables.bind("<<TreeviewSelect>>", lambda event: self.selected())

    def load_table(self):
        column_names = self.queryDAO.getAllColumns()

        for i in range(0, len(self.queryDAO.table_names)):
            self.tables.insert('', tk.END, text=self.queryDAO.table_names[i],
                               iid=str(i) + ' ' + self.queryDAO.table_names[i], values=self.queryDAO.table_names[i])
            self.tables.move(str(i) + ' ' + self.queryDAO.table_names[i], '0', i)

            for j in range(0, len(column_names[i])):
                self.tables.insert('', tk.END, text=column_names[i][j][1], iid=str(i) + ' ' + column_names[i][j][1],
                                   values=self.queryDAO.table_names[i])
                self.tables.move(str(i) + ' ' + column_names[i][j][1], str(i) + ' ' + self.queryDAO.table_names[i], j)

    def selected(self):
        selected_item_id = self.tables.selection()[0]  # get the ID of the selected item
        selected_item = self.tables.item(selected_item_id)  # get the data for the selected item
        values = selected_item["values"]  # get the values of the selected item

        if len(values):  # checks if there is a value
            self.queryDAO.selected_table = values[0]

            self.load_data()

    def load_data(self):
        if self.data_loaded:
            self.right_frame.destroy()

        # right frame
        self.right_frame = ttk.Frame(self.master)

        self.queryDAO.selected_raw_column_names = self.queryDAO.getSelectedColumns()

        # top and data frame in right frame
        top_frame = ttk.Frame(self.right_frame)
        data_frame = ttk.Frame(self.right_frame)

        #
        columns_no_id = []
        for column in self.queryDAO.selected_raw_column_names:
            if not column[5]:
                columns_no_id.append(column[1])
        self.queryDAO.selected_column_names_no_id = columns_no_id

        columns = [column[1] for column in self.queryDAO.selected_raw_column_names]
        self.queryDAO.selected_column_names = columns

        print(columns)
        data = tk.ttk.Treeview(data_frame, columns=columns, show='headings')

        data_str_len = []
        for i, column in enumerate(columns):
            data.heading(column, text=column)
            data_str_len.append(len(str(column)))

        column_data = self.queryDAO.getData()

        for i, row in enumerate(column_data):
            data.insert(parent='', index=i, values=row)
            row_list = list(row)
            for i, r in enumerate(row_list):
                if data_str_len[i] < len(str(r)):
                    data_str_len[i] = len(str(r))

        print(data_str_len)

        for i, column in enumerate(columns):
            data.column(column, width=data_str_len[i] * 9)

        # vertical scrollbar
        vsb = ttk.Scrollbar(data_frame, orient="vertical", command=data.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)


        # widgets
        add_button = tk.Button(top_frame, text="Lisa", command=Add(self.master, self.queryDAO).add_window)
        delete_button = tk.Button(top_frame, text="Kustuta", command=Delete().selected)

        # confs and display
        add_button.pack(side='left')
        delete_button.pack(side="left")

        data.config(height=15)
        data.pack(side='bottom')
        self.data_loaded = True

        self.right_frame.pack(fill='both', expand=True)
        top_frame.pack(side='top', fill='both', expand=True)
        data_frame.pack(side='bottom', fill='both', expand=True)
