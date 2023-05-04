import sqlite3
from DB import DBConnection


class QueryDAO:
    GET_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table';"
    GET_COLUMN_NAMES = "PRAGMA table_info({table_name})"

    def __init__(self):
        self.data = []
        self.table_names = []
        self.selected_column_names = []
        self.selected_column_names_no_id = []  # all columns but auto incremented columns
        self.selected_raw_column_names = []
        self.selected_table = ''
        self.selected_column = ''

    @staticmethod
    def validation():
        value = input("(Y)es or (N)o: ")
        if value.lower() == 'y':
            return True

        return False

    def queryAddDataToDatabase(self, id_value):
        try:
            print("hey")
            connect = DBConnection.connect()
            cursor = connect.cursor()

            sql = f"INSERT INTO {self.selected_table} "
            sql = sql + "({})".format(", ".join(self.selected_column_names_no_id))
            sql = sql + " VALUES "
            sql = sql + "({})".format(", ".join('?' * len(id_value)))
            cursor.execute(sql, id_value)

            connect.commit()
            cursor.close()
            return "was successfully added to table"

        except sqlite3.Error as error:
            return "data failed to insert into SQLite table", str(error)

    def getAllColumns(self):
        try:
            connect = DBConnection.connect()
            cursor = connect.cursor()

            table_columns = []
            print(self.table_names)
            for table in self.table_names:
                cursor.execute(f"PRAGMA table_info({table})")
                rows = cursor.fetchall()
                table_columns.append(rows)

            return table_columns

        except sqlite3.Error as error:
            print(error)

    def getSelectedColumns(self):
        try:
            connect = DBConnection.connect()
            cursor = connect.cursor()

            cursor.execute(f"PRAGMA table_info({self.selected_table})")
            rows = cursor.fetchall()

            return rows

        except sqlite3.Error as error:
            print(error)

    def deleteWHERE(self, id_value):
        try:
            connect = DBConnection.connect()
            cursor = connect.cursor()

            sql = f"SELECT * FROM {self.table_names} WHERE {self.selected_column} IN "
            sql = sql + "({})".format(", ".join('?' * len(id_value)))
            cursor.execute(sql, id_value)  # (f"SELECT * FROM {self.table_name} WHERE {id} = ?;", id_value)

            items = cursor.fetchall()
            column_names = self.getAllColumns()
            table_name_size = []

            for i in range(0, len(column_names)):
                table_name_size.append(len(str(column_names[i][1])))

            for i in range(0, len(items)):
                for j in range(0, len(items[i])):
                    if len(table_name_size) <= j:
                        table_name_size.append(len(str(items[i][j])))

                    elif table_name_size[j] < len(str(items[i][j])):
                        table_name_size[j] = len(str(items[i][j]))

            # shows column
            for i in range(0, len(column_names)):
                centered_name = str(column_names[i][1]).center(table_name_size[i])
                print(centered_name, end='   ')

            print('')
            #items = [item[0] for item in items]
            for j in range(0, len(items)):
                for i in range(0, len(items[j])):
                    centered_item = str(items[j][i]).center(table_name_size[i])
                    print(centered_item, end='   ')
                print()

            print("\nKas soovid kustutada ", end='')

            if self.validation():
                sql = f"DELETE FROM {self.table_names} WHERE {self.selected_column} IN "
                sql = sql + "({})".format(", ".join('?' * len(id_value)))
                cursor.execute(sql, id_value)
                connect.commit()

            connect.close()
        except sqlite3.Error as error:
            print(str(error))


    def getTables(self):
        try:
            connect = DBConnection.connect()
            cursor = connect.cursor()

            cursor.execute(QueryDAO.GET_TABLE_NAMES)
            tables = cursor.fetchall()

            connect.close()

            for table in tables:
                self.table_names.append(table[0])

            #return [table[0] for table in tables]

            # return "was successfully deleted from the table"

        except sqlite3.Error as error:
            print(error)
            # return "failed to delete table", str(error)

    # cursor.execute("PRAGMA table_info(kjugapuu)")

    def getData(self):
        try:
            connect = DBConnection.connect()
            cursor = connect.cursor()

            cursor.execute(f'SELECT * FROM {self.selected_table}')

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(error)
