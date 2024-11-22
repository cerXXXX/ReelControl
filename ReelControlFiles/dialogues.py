# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QMessageBox, QPushButton
from PyQt6 import QtWidgets
from PyQt6 import QtCore
import string
import datetime

from database import *


def remove_duplicates(nested_list) -> list:
    """Удалить повторяющиеся элементы в списке"""
    unique_list = []
    for element in nested_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


class BigRow(QtWidgets.QWidget):
    """Виджет из двух label в одну строку"""

    def __init__(self, *args) -> None:
        super().__init__()
        self.left = QtWidgets.QLabel()
        self.right = QtWidgets.QLabel()

        # Если получили str для обоих label
        if args:
            self.left.setText(args[0])
            self.right.setText(args[1])

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.left)
        layout.addWidget(self.right, alignment=QtCore.Qt.AlignmentFlag.AlignRight)


class LoginDialog(QDialog):
    """Диалоговое окно для входа"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Вход")

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()

        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("&Имя:", QtWidgets.QLineEdit())

        self.form_layout.addRow("&Пароль:", QtWidgets.QLineEdit())

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

        self.role = None

    def accept(self) -> None:
        """Переопределение accept"""
        self.role = check_user(self.form_layout.itemAt(1).widget().text(), self.form_layout.itemAt(3).widget().text())
        if not self.role:
            self.statusbar.showMessage("Неверный логин или пароль")
        else:
            super().accept()


class RegisterDialog(QDialog):
    """Диалоговое окно для регистрации"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Регистрация")

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout со всеми элементами
        self.layout = QtWidgets.QVBoxLayout()

        # Layout с формой для заполнения
        self.form_layout = QtWidgets.QFormLayout()

        self.form_layout.addRow("&Имя:", QtWidgets.QLineEdit())

        # Список ролей
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItem('Админ')
        self.combobox.addItem('Кассир')

        self.form_layout.addRow("&Роль:", self.combobox)
        self.form_layout.addRow("&Пароль:", QtWidgets.QLineEdit())
        self.form_layout.addRow("&Подтвердить пароль:", QtWidgets.QLineEdit())

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

        # Основные переменные
        self.name = ''
        self.role = ''
        self.password = ''
        self.confirm_password = ''

    def accept(self) -> None:
        """Переопределение accept"""

        # Получаем данные из формы
        self.name = self.form_layout.itemAt(1).widget().text()
        self.role = self.combobox.currentText()
        self.password = self.form_layout.itemAt(5).widget().text()
        self.confirm_password = self.form_layout.itemAt(7).widget().text()

        # Проверяем данные на корректность
        if ';' in self.name:
            self.statusbar.showMessage("В имени не должно быть ';'")
        elif ';' in self.password:
            self.statusbar.showMessage("В пароле не должно быть ';'")
        elif not self.password:
            self.statusbar.showMessage("Пароль не может быть пустым")
        elif not self.name:
            self.statusbar.showMessage("Логин не может быть пустым")
        elif check_login_name(self.name):
            self.statusbar.showMessage("Такой логин уже существует")
        elif len(self.password) < 8:
            self.statusbar.showMessage("Пароль должен быть не менее 8 символов")
        elif not self.confirm_password:
            self.statusbar.showMessage("Повторите пароль")
        elif self.password != self.confirm_password:
            self.statusbar.showMessage("Пароли не совпадают")
        else:
            # Добавляем пользователя
            write_user(self.name, self.role, self.password)
            super().accept()


class DeleteDialog(QDialog):
    """Диалоговое окно для подтверждения удаления"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Подтверждение удаления")

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()
        message = QtWidgets.QLabel("Удалить?")
        self.layout.addWidget(message, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)


class AddCinemaDialog(QDialog):
    """Диалоговое окно для добавления кинотеатра"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Добавление кинотеатра")

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()

        # Layout с формой
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("&Название:", QtWidgets.QLineEdit())

        self.form_layout.addRow("&Адрес:", QtWidgets.QLineEdit())

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

        # Основные переменные
        self.name = ''
        self.address = ''

    def accept(self) -> None:
        """Переопределение accept"""

        # Получаем данные из формы
        self.name = self.form_layout.itemAt(1).widget().text()
        self.address = self.form_layout.itemAt(3).widget().text()

        # Проверка на корректность
        if not self.name:
            self.statusbar.showMessage("Название не может быть пустым")
        elif not self.address:
            self.statusbar.showMessage("Адрес не может быть пустым")
        elif self.name in get_cinemas():
            self.statusbar.showMessage("Такой кинотеатр уже существует")
        elif ';' in self.name:
            self.statusbar.showMessage("В названии не должно быть ';'")
        elif ';' in self.address:
            self.statusbar.showMessage("В адресе не должно быть ';'")
        else:
            # Добавляем кинотеатр
            add_cinema(self.name, self.address)
            super().accept()


class AddHallDialog(QDialog):
    """Диалоговое окно для добавления зала"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Добавить кинозал")
        self.resize(1000, 600)

        # Переменные для имени и конфигурации (10x10 по 200 каждое место)
        self.name = ''
        self.configuration = [['200' for i in range(10)] for j in range(10)]

        # Виджеты для выбора размеров зала
        self.width = QtWidgets.QSpinBox(minimum=4, maximum=25, value=10)
        self.height = QtWidgets.QSpinBox(minimum=4, maximum=25, value=10)

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.buttonBox, 10, 18)

        # layout с формой
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.addRow("Название:", QtWidgets.QLineEdit())

        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.formLayout.addRow(line)

        self.width.valueChanged.connect(self.update_ui)
        self.height.valueChanged.connect(self.update_ui)

        self.formLayout.addRow("Мест в ширину:", self.width)
        self.formLayout.addRow("Мест в высоту:", self.height)

        line2 = QtWidgets.QFrame(self)
        line2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.formLayout.addRow(line2)

        # Виджет для установки цены для всех
        self.price_for_all = QtWidgets.QLineEdit('200')
        self.formLayout.addRow("Цена:", self.price_for_all)

        self.but_price_for_all = QtWidgets.QPushButton("Для всех")
        self.but_price_for_all.clicked.connect(self.set_price_for_all)
        self.formLayout.addRow(self.but_price_for_all)

        line3 = QtWidgets.QFrame(self)
        line3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.formLayout.addRow(line3)

        # Виджет для установки цены для одного
        self.price_for_one = QtWidgets.QLineEdit()
        self.formLayout.addRow("Для одного:", self.price_for_one)

        self.layout.addLayout(self.formLayout, 0, 0, 1, 10)

        # Создаем layout для отображения мест
        self.boxLayout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.boxLayout, 0, 10, 9, 9)
        for i in range(self.height.value()):
            for j in range(self.width.value()):
                a = QtWidgets.QPushButton(self.configuration[i][j])
                a.setMaximumSize(40, 20)
                a.clicked.connect(self.set_price_for_one)
                self.boxLayout.addWidget(a, i, j)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar, 11, 0, 1, 19)

    def update_ui(self) -> None:
        """Обновление ui"""

        # Сохраняем конфигурацию зала
        last_width = len(self.configuration[0])
        last_height = len(self.configuration)
        self.configuration = []
        for i in range(int(last_height)):
            a = []
            for j in range(int(last_width)):
                a.append(self.boxLayout.itemAt(int(last_width) * i + j).widget().text())
            self.configuration.append(a)

        # Изменяем boxlayout
        width = self.width.value()
        height = self.height.value()
        if last_height > height or last_width > width:
            # Если количество мест уменьшилось, то просто удаляем ряд или столбец
            self.configuration = [line[:width] for line in self.configuration]
            self.configuration = self.configuration[:height]
        else:
            # Если количество мест увеличилось, то необходимо добавить ряд или столбец
            self.configuration.extend([[self.price_for_all.text() for _ in range(width)]
                                       for i in range(height - last_height)])
            [self.configuration[i].extend(self.price_for_all.text() for _ in
                                          range(width - last_width)) for i in
             range(last_height)]

        # Полностью очищаем boxlayout
        for i in reversed(range(self.boxLayout.count())):
            self.boxLayout.itemAt(i).widget().setParent(None)

        # Добавляем места на boxlayout
        for i in range(self.height.value()):
            for j in range(self.width.value()):
                a = QtWidgets.QPushButton(self.configuration[i][j])
                a.setMaximumSize(40, 20)
                a.clicked.connect(self.set_price_for_one)
                self.boxLayout.addWidget(a, i, j)

    def set_price_for_all(self) -> None:
        """Установить цену для всех"""

        # Получаем цену
        try:
            price = int(self.price_for_all.text())
        except ValueError:
            # Если получили не число
            self.statusbar.showMessage("Цена должна быть числом")
            return

        # Если цена отрицательна
        if price < 0:
            self.statusbar.showMessage("Цена не может быть отрицательной")
            return

        # Обновляем все места
        for i in reversed(range(self.boxLayout.count())):
            self.boxLayout.itemAt(i).widget().setText(str(price))

    def set_price_for_one(self) -> None:
        """Установить цену для одного"""
        # Получаем цену
        try:
            price = int(self.price_for_one.text())
        except ValueError:
            # Если получили не число
            self.statusbar.showMessage("Цена должна быть числом")
            return

        # Если цена отрицательна
        if price < 0:
            self.statusbar.showMessage("Цена не может быть отрицательной")
            return

        # Устанавливаем цену
        if price:
            self.sender().setText(str(price))

    def accept(self) -> None:
        """Переопределение accept"""

        # Получаем название зала
        self.name = self.formLayout.itemAt(1).widget().text()

        # Получаем конфигурацию (из каждой кнопки boxlayout)
        self.configuration = []
        for i in range(int(self.height.value())):
            a = []
            for j in range(int(self.width.value())):
                a.append(self.boxLayout.itemAt(int(self.width.value()) * i + j).widget().text())
            self.configuration.append(a)

        # Проверка на корректность данных
        if self.name == '':
            self.statusbar.showMessage('Введите имя')
        elif ';' in self.name:
            self.statusbar.showMessage('В имени не должно быть символа ";"')
        elif self.name in get_halls(self.parent().curr_cinema):
            self.statusbar.showMessage('Такой зал уже существует')
        else:
            # Добавление зала
            add_hall(self.parent().curr_cinema, self.name, self.width.value(), self.height.value(), self.configuration)
            super().accept()


# TODO: продолжить комментировать
class ChangeHallDialog(QDialog):
    """Диалоговое окно для изменения зала"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(1000, 600)
        self.setWindowTitle("Изменить кинозал")

        # Получаем конфигурацию зала
        self.configuration = get_hall_configuration(parent.curr_cinema, parent.sender().text())

        # Сохраним предыдущее название, чтобы потом найти зал в БД
        self.last_name = parent.sender().text()
        # Переменная для нового названия
        self.name = ''

        # Виджет для выбора ширины и высоты зала
        a, b = get_hall_width_height(parent.curr_cinema, parent.sender().text())
        self.width = QtWidgets.QSpinBox(minimum=4, maximum=25, value=a)
        self.height = QtWidgets.QSpinBox(minimum=4, maximum=25, value=b)

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.buttonBox, 10, 18)

        # layout с формой для заполнения
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.addRow("Название:", QtWidgets.QLineEdit(self.last_name))

        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.formLayout.addRow(line)

        self.width.valueChanged.connect(self.update_ui)
        self.height.valueChanged.connect(self.update_ui)

        self.formLayout.addRow("Мест в ширину:", self.width)
        self.formLayout.addRow("Мест в высоту:", self.height)

        line2 = QtWidgets.QFrame(self)
        line2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.formLayout.addRow(line2)

        # Виджет для выбора цены для всех
        self.price_for_all = QtWidgets.QLineEdit('200')
        self.formLayout.addRow("Цена:", self.price_for_all)

        # Виджет для установки цены для всех
        self.but_price_for_all = QtWidgets.QPushButton("Для всех:")
        self.but_price_for_all.clicked.connect(self.set_price_for_all)
        self.formLayout.addRow(self.but_price_for_all)

        line3 = QtWidgets.QFrame(self)
        line3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.formLayout.addRow(line3)

        # Виджет для выбора цены для одного
        self.price_for_one = QtWidgets.QLineEdit()
        self.formLayout.addRow("Для одного:", self.price_for_one)

        self.layout.addLayout(self.formLayout, 0, 0, 1, 10)

        # Виджет с кнопками конфигурации зала
        self.boxLayout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.boxLayout, 0, 10, 9, 9)

        # Добавление кнопок из конфигурации зала
        for i in range(self.height.value()):
            for j in range(self.width.value()):
                a = QtWidgets.QPushButton(self.configuration[i][j])
                a.setMaximumSize(40, 20)
                a.clicked.connect(self.set_price_for_one)
                self.boxLayout.addWidget(a, i, j)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar, 11, 0, 1, 19)

    def update_ui(self) -> None:
        """Обновление ui"""

        # Получаем предыдущее значение ширины и высоты, чтобы обновить конфигурацию
        last_width = len(self.configuration[0])
        last_height = len(self.configuration)

        # Собираем конфигурацию с кнопок
        self.configuration = []
        for i in range(int(last_height)):
            a = []
            for j in range(int(last_width)):
                a.append(self.boxLayout.itemAt(int(last_width) * i + j).widget().text())
            self.configuration.append(a)

        # Получаем текущее значение ширины и высоты, чтобы обновить конфигурацию
        width = self.width.value()
        height = self.height.value()

        if last_height > height or last_width > width:
            # Если ширина или высота уменьшилась, то просто обрезаем конфигурацию
            self.configuration = [line[:width] for line in self.configuration]
            self.configuration = self.configuration[:height]
        else:
            # Если ширина или высота увеличилась, то дополняем конфигурацию местами
            self.configuration.extend([[self.price_for_all.text() for _ in range(width)]
                                       for i in range(height - last_height)])
            [self.configuration[i].extend(self.price_for_all.text() for _ in
                                          range(width - last_width)) for i in
             range(last_height)]

        # Полностью очищаем старый виджет с местами
        for i in reversed(range(self.boxLayout.count())):
            self.boxLayout.itemAt(i).widget().setParent(None)

        # Добавляем все кнопки на виджет с местами
        for i in range(self.height.value()):
            for j in range(self.width.value()):
                a = QtWidgets.QPushButton(self.configuration[i][j])
                a.setMaximumSize(40, 20)
                a.clicked.connect(self.set_price_for_one)
                self.boxLayout.addWidget(a, i, j)

    def set_price_for_all(self) -> None:
        """Установить цену для всех"""

        # Получаем цену
        try:
            price = int(self.price_for_all.text())
        except ValueError:
            # Если получили не число
            self.statusbar.showMessage("Цена должна быть числом")
            return

        # Если цена отрицательна
        if price < 0:
            self.statusbar.showMessage("Цена не может быть отрицательной")
            return

        # Обновляем места новой ценой
        for i in reversed(range(self.boxLayout.count())):
            self.boxLayout.itemAt(i).widget().setText(price)

    def set_price_for_one(self) -> None:
        """Установить цену для одного"""

        # Получаем цену
        try:
            price = int(self.price_for_one.text())
        except ValueError:
            # Если получили не число
            self.statusbar.showMessage("Цена должна быть числом")
            return

        # Если цена отрицательна
        if price < 0:
            self.statusbar.showMessage("Цена не может быть отрицательной")
            return

        # Устанавливаем цену
        if price:
            self.sender().setText(str(price))

    def accept(self) -> None:
        """Переопределение accept"""

        # Получаем новое имя
        self.name = self.formLayout.itemAt(1).widget().text()

        # Получаем ширину и высоту зала
        last_width = len(self.configuration[0])
        last_height = len(self.configuration)

        # Обновляем конфигурацию зала
        self.configuration = []
        for i in range(int(last_height)):
            a = []
            for j in range(int(last_width)):
                a.append(self.boxLayout.itemAt(int(last_width) * i + j).widget().text())
            self.configuration.append(a)

        # Проверка на корректность данных
        if self.name == '':
            self.statusbar.showMessage('Введите имя')
        elif ';' in self.name:
            self.statusbar.showMessage('В имени не должно быть символа ";"')
        else:
            # Изменение конфигурации зала
            edit_hall_configuration(self.parent().curr_cinema, self.name, self.last_name,
                                    len(self.configuration[0]), len(self.configuration), self.configuration)
            super().accept()


class AddCashiers(QDialog):
    """Диалог для изменения списка кассиров"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.cashiers = []
        self.setWindowTitle("Добавить кассиров")

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Получаем список доступных кассиров
        cashiers = get_cashiers()
        if not cashiers:
            # Если кассиров не нашли
            self.label = QtWidgets.QLabel("Создайте аккаунт для кассира")
        else:
            # Если кассиры найдены
            self.label = QtWidgets.QLabel("Выберите кассиров:")

        # Настройки стиля
        self.layout.setContentsMargins(20, 5, 20, 20)
        self.layout.setSpacing(1)
        self.label.setStyleSheet('font-size: 20px')

        self.layout.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Создаем лист с checkbox для кассиров
        selected_cashiers = get_cashiers_for_cinema(parent.curr_cinema)
        for cashier in cashiers:
            if cashier in selected_cashiers:
                # Если кассир уже был выбран, то ставим рядом с ним галочку
                checkbox = QtWidgets.QCheckBox(cashier)
                checkbox.setStyleSheet('font-size: 20px')
                checkbox.setChecked(True)
                self.layout.addWidget(checkbox, -2, QtCore.Qt.AlignmentFlag.AlignLeft)
            else:
                # Если кассир не был выбран
                checkbox = QtWidgets.QCheckBox(cashier)
                checkbox.setStyleSheet('font-size: 20px')
                self.layout.addWidget(checkbox, -2, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.layout.addStretch(1)
        self.layout.addWidget(self.buttonBox, -1, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.layout)

    def accept(self) -> None:
        """Переопределение accept"""

        # Получаем список кассиров
        self.cashiers = []
        for i in range(self.layout.count()):
            # Если виджет - checkbox
            if isinstance(self.layout.itemAt(i).widget(), QtWidgets.QCheckBox):
                # Проверим поставлена ли галочка
                if self.layout.itemAt(i).widget().isChecked():
                    # Добавим кассира в список
                    self.cashiers.append(self.layout.itemAt(i).widget().text())

        # Обновим список кассиров для кинотеатра
        set_cashiers_to_cinema(self.cashiers, self.parent().curr_cinema)
        super().accept()


class AddEventDialog(QDialog):
    """Диалоговое окно для входа"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Добавить событие")

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()

        # layout с формой для заполнения
        self.form_layout = QtWidgets.QFormLayout()

        self.form_layout.addRow("&Название:", QtWidgets.QLineEdit())

        self.form_layout.addRow("&Дата:", QtWidgets.QDateEdit())
        # Добавим возможность выбирать дату на календаре
        self.form_layout.itemAt(3).widget().setCalendarPopup(True)
        # Установим текущую дату
        self.form_layout.itemAt(3).widget().setDate(QtCore.QDate.currentDate())

        self.form_layout.addRow("&Время:", QtWidgets.QTimeEdit())
        # Установим время 12:00
        self.form_layout.itemAt(5).widget().setTime(QtCore.QTime(12, 0))

        # Виджет для выбора кинозала
        self.form_layout.addRow("&Кинозал:", QtWidgets.QComboBox())
        self.form_layout.itemAt(7).widget().addItems(get_halls(parent.curr_cinema))

        self.form_layout.addRow("&Описание:", QtWidgets.QPlainTextEdit())

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

        # Основные переменные
        self.name = ''
        self.date = ''
        self.time = ''
        self.description = ''
        self.hall = ''

    def accept(self) -> None:
        """Переопределение accept"""

        # Получение переменных
        self.name = self.form_layout.itemAt(1).widget().text()
        self.date = self.form_layout.itemAt(3).widget().date()
        self.time = self.form_layout.itemAt(5).widget().time()
        self.hall = self.form_layout.itemAt(7).widget().currentText()
        self.description = self.form_layout.itemAt(9).widget().toPlainText()

        # Получение id и названий всех событий для текущего кинотеатра
        parent_events_id = get_events_from_cinema(self.parent().curr_cinema)
        parent_events_names = [get_event_from_id(i)[1] for i in parent_events_id]

        # Проверка данных на корректность
        if not self.name:
            self.statusbar.showMessage("Название не может быть пустым")
        elif ';' in self.name:
            self.statusbar.showMessage("В названии не должно быть ';'")
        elif self.name in parent_events_names:
            self.statusbar.showMessage("Событие с таким названием уже существует")
        else:
            # Добавление ивента для кинотеатра
            id_ = add_event(self.name, self.date.toString("yyyy-MM-dd"), self.time.toString("hh:mm"),
                            self.parent().curr_cinema, self.hall, self.description)
            add_event_to_cinema(id_, self.parent().curr_cinema)

            super().accept()


class ChangeEventDialog(QDialog):
    """Диалоговое окно для входа"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Изменить событие")

        # Кнопки 'Ок', 'Отмена' и 'Завершить событие'
        self.buttonBox = QDialogButtonBox()
        end_but = QPushButton('Завершить событие')
        self.buttonBox.addButton(end_but, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        end_but.clicked.connect(self.end_event)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()

        # Получение данных о событии
        self.name = parent.sender().text()
        self.cinema = parent.curr_cinema
        self.id_, self.name, self.date, self.time, self.cinema, self.hall, self.description = (
            get_event_from_id(get_event_id_from_cinema_and_title(self.cinema, self.name)))

        # layout с формой для заполнения
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("&Название:", QtWidgets.QLineEdit())
        self.form_layout.itemAt(1).widget().setText(self.name)

        self.form_layout.addRow("&Дата:", QtWidgets.QDateEdit())
        # Добавление возможности выбрать дату через календарь
        self.form_layout.itemAt(3).widget().setCalendarPopup(True)
        # Установка даты события
        self.form_layout.itemAt(3).widget().setDate(QtCore.QDate.fromString(self.date, "yyyy-MM-dd"))

        self.form_layout.addRow("&Время:", QtWidgets.QTimeEdit())
        # Установка времени события
        self.form_layout.itemAt(5).widget().setTime(QtCore.QTime.fromString(self.time, "hh:mm"))

        self.form_layout.addRow("&Кинотеатр:", QtWidgets.QLabel())
        # Установка кинотеатра (label, так как менять нельзя)
        self.form_layout.itemAt(7).widget().setText(self.hall)

        self.form_layout.addRow("&Описание:", QtWidgets.QPlainTextEdit())
        # Установка описания
        self.form_layout.itemAt(9).widget().setPlainText(self.description)

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

    def accept(self) -> None:
        """Переопределение accept"""

        # Получение переменных
        self.name = self.form_layout.itemAt(1).widget().text()
        self.date = self.form_layout.itemAt(3).widget().date()
        self.time = self.form_layout.itemAt(5).widget().time()
        self.hall = self.form_layout.itemAt(7).widget().text()
        self.description = self.form_layout.itemAt(9).widget().toPlainText()

        # Проверка данных на корректность
        if not self.name:
            self.statusbar.showMessage("Название не может быть пустым")
        elif ';' in self.name:
            self.statusbar.showMessage("В названии не должно быть ';'")
        else:
            # Изменение данных события
            change_event(int(self.id_), self.name, self.date.toString("yyyy-MM-dd"), self.time.toString("hh:mm"),
                         self.cinema, self.hall, self.description)
            super().accept()

    def end_event(self):
        """Завершение события"""

        # Получение переменных
        width, height = get_event_config_width_height(int(self.id_))
        configuration = get_event_configuration(int(self.id_))

        # Получение списка занятых мест
        places = [(i, j) for i in range(width) for j in range(height) if configuration[i][j][0] == '!']
        # Подсчет прибыли с события
        profit = sum([int(configuration[i[0]][i[1]][1:]) for i in places])
        # Получение списка мест в формате: A1, B3...
        places = [string.ascii_uppercase[i[1]] + str(i[0] + 1) for i in places]

        # Получение текущей даты
        now_date_time = datetime.datetime.now()

        # Создание отчета
        report = (f"Событие {self.name} (id: {self.id_}) завершено {now_date_time}. Забронированы места: "
                  f"{', '.join(places)}. "
                  f"Прибыль: {profit}")
        # Добавление отчета в БД и создание .txt файла
        add_report(report)

        # Удаление ивента
        delete_event(int(self.id_))

        super().reject()
        # Обновление главной страницы
        self.parent().update_data()


class BookPlaces(QDialog):
    """Диалоговое окно для бронирования места"""

    def __init__(self, parent=None, id_=0) -> None:
        # Получение id ивента
        self.event_id = id_

        super().__init__(parent)
        self.resize(1000, 600)
        self.setWindowTitle("Забронировать места")

        # Получение конфигурации
        self.configuration = get_event_configuration(self.event_id)

        # Получение название события
        self.last_name = parent.sender().text()
        self.name = ''

        # Получение ширины и высоты зала
        self.width, self.height = get_event_config_width_height(self.event_id)

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.buttonBox, 10, 18)

        # Получение даты, времени и названия зала
        date = str(get_event_from_id(id_)[2])
        time = str(get_event_from_id(id_)[3])
        hall = str(get_event_from_id(id_)[5])

        # layout с формой для заполнения
        self.formLayout = QtWidgets.QVBoxLayout()
        self.formLayout.setSpacing(0)

        self.formLayout.addWidget(BigRow("Название:", get_event_from_id(self.event_id)[1]))

        line = QtWidgets.QFrame(self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)

        self.formLayout.addWidget(line)

        self.formLayout.addWidget(BigRow("Дата:", date))
        self.formLayout.addWidget(BigRow("Время:", time))
        self.formLayout.addWidget(BigRow("Зал:", hall))

        self.layout.addLayout(self.formLayout, 0, 0, 1, 10)

        # layout для мест
        self.boxLayout = QtWidgets.QGridLayout()
        self.layout.addLayout(self.boxLayout, 0, 10, 9, 9)

        # list со всеми кнопками
        self.buttons = []

        # Заполнения layout-а для мест
        for i in range(self.height):
            for j in range(self.width):
                if self.configuration[i][j][0] == '!':
                    # Если место уже забронировано, то ставим кнопке синий цвет
                    a = QtWidgets.QPushButton(self.configuration[i][j][1:])
                    a.setStyleSheet("background-color: blue")
                else:
                    a = QtWidgets.QPushButton(self.configuration[i][j])

                a.setMaximumSize(40, 20)
                a.clicked.connect(self.book_place)

                # Добавление кнопки в list
                self.buttons.append(a)
                self.boxLayout.addWidget(a, i, j)

        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar, 11, 0, 1, 19)

        # list для забронированных мест
        self.booked_places = []

    def update_ui(self) -> None:
        """Обновление ui"""

        # Очищаем список с кнопками, так как при обновлении они все изменятся
        self.buttons = []

        # Перерисовываем зал
        for i in range(self.height):
            for j in range(self.width):
                a = QtWidgets.QPushButton(self.configuration[i][j])
                a.setMaximumSize(40, 20)
                a.clicked.connect(self.book_place)

                if any(True for x in self.booked_places if x == (i, j)):
                    # Если место забронировано сейчас, то меняем кнопке цвет на красный
                    a.setStyleSheet("background-color: red")
                elif self.configuration[i][j][0] == '!':
                    # Если место было забронировано раньше, то меняем кнопке цвет на синий
                    a.setStyleSheet("background-color: blue")
                    a.setText(self.configuration[i][j][1:])

                # Добавление кнопки в list
                self.buttons.append(a)
                self.boxLayout.addWidget(a, i, j)

    def book_place(self) -> None:
        """Бронирование места"""

        # Получаем координаты места
        j, i = self.buttons.index(self.sender()) % self.width, self.buttons.index(self.sender()) // self.width

        if (i, j) not in self.booked_places and self.configuration[i][j][0] == '!':
            # Если место уже было забронировано, то сообщаем об этом
            QMessageBox.critical(self, 'Внимание', 'Вы уже забронировали это место')
            return
        if (i, j) not in self.booked_places:
            # Если место еще не забронировано, то бронируем его
            self.booked_places.append((i, j))
        else:
            # Если место уже забронировано, то снимаем бронь его
            self.booked_places.remove((i, j))

        # Получаем список забронированных мест
        self.booked_places = remove_duplicates(self.booked_places)
        # Обновляем ui
        self.update_ui()

    def accept(self) -> None:
        """Переопределение accept"""

        # Пересобираем конфигурацию
        for i in range(self.height):
            for j in range(int(self.width)):
                if any(True for x in self.booked_places if x == (i, j)):
                    # Если место в списки забронированных, то добавляем '!' в начало
                    self.configuration[i][j] = '!' + self.boxLayout.itemAt(int(self.width) * i + j).widget().text()

        # Если места добавлены не были, то просто выходим
        if not self.booked_places:
            super().reject()
            return

        # Диалог для подтверждения выбранных мест
        dlg = AcceptDialog(self)
        dlg.exec()
        if dlg.result() == QDialog.DialogCode.Accepted:
            # Сохраняем конфигурацию
            update_event_config(self.event_id, self.configuration)
            super().accept()
        else:
            self.reject()


class AcceptDialog(QtWidgets.QDialog):
    """Диалоговое окно для подтверждения"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.resize(300, 100)
        self.setWindowTitle("Подтверждение")

        # Кнопки Ок и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Ок'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(QtWidgets.QLabel('Вы хотите забронировать следующие места:'))

        # Выводим список мест в формате A1, B3...
        for i in parent.booked_places:
            self.layout.addWidget(QtWidgets.QLabel(f'({string.ascii_uppercase[i[1]]}, {i[0] + 1})'))
        self.layout.addWidget(self.buttonBox)

    def accept(self) -> None:
        super().accept()

    def reject(self) -> None:
        super().reject()


class AddDatabaseDialog(QDialog):
    """Диалог для добавления базы данных в /database"""

    def __init__(self, parent=None):
        super(AddDatabaseDialog, self).__init__(parent)
        self.setWindowTitle('Добавление базы данных')
        self.resize(300, 100)

        # Основной layout
        self.layout = QtWidgets.QVBoxLayout()

        # Кнопки Добавить и Отмена
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Добавить'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.addButton(QPushButton('Отмена'), QDialogButtonBox.ButtonRole.RejectRole)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # layout с формой для заполнения
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.addRow("&Название:", QtWidgets.QLineEdit())

        self.layout.addLayout(self.form_layout)

        self.layout.addWidget(self.buttonBox, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Информационный statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.showMessage("Заполните форму")
        self.layout.addWidget(self.statusbar)

        # Переменная для названия базы данных
        self.name = ''

    def accept(self):

        # Получения названия базы данных
        self.name = self.form_layout.itemAt(1).widget().text()
        if not self.name:
            self.statusbar.showMessage("Введите название базы данных")
        elif '.' in self.name:
            self.statusbar.showMessage("Название не должно содержать точку")
        elif self.name in get_databases():
            self.statusbar.showMessage("База данных с такими названием уже существует")
        else:
            # Создание базы данных
            create_database('database/' + self.name + '.db')
            super().accept()
