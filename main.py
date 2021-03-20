from Camera.camera_onvif import *
from Modbus.modbus import *
from Detector.detector import *
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


def main():

    # 'D:/Diploma/Detection/Detector/model.pth'
    detector = Detector("D:/Diploma/Detection/Detector/model_all.pth")
    img_class = detector.predict("D:/Diploma/Detection/Pic/Image05.jpg")

    print(img_class)

    return


if __name__ == '__main__':
    main()

