from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItem


class StandardItem(QStandardItem):
    """Стандартный элемент для tree-view (списка тем)."""

    def __init__(
        self, txt="", font_size=14, set_bold=False, color=QtGui.QColor(255, 255, 255)
    ):
        super().__init__()

        fnt = QtGui.QFont("Open Sans", font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
