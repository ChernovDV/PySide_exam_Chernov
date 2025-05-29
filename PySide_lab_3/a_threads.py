"""
Модуль в котором содержаться потоки Qt
"""

import time
import psutil
from PySide6 import QtCore
from PySide6.QtCore import Signal, QThread, QObject, Slot
import requests


class SystemInfo(QtCore.QThread):
    systemInfoReceived = Signal(list)  # Создайте экземпляр класса Signal и передайте ему в конструктор тип данных передаваемого значения (в текущем случае list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = 1  #   Cоздайте атрибут класса self.delay = None, для управлением задержкой получения данных (Начальная задержка в секунду)

    def run(self) -> None:  # переопределить метод run
        while True:  # Запустите бесконечный цикл получения информации о системе
            cpu_value = psutil.cpu_percent(interval=1)  # с помощью вызова функции cpu_percent() в пакете psutil получите загрузку CPU
            ram_value = psutil.virtual_memory().percent  # с помощью вызова функции virtual_memory().percent в пакете psutil получите загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # с помощью метода .emit передайте в виде списка данные о загрузке CPU и RAM
            time.sleep(self.delay)  # с помощью функции .sleep() приостановите выполнение цикла на время self.delay


class WeatherHandler(QThread):
    weatherDataReceived = Signal(dict)
    # Пропишите сигналы, которые считаете нужными

    def __init__(self, latitude, longitude, parent=None):
        super().__init__(parent)

        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        self.delay = 10
        self.status = True

    def setDelay(self, new_delay) -> None:
        """
        Метод для установки времени задержки обновления сайта
        """
        self.delay = new_delay


    def run(self) -> None:
        # настройте метод для корректной работы

        while self.status:
            try:
                response = requests.get(self.api_url)
                if response.ok:
                    data = response.json()["current_weather"]
                    self.weatherDataReceived.emit(data)
                else:
                    print(f'Ошибка при получении данных: {response.status_code}')
            except Exception as e:
                print(f'Ошибка обработки запроса: {e}')
            finally:
                time.sleep(self.delay)

