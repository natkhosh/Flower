# версия от 20.02.2021

import configparser
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException


# configparser - библиотека парсера конфигураци
# pymodbus - библиотека с реализацией Modbus протокола

class ModbusDevice:
    """ Базовый класс для контроллеров с Modbus интерфейсом

    """

    def __init__(self, ip='192.168.0.20'):
        """

        :param ip: IP адрес устройства (default 192.168.0.200)
        """
        self.ip = ip
        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read("D:/Diploma/Detection/settings.ini")

        self.port = config["MODBUS"]["PORT"]

        # открываем соединение с контроллером
        try:
            self.client = ModbusTcpClient(self.ip, self.port)
        except ModbusException as e:
            print(f"Device with {self.ip} is offline")

    def modbus_disconnect(self):
        """ Функция закрытия соединения

        """
        self.client.close()
        return

    @property
    def modbus_check_connection(self):
        """ Функция проверки соединения

        """
        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read("D:/Diploma/Detection/settings.ini")

        # открываем соединение с контроллером
        try:
            result = self.client.read_coils(1, 1)
            print(f"Device with {self.ip} is online. Coil 1 status {result}")
            return True
        except ModbusException:
            print(f"Device with {self.ip} is offline")
            return False

    def modbus_read(self, register=1):
        """ Функция чтения входного регистра

        """

        try:
            result = self.client.read_discrete_inputs(int(register), 1)
            if result.bits[0]:
                return True
            else:
                return False
        except ModbusException:
            print(f"Device with {self.ip} is offline")

    def modbus_plant_watering(self, watering_zone=1, watering_volume=10):
        """ Функиця полива

        :param watering_zone: Зона полива 1 - Low, 2 - Middle, 3 - High (default 1-Low)
        :param watering_volume: Объем полива ml (default 10)
        """

        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read('D:/Diploma/Detection/settings.ini')

        # по умолчанию в settings.ini реле N6 параметр 125 - оно в программе контроллера управляемое по сети
        if watering_zone == 1:
            self.client.write_coil(int(config["MODBUS"]["ZONE_LOW"]), True)
        elif watering_zone == 2:
            self.client.write_coil(int(config["MODBUS"]["ZONE_MID"]), True)
        elif watering_zone == 3:
            self.client.write_coil(int(config["MODBUS"]["ZONE_HIGH"]), True)

        # отправляем объем полива
        self.client.write_register(int(config["MODBUS"]["VOLUME"]), watering_volume)

        # закрываем соединение с контроллером
        self.modbus_disconnect()

        return True
