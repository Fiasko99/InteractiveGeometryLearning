import math

from scipy.spatial.qhull import QhullError

from .abstract_controllers import AbstractGraphicsController

__all__ = ["ThemeTwoController"]

from ...handlers.mplt import LineBuilder


class ThemeTwoController(AbstractGraphicsController):
    """Контроллер для второй темы."""
    def draw_first_example(self, *args, **kwargs):
        """Отрисовка превого примера."""
        x = [0, kwargs["x"], 0]
        y = [0, 0, kwargs["y"]]
        vx, vy = kwargs["x"], kwargs["y"]
        P = vx + vy + math.sqrt(pow(vx, 2) + pow(vy, 2))
        S = vx * vy / 2
        self.axes.fill(x, y, label=f"P={P} S={S}")
        self.axes.legend(loc="best")

    def draw_second_example(self, *args, **kwargs):
        """Отрисовка второго примера."""
        (line,) = self.axes.plot([], [], marker="o", ms=10, ls="")  # empty line
        try:
            LineBuilder(line)
        except QhullError:
            LineBuilder(line)
