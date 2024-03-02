from PyQt5.QtWidgets import QHBoxLayout, QWidget

from .view import View
from .settings_panel import SettingsPanel


class CentralWidget(QWidget):
    def __init__(self, graphics_view: View, settings_panel: SettingsPanel):
        super().__init__()

        self._graphics_view = graphics_view
        self._settings_panel = settings_panel

        self._layout = QHBoxLayout()

        self._init_ui()

    def _init_ui(self) -> None:
        self._layout.addWidget(self._graphics_view)
        self._layout.addWidget(self._settings_panel)

        self.setLayout(self._layout)
