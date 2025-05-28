"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущий основной монитор
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""
import sys
from datetime import datetime
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGroupBox, QHBoxLayout, QVBoxLayout, \
    QPlainTextEdit, QSpinBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Заголовок окна
        self.setWindowTitle('Окно мониторинга')

        # Элементы интерфейса
        group_box_move = QGroupBox("Перемещение окна:")
        layout_move = QVBoxLayout(group_box_move)

        # Кнопки направления движения окна
        hbox_top = QHBoxLayout()
        btn_left_top = QPushButton("Лево/Верх")
        btn_right_top = QPushButton("Право/Верх")
        hbox_top.addWidget(btn_left_top)
        hbox_top.addWidget(btn_right_top)
        layout_move.addLayout(hbox_top)

        btn_center = QPushButton("Центр")
        layout_move.addWidget(btn_center)

        hbox_bottom = QHBoxLayout()
        btn_left_bottom = QPushButton("Лево/Низ")
        btn_right_bottom = QPushButton("Право/Низ")
        hbox_bottom.addWidget(btn_left_bottom)
        hbox_bottom.addWidget(btn_right_bottom)
        layout_move.addLayout(hbox_bottom)

        # Перемещение по заданным координатам
        group_box_coords = QGroupBox("Переместить в координаты:")
        layout_coords = QVBoxLayout(group_box_coords)
        hbox_coords = QHBoxLayout()
        label_x = QLabel("X:")
        spin_x = QSpinBox()
        label_y = QLabel("Y:")
        spin_y = QSpinBox()
        hbox_coords.addWidget(label_x)
        hbox_coords.addWidget(spin_x)
        hbox_coords.addWidget(label_y)
        hbox_coords.addWidget(spin_y)
        layout_coords.addLayout(hbox_coords)
        btn_move_to = QPushButton("Переместить")
        layout_coords.addWidget(btn_move_to)

        # Лог сообщений
        log_group = QGroupBox("Лог:")
        log_layout = QHBoxLayout(log_group)
        self.log_text_edit = QPlainTextEdit()
        log_layout.addWidget(self.log_text_edit)

        # Получение данных окна
        btn_get_data = QPushButton("Получить данные окна")

        # Основные компоновщики элементов
        main_hbox = QHBoxLayout()
        vbox_left = QVBoxLayout()
        vbox_right = QVBoxLayout()

        vbox_left.addWidget(group_box_move)
        vbox_left.addWidget(group_box_coords)
        vbox_right.addWidget(log_group)
        vbox_right.addWidget(btn_get_data)

        main_hbox.addLayout(vbox_left)
        main_hbox.addLayout(vbox_right)

        self.setLayout(main_hbox)

        # Обработчики кнопок
        btn_left_top.clicked.connect(lambda: self.move_to_corner(Qt.LeftEdge, Qt.TopEdge))
        btn_right_top.clicked.connect(lambda: self.move_to_corner(Qt.RightEdge, Qt.TopEdge))
        btn_left_bottom.clicked.connect(lambda: self.move_to_corner(Qt.LeftEdge, Qt.BottomEdge))
        btn_right_bottom.clicked.connect(lambda: self.move_to_corner(Qt.RightEdge, Qt.BottomEdge))
        btn_center.clicked.connect(self.center_window)
        btn_move_to.clicked.connect(lambda: self.move_to_coords(spin_x.value(), spin_y.value()))
        btn_get_data.clicked.connect(self.get_window_data)

        # Инициализация размеров и позиции окна
        self.resize(800, 600)
        self.center_window()

    def move_to_corner(self, horizontal_edge, vertical_edge):
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        x_pos = 0 if horizontal_edge == Qt.LeftEdge else screen_geometry.width() - self.width()
        y_pos = 0 if vertical_edge == Qt.TopEdge else screen_geometry.height() - self.height()
        old_position = f'({self.x()}, {self.y()})'
        new_position = f'({x_pos}, {y_pos})'
        print(f'{datetime.now()} - Окно переместилось с {old_position} на {new_position}')
        self.move(x_pos, y_pos)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        old_position = f'({self.x()}, {self.y()})'
        new_position = f'({qr.left()}, {qr.top()})'
        print(f'{datetime.now()} - Окно переместилось с {old_position} на {new_position}')

    def move_to_coords(self, x, y):
        old_position = f'({self.x()}, {self.y()})'
        new_position = f'({x}, {y})'
        print(f'{datetime.now()} - Окно переместилось с {old_position} на {new_position}')
        self.move(x, y)

    def get_window_data(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        screens_count = len(QGuiApplication.screens())
        primary_screen = QGuiApplication.primaryScreen()
        resolution = primary_screen.geometry().size()
        window_size = self.size()
        min_size = self.minimumSize()
        pos = self.pos()
        center_point = self.rect().center()
        state = 'Активное' if self.isActiveWindow() else 'Не активное'
        visible_state = 'Отображается' if self.isVisible() else 'Скрыто'
        minimized_state = 'Развёрнутое' if not self.isMinimized() else 'Минимизированное'

        data_log = (
            f"{current_time}\n"
            f"Количество экранов: {screens_count}\n"
            f"Текущий основной монитор: {primary_screen.name()}\n"
            f"Разрешение основного монитора: {resolution.width()}x{resolution.height()}\n"
            f"Размеры окна: {window_size.width()}x{window_size.height()}\n"
            f"Минимальные размеры окна: {min_size.width()}x{min_size.height()}\n"
            f"Положение окна: ({pos.x()},{pos.y()})\n"
            f"Центральная точка окна: ({center_point.x()},{center_point.y()})\n"
            f"Состояние окна: {state}/{visible_state}/{minimized_state}"
        )
        self.log_text_edit.appendPlainText(data_log)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec())