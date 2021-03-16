# версия от 2020.03.16

import os
import datetime
import requests
import configparser


def set_snapshot_name():
    """ Функция создания имени файла
    Генерирует имя файл из текущей даты и времени
    """
    # TODO: оформить парсинг в красивом виде

    ts = datetime.datetime.now()
    file_name = str(ts.year) + \
                "-" + \
                str(ts.month) + \
                "-" + \
                str(ts.day) + \
                "-" + \
                str(ts.hour) + \
                "-" + \
                str(ts.minute) + \
                "-" + \
                str(ts.second) + \
                ".jpg"
    return file_name


class Camera:
    """ Базовый класс для камер

    :param ip: IP адрес камеры (default 192.168.0.20)
    """

    def __init__(self, ip='192.168.0.20'):
        self.ip = ip

        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read("D:/Diploma/Detection/settings.ini")

        self.data_dir = config["CAMERA"]["DATA_DIR"]
        os.chdir(self.data_dir)

    @property
    def check_connection(self):
        """ Функция проверки соединения

        """
        try:
            response = requests.get("http://" + self.ip)
            if response.status_code == 200:
                print(f"Camera with {self.ip} is online.")
            return True

        except requests.ConnectionError:
            print(f"Camera with {self.ip} is offline")
            return False

    def get_snapshot(self):
        """ Функция захвата картинки и сохраниния в файла с текущим таймстампом

        """

        file_snapshot_name = set_snapshot_name()

        url = 'http://' + self.ip + '/jpeg/jpeg.jpg'

        r = requests.get(url)

        with open(self.data_dir + '\\' + file_snapshot_name, 'wb') as f:
            f.write(r.content)
