from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi() # Вызовите метод для инициализации интерфейса

    def initUi(self) -> None:
        """
        Инициализация интерфейса

        :return: None
        """

        labelLogin = QtWidgets.QLabel("Логин")  # Создайте виджет QLabel с текстом "Логин"
        labelRegistration = QtWidgets.QLabel("Регистрация")  # Создайте виджет QLabel с текстом "Регистрация"

        # Поле ввода пароля
        self.lineEditLogin = QtWidgets.QLineEdit()  # создайте виджет QLineEdit
        self.lineEditLogin.setPlaceholderText("Введите логин")  # добавьте placeholderText "Введите логин" с помощью метода .setPlaceholderText()

        # Поле регистрации
        self.lineEditPassword = QtWidgets.QLineEdit()  # создайте виджет QLineEdit
        self.lineEditPassword.setPlaceholderText("Введите пароль")  # добавьте placeholderText "Введите пароль"
        self.lineEditPassword.setEchoMode(QtWidgets.QLineEdit.Password)  # установите ограничение видимости вводимых знаков с помощью метода .setEchoMode()

        # Кнопка входа
        self.pushButtonLogin = QtWidgets.QPushButton()  # создайте виджет QPushButton
        self.pushButtonLogin.setText("Войти")  # установите текст "Войти" с помощью метода setText()

        # Кнопка регистрации
        self.pushButtonRegistration = QtWidgets.QPushButton()  # создайте виджет QPushButton
        self.pushButtonRegistration.setText("Регистрация") # установите текст "Регистрация" с помощью метода setText()

        # Компоновка
        layoutLogin = QtWidgets.QHBoxLayout()  # Создайте QHBoxLayout
        layoutLogin.addWidget(labelLogin)  # с помощью метода .addWidget() добавьте labelLogin
        layoutLogin.addWidget(self.lineEditLogin)  # с помощью метода .addWidget() добавьте self.lineEditLogin

        layoutPassword = QtWidgets.QHBoxLayout()  # Создайте QHBoxLayout
        layoutPassword.addWidget(labelRegistration)  # с помощью метода .addWidget() добавьте labelRegistration
        layoutPassword.addWidget(self.lineEditPassword)  # с помощью метода .addWidget() добавьте self.lineEditPassword

        layoutButtons = QtWidgets.QHBoxLayout()  #  Создайте QHBoxLayout
        layoutButtons.addWidget(self.pushButtonLogin) # с помощью метода .addWidget() добавьте self.pushButtonLogin
        layoutButtons.addWidget(self.pushButtonRegistration)  # с помощью метода .addWidget() добавьте self.pushButtonRegistration

        # Основная вертикальная компоновка
        layoutMain = QtWidgets.QVBoxLayout()  # Создайте QVBoxLayout
        layoutMain.addLayout(layoutLogin)  # с помощью метода .addLayout() добавьте layoutLogin
        layoutMain.addLayout(layoutPassword) # с помощью метода .addLayout() добавьте layoutPassword
        layoutMain.addLayout(layoutButtons)  # с помощью метода .addLayout() добавьте layoutButtons

        self.setLayout(layoutMain)  # с помощью метода setLayout установите layoutMain на основной виджет


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
