import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('lib.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class BaseModel:
    def __init__(self, connection, tableName, columnNames):
        self.connection = connection
        self.tableName = tableName
        self.columnNames = columnNames
        self.create()

    def create(self):
        query = 'CREATE TABLE IF NOT EXISTS {0} '.format(self.tableName);
        fields = 'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        for i in range(0, len(self.columnNames)):
            fields += '{0} VARCHAR(128),'.format(self.columnNames[i])
        query = '{0} ({1})'.format(query, fields[:-1])
        self.execute(query)

    def drop(self):
        query = 'DROP TABLE IF NOT EXISTS {0} '.format(self.tableName);
        self.execute(query)

    def select(self, conditionField="", conditionValue=""):
        cursor = self.connection.cursor()
        if len(conditionValue) > 0 and len(conditionField) > 0:
            query = "SELECT * FROM {0} WHERE {1}='{2}'".format(self.tableName, conditionField, conditionValue)
        else:
            query = 'SELECT * FROM {0}'.format(self.tableName)
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def insert(self, values):
        if (len(values) > 0):
            query = 'INSERT INTO {0}'.format(self.tableName)
            fields = ""
            for i in range(0, len(self.columnNames)):
                fields += '{0},'.format(self.columnNames[i])
            fields = '({})'.format(fields[:-1])
            valuesStr = ""
            for i in range(0, len(values)):
                valuesStr += "'{0}',".format(values[i])
            valuesStr = 'VALUES ({0})'.format(valuesStr[:-1])
            query = '{0} {1} {2}'.format(query, fields, valuesStr)
            self.execute(query)

    def update(self, conditionField="", conditionValue="", updateField="", updateValue=""):
        if len(updateValue) > 0 and len(conditionField) > 0 and len(conditionValue) > 0 and len(
                updateField) > 0:
            query = "UPDATE {0} SET {1}='{2}' WHERE {3}='{4}'".format(self.tableName, conditionField, conditionValue,
                                                                      updateField, updateValue)
            self.execute(query)

    def delete(self, conditionField="", conditionValue=""):
        if len(conditionField) > 0 and len(conditionValue) > 0:
            query = "DELETE FROM {0} WHERE {1}='{2}'".format(self.tableName, conditionField, conditionValue)
            self.execute(query)

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()
        self.connection.commit()


class UserModel(BaseModel):
    def __init__(self, connection):
        tableName = "Users"
        columnNames = ["name", "password", "isAdmin"]
        super(UserModel, self).__init__(connection, tableName, columnNames)


class BookModel(BaseModel):
    def __init__(self, connection):
        tableName = "Books"
        columnNames = ["title", "description", "url"]
        super(BookModel, self).__init__(connection, tableName, columnNames)
