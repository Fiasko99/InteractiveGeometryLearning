import math

import numpy as np

from .abstract_controllers import AbstractGraphicsController

__all__ = ["ThemeOneController"]


class ThemeOneController(AbstractGraphicsController):
    """Контроллер для первой темы."""

    @staticmethod
    def _build_vector(
        task_one_x_start=0, task_one_x_end=10, coefficient_deviation=1, upper=0
    ):
        """Создание вектора на основе формулы y=kx+b."""
        x = np.arange(task_one_x_start, task_one_x_end + 1)
        y = coefficient_deviation * x + upper
        return x, y

    def draw_first_example(self, *args, **kwargs):
        """Отрисовка превого примера."""
        if not kwargs["task_one_x_start"] < kwargs["task_one_x_end"]:
            return self._show_validate_error("X начала не может быть больше X конца.")
        points = self._build_vector(
            **kwargs
        )
        x1, x2 = points[0][0], points[0][-1]
        y1, y2 = points[1][0], points[1][-1]

        self.axes.plot(
            *points,
            label=f"d={np.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))}",
        )
        self.axes.legend(loc="best")

    def draw_second_example(self, *args, **kwargs):
        """Отрисовка второго примера."""
        k1 = 0
        k2 = kwargs["coefficient_deviation"]
        if k2 < 0:
            return self._show_validate_error(
                "Значение коэффициента отклонения не может быть меньше 0."
            )
        denominator = 1 + k1 * k2

        angle = 90 if denominator == 0 else math.atan((k2 - k1) / denominator)

        self.axes.plot(
            *self._build_vector(**kwargs),
            label=f"angle={round(math.degrees(angle), 1)}",
        )
        self.axes.set_ylim([0, 20])
        self.axes.legend(loc="best")
