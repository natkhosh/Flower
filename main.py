from Camera.camera_onvif import *
from Modbus.modbus import *
import configparser


def main():

    # IP адреса устройств, к которым будем подключаться беруться из файла настроек
    config = configparser.ConfigParser()
    config.read("D:/Diploma/Detection/settings.ini")

    # создаем экземляры наших устройств
    cam = Camera(config["CAMERA"]["IP"])
    device = ModbusDevice(config["MODBUS"]["IP"])

    if cam.check_connection & device.modbus_check_connection:
        print("all ok")

    device.modbus_disconnect()
    return


if __name__ == '__main__':
    main()

