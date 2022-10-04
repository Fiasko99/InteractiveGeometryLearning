from abc import ABC, abstractmethod
from typing import Callable

from ...exceptions import NoMainArguments

__all__ = ["AbstractGraphicsController", "Abstract3dController"]

from ...handlers.message import show_input_value_error


class AbstractGraphicsController:
    """Контроллер для графиков."""

    axes = ...

    def __init__(self, axes):
        if axes:
            self.axes = axes
        else:
            raise NoMainArguments(axes="axes")

    @abstractmethod
    def draw_first_example(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def draw_second_example(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def _show_validate_error(message: str) -> None:
        return show_input_value_error(message)



class Abstract3dController(AbstractGraphicsController, ABC):
    """Контроллер для отрисовки 3д задач."""

    def _plot_builder(self, function: Callable[[], None], **kwargs):
        """Установка возможности вращать 3д фигуры, установка надписей осей
        координат."""
        if self._parse_args(**kwargs):
            return
        self.axes.mouse_init()

        function()

        self.axes.set(
            xlabel="X",
            ylabel="Y",
            zlabel="Z",
        )

    @abstractmethod
    def _parse_args(self, **kwargs):
        """Установка переменных в качестве аттрибутов класса из kwargs."""
        raise NotImplementedError
