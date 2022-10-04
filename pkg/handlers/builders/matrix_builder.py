from .abstract_builder import ABCBuilder

__all__ = ["MatrixBuilder"]


class MatrixBuilder(ABCBuilder):
    """Оставляем префик функций пустой.

    Пример:
        выбран пример 1 -> first_example
    """

    callback_function_prefix = ""
