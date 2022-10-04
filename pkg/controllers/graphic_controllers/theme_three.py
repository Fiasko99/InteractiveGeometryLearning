import math
from typing import List

import numpy as np
from matplotlib.patches import Circle

from .abstract_controllers import AbstractGraphicsController

__all__ = ["ThemeThreeController"]


class ThemeThreeController(AbstractGraphicsController):
    x: List[int]
    y: List[int]
    _point_counter: int = 0
    xs: List[float] = []
    ys: List[float] = []

    def __init__(self, axes):
        super().__init__(axes)
        self.line = None

    def __call__(self, event):
        """Функция для отлова события нажатия кнопок мыши на полотно canvas."""
        if event.dblclick is True:
            self._point_counter += 1
            # Если кнопка мыши была нажата дважды подряд
            # то функция добавит точку в датасет полотна
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)

        if self._point_counter == 4:
            # Если было нажато колесико мыши
            # то функция рисует ребра и диагонали для многоугольника
            points = [(x, y) for x, y in zip(self.xs, self.ys)]
            for x1, y1 in points:
                for x2, y2 in points:
                    self.axes.plot([x1, x2], [y1, y2], color="gray")
            self.axes.plot(self.xs, self.ys, color="blue")
            self.axes.plot(
                [self.xs[-1], self.xs[0]],
                [self.ys[-1], self.ys[0]],
                color="blue",
                label="Ребра",
            )
            self.xs, self.ys = [], []
            self._point_counter = 0

        # Нарисовать все созданные линии или точки при активации функции
        self.line.figure.canvas.draw()

    def draw_first_example(self, *args, **kwargs):
        # Находим все точки вершин треугольника
        x1 = kwargs["x1"]
        x2 = kwargs["x2"]
        x3 = kwargs["x3"]

        y1 = kwargs["y1"]
        y2 = kwargs["y2"]
        y3 = kwargs["y3"]

        x = [x1, x2, x3, x1]
        y = [y1, y2, y3, y1]

        # Вычисляем все длины линий относительно вершин треугольника
        len_lines = [
            np.sqrt(abs(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))),
            np.sqrt(abs(math.pow((x3 - x2), 2) + math.pow((y3 - y2), 2))),
            np.sqrt(abs(math.pow((x3 - x1), 2) + math.pow((y3 - y1), 2))),
        ]

        # Определяем центр вписанной окружности для конкретного треугольника
        y0 = (len_lines[1] * y1 + len_lines[2] * y2 + len_lines[0] * y3) / sum(
            len_lines
        )
        x0 = (len_lines[1] * x1 + len_lines[2] * x2 + len_lines[0] * x3) / sum(
            len_lines
        )

        # Определяем полупериметр и площадь для треугольника
        P = sum(len_lines) / 2
        # Определяем радиус вписанной окружности
        r = np.sqrt(((P - len_lines[0]) * (P - len_lines[1]) * (P - len_lines[2])) / P)
        S = P * r

        # Рисуем линии по указанным данным
        self.axes.plot(x, y)

        # Рисуем точку центра окружности
        self.axes.scatter(x0, y0, label=f"S={S}\nP={P*2}\nr={r}")

        # Рисуем саму вписанную окружность
        circle = Circle((x0, y0), r, fill=False)
        self.axes.add_patch(circle)
        self.axes.legend(loc="best")

    def draw_second_example(self, *args, **kwargs):
        # Создает новое полотно для рисования под нажатия кнопок мыши
        # Привязывает события кнопок мыши к полотну canvas
        self.line = None

        # Очищаем датасет с точками
        self.xs, self.ys = [], []
        (self.line,) = self.axes.plot([], [], marker="o", ms=10, ls="")

        # Тут происходит привязка событий мыши к полотну
        self.cid = self.line.figure.canvas.mpl_connect("button_press_event", self)
