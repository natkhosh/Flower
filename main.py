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
    cam = Camera(config["CAMERA"]["IP"])
    device = ModbusDevice(config["MODBUS"]["IP"])

    # if cam.check_connection & device.modbus_check_connection:
    #     print("all ok")

    # отслеживаем изменение состояние входа
    trigger = False

    while True:

        input_state = device.modbus_read(config["MODBUS"]["DI1"])
        if input_state & (input_state != trigger):
            cam.get_snapshot()
            trigger = input_state
            print("Photo")
            time.sleep(10)
        else:
            trigger = input_state
            time.sleep(10)

    device.modbus_disconnect()
    return


def main_test_det():

    detector = Detector("D:/Diploma/Detection/Detector/model_all.pth")
    img_class = detector.predict("D:/Diploma/Detection/Pic/Image05.jpg")
    print(img_class)

    return


def main_test_db():
    db = DB('db.sqlite3')
    db_connection = db.create_connection()
    db_query = "SELECT * FROM flower_watering WHERE class_name='Ficus' ORDER BY class_name"
    db_result = db.execute_read_query(db_connection, db_query)
    db_connection.close()
    print(db_result)

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

    return

if __name__ == '__main__':
    main()

