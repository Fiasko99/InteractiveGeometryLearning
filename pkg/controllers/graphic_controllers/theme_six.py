import math

import numpy as np
from matplotlib.patches import Circle
from mpl_toolkits.mplot3d import art3d

from .abstract_controllers import Abstract3dController

__all__ = ["ThemeSixController"]


class ThemeSixController(Abstract3dController):
    height: int = 10
    radius: int = 5

    def _parse_args(self, **kwargs):
        """Получение аргументов из kwargs."""
        self.height, self.radius, = (
            kwargs.get("height", self.height),
            kwargs.get("radius", self.radius),
        )
        if self.radius < 0 or self.height < 0:
            self._show_validate_error("Радиус или высота не могут быть отрциательными.")
            return True

    def draw_first_example(self, *args, **kwargs):
        """Отрисовка превого примера."""
        self._plot_builder(self.__build_cylinder, **kwargs)

    def draw_second_example(self, *args, **kwargs):
        """Отрисовка второго примера."""
        self._plot_builder(self.__build_cone, **kwargs)

    def __build_cone(self):
        """Отрисовка конуса."""
        theta = np.linspace(0, 2 * np.pi, 25)
        r = np.linspace(0, self.radius, 25)
        t, R = np.meshgrid(theta, r)

        X = R * np.cos(t) + self.radius
        Y = R * np.sin(t) + self.radius
        Z = -R * 2.5 + self.height

        self.axes.plot_surface(X, Y, Z, alpha=0.8)
        self.axes.annotate(
            f"V={self.height/3 * np.pi * math.pow(self.radius, 2)}",
            xy=(-30, -15),
            xycoords="axes points",
            size=14,
            bbox=dict(boxstyle="round", fc="w"),
        )

    def __build_cylinder(self):
        """Отрисовка цилиндра."""
        color = "b"

        x_center = 0
        y_center = 0

        x = np.linspace(x_center - self.radius, x_center + self.radius, 16)
        z = np.linspace(0, self.height, 25)
        X, Z = np.meshgrid(x, z)

        Y = np.sqrt(self.radius ** 2 - (X - x_center) ** 2) + y_center

        self.axes.plot_surface(X, Y, Z, linewidth=0, color=color)
        self.axes.plot_surface(X, (2 * y_center - Y), Z, linewidth=0, color=color)

        floor = Circle((x_center, y_center), self.radius, color=color)
        self.axes.add_patch(floor)
        art3d.pathpatch_2d_to_3d(floor)

        ceiling = Circle((x_center, y_center), self.radius, color=color)
        self.axes.add_patch(ceiling)
        art3d.pathpatch_2d_to_3d(ceiling, z=self.height)
        self.axes.annotate(
            f"V={self.height * np.pi * math.pow(self.radius, 2)}",
            xy=(-30, -15),
            xycoords="axes points",
            size=14,
            bbox=dict(boxstyle="round", fc="w"),
        )
