# версия от 20.02.2021

import configparser
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException


# configparser - библиотека парсера конфигураци
# pymodbus - библиотека с реализацией Modbus протокола

class ModbusDevice:
    """ Базовый класс для контроллеров с Modbus интерфейсом

        :param ip: IP адрес устройства (default 192.168.0.200)

        """

    def __init__(self, ip='192.168.0.20'):
        self.ip = ip

        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read("D:/Diploma/Detection/settings.ini")

        self.port = config["MODBUS"]["PORT"]

        self.client = ModbusTcpClient(self.ip, self.port)

    def modbus_disconnect(self):
        """
        Функция закрытие соединения

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
            print('No connection')


    # TODO: modbus_plant_watering - сделать через TRY подключение к контроллеру, как в проверке соединения

    def modbus_plant_watering(self, watering_zone=1, watering_volume=10):
        """ Implementation of a modbus watering

        :param watering_zone: Zone of watering 1 - Low, 2 - Middle, 3 - High (default 1-Low)
        :param watering_volume: Water volume in ml (default 10)
        """
        zone = watering_zone
        volume = watering_volume

        # результат работы функции в текстовом формате
        function_result = 'Watering complete'

        # чтение и загрузка конфигурации из файла
        config = configparser.ConfigParser()
        config.read('D:/Diploma/Detection/settings.ini')

        # открываем соединение с контроллером
        # сделать через TRY и по исключению выдавать результат ошибки
        client = ModbusTcpClient(config["MODBUS"]["IP"], config["MODBUS"]["PORT"])

        # по умолчанию в settings.ini реле N6 параметр 125 - оно в программе контроллера управляемое по сети
        if zone == 1:
            client.write_coil(int(config["MODBUS"]["ZONE_LOW"]), True)
        elif zone == 2:
            client.write_coil(int(config["MODBUS"]["ZONE_MID"]), True)
        elif zone == 3:
            client.write_coil(int(config["MODBUS"]["ZONE_HIGH"]), True)
        else:
            function_result = 'Wrong watering Zone argument!'

        # отправляем объем полива
        client.write_register(int(config["MODBUS"]["VOLUME"]), watering_volume)

        # закрываем соединение с контроллером
        client.close()

        return function_result
