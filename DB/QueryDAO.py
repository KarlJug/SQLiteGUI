import sqlite3
from DB.DBConnection import Connection


class QueryDAO:
    GET_TABLE_NAMES = "SELECT name FROM sqlite_master WHERE type='table';"
    GET_COLUMN_NAMES = "PRAGMA table_info({table_name})"

    def __init__(self, connection):
        self.connection = connection
        self.data = []
        self.table_names = []
        self.selected_column_names = []
        self.selected_column_names_no_id = []  # all columns name without auto incremented columns
        self.selected_column_names_with_id = []  # all columns name that auto incremented columns ↓
        self.selected_column_id_spot = []  # all column spots that auto increment in an array
        self.selected_column_types = []  # all selected column types
        self.selected_raw_column_names = []
        self.selected_table = ''
        self.selected_column = ''

    @staticmethod
    def validation():
        value = input("(Y)es or (N)o: ")
        if value.lower() == 'y':
            return True

        return False

    def queryAddDataToDatabase(self, id_value, parent_item):
        try:
            conn = self.connection.connect(parent_item)
            cursor = conn.cursor()

            sql = f"INSERT INTO {self.selected_table} "
            sql = sql + "({})".format(", ".join(self.selected_column_names_no_id))
            sql = sql + " VALUES "
            sql = sql + "({})".format(", ".join('?' * len(id_value)))
            cursor.execute(sql, id_value)
            print(sql)

            conn.commit()
            cursor.close()
            conn.close()
            return "was successfully added to table"

        except sqlite3.Error as error:
            return "data failed to insert into SQLite table", str(error)

    def getAllColumns(self, base, num):
        '''For start
        gets all database columns'''
        try:
            table_columns = []
            cursor = self.connection.connect(base).cursor()
            for table in self.table_names[num]:
                cursor.execute(f"PRAGMA table_info({table})")
                rows = cursor.fetchall()
                table_columns.append(rows)

            return table_columns

        except sqlite3.Error as error:
            print(error)

    def getSelectedColumns(self, database_file_name):
        try:
            cursor = self.connection.connect(database_file_name).cursor()
            cursor.execute(f"PRAGMA table_info({self.selected_table})")
            rows = cursor.fetchall()

            return rows

        except sqlite3.Error as error:
            print(error)

    # id_value needs to be a list
    def deleteWHERE(self, id_value, parent_item):
        try:
            conn = self.connection.connect(parent_item)
            cursor = conn.cursor()


            sql = f"DELETE FROM {self.selected_table} WHERE {self.selected_column_names_with_id[0]} IN "
            sql = sql + "({})".format(", ".join('?' * len(id_value)))
            cursor.execute(sql, id_value)
            conn.commit()

            cursor.close()
            conn.close()
        except sqlite3.Error as error:
            print(str(error))

    def updateData(self, values, id_name, id, parent_item):
        try:
            conn = self.connection.connect(parent_item)
            cursor = conn.cursor()

            sql = f"UPDATE {self.selected_table} SET "
            sql = sql + "{}".format(" = ?, ".join(self.selected_column_names_no_id))
            sql = sql + f"= ? WHERE {id_name[0]} = {id[0]}"

            cursor.execute(sql, values)

            conn.commit()
            cursor.close()
            conn.close()
            return "was successfully changed to table"

        except sqlite3.Error as error:
            return "data failed to insert into SQLite table", str(error)

    def getTables(self):
        try:
            for base in self.connection.file_names:
                cursor = self.connection.connect(base).cursor()

                cursor.execute(QueryDAO.GET_TABLE_NAMES)
                tables = cursor.fetchall()

                cursor.close()
                #print(tables)
                temp_table_names = []
                for table in tables:
                    #print(table)
                    temp_table_names.append(table[0])

                self.table_names.append(temp_table_names)

            #return [table[0] for table in tables]

            #return "was successfully"

        except sqlite3.Error as error:
            print(error)
            # return "failed to ", str(error)

    # cursor.execute("PRAGMA table_info(kjugapuu)")

    def getData(self, parent_item):
        try:
            cursor = self.connection.connect(parent_item).cursor()

            cursor.execute(f'SELECT * FROM {self.selected_table}')

            return cursor.fetchall()

        except sqlite3.Error as error:
            print(error)
