from typing import List

import numpy as np

from .abstract_controller import AbstractMatrixController
from .handlers import parse_matrix_from_kwargs

__all__ = ["ThemeOneController"]


class ThemeOneController(AbstractMatrixController):
    @parse_matrix_from_kwargs
    def first_example(self, matrices: List[np.ndarray], *args, **kwargs) -> None:
        """Получаем все матрицы, проходим по ним циклом, суммируем каждый элемент."""
        buff = matrices[0]
        for matrix in matrices[1:]:
            buff += matrix
        self.fill_answer_area(buff)

    @parse_matrix_from_kwargs
    def second_example(self, matrices: List[np.ndarray], *args, **kwargs) -> None:
        """Получаем все матрицы, проходим по ним циклом, вычитаем каждый элемент."""
        buff = matrices[0]
        for matrix in matrices[1:]:
            buff -= matrix
        self.fill_answer_area(buff)
