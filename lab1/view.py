from PyQt5.QtWidgets import QGraphicsView

from .scene import Scene


class View(QGraphicsView):
    def __init__(self, graphics_scene: Scene):
        super().__init__(graphics_scene)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        zoom_factor = 1.25

        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1.0 / zoom_factor, 1.0 / zoom_factor)
