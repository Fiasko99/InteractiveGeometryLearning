import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QSizePolicy

matplotlib.use("Qt5Agg")
__all__ = ["MplCanvas"]


class MplCanvas(FigureCanvas):
    """Создает холст matplotlib."""

    toolbar: NavigationToolbar2QT

    def __init__(self, parent=None, width=5, height=5, dpi=1, td=False):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = (
            fig.add_subplot(111, projection="3d") if td else fig.add_subplot(111)
        )
        FigureCanvas.__init__(self, fig)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.parent = parent
        super(MplCanvas, self).__init__(fig)
        self.setFixedSize(700, 500)

    def create_toolbar(self):
        """Подключает к хослту тулбар."""
        self.toolbar = NavigationToolbar2QT(self, self.parent)
        self.toolbar.update()
        return self.toolbar
