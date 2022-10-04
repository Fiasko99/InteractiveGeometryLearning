__all__ = ["AbstractMatrixController"]

from abc import abstractmethod
from typing import List

import numpy as np
from PyQt5.QtWidgets import QLabel

from pkg.exceptions import NoMainArguments


class AbstractMatrixController:
    """Контроллер для матриц."""

    text_field_answer: QLabel

    def __init__(self, text_field_answer):
        """Записываем поле для ответа в аттрибуты класса.

        Если поля нет, вызываем ошибку.
        """
        if text_field_answer:
            self.text_field_answer = text_field_answer
        else:
            raise NoMainArguments(text_field_answer="text_field_answer")

    @abstractmethod
    def first_example(
        self, matrices: List[List[List[int]]] = None, *args, **kwargs
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def second_example(
        self, matrices: List[List[List[int]]] = None, *args, **kwargs
    ) -> None:
        raise NotImplementedError

    def fill_answer_area(self, array: np.ndarray, clear: bool = True) -> None:
        """Функция для заполенения поля ответа.

        :param array: Матрица.
        :param clear: Нужно ли очищать поле.
        """
        if clear:
            self.text_field_answer.clear()
        text = t + "\n\n" if (t := self.text_field_answer.text()) else ""
        text += "\n".join(
            ["".join(["{:4}".format(item) for item in row]) for row in array]
        )
        self.text_field_answer.setText(text)
