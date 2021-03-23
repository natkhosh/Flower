from Modbus.modbus import *
from DataBase.database import *
from Detector.detector import *
from Camera.camera_onvif import *
import configparser
import time


def main_():

    # IP адреса устройств, к которым будем подключаться беруться из файла настроек
    config = configparser.ConfigParser()
    # TODO: сделать нормальные относительные пути
    config.read("D:/Diploma/Detection/settings.ini")

    # создаем экземляры наших устройств
    db = DB('db.sqlite3')
    cam = Camera(config["CAMERA"]["IP"])
    device = ModbusDevice(config["MODBUS"]["IP"])
    detector = Detector("D:/Diploma/Detection/Detector/model_all.pth")

    if cam.check_connection & device.modbus_check_connection:
        print("all ok")

    # отслеживаем изменение состояние входа
    trigger = False

    while True:
        system_stop = device.modbus_read(config["MODBUS"]["DI2"])
        input_state = device.modbus_read(config["MODBUS"]["DI1"])

        # Если подана команда на остановку (2 регистр в ON) выходим из цикла и завершаем программу
        if system_stop:
            break

        elif input_state & (input_state != trigger):

            # Захватываем изображение. Получаем имя файла с изображением
            file_name = cam.get_snapshot()
            # Определяем класс растения
            img_class = detector.predict(config["CAMERA"]["DATA_DIR"] + "/" + file_name)
            # Соединяемся с БД
            db_connection = db.create_connection()
            # Формируем запрос к БД
            db_query = "INSERT INTO flower_camera ('class_name_id' , 'store_position_id', 'image') VALUES ('" + img_class + "', 'A1', 'uploads/" + file_name + "')"

            #db_query = "SELECT * FROM flower_camera"

            db_result = db.execute_write_query(db_connection, db_query)
            print(db_result)
            db_connection.close()

            trigger = input_state
            print("Photo")

        elif not input_state:
            trigger = input_state

        time.sleep(15)

    device.modbus_disconnect()
    return


def main_test_det():

    detector = Detector("D:/Diploma/Detection/Detector/model_all.pth")
    img_class = detector.predict("D:/Diploma/Detection/Pic/Image05.jpg")
    print(img_class)

    return


def main():
    db = DB('db.sqlite3')
    db_connection = db.create_connection()
    db_query = "INSERT INTO flower_camera ('class_name_id' , 'store_position_id', 'image') VALUES ('Unknown' ,'A3', 'D:\\Diploma\\Flower_01\\flower\\static\\uploads\\2021-3-22-1-58-15.jpg')"
    # db_query = "SELECT * FROM flower_camera"
    db_result = db.execute_read_query(db_connection, db_query)

    db_connection.close()
    print(db_result)

    return


if __name__ == '__main__':

    main()



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
