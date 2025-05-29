"""
Реализовать виджет, который будет работать с потоком WeatherHandler из модуля a_threads

Создавать форму можно как в ручную, так и с помощью программы Designer

Форма должна содержать:
1. поле для ввода широты и долготы (после запуска потока они должны блокироваться)
2. поле для ввода времени задержки (после запуска потока оно должно блокироваться)
3. поле для вывода информации о погоде в указанных координатах
4. поток необходимо запускать и останавливать при нажатии на кнопку
"""

import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from a_threads import *


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Инициализация элементов окна
        layout = QVBoxLayout()

        # Поля ввода координат
        hbox_lat_long = QHBoxLayout()
        label_lat = QLabel("Широта:")
        self.lat_input = QLineEdit()
        label_lon = QLabel("Долгота:")
        self.lon_input = QLineEdit()
        hbox_lat_long.addWidget(label_lat)
        hbox_lat_long.addWidget(self.lat_input)
        hbox_lat_long.addWidget(label_lon)
        hbox_lat_long.addWidget(self.lon_input)

        # Поле для выбора задержки
        delay_layout = QHBoxLayout()
        label_delay = QLabel("Интервал (секунды):")
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 60)
        self.delay_spinbox.setValue(10)
        delay_layout.addWidget(label_delay)
        delay_layout.addWidget(self.delay_spinbox)

        # Кнопка для управления потоком
        self.start_stop_button = QPushButton("Запрос данных")
        self.start_stop_button.clicked.connect(self.toggle_thread)

        # Метка для отображения погодных данных
        self.weather_label = QLabel("Информация о погоде.")
        font = QFont()
        font.setPointSize(12)
        self.weather_label.setFont(font)

        # Добавляем элементы в общий макет
        layout.addLayout(hbox_lat_long)
        layout.addLayout(delay_layout)
        layout.addWidget(self.start_stop_button)
        layout.addWidget(self.weather_label)

        self.setLayout(layout)

        # Начальные настройки
        self.thread = None
        self.is_running = False

    def toggle_thread(self):
        """Метод переключения состояния потока."""
        if not self.is_running:
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            interval = int(self.delay_spinbox.value())

            # Блокируем поля ввода
            self.lat_input.setDisabled(True)
            self.lon_input.setDisabled(True)
            self.delay_spinbox.setDisabled(True)

            # Создание и запуск нового потока
            self.thread = WeatherHandler(lat, lon)
            self.thread.setDelay(interval)
            self.thread.weatherDataReceived.connect(self.update_weather_data)
            self.thread.finished.connect(self.on_thread_finished)
            self.thread.start()
            self.is_running = True
            self.start_stop_button.setText("Остановить получение данных")
        else:
            # Останавливаем поток
            self.stop_thread()

    def stop_thread(self):
        """Останавливает поток и разблокирует поля ввода."""
        if self.thread is not None and self.is_running:
            self.thread.status = False
            self.thread.wait()
            self.thread.deleteLater()
            self.thread = None

        # Разблокировка полей ввода
        self.lat_input.setEnabled(True)
        self.lon_input.setEnabled(True)
        self.delay_spinbox.setEnabled(True)
        self.is_running = False
        self.start_stop_button.setText("Запустить получение данных")

    def update_weather_data(self, data):
        """Обновляет метку с информацией о погоде."""
        temperature = data['temperature']
        wind_speed = data['windspeed']
        text = f"Температура: {temperature:.1f}°C\nСкорость ветра: {wind_speed:.1f} м/с"
        self.weather_label.setText(text)

    def on_thread_finished(self):
        """Выполняется при завершении потока."""
        self.stop_thread()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())