from PyQt5 import QtWidgets

__all__ = ["Application"]

from pkg.handlers.content.home import UiHomeWindowImpl


class Application:
    """Точка входа для приложения."""

    @staticmethod
    def run():
        import sys

        app = QtWidgets.QApplication(sys.argv)
        window = UiHomeWindowImpl()
        window.show()
        app.exec_()

    ...
