from functools import wraps

import numpy as np

__all__ = ["parse_matrix_from_kwargs"]


def parse_matrix_from_kwargs(_func=None, *, key_name: str = "widgets"):
    """Декоративная функция для преоброазования виджетов в значения матрицы.

    :param _func: Вызываемая функция.
    :param key_name: Наименоние ключа, значение которого являеются виджеты.
    """

    def _collector(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            """Функция для преоброазования виджетов в значения матрицы."""
            _func(
                matrices=[
                    np.array([[item.value() for item in row] for row in matrix])
                    for matrix in kwargs[key_name]
                ],
                *args,
                **kwargs
            )

        return inner

    if _func is None:
        return _collector
    else:
        return _collector(_func)
