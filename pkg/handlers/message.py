from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox


def show_input_value_error(message: str) -> None:
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(message)
    msg.setWindowTitle("Внимание!")
    msg.exec_()
