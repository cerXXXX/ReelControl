# -*- coding: utf-8 -*-
from MainClass import *
import sys


PYTHONPATH = "/.venv/Lib/site-packages"


def main():
    """Главная функция"""

    app = QtWidgets.QApplication(sys.argv)
    ui = MainClass()
    ui.setup_ui()
    ui.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
