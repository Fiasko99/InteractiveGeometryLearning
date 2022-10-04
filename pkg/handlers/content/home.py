from PyQt5.QtWidgets import QMainWindow

from pkg.gui.views import Ui_MainWindow
from pkg.handlers.paths import resource_path


class UiHomeWindowImpl(QMainWindow, Ui_MainWindow):
    """Класс для отрисовки окна `Главная`."""

    spa_app: ...

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.prev.clicked.connect(self.to_main)

    @staticmethod
    def __image_path_builder(image_name):
        return resource_path("assets", "images", image_name)

    def to_main(self):
        """Переход к окну `интерактивного обучения`."""
        from pkg.handlers.content.connector import Connector

        self.spa_app = Connector()
        self.spa_app.adjust_connection()
        self.spa_app.show()
        self.close()
