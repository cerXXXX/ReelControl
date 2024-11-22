# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget

from dialogues import *
from database import (get_cinemas, delete_cinema, get_halls, delete_hall, main_color, selected_color, set_vars,
                      delete_cashier_from_cinema, get_event_from_id, delete_event)


class BigButton(QWidget):
    """Виджет из двух кнопок"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # self.setWindowTitle('BigButton')
        self.main = QtWidgets.QPushButton()
        self.delete = QtWidgets.QPushButton()
        self.delete.setText('🗑️')
        self.delete.setMaximumSize(23, 10000)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.main)
        layout.addWidget(self.delete)

    def setText(self, text) -> None:
        """Устанавливает текст кнопки"""
        self.main.setText(str(text))

    def text(self) -> str:
        """Возвращает текст кнопки"""
        return self.main.text()


class AdminPage(QWidget):
    """Страница администратора"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("self")
        self.resize(759, 445)

        # Общий layout
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        # layout для кинотеатров
        self.cinemas_layout = QtWidgets.QVBoxLayout()
        self.cinemas_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.cinemas_layout.setSpacing(0)
        self.cinemas_layout.setObjectName("cinemas_layout")

        # кнопка для добавления кинотеатра
        self.add_cinema = QtWidgets.QPushButton(self)
        self.add_cinema.setObjectName("add_cinema")
        self.cinemas_layout.addWidget(self.add_cinema, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.horizontalLayout_5.addLayout(self.cinemas_layout)

        # линия-разделитель
        self.line = QtWidgets.QFrame(self)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_5.addWidget(self.line)

        # layout для залов
        self.halls_layout = QtWidgets.QVBoxLayout()
        self.halls_layout.setObjectName("halls_layout")

        # кнопка добавления зала
        self.add_hall = QtWidgets.QPushButton(self)
        self.add_hall.setObjectName("add_hall")
        self.halls_layout.addWidget(self.add_hall)
        self.horizontalLayout_5.addLayout(self.halls_layout)

        # линия-разделитель
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_5.addWidget(self.line_2)

        # layout для кассиров
        self.cashiers_layout = QtWidgets.QVBoxLayout()
        self.cashiers_layout.setObjectName("cashiers_layout")

        # кнопка добавления кассира
        self.add_cashier = QtWidgets.QPushButton(self)
        self.add_cashier.setObjectName("add_cashier")
        self.cashiers_layout.addWidget(self.add_cashier)
        self.horizontalLayout_5.addLayout(self.cashiers_layout)

        # линия-разделитель
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_5.addWidget(self.line_3)

        # layout для событий
        self.events_layout = QtWidgets.QVBoxLayout()
        self.events_layout.setObjectName("events_layout")

        # кнопка добавления события
        self.add_event = QtWidgets.QPushButton(self)
        self.add_event.setObjectName("add_event")
        self.events_layout.addWidget(self.add_event)
        self.horizontalLayout_5.addLayout(self.events_layout)

        # установка названий
        self.setWindowTitle("Админ")
        self.add_cinema.setText("Добавить кинотеатр")
        self.add_hall.setText("Добавить кинозал")
        self.add_event.setText("Добавить событие")
        self.add_cashier.setText("Добавить кассира")

        # добавление в каждый layout spacer item-а, чтобы все элементы были сверху
        self.cinemas_layout.addStretch(1)
        self.halls_layout.addStretch(1)
        self.events_layout.addStretch(1)
        self.cashiers_layout.addStretch(1)

        # подключение кнопок
        self.add_cinema.clicked.connect(self.clicked)
        self.add_hall.clicked.connect(self.clicked)
        self.add_event.clicked.connect(self.clicked)
        self.add_cashier.clicked.connect(self.clicked)

        # переменная для хранения текущего кинотеатра
        self.curr_cinema = ''

        self.update_data()

    def clicked(self) -> None:
        """Обработка нажатия кнопки добавить"""

        # обновляем ui
        self.update_data()

        # получаем текст кнопки
        sender_text = self.sender().text()

        # вызываем нужный диалог
        if sender_text == 'Добавить кинотеатр':
            dlg = AddCinemaDialog(self)
            if not dlg.exec():
                return
        elif sender_text == 'Добавить кинозал':
            if not get_cinemas():
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Нет кинотеатров')
            else:
                dlg = AddHallDialog(self)
                if not dlg.exec():
                    return
        elif sender_text == 'Добавить событие':
            if not get_halls(self.curr_cinema):
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Нет кинозалов')
            else:
                dlg = AddEventDialog(self)
                if not dlg.exec():
                    return
        elif sender_text == 'Добавить кассира':
            if not get_cinemas():
                QtWidgets.QMessageBox.warning(self, 'Ошибка', 'Нет кинотеатров')
            else:
                dlg = AddCashiers(self)
                if not dlg.exec():
                    return

        # обновление ui
        self.update_data()

    def delete_clicked(self, widget=None, layout=None) -> None:
        """Удаление элемента из layout"""

        dlg = DeleteDialog(self)
        if dlg.exec():
            if layout.objectName() == 'cinemas_layout':
                try:
                    # если нажали удалить кинотеатр
                    delete_cinema(self.sender().parent().text())
                    try:
                        # устанавливаем кинотеатр
                        if self.curr_cinema not in get_cinemas():
                            self.curr_cinema = get_cinemas()[0]
                    except (AttributeError, IndexError):
                        # если удалили последний кинотеатр
                        self.curr_cinema = ''
                except Exception as e:
                    print(e)
            elif layout.objectName() == 'halls_layout':
                # если нажали удалить кинозал
                delete_hall(self.curr_cinema, self.sender().parent().text())
            elif layout.objectName() == 'cashiers_layout':
                # если нажали удалить кассира
                delete_cashier_from_cinema(self.sender().parent().text(), self.curr_cinema)
            elif layout.objectName() == 'events_layout':
                # если нажали удалить событие
                delete_event(get_event_id_from_cinema_and_title(self.curr_cinema, self.sender().parent().text()))

            try:
                layout.removeWidget(widget)
                widget.deleteLater()
            except Exception:
                self.update_data()

            # обновляем ui
            self.update_data()

    def update_data(self) -> None:
        """Обновление главного окна"""

        # обновляем переменные
        set_vars()

        # получаем все кинотеатры
        cinemas = get_cinemas()

        # очищаем cinemas_layout
        for i in reversed(range(self.cinemas_layout.count())):
            try:
                self.cinemas_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                # если наткнулись на spacer
                pass

        # добавляем кнопку добавить кинотеатр
        self.cinemas_layout.insertWidget(0, self.add_cinema, QtCore.Qt.AlignmentFlag.AlignTop)

        # добавляем все кинотеатры
        for cinema in cinemas:
            but = BigButton(self)
            but.setText(cinema)
            # but.delete.clicked.connect(lambda: self.delete_clicked(but, curr_layout))
            but.delete.clicked.connect(lambda: self.delete_clicked(but, self.cinemas_layout))
            but.main.clicked.connect(self.set_curr_cinema)
            self.cinemas_layout.insertWidget(self.cinemas_layout.count() - 1, but, 0,
                                             QtCore.Qt.AlignmentFlag.AlignTop)

        # получаем список кинотеатров
        last_cinemas = [self.cinemas_layout.itemAt(i).widget() for i in
                        range(1, self.cinemas_layout.count() - 1)]

        # устанавливаем цвет кинотеатру
        for cinema in last_cinemas:
            if cinema.text() != self.curr_cinema:
                # если кинотеатр не выбран
                cinema.main.setStyleSheet('QPushButton {background-color: ' + main_color + '}')
            else:
                # если выбран данный кинотеатр
                cinema.main.setStyleSheet('QPushButton {background-color: ' + selected_color + '}')

        # если текущий кинотеатр не установлен
        if not self.curr_cinema:
            try:
                # если кинотеатр не установлен, то он максимум один, и первый виджет обязательно его, значит его можно
                # закрасить
                self.curr_cinema = self.cinemas_layout.itemAt(1).widget().text()
                self.cinemas_layout.itemAt(1).widget().main.setStyleSheet('QPushButton {background-color: '
                                                                          + selected_color + '}')
            except AttributeError:
                # если кинотеатров нет, то очищаем переменную
                self.curr_cinema = ''

        # получаем список кинозалов
        halls = get_halls(self.curr_cinema)

        # очищаем halls_layout
        for i in reversed(range(self.halls_layout.count())):
            try:
                self.halls_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                # наткнулись на spacer
                pass

        # добавляем кнопку добавления зала
        self.halls_layout.insertWidget(0, self.add_hall, QtCore.Qt.AlignmentFlag.AlignTop)

        # добавляем все кинозалы
        for hall in halls:
            but = BigButton(self)
            but.setText(hall)
            but.delete.clicked.connect(lambda: self.delete_clicked(but, self.halls_layout))
            but.main.clicked.connect(self.change_hall_configuration)
            self.halls_layout.insertWidget(self.halls_layout.count() - 1, but, 0,
                                           QtCore.Qt.AlignmentFlag.AlignTop)

        # получаем всех кассиров
        cashiers = get_cashiers_for_cinema(self.curr_cinema)

        # очищаем cashiers_layout
        for i in reversed(range(self.cashiers_layout.count())):
            try:
                self.cashiers_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                # наткнулись на spacer
                pass

        # добавляем кнопку добавления кассиров
        self.cashiers_layout.insertWidget(0, self.add_cashier, QtCore.Qt.AlignmentFlag.AlignTop)

        # добавляем кассиров
        for cashier in cashiers:
            but = BigButton(self)
            but.setText(cashier)
            but.delete.clicked.connect(lambda: self.delete_clicked(but, self.cashiers_layout))
            self.cashiers_layout.insertWidget(self.cashiers_layout.count() - 1, but, 0,
                                              QtCore.Qt.AlignmentFlag.AlignTop)

        # получаем все события
        events = get_events_from_cinema(self.curr_cinema)

        # очищаем events_layout
        for i in reversed(range(self.events_layout.count())):
            try:
                self.events_layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                # если наткнулись на spacer
                pass

        # добавляем кнопку добавления события
        self.events_layout.insertWidget(0, self.add_event, QtCore.Qt.AlignmentFlag.AlignTop)

        # если событий нет, выходим из функции
        if not events:
            return

        # добавляем события
        for event_ in events:
            data = get_event_from_id(event_)
            but = BigButton(self)
            but.setText(data[1])
            but.delete.clicked.connect(lambda: self.delete_clicked(but, self.events_layout))
            but.main.clicked.connect(self.change_event_configuration)
            self.events_layout.insertWidget(self.events_layout.count() - 1, but, 0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)

    def change_hall_configuration(self):
        """Открывает диалог для изменения настроек кинозала"""
        dlg = ChangeHallDialog(self)
        if dlg.exec():
            self.update_data()

    def set_curr_cinema(self) -> None:
        """Устанавливает curr_cinema"""
        self.curr_cinema = self.sender().text()
        self.sender().setStyleSheet('QPushButton {background-color: ' + selected_color + '}')
        self.update_data()

    def change_event_configuration(self):
        """Открывает диалог для изменения настроек события"""
        dlg = ChangeEventDialog(self)
        if dlg.exec():
            self.update_data()


class BigRow(QWidget):
    """Виджет из двух label"""

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
        layout.addWidget(self.right)


class CashierPage(QWidget):
    """Страница кассира"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.resize(759, 445)

        # основной layout
        self.layout = QtWidgets.QGridLayout(self)

        # layout для кинотеатров
        self.cinemas_layout = QtWidgets.QVBoxLayout()

        # заголовок layout-а
        self.cinema_label = QtWidgets.QLabel("Кинотеатры")
        self.cinemas_layout.addWidget(self.cinema_label)

        # layout для событий
        self.events_layout = QtWidgets.QVBoxLayout()

        # заголовок layout-а
        self.event_label = QtWidgets.QLabel("События")
        self.events_layout.addWidget(self.event_label)

        # layout для информации о событии
        self.event_data_layout = QtWidgets.QVBoxLayout()

        # заголовок layout-а
        self.event_data_label = QtWidgets.QLabel("Информация")
        self.event_data_layout.addWidget(self.event_data_label)

        # линия-разделитель
        self.line_1 = QtWidgets.QFrame(self)
        self.line_1.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_1.setObjectName("line_1")

        # линия разделитель
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        self.layout.addLayout(self.cinemas_layout, 0, 0, 1, 1)
        self.layout.addWidget(self.line_1, 0, 1, 1, 1)
        self.layout.addLayout(self.events_layout, 0, 2, 1, 1)
        self.layout.addWidget(self.line_2, 0, 3, 1, 1)
        self.layout.addLayout(self.event_data_layout, 0, 4, 1, 2)
        self.setLayout(self.layout)

        # добавление в каждый layout spacer item-а, чтобы все элементы были сверху
        self.cinemas_layout.addStretch(1)
        self.events_layout.addStretch(1)
        self.event_data_layout.addStretch(1)

        # установка переменных
        self.curr_cinema = None
        self.curr_event = None

        self.update_data()

    def update_data(self) -> None:
        """Обновляет данные"""

        # получаем все кинотеатры
        cinemas = get_cinemas_for_cashier(self.parent.cashier_name)

        # если кинотеатров нет, то очищаем все layout-ы
        if not cinemas:
            # очищаем кинотеатры
            for i in reversed(range(self.cinemas_layout.count() - 1)):
                self.cinemas_layout.itemAt(i).widget().setParent(None)
            self.cinemas_layout.insertWidget(0, self.cinema_label)

            # очищаем события
            for i in reversed(range(self.events_layout.count() - 1)):
                self.events_layout.itemAt(i).widget().setParent(None)
            self.events_layout.insertWidget(0, self.event_label)

            # очищаем информацию о событии
            for i in reversed(range(self.event_data_layout.count() - 1)):
                self.event_data_layout.itemAt(i).widget().setParent(None)
            self.event_data_layout.insertWidget(0, self.event_data_label)

            # выходим из функции
            return

        # очищаем все кинотеатры
        for i in reversed(range(self.cinemas_layout.count() - 1)):
            self.cinemas_layout.itemAt(i).widget().setParent(None)

        # добавляем заголовок layout-а
        self.cinemas_layout.insertWidget(0, self.cinema_label)

        # добавляем кинотеатры
        for cinema in cinemas:
            but = QtWidgets.QPushButton(self)
            but.setText(cinema)
            but.clicked.connect(self.set_curr_cinema)
            self.cinemas_layout.insertWidget(self.cinemas_layout.count() - 1, but, 0,
                                             QtCore.Qt.AlignmentFlag.AlignTop)

        try:
            # если текущий кинотеатр не установлен, то устанавливаем первый
            if self.curr_cinema is None:
                self.curr_cinema = cinemas[0]
        except IndexError:
            # если кинотеатров нет, то ничего не делаем
            pass

        # получаем список кинотеатров
        last_cinemas = [self.cinemas_layout.itemAt(i).widget() for i in
                        range(1, self.cinemas_layout.count() - 1)]

        # устанавливаем цвета для кнопок
        for cinema in last_cinemas:
            if cinema.text() != self.curr_cinema:
                cinema.setStyleSheet('QPushButton {background-color: ' + main_color + '}')
            else:
                cinema.setStyleSheet('QPushButton {background-color: ' + selected_color + '}')

        # получаем список событий
        events = [get_event_from_id(i)[1] for i in get_events_from_cinema(self.curr_cinema)]

        # очищаем все события
        for i in reversed(range(self.events_layout.count() - 1)):
            self.events_layout.itemAt(i).widget().setParent(None)

        # добавляем заголовок layout-а
        self.events_layout.insertWidget(0, self.event_label)

        # добавляем события
        for event in events:
            but = QtWidgets.QPushButton(self)
            but.setText(event)
            but.clicked.connect(self.set_curr_event)
            self.events_layout.insertWidget(self.events_layout.count() - 1, but, 0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)

        try:
            # если текущее событие не установлен, то устанавливаем первый
            if self.curr_event is None:
                self.curr_event = events[0]
        except IndexError:
            # если событий нет, то ничего не делаем
            pass

        # получаем список событий
        last_events = [self.events_layout.itemAt(i).widget() for i in
                       range(1, self.events_layout.count() - 1)]

        # устанавливаем цвета для кнопок
        for event in last_events:
            if event.text() != self.curr_event:
                event.setStyleSheet('QPushButton {background-color: ' + main_color + '}')
            else:
                event.setStyleSheet('QPushButton {background-color: ' + selected_color + '}')

        # очищаем информацию о событии
        for i in reversed(range(self.event_data_layout.count() - 1)):
            self.event_data_layout.itemAt(i).widget().setParent(None)

        # добавляем заголовок layout-а
        self.event_data_layout.insertWidget(0, self.event_data_label)

        # если текущее событие не установлено, то выходим из функции
        if self.curr_event is None:
            return

        # добавляем заголовок layout-а
        self.event_data_layout.insertWidget(self.event_data_layout.count() - 1, BigRow('Название:',
                                                                                       self.curr_event),
                                            0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)

        # получаем переменные
        id_ = get_event_id_from_cinema_and_title(self.curr_cinema, self.curr_event)
        date = str(get_event_from_id(id_)[2])
        time = str(get_event_from_id(id_)[3])
        hall = str(get_event_from_id(id_)[5])

        # добавляем информацию о событии
        self.event_data_layout.insertWidget(self.event_data_layout.count() - 1, BigRow('Дата:', date),
                                            0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)
        self.event_data_layout.insertWidget(self.event_data_layout.count() - 1, BigRow('Время:', time),
                                            0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)
        self.event_data_layout.insertWidget(self.event_data_layout.count() - 1, BigRow('Зал:', hall),
                                            0,
                                            QtCore.Qt.AlignmentFlag.AlignTop)

        # добавляем кнопку бронирование мест
        but = QtWidgets.QPushButton()
        but.setText('Забронировать места')
        but.clicked.connect(lambda: self.book_event(id_))
        self.event_data_layout.insertWidget(self.event_data_layout.count() - 1, but)

    def book_event(self, id_) -> None:
        """Открывает диалог бронирования мест"""

        dlg = BookPlaces(self, id_)
        if dlg.exec():
            self.update_data()

    def set_curr_cinema(self) -> None:
        """Устанавливает текущий кинотеатр"""

        self.curr_cinema = self.sender().text()

        # сбрасываем текущее событие
        self.curr_event = None

        self.sender().setStyleSheet('QPushButton {background-color: ' + selected_color + '}')
        self.update_data()

    def set_curr_event(self) -> None:
        """Устанавливает текущее событие"""

        self.curr_event = self.sender().text()
        self.sender().setStyleSheet('QPushButton {background-color: ' + selected_color + '}')
        self.update_data()
