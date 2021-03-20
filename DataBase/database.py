import sqlite3


class DB:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_connection(self):
        c_connection = None
        try:
            c_connection = sqlite3.connect(self.db_path)
            print("Connection to SQLite DB successful")
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        return c_connection


    @staticmethod
    def execute_read_query(connection, query):
        """
        Извлечение данных из записей
        :param connection:
        :param query:
        :return:
        """
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            print(f"The error '{e}' occurred")

        # ---- Вставка записей ----
        # create_users = """
        # INSERT INTO
        #   `users` (`name`, `age`, `gender`, `nationality`)
        # VALUES
        #   ('James', 25, 'male', 'USA'),
        #   ('Leila', 32, 'female', 'France'),
        #   ('Brigitte', 35, 'female', 'England'),
        #   ('Mike', 40, 'male', 'Denmark'),
        #   ('Elizabeth', 21, 'female', 'Canada');
        # """
        # execute_query(connection, create_users)

        # ----UPDATE BD-----
        # update_post_description = """
        # UPDATE
        #   posts
        # SET
        #   description = "The weather has become pleasant now"
        # WHERE
        #   id = 2
        # """
        #
        # execute_query(connection, update_post_description)

db = DB('db.sqlite3')

db_connection = db.create_connection()
db_query = "SELECT * FROM flower_watering WHERE class_name='Ficus' ORDER BY class_name"
db_result = db.execute_read_query(db_connection, db_query)
db_connection.close()
print(db_result)
