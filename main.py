from Camera.camera_onvif import *
from Modbus.modbus import *
import configparser
import time


def main():

    # IP адреса устройств, к которым будем подключаться беруться из файла настроек
    config = configparser.ConfigParser()
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


if __name__ == '__main__':
    main()

