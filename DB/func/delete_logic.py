import tkinter as tk
from tkinter import ttk
from DB.QueryDAO import QueryDAO


class Delete:
    def __init__(self, data_column, queryDAO, load_data, parent_item):
        self.data_column = data_column
        self.queryDAO = queryDAO
        self.load_data = load_data
        self.parent_item = parent_item

    def selected(self):
        selected_data = self.data_column.selection()
        id_values = []
        for data in selected_data:
            values = self.data_column.item(data, 'values')
            id_values.append(values[self.queryDAO.selected_column_id_spot[0]])

        self.queryDAO.deleteWHERE(id_values, self.parent_item)
        self.load_data()

    @staticmethod
    def separate_numbers(str_nums):
        num = ''
        nums = []
        for i in range(0, len(str_nums)):

            if i == len(str_nums) - 1 and str_nums[i].isdigit():
                num += str_nums[i]
                nums.append(int(num))

            elif str_nums[i].isdigit():
                num += str_nums[i]

            elif str_nums[i] == ' ':
                pass

            else:
                nums.append(int(num))
                num = ''

        return nums

    @staticmethod
    def integer_type(action, queryDAO):

        match action:
            case 1:
                try:
                    value = Delete.separate_numbers(input("Sisesta numberid: "))
                    queryDAO.deleteWHERE(value)
                except ValueError as error:
                    print("Error: " + str(error))
