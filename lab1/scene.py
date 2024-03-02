from PyQt5.QtWidgets import QGraphicsScene

from .plot import Plot


class Scene(QGraphicsScene):
    def __init__(self, plot: Plot):
        super().__init__()

        self._plot = plot

        self._init_ui()

    def _init_ui(self) -> None:
        self.addWidget(self._plot)

    def draw(self, *calculators) -> None:
        self._plot.plot(*calculators)

    def clear(self) -> None:
        self._plot.clear()
