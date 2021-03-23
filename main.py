from Modbus.modbus import *
from DataBase.database import *
from Detector.detector import *
from Camera.camera_onvif import *
import configparser
import time


def main():

    # IP адреса устройств, к которым будем подключаться беруться из файла настроек
    config = configparser.ConfigParser()
    # TODO: сделать нормальные относительные пути
    config.read("D:/Diploma/Detection/settings.ini")

    # создаем экземляры наших устройств
    db = DB('D:/Diploma/Flower_01/db.sqlite3')
    cam = Camera(config["CAMERA"]["IP"])
    device = ModbusDevice(config["MODBUS"]["IP"])
    detector = Detector("D:/Diploma/Detection/Detector/model_all.pth")

    if cam.check_connection & device.modbus_check_connection:
        print("all ok")

    # отслеживаем изменение состояние входа
    trigger = False
    # складская позиция фиксированная
    store_position_id = 1

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
            # Формируем запрос к БД о параметрах полива по классу растения

            db_query_watering = "SELECT id_plant, class_name, watering_volume, watering_point  " \
                                "FROM flower_watering WHERE class_name='" + img_class + "'"

            db_result_watering = db.execute_read_query(db_connection, db_query_watering)
            plant_name_id = db_result_watering[0][0]
            watering_volume_fact = db_result_watering[0][2]
            watering_point_fact = db_result_watering[0][3]

            # Формируем запрос к БД запись изображения
            db_query_camera = "INSERT INTO flower_camera (" \
                              "'class_name_id' , " \
                              "'store_position_id', " \
                              "'image') " \
                              "VALUES ('"\
                              + str(plant_name_id) + "', '" \
                              + str(store_position_id) + "', 'uploads/" + file_name + "')"

            db.execute_write_query(db_connection, db_query_camera)

            # добавить полив

            # Получаем время операции для журнала
            ts = datetime.datetime.now()
            timestamp = str(ts.year) + \
                        "-" + \
                        str(ts.month) + \
                        "-" + \
                        str(ts.day) + \
                        " " + \
                        str(ts.hour) + \
                        ":" + \
                        str(ts.minute) + \
                        ":" + \
                        str(ts.second)
            # Формируем запрос к БД запись изображения
            db_query_journal = "INSERT INTO flower_journal (" \
                               "'timestamp' , " \
                               "'watering_volume_fact', " \
                               "'plant_name_id', " \
                               "'store_position_id', " \
                               "'watering_point_fact') " \
                               "VALUES ('" \
                               + str(timestamp) + "', '" \
                               + str(watering_volume_fact) + "', '" \
                               + str(plant_name_id) + "', '" \
                               + str(store_position_id) + "', '" \
                               + str(watering_point_fact) + "')"

            db.execute_write_query(db_connection, db_query_journal)

            db_connection.close()

            trigger = input_state

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


def main_():
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
