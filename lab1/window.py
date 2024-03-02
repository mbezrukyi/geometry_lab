from PyQt5.QtWidgets import QMainWindow

from .central_widget import CentralWidget


class Window(QMainWindow):
    def __init__(self, central_widget: CentralWidget, title: str, width: int, height: int):
        super().__init__()

        self._central_widget = central_widget

        self.title = title
        self._width = width
        self._height = height

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle(self.title)
        self.setFixedSize(self._width, self._height)
        self.setCentralWidget(self._central_widget)
