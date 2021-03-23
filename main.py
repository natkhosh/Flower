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

    # Проверка соединений
    if cam.check_connection & device.modbus_check_connection:
        print("Camera and device connection created.")

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
            if watering_point_fact == "Дождевание":
                watering_zone = 1
            elif watering_point_fact == "Дождевание":
                watering_zone = 2
            elif watering_point_fact == "Дождевание":
                watering_zone = 3
            else:
                watering_zone = 0

            watering_result = device.modbus_plant_watering(watering_zone, watering_volume_fact)

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

            if watering_result:
                db.execute_write_query(db_connection, db_query_journal)

            db_connection.close()

            trigger = input_state

        elif not input_state:
            trigger = input_state

        time.sleep(5)

    device.modbus_disconnect()
    return


if __name__ == '__main__':
    main()
