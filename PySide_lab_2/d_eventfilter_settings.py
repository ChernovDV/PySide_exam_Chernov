"""
Реализация программу взаимодействия виджетов друг с другом:
Форма для приложения (ui/d_eventfilter_settings_form.ui)

Программа должна обладать следующим функционалом:

1. Добавить для dial возможность установки значений кнопками клавиатуры(+ и -),
   выводить новые значения в консоль

2. Соединить между собой QDial, QSlider, QLCDNumber
   (изменение значения в одном, изменяет значения в других)

3. Для QLCDNumber сделать отображение в различных системах счисления (oct, hex, bin, dec),
   изменять формат отображаемого значения в зависимости от выбранного в comboBox параметра.

4. Сохранять значение выбранного в comboBox режима отображения
   и значение LCDNumber в QSettings, при перезапуске программы выводить
   в него соответствующие значения
"""

from PySide6 import QtWidgets, QtCore
import os
from PySide6.QtCore import QSettings

# Путь к файлу конфигурации
settings_file_path = os.path.join(os.path.expanduser("~"), ".config", "myapp.ini")


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        l = QtWidgets.QVBoxLayout()

        # Создание интерфейса
        self.lcd_modes = {
            "hex": QtWidgets.QLCDNumber.Mode.Hex,
            "dec": QtWidgets.QLCDNumber.Mode.Dec,
            "oct": QtWidgets.QLCDNumber.Mode.Oct,
            "bin": QtWidgets.QLCDNumber.Mode.Bin,
        }

        self.dial = QtWidgets.QDial()
        self.dial.valueChanged.connect(self.onValueChanged)
        self.dial.installEventFilter(self)
        self.lcd = QtWidgets.QLCDNumber()
        self.lcd.display(14)
        self.lcd.setMinimumHeight(60)
        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.cb = QtWidgets.QComboBox()
        self.cb.addItems(list(self.lcd_modes.keys()))  # Список возможных форматов
        self.cb.currentTextChanged.connect(
            lambda mode: self.lcd.setMode(self.lcd_modes.get(mode))
        )

        # Добавляем компоненты в макет
        l.addWidget(self.dial)
        l.addWidget(self.lcd)
        l.addWidget(self.slider)
        l.addWidget(self.cb)

        self.setLayout(l)

        # Загрузка предыдущих настроек
        self.load_settings()

    def onValueChanged(self, value):
        """Обработчик изменения значения."""
        self.dial.setValue(value)
        self.slider.setValue(value)
        self.lcd.display(value)

    def eventFilter(self, watched, event):
        """Фильтр событий для реакции на нажатия клавиш."""
        if watched == self.dial and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Minus:
                new_value = max(0, self.dial.value() - 1)
                print(f'Значение уменьшено до {new_value}')
                self.dial.setValue(new_value)
            elif event.key() == QtCore.Qt.Key.Key_Plus:
                new_value = min(self.dial.maximum(), self.dial.value() + 1)
                print(f'Значение увеличено до {new_value}')
                self.dial.setValue(new_value)

        return super().eventFilter(watched, event)

    def closeEvent(self, event):
        """Сохранение настроек при закрытии окна."""
        settings = QSettings(settings_file_path, QSettings.Format.IniFormat)
        settings.beginGroup('Main')
        settings.setValue('last_lcd_mode', self.cb.currentText())  # Запоминаем выбранный режим
        settings.setValue('last_lcd_value', int(self.lcd.value()))  # Текущее значение
        settings.endGroup()
        event.accept()

    def load_settings(self):
        """Загружаем предыдущие настройки."""
        settings = QSettings(settings_file_path, QSettings.Format.IniFormat)
        settings.beginGroup('Main')
        last_lcd_mode = settings.value('last_lcd_mode', 'dec')  # По умолчанию Decimal
        last_lcd_value = settings.value('last_lcd_value', 14)  # Начальное значение
        settings.endGroup()
        self.cb.setCurrentText(last_lcd_mode)
        self.lcd.display(int(last_lcd_value))
        self.onValueChanged(int(last_lcd_value))  # Обновляем остальные элементы


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = Window()
    window.show()
    app.exec()
