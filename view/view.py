import tkinter as tk
from itertools import zip_longest
from tkinter import ttk
import re
from DB.QueryDAO import QueryDAO
from DB.func.add_logic import Add
from DB.func.delete_logic import Delete
from DB.func.PlaceholderEntry import PlaceholderEntry
from DB.func.Tooltip import ToolTip
from DB.func.CustomCircle import CustomCircle
from DB.func.Edit import Edit
from DB.DBConnection import Connection


class TreeGUI:
    connection = Connection()
    queryDAO = QueryDAO(connection)
    queryDAO.getTables()

    def __init__(self, master):

        self.data_loaded = False
        self._selected_data = False
        self.values = []  # selected data.Treeview data in a list
        self.parent_item = ''

        self.connection.get_database_file_names()

        self.master = master
        self.tables = tk.ttk.Treeview(master)
        self.tables.pack(side='left', fill=tk.BOTH)

        # temp widgets to be loaded later
        self.right_frame = ttk.Frame(self.master)

        # Set up the columns for the tree
        self.tables.heading("#0", text="Databases")

        for base in self.connection.file_names:
            self.tables.insert("", "end", text=base, iid=base)

        #self.tables.bind("<ButtonRelease-1>", lambda event: self.get_selected_row(event, self.tables, self.connection.selected_table, parent=True))

        self.load_table()
        self.tables.bind("<<TreeviewSelect>>", lambda event: self.selected())


    def load_table(self):
        for num, base in enumerate(self.queryDAO.table_names):
            column_names = self.queryDAO.getAllColumns(self.connection.file_names[num], num)

            for i, table in enumerate(base):
                self.tables.insert('', tk.END, text=table, iid=str(num) + '.' + str(i) + ' ' + table, values=table)
                self.tables.move(str(num) + '.' + str(i) + ' ' + table, self.connection.file_names[num], i)

                for j, name in enumerate(column_names[i]):
                    self.tables.insert('', tk.END, text=name[1], iid=str(num) + '.' + str(i) + '.' + str(j) + ' ' + name[1], values=table)
                    self.tables.move(str(num) + '.' + str(i) + '.' + str(j) + ' ' + name[1], str(num) + '.' + str(i) + ' ' + table, j)

    def selected(self):
        selected_item_id = self.tables.selection()[0]  # get the ID of the selected item
        selected_item = self.tables.item(selected_item_id)  # get the data for the selected item
        values = selected_item["values"]  # get the values of the selected item

        if len(values):  # checks if there is a value
            self.queryDAO.selected_table = values[0]
            self.parent_item = self.tables.parent(selected_item_id)

            self.load_data()

    def load_data(self):
        if self.data_loaded:
            self.right_frame.destroy()
            self.entry.destroy()

        # right frame
        self.right_frame = ttk.Frame(self.master)

        self.queryDAO.selected_raw_column_names = self.queryDAO.getSelectedColumns(self.parent_item)

        # top and data frame in right frame
        top_frame = ttk.Frame(self.right_frame)
        data_frame = ttk.Frame(self.right_frame)
        menu_frame = ttk.Frame(top_frame)
        buttons_frame = ttk.Frame(menu_frame)
        filter_frame = ttk.Frame(menu_frame)
        filter_layout = ttk.Frame(filter_frame)

        #
        columns_no_id = []
        columns_id = []
        columns_id_names = []
        for i, column in enumerate(self.queryDAO.selected_raw_column_names):
            if not column[5]:
                columns_no_id.append(column[1])

            else:
                columns_id_names.append(column[1])
                columns_id.append(i)

        self.queryDAO.selected_column_names_no_id = columns_no_id
        self.queryDAO.selected_column_id_spot = columns_id

        self.queryDAO.selected_column_names_with_id = columns_id_names

        self.queryDAO.selected_column_names = [column[1] for column in self.queryDAO.selected_raw_column_names]
        self.queryDAO.selected_column_types = [column[2] for column in self.queryDAO.selected_raw_column_names]

        self.data = tk.ttk.Treeview(data_frame, columns=self.queryDAO.selected_column_names, show='headings')

        for header in self.queryDAO.selected_column_names:
            self.data.heading(header, command=lambda h=header: self.sort_treeview(self.data, h, False))

        self.data.bind("<ButtonRelease-1>", lambda event: self.get_selected_row(event, self.data, self.values, boolean=True))
        self.data.bind("<FocusOut>", self.unselected)

        data_str_len = []
        for i, column in enumerate(self.queryDAO.selected_column_names):
            self.data.heading(column, text=column)
            data_str_len.append(len(str(column)))

        self.column_data = self.queryDAO.getData(self.parent_item)

        for i, row in enumerate(self.column_data):
            self.data.insert(parent='', index=i, values=row)

            # for with of tree column
            row_list = list(row)
            for i, r in enumerate(row_list):
                if data_str_len[i] < len(str(r)):
                    data_str_len[i] = len(str(r))

        # setting with of tree column
        for i, column in enumerate(self.queryDAO.selected_column_names):
            self.data.column(column, width=data_str_len[i] * 9)

        # vertical scrollbar
        vsb = ttk.Scrollbar(data_frame, orient="vertical", command=self.data.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # widgets
        add_button = tk.Button(buttons_frame, text="Lisa", command=Add(self.master, self.queryDAO, self.load_data, self.parent_item).add_window)
        self.delete_button = tk.Button(buttons_frame, text="Kustuta", state="disabled", command=Delete(self.data, self.queryDAO, self.load_data, self.parent_item).selected)
        self.edit_button = tk.Button(buttons_frame, text="Muuda", state="disabled", command=lambda: Edit(buttons_frame, self.queryDAO, self.load_data, self.parent_item).edit_window(self.values))

        self.placeholder = "Filter"
        self.entry = PlaceholderEntry(filter_layout, self.placeholder)
        self.entry.pack(side='left')

        self.entry_var = tk.StringVar()
        self.entry_var.trace("w", self.filter_data)
        self.entry.config(textvariable=self.entry_var)
        self.entry.insert_placeholder()

        question_toolip = CustomCircle(filter_layout, 20)
        ToolTip(question_toolip, "number-number\n>number\n<number")

        # confs and display
        add_button.pack(side='bottom', fill=tk.X)
        self.delete_button.pack(side="bottom")
        self.edit_button.pack(side='right', fill=tk.X)

        self.data.config(height=15)
        self.data.pack(side='bottom', fill='both')
        question_toolip.pack(side='right')
        self.data_loaded = True  # will allow for stuff to be unloaded

        self.right_frame.pack(fill='both', expand=True)
        top_frame.pack(side='top', fill='both', expand=True)
        data_frame.pack(side='bottom', fill='both', expand=True)
        menu_frame.pack(fill='both', expand=True)
        buttons_frame.pack(side='left', fill='both')
        filter_frame.pack(side='right', fill='both', expand=True)
        filter_layout.pack(expand=True)

    @staticmethod
    def compare_strings(str1, str2):
        # compares str1 for the length of str 2
        if str1[:len(str2)] == str2:
            return True
        return False

    # filters the data with a textbox
    def filter_data(self, *args):
        filter_text = self.entry.get()
        if filter_text == self.placeholder:
            filter_text = ""

        # Remove all existing items from the treeview
        self.data.delete(*self.data.get_children())

        # get column int str and boolean spots
        sql_type = []
        int_type = []
        str_type = []

        for i, column in enumerate(self.queryDAO.selected_column_types):

            if 'INTEGER' in column:
                sql_type.append(int)
                int_type.append(i)

            elif 'VARCHAR' in column:
                sql_type.append(str)
                str_type.append(i)

            elif 'DATETIME' in column:
                sql_type.append(int)
                int_type.append(i)

            elif 'REAL' in column:
                sql_type.append(int)
                int_type.append(i)

            else:
                sql_type.append(str)
                str_type.append(i)

        through_pattern = r'^-?\d+-\d+$'
        index = 0

        if re.match(through_pattern, filter_text):
            num1 = 0
            num2 = 0
            temp1 = ''
            temp2 = ''

            second = False
            for i in range(0, len(filter_text)):
                if filter_text[i] and filter_text[i] != "-" and not second:
                    temp1 += filter_text[i]

                elif filter_text[i] and filter_text[i] != "-" and second:
                    temp2 += filter_text[i]

                else:
                    second = True

                if i == len(filter_text) - 1:
                    num1 = int(temp1)
                    num2 = int(temp2)

            for row in self.column_data:
                for j in int_type:
                    if num1 <= row[j] <= num2:
                        self.data.insert(parent='', index=index, values=row)
                        index += 1
                        break


        elif filter_text and filter_text[0] == "<" and filter_text[1:].isdigit():
            num = int(filter_text[1:])
            for row in self.column_data:
                for j in int_type:
                    if row[j] < num:
                        self.data.insert(parent='', index=index, values=row)
                        index += 1
                        break


        elif filter_text and filter_text[0] == ">" and filter_text[1:].isdigit():
            num = int(filter_text[1:])
            for row in self.column_data:
                for j in int_type:
                    if row[j] > num:
                        self.data.insert(parent='', index=index, values=row)
                        index += 1
                        break


        elif filter_text and filter_text.isdigit():
            for row in self.column_data:
                for int_j, str_j in zip_longest(int_type, str_type):
                    if int_j is not None:
                        if int(filter_text) == row[int_j]:
                            self.data.insert(parent='', index=index, values=row)
                            index += 1
                            break

                    elif str_j is not None:
                        if filter_text.lower() in row[str_j].lower():
                            self.data.insert(parent='', index=index, values=row)
                            index += 1
                            break


        else:
            for row in self.column_data:
                for j in str_type:
                    if filter_text.lower() in row[j].lower():
                        self.data.insert(parent='', index=index, values=row)
                        index += 1
                        break

    def get_selected_row(self, event, treeview, storages, boolean=False, parent=False):

        selected_items = treeview.selection()
        if selected_items:
            item = selected_items[0]
            values = treeview.item(item, 'values')
            storages.clear()
            storages.extend(values)

            if parent:
                self.parent_item = treeview.parent(item)

                self.load_data()

            if boolean:
                self.selected_data = True



    def unselected(self, event):
        self.values = []
        self.selected_data = False

    @staticmethod
    def is_numeric_string(value):
        try:
            float_value = float(value)
            return True
        except ValueError:
            return False

    def sort_treeview(self, treeview, column, reverse=False):
        '''Sorts tree view data and arranges it'''
        is_digit = False

        for child in treeview.get_children(''):
            if treeview.set(child, column).isdigit() or self.is_numeric_string(treeview.set(child, column)):
                is_digit = True
            else:
                is_digit = False

        if is_digit:
            data = [(float(treeview.set(child, column)), child) for child in treeview.get_children('')]
        else:
            data = [(treeview.set(child, column), child) for child in treeview.get_children('')]
        data.sort(reverse=reverse)
        for index, (_, child) in enumerate(data):
            treeview.move(child, '', index)
        treeview.heading(column, command=lambda: self.sort_treeview(treeview, column, not reverse))

    """Will detect when a value has been changed and change button states accordingly"""
    @property
    def selected_data(self):
        return self._selected_data

    @selected_data.setter
    def selected_data(self, value):
        if self._selected_data != value:
            self._selected_data = value
            if value:
                self.delete_button.config(state="normal")
                self.edit_button.config(state="normal")
            else:
                self.delete_button.config(state="disabled")
                self.edit_button.config(state="disabled")
