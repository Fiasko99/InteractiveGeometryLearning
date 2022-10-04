import math

__all__ = ["ThemeFiveController"]

from itertools import combinations, product
from typing import List, Tuple

import numpy
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .abstract_controllers import Abstract3dController


class ThemeFiveController(Abstract3dController):
    """Класс контроллер для пятой темы."""

    height: float = 10
    volume: float = 30
    width: float = 1

    rib_length: float = 10
    radius: float = 5

    A: Tuple[float, float, float]
    B: Tuple[float, float, float]
    C: Tuple[float, float, float]
    D: Tuple[float, float, float]
    E: Tuple[float, float, float]

    def draw_first_example(self, *args, **kwargs):
        """Отрисовка первого примера"""
        self._plot_builder(self._build_pyramid, **kwargs)

    def draw_second_example(self, *args, **kwargs):
        """Отрисовка второго примера"""
        self._plot_builder(self._build_cube_with_sphere, **kwargs)

    def __create_coordinates_for_pyramid(self):
        """Создание вершин пирамиды."""
        self.width = self.__calculate_parties(self.height, self.volume)
        self.__assign_vertices(
            self.__build_x_vector(self.width),
            self.__build_y_vector(self.width),
            self.__build_z_vector(self.height),
        )

    @staticmethod
    def __calculate_parties(height, volume) -> float:
        """Вычисление стороны на основании высоты и оъема."""
        return math.sqrt(3 * volume / height)

    @staticmethod
    def __build_x_vector(x: float) -> List[float]:
        """Создание массива, которые отвечают за векторы по X"""
        return [0, x, x, 0, x / 2]

    @staticmethod
    def __build_y_vector(y: float) -> List[float]:
        """Создание массива, которые отвечают за векторы по Y"""
        return [0, 0, y, y, y / 2]

    @staticmethod
    def __build_z_vector(z: float) -> List[float]:
        """Создание массива, которые отвечают за векторы по Z"""
        return [0, 0, 0, 0, z]

    def __assign_vertices(self, x: List[float], y: List[float], z: List[float]):
        """Установка спресованного массива (см.zip) аттрибутам класса."""
        self.A, self.B, self.C, self.D, self.E = zip(x, y, z)

    def _parse_args(self, **kwargs) -> bool:
        """Имплементация родительского метода для получения значений из kwargs."""
        self.height, self.volume, self.width, self.radius, self.rib_length = (
            kwargs.get("height", self.height),
            kwargs.get("volume", self.volume),
            kwargs.get("radius", self.width),
            kwargs.get("radius", self.radius),
            kwargs.get("rib_length", self.rib_length),
        )
        if self.height < 0 or self.volume < 0:
            self._show_validate_error("Высота или объем не могут быть отрицательными.")
            return True
        if self.radius < 0 or self.rib_length < 0:
            self._show_validate_error(
                "Радиус или длина ребра не могут быть отрицательными."
            )
            return True

    def _build_cube_with_sphere(self):
        """Отрисовка сферы в кубе."""
        self.__build_cube()
        self.__build_sphere()
        self.axes.annotate(
            f"V={math.pow(self.rib_length, 3) - 4/3*np.pi*math.pow(self.radius, 3)}",
            xy=(-30, -15),
            xycoords="axes points",
            size=14,
            bbox=dict(boxstyle="round", fc="w"),
        )

    def __build_sphere(self):
        """Создание сферы."""
        # fmt: off
        u, v = np.mgrid[0: 2 * np.pi: 20j, 0: np.pi: 10j]
        # fmt: on
        center_offset = self.rib_length / 2
        x = np.cos(u) * np.sin(v) * self.radius + center_offset
        y = np.sin(u) * np.sin(v) * self.radius + center_offset
        z = np.cos(v) * self.radius + center_offset
        self.axes.plot_wireframe(x, y, z)

    def __build_cube(self):
        """Создание куба."""
        r = [0, self.rib_length]
        for s, e in combinations(np.array(list(product(r, r, r))), 2):
            if np.sum(np.abs(s - e)) == r[1] - r[0]:
                self.axes.plot3D(*zip(s, e), color="b")

    def _build_pyramid(self):
        """Создание пирамиды используя последовательное соединение вершин."""
        self.__create_coordinates_for_pyramid()
        v = numpy.array([self.A, self.B, self.C, self.D, self.E])
        self.axes.scatter3D(v[:, 0], v[:, 1], v[:, 2])
        self.axes.add_collection3d(
            Poly3DCollection(
                [
                    [self.A, self.B, self.E],
                    [self.A, self.D, self.E],
                    [self.C, self.B, self.E],
                    [self.C, self.D, self.E],
                    [self.A, self.B, self.C, self.D],
                ],
                linewidths=1,
                edgecolors="r",
                alpha=0.25,
            )
        )

        """Установка наименований вершин"""
        for pos in list("abcde".upper()):
            self.axes.text(
                *eval(f"self.{pos}"),  # nosec: B307
                s=pos,
                fontsize=18,
                color="darkgreen",
            )
