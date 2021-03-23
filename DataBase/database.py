import sqlite3


class DB:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_connection(self):
        """ Функция соединения с базой данных

        :return: Возвращает "соединение"
        """
        sqlite_connection = None
        try:
            sqlite_connection = sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        return sqlite_connection

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
            cursor.close()
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

    @staticmethod
    def execute_write_query(connection, query):
        """
        Запись данных в базу данных
        :param connection: Принимает "соединение"
        :param query: Запрос в формате SQL
        """
        try:
            cursor = connection.cursor()
            print("Подключен к SQLite")

            cursor.execute(query)
            connection.commit()
            print("Запись успешно вставлена ​​в таблицу ", cursor.rowcount)
            cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

