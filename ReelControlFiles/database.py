# -*- coding: utf-8 -*-
import sqlite3
import os


main_color = '#e1e1e1'
selected_color = '#A3C1DA'
database_name = 'database/database.db'


def create_database(*args) -> None:
    """Создание базы данных"""
    if not args:
        name = 'database/database.db'
    else:
        name = args[0]
    conn = sqlite3.connect(name)
    cursor = conn.cursor()
    cursor.executescript('''PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: data
CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, cinema TEXT NOT NULL UNIQUE, address 
TEXT NOT NULL, users TEXT, events TEXT);

-- Таблица: events
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, title TEXT NOT NULL, date TEXT, 
time TEXT, cinema TEXT NOT NULL, hall TEXT NOT NULL, description TEXT);

-- Таблица: events_config
CREATE TABLE IF NOT EXISTS events_config (id INTEGER PRIMARY KEY AUTOINCREMENT, event_id, width, height, places);

-- Таблица: halls
CREATE TABLE IF NOT EXISTS halls (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, cinema TEXT REFERENCES data 
(cinema) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, hall TEXT NOT NULL, width INTEGER NOT NULL, height 
INTEGER NOT NULL, places BLOB);

-- Таблица: reports
CREATE TABLE IF NOT EXISTS reports (id INTEGER PRIMARY KEY AUTOINCREMENT, report TEXT);

-- Таблица: users
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, role TEXT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;''')
    conn.commit()
    conn.close()

    # Установка имени базы данных по умолчанию
    set_database_name('database/database.db')


def get_databases() -> list:
    """Получить список баз данных"""
    # Получить список файлов базы данных
    try:
        files = os.listdir('database')
    except FileNotFoundError:
        # Если нет папки с БД
        os.mkdir('database')
        files = os.listdir('database')

    res = []
    for file in files:
        if file.endswith('.db'):
            res.append(file.split('.db')[0])

    # Если не нашли базу данных, создадим ее
    if not res:
        create_database()
        res = get_databases()
    return res


def set_database_name(name: str) -> None:
    """Установить имя базы данных"""
    # Устанавливаем имя базы данных
    global database_name
    database_name = name

    # Меняем БД в cfg.txt
    with open('cfg.txt', 'r') as f:
        lines = f.readlines()
    lines = [i for i in lines if not i.startswith('DATABASE_NAME')]
    lines.append(f'DATABASE_NAME={database_name}')
    with open('cfg.txt', 'w') as f:
        f.writelines(lines)


def get_var(var: str) -> str:
    """Получить значение переменной var из файла cfg.txt"""
    with open('cfg.txt', 'r') as f:
        lines = f.readlines()
        if not lines:
            pass
        for line in lines:
            if line.split('=')[0].strip() == var:
                return line.split('=')[1].strip()
        raise Exception(f'{var} not found')


def set_vars() -> None:
    """Установить значения глобальных переменных"""
    global main_color
    global selected_color
    global database_name
    try:
        # Устанавливаем значения глобальных переменных
        main_color = get_var('MAIN_COLOR')
        selected_color = get_var('SELECTED_COLOR')
        database_name = get_var('DATABASE_NAME')
    except FileNotFoundError:
        # Если не нашли файл cfg.txt
        with open('cfg.txt', 'w') as f:
            f.write('MAIN_COLOR=#e1e1e1\nSELECTED_COLOR=#A3C1DA\nDATABASE_NAME=database/database.db')

        # Получаем заново
        main_color = get_var('MAIN_COLOR')
        selected_color = get_var('SELECTED_COLOR')
        database_name = get_var('DATABASE_NAME')


set_vars()  # Установка значений глобальных переменных


def remove_duplicates(nested_list) -> list:
    """Удалить повторяющиеся элементы в списке"""
    unique_list = []
    for element in nested_list:
        if element not in unique_list:
            unique_list.append(element)
    return unique_list


def check_login_name(name: str) -> bool:
    """"Проверка логина на существование в базе данных"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        users = list(cur.execute('SELECT * FROM users where name = ?', (name,)))
        # Если нашли пользователя
        if len(users) != 0:
            return True
    return False


def write_user(name: str, role: str, password: str) -> None:
    """Добавление пользователя"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Перевод роли на английский
        if role == 'Админ':
            role = 'Admin'
        elif role == 'Кассир':
            role = 'Cashier'

        cur.execute('INSERT INTO users (name, role, password) VALUES (?, ?, ?)',
                    (name, role, password))
        con.commit()


def check_user(name: str, password: str) -> str:
    """Проверка пользователя по имени и паролю"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        users = list(cur.execute('SELECT * FROM users where name = ? and password = ?',
                                 (name, password)))
        # Если нашли пользователя
        if len(users) != 0:
            return users[0][-1]
    return ''


def add_cinema(cinema: str, address: str) -> None:
    """Добавление кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute('INSERT INTO data (cinema, address) VALUES (?, ?)', (cinema, address))
        con.commit()


def get_cinemas() -> list[str]:
    """Возвращает список названий всех кинотеатров в БД"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cinemas = list(cur.execute('SELECT cinema FROM data ORDER BY id ASC').fetchall())

        # Выбираем только названия
        cinemas = [cinema[0] for cinema in cinemas]
        return cinemas


def delete_cinema(cinema: str) -> None:
    """Удаление кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        # Удаляем кинотеатр из основной таблицы
        cur.execute('DELETE FROM data WHERE cinema = ?', (cinema,))
        # Удаляем все залы, принадлежащие кинотеатру
        cur.execute('DELETE FROM halls WHERE cinema = ?', (cinema,))
        con.commit()
        delete_halls(cinema)

    # Удаляем все события, принадлежащие кинотеатру
    delete_events_from_cinema(cinema)


def add_hall(cinema: str, hall: str, width: int, height: int, places: list[list[str]]) -> None:
    """Добавление зала"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Преобразуем list[list[str]] в list[str]
        line_places = []
        for place in places:
            line_places.append(';'.join(place))

        cur.execute('INSERT INTO halls (cinema, hall, width, height, places) VALUES (?, ?, ?, ?, ?)',
                    (cinema, hall, width, height, ';'.join(line_places)))
        con.commit()


def get_halls(cinema: str) -> list[str]:
    """Возвращает список названий кинозалов в кинотеатре"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        halls = list(cur.execute('SELECT hall FROM halls WHERE cinema = ?', (cinema,)).fetchall())

        # Возвращаем только названия
        halls = [hall[0] for hall in halls]
        return halls


def delete_hall(cinema: str, hall: str) -> None:
    """Удаление кинозала"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute('DELETE FROM halls WHERE cinema = ? AND hall = ?', (cinema, hall))
        con.commit()


def delete_halls(cinema: str) -> None:
    """Удаление всех кинозалов"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute('DELETE FROM halls WHERE cinema = ?', (cinema,))
        con.commit()


def get_hall_configuration(cinema: str, hall: str) -> list[list[str]]:
    """Возвращает конфигурацию кинозала"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        places = list(cur.execute('SELECT places FROM halls WHERE cinema = ? AND hall = ?',
                                  (cinema, hall)))

        # Преобразуем str в list[str]
        places = places[0][0].split(';')
        width, height = get_hall_width_height(cinema, hall)

        # Преобразуем list[str] в list[list[str]]
        places = [places[i:i + width] for i in range(0, len(places), width)]
        return places


def get_hall_width_height(cinema: str, hall: str) -> tuple[int, int]:
    """Возвращает ширину и высоту зала"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        width_height = list(cur.execute('SELECT width, height FROM halls WHERE cinema = ? AND hall = ?',
                                        (cinema, hall)))

        # Т.к получили list[list[str]], преобразуем str в list[str]
        width_height = width_height[0]
        return width_height[0], width_height[1]


def edit_hall_configuration(cinema: str, hall: str, last_name: str, width: int,
                            height: int, places: list[list[str]]) -> None:
    """Изменение конфигурации кинозала"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Преобразуем list[list[str]] в list[str]
        line_places = []
        for place in places:
            line_places.append(';'.join(place))

        cur.execute('UPDATE halls SET places = ?, hall = ?, width = ?, height = ? WHERE cinema = ? AND hall = ?',
                    (';'.join(line_places), hall, width, height, cinema, last_name))
        con.commit()


def get_cashiers_for_cinema(cinema: str) -> list[str]:
    """Возвращает список кассиров для кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cursor = con.cursor()
        cashiers = cursor.execute(f'SELECT users FROM data WHERE cinema = "{cinema}"').fetchall()
        cursor.close()

        # Если не нашли ни одного кассира (получили None), возвращаем пустой список
        if not cashiers:
            return []

        if cashiers[0][0]:
            # Если кассиры есть, преобразуем str в list[str]
            res = [i for i in list(cashiers)[0][0].split(';') if i != '']
        else:
            # Если кассиров нет (получили list[list[None]]), возвращаем пустой список
            res = []
        return res


def get_cashiers() -> list[str]:
    """Возвращает список всех кассиров для всех кинотеатров в БД"""
    with sqlite3.connect(database_name) as con:
        cursor = con.cursor()
        cashiers = cursor.execute(f'SELECT name FROM users WHERE role = "Cashier"').fetchall()
        cursor.close()

        # Возвращаем только имена
        res = [i[0] for i in list(cashiers)]
        return res


def set_cashiers_to_cinema(name: list[str], cinema: str) -> None:
    """Установка списка кассиров для кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cursor = con.cursor()
        cursor.execute(f'UPDATE data SET users = "{";".join(name)}" WHERE cinema = "{cinema}"')
        con.commit()
        cursor.close()


def delete_cashier_from_cinema(cashier: str, cinema: str) -> None:
    """Удаление кассира из кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cursor = con.cursor()

        # Получаем список кассиров для кинотеатра
        cashiers = get_cashiers_for_cinema(cinema)
        # Удаляем кассира из списка
        cashiers.remove(cashier)
        # Устанавливаем список кассиров для кинотеатра
        set_cashiers_to_cinema(cashiers, cinema)

        cursor.close()


def add_event(name: str, date: str, time: str, cinema: str, hall: str, description: str) -> int:
    """Добавление события для кинотеатра в БД, возвращает id события"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO events (title, date, time, cinema, hall, description) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, date, time, cinema, hall, description))
        con.commit()

        # Получаем id события и конфигурацию его мест
        id_ = get_event_id_from_cinema_and_title(cinema, name)
        configuration = get_hall_configuration(cinema, hall)
        # Добавляем конфигурацию мест для события
        add_event_configuration(id_, configuration)
        return cur.execute("SELECT last_insert_rowid()").fetchone()[0]


def get_event_from_id(id_: int) -> list[str]:
    """Возвращает список с данными события по его id"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM events WHERE id = ?", (id_,))
        return cur.fetchone()


def get_events_from_cinema(cinema: str) -> list[int]:
    """Возвращает список id событий для кинотеатра"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        data = cur.execute("SELECT events FROM data WHERE cinema = ?", (cinema,)).fetchall()

        # Если события не найдены (получили None)
        if not data:
            return []

        data = data[0][0]
        if data:
            # Если события найдены
            return [int(i) for i in data.split(';')]
        else:
            # Если событий нет (получили пустой список)
            return []


def get_event_id_from_cinema_and_title(cinema: str, title: str) -> int:
    """Возвращает id события по его названию и кинотеатру"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("SELECT id FROM events WHERE title = ? AND cinema = ?", (title, cinema))
        res = cur.fetchone()
        return res[0]


def add_event_to_cinema(id_: int, cinema: str) -> None:
    """Добавление события для кинотеатра в БД"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Получаем список событий для кинотеатра
        events = [str(i) for i in get_events_from_cinema(cinema)]
        cur.execute("""UPDATE data SET events = ? WHERE cinema = ?""", (';'.join(events + [str(id_)]), cinema))
        con.commit()


def change_event(id_: int, name: str, date: str, time: str, cinema: str, hall: str, description: str):
    """Изменение данных события по его id"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("UPDATE events SET title = ?, date = ?, time = ?, cinema = ?, hall = ?, "
                    "description = ? WHERE id = ?",
                    (name, date, time, cinema, hall, description, id_))
        con.commit()

        id_ = get_event_id_from_cinema_and_title(cinema, name)
        configuration = get_hall_configuration(cinema, hall)
        update_event_config(id_, configuration)


def delete_event(id_: int):
    """Удаление события по его id"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Получаем кинотеатр и список событий
        cinema = get_event_from_id(id_)[4]
        prev_events = get_events_from_cinema(cinema)

        # Удаляем событие из списка
        prev_events.remove(id_)

        # Преобразуем list[int] в list[str]
        prev_events = [str(i) for i in prev_events]

        # Удаляем событие из кинотеатра
        cur.execute("UPDATE data SET events = ? WHERE cinema = ?", (';'.join(prev_events), cinema))
        con.commit()

        # Удаляем событие из таблицы с событиями
        cur.execute("DELETE FROM events WHERE id = ?", (id_,))
        con.commit()

        # Удаляем конфигурацию события
        cur.execute("DELETE FROM events_config WHERE event_id = ?", (id_,))
        con.commit()


def delete_events_from_cinema(cinema: str) -> None:
    """Удаление всех событий для кинотеатра"""

    with sqlite3.connect(database_name) as con:
        cur = con.cursor()

        # Удаляем все события из кинотеатра
        cur.execute(f"UPDATE data SET events = '' WHERE cinema = '{cinema}'")
        con.commit()
        # Удаляем конфигурации событий
        cur.execute(f"DELETE FROM events_config WHERE event_id IN (SELECT id FROM events WHERE cinema = '{cinema}')")
        con.commit()
        # Удаляем события из таблицы с событиями
        cur.execute(f"DELETE FROM events WHERE cinema = '{cinema}'")
        con.commit()


def add_event_configuration(id_: int, places: list[list[str]]) -> None:
    """Добавить конфигурацию ивента"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO events_config (event_id, places, width, height) VALUES ({id_}, ?, ?, ?)",
                    (';'.join(';'.join(x) for x in places), len(places[0]), len(places)))
        con.commit()


def get_event_configuration(id_: int) -> list[list[str]]:
    """Получить конфигурацию ивента"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(f"SELECT places FROM events_config WHERE event_id = {id_}")
        res = cur.fetchall()

        # Если конфигурации нет (получили None)
        if not res:
            return []

        # Преобразовываем str в list[str]
        places = res[0][0].split(';')
        width, height = get_event_config_width_height(id_)

        # Преобразовываем list[str] в list[list[str]]
        res = [places[i:i + width] for i in range(0, len(places), width)]
        return res


def get_event_config_width_height(id_: int) -> tuple[int, int]:
    """Получить ширину и высоту конфигурации ивента"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(f"SELECT width, height FROM events_config WHERE event_id = {id_}")
        res = cur.fetchall()

        # Если конфигурации нет (получили None)
        if not res:
            return 0, 0

        return res[0]


def update_event_config(id_: int, places: list[list[str]]) -> None:
    """Обновить конфигурацию ивента"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE events_config SET places = ? WHERE event_id = ?",
                    (';'.join(';'.join(x) for x in places), id_))
        con.commit()


def get_cinemas_for_cashier(cashier: str):
    """Получить список кинотеатров, в которых работает кассир"""

    # Если не получили cashier
    if not cashier:
        return []

    res = []
    with sqlite3.connect(database_name) as conn:
        cur = conn.cursor()

        # Получаем список кинотеатров
        cinemas = [i[0] for i in cur.execute("SELECT cinema FROM data").fetchall()]

        # Для каждого кинотеатра получаем список пользователей
        for cinema in cinemas:
            users = cur.execute("SELECT users FROM data WHERE cinema = ?", (cinema,)).fetchall()

            # Если пользователей нет
            if not users or not users[0] or not users[0][0]:
                continue

            users = users[0][0].split(';')

            # Проверяем, есть ли пользователь в списке
            if cashier in users:
                res.append(cinema)
                continue
        return res


def add_report(report: str) -> None:
    """Добавить отчет о завершенном событии"""
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO reports (report) VALUES (?)", (report,))
        con.commit()

        # Идентификатор нового отчета
        id_ = cur.lastrowid

    try:
        os.listdir('reports')
    except FileNotFoundError:
        # Если не нашли папку с отчетами
        os.mkdir('reports')

    # Создаем txt файл с отчетом
    with open(f'reports/report_{id_}.txt', mode='w', encoding='utf-8') as f:
        f.write(report)
