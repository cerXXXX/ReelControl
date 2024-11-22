# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6 import QtGui
from MainWindow import *


class LoginPage(QWidget):
    """Страница входа"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("parent")
        parent.resize(512, 570)

        # основной layout
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # кнопка входа
        self.Login = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Login.setFont(font)
        self.Login.setObjectName("Login")

        self.verticalLayout.addWidget(self.Login, 0,
                                      QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        # кнопка регистрации
        self.signup = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.signup.setFont(font)
        self.signup.setObjectName("signup")

        self.verticalLayout.addWidget(self.signup, 0,
                                      QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        # устанавливаем названия кнопок
        self.setWindowTitle("Вход")
        self.Login.setText("Войти")
        self.signup.setText("Зарегистрироваться")

        # подключаем кнопки
        self.Login.clicked.connect(lambda: self.login_func(parent))
        self.signup.clicked.connect(lambda: self.signup_func(parent))

    def login_func(self, parent=None):

        """Вызывается при нажатии на кнопку входа"""

        # открываем диалог входа
        dlg = LoginDialog(self)
        if dlg.exec():
            if dlg.role == "Admin":
                # если роль — админ, переключаем на окно админа
                parent.stacked.setCurrentIndex(1)
                parent.resize(759, 445)
                parent.setWindowTitle("Администратор")
                parent.admin_name = dlg.form_layout.itemAt(1).widget().text()
                parent.cashier_name = ''
            elif dlg.role == "Cashier":
                # если роль — кассир, переключаем на окно кассира
                parent.stacked.setCurrentIndex(2)
                parent.resize(759, 445)
                parent.setWindowTitle("Кассир")
                parent.admin_name = ''
                parent.cashier_name = dlg.form_layout.itemAt(1).widget().text()
                parent.stacked.widget(2).update_data()

    def signup_func(self, parent=None):
        """Вызывается при нажатии на кнопку регистрации"""

        # открываем диалог регистрации
        dlg = RegisterDialog(self)
        if dlg.exec():
            if dlg.role == "Admin":
                # если роль — админ, переключаем на окно админа
                parent.stacked.setCurrentIndex(1)
                parent.resize(759, 445)
                parent.setWindowTitle("Admin")
            elif dlg.role == "Cashier":
                # если роль — кассир, переключаем на окно кассира
                parent.stacked.setCurrentIndex(2)
                parent.resize(759, 445)
                parent.setWindowTitle("Кассир")


class MainClass(QMainWindow):
    """Класс главного окна"""

    def __init__(self):
        super().__init__()
        self.resize(512, 570)

        # виджет для всех окон
        self.stacked = QStackedWidget(self)

        # если БД нет, создадим ее
        if not get_databases():
            create_database()

        # имя кассира или админа
        self.cashier_name = ''
        self.admin_name = ''

        # основное меню
        self.menu = None

        # подменю для баз данных
        self.database_menu = None

    def setup_ui(self):
        """Инициализация окна"""

        self.setWindowTitle("Вход")
        self.resize(512, 570)

        self.setCentralWidget(self.stacked)

        # страница входа
        a = LoginPage(self)
        self.stacked.addWidget(a)

        # страница админа
        b = AdminPage(self)
        self.stacked.addWidget(b)

        # страница кассира
        c = CashierPage(self)
        self.stacked.addWidget(c)

        # добавляем меню
        self.menu = QtWidgets.QMenu("&Меню", self)
        self.menuBar().addMenu(self.menu)

        # получаем список баз данных
        databases = get_databases()

        # добавляем подменю для баз данных
        self.database_menu = self.menu.addMenu("&Базы данных")

        # добавляем базы данных в меню для баз данных
        for database in databases:
            # иконка базы данных
            action = QtGui.QAction(QtGui.QIcon().fromTheme("drive-harddisk"), database, self)
            action.triggered.connect(self.set_database)
            self.database_menu.addAction(action)

        # кнопка добавить базу данных в меню баз данных
        add_database = QtGui.QAction(QtGui.QIcon().fromTheme("list-add"), 'Добавить базу данных', self)
        add_database.triggered.connect(self.add_database)
        self.database_menu.addAction(add_database)

        # кнопка обновить в основном меню
        action = QtGui.QAction(QtGui.QIcon().fromTheme("view-refresh"), '&Обновить', self)
        action.triggered.connect(self.refresh)
        self.menu.addAction(action)

        # кнопка выхода в основном меню
        action = QtGui.QAction(QtGui.QIcon().fromTheme("system-log-out"), '&Выйти', self)
        action.triggered.connect(self.logout_click)
        self.menu.addAction(action)

    def set_database(self):
        """Устанавливаем базу данных"""

        set_database_name('database/' + self.sender().text() + '.db')
        if get_cinemas():
            db = get_cinemas()[0]
        else:
            db = ''
        self.stacked.widget(1).curr_cinema = db
        self.stacked.widget(2).curr_cinema = db
        self.stacked.widget(1).update_data()
        self.stacked.widget(2).update_data()

        self.logout_click()

    def logout_click(self):
        """Вызывается при нажатии на кнопку выхода"""

        # выкидываем пользователя на окно входа
        if self.stacked.currentIndex() != 0:
            self.stacked.setCurrentIndex(0)
            self.resize(512, 570)
            self.setWindowTitle("Вход")
            self.admin_name = ''
            self.cashier_name = ''

    def add_database(self):
        """Добавляем базу данных"""

        # диалог добавления базы данных
        dlg = AddDatabaseDialog(self)

        if dlg.exec():
            # получаем список баз данных
            databases = get_databases()

            # очищаем меню баз данных
            self.database_menu.clear()

            # добавляем все базы данных в меню
            for database in databases:
                action = QtGui.QAction(QtGui.QIcon().fromTheme("drive-harddisk"), database, self)
                action.triggered.connect(self.set_database)
                self.database_menu.addAction(action)

            # кнопка добавить базу данных в меню баз данных
            add_database = QtGui.QAction(QtGui.QIcon().fromTheme("list-add"), 'Добавить базу данных', self)
            add_database.triggered.connect(self.add_database)
            self.database_menu.addAction(add_database)

    def refresh(self):
        """Обновляем данные"""

        self.stacked.widget(1).update_data()
        self.stacked.widget(2).update_data()
