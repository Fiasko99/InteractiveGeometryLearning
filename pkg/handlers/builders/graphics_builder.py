from .abstract_builder import ABCBuilder

__all__ = ["GraphicsBuilder"]


class GraphicsBuilder(ABCBuilder):
    """
    Меняем префик для всех функций которые связанны с отрисовкой графиков на `draw`
    Пример:
        выбран пример 1 -> draw_first_example
    """

    callback_function_prefix = "draw_"
