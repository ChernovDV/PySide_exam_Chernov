"""
Реализовать виджет, который будет работать с потоком SystemInfo из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода времени задержки
2. поле для вывода информации о загрузке CPU
3. поле для вывода информации о загрузке RAM
4. поток необходимо запускать сразу при старте приложения
5. установку времени задержки сделать "горячей", т.е. поток должен сразу
реагировать на изменение времени задержки
"""
import sys
from PySide6.QtWidgets import *
from a_threads import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Запуск потоков сбора данных
        self.sysinfo_thread = SystemInfo()
        self.sysinfo_thread.systemInfoReceived.connect(self.update_system_info)
        self.sysinfo_thread.start()

        self.weather_thread = WeatherHandler(latitude=55.7522, longitude=37.6156)  # Координаты Москвы
        self.weather_thread.weatherDataReceived.connect(self.update_weather_data)
        self.weather_thread.start()

    def initUI(self):
        layout = QVBoxLayout()

        # Поле для установки интервала опроса
        self.delay_input = QLineEdit("1")
        self.delay_input.textChanged.connect(self.change_delay)
        layout.addWidget(QLabel("Интервал опроса (секунды):"))
        layout.addWidget(self.delay_input)

        # Индикатор CPU
        self.cpu_label = QLabel("Загрузка CPU: ")
        layout.addWidget(self.cpu_label)

        # Индикатор RAM
        self.ram_label = QLabel("Использование RAM: ")
        layout.addWidget(self.ram_label)

        # Погода
        self.temperature_label = QLabel("Температура:")
        layout.addWidget(self.temperature_label)

        self.wind_speed_label = QLabel("Скорость ветра:")
        layout.addWidget(self.wind_speed_label)

        self.setLayout(layout)
        self.resize(300, 200)
        self.show()

    def update_system_info(self, info_list):
        """ Обновление показателей загрузки CPU и RAM """
        cpu_usage, ram_usage = info_list
        self.cpu_label.setText(f"Загрузка CPU: {cpu_usage}%")
        self.ram_label.setText(f"Использование RAM: {ram_usage}%")

    def change_delay(self, text):
        """ Изменение интервала опроса """
        try:
            new_delay = int(text.strip())
            if new_delay > 0:
                self.sysinfo_thread.delay = new_delay
        except ValueError:
            pass

    def update_weather_data(self, weather_data):
        """ Обновление метеоданных """
        temperature = weather_data['temperature']
        wind_speed = weather_data['windspeed']
        self.temperature_label.setText(f"Температура: {temperature}°C")
        self.wind_speed_label.setText(f"Скорость ветра: {wind_speed} м/с")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())