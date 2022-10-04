__all__ = ["LineBuilder"]

import numpy
from scipy.spatial import Delaunay


class LineBuilder:
    """Класс для постройки точек на `plot`.

    Используется в 'интерактивных' примерах.

    _point_counter служит для автоматической отрисовки.
    """

    _point_counter: int

    def __init__(self, line):
        self._point_counter = 0
        self.line = line
        self.xs = []
        self.ys = []
        self.cid = line.figure.canvas.mpl_connect("button_press_event", self)

    def __call__(self, event):
        if event.inaxes != self.line.axes:
            return
        if event.button == 1:
            # Если нажата левая кнопка мыши, добавляем счетчику +1 и добавляем
            # координаты точки в массив.
            self._point_counter += 1
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            self.line.set_data(self.xs, self.ys)

        if self._point_counter == 3:
            # Когда нарисованно 3 точки, соединяем их.
            points = numpy.c_[self.xs, self.ys]
            tri = Delaunay(points)
            self.line.axes.triplot(points[:, 0], points[:, 1], tri.simplices.copy())
            self.line.figure.canvas.draw()
            self.__init__(self.line)
        self.line.figure.canvas.draw()
