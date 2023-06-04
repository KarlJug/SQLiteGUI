import sqlite3
import os

class Connection:
    def __init__(self):
        self.folder_path = "./databases"
        self.file_names = []
        self.selected_table = []
        self.get_database_file_names()

    def get_database_file_names(self):
        self.file_names = os.listdir(self.folder_path)

    def connect(self, file_name):
        return sqlite3.connect("./databases/" + file_name)

