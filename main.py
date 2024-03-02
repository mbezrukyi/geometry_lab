import sys
from lab1.config import load_config

from PyQt5.QtWidgets import QApplication

from lab1.central_widget import CentralWidget
from lab1.plot import Plot
from lab1.view import View
from lab1.scene import Scene
from lab1.settings_panel import SettingsPanel
from lab1.window import Window


def main() -> None:
    config = load_config('config.ini')

    app = QApplication(sys.argv)

    scene = Scene(Plot())
    view = View(scene)

    settings_panel = SettingsPanel(
        data_file_name=config.data.data_file_name,
        graphics_scene=scene
    )

    central_widget = CentralWidget(
        graphics_view=view,
        settings_panel=settings_panel
    )

    window = Window(
        central_widget=central_widget,
        title=config.window.title,
        width=config.window.width,
        height=config.window.height
    )

    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
