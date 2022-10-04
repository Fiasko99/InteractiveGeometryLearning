import math

__all__ = ["ThemeFourController"]

from typing import Callable, List, Tuple

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from .abstract_controllers import Abstract3dController


class ThemeFourController(Abstract3dController):
    """Контроллер для четвертой темы."""
    height: int = 10

    x: int = 10
    y: int = 5
    z: int = 20

    A: Tuple[int, int, int]
    B: Tuple[int, int, int]
    C: Tuple[int, int, int]
    D: Tuple[int, int, int]
    E: Tuple[int, int, int]
    F: Tuple[int, int, int]
    G: Tuple[int, int, int]
    H: Tuple[int, int, int]

    def draw_first_example(self, *args, **kwargs):
        """Отрисовка первого примера."""
        self.__connector(self._build_diagonals, **kwargs)

    def draw_second_example(self, *args, **kwargs):
        """Отрисовка второго примера."""
        self.__connector(self._build_pyramid, **kwargs)

    def __show_vertex(self):
        """Отрсиовка наименований вершин фигуры."""
        for pos in list("abcdefgh".upper()):
            self.axes.text(
                *eval(f"self.{pos}"),  # nosec: B307
                s=pos,
                fontsize=18,
                color="darkgreen",
            )

    def __connector(self, example_function: Callable[[], None], **kwargs):
        """
            Функция для подключения функции с темой, отрисовки контура и
                отрисовки вершин.
        """
        self._plot_builder(example_function, **kwargs)
        self._build_circuit()
        self.__show_vertex()

    def __create_coordinates_for_diagonals(self, height: int):
        """Создание векторов для диагоналей."""
        x = self.__build_x_vector(height)
        y = self.__build_y_vector(height)
        z = self.__build_z_vector(height)
        self.__assign_vertices(x, y, z)

    def __create_coordinates_for_pyramid(self, x: int, z: int, y: int):
        """Создание векторов для пирамиды."""
        self.__assign_vertices(
            self.__build_x_vector(x), self.__build_y_vector(y), self.__build_z_vector(z)
        )

    @staticmethod
    def __build_x_vector(x: int) -> List[int]:
        """Создание массива, который отвечают за векторы по X"""
        return [x, x, x, x, 0, 0, 0, 0]

    @staticmethod
    def __build_y_vector(y: int) -> List[int]:
        """Создание массива, которые отвечают за векторы по Y"""
        return [0, y, y, 0, 0, y, y, 0]

    @staticmethod
    def __build_z_vector(z: int) -> List[int]:
        """Создание массива, которые отвечают за векторы по Z"""
        return [z, z, 0, 0, z, z, 0, 0]

    def __assign_vertices(self, x: List[int], y: List[int], z: List[int]):
        """Установка спресованного массива (см.zip) аттрибутам класса."""
        (
            self.A,
            self.B,
            self.C,
            self.D,
            self.E,
            self.F,
            self.G,
            self.H,
        ) = zip(x, y, z)

    def _parse_args(self, **kwargs):
        """Имплементация родительского метода для получения значений из kwargs."""
        self.height, self.x, self.y, self.z = (
            kwargs.get("height", self.height),
            kwargs.get("x", self.x),
            kwargs.get("y", self.y),
            kwargs.get("z", self.z),
        )
        if self.height < 0:
            self._show_validate_error("Высота не может быть отрицательной.")
            return True

    def _build_circuit(self):
        """Отрисовка граней по вершинам."""
        self.axes.plot3D(
            *zip(
                self.A,
                self.B,
                self.C,
                self.D,
                self.A,
                self.E,
                self.F,
                self.G,
                self.C,
                self.B,
                self.F,
                self.G,
                self.H,
                self.E,
                self.A,
                self.A,
                self.D,
                self.H,
                self.E,
            ),
            zdir="z",
            c="k",
            marker="o",
            mfc="r",
            mec="g",
            ms=10,
        )

    def _build_diagonals(self):
        """Отрисовка диагоналей."""
        self.__create_coordinates_for_diagonals(self.height)
        self.axes.plot(
            *zip(self.E, self.G),
            ls=":",
            label=f"d_{self.height}={round(self.height * math.sqrt(2), 2)}",
        )
        self.axes.legend(loc="best")
        self.axes.plot(
            *zip(self.H, self.B),
            ls=":",
            label=f"d_{self.height}={round(self.height * math.sqrt(3), 2)}",
        )
        self.axes.legend(loc="best")

    def _build_pyramid(self):
        """Отрисовка пирамиды."""
        self.__create_coordinates_for_pyramid(self.x, self.z, self.y)
        """Объединяем вершины."""
        self.axes.plot(*zip(self.D, self.E), color="red")
        self.axes.plot(*zip(self.D, self.G), color="red")
        self.axes.plot(*zip(self.D, self.B), color="red")
        self.axes.plot(*zip(self.G, self.E), color="red")
        self.axes.plot(*zip(self.E, self.B), color="red")
        """Производим расчеты объема."""
        self.axes.plot(
            *zip(self.B, self.G),
            color="red",
            label=f"V[{self.x};{self.y};{self.z}]"
            f"={round((self.x * self.y * self.z) / 3, 3)}",
        )
        """Создаем куб."""
        self.axes.add_collection3d(
            Poly3DCollection(
                [
                    self.E,
                    self.G,
                    self.D,
                    self.E,
                    self.B,
                    self.D,
                    self.B,
                    self.G,
                    self.E,
                    self.B,
                    self.D,
                    self.G,
                ],
                facecolors="cyan",
                linewidths=1,
                edgecolors="r",
                alpha=0.25,
            )
        )
        self.axes.legend(loc="best")
