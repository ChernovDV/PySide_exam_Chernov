import random

from PySide6 import QtWidgets, QtCore


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initSignals()

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        # comboBox -----------------------------------------------------------
        self.comboBox = QtWidgets.QComboBox()
        self.comboBox.addItem("Элемент 1")
        self.comboBox.addItem("Элемент 2")
        self.comboBox.addItems(["Элемент 3", "Элемент 4", "Элемент 5"])
        self.comboBox.insertItem(0, "")

        self.pushButtonComboBox = QtWidgets.QPushButton("Получить данные")

        layoutComboBox = QtWidgets.QHBoxLayout()
        layoutComboBox.addWidget(self.comboBox)
        layoutComboBox.addWidget(self.pushButtonComboBox)

        # lineEdit -----------------------------------------------------------
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Введите текст")

        self.pushButtonLineEdit = QtWidgets.QPushButton("Получить данные")

        layoutLineEdit = QtWidgets.QHBoxLayout()
        layoutLineEdit.addWidget(self.lineEdit)
        layoutLineEdit.addWidget(self.pushButtonLineEdit)

        # textEdit -----------------------------------------------------------
        self.textEdit = QtWidgets.QTextEdit()
        self.textEdit.setPlaceholderText("Введите текст")

        self.pushButtonTextEdit = QtWidgets.QPushButton("Получить данные")

        layoutTextEdit = QtWidgets.QHBoxLayout()
        layoutTextEdit.addWidget(self.textEdit)
        layoutTextEdit.addWidget(self.pushButtonTextEdit)

        # plainTextEdit ------------------------------------------------------
        self.plainTextEdit = QtWidgets.QPlainTextEdit()
        self.plainTextEdit.setPlaceholderText("Введите текст")

        self.pushButtonPlainTextEdit = QtWidgets.QPushButton("Получить данные")

        layoutPlainTextEdit = QtWidgets.QHBoxLayout()
        layoutPlainTextEdit.addWidget(self.plainTextEdit)
        layoutPlainTextEdit.addWidget(self.pushButtonPlainTextEdit)

        # spinBox ------------------------------------------------------------
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setValue(random.randint(-50, 50))

        self.pushButtonSpinBox = QtWidgets.QPushButton("Получить данные")

        layoutSpinBox = QtWidgets.QHBoxLayout()
        layoutSpinBox.addWidget(self.spinBox)
        layoutSpinBox.addWidget(self.pushButtonSpinBox)

        # doubleSpinBox ------------------------------------------------------
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox()
        self.doubleSpinBox.setValue(random.randint(-50, 50))

        self.pushButtonDoubleSpinBox = QtWidgets.QPushButton("Получить данные")

        layoutDoubleSpinBox = QtWidgets.QHBoxLayout()
        layoutDoubleSpinBox.addWidget(self.doubleSpinBox)
        layoutDoubleSpinBox.addWidget(self.pushButtonDoubleSpinBox)

        # timeEdit -----------------------------------------------------------
        self.timeEdit = QtWidgets.QTimeEdit()
        self.timeEdit.setTime(QtCore.QTime.currentTime().addSecs(random.randint(-10000, 10000)))

        self.pushButtonTimeEdit = QtWidgets.QPushButton("Получить данные")

        layoutTimeEdit = QtWidgets.QHBoxLayout()
        layoutTimeEdit.addWidget(self.timeEdit)
        layoutTimeEdit.addWidget(self.pushButtonTimeEdit)

        # dateTimeEdit -------------------------------------------------------
        self.dateTimeEdit = QtWidgets.QDateTimeEdit()
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime().addDays(random.randint(-10, 10)))

        self.pushButtonDateTimeEdit = QtWidgets.QPushButton("Получить данные")

        layoutDateTimeEdit = QtWidgets.QHBoxLayout()
        layoutDateTimeEdit.addWidget(self.dateTimeEdit)
        layoutDateTimeEdit.addWidget(self.pushButtonDateTimeEdit)

        # plainTextEditLog ---------------------------------------------------
        self.plainTextEditLog = QtWidgets.QPlainTextEdit()

        self.pushButtonClearLog = QtWidgets.QPushButton("Очистить лог")

        layoutLog = QtWidgets.QHBoxLayout()
        layoutLog.addWidget(self.plainTextEditLog)
        layoutLog.addWidget(self.pushButtonClearLog)

        # main layout

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutComboBox)
        layoutMain.addLayout(layoutLineEdit)
        layoutMain.addLayout(layoutTextEdit)
        layoutMain.addLayout(layoutPlainTextEdit)
        layoutMain.addLayout(layoutSpinBox)
        layoutMain.addLayout(layoutDoubleSpinBox)
        layoutMain.addLayout(layoutTimeEdit)
        layoutMain.addLayout(layoutDateTimeEdit)
        layoutMain.addLayout(layoutLog)

        self.setLayout(layoutMain)

    def initSignals(self) -> None:
        """
        Инициализация сигналов

        :return: None
        """
        # Подключение обработчиков кнопок
        self.pushButtonComboBox.clicked.connect(self.onPushButtonComboBoxClicked)  # подключить слот для вывода текста из comboBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonLineEdit.clicked.connect(self.onPushButtonLineEditClicked)
        self.pushButtonTextEdit.clicked.connect(self.onPushButtonTextEditClicked)  # подключить слот для вывода текста из textEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonPlainTextEdit.clicked.connect(self.onPushButtonPlainTextEditClicked)  # подключить слот для вывода текста из plaineTextEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonSpinBox.clicked.connect(self.onPushButtonSpinBoxClicked)  # подключить слот для вывода значения из spinBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonDoubleSpinBox.clicked.connect(self.onPushButtonDoubleSpinBoxClicked)  # подключить слот для вывода значения из doubleSpinBox в plainTextEditLog при нажатии на кнопку
        self.pushButtonTimeEdit.clicked.connect(self.onPushButtonTimeEditClicked)  # подключить слот для вывода времени из timeEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonDateTimeEdit.clicked.connect(self.onPushButtonDateTimeEditClicked)  # подключить слот для вывода времени из dateTimeEdit в plainTextEditLog при нажатии на кнопку
        self.pushButtonClearLog.clicked.connect(self.onPushButtonClearLogClicked)  # подключить слот для очистки plainTextEditLog при нажатии на кнопку

        # Сигналы изменений виджетов
        self.comboBox.currentIndexChanged.connect(self.onComboBoxCurrentIndexChanged)  # подключить слот для вывода текста в plainTextEditLog при изменении выбранного элемента в comboBox
        self.spinBox.valueChanged.connect(self.onSpinBoxValueChanged)  # подключить слот для вывода значения в plainTextEditLog при изменении значения в spinBox
        self.dateTimeEdit.dateTimeChanged.connect(self.onDateTimeEditDateTimeChanged)  # подключить слот для вывода датывремени в plainTextEditLog при изменении датывремени в dateTimeEdit

    # slots --------------------------------------------------------------
    def onPushButtonLineEditClicked(self) -> None:
        """
        Обработка сигнала clicked для кнопки pushButtonLineEdit
        :return: None
        """

        current_text = self.lineEdit.text()
        if current_text.strip():
            self.plainTextEditLog.appendPlainText(f"Введён текст: {current_text}")

    def onPushButtonComboBoxClicked(self) -> None:
    # Самостоятельная реализация слотов для сигналов
        selected_item = self.comboBox.currentText()
        if selected_item.strip():
            self.plainTextEditLog.appendPlainText(f"Выбран элемент: {selected_item}")

    def onPushButtonTextEditClicked(self) -> None:
        content = self.textEdit.toPlainText()
        if content.strip():
            self.plainTextEditLog.appendPlainText(f"Текст: {content}")

    def onPushButtonPlainTextEditClicked(self) -> None:
        content = self.plainTextEdit.toPlainText()
        if content.strip():
            self.plainTextEditLog.appendPlainText(f"Простой текст: {content}")

    def onPushButtonSpinBoxClicked(self) -> None:
        value = str(self.spinBox.value())
        self.plainTextEditLog.appendPlainText(f"Счетчик: {value}")

    def onPushButtonDoubleSpinBoxClicked(self) -> None:
        value = str(self.doubleSpinBox.value())
        self.plainTextEditLog.appendPlainText(f"Двойной счётчик: {value}")

    def onPushButtonTimeEditClicked(self) -> None:
        time_value = self.timeEdit.time().toString("hh:mm:ss")
        self.plainTextEditLog.appendPlainText(f"Время: {time_value}")

    def onPushButtonDateTimeEditClicked(self) -> None:
        datetime_value = self.dateTimeEdit.dateTime().toString("dd-MM-yyyy hh:mm:ss")
        self.plainTextEditLog.appendPlainText(f"Дата и время: {datetime_value}")

    def onPushButtonClearLogClicked(self) -> None:
        self.plainTextEditLog.clear()

    def onComboBoxCurrentIndexChanged(self, index: int) -> None:
        item = self.comboBox.itemText(index)
        self.plainTextEditLog.appendPlainText(f"Комбобокс изменил выбор: {item}")

    def onSpinBoxValueChanged(self, value: int) -> None:
        self.plainTextEditLog.appendPlainText(f"Значение спинбокса изменилось: {value}")

    def onDateTimeEditDateTimeChanged(self, dt: QtCore.QDateTime) -> None:
        formatted_dt = dt.toString("dd-MM-yyyy hh:mm:ss")
        self.plainTextEditLog.appendPlainText(f"Дата и время изменились: {formatted_dt}")

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
