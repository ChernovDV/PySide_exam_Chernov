"""
Реализовать окно, которое будет объединять в себе сразу два предыдущих виджета
"""
import sys
from PySide6.QtGui import QFont
from PySide6.QtWidgets import *

from a_threads import *

class SystemInfo(QThread):
    systemInfoReceived = Signal(list)  # Сигнал для передачи списка с информацией о ресурсах

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = 1  # Начальная задержка в секунду

    def run(self) -> None:
        while True:
            cpu_value = psutil.cpu_percent(interval=1)  # Процент нагрузки на процессор
            ram_value = psutil.virtual_memory().percent  # Процент используемой оперативной памяти
            self.systemInfoReceived.emit([cpu_value, ram_value])
            time.sleep(self.delay)

class WeatherHandler(QThread):
    weatherDataReceived = Signal(dict)  # Сигнал для отправки данных о погоде

    def __init__(self, latitude, longitude, parent=None):
        super().__init__(parent)
        self.api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        self.delay = 10  # Интервал запросов составляет 10 секунд
        self.status = True  # Флаг активности потока

    def setDelay(self, new_delay):
        self.delay = new_delay

    def run(self) -> None:
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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        # Запуск потоков сбора данных
        self.sysinfo_thread = SystemInfo()
        self.sysinfo_thread.systemInfoReceived.connect(self.update_system_info)
        self.sysinfo_thread.start()

    def initUI(self):
        layout = QVBoxLayout()

        # Поле для установки интервала опроса
        self.delay_input = QLineEdit("1")
        self.delay_input.textChanged.connect(self.change_delay)
        layout.addWidget(QLabel("Интервал опроса (секунды):"))
        layout.addWidget(self.delay_input)

        # Индикатор CPU Load
        self.cpu_label = QLabel("Загрузка CPU: ")
        layout.addWidget(self.cpu_label)

        # Индикатор RAM Usage
        self.ram_label = QLabel("Использование RAM: ")
        layout.addWidget(self.ram_label)

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
        layout.addLayout(hbox_lat_long)

        # Поле для выбора задержки
        delay_layout = QHBoxLayout()
        label_delay = QLabel("Интервал (секунды):")
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setRange(1, 60)
        self.delay_spinbox.setValue(10)
        delay_layout.addWidget(label_delay)
        delay_layout.addWidget(self.delay_spinbox)
        layout.addLayout(delay_layout)

        # Кнопка для управления потоком
        self.start_stop_button = QPushButton("Запрос данных")
        self.start_stop_button.clicked.connect(self.toggle_thread)
        layout.addWidget(self.start_stop_button)

        # Метка для отображения погодных данных
        self.weather_label = QLabel("Информация о погоде.")
        font = QFont()
        font.setPointSize(12)
        self.weather_label.setFont(font)
        layout.addWidget(self.weather_label)

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

    def toggle_thread(self):
        """Метод переключения состояния потока."""
        if not hasattr(self, 'weather_thread') or not self.weather_thread.isRunning():
            lat = float(self.lat_input.text())
            lon = float(self.lon_input.text())
            interval = int(self.delay_spinbox.value())

            # Блокируем поля ввода
            self.lat_input.setDisabled(True)
            self.lon_input.setDisabled(True)
            self.delay_spinbox.setDisabled(True)

            # Создание и запуск нового потока
            self.weather_thread = WeatherHandler(lat, lon)
            self.weather_thread.setDelay(interval)
            self.weather_thread.weatherDataReceived.connect(self.update_weather_data)
            self.weather_thread.finished.connect(self.on_thread_finished)
            self.weather_thread.start()
            self.is_running = True
            self.start_stop_button.setText("Остановить получение данных")
        else:
            # Останавливаем поток
            self.stop_thread()

    def stop_thread(self):
        """Останавливает поток и разблокирует поля ввода."""
        if hasattr(self, 'weather_thread') and self.weather_thread.isRunning():
            self.weather_thread.status = False
            self.weather_thread.wait()
            del self.weather_thread

        # Разблокировка полей ввода
        self.lat_input.setEnabled(True)
        self.lon_input.setEnabled(True)
        self.delay_spinbox.setEnabled(True)
        self.is_running = False
        self.start_stop_button.setText("Запустить получение данных")

    def update_weather_data(self, weather_data):
        """Обновляет метку с информацией о погоде."""
        temperature = weather_data['temperature']
        wind_speed = weather_data['windspeed']
        text = f"Температура: {temperature:.1f}°C\nСкорость ветра: {wind_speed:.1f} м/с"
        self.weather_label.setText(text)

    def on_thread_finished(self):
        """Выполняется при завершении потока."""
        self.stop_thread()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())