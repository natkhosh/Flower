import sqlite3


class DB:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_connection(self):
        """ Функция соединения с базой данных

        :return: Возвращает "соединение"
        """
        c_connection = None
        try:
            c_connection = sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        return c_connection

    @staticmethod
    def execute_read_query(connection, query):
        """ Извлечение данных из записей

        :param connection: Принимает "соединение"
        :param query: Запрос в формате SQL
        :return: Возвращает резуьтат запроса
        """
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

